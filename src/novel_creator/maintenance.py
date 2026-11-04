"""Durable maintenance pause and cooperating-operation exclusion.

Legacy writer fences persist after interruption. Only matching, confirmed
ownership permits recovery; an empty lock directory is never ours by inference.
"""
from contextlib import contextmanager, ExitStack
from contextvars import ContextVar
from functools import wraps
import os
from pathlib import Path
import uuid

from .cli import ToolError
from . import records


_normal_roots = ContextVar('novel_creator_normal_operations', default=frozenset())
_verification = ContextVar('novel_creator_read_verification', default=None)


@contextmanager
def access_guard(root, *, exclusive=False):
    """Ordinary operations share a lease; maintenance excludes all of them.

    Revocation must remain independent of another contribution's in-flight
    work. Serializing every normal operation would break that existing rule.
    """
    path = _path(root, '.novel-creator/local/update/access.guard')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if os.name == 'nt':
            import ctypes
            import msvcrt
            from ctypes import wintypes
            class Overlapped(ctypes.Structure):
                _fields_ = [('Internal', ctypes.c_size_t), ('InternalHigh', ctypes.c_size_t),
                            ('Offset', wintypes.DWORD), ('OffsetHigh', wintypes.DWORD),
                            ('hEvent', wintypes.HANDLE)]
            api = ctypes.WinDLL('kernel32', use_last_error=True)
            api.LockFileEx.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
                                       wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(Overlapped)]
            api.UnlockFileEx.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD,
                                         wintypes.DWORD, ctypes.POINTER(Overlapped)]
            handle = wintypes.HANDLE(msvcrt.get_osfhandle(stream.fileno()))
            overlapped = Overlapped()
            if not api.LockFileEx(handle, 1 | (2 if exclusive else 0), 0, 1, 0, ctypes.byref(overlapped)):
                raise ToolError(6, 'Book maintenance or a cooperating operation is active')
            try:
                yield
            finally:
                # Closing this handle also releases its lease if explicit unlock
                # fails. Do not replace a published operation's result here.
                api.UnlockFileEx(handle, 0, 1, 0, ctypes.byref(overlapped))
        else:
            import fcntl
            try:
                fcntl.flock(stream.fileno(), (fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH) | fcntl.LOCK_NB)
            except OSError as error:
                raise ToolError(6, 'Book maintenance or a cooperating operation is active') from error
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _path(root, relative):
    from .storage import safe_path
    return safe_path(Path(root), relative)


def operation_path(root, identifier):
    try:
        if str(uuid.UUID(identifier)) != identifier:
            raise ValueError()
    except (TypeError, ValueError, AttributeError) as error:
        raise ToolError(2, 'Invalid update operation identity') from error
    return _path(root, '.novel-creator/local/update/operations/' + identifier + '/journal.json')


def read_operation(root, identifier):
    from .update_release import validate_document
    try:
        value = validate_document('operation', records.loads(operation_path(root, identifier).read_bytes()))
        if value['operation_id'] != identifier or Path(value['preview']['novel_root']) != Path(root):
            raise ValueError()
        return value
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise ToolError(3, 'Update evidence is unavailable or changed; preserve it before recovery') from error


def active(root):
    from .update_release import validate_document
    path = _path(root, '.novel-creator/local/update/active.json')
    if not path.exists():
        return None
    try:
        pointer = validate_document('active', records.loads(path.read_bytes()))
        return read_operation(root, pointer['operation_id'])
    except (OSError, ValueError, TypeError, KeyError, ToolError) as error:
        raise ToolError(6, 'Update maintenance evidence requires external-controller inspection') from error


def ensure_ready(root, *, read_only=False):
    root = Path(root).absolute()
    value = active(root)
    if value is None:
        owner = _path(root, '.novel-creator/local/write.lock/owner.json')
        if owner.is_file():
            try:
                if records.loads(owner.read_bytes()).get('update_operation'):
                    raise ToolError(6, 'Update fence remains; inspect external-controller recovery')
            except (OSError, ValueError, AttributeError) as error:
                raise ToolError(6, 'Persistence lock metadata requires inspection') from error
        return
    permission = _verification.get()
    if read_only and permission == (str(root), value['operation_id'], value['fence']['token']):
        from .storage import head
        if value['state'] in ('verifying', 'complete') and head(root) == value['candidate']:
            return
    raise ToolError(6, 'Book update is incomplete; use the external updater status/recovery command')


@contextmanager
def normal_operation(root):
    from .storage import root_path
    root = root_path(root)
    key = str(root)
    if key in _normal_roots.get():
        yield
        return
    ensure_ready(root)
    with access_guard(root):
        ensure_ready(root)
        token = _normal_roots.set(_normal_roots.get() | {key})
        try:
            yield
        finally:
            _normal_roots.reset(token)


def guarded_mutation(function):
    @wraps(function)
    def guarded(self, *args, **kwargs):
        with normal_operation(self.root):
            return function(self, *args, **kwargs)
    return guarded


def owner_identity():
    """Bind the current holder to a process lifetime, not just a reused PID."""
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL('kernel32', use_last_error=True)
        api.GetCurrentProcess.restype = wintypes.HANDLE
        api.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        times = [wintypes.FILETIME() for _ in range(4)]
        if not api.GetProcessTimes(api.GetCurrentProcess(), *(ctypes.byref(value) for value in times)):
            raise ToolError(6, 'Process identity is unavailable; do not acquire update ownership')
        return 'windows:' + str((times[0].dwHighDateTime << 32) | times[0].dwLowDateTime)
    try:
        fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        return 'linux:' + boot + ':' + fields[19]
    except (OSError, IndexError) as error:
        raise ToolError(6, 'Process identity is unavailable; do not acquire update ownership') from error


def owner_is_dead(pid, identity):
    """Prove the recorded process lifetime ended; uncertainty never permits retry."""
    import re
    pattern = r'windows:[0-9]+' if os.name == 'nt' else r'linux:[0-9a-f-]{36}:[0-9]+'
    if type(pid) is not int or pid < 1 or not isinstance(identity, str) or not re.fullmatch(pattern, identity):
        raise ToolError(6, 'Recorded process lifetime identity is invalid or unsupported')
    if pid == os.getpid():
        return identity != owner_identity()
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL('kernel32', use_last_error=True)
        api.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        api.OpenProcess.restype = wintypes.HANDLE
        api.CloseHandle.argtypes = [wintypes.HANDLE]
        api.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        api.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        api.WaitForSingleObject.restype = wintypes.DWORD
        handle = api.OpenProcess(0x1000 | 0x100000, False, pid)
        if not handle:
            if ctypes.get_last_error() == 87:  # No process exists with this PID.
                return True
            raise ToolError(6, 'Cannot prove the update owner process ended')
        try:
            observed = api.WaitForSingleObject(handle, 0)
            if observed == 0:
                return True
            if observed != 258:
                raise ToolError(6, 'Cannot determine whether the recorded updater still runs')
            times = [wintypes.FILETIME() for _ in range(4)]
            if not api.GetProcessTimes(handle, *(ctypes.byref(value) for value in times)):
                raise ToolError(6, 'Update process lifetime is unavailable')
            actual = 'windows:' + str((times[0].dwHighDateTime << 32) | times[0].dwLowDateTime)
            if not identity.startswith('windows:'):
                raise ToolError(6, 'Recorded process platform is unsupported for recovery')
            return actual != identity
        finally:
            api.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    except PermissionError as error:
        raise ToolError(6, 'Update owner process cannot be inspected') from error
    try:
        fields = Path('/proc/' + str(pid) + '/stat').read_text().rsplit(')', 1)[1].split()
        if fields[0] == 'Z':
            return True
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        if not identity.startswith('linux:'):
            raise ToolError(6, 'Recorded process platform is unsupported for recovery')
        return identity != 'linux:' + boot + ':' + fields[19]
    except (OSError, IndexError) as error:
        raise ToolError(6, 'Cannot prove the recorded update process lifetime ended') from error


def claim_fence(root, identifier, *, fault=None):
    """Caller holds access.guard; retain all acquisition evidence on failure."""
    from . import storage
    fault = fault or (lambda point: None)
    value = read_operation(root, identifier)
    if value['state'] != 'prepared' or value['fence']['ownership_confirmed']:
        raise ToolError(3, 'Update is not at its original fence acquisition checkpoint')
    if (value['fence']['owner_pid'] != os.getpid()
            or value['fence']['owner_identity'] != owner_identity()):
        raise ToolError(6, 'Prepared operation belongs to another process lifetime')
    fence = _path(root, '.novel-creator/local/write.lock')
    try:
        fence.mkdir()
    except FileExistsError as error:
        raise ToolError(6, 'Persistence fence ownership is unproven or held; never take it over') from error
    fault('before_fence_owner')
    owner = {'update_operation': identifier, 'token': value['fence']['token'],
             'pid': os.getpid(), 'identity': value['fence']['owner_identity']}
    storage.atomic_json(_path(root, '.novel-creator/local/write.lock/owner.json'), owner)
    storage.fsync_directory(fence.parent)
    fault('before_fence_confirmation')
    value['state'] = 'fenced'
    value['fence']['ownership_confirmed'] = True
    storage.atomic_json(operation_path(root, identifier), value)
    fault('after_fence_confirmation')
    return value


def confirmed_owner(root, value):
    try:
        owner = records.loads(_path(root, '.novel-creator/local/write.lock/owner.json').read_bytes())
        expected = {'update_operation': value['operation_id'], 'token': value['fence']['token'],
                    'pid': value['fence']['owner_pid'], 'identity': value['fence']['owner_identity']}
        return bool(value['fence']['ownership_confirmed']) and owner == expected
    except (OSError, ValueError, KeyError):
        return False


@contextmanager
def read_verification(root, identifier, token):
    value = read_operation(root, identifier)
    if token != value['fence']['token'] or not confirmed_owner(root, value):
        raise ToolError(6, 'Read-only verification requires confirmed update ownership')
    permission = _verification.set((str(Path(root).absolute()), identifier, token))
    try:
        yield
    finally:
        _verification.reset(permission)


def retro_snapshot(root):
    """Inspect local typed documents without rendering notices or reconciling work."""
    from importlib.resources import files
    from .retro import validate, guarded
    base = _path(root, '.novel-creator/local/retro')
    documents = []
    kinds = records.loads(files('novel_creator.schemas.v1').joinpath('retro.schema.json').read_bytes())['$defs']
    if base.exists():
        for path in sorted(base.rglob('*.json')):
            checked = _path(root, path.relative_to(root).as_posix())
            try:
                value = records.loads(checked.read_bytes())
                kind = value.get('document')
                if kind not in kinds:
                    raise ValueError()
                validate(value, kind)
            except (OSError, ValueError, TypeError, AttributeError, ToolError) as error:
                raise ToolError(4, 'Retrospective evidence is invalid; preserve it before updating') from error
            documents.append({'kind': kind, 'value': value})
    grant_path = _path(root, '.novel-creator/local/retro/authorization.json')
    try:
        grant = records.loads(grant_path.read_bytes()) if grant_path.exists() else None
        if grant is not None:
            validate(grant, 'authorization')
    except (ValueError, TypeError, OSError, ToolError) as error:
        raise ToolError(4, 'Retrospective authorization changed or is invalid') from error
    machine = None
    machine_digest = None
    if grant:
        registry = (Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local')) / 'NovelCreator/retro/grants'
                    if os.name == 'nt' else
                    Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'novel-creator/retro/grants')
        candidate = guarded(registry / (grant['grant_id'] + '.json'))
        if candidate.exists():
            try:
                raw = candidate.read_bytes()
                machine = records.loads(raw)
                validate(machine, 'authorization')
            except (ValueError, TypeError, OSError, ToolError) as error:
                raise ToolError(4, 'Machine grant evidence changed or is invalid') from error
            import hashlib
            machine_digest = hashlib.sha256(raw).hexdigest()
    try:
        novel_id = records.loads(_path(root, '.novel-creator/manifest.json').read_bytes())['novel_id']
    except (ValueError, TypeError, OSError, KeyError) as error:
        raise ToolError(4, 'Book identity is unavailable for retrospective binding inspection') from error
    return {'documents': documents, 'grant': grant, 'machine_grant': machine,
            'machine_grant_digest': machine_digest, 'novel_root': str(root), 'novel_id': novel_id}


def require_quiet_retro(snapshot):
    terminal = {'published', 'abandoned', 'duplicate', 'no_action', 'insufficient_evidence'}
    grant = snapshot['grant']
    bound = (grant and grant['enabled'] and grant == snapshot['machine_grant']
             and grant['novel_root'] == snapshot['novel_root'] and grant['novel_id'] == snapshot['novel_id'])
    for item in snapshot['documents']:
        value = item['value']
        if item['kind'] == 'run':
            if value['status'] not in terminal:
                raise ToolError(3, 'Unfinished retrospective work must be resolved before updating')
            if value.get('contribution') and not bound:
                raise ToolError(3, 'Retained contribution ownership needs separately authorized recovery')
            if value.get('contribution') and value['contribution']['stage'] in ('push_intent', 'pushed', 'create_intent', 'publication_unknown'):
                raise ToolError(3, 'Uncertain retrospective publication must be resolved separately')
        if item['kind'] == 'reservation' and value['state'] == 'reserved':
            raise ToolError(3, 'A pending notice reservation must be resolved before updating')
        if item['kind'] == 'notice' and value['state'] == 'reserved':
            raise ToolError(3, 'A reserved retrospective notice must be reconciled before updating')


@contextmanager
def legacy_exclusions(root, value):
    """Bridge shipped 0.2 bookkeeping locks, without invoking its service APIs."""
    from . import storage
    from .retro import inspection_guard, guarded
    if not confirmed_owner(root, value):
        raise ToolError(6, 'Legacy exclusion requires confirmed update fence ownership')
    base = _path(root, '.novel-creator/local/retro')
    with ExitStack() as stack:
        if base.exists():
            stack.enter_context(inspection_guard(base, 'state.lock.guard'))
            stack.enter_context(inspection_guard(base, 'authorization.lock.guard'))
            for path in sorted((base / 'runs').glob('*.json')):
                try:
                    if str(uuid.UUID(path.stem)) != path.stem:
                        raise ValueError()
                except ValueError as error:
                    raise ToolError(4, 'Invalid retrospective run identity') from error
                stack.enter_context(inspection_guard(base / 'runs', path.stem + '.lock.guard'))
        state = retro_snapshot(root)
        require_quiet_retro(state)
        grant = state['grant']
        # A disabled/unbound grant never authorizes external checkout inspection.
        if (grant and grant['enabled'] and grant == state['machine_grant']
                and grant['novel_id'] == value['preview']['novel_id'] and grant['novel_root'] == str(root)):
            checkout, common = guarded(grant['checkout_root']), guarded(grant['git_common_dir'])
            if (not checkout.is_absolute() or not common.is_absolute()
                    or checkout.is_relative_to(root) or root.is_relative_to(checkout)
                    or common.is_relative_to(root) or root.is_relative_to(common)):
                raise ToolError(3, 'Retrospective checkout binding is unsafe')
            actual = storage.git(checkout, 'rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip()
            if Path(actual).resolve() != common:
                raise ToolError(3, 'Retrospective repository binding changed')
            external = guarded(common / 'novel-creator-retro')
            stack.enter_context(inspection_guard(external))
            if guarded(external / 'operation.lock').exists() or guarded(external / 'owner.json').exists():
                raise ToolError(6, 'Contribution repository ownership needs separate completion or recovery')
        yield state
