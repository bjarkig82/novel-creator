"""Local exchange transaction: private candidate index, conditional ref publication.

Only a published local branch commit is authority. Pending files/receipts are not.
The lock serializes this tool, not arbitrary external Git operations.
"""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

from . import records, validation
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


def safe_path(root, relative, *, setup=False):
    """Allow only fixed managed locations; check each existing path component."""
    path = PurePosixPath(relative)
    if (not relative or path.is_absolute() or '..' in path.parts or '\\' in relative or
        str(path) != relative or any(c in relative for c in ('\x00', '\n', '\r'))):
        raise ToolError(2, 'Invalid managed path')
    allowed = (BUNDLE.fullmatch(relative) or relative.startswith('.novel-creator/local/') or
               relative == '.novel-creator/manifest.json')
    if setup:
        allowed = allowed or (relative in ('.gitignore', '.gitattributes') or
                    relative.startswith(('.novel-creator/src/', '.novel-creator/schemas/',
                     '.novel-creator/workflows/', '.novel-creator/languages/')) or
                    relative == '.novel-creator/run.py' or
                    bool(re.fullmatch(r'\.agents/skills/novel-[a-z-]+/SKILL\.md', relative)))
    if not allowed:
        raise ToolError(2, 'Write is outside the managed allowlist')
    current = Path(root)
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ToolError(2, 'Symlink in managed path')
    return current


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


def read_history(root, commit=None):
    root = Path(root)
    commit = commit or head(root)
    history = []
    entries = committed_entries(root, commit)
    for path in sorted(p for p in entries if p.startswith('story/exchanges/')):
        try:
            if not BUNDLE.fullmatch(path) or entries[path][0] != '100644':
                raise ToolError(4, 'Invalid committed exchange path or file mode', affected_refs=[path])
            value = records.loads(git(root, 'cat-file', 'blob', entries[path][1]))
            if not isinstance(value, dict):
                raise ValueError('Exchange must be an object')
            if value.get('schema_version') != '1.0':
                raise ToolError(4, 'Unsupported exchange schema', affected_refs=[path])
            validation.validate_exchange(value, history)
            if bundle_path(value) != path:
                raise ValueError('Exchange filename mismatch')
        except (ToolError, ValueError, TypeError, KeyError) as cause:
            error = cause if isinstance(cause, ToolError) else ToolError(4, 'Committed exchange context is unreadable')
            error.affected_refs = error.affected_refs or [path]
            error.checkpoint = _prefix_checkpoint(root, history, commit, entries)
            if error is cause:
                raise
            raise error from cause
        history.append(value)
    return history


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
    for path, (mode, oid) in entries.items():
        if path.startswith(('story/exchanges/', '.novel-creator/')) and not path.startswith('.novel-creator/local/'):
            target = safe_path(root, path, setup=True)
            if mode != '100644' or not target.is_file():
                raise ToolError(3, 'Managed file is missing or has an unsafe mode')
            current = git(root, 'hash-object', '--no-filters', '--', str(target)).decode().strip()
            if current != oid:
                raise ToolError(3, 'Managed working file changed outside the exchange transaction')
            baseline = f'100644 {oid} 0\t{path}\0'.encode()
            if index_entries(root, [path]) != baseline:
                raise ToolError(3, 'Managed index entry changed outside the transaction')
    for path in paths:
        if path in entries:
            raise ToolError(3, 'Exchange path already exists in confirmed history')
        if index_entries(root, [path]):
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
        with lock.open('rb') as stream:
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
            history = read_history(root, initial)
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
            validation.validate_exchange(bundle, history)
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
