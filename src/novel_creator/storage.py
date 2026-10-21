"""Local exchange transaction: private candidate index, conditional ref publication.

Only a published local branch commit is authority. Pending files/receipts are not.
The lock serializes this tool, not arbitrary external Git operations.
"""
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid

from . import records, validation, validation_cache
from .cli import ToolError


UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
BUNDLE = re.compile(r'^story/exchanges/[0-9]{6,}-' + UUID + r'\.json$')


def git(root, *args, env=None, input=None, check=True):
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment.update({'GIT_TERMINAL_PROMPT': '0', 'GIT_CONFIG_NOSYSTEM': '1'})
    if env:
        environment.update(env)
    result = subprocess.run(['git', '-C', str(root), *args], env=environment,
                            input=input, capture_output=True)
    if check and result.returncode:
        # Avoid leaking story contents or config via Git diagnostics.
        raise ToolError(5, 'Local Git operation failed')
    return result.stdout if check else result


def head(root):
    result = git(root, 'rev-parse', '--verify', 'HEAD', check=False)
    return result.stdout.decode().strip() if result.returncode == 0 else None


def branch(root):
    result = git(root, 'symbolic-ref', '--quiet', 'HEAD', check=False)
    value = result.stdout.decode().strip()
    if result.returncode or not value.startswith('refs/heads/'):
        raise ToolError(3, 'A checked-out local branch is required')
    return value


def root_path(root):
    path = Path(root).absolute()
    if '..' in path.parts or path.resolve() != path:
        raise ToolError(2, 'Symlink or traversing novel root is not allowed')
    actual = git(path, 'rev-parse', '--show-toplevel').decode().strip()
    if Path(actual).resolve() != path:
        raise ToolError(3, 'Novel must be an independent Git root')
    gitdir = path / '.git'
    if not gitdir.is_dir() or gitdir.is_symlink():
        raise ToolError(3, 'Linked worktrees and redirected Git directories are unsupported')
    return path


def safe_path(root, relative, *, setup=False, _regular_leaf=False):
    """Allow only fixed managed locations; check each existing path component."""
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or '..' in path.parts or '\\' in relative or
        str(path) != relative or any(c in relative for c in ('\x00', '\n', '\r'))):
        raise ToolError(2, 'Invalid managed path')
    allowed = (BUNDLE.fullmatch(relative) or relative.startswith('.novel-creator/local/') or
               relative == '.novel-creator/manifest.json')
    if setup:
        allowed = allowed or (relative in ('.gitignore', '.gitattributes', 'AGENTS.md') or
                    relative.startswith(('.novel-creator/src/', '.novel-creator/schemas/',
                     '.novel-creator/workflows/', '.novel-creator/languages/')) or
                    relative == '.novel-creator/run.py' or
                    bool(re.fullmatch(r'\.agents/skills/novel-[a-z-]+/SKILL\.md', relative)))
    if not allowed:
        raise ToolError(2, 'Write is outside the managed allowlist')
    current = os.fspath(root)
    parts = path.parts
    for index, part in enumerate(parts):
        current = os.path.join(current, part)
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            if _regular_leaf and index == len(parts) - 1:
                raise ToolError(3, 'Managed file is missing or has an unsafe mode')
            continue
        if stat.S_ISLNK(mode):
            raise ToolError(2, 'Symlink in managed path')
        if _regular_leaf and index == len(parts) - 1 and not stat.S_ISREG(mode):
            raise ToolError(3, 'Managed file is missing or has an unsafe mode')
    return Path(current)


def bundle_path(bundle):
    try:
        identifier = str(uuid.UUID(bundle['exchange_id']))
        sequence = bundle['sequence']
        if identifier != bundle['exchange_id'] or type(sequence) is not int or sequence < 1:
            raise ValueError()
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise ToolError(2, 'Invalid exchange identity') from error
    return f'story/exchanges/{sequence:06d}-{identifier}.json'


def checkpoint(root, history=None, commit=None):
    history = read_history(root) if history is None else history
    latest = history[-1] if history else None
    return {'git_head': commit or head(root),
            'exchange_id': latest['exchange_id'] if latest else None,
            'sequence': latest['sequence'] if latest else 0}


def committed_entries(root, commit):
    if not commit:
        return {}
    entries = {}
    for line in git(root, 'ls-tree', '-rz', commit).split(b'\0'):
        if not line:
            continue
        meta, path = line.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        entries[path.decode('utf-8')] = (mode, oid)
    return entries


def _prefix_checkpoint(root, history, commit, entries):
    """Name a verified journal prefix without labeling a damaged tree confirmed."""
    if not history:
        return None
    latest = history[-1]
    confirmed = {'git_head': None, 'exchange_id': latest['exchange_id'], 'sequence': latest['sequence']}
    try:
        candidate = git(root, 'log', '-1', '--format=%H', commit, '--', bundle_path(latest)).decode().strip()
        candidate_entries = {path: entry for path, entry in committed_entries(root, candidate).items()
                             if path.startswith('story/exchanges/')}
        expected = {bundle_path(item): entries[bundle_path(item)] for item in history}
        if candidate and candidate_entries == expected:
            confirmed['git_head'] = candidate
    except ToolError:
        # The validated prefix is still known even if its historical snapshot is unavailable.
        pass
    return confirmed


def _batch_blobs(root, entries, paths):
    """One snapshot-bound Git request, with binary lengths and per-path failures."""
    if not paths:
        return
    result = git(root, 'cat-file', '--batch', input=''.join(entries[p][1] + '\n' for p in paths).encode(), check=False)
    stream = io.BytesIO(result.stdout)
    for path in paths:
        try:
            header = stream.readline().decode('ascii').strip().split()
            if len(header) != 3 or header[0] != entries[path][1] or header[1] != 'blob':
                raise ValueError('Unavailable blob')
            size = int(header[2])
            if size < 0:
                raise ValueError('Invalid blob size')
            raw = stream.read(size)
            if len(raw) != size or stream.read(1) != b'\n':
                raise ValueError('Truncated blob')
            yield path, raw
        except (UnicodeError, ValueError):
            yield path, ToolError(4, 'Committed exchange blob is unavailable', affected_refs=[path])


def read_history(root, commit=None):
    return read_snapshot(root, commit)[0]


def read_snapshot(root, commit=None):
    """Return the validated prefix and its ephemeral indexes from one Git tree."""
    root = Path(root)
    commit = commit or head(root)
    history = []
    chain = validation.ExchangeValidator()
    entries = committed_entries(root, commit)
    certified = validation_cache.trusted(root, commit, entries)
    chain.cache_hit = certified
    paths = sorted(p for p in entries if p.startswith('story/exchanges/'))
    for path, raw in _batch_blobs(root, entries, paths):
        try:
            if not BUNDLE.fullmatch(path) or entries[path][0] != '100644':
                raise ToolError(4, 'Invalid committed exchange path or file mode', affected_refs=[path])
            if isinstance(raw, ToolError):
                raise raw
            if certified:
                oid = entries[path][1]
                algorithm = 'sha256' if len(oid) == 64 else 'sha1'
                actual = hashlib.new(algorithm, b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
                if actual != oid:
                    raise ToolError(4, 'Committed exchange object hash differs from validated snapshot', affected_refs=[path])
                value = json.loads(raw)
            else:
                value = records.loads(raw)
            if not isinstance(value, dict):
                raise ValueError('Exchange must be an object')
            if value.get('schema_version') != '1.0':
                raise ToolError(4, 'Unsupported exchange schema', affected_refs=[path])
            if bundle_path(value) != path:
                raise ValueError('Exchange filename mismatch')
            if certified:
                chain._append_certified(value)
            else:
                chain._append_owned(value)
        except (ToolError, ValueError, TypeError, KeyError) as cause:
            error = cause if isinstance(cause, ToolError) else ToolError(4, 'Committed exchange context is unreadable')
            error.affected_refs = error.affected_refs or [path]
            error.checkpoint = _prefix_checkpoint(root, history, commit, entries)
            if error is cause:
                raise
            raise error from cause
        history.append(value)
    if not certified:
        validation_cache.remember(root, commit, entries)
    return history, chain


def read_receipt(root, path):
    """Treat malformed local recovery metadata as unavailable, never as success."""
    relative = path.relative_to(root).as_posix()
    safe_path(root, relative)
    try:
        value = records.loads(path.read_bytes())
        if (not isinstance(value, dict) or value.get('state') not in ('pending', 'published') or
            not isinstance(value.get('bundle'), dict) or
            not isinstance(value.get('branch'), str) or
            not isinstance(value.get('paths'), list) or
            not all(isinstance(item, str) for item in value['paths']) or
            not isinstance(value.get('baseline_index'), str) or
            type(value.get('cleanup_required')) is not bool):
            raise ValueError('Invalid recovery receipt')
    except (ValueError, TypeError) as error:
        raise ToolError(4, 'Local recovery metadata is unreadable', affected_refs=[relative]) from error
    return value


def fsync_directory(path):
    if os.name == 'nt':
        return  # Durability on Windows requires a separate real filesystem evaluation.
    descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp = tempfile.mkstemp(prefix='prepare-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        fsync_directory(path.parent)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextmanager
def writer_lock(root, *, pending=None):
    local = safe_path(root, '.novel-creator/local/write.lock')
    local.parent.mkdir(parents=True, exist_ok=True)
    try:
        local.mkdir()
    except FileExistsError as error:
        confirmed, affected = None, []
        try:
            # Readers can inspect an immutable committed snapshot without owning
            # the writer lock. Capture HEAD once so a competing save cannot mix trees.
            initial = head(root)
            if initial is not None:
                history = read_history(root, initial)
                confirmed = checkpoint(root, history, initial)
        except ToolError as unavailable:
            confirmed, affected = unavailable.checkpoint, unavailable.affected_refs
        except (OSError, UnicodeError):
            pass  # No checkpoint can be claimed when inspection itself is unavailable.
        raise ToolError(6, 'Novel writer lock held; inspect recovery before removal',
                        checkpoint=confirmed, pending=pending, affected_refs=affected) from error
    try:
        (local / 'owner.json').write_text(json.dumps({'pid': os.getpid()}), encoding='utf-8')
        yield
    finally:
        active_error = sys.exc_info()[0] is not None
        try:
            (local / 'owner.json').unlink(missing_ok=True)
            local.rmdir()
        except OSError:
            # Never replace the original conflict/save error with a cleanup error.
            if not active_error:
                raise


def index_entries(root, paths):
    return git(root, 'ls-files', '--stage', '-z', '--', *paths)


def check_managed(root, commit, paths):
    entries = committed_entries(root, commit)
    indexed = {}
    for entry in index_entries(root, []).split(b'\0'):
        if entry:
            _, path_bytes = entry.split(b'\t', 1)
            path = path_bytes.decode('utf-8')
            indexed[path] = indexed.get(path, b'') + entry + b'\0'
    managed = []
    for path, (mode, oid) in entries.items():
        if path.startswith(('story/exchanges/', '.novel-creator/')) and not path.startswith('.novel-creator/local/'):
            target = safe_path(root, path, setup=True, _regular_leaf=True)
            if mode != '100644':
                raise ToolError(3, 'Managed file is missing or has an unsafe mode')
            baseline = f'100644 {oid} 0\t{path}\0'.encode()
            if indexed.get(path, b'') != baseline:
                raise ToolError(3, 'Managed index entry changed outside the transaction')
            managed.append((target, oid))
    if managed:
        # Git's native reader avoids Python open() overhead for every file while
        # hashing every byte, including same-size/mtime edits. C quoting protects
        # spaces, quotes and non-ASCII paths in the stdin-paths protocol.
        payload = ''.join(json.dumps(target.as_posix(), ensure_ascii=False) + '\n' for target, _ in managed).encode()
        hashes = git(root, 'hash-object', '--no-filters', '--stdin-paths', input=payload).decode().splitlines()
        if len(hashes) != len(managed):
            raise ToolError(5, 'Managed file hashing returned an incomplete result')
        if any(current != oid for current, (_, oid) in zip(hashes, managed)):
            raise ToolError(3, 'Managed working file changed outside the exchange transaction')
    for path in paths:
        if path in entries:
            raise ToolError(3, 'Exchange path already exists in confirmed history')
        if indexed.get(path, b''):
            raise ToolError(3, 'New managed exchange has incompatible staged contents')


def sync_index(root, paths, baseline, commit):
    """Merge only managed entries while holding the real Git index lock."""
    index = root / '.git/index'
    lock = root / '.git/index.lock'
    if index.is_symlink() or lock.is_symlink():
        raise OSError('Unsafe Git index path')
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        if index_entries(root, paths) != baseline:
            raise OSError('Managed index entries changed concurrently')
        with os.fdopen(descriptor, 'wb') as stream:
            descriptor = None
            if index.exists():
                stream.write(index.read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        if not index.exists():
            # Keep the real index lock held while preparing a valid empty index.
            with tempfile.TemporaryDirectory(dir=root / '.novel-creator/local') as temp:
                temporary = str(Path(temp) / 'empty-index')
                git(root, 'read-tree', '--empty', env={'GIT_INDEX_FILE': temporary})
                lock.write_bytes(Path(temporary).read_bytes())
        entries = committed_entries(root, commit)
        payload = b''.join(f'{entries[p][0]} {entries[p][1]} 0\t{p}\0'.encode() for p in paths)
        git(root, 'update-index', '-z', '--index-info', input=payload, env={'GIT_INDEX_FILE': str(lock)})
        # Windows FlushFileBuffers requires write access; a read-only descriptor
        # makes an otherwise published save permanently need index recovery.
        with lock.open('r+b') as stream:
            os.fsync(stream.fileno())
        os.replace(lock, index)
        fsync_directory(index.parent)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        lock.unlink(missing_ok=True)


def success(bundle, commit, *, already=False, cleanup=False, warnings=None):
    return {'ok': True, 'operation': 'exchange.save', 'novel_id': bundle['novel_id'],
            'data': {'saved': True, 'already_saved': already, 'cleanup_required': cleanup},
            'warnings': warnings or [], 'checkpoint': {'git_head': commit,
             'exchange_id': bundle['exchange_id'], 'sequence': bundle['sequence']}}


def _save(root, bundle, *, fault=None):
    fault = fault or (lambda point: None)
    root = root_path(root)
    path = bundle_path(bundle)
    final = safe_path(root, path)
    confirmed = None
    pending_id = bundle['exchange_id']
    published = None
    receipt = safe_path(root, f'.novel-creator/local/{pending_id}.json')
    with writer_lock(root, pending=pending_id):
        try:
            reference = branch(root)
            initial = head(root)
            history, chain = read_snapshot(root, initial)
            confirmed = checkpoint(root, history, initial)
            for old in history:
                if old['exchange_id'] == pending_id:
                    if old != bundle or records.digest(bundle) != old['payload_digest']:
                        raise ToolError(3, 'Exchange ID was already saved with a different payload')
                    commit = git(root, 'log', '-1', '--format=%H', initial, '--', path).decode().strip()
                    local_state = read_receipt(root, receipt) if receipt.exists() else {}
                    cleanup = bool(local_state) and (local_state.get('state') != 'published' or local_state.get('cleanup_required', True))
                    retry_paths = [path]
                    if bundle['expected_git_head'] is None:
                        manifest = records.loads(git(root, 'show', commit + ':.novel-creator/manifest.json'))
                        retry_paths += ['.novel-creator/manifest.json', '.gitignore'] + manifest.get('managed_paths', [])
                    saved_entries = committed_entries(root, commit)
                    expected_index = b''.join(f'{saved_entries[p][0]} {saved_entries[p][1]} 0\t{p}\0'.encode()
                                              for p in sorted(set(retry_paths)))
                    cleanup = cleanup or index_entries(root, sorted(set(retry_paths))) != expected_index
                    return success(old, commit, already=True, cleanup=cleanup,
                                   warnings=['Managed index recovery required'] if cleanup else [])
            # Incomplete/published cleanup and failed saves pause unrelated writes.
            for local in receipt.parent.glob('*.json'):
                if local != receipt:
                    state = read_receipt(root, local)
                    if state.get('cleanup_required') or state.get('state') == 'pending':
                        raise ToolError(3, 'Prior transaction requires recovery before further saves')
            if bundle.get('expected_git_head') != initial:
                raise ToolError(3, 'Stale expected Git checkpoint',
                                expected_head=bundle.get('expected_git_head'), actual_head=initial)
            if bundle.get('schema_version') != '1.0':
                raise ToolError(4, 'Unsupported exchange schema')
            chain.append(bundle)
            manifest_path = safe_path(root, '.novel-creator/manifest.json')
            manifest = records.loads(manifest_path.read_bytes())
            if manifest.get('novel_id') != bundle['novel_id']:
                raise ToolError(3, 'Exchange belongs to another novel')
            paths = [path]
            if initial is None:
                paths += ['.novel-creator/manifest.json', '.gitignore'] + manifest.get('managed_paths', [])
            paths = sorted(set(paths))
            for managed in paths:
                safe_path(root, managed, setup=True)
            check_managed(root, initial, paths)
            baseline = index_entries(root, paths)
            if receipt.exists():
                previous = read_receipt(root, receipt)
                if previous.get('bundle') != bundle or previous.get('branch') != reference:
                    raise ToolError(3, 'Pending transaction identity or payload changed')
            state = {'state': 'pending', 'bundle': bundle, 'branch': reference,
                     'expected_head': initial, 'paths': paths, 'baseline_index': baseline.decode(),
                     'cleanup_required': False}
            atomic_json(receipt, state)
            fault('before_file')
            final.parent.mkdir(parents=True, exist_ok=True)
            if final.exists():
                if records.loads(final.read_bytes()) != bundle:
                    raise ToolError(3, 'Pending exchange contents changed')
            else:
                # The novel writer lock excludes cooperating writers. Exclusive
                # create prevents replacing an external file at the same name.
                descriptor, temporary = tempfile.mkstemp(dir=final.parent, prefix='prepare-')
                try:
                    raw = (json.dumps(bundle, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
                    with os.fdopen(descriptor, 'wb') as stream:
                        stream.write(raw)
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.link(temporary, final)
                    fsync_directory(final.parent)
                finally:
                    os.unlink(temporary)
            fault('after_file')
            with tempfile.TemporaryDirectory(dir=receipt.parent, prefix='candidate-') as directory:
                environment = {'GIT_INDEX_FILE': str(Path(directory) / 'index')}
                git(root, 'read-tree', initial if initial else '--empty', env=environment)
                for managed in paths:
                    target = safe_path(root, managed, setup=True)
                    oid = git(root, 'hash-object', '-w', '--no-filters', '--', str(target)).decode().strip()
                    git(root, 'update-index', '--add', '--cacheinfo', f'100644,{oid},{managed}', env=environment)
                tree = git(root, 'write-tree', env=environment).decode().strip()
                arguments = ['commit-tree', tree, '-m', 'Save story exchange ' + pending_id]
                if initial:
                    arguments += ['-p', initial]
                candidate = git(root, *arguments).decode().strip()
            changes = (git(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', initial, candidate)
                       if initial else git(root, 'ls-tree', '-r', '--name-only', candidate))
            if set(changes.decode().splitlines()) != set(paths):
                raise ToolError(5, 'Candidate delta contains unexpected paths')
            parents = git(root, 'rev-list', '--parents', '-n', '1', candidate).decode().split()[1:]
            if parents != ([initial] if initial else []):
                raise ToolError(5, 'Candidate parent differs from expected checkpoint')
            candidate_bundle = records.loads(git(root, 'show', candidate + ':' + path))
            if candidate_bundle != bundle or records.digest(candidate_bundle) != bundle['payload_digest']:
                raise ToolError(5, 'Candidate exchange failed digest verification')
            state['candidate'] = candidate
            atomic_json(receipt, state)
            fault('after_candidate')
            fault('before_ref')
            if branch(root) != reference:
                raise ToolError(3, 'Checked-out branch changed during save')
            # Recheck managed worktree and index after external preparation/race.
            check_managed(root, initial, paths)
            candidate_entries = committed_entries(root, candidate)
            for managed in paths:
                target = safe_path(root, managed, setup=True)
                working_oid = git(root, 'hash-object', '--no-filters', '--', str(target)).decode().strip()
                if working_oid != candidate_entries[managed][1]:
                    raise ToolError(3, 'Managed input changed after candidate construction')
            result = git(root, 'update-ref', reference, candidate, initial or '0' * len(candidate), check=False)
            if result.returncode:
                actual = head(root)
                if actual != initial:
                    raise ToolError(3, 'Git branch advanced before conditional publication',
                                    expected_head=initial, actual_head=actual)
                raise ToolError(5, 'Git conditional publication failed')
            published = candidate
            # The pending receipt already contains candidate and baseline; it is
            # enough for recovery even if every subsequent filesystem write fails.
            state.update(state='published', cleanup_required=True)
            try:
                atomic_json(receipt, state)
                fault('after_ref')
                fault('before_cleanup')
                if branch(root) != reference or head(root) != candidate:
                    raise OSError('Branch changed after publication')
                sync_index(root, paths, baseline, candidate)
                state['cleanup_required'] = False
                fault('before_receipt')
                atomic_json(receipt, state)
                validation_cache.remember(root, candidate, candidate_entries)
                return success(bundle, candidate)
            except (OSError, ToolError):
                return success(bundle, candidate, cleanup=True, warnings=['Saved; managed index recovery required'])
        except ToolError as error:
            if confirmed is not None:
                error.checkpoint = confirmed
            error.pending = pending_id
            raise
        except (ValueError, TypeError, KeyError) as error:
            raise ToolError(2, 'Invalid exchange data or references', checkpoint=confirmed, pending=pending_id) from error
        except OSError as error:
            if published:
                return success(bundle, published, cleanup=True, warnings=['Saved; managed index recovery required'])
            raise ToolError(5, 'Exchange save failed; pending work is not confirmed', checkpoint=confirmed, pending=pending_id) from error


def save(root, bundle, *, fault=None):
    """Keep the commit point truthful even when releasing the writer lock fails."""
    try:
        return _save(root, bundle, fault=fault)
    except OSError as error:
        # A context-manager cleanup occurs after the transaction has returned.
        # Resolve authority from Git, never from the presence of a local receipt.
        try:
            confirmed = read_history(root)
            for old in confirmed:
                if old == bundle:
                    commit = git(root, 'log', '-1', '--format=%H', 'HEAD', '--', bundle_path(old)).decode().strip()
                    receipt = safe_path(Path(root), f".novel-creator/local/{old['exchange_id']}.json")
                    if receipt.exists():
                        try:
                            state = read_receipt(Path(root), receipt)
                            state.update(cleanup_required=True, lock_cleanup_required=True)
                            atomic_json(receipt, state)
                        except (OSError, ValueError, ToolError):
                            pass
                    return success(old, commit, cleanup=True,
                                   warnings=['Saved; writer lock cleanup requires recovery'])
        except (ToolError, OSError, ValueError, TypeError):
            pass
        raise ToolError(5, 'Writer lock cleanup failed; inspect recovery',
                        pending=bundle.get('exchange_id') if isinstance(bundle, dict) else None) from error


def recover(root, exchange_id, *, retry=False, expected_head=None):
    """Inspect freely; retry publishes unchanged work or finishes managed cleanup.

    Never remove a writer lock, reset a ref, or replay a published bundle.
    """
    root = root_path(root)
    try:
        if str(uuid.UUID(exchange_id)) != exchange_id:
            raise ValueError()
    except (ValueError, TypeError, AttributeError) as error:
        raise ToolError(2, 'Recovery requires an exchange UUID') from error
    initial = head(root)
    history = read_history(root, initial)
    confirmed = checkpoint(root, history, initial)
    receipt_path = safe_path(root, f'.novel-creator/local/{exchange_id}.json')
    receipt = read_receipt(root, receipt_path) if receipt_path.exists() else None
    bundle = next((b for b in history if b['exchange_id'] == exchange_id), None)
    published = bundle is not None
    if bundle is None and receipt:
        bundle = receipt['bundle']
        try:
            if bundle['exchange_id'] != exchange_id:
                raise ValueError('Receipt identity mismatch')
            validation.validate_exchange(bundle, history)
        except (ValueError, TypeError, KeyError) as error:
            raise ToolError(4, 'Pending payload is unavailable', checkpoint=confirmed, pending=exchange_id) from error
    if bundle is None:
        raise ToolError(4, 'No saved or pending exchange with this identity', checkpoint=confirmed)
    paths = [bundle_path(bundle)]
    saved_commit = None
    if published:
        saved_commit = git(root, 'log', '-1', '--format=%H', initial, '--', paths[0]).decode().strip()
        if bundle['expected_git_head'] is None:
            manifest = records.loads(git(root, 'show', saved_commit + ':.novel-creator/manifest.json'))
            paths += ['.novel-creator/manifest.json', '.gitignore'] + manifest.get('managed_paths', [])
    elif receipt:
        paths = receipt['paths']
    paths = sorted(set(paths))
    for path in paths:
        safe_path(root, path, setup=True)
    cleanup = False
    if published:
        entries = committed_entries(root, saved_commit)
        try:
            desired = b''.join(f'{entries[p][0]} {entries[p][1]} 0\t{p}\0'.encode() for p in paths)
        except KeyError as error:
            raise ToolError(4, 'Saved recovery scope is unavailable', checkpoint=confirmed) from error
        cleanup = index_entries(root, paths) != desired or bool(receipt and receipt.get('cleanup_required'))
    held = safe_path(root, '.novel-creator/local/write.lock').exists()
    report = {'ok': True, 'operation': 'recover', 'novel_id': bundle['novel_id'],
              'checkpoint': confirmed, 'warnings': [], 'data': {
                  'state': 'cleanup_needed' if cleanup else ('published' if published else 'pending'),
                  'saved': published, 'cleanup_required': cleanup, 'writer_lock_held': held,
                  'exchange_id': exchange_id, 'saved_response_display': 'unconfirmed',
                  'saved_response': next((m['text'] for m in bundle['messages'] if m['role'] == 'assistant'), None) if published else None,
                  'next_action': 'Inspect lock ownership; never remove a live lock' if held else
                                 ('Explicit unchanged retry required' if cleanup or not published else 'Continue from saved context')}}
    if not retry:
        return report
    actual_expected = None if expected_head == 'unborn' else expected_head
    if actual_expected != initial:
        raise ToolError(3, 'Recovery checkpoint changed', checkpoint=confirmed, pending=exchange_id,
                        expected_head=actual_expected, actual_head=initial)
    if not published:
        result = save(root, bundle)
        result['operation'] = 'recover'
        return result
    with writer_lock(root, pending=exchange_id):
        if head(root) != initial:
            raise ToolError(3, 'Recovery checkpoint advanced', checkpoint=confirmed, pending=exchange_id)
        if not cleanup:
            result = success(bundle, saved_commit, already=True)
            result['operation'] = 'recover'
            return result
        if initial != saved_commit:
            raise ToolError(3, 'Published cleanup requires inspection after branch advancement', checkpoint=confirmed)
        current = index_entries(root, paths)
        if receipt:
            if receipt['bundle'] != bundle or receipt['branch'] != branch(root):
                raise ToolError(3, 'Recovery receipt changed', checkpoint=confirmed)
            baseline = receipt['baseline_index'].encode()
        else:
            prior_entries = committed_entries(root, bundle['expected_git_head'])
            baseline = b''.join(f'{prior_entries[p][0]} {prior_entries[p][1]} 0\t{p}\0'.encode()
                                for p in paths if p in prior_entries)
        if current not in (baseline, desired):
            raise ToolError(3, 'Managed index changed; cleanup would overwrite staged work', checkpoint=confirmed)
        for path in paths:
            target = safe_path(root, path, setup=True)
            if not target.is_file() or git(root, 'hash-object', '--no-filters', '--', str(target)).decode().strip() != entries[path][1]:
                raise ToolError(3, 'Managed working file changed; cleanup paused', checkpoint=confirmed, affected_refs=[path])
        try:
            sync_index(root, paths, current, saved_commit)
            if receipt:
                receipt.update(state='published', cleanup_required=False)
                atomic_json(receipt_path, receipt)
        except (OSError, ToolError) as error:
            raise ToolError(5, 'Saved checkpoint retained; index cleanup still required', checkpoint=confirmed, pending=exchange_id) from error
        result = success(bundle, saved_commit, already=True)
        result['operation'] = 'recover'
        return result
