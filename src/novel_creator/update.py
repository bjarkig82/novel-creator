"""Explicit release previews and local, read-only maintenance observations."""
import base64
import os
from pathlib import Path
import stat
import tempfile
import sys
import uuid

from . import maintenance, records, storage, update_release as release
from .cli import ToolError


MANIFEST = '.novel-creator/manifest.json'
SHARED = {'AGENTS.md': 'instructions', '.gitignore': 'ignore_rules', '.gitattributes': 'attributes'}
RULES = {'.gitignore': ['.novel-creator/local/', '__pycache__/', '*.pyc'],
         '.gitattributes': ['.novel-creator/** text eol=lf', 'story/exchanges/** text eol=lf',
                            '.agents/skills/** text eol=lf']}
MAINTENANCE_LAUNCHER = (
    'import json,sys\n'
    "if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')\n"
    "print(json.dumps({'ok':False,'error':{'code':6,'message':'Update pending; use external-controller recovery'}}))\n"
    'raise SystemExit(6)\n').encode()
LAUNCHER = '.novel-creator/run.py'


def _read_manifest(root):
    try:
        raw = storage.safe_path(root, MANIFEST).read_bytes()
        value = records.loads(raw)
        if (not isinstance(value, dict) or not isinstance(value.get('novel_id'), str)
                or value.get('schema_version') != '1.0' or str(uuid.UUID(value['novel_id'])) != value['novel_id']):
            raise ValueError()
        installation_format = value.get('installation_format', 1)
        if type(installation_format) is not int or installation_format not in (1, 2):
            raise ValueError()
        return value, raw
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise ToolError(4, 'Book installation metadata is unavailable or unsupported') from error


def _result(root, manifest, *, operation='update.preview', state, target=None, identifier=None,
            operation_id=None, changes=None, blockers=None, ready=False, cleanup=False, next_action=None, **extra):
    return {'ok': True, 'operation': operation, 'novel_id': manifest.get('novel_id'),
            'checkpoint': {'git_head': storage.head(root)}, 'warnings': [],
            'data': {'state': state, 'installed_version': manifest.get('bundle_version'),
                     'target_version': target, 'preview_id': identifier, 'operation_id': operation_id,
                     'changes': changes or [], 'blockers': blockers or [], 'ready': ready,
                     'cleanup_required': cleanup, 'next_action': next_action, **extra}}


def _file_identity(path):
    try:
        mode = storage._path_mode(path)
        if not stat.S_ISREG(mode):
            raise ToolError(3, 'Preview encountered a nonregular or redirected file')
        return {'sha256': release.digest(path.read_bytes()),
                'mode': '100755' if os.name != 'nt' and mode & 0o111 else '100644'}
    except FileNotFoundError:
        return None


def fingerprint(novel):
    """Hash semantic staging, visible work and ignored operational evidence."""
    root = storage.root_path(novel)
    branch, head = storage._branch_head(root)
    names = set(storage.git(root, 'ls-files', '--cached', '--others', '--exclude-standard', '-z').decode('utf-8').split('\0')) - {''}
    local = storage.safe_path(root, '.novel-creator/local/evidence').parent
    if local.exists():
        for path in local.rglob('*'):
            name = path.relative_to(root).as_posix()
            storage.safe_path(root, name)
            if path.is_file() and not name.endswith('.guard'):
                names.add(name)
    values = {}
    for name in sorted(names):
        # Check every parent, including arbitrary writer-owned paths, without following links.
        relative = release._relative(name)
        path = root
        for part in relative.parts:
            path = path / part
            try:
                if stat.S_ISLNK(storage._path_mode(path)):
                    raise ToolError(3, 'Preview does not follow redirected worktree paths')
            except FileNotFoundError:
                break
        values[name] = _file_identity(root / name)
    retro = maintenance.retro_snapshot(root)
    return release.digest(release.canonical({'branch': branch, 'head': head, 'files': values,
        'index': base64.b64encode(storage.git(root, 'ls-files', '--stage', '-z')).decode(),
        'machine_grant': retro['machine_grant'], 'machine_grant_digest': retro['machine_grant_digest']}))


def _external_cache(root):
    cache = release.cache_home().resolve()
    if cache == root or cache.is_relative_to(root):
        raise ToolError(3, 'Update preparation cache must be outside the book')
    return cache


def _require_external_controller(root):
    if Path(__file__).resolve().is_relative_to(root):
        raise ToolError(4, 'Use a separately installed controller outside the book for preview, application and recovery retry')


def _source_bundle(manifest, metadata, transport, runtime):
    artifact = release.select_release(metadata, version=manifest['bundle_version'], runtime=runtime)
    try:
        raw = transport.get(artifact['url'])
    except OSError as error:
        raise ToolError(5, 'Installed source release identity could not be established') from error
    inventory = release.wheel_inventory(raw, artifact)
    legacy = manifest.get('installation_format', 1) == 1
    if legacy and manifest['bundle_version'] not in ('0.1.0', '0.2.0'):
        raise ToolError(4, 'Unsupported legacy installation format/version')
    return (release.bundle_inventory(inventory, legacy=legacy),
            inventory.get('novel_creator/codex/AGENTS.production.md'), artifact, raw)


def _plan_changes(root, manifest, raw_manifest, source, source_agents, prepared, identifier):
    head = storage.head(root)
    committed = storage.committed_entries(root, head)
    if storage.git(root, 'show', head + ':' + MANIFEST) != raw_manifest:
        raise ToolError(3, 'Installation manifest differs from its committed evidence')
    checksums = manifest.get('checksums')
    if not isinstance(checksums, dict) or set(manifest.get('managed_paths', [])) != set(checksums):
        raise ToolError(4, 'Installed ownership inventory is malformed')
    exclusive = set(checksums) - set(SHARED)
    if exclusive != set(source):
        raise ToolError(3, 'Installed ownership inventory differs from its published source release')
    if manifest.get('installation_format', 1) == 2:
        ownership = manifest.get('ownership', {})
        if (set(ownership.get('exclusive', {})) != exclusive or set(ownership.get('shared', {})) != set(SHARED)
                or any(ownership['exclusive'][path] != {'sha256': checksums[path], 'mode': '100644'} for path in exclusive)
                or any(ownership['shared'][path].get('role') != role for path, role in SHARED.items())):
            raise ToolError(4, 'Installed format-2 ownership is inconsistent')
    for path in exclusive:
        raw = source[path]
        actual = storage.safe_path(root, path, setup=True, _regular_leaf=True)
        entry = committed.get(path)
        if (checksums[path] != release.digest(raw) or actual.read_bytes() != raw or not entry
                or entry[0] != '100644'
                or storage.git(root, 'cat-file', 'blob', entry[1]) != raw):
            raise ToolError(3, 'Exclusive installed resource changed; preserve it before updating', affected_refs=[path])
        if _file_identity(actual)['mode'] != entry[0]:
            raise ToolError(3, 'Installed resource mode changed', affected_refs=[path])
    target = dict(prepared['files'])
    shared_metadata = {}
    for path, role in SHARED.items():
        current = storage.safe_path(root, path, setup=True)
        old = current.read_bytes() if current.exists() else None
        shared_metadata[path] = {'role': role, 'required_lines': RULES.get(path, [])}
        if path == 'AGENTS.md':
            # Full replacement is granted only by the verified source default identity.
            identity = (checksums.get(path) if manifest.get('installation_format', 1) == 1 else
                        manifest.get('ownership', {}).get('shared', {}).get(path, {}).get('generated_default_sha256'))
            if (old is not None and old == source_agents and identity == release.digest(old)
                    and _file_identity(current)['mode'] == '100644' and committed.get(path, (None,))[0] == '100644'):
                target[path] = prepared['agents_default']
                shared_metadata[path]['generated_default_sha256'] = release.digest(prepared['agents_default'])
        else:
            missing = [line.encode() for line in RULES[path] if line.encode() not in (old or b'').splitlines()]
            if missing:
                target[path] = (old or b'') + (b'\n' if old and not old.endswith(b'\n') else b'') + b'\n'.join(missing) + b'\n'
    target_manifest = dict(manifest, installation_format=2, bundle_version=prepared['version'],
        managed_paths=sorted(prepared['files']), checksums=prepared['checksums'],
        ownership={'exclusive': {path: {'sha256': prepared['checksums'][path], 'mode': prepared['modes'][path]}
                                 for path in sorted(prepared['files'])}, 'shared': shared_metadata})
    target_manifest['last_update'] = {'operation_id': identifier, 'source_head': head,
                                      'artifact_sha256': prepared['artifact']['sha256']}
    target[MANIFEST] = release.canonical(target_manifest) + b'\n'
    changes = []
    for path in sorted(exclusive | set(target)):
        file = storage.safe_path(root, path, setup=True)
        identity = _file_identity(file)
        old = file.read_bytes() if identity is not None else None
        new = target.get(path)
        if path not in exclusive and path not in SHARED and path != MANIFEST and old is not None:
            raise ToolError(3, 'Target resource collides with existing content', affected_refs=[path])
        if old == new:
            continue
        if path in SHARED or path == MANIFEST or path in exclusive:
            expected = committed.get(path)
            actual = storage.index_entries(root, [path])
            wanted = (f'{expected[0]} {expected[1]} 0\t{path}\0'.encode() if expected else b'')
            if actual != wanted:
                raise ToolError(3, 'Affected installed/shared path has staged changes', affected_refs=[path])
        elif storage.index_entries(root, [path]):
            raise ToolError(3, 'Target resource collides with staged content', affected_refs=[path])
        changes.append({'path': path, 'action': 'add' if old is None else 'remove' if new is None else 'replace',
                        'before': base64.b64encode(old).decode() if old is not None else None,
                        'after': base64.b64encode(new).decode() if new is not None else None,
                        'before_mode': identity['mode'] if identity else None,
                        'after_mode': (identity['mode'] if path in SHARED and identity else '100644') if new is not None else None})
    return changes, target_manifest


def preview(novel, *, version=None, python=None, transport=None):
    root = storage.root_path(novel)
    _require_external_controller(root)
    maintenance.ensure_ready(root)
    manifest, raw = _read_manifest(root)
    from .install import _preflight
    _preflight(root, require_identity=False)
    _external_cache(root)  # Before preparation may create anything.
    initial = fingerprint(root)
    branch, head = storage._branch_head(root)
    if not head:
        raise ToolError(3, 'A committed initialized book is required')
    _check_story(root, head)
    runtime = release.runtime_info(python)
    transport = transport or release.PublicReleaseTransport()
    metadata = release.release_index(transport)
    selected = release.select_release(metadata, version=version, runtime=runtime)
    installed = release.stable_version(manifest.get('bundle_version'))
    chosen = release.stable_version(selected['version'])
    if chosen < installed:
        raise ToolError(2, 'Downgrading an existing book is unsupported')
    if chosen == installed:
        if fingerprint(root) != initial:
            raise ToolError(3, 'Book changed during release inspection; check again')
        return _result(root, manifest, state='already_current', target=selected['version'], ready=True,
                       runtime_python=runtime['python'], next_action='No book update is required.')
    source, source_agents, source_artifact, source_raw = _source_bundle(manifest, metadata, transport, runtime)
    prepared = release.prepare(selected, python=runtime['python'], transport=transport)
    if manifest.get('installation_format', 1) not in prepared['protocol']['source_installation_formats']:
        raise ToolError(4, 'Selected release cannot update this installation format')
    identifier = str(uuid.uuid4())
    changes, target_manifest = _plan_changes(root, manifest, raw, source, source_agents, prepared, identifier)
    history = storage.read_history(root)
    if not history or history[-1]['novel_id'] != manifest['novel_id']:
        raise ToolError(3, 'Book identity does not match committed story records')
    retro = maintenance.retro_snapshot(root)
    maintenance.require_quiet_retro(retro)
    release.probe_prepared(prepared, {'history': history, 'retro_documents': retro['documents']})
    if fingerprint(root) != initial or release.runtime_info(runtime['python'])['fingerprint'] != runtime['fingerprint']:
        raise ToolError(3, 'Book or configured runtime changed during preview; check again')
    document = release.validate_document('preview', {'kind': 'preview', 'document_version': 1,
        'preview_id': identifier, 'novel_id': manifest['novel_id'], 'novel_root': str(root),
        'branch': branch, 'source_head': head, 'source_manifest_digest': release.digest(raw),
        'source_version': manifest['bundle_version'], 'target_version': selected['version'],
        'fingerprint': initial, 'runtime_python': runtime['python'], 'runtime_fingerprint': runtime['fingerprint'],
        'artifact': selected, 'bundle_digest': prepared['bundle_digest'], 'changes': changes,
        'source_manifest': manifest, 'target_manifest': target_manifest})
    cache = _external_cache(root)
    _cache_archive(cache, source_artifact['sha256'], source_raw)
    _cache_archive(cache, selected['sha256'], Path(prepared['wheel_path']).read_bytes())
    storage.atomic_json(cache / 'previews' / (identifier + '.inputs.json'), {
        'source_artifact': source_artifact, 'preview_digest': release.digest(release.canonical(document))})
    storage.atomic_json(cache / 'previews' / (identifier + '.json'), document)
    return _result(root, manifest, state='preview', target=selected['version'], identifier=identifier,
                   changes=[{'path': item['path'], 'action': item['action']} for item in changes],
                   artifact_sha256=selected['sha256'], bundle_digest=prepared['bundle_digest'],
                   reviewed_head=head, runtime_python=runtime['python'],
                   controller_python=str(Path(sys.executable).absolute()),
                   apply_command=[str(Path(sys.executable).absolute()), '-I', '-B', '-m', 'novel_creator',
                       'update', '--novel', str(root), '--apply', '--preview', identifier,
                       '--version', selected['version'], '--expected-head', head,
                       *(['--confirm-quiescent'] if manifest.get('installation_format', 1) == 1 else []), '--json'],
                   recovery_command=[str(Path(sys.executable).absolute()), '-I', '-B', '-m', 'novel_creator',
                       'update', 'recover', '--novel', str(root), '--operation', identifier, '--json'],
                   next_action=('Review these changes before explicitly applying. Close other legacy book clients through apply/recovery, then restart the guarded launcher (FUP-001).'
                                if manifest.get('installation_format', 1) == 1 else 'Review these changes before explicitly applying.'))


def _cache_archive(cache, digest, raw):
    if release.digest(raw) != digest:
        raise ToolError(3, 'Prepared artifact changed before caching')
    folder = cache / 'artifacts'
    folder.mkdir(parents=True, mode=0o700, exist_ok=True)
    path = folder / (digest + '.whl')
    if path.is_symlink():
        raise ToolError(3, 'Private artifact cache is redirected')
    try:
        with path.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        storage.fsync_directory(folder)
    except FileExistsError:
        if path.read_bytes() != raw:
            raise ToolError(3, 'Existing cached artifact differs from its verified identity')


class _OfflineArtifact:
    def __init__(self, artifact, raw):
        self.artifact, self.raw = artifact, raw

    def get(self, url):
        if url != self.artifact['url']:
            raise ToolError(3, 'Offline transaction cannot change its pinned artifact')
        return self.raw


def _identifier(value):
    try:
        if str(uuid.UUID(value)) != value:
            raise ValueError()
    except (ValueError, TypeError, AttributeError) as error:
        raise ToolError(2, 'Expected a canonical update UUID') from error
    return value


def _load_preview(root, identifier):
    cache = _external_cache(root)
    try:
        path = cache / 'previews' / (_identifier(identifier) + '.json')
        if path.is_symlink():
            raise ValueError()
        document = release.validate_document('preview', records.loads(path.read_bytes()))
        if document['novel_root'] != str(root) or document['preview_id'] != identifier:
            raise ValueError()
        inputs = records.loads(path.with_name(identifier + '.inputs.json').read_bytes())
        if (set(inputs) != {'source_artifact', 'preview_digest'}
                or inputs['preview_digest'] != release.digest(release.canonical(document))
                or document['target_version'] != document['artifact']['version']
                or document['target_manifest'].get('bundle_version') != document['target_version']
                or document['source_manifest'].get('bundle_version') != document['source_version']
                or document['source_manifest'].get('novel_id') != document['novel_id']
                or document['target_manifest'].get('novel_id') != document['novel_id']):
            raise ValueError()
        source_artifact = release.validate_artifact(inputs['source_artifact'])
        source_raw = (cache / 'artifacts' / (source_artifact['sha256'] + '.whl')).read_bytes()
        source_inventory = release.wheel_inventory(source_raw, source_artifact)
        if source_artifact['version'] != document['source_version']:
            raise ValueError()
        target_raw = (cache / 'artifacts' / (document['artifact']['sha256'] + '.whl')).read_bytes()
        release.wheel_inventory(target_raw, document['artifact'])
        return document, source_inventory, target_raw
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise ToolError(3, 'Preview or its verified cached artifacts are unavailable; request a fresh preview') from error


def _journal(root, value):
    release.validate_document('operation', value)
    storage.atomic_json(maintenance.operation_path(root, value['operation_id']), value)


def _operation_file(root, identifier, name):
    return storage.safe_path(root, '.novel-creator/local/update/operations/' + _identifier(identifier) + '/' + name)


def _operational_digest(root):
    base = storage.safe_path(root, '.novel-creator/local/evidence').parent
    values = {}
    for path in sorted(base.rglob('*')):
        name = path.relative_to(root).as_posix()
        storage.safe_path(root, name)
        if (path.is_file() and not name.endswith('.guard')
                and not name.startswith(('.novel-creator/local/update/', '.novel-creator/local/write.lock/'))):
            values[name] = release.digest(path.read_bytes())
    retro = maintenance.retro_snapshot(root)
    values['machine_grant_digest'] = retro['machine_grant_digest']
    return release.digest(release.canonical(values))


def _check_story(root, head):
    # Use the existing immutable-story guard only; replacements have their own
    # expected-before checks and never enter the new-exchange path guard.
    entries = {path: entry for path, entry in storage.committed_entries(root, head).items()
               if path.startswith('story/exchanges/')}
    storage.check_managed(root, head, [], entries=entries)


def _runtime_unchanged(document):
    if release.runtime_info(document['runtime_python'])['fingerprint'] != document['runtime_fingerprint']:
        raise ToolError(3, 'Configured runtime changed since the reviewed update')


def _index_rows(root, paths):
    rows = dict.fromkeys(paths, b'')
    for entry in storage.index_entries(root, list(rows)).split(b'\0'):
        if entry:
            name = entry.rsplit(b'\t', 1)[1].decode('utf-8')
            if name in rows:
                rows[name] += entry + b'\0'
    return {path: base64.b64encode(raw).decode() for path, raw in rows.items()}


def _candidate(root, document, folder):
    index = str(folder / 'candidate-index')
    environment = {'GIT_INDEX_FILE': index}
    no_hooks = folder / 'hooks-disabled'
    no_hooks.write_bytes(b'')
    options = ('-c', 'core.hooksPath=' + no_hooks.as_posix())
    storage.git(root, *options, 'read-tree', document['source_head'], env=environment)
    payload = b''
    for change in document['changes']:
        path = change['path']
        storage.safe_path(root, path, setup=True)
        if change['after'] is None:
            payload += f'0 {"0" * len(document["source_head"])}\t{path}\0'.encode()
        else:
            raw = base64.b64decode(change['after'], validate=True)
            oid = storage.git(root, 'hash-object', '-w', '--stdin', input=raw).decode().strip()
            payload += f'{change["after_mode"]} {oid} 0\t{path}\0'.encode()
    storage.git(root, *options, 'update-index', '-z', '--index-info', env=environment, input=payload)
    tree = storage.git(root, *options, 'write-tree', env=environment).decode().strip()
    return storage.git(root, *options, '-c', 'commit.gpgSign=false', 'commit-tree', tree, '-p', document['source_head'],
        input=('Update Novel Creator to ' + document['target_version'] + '\n\nOperation: ' + document['preview_id'] + '\n').encode()).decode().strip()


def _check_candidate(root, value, prepared):
    preview, candidate = value['preview'], value['candidate']
    parents = storage.git(root, 'rev-list', '--parents', '-n', '1', candidate).decode().split()
    if parents != [candidate, preview['source_head']]:
        raise ToolError(3, 'Update candidate has a different parent')
    before = storage.committed_entries(root, preview['source_head'])
    after = storage.committed_entries(root, candidate)
    changes = {item['path']: item for item in preview['changes']}
    if len(changes) != len(preview['changes']):
        raise ToolError(3, 'Duplicate paths in update evidence')
    actual = {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}
    # A shared working-file edit can legitimately produce a reviewed commit change.
    if not actual <= set(changes):
        raise ToolError(3, 'Candidate contains changes outside the reviewed update')
    allowed = set(preview['source_manifest']['managed_paths']) | set(prepared['files']) | set(SHARED) | {MANIFEST}
    for path, change in changes.items():
        storage.safe_path(root, path, setup=True)
        if path not in allowed:
            raise ToolError(3, 'Update path is outside verified installation ownership')
        if change['after'] is None:
            if path in after or path in prepared['files'] or path in SHARED or path == MANIFEST:
                raise ToolError(3, 'Candidate removal disagrees with target inventory')
        else:
            raw = base64.b64decode(change['after'], validate=True)
            if (path not in after or after[path][0] != change['after_mode']
                    or storage.git(root, 'cat-file', 'blob', after[path][1]) != raw):
                raise ToolError(3, 'Candidate resource differs from journaled bytes')
    for path, raw in prepared['files'].items():
        if path not in after or after[path][0] != prepared['modes'][path] or storage.git(root, 'cat-file', 'blob', after[path][1]) != raw:
            raise ToolError(3, 'Candidate bundle differs from its verified target wheel')
    if (records.loads(storage.git(root, 'show', candidate + ':' + MANIFEST)) != preview['target_manifest']
            or prepared['bundle_digest'] != preview['bundle_digest']):
        raise ToolError(3, 'Candidate manifest or bundle digest changed')


def _replace(root, path, content, mode):
    target = storage.safe_path(root, path, setup=True)
    if content is None:
        target.unlink(missing_ok=True)
        storage.fsync_directory(target.parent)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='update-', dir=target.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o755 if mode == '100755' else 0o644)
        os.replace(temporary, target)
        storage.fsync_directory(target.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _check_worktree(root, value, *, final=False, only_path=None, allow_launcher=True):
    for change in value['preview']['changes']:
        if only_path is not None and change['path'] != only_path:
            continue
        path = storage.safe_path(root, change['path'], setup=True)
        identity = _file_identity(path)
        raw = path.read_bytes() if identity else None
        after = base64.b64decode(change['after'], validate=True) if change['after'] is not None else None
        before = base64.b64decode(change['before'], validate=True) if change['before'] is not None else None
        allowed = [(after, change['after_mode'])]
        if not final:
            allowed.append((before, change['before_mode']))
        if change['path'] == LAUNCHER and allow_launcher:
            allowed.append((MAINTENANCE_LAUNCHER, '100644'))
        if (raw, identity['mode'] if identity else None) not in allowed:
            raise ToolError(3, 'Installed working file differs from recorded update evidence', affected_refs=[change['path']])


def _check_untouched_resources(root, value, prepared):
    affected = {item['path'] for item in value['preview']['changes']}
    for path, raw in prepared['files'].items():
        if path in affected:
            continue
        target = storage.safe_path(root, path, setup=True, _regular_leaf=True)
        if target.read_bytes() != raw or _file_identity(target)['mode'] != prepared['modes'][path]:
            raise ToolError(3, 'An unchanged installed resource was modified during maintenance', affected_refs=[path])


def _verify_target(root, value, prepared):
    _check_worktree(root, value, final=True)
    _check_story(root, value['candidate'])
    for path, raw in prepared['files'].items():
        if path == LAUNCHER:
            continue
        actual = storage.safe_path(root, path, setup=True, _regular_leaf=True)
        if actual.read_bytes() != raw or _file_identity(actual)['mode'] != prepared['modes'][path]:
            raise ToolError(3, 'Installed target bundle changed during verification', affected_refs=[path])
    release.probe_prepared(prepared, {'history': storage.read_history(root),
                                     'retro_documents': maintenance.retro_snapshot(root)['documents']})
    program = '''
import sys,json
from novel_creator.context import read
from novel_creator.maintenance import read_verification
with read_verification(sys.argv[1], sys.argv[2], sys.argv[3]):
 result=read(sys.argv[1],operation='validate')
print(json.dumps({'ok':result['ok'],'checkpoint':result['checkpoint']}))
'''
    result = records.loads(release._run([prepared['env_python'], '-I', '-B', '-X', 'utf8', '-c', program,
        root, value['operation_id'], value['fence']['token']], cwd=Path(prepared['wheel_path']).parent))
    if result.get('ok') is not True or result['checkpoint']['git_head'] != value['candidate']:
        raise ToolError(5, 'Published target could not reopen the confirmed book context')


def _ready_to_release(root, value, prepared, baseline, desired):
    document = value['preview']
    if (storage._branch_head(root) != (document['branch'], value['candidate'])
            or _operational_digest(root) != baseline['operational_digest']
            or _index_rows(root, list(desired)) != desired):
        raise ToolError(3, 'Published update state changed during final verification')
    _check_worktree(root, value, final=True, allow_launcher=False)
    _check_untouched_resources(root, value, prepared)
    _check_story(root, value['candidate'])
    _runtime_unchanged(document)


def _finish(root, value, prepared, *, fault):
    from .install import _preflight
    _preflight(root, require_identity=False)
    document = value['preview']
    identifier = value['operation_id']
    paths = [change['path'] for change in document['changes']]
    baseline = records.loads(_operation_file(root, identifier, 'baseline.json').read_bytes())
    if baseline['preview_digest'] != release.digest(release.canonical(document)):
        raise ToolError(3, 'Recorded preview changed after transaction preparation')
    if (baseline['candidate'] != value['candidate'] or baseline['index_baseline_digest'] != release.digest(release.canonical(value['index_baseline']))):
        raise ToolError(3, 'Recorded candidate or index baseline changed')
    _check_candidate(root, value, prepared)
    _runtime_unchanged(document)
    branch, head = storage._branch_head(root)
    if branch != document['branch'] or head not in (document['source_head'], value['candidate']):
        raise ToolError(3, 'Update branch/checkpoint changed; preserve the candidate')
    if _operational_digest(root) != baseline['operational_digest']:
        raise ToolError(3, 'Book operational evidence changed during maintenance')
    _check_worktree(root, value)
    _check_untouched_resources(root, value, prepared)
    if head == document['source_head']:
        value['state'] = 'replacing'
        _journal(root, value)
        _replace(root, LAUNCHER, MAINTENANCE_LAUNCHER, '100644')
        fault('after_launcher_swap')
        for change in document['changes']:
            if change['path'] == LAUNCHER:
                continue
            _check_worktree(root, value, only_path=change['path'])
            raw = base64.b64decode(change['after'], validate=True) if change['after'] is not None else None
            fault('before_replace:' + change['path'])
            _check_worktree(root, value, only_path=change['path'])
            _replace(root, change['path'], raw, change['after_mode'])
            fault('after_replace:' + change['path'])
        _check_worktree(root, value, final=True)
        _check_untouched_resources(root, value, prepared)
        _check_story(root, document['source_head'])
        if _index_rows(root, paths) != value['index_baseline']:
            raise ToolError(3, 'Affected index entries changed before publication')
        if storage.branch(root) != document['branch']:
            raise ToolError(3, 'Checked-out branch changed before update publication')
        fault('before_ref_publication')
        _runtime_unchanged(document)
        if storage.branch(root) != document['branch']:
            raise ToolError(3, 'Checked-out branch changed at publication')
        # A verified regular archive cannot contain filesystem hook children.
        # Ref publication must not invoke repository-configured push/services.
        no_hooks = _operation_file(root, identifier, 'target.whl').as_posix()
        published = storage.git(root, '-c', 'core.hooksPath=' + no_hooks, 'update-ref',
                                document['branch'], value['candidate'], document['source_head'], check=False)
        if published.returncode:
            raise ToolError(3, 'Reviewed branch changed before conditional publication',
                            expected_head=document['source_head'], actual_head=storage.head(root))
        fault('after_ref_publication')
    if storage._branch_head(root) != (document['branch'], value['candidate']):
        raise ToolError(3, 'Checked-out branch advanced after candidate publication')
    value['state'] = 'candidate_published'
    _journal(root, value)
    fault('before_index_sync')
    current = _index_rows(root, paths)
    entries = storage.committed_entries(root, value['candidate'])
    desired = {path: base64.b64encode((f'{entries[path][0]} {entries[path][1]} 0\t{path}\0'.encode()
                                     if path in entries else b'')).decode() for path in paths}
    if any(current[path] not in (value['index_baseline'][path], desired[path]) for path in paths):
        raise ToolError(3, 'Affected index changed; cleanup must preserve external staged work')
    storage.sync_index(root, paths, storage.index_entries(root, paths), value['candidate'], entries=entries,
        git_options=('-c', 'core.hooksPath=' + _operation_file(root, identifier, 'target.whl').as_posix()))
    fault('after_index_sync')
    value['state'] = 'verifying'
    _journal(root, value)
    _verify_target(root, value, prepared)
    fault('after_verification')
    _replace(root, LAUNCHER, prepared['files'][LAUNCHER], prepared['modes'][LAUNCHER])
    fault('after_final_launcher')
    _ready_to_release(root, value, prepared, baseline, desired)
    value['state'] = 'complete'
    _journal(root, value)
    fault('after_completion')
    if not maintenance.confirmed_owner(root, value):
        raise ToolError(6, 'Update fence ownership changed before cleanup')
    active = storage.safe_path(root, '.novel-creator/local/update/active.json')
    if active.exists():
        if records.loads(active.read_bytes())['operation_id'] != identifier:
            raise ToolError(6, 'Another operation owns maintenance state')
        active.unlink()
        storage.fsync_directory(active.parent)
    fault('after_active_release')
    owner = storage.safe_path(root, '.novel-creator/local/write.lock/owner.json')
    fault('before_fence_release')
    _ready_to_release(root, value, prepared, baseline, desired)
    # Archive the still-owned directory atomically. Deleting owner.json first
    # would leave an unprovable empty fence if the process died before rmdir.
    archived = _operation_file(root, identifier, 'released-fence')
    if archived.exists():
        raise ToolError(6, 'Fence release evidence already exists; preserve both locations')
    os.rename(owner.parent, archived)
    storage.fsync_directory(archived.parent)
    storage.fsync_directory(owner.parent.parent)
    fault('after_fence_release')
    return _result(root, document['target_manifest'], operation='update.apply', state='complete',
                   target=document['target_version'], identifier=document['preview_id'], operation_id=identifier,
                   ready=True, runtime_python=document['runtime_python'],
                   next_action='Reload the book instructions before continuing writing.')


def _operation_error(root, value, error):
    reference = storage.git(root, 'rev-parse', '--verify', value['preview']['branch'], check=False)
    published = (not reference.returncode and not storage.git(root, 'merge-base', '--is-ancestor',
        value['candidate'], reference.stdout.decode().strip(), check=False).returncode)
    code = 5 if published else (error.code if isinstance(error, ToolError) else 5)
    try:
        recorded = maintenance.read_operation(root, value['operation_id'])
    except ToolError:
        recorded = value
    unproven = (storage.safe_path(root, '.novel-creator/local/write.lock').exists()
                and not maintenance.confirmed_owner(root, recorded))
    return ToolError(code, str(error) if isinstance(error, ToolError) else 'Update interrupted; preserve its evidence and use external recovery',
        checkpoint={'git_head': storage.head(root)}, affected_refs=getattr(error, 'affected_refs', []),
        data={'operation_id': value['operation_id'], 'preview_id': value['preview']['preview_id'],
              'state': 'published' if published else 'pending', 'ready': False, 'cleanup_required': True,
              'candidate_published': published, 'candidate': value['candidate'],
              'blockers': ([{'reason': 'ownership_unproven', 'path': '.novel-creator/local/write.lock'}] if unproven else []),
              'next_action': 'Inspect this operation with the external controller before explicit recovery.'})


def _inspect_operation(root, value):
    """Verify local recovery evidence without running or preparing a product."""
    identifier, document = value['operation_id'], value['preview']
    try:
        baseline = records.loads(_operation_file(root, identifier, 'baseline.json').read_bytes())
        if (baseline['preview_digest'] != release.digest(release.canonical(document))
                or baseline['candidate'] != value['candidate']
                or baseline['index_baseline_digest'] != release.digest(release.canonical(value['index_baseline']))):
            raise ValueError()
        original = storage.git(root, 'show', document['source_head'] + ':' + MANIFEST)
        if release.digest(original) != document['source_manifest_digest'] or records.loads(original) != document['source_manifest']:
            raise ValueError()
        artifact = document['artifact']
        raw = _operation_file(root, identifier, 'target.whl').read_bytes()
        inventory = release.wheel_inventory(raw, artifact)
        release.validate_document('release', records.loads(inventory['novel_creator/update-release.json']))
        files = release.bundle_inventory(inventory)
        hashes = {path: release.digest(content) for path, content in files.items()}
        modes = {path: '100644' for path in files}
        prepared = {'files': files, 'modes': modes, 'checksums': hashes,
                    'bundle_digest': release.digest(release.canonical({
                        path: {'sha256': hashes[path], 'mode': modes[path]} for path in sorted(files)}))}
        _check_candidate(root, value, prepared)
        _check_untouched_resources(root, value, prepared)
        if storage._branch_head(root) not in ((document['branch'], document['source_head']), (document['branch'], value['candidate'])):
            raise ValueError()
        if _operational_digest(root) != baseline['operational_digest']:
            raise ValueError()
        _check_worktree(root, value)
        source_entries = storage.committed_entries(root, document['source_head'])
        target_entries = storage.committed_entries(root, value['candidate'])
        observed_head = storage.head(root)
        _check_story(root, observed_head)
        current_index = _index_rows(root, value['index_baseline'])
        for path in value['index_baseline']:
            expected = (f'{source_entries[path][0]} {source_entries[path][1]} 0\t{path}\0'.encode()
                        if path in source_entries else b'')
            if base64.b64decode(value['index_baseline'][path], validate=True) != expected:
                raise ValueError()
            desired = (f'{target_entries[path][0]} {target_entries[path][1]} 0\t{path}\0'.encode()
                       if path in target_entries else b'')
            permitted = (expected, desired) if observed_head == value['candidate'] else (expected,)
            if base64.b64decode(current_index[path], validate=True) not in permitted:
                raise ValueError()
        if storage._branch_head(root) != (document['branch'], observed_head):
            raise ValueError()
        return raw
    except (OSError, ValueError, KeyError, TypeError, ToolError) as error:
        raise ToolError(3, 'Recovery artifacts, checkpoint, files or index differ from the recorded operation') from error


def recover(novel, *, operation_id, retry=False, expected_head=None, fault=None):
    root = storage.root_path(novel)
    identifier = _identifier(operation_id)
    if bool(retry) != (expected_head is not None):
        raise ToolError(2, 'Explicit update recovery retry requires --expected-head; inspection accepts neither')
    report = status(root, operation_id=identifier)
    report['operation'] = 'update.recover'
    report['data']['retry_eligible'] = False
    value = maintenance.read_operation(root, identifier)
    fence = storage.safe_path(root, '.novel-creator/local/write.lock')
    blockers = report['data']['blockers']
    try:
        raw = _inspect_operation(root, value)
        if fence.exists() and not maintenance.confirmed_owner(root, value):
            raise ToolError(6, 'Persistence fence ownership is unproven; preserve the directory and journal')
        if not fence.exists() and value['state'] not in ('prepared', 'complete'):
            raise ToolError(6, 'Recorded update fence is missing; ownership cannot be inferred')
        if value['state'] != 'complete' or fence.exists():
            if not maintenance.owner_is_dead(value['fence']['owner_pid'], value['fence']['owner_identity']):
                raise ToolError(6, 'Recorded updater process is still alive; do not take over its fence')
        _runtime_unchanged(value['preview'])
        from .install import _preflight
        _preflight(root, require_identity=False)
        report['data']['retry_eligible'] = not blockers
    except ToolError as error:
        if retry:
            raise error
        report['data']['ready'] = False
        report['data']['cleanup_required'] = True
        if not blockers:
            blockers.append({'reason': 'owner_live_or_unproven' if error.code == 6 else 'recovery_evidence_changed'})
        return report
    if not retry:
        return report
    _require_external_controller(root)
    _external_cache(root)
    if expected_head != storage.head(root):
        raise ToolError(3, 'Recovery checkpoint changed', expected_head=expected_head, actual_head=storage.head(root),
                        data={'operation_id': identifier})
    document = value['preview']
    if release.runtime_info(document['runtime_python'])['fingerprint'] != document['runtime_fingerprint']:
        raise ToolError(3, 'Configured runtime changed since the reviewed update')
    prepared = release.prepare(document['artifact'], python=document['runtime_python'],
                               transport=_OfflineArtifact(document['artifact'], raw))
    if prepared['runtime']['fingerprint'] != document['runtime_fingerprint']:
        raise ToolError(3, 'Configured runtime changed during recovery preparation')
    with maintenance.access_guard(root, exclusive=True):
        value = maintenance.read_operation(root, identifier)
        _inspect_operation(root, value)
        if storage.head(root) != expected_head:
            raise ToolError(3, 'Recovery checkpoint changed while acquiring exclusion')
        pointer = maintenance.active(root)
        if pointer and pointer['operation_id'] != identifier:
            raise ToolError(6, 'Another operation owns maintenance evidence')
        if value['state'] == 'complete' and not fence.exists():
            archived = records.loads(_operation_file(root, identifier, 'released-fence/owner.json').read_bytes())
            expected_owner = {'update_operation': identifier, 'token': value['fence']['token'],
                              'pid': value['fence']['owner_pid'], 'identity': value['fence']['owner_identity']}
            if archived != expected_owner or pointer:
                raise ToolError(6, 'Completed fence release is not proven by its archived owner evidence')
            for path, content in prepared['files'].items():
                if storage.safe_path(root, path, setup=True, _regular_leaf=True).read_bytes() != content:
                    raise ToolError(3, 'Completed target files changed; recovery cannot replace them')
            report = status(root, operation_id=identifier)
            report['operation'] = 'update.recover'
            return report
        if value['state'] == 'prepared' and not fence.exists():
            value['fence']['owner_pid'] = os.getpid()
            value['fence']['owner_identity'] = maintenance.owner_identity()
            _journal(root, value)
            value = maintenance.claim_fence(root, identifier, fault=fault)
        elif not maintenance.confirmed_owner(root, value):
            raise ToolError(6, 'Recovery requires the positively identified recorded fence')
        elif not maintenance.owner_is_dead(value['fence']['owner_pid'], value['fence']['owner_identity']):
            raise ToolError(6, 'Recorded update owner remains live')
        if pointer is None:
            storage.atomic_json(storage.safe_path(root, '.novel-creator/local/update/active.json'),
                {'kind': 'active', 'document_version': 1, 'operation_id': identifier})
        try:
            with maintenance.legacy_exclusions(root, value):
                result = _finish(root, value, prepared, fault=fault or (lambda point: None))
                result['operation'] = 'update.recover'
                return result
        except (ToolError, OSError) as error:
            raise _operation_error(root, value, error) from error


def apply(novel, *, preview_id, version, expected_head, confirm_quiescent=False, fault=None):
    """Internal transaction; public CLI exposure awaits interruption qualification."""
    root = storage.root_path(novel)
    _require_external_controller(root)
    identifier = _identifier(preview_id)
    fault = fault or (lambda point: None)
    journal = maintenance.operation_path(root, identifier)
    if journal.exists():
        existing = maintenance.read_operation(root, identifier)
        report = status(root, operation_id=identifier)
        if (report['data']['ready'] and existing['preview']['target_version'] == version
                and existing['preview']['source_head'] == expected_head):
            report['operation'] = 'update.apply'
            return report
        raise ToolError(3, 'Update operation already exists; inspect external-controller recovery',
                        data={'operation_id': identifier})
    maintenance.ensure_ready(root)
    from .install import _preflight
    _preflight(root)
    document, source_inventory, raw = _load_preview(root, identifier)
    if version != document['target_version'] or expected_head != document['source_head']:
        raise ToolError(3, 'Apply requires the exact reviewed target and checkpoint')
    if release.stable_version(version) <= release.stable_version(document['source_version']):
        raise ToolError(3, 'Reviewed update must select a newer stable target')
    if document['source_manifest'].get('installation_format', 1) == 1 and not confirm_quiescent:
        raise ToolError(6, 'Close all other legacy book clients through apply/recovery, then explicitly confirm quiescence (FUP-001)')
    if fingerprint(root) != document['fingerprint']:
        raise ToolError(3, 'Book changed since preview; request a fresh preview')
    if release.runtime_info(document['runtime_python'])['fingerprint'] != document['runtime_fingerprint']:
        raise ToolError(3, 'Configured runtime changed since preview')
    prepared = release.prepare(document['artifact'], python=document['runtime_python'],
                               transport=_OfflineArtifact(document['artifact'], raw))
    if prepared['runtime']['fingerprint'] != document['runtime_fingerprint']:
        raise ToolError(3, 'Configured runtime changed during application preparation')
    manifest, raw_manifest = _read_manifest(root)
    if (manifest != document['source_manifest'] or release.digest(raw_manifest) != document['source_manifest_digest']
            or storage._branch_head(root) != (document['branch'], document['source_head'])):
        raise ToolError(3, 'Cached preview source identity/checkpoint differs from the current book')
    source = release.bundle_inventory(source_inventory, legacy=manifest.get('installation_format', 1) == 1)
    changes, target = _plan_changes(root, manifest, raw_manifest, source,
        source_inventory.get('novel_creator/codex/AGENTS.production.md'), prepared, identifier)
    if changes != document['changes'] or target != document['target_manifest']:
        raise ToolError(3, 'Cached preview differs from verified artifacts/current ownership')
    local = storage.safe_path(root, '.novel-creator/local/evidence').parent
    for receipt in local.glob('*.json'):
        state = storage.read_receipt(root, receipt)
        if state['cleanup_required'] or state['state'] != 'published':
            raise ToolError(3, 'Resolve pending story-save recovery before updating')
    paths = [item['path'] for item in changes]
    with maintenance.access_guard(root, exclusive=True):
        maintenance.ensure_ready(root)
        if fingerprint(root) != document['fingerprint']:
            raise ToolError(3, 'Book changed while preparing application')
        with tempfile.TemporaryDirectory(dir=_external_cache(root)) as folder:
            candidate = _candidate(root, document, Path(folder))
        value = {'kind': 'operation', 'document_version': 1, 'operation_id': identifier,
                 'preview': document, 'candidate': candidate, 'state': 'prepared',
                 'index_baseline': _index_rows(root, paths),
                 'fence': {'token': str(uuid.uuid4()), 'owner_pid': os.getpid(),
                           'owner_identity': maintenance.owner_identity(), 'ownership_confirmed': False,
                           'confirm_quiescent': confirm_quiescent}}
        _replace(root, _operation_file(root, identifier, 'target.whl').relative_to(root).as_posix(), raw, '100644')
        storage.atomic_json(_operation_file(root, identifier, 'baseline.json'),
            {'preview_digest': release.digest(release.canonical(document)), 'operational_digest': _operational_digest(root),
             'candidate': candidate, 'index_baseline_digest': release.digest(release.canonical(value['index_baseline']))})
        _journal(root, value)
        storage.atomic_json(storage.safe_path(root, '.novel-creator/local/update/active.json'),
                            {'kind': 'active', 'document_version': 1, 'operation_id': identifier})
        fault('after_preparation')
        try:
            value = maintenance.claim_fence(root, identifier, fault=fault)
            with maintenance.legacy_exclusions(root, value):
                return _finish(root, value, prepared, fault=fault)
        except (OSError, ToolError) as error:
            raise _operation_error(root, value, error) from error


def status(novel, *, operation_id=None):
    root = storage.root_path(novel)
    manifest, _ = _read_manifest(root)
    value = None
    try:
        value = maintenance.read_operation(root, operation_id) if operation_id else maintenance.active(root)
        fence = storage.safe_path(root, '.novel-creator/local/write.lock')
        if value is None and fence.exists():
            owner_path = storage.safe_path(root, '.novel-creator/local/write.lock/owner.json')
            if owner_path.exists():
                owner = records.loads(owner_path.read_bytes())
                if isinstance(owner, dict) and owner.get('update_operation'):
                    value = maintenance.read_operation(root, owner['update_operation'])
        if value is None:
            if fence.exists():
                return _result(root, manifest, operation='update.status', state='conflict',
                    blockers=[{'reason': 'ownership_unproven', 'path': '.novel-creator/local/write.lock'}],
                    next_action='Inspect existing persistence lock ownership; never remove it automatically.')
            return _result(root, manifest, operation='update.status', state='no_operation', ready=True,
                           next_action='Request an update check when needed.')
        source = value['preview']
        branch, head = storage._branch_head(root)
        blockers = []
        if fence.exists() and not maintenance.confirmed_owner(root, value):
            blockers.append({'reason': 'ownership_unproven', 'path': '.novel-creator/local/write.lock'})
        completed = value['state'] == 'complete' and not fence.exists() and maintenance.active(root) is None
        # Finished maintenance remains finished after subsequent writer commits.
        # Incomplete transactions still require their exact original checkpoints.
        checkpoint_valid = (bool(head) and (head == value['candidate'] or not storage.git(
            root, '--no-replace-objects', 'merge-base', '--is-ancestor', value['candidate'], head, check=False).returncode)
            if completed else head in (source['source_head'], value['candidate']))
        if branch != source['branch'] or not checkpoint_valid:
            state = 'conflict'
            blockers.append({'reason': 'checkpoint_changed'})
        elif completed:
            state = 'complete'
            if source['changes']:
                baseline = records.loads(_operation_file(root, value['operation_id'], 'baseline.json').read_bytes())
                if (baseline['candidate'] != value['candidate']
                        or baseline['preview_digest'] != release.digest(release.canonical(source))
                        or manifest != source['target_manifest']):
                    raise ToolError(3, 'Completed update evidence changed')
                for change in source['changes']:
                    path = storage.safe_path(root, change['path'], setup=True)
                    identity = _file_identity(path)
                    actual = path.read_bytes() if identity else None
                    expected = base64.b64decode(change['after'], validate=True) if change['after'] is not None else None
                    if (actual != expected or (identity['mode'] if identity else None) != change['after_mode']):
                        raise ToolError(3, 'Completed update path changed', affected_refs=[change['path']])
            for path, checksum in source['target_manifest'].get('checksums', {}).items():
                identity = _file_identity(storage.safe_path(root, path, setup=True))
                expected_mode = source['target_manifest'].get('ownership', {}).get('exclusive', {}).get(path, {}).get('mode', '100644')
                if identity is None or identity['sha256'] != checksum or identity['mode'] != expected_mode:
                    state = 'conflict'
                    blockers.append({'reason': 'installed_resource_changed', 'path': path})
        elif head == value['candidate'] and head != source['source_head']:
            state = 'published'
        else:
            state = 'pending'
        return _result(root, manifest, operation='update.status', state=state,
            target=source['target_version'], identifier=source['preview_id'], operation_id=value['operation_id'],
            blockers=blockers, ready=state == 'complete', cleanup=state != 'complete', runtime_python=source['runtime_python'],
            next_action='Update complete.' if state == 'complete' else 'Preserve operation evidence and use external-controller recovery.')
    except (OSError, ValueError, TypeError, KeyError, ToolError) as error:
        if isinstance(error, ToolError) and error.code == 2:
            raise
        return _result(root, manifest, operation='update.status', state='conflict', operation_id=operation_id,
                       blockers=[{'reason': 'evidence_unavailable'}], cleanup=True,
                       next_action='Preserve maintenance evidence and inspect it before any retry.')
