"""Opt-in local contribution state. Story transactions remain the only story authority."""
from contextlib import contextmanager, nullcontext
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import uuid
from importlib.resources import files

from jsonschema import Draft202012Validator, FormatChecker

from . import records, storage
from .cli import ToolError
from .retro_github import Github, REPOSITORY, canonical_origin, git as contribution_git


class StaleRunError(ToolError):
    """A delayed command must not journal a failure against a newer receipt."""


def uid():
    return str(uuid.uuid4())


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def privacy_check(text, *, private_values):
    """Defense in depth only. Host semantic approval is separately required."""
    if (not isinstance(text, str) or not text.strip() or '\x00' in text or
        re.search(r'(?i)(?:[a-z]:[\\/]|/(?:home|users|tmp|var|private)/|'
                  r'\.novel-creator|sk-[a-z0-9_-]{12,}|(?:password|token|secret)\s*[=:])', text) or
        any(value and len(value) >= 8 and value.casefold() in text.casefold() for value in private_values)):
        raise ToolError(3, 'Contribution material requires safe generalization')


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(storage.UUID, value):
        raise ToolError(2, 'Expected a canonical UUID')
    return value


def guarded(path):
    path = Path(path).absolute()
    if '..' in path.parts:
        raise ToolError(2, 'Traversing operational path is not allowed')
    for parent in [*reversed(path.parents), path]:
        try:
            mode = storage._path_mode(parent)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode) or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise ToolError(2, 'Redirected or special operational path is not allowed')
    return path


def document(kind, **values):
    return dict(retro_version=1, document=kind, **values)


def validate(value, kind):
    try:
        schema = records.loads(files('novel_creator.schemas.v1').joinpath('retro.schema.json').read_bytes())
        validator = Draft202012Validator({'$ref': '#/$defs/' + kind, '$defs': schema['$defs']},
                                        format_checker=FormatChecker())
        if not validator.is_valid(value):
            raise ValueError()
    except (ValueError, TypeError) as error:
        raise ToolError(2, 'Invalid or unsupported retrospective state/input') from error
    return value


def load(path, kind, default=None):
    path = guarded(path)
    if not path.exists():
        return default
    if not path.is_file():
        raise ToolError(2, 'Operational document must be an ordinary file')
    try:
        return validate(records.loads(path.read_bytes()), kind)
    except (ValueError, UnicodeError) as error:
        raise ToolError(2, 'Operational document is not valid UTF-8 JSON') from error


def write(path, value, kind):
    path = guarded(path)
    validate(value, kind)
    path.parent.mkdir(parents=True, exist_ok=True)
    storage.atomic_json(path, value)


@contextmanager
def inspection_guard(base, name='inspection.guard'):
    """OS advisory lock: released on process death, also shared by lock acquisition."""
    base = guarded(base)
    base.mkdir(parents=True, exist_ok=True)
    path = guarded(base / name)
    with path.open('a+b') as stream:
        if stream.seek(0, 2) == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        acquired = False
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
            yield
        except OSError as error:
            if acquired:
                raise  # Preserve operation failures; only acquisition is a held-lock error.
            raise ToolError(6, 'Operation inspection is held or unavailable') from error
        finally:
            if acquired:
                stream.seek(0)
                if os.name == 'nt':
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


@contextmanager
def lock(path, *, owner=None):
    path = guarded(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.name != 'operation.lock':
        # Local bookkeeping needs exclusion, not persistent repository ownership.
        # The OS releases this lock even if the host dies without running finally.
        with inspection_guard(path.parent, path.name + '.guard'):
            yield
        return
    token = uid()
    def mutex():
        return inspection_guard(path.parent) if path.name == 'operation.lock' else nullcontext()
    with mutex():
        try:
            path.mkdir()
        except FileExistsError as error:
            raise ToolError(6, 'Retrospective lock held; inspect ownership before retry') from error
        metadata = document('lock', pid=os.getpid(), token=token)
        if owner is not None:
            metadata['owner'] = owner
        storage.atomic_json(path / 'holder.json', metadata)
    try:
        yield
    finally:
        with mutex():
            holder = path / 'holder.json'
            try:
                value = records.loads(holder.read_bytes())
            except (OSError, ValueError):
                value = None
            if value and value.get('token') == token:
                # Remove the lock name atomically while its identity still exists.
                # A crash during later cleanup leaves only a private quarantine.
                released = guarded(path.parent / ('released-' + token))
                path.rename(released)
                guarded(released / 'holder.json').unlink()
                released.rmdir()


def process_alive(pid):
    """Return False only when process death is positively established; never kill."""
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        api = ctypes.WinDLL('kernel32', use_last_error=True)
        api.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        api.OpenProcess.restype = wintypes.HANDLE
        api.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        api.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = api.OpenProcess(0x1000, False, pid)  # Query limited information only.
        if not handle:
            return ctypes.get_last_error() not in (87, 1168)
        try:
            code = wintypes.DWORD()
            return not api.GetExitCodeProcess(handle, ctypes.byref(code)) or code.value == 259
        finally:
            api.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except (PermissionError, OSError):
        return True


class Retro:
    def __init__(self, novel, *, github=None, registry=None):
        self.root = storage.root_path(novel)
        manifest = records.loads(storage.safe_path(self.root, '.novel-creator/manifest.json').read_bytes())
        self.novel_id = identifier(manifest.get('novel_id'))
        self.local = storage.safe_path(self.root, '.novel-creator/local/retro')
        self.github = github if github is not None else Github()
        if registry is None:
            if os.name == 'nt':
                registry = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local')) / 'NovelCreator/retro/grants'
            else:
                registry = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'novel-creator/retro/grants'
        self.registry = guarded(registry)

    def path(self, name):
        return guarded(self.local / name)

    def grant(self):
        return load(self.path('authorization.json'), 'authorization')

    def separate_repository_path(self, path):
        path = guarded(path)
        if (path.resolve() != path or self.root.is_relative_to(path) or path.is_relative_to(self.root)):
            raise ToolError(3, 'Framework checkout and Git storage must be separate canonical roots from the novel')
        return path

    def bound(self):
        grant = self.grant()
        if not grant or not grant['enabled']:
            return None
        if grant['novel_id'] != self.novel_id or grant['novel_root'] != str(self.root):
            return None
        # Pure local binding check: status/disabled paths never inspect framework storage.
        for name in ('checkout_root', 'git_common_dir'):
            path = Path(grant[name])
            if self.root.is_relative_to(path) or path.is_relative_to(self.root):
                return None
        machine = load(self.registry / (grant['grant_id'] + '.json'), 'authorization')
        return grant if machine == grant else None

    def status(self, run=None):
        grant = self.bound()
        result = {'enabled': bool(grant), 'binding_valid': bool(grant),
                  'repository': REPOSITORY, 'latest_run': None}
        if run:
            item = self.run(run)
            result['latest_run'] = {k: item[k] for k in ('run_id', 'status', 'reason_code')}
        else:
            paths = sorted(self.path('runs').glob('*.json'))
            if paths:
                item = load(max(paths, key=lambda p: p.stat().st_mtime_ns), 'run')
                result['latest_run'] = {k: item[k] for k in ('run_id', 'status', 'reason_code')}
        if result['latest_run'] and item.get('remote_outcome'):
            outcome = item['remote_outcome']
            result['latest_run']['remote_outcome'] = outcome['kind']
            result['latest_run']['pr'] = self.public_reference(outcome['pr'])
        if result['latest_run'] and item['contribution'] and item['contribution'].get('diagnostics'):
            attempt = item['contribution']['diagnostics'][-1]
            result['latest_run']['validation'] = dict(attempt_id=attempt['attempt_id'], state=attempt['state'],
                                                     checks=len(attempt['checks']))
        return result

    def enable(self, checkout, *, authorize=False):
        if not authorize:
            raise ToolError(2, 'Explicit draft-PR authorization is required')
        checkout = self.separate_repository_path(checkout)
        top = storage.git(checkout, 'rev-parse', '--show-toplevel').decode().strip()
        if Path(top).resolve() != checkout:
            raise ToolError(3, 'Select the framework repository root')
        canonical_origin(storage.git(checkout, 'remote', 'get-url', 'origin').decode().strip())
        # Reject all rewrite rules before any GitHub request or repository mutation.
        rewrite = storage.git(checkout, 'config', '--get-regexp', r'^url\..*\.(insteadOf|pushInsteadOf)$', check=False)
        if rewrite.returncode == 0:
            raise ToolError(3, 'Git URL rewrites require inspection before participation')
        common = Path(storage.git(checkout, 'rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip())
        common = self.separate_repository_path(common)
        identity = self.github.identity()
        if identity['repository'] != REPOSITORY:
            raise ToolError(3, 'Repository identity changed')
        with lock(self.path('authorization.lock')):
            old = self.grant()
            grant = document('authorization', enabled=True, grant_id=old['grant_id'] if old else uid(),
                             generation=old['generation'] + 1 if old else 1,
                             novel_id=self.novel_id, novel_root=str(self.root), checkout_root=str(checkout),
                             git_common_dir=str(common), repository=REPOSITORY,
                             github_login=identity['login'], authorization_source='direct_cli')
            # Registry first; until both agree enabled state is unusable.
            write(self.registry / (grant['grant_id'] + '.json'), grant, 'authorization')
            write(self.path('authorization.json'), grant, 'authorization')
        return self.status()

    def disable(self):
        with lock(self.path('authorization.lock')):
            grant = self.grant()
            if grant:
                grant.update(enabled=False, generation=grant['generation'] + 1)
                write(self.path('authorization.json'), grant, 'authorization')
                write(self.registry / (grant['grant_id'] + '.json'), grant, 'authorization')
        return self.status()

    def require(self, run=None):
        grant = self.bound()
        if not grant:
            raise ToolError(3, 'Re-enablement required; no further framework or GitHub access permitted')
        for name in ('checkout_root', 'git_common_dir'):
            self.separate_repository_path(grant[name])
        if run and (run['grant_id'] != grant['grant_id'] or run['authorization_generation'] != grant['generation']):
            raise ToolError(3, 'Authorization generation changed; explicitly resume existing work')
        return grant

    def run(self, run_id):
        item = load(self.path('runs/' + identifier(run_id) + '.json'), 'run')
        if item is None:
            raise ToolError(3, 'Requested retrospective run is unavailable')
        return item

    def save_run(self, item):
        write(self.path('runs/' + item['run_id'] + '.json'), item, 'run')

    def run_lock(self, run_id):
        # Shared by contribution operations and local failure journaling. This
        # never holds the novel writer lock or prevents authorization revocation.
        return lock(self.path('runs/' + identifier(run_id) + '.lock'))

    def current_run(self, item):
        if self.run(item['run_id']) != item:
            raise StaleRunError(3, 'Retrospective state changed; resume the current receipt before retrying')

    def history(self, *, allow_pause=False):
        if not allow_pause:
            if storage.safe_path(self.root, '.novel-creator/local/write.lock').exists():
                raise ToolError(6, 'Novel persistence is locked')
            for path in (self.root / '.novel-creator/local').glob('*.json'):
                receipt = storage.read_receipt(self.root, path)
                if receipt['state'] == 'pending' or receipt['cleanup_required']:
                    raise ToolError(3, 'Novel persistence is paused; recover before retrospective work')
        history = storage.read_history(self.root)
        if not history or history[0]['novel_id'] != self.novel_id:
            raise ToolError(4, 'Confirmed novel history is unavailable')
        return history

    def checkpoint(self, exchange_id, checkpoint):
        history = self.history()
        if not any(e['exchange_id'] == exchange_id for e in history):
            raise ToolError(3, 'Completion exchange is not confirmed')
        if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', checkpoint):
            raise ToolError(2, 'Expected a confirmed commit identity')
        result = storage.git(self.root, 'merge-base', '--is-ancestor', checkpoint, 'HEAD', check=False)
        if result.returncode or not any(e['exchange_id'] == exchange_id for e in storage.read_history(self.root, checkpoint)):
            raise ToolError(3, 'Completion checkpoint is stale or unavailable')

    def begin(self, data):
        if not self.bound():
            return {'eligible': False, 'review_required': False}
        validate(data, 'begin')
        if not all(data[k].strip() for k in ('thread_id', 'initiating_turn_id')):
            raise ToolError(2, 'Stable public task identity is required')
        grant = self.require()
        self.checkpoint(data['completion_exchange_id'], data['checkpoint'])
        key = digest(json.dumps([self.novel_id, data['host_kind'], data['thread_id'],
                                 data['initiating_turn_id']], ensure_ascii=False).encode())
        with lock(self.path('state.lock')):
            index = load(self.path('index.json'), 'index', document('index', claims={}))
            # A crash between immutable run publication and index update cannot create a second run.
            for path in self.path('runs').glob('*.json'):
                item = load(path, 'run')
                if item['task_key'] == key:
                    index['claims'][key] = item['run_id']
                    write(self.path('index.json'), index, 'index')
                    return {'eligible': True, 'run_id': item['run_id'], 'review_required': False}
            if key in index['claims']:
                raise ToolError(3, 'Claim index references unavailable work; inspect before retry')
            item = document('run', run_id=uid(), task_key=key,
                completion_exchange_id=data['completion_exchange_id'], checkpoint=data['checkpoint'],
                grant_id=grant['grant_id'], authorization_generation=grant['generation'],
                bindings={k: grant[k] for k in ('checkout_root', 'git_common_dir', 'github_login')},
                status='claimed', reason_code='', evidence_refs=[], finding=None,
                contribution=None, notice=None)
            self.require()
            self.save_run(item)
            index['claims'][key] = item['run_id']
            write(self.path('index.json'), index, 'index')
            return {'eligible': True, 'run_id': item['run_id'], 'review_required': True}

    def private_values(self):
        values = [str(self.root), self.novel_id]
        for exchange in self.history(allow_pause=True):
            values.extend(m['text'] for m in exchange['messages'] if len(m['text']) >= 12)
        return values

    def review(self, run_id, data):
        validate(data, 'review')
        with lock(self.path('state.lock')):
            item = self.run(run_id)
            self.require(item)
            self.checkpoint(item['completion_exchange_id'], item['checkpoint'])
            if item['status'] not in ('claimed', 'reviewing'):
                raise ToolError(3, 'Review already completed or unavailable')
            if data['outcome'] == 'selected':
                if set(data) != {'outcome','category','problem','reproduction','evidence_refs'} or not data['evidence_refs']:
                    raise ToolError(2, 'A selected correction requires category, reproduction and local evidence')
                ids = {e['exchange_id'] for e in self.history()}
                if not set(data['evidence_refs']).issubset(ids):
                    raise ToolError(3, 'Review evidence is unavailable')
                privacy_check(data['problem'] + '\n' + data['reproduction'], private_values=self.private_values())
                item['finding'] = {k: data[k] for k in ('category','problem','reproduction')}
                item['evidence_refs'] = data['evidence_refs']
            elif set(data) != {'outcome'}:
                raise ToolError(2, 'No-action review must not carry a proposed finding')
            item['status'] = data['outcome']
            if data['outcome'] == 'insufficient_evidence':
                self.notice(item, 'Retrospective skipped: sufficient evidence was unavailable.')
            self.save_run(item)
            return {'run_id': run_id, 'status': item['status']}

    def notice(self, item, text, url=None):
        kind = 'published' if url else ('insufficient' if item['status'] == 'insufficient_evidence' else 'problem')
        notice_id = str(uuid.uuid5(uuid.UUID(item['run_id']), json.dumps([kind, item['reason_code'], url])))
        path = self.path('notices/' + notice_id + '.json')
        existing = load(path, 'notice')
        if existing:
            item['notice'] = existing  # Preserve rendering, reservation and immutable acknowledgement.
            return
        item['notice'] = document('notice', notice_id=notice_id, text=text, text_digest=digest(text.encode()), url=url,
                              state='pending', reservation_id=None, included_exchange_id=None,
                              language='en', notice_kind=kind,
                              reason_code=item['reason_code'])
        write(self.path('notices/' + item['notice']['notice_id'] + '.json'), item['notice'], 'notice')

    def notice_items(self):
        result = {}
        for path in self.path('notices').glob('*.json'):
            value = load(path, 'notice')
            if value['notice_id'] in result:
                raise ToolError(3, 'Notice identity is ambiguous')
            result[value['notice_id']] = value
        return result

    def notices_pending(self, language=None):
        if language not in (None, 'en', 'is'):
            raise ToolError(2, 'Supported notice interaction languages are en and is')
        with lock(self.path('state.lock')):
            notices = self.notice_items()
            reserved = set()
            reservations = []
            for path in self.path('reservations').glob('*.json'):
                value = load(path, 'reservation')
                if value['state'] == 'reserved':
                    reservations.append(value['reservation_id'])
                    reserved.update(n['notice_id'] for n in value['notices'])
            for key, note in notices.items():
                if language and note['state'] == 'pending' and key not in reserved and note['language'] != language:
                    text = self.render_notice(note, language)
                    note.update(text=text, text_digest=digest(text.encode()), language=language)
                    write(self.path('notices/' + key + '.json'), note, 'notice')
            return {'notices': [notices[k] for k in sorted(notices)
                                if notices[k]['state'] == 'pending' and k not in reserved],
                    'reservations': sorted(reservations)}

    @staticmethod
    def render_notice(note, language):
        if note['notice_kind'] == 'published':
            return ('Endurskoðun bjó til drög að breytingatillögu: ' if language == 'is' else
                    'Retrospective created a draft PR: ') + note['url']
        if note['notice_kind'] == 'insufficient':
            return ('Endurskoðun sleppt: næg gögn voru ekki tiltæk.' if language == 'is' else
                    'Retrospective skipped: sufficient evidence was unavailable.')
        if language == 'is':
            reasons = {'validation_failed': 'nauðsynlegt próf mistókst',
                       'validation_unavailable': 'nauðsynlegt próf var ekki tiltækt',
                       'publication_unknown': 'óvissa um birtingu',
                       'push_outcome_unknown': 'óvissa um sendingu breytinga',
                       'upstream_changed': 'grunnur frumkóðans hefur breyst',
                       'validation_invalidated': 'breytingin hefur breyst eftir prófun'}
            return 'Framlag endurskoðunar er stöðvað: ' + reasons.get(note['reason_code'], 'skoða þarf staðbundna stöðu') + '.'
        return 'Retrospective contribution blocked: ' + note['reason_code'].replace('_', ' ') + '.'

    def notices_reserve(self, data):
        validate(data, 'reservation_input')
        with lock(self.path('state.lock')):
            path = self.path('reservations/' + identifier(data['reservation_id']) + '.json')
            expected = document('reservation', **{k: v for k,v in data.items() if k != 'retro_version'}, state='reserved')
            existing = load(path, 'reservation')
            if existing:
                if {k: v for k,v in existing.items() if k != 'state'} != {k: v for k,v in expected.items() if k != 'state'}:
                    raise ToolError(3, 'Reservation identity is already bound to another exchange')
                return {'reservation_id': existing['reservation_id'], 'state': existing['state']}
            items = self.notice_items()
            occupied = set()
            for other in self.path('reservations').glob('*.json'):
                value = load(other, 'reservation')
                if value['state'] == 'reserved':
                    occupied.update(n['notice_id'] for n in value['notices'])
            seen = set()
            end = 0
            for span in data['notices']:
                note = items.get(span['notice_id'])
                if (not note or note['state'] != 'pending' or span['notice_id'] in occupied or
                    span['notice_id'] in seen or note['text_digest'] != span['text_digest'] or
                    span['start_byte'] < end or span['end_byte'] <= span['start_byte'] or
                    span['end_byte'] - span['start_byte'] != len(note['text'].encode())):
                    raise ToolError(3, 'Notice reservation conflicts with pending content or spans')
                seen.add(span['notice_id'])
                end = span['end_byte']
            # The reservation is the durable batch intent; individual updates are recoverable.
            write(path, expected, 'reservation')
            for span in data['notices']:
                note = items[span['notice_id']]
                note.update(state='reserved', reservation_id=data['reservation_id'])
                write(self.path('notices/' + note['notice_id'] + '.json'), note, 'notice')
            return {'reservation_id': data['reservation_id'], 'state': 'reserved'}

    def notices_confirm(self, reservation):
        return self._notice_result(reservation, allow_release=False)

    def notices_reconcile(self, reservation):
        return self._notice_result(reservation, allow_release=True)

    def _notice_result(self, reservation, *, allow_release):
        with lock(self.path('state.lock')):
            path = self.path('reservations/' + identifier(reservation) + '.json')
            value = load(path, 'reservation')
            if value is None:
                raise ToolError(3, 'Notice reservation is unavailable')
            if value['state'] == 'released':
                return {'reservation_id': reservation, 'state': 'released'}
            history = self.history(allow_pause=True)
            matches = [e for e in history if e['exchange_id'] == value['exchange_id']]
            items = self.notice_items()
            if matches:
                exchange = matches[0]
                messages = [m for m in exchange['messages'] if m['message_id'] == value['message_id'] and m['role'] == 'assistant']
                if (exchange['payload_digest'] != value['payload_digest'] or
                    exchange['expected_git_head'] != value['expected_head'] or len(messages) != 1 or
                    digest(messages[0]['text'].encode()) != value['assistant_text_digest']):
                    raise ToolError(3, 'Saved notice exchange does not match its reservation')
                raw = messages[0]['text'].encode()
                for span in value['notices']:
                    note = items.get(span['notice_id'])
                    content = raw[span['start_byte']:span['end_byte']]
                    if not note or content != note['text'].encode() or digest(content) != span['text_digest']:
                        raise ToolError(3, 'Saved notice content does not match its reservation')
                state = 'included'
            else:
                if value['state'] == 'included' or any(
                        items.get(span['notice_id'], {}).get('state') == 'included' for span in value['notices']):
                    raise ToolError(3, 'Previously confirmed notice history is unavailable; inclusion is retained')
                if not allow_release:
                    raise ToolError(3, 'Notice target is not confirmed saved')
                receipt_path = self.root / '.novel-creator/local' / (value['exchange_id'] + '.json')
                if receipt_path.exists() or storage.safe_path(self.root, '.novel-creator/local/write.lock').exists():
                    raise ToolError(3, 'Notice save is pending or uncertain; recover before replacement')
                self.history()  # Other persistence pauses also block replacement.
                state = 'released'
            for span in value['notices']:
                note = items.get(span['notice_id'])
                if not note:
                    raise ToolError(3, 'Reserved notice is unavailable')
                note.update(state='included' if state == 'included' else 'pending',
                            reservation_id=reservation if state == 'included' else None,
                            included_exchange_id=value['exchange_id'] if state == 'included' else None)
                write(self.path('notices/' + note['notice_id'] + '.json'), note, 'notice')
            value['state'] = state
            write(path, value, 'reservation')
            return {'reservation_id': reservation, 'state': state}

    def access(self, item):
        grant = self.require(item)
        self.checkpoint(item['completion_exchange_id'], item['checkpoint'])
        from .retro_github import verify_transport
        verify_transport(grant['checkout_root'], guard=lambda: self.require(item))
        identity = self.remote(item, 'identity')
        if identity != {'login': grant['github_login'], 'repository': REPOSITORY}:
            raise ToolError(3, 'Authenticated contribution identity changed')
        return grant

    def git(self, item, root, *args, input=None):
        # Each subprocess has its own authorization boundary. Do not hold the
        # control lock across a process: disablement must remain independent of
        # contribution locks and in-flight work. Preserve its result before the
        # next boundary (notably commit identity and known remote PR effects).
        self.require(item)
        return contribution_git(root, *args, input=input, guard=lambda: self.require(item))

    def remote(self, item, method, *args):
        self.require(item)
        result = getattr(self.github, method)(*args)
        self.require(item)  # Revocation during one request prevents the next phase.
        return result

    @contextmanager
    def repository_operation(self, item, *, claim=True):
        with self.run_lock(item['run_id']):
            self.current_run(item)
            with self._repository_operation(item, claim=claim) as operation:
                yield operation

    @contextmanager
    def _repository_operation(self, item, *, claim=True):
        grant = self.require(item)
        checkout = guarded(grant['checkout_root'])
        common = guarded(grant['git_common_dir'])
        actual = self.git(item, checkout, 'rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip()
        if Path(actual) != common:
            raise ToolError(3, 'Framework repository identity changed')
        base = guarded(common / 'novel-creator-retro')
        expected = document('owner', run_id=item['run_id'], grant_id=item['grant_id'], novel_root=str(self.root))
        with lock(base / 'operation.lock', owner=expected):
            self.require(item)
            owner = load(base / 'owner.json', 'owner')
            if claim and owner and owner != expected:
                raise ToolError(6, 'Another contribution owns this repository; inspect before retry')
            if claim and owner is None:
                write(base / 'owner.json', expected, 'owner')
            previous = getattr(self.github, 'guard', None)
            self.github.guard = lambda: self.require(item)
            try:
                yield grant, base
            finally:
                self.github.guard = previous

    def release_owner(self, item, base):
        self.require(item)
        owner = load(base / 'owner.json', 'owner')
        expected = document('owner', run_id=item['run_id'], grant_id=item['grant_id'], novel_root=str(self.root))
        if owner == expected:
            guarded(base / 'owner.json').unlink()

    def terminal_result(self, item):
        # Terminal receipt precedes cleanup. Explicit recovery can retry cleanup
        # after a crash without acquiring a new claim or repeating a remote effect.
        grant = self.require(item)
        self.inspect_dead_lock(item, grant)
        with self.repository_operation(item, claim=False) as (_, base):
            self.release_owner(item, base)
        result = {'run_id': item['run_id'], 'status': item['status']}
        if item['contribution'] and item['contribution']['pr']:
            result['url'] = item['contribution']['pr']['url']
        return result

    @staticmethod
    def public_reference(pr):
        # Remote text is untrusted. Status never echoes bodies or arbitrary URLs.
        result = {k: pr[k] for k in ('number', 'draft', 'state', 'merged') if k in pr}
        if re.fullmatch(r'https://github\.com/bjarkig82/novel-creator/pull/[1-9][0-9]*', pr.get('url', '')):
            result['url'] = pr['url']
        if pr.get('repository') == REPOSITORY:
            result['repository'] = REPOSITORY
        for name in ('head', 'base'):
            value = pr.get(name)
            if isinstance(value, str) and len(value) <= 256 and not any(ord(c) < 32 for c in value):
                result[name] = value
        if re.fullmatch(r'[0-9a-f]{40,64}', pr.get('sha', '')):
            result['sha'] = pr['sha']
        return result

    def comparison_scope(self, item, grant):
        upstream = self.remote(item, 'base', Path(grant['checkout_root']))
        own = item['contribution']['public_id'] if item['contribution'] else None
        candidates = [p for p in self.remote(item, 'pulls_for') if p.get('repository') == REPOSITORY and
                      (p['state'] == 'open' or p.get('merged') is True) and
                      not (own and 'novel-retro-contribution:' + own in p['body'])]
        candidates.sort(key=lambda p: p['number'], reverse=True)
        snapshot = digest(json.dumps({'base': upstream, 'finding': item['finding'], 'candidates': candidates},
                                     sort_keys=True, ensure_ascii=False).encode())
        return upstream, candidates, snapshot

    def comparison_request(self, item, upstream, candidates, snapshot):
        approved = item.get('comparison')
        if approved and approved['snapshot'] == snapshot and approved['approved']:
            return None
        return {'run_id': item['run_id'], 'status': 'comparison_required', 'snapshot': snapshot,
                'base': upstream, 'candidate_count': len(candidates), 'has_more': len(candidates) > 50,
                'candidates': [dict(self.public_reference(p), title=p['title'][:1024], body=p['body'][:8192],
                                    text_truncated=len(p['title']) > 1024 or len(p['body']) > 8192)
                               for p in candidates[:50]]}

    def compare(self, run_id, data):
        validate(data, 'comparison_input')
        item = self.run(run_id)
        self.require(item)
        part = item['contribution']
        recovering_push = part and part['stage'] in ('push_intent', 'pushed')
        if (item['status'] not in ('selected', 'prepared', 'validated', 'blocked') and
                not (item['status'] == 'publishing' and recovering_push)) or (
                part and part['stage'] != 'not_started' and not recovering_push):
            raise ToolError(3, 'Comparison requires an unpublished correction')
        with self.repository_operation(item) as (grant, base):
            self.access(item)
            if recovering_push:
                result = self.reconcile_publication(item, base)
                if item['status'] == 'published':
                    return result
                approved = part['validation']
                if not approved or self.prospective(item) != approved['tree']:
                    raise ToolError(3, 'Contribution changed after validation; preserve and inspect existing intent')
                if (not part['commit'] or
                        self.git(item, self.worktree(item), 'rev-parse', part['commit'] + '^{tree}').decode().strip() != approved['tree']):
                    raise ToolError(3, 'Intended commit differs from the approved tree')
            upstream, candidates, snapshot = self.comparison_scope(item, grant)
            if recovering_push and upstream != part['base']:
                self.block(item, 'upstream_changed')
                raise ToolError(3, 'Upstream base changed; inspect and explicitly abandon, preserving the correction')
            if data['snapshot'] != snapshot:
                raise ToolError(3, 'Public comparison scope changed; inspect the current snapshot')
            equivalent = next((p for p in candidates if p['number'] == data['equivalent_pr']), None)
            if data['equivalent_pr'] is not None and equivalent is None:
                raise ToolError(3, 'Equivalent reference is not an open or merged upstream contribution')
            item['comparison'] = dict(snapshot=snapshot, approved=True,
                                     equivalent_pr=data['equivalent_pr'], upstream_fix_present=data['upstream_fix_present'])
            if equivalent or data['upstream_fix_present']:
                item.update(status='duplicate', reason_code='equivalent_contribution' if equivalent else 'upstream_already_fixed')
                if equivalent:
                    item['remote_outcome'] = dict(kind='equivalent', pr=equivalent)
                self.save_run(item)
                self.release_owner(item, base)
                return {'run_id': run_id, 'status': 'duplicate',
                        **({'url': equivalent['url']} if equivalent else {})}
            self.save_run(item)
            return {'run_id': run_id, 'status': item['status'], 'comparison': 'approved', 'base': upstream}

    def prepare(self, run_id):
        item = self.run(run_id)
        self.require(item)
        if item['status'] not in ('selected', 'preparing', 'prepared'):
            raise ToolError(3, 'Select one evidenced correction before preparation')
        with self.repository_operation(item) as (grant, base):
            self.access(item)
            if item['contribution']:
                part = item['contribution']
                worktree = guarded(part['worktree'])
                if not worktree.exists():
                    expected = guarded(base / 'worktrees' / run_id)
                    if worktree != expected or part['stage'] != 'not_started' or part['commit'] is not None:
                        raise ToolError(3, 'Preparation allocation requires inspection')
                    self.require(item)
                    existing = self.git(item, grant['checkout_root'], 'for-each-ref', '--format=%(objectname)',
                                                'refs/heads/' + part['branch']).decode().strip()
                    if existing and existing != part['base']['sha']:
                        raise ToolError(3, 'Preparation branch differs from its recorded base')
                    argv = ['worktree', 'add']
                    if not existing:
                        argv += ['-b', part['branch'], str(worktree), part['base']['sha']]
                    else:
                        argv += [str(worktree), part['branch']]
                    self.git(item, grant['checkout_root'], *argv)
                worktree = self.worktree(item)
                item['status'] = 'prepared'
                self.save_run(item)
                return {'run_id': run_id, 'worktree': str(worktree), 'status': item['status']}
            fingerprint = digest(json.dumps(item['finding'], sort_keys=True, ensure_ascii=False).encode())
            upstream, candidates, snapshot = self.comparison_scope(item, grant)
            request = self.comparison_request(item, upstream, candidates, snapshot)
            if request:
                return request
            self.require(item)
            branch = 'codex/retro-' + run_id
            worktree = guarded(base / 'worktrees' / run_id)
            if worktree.exists():
                raise ToolError(3, 'Unrecorded worktree exists; inspect instead of replacing it')
            item['status'] = 'preparing'
            item['contribution'] = dict(base=upstream, worktree=str(worktree), branch=branch,
                stage='not_started', commit=None, validation=None, pr=None, fingerprint=fingerprint, public_id=uid())
            self.save_run(item)  # Durable identity precedes Git mutation.
            self.require(item)
            self.git(item, grant['checkout_root'], 'worktree', 'add', '-b', branch, str(worktree), upstream['sha'])
            self.worktree(item)
            item['status'] = 'prepared'
            self.save_run(item)
            return {'run_id': run_id, 'worktree': str(worktree), 'status': 'prepared'}

    def worktree(self, item):
        grant = self.require(item)
        part = item['contribution']
        if not part:
            raise ToolError(3, 'No contribution is prepared')
        expected = guarded(Path(grant['git_common_dir']) / 'novel-creator-retro/worktrees' / item['run_id'])
        if str(expected) != part['worktree'] or not expected.is_dir():
            raise ToolError(3, 'Allocated worktree is unavailable')
        top = self.git(item, expected, 'rev-parse', '--show-toplevel').decode().strip()
        common = self.git(item, expected, 'rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip()
        branch = self.git(item, expected, 'symbolic-ref', '--short', 'HEAD').decode().strip()
        if Path(top) != expected or Path(common) != Path(grant['git_common_dir']) or branch != part['branch']:
            raise ToolError(3, 'Worktree identity changed')
        head = self.git(item, expected, 'rev-parse', 'HEAD').decode().strip()
        if head not in (part['base']['sha'], part['commit']):
            raise ToolError(3, 'Unreviewed worktree history is not publishable')
        return expected

    def body_path(self, value):
        path = guarded(value)
        if not path.is_relative_to(self.local) or not path.is_file():
            raise ToolError(2, 'Public payload must be an ordinary file in local retrospective storage')
        return path

    def prospective(self, item):
        worktree = self.worktree(item)
        self.require(item)
        self.git(item, worktree, 'add', '--all')
        tree = self.git(item, worktree, 'write-tree').decode().strip()
        raw = self.git(item, worktree, 'diff', '--cached', '--raw', item['contribution']['base']['sha'])
        if not raw.strip():
            raise ToolError(3, 'No focused correction is present')
        for line in raw.splitlines():
            modes = line.split()[:2]
            if any(mode not in (b':100644', b':100755', b':000000', b'100644', b'100755', b'000000') for mode in modes):
                raise ToolError(3, 'Contribution contains a redirected or unsupported file mode')
        diff = self.git(item, worktree, 'diff', '--cached', '--binary', item['contribution']['base']['sha'])
        try:
            text = diff.decode('utf-8')
        except UnicodeError as error:
            raise ToolError(3, 'Contribution requires a reviewable text reproduction') from error
        if 'GIT binary patch' in text:
            raise ToolError(3, 'Binary contribution requires separate review')
        privacy_check(text, private_values=self.private_values())
        return tree

    def validate_contribution(self, run_id, data):
        validate(data, 'validation')
        item = self.run(run_id)
        if item['status'] not in ('prepared', 'validating', 'validated', 'blocked') or not item['contribution']:
            raise ToolError(3, 'No prepared contribution is available for validation')
        if item['contribution']['stage'] != 'not_started' or item['contribution']['commit'] is not None:
            raise ToolError(3, 'Commit/publication intent is immutable; resume or inspect existing work')
        with self.repository_operation(item):
            self.access(item)
            worktree = self.worktree(item)
            body = self.body_path(data['body_file']).read_text(encoding='utf-8')
            privacy_check(data['title'] + '\n' + body, private_values=self.private_values())
            if '\n' in data['title'] or '\r' in data['title']:
                raise ToolError(2, 'Public title must be one line')
            tree = self.prospective(item)
            item['status'] = 'validating'
            item['contribution']['validation'] = None
            attempt = dict(attempt_id=uid(), tree=tree, state='running', checks=[])
            item['contribution'].setdefault('diagnostics', []).append(attempt)
            self.save_run(item)
            results = []
            # Test code is trusted repository code subject to host permission, not a sandbox.
            allowed = ('PATH', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT', 'TEMP', 'TMP')
            env = {k: os.environ[k] for k in allowed if k in os.environ}
            for argv in data['checks']:
                self.require(item)
                if any(not a or '\x00' in a or str(self.root).casefold() in a.casefold() for a in argv):
                    raise ToolError(2, 'Validation arguments must not reference novel evidence')
                prefix = 'diagnostics/' + run_id + '/' + attempt['attempt_id'] + '/' + str(len(results))
                check = dict(argv=argv, exit_code=None, state='running',
                             stdout=dict(path=prefix + '.stdout', digest=None),
                             stderr=dict(path=prefix + '.stderr', digest=None))
                attempt['checks'].append(check)
                self.save_run(item)  # Durable paths precede process start, including hard interruption.
                stdout = self.path(check['stdout']['path'])
                stderr = self.path(check['stderr']['path'])
                stdout.parent.mkdir(parents=True, exist_ok=True)
                try:
                    # Stream into ignored files so process/host termination does not
                    # discard output already produced. Never stage these files.
                    with stdout.open('xb') as out, stderr.open('xb') as err:
                        try:
                            self.require(item)
                            result = subprocess.run(argv, cwd=worktree, env=env, stdout=out, stderr=err, timeout=300)
                            check.update(exit_code=result.returncode, state='failed' if result.returncode else 'passed')
                        finally:
                            for stream in (out, err):
                                stream.flush()
                                os.fsync(stream.fileno())
                except (OSError, subprocess.TimeoutExpired, KeyboardInterrupt) as error:
                    check['state'] = 'unavailable' if isinstance(error, OSError) else 'interrupted'
                    attempt['state'] = check['state']
                    if isinstance(error, KeyboardInterrupt):
                        raise
                    self.block(item, 'validation_unavailable')
                    raise ToolError(5, 'Required contribution validation is unavailable') from error
                finally:
                    for name, path in (('stdout', stdout), ('stderr', stderr)):
                        if path.is_file():
                            check[name]['digest'] = digest(guarded(path).read_bytes())
                    self.save_run(item)
                # Never include raw check output in public material or ordinary diagnostics.
                results.append({'argv': argv, 'exit_code': result.returncode})
                if result.returncode:
                    attempt['state'] = 'failed'
                    self.block(item, 'validation_failed')
                    raise ToolError(5, 'Required contribution validation failed')
            self.require(item)
            if self.prospective(item) != tree:
                attempt['state'] = 'failed'
                self.block(item, 'tree_changed_during_checks')
                raise ToolError(3, 'Contribution tree changed during validation')
            item['contribution']['validation'] = dict(tree=tree, title=data['title'], body=body,
                title_digest=digest(data['title'].encode()), body_digest=digest(body.encode()),
                checks=results, privacy_approved=True, synthetic_only=True, attempt_id=attempt['attempt_id'])
            attempt['state'] = 'passed'
            item['status'] = 'validated'
            self.save_run(item)
            return {'run_id': run_id, 'status': 'validated', 'tree': tree}

    def block(self, item, reason):
        item.update(status='blocked', reason_code=reason)
        self.notice(item, 'Retrospective contribution blocked: ' + reason.replace('_', ' ') + '.')
        self.save_run(item)

    def verified_pr(self, item, pr):
        part = item['contribution']
        if (pr.get('repository') != REPOSITORY or pr.get('head') != part['branch'] or
            pr.get('base') != part['base']['branch'] or pr.get('sha') != part['commit'] or
            pr.get('draft') is not True or pr.get('state') != 'open' or pr.get('merged') is True or
            pr.get('url') != f'https://github.com/{REPOSITORY}/pull/{pr.get("number")}' or
            'novel-retro-contribution:' + part['public_id'] not in pr.get('body','')):
            raise ToolError(3, 'Created pull request does not match the approved draft')
        return pr

    def published(self, item, pr, base):
        # Record a known remote result before applying the stricter success gate.
        validate(pr, 'remote_pr')
        item['remote_outcome'] = dict(kind='observed', pr=pr)
        item['contribution']['stage'] = 'remote_observed'
        self.save_run(item)
        try:
            self.verified_pr(item, pr)
        except ToolError:
            self.block(item, 'unexpected_remote_result')
            raise
        item['remote_outcome']['kind'] = 'verified'
        item['contribution'].update(stage='published', pr=pr)
        item.update(status='published', reason_code='')
        self.notice(item, 'Retrospective created a draft PR: ' + pr['url'], pr['url'])
        self.save_run(item)
        self.release_owner(item, base)
        return {'run_id': item['run_id'], 'status': 'published', 'url': pr['url']}

    def observed_reference(self, item, reference):
        validate(reference, 'remote_reference')
        if reference['url'] != f'https://github.com/{REPOSITORY}/pull/{reference["number"]}':
            raise ToolError(3, 'Observed remote reference differs from the designated repository')
        # This records an already-completed in-flight effect even after revocation.
        item['remote_outcome'] = dict(kind='observed', pr=reference)
        item['contribution']['stage'] = 'remote_observed'
        self.save_run(item)

    def reconcile_publication(self, item, base, *, abandoning=False):
        part = item['contribution']
        self.access(item)
        if part['stage'] == 'remote_observed' and item.get('remote_outcome'):
            prior = item['remote_outcome']['pr']
            actual = self.remote(item, 'pull', prior['number'])
            if actual['number'] != prior['number'] or actual['url'] != prior['url'] or actual['repository'] != REPOSITORY:
                raise ToolError(3, 'Observed remote identity cannot be established')
            if abandoning:
                item['remote_outcome'] = dict(kind='observed', pr=actual)
                self.save_run(item)
                return {'run_id': item['run_id'], 'status': item['status'], 'pr': self.public_reference(actual)}
            return self.published(item, actual, base)
        candidates = self.remote(item, 'pulls_for', part['branch'])
        found = [p for p in candidates if 'novel-retro-contribution:' + part['public_id'] in p.get('body','')]
        if len(found) == 1:
            try:
                return self.published(item, found[0], base)
            except ToolError:
                pr = found[0]
                if (abandoning and item['reason_code'] == 'unexpected_remote_result' and
                        pr.get('repository') == REPOSITORY and
                        pr.get('url') == f'https://github.com/{REPOSITORY}/pull/{pr.get("number")}'):
                    return {'run_id': item['run_id'], 'status': item['status'], 'pr': self.public_reference(pr)}
                raise
        if found or part['stage'] in ('create_intent', 'publication_unknown'):
            self.block(item, 'publication_unknown')
            raise ToolError(3, 'Publication outcome is uncertain; no second create request is permitted')
        remote = self.remote(item, 'remote_sha', part['branch'])
        if remote and remote != part['commit']:
            raise ToolError(3, 'Remote branch differs from the intended commit')
        if remote:
            part['stage'] = 'pushed'
            self.save_run(item)
        return {'run_id': item['run_id'], 'status': item['status'], 'stage': part['stage']}

    def publish(self, run_id):
        item = self.run(run_id)
        self.require(item)
        if item['status'] == 'published':
            return self.terminal_result(item)
        if item['status'] not in ('validated', 'publishing', 'blocked'):
            raise ToolError(3, 'Run lifecycle does not permit publication')
        part = item['contribution']
        if not part or not part['validation']:
            raise ToolError(3, 'Successful validation and privacy approval are required')
        with self.repository_operation(item) as (grant, base):
            self.access(item)
            if part['stage'] in ('create_intent', 'publication_unknown', 'remote_observed'):
                return self.reconcile_publication(item, base)
            approved = part['validation']
            if self.prospective(item) != approved['tree']:
                self.block(item, 'validation_invalidated')
                raise ToolError(3, 'Contribution changed after validation')
            current, candidates, snapshot = self.comparison_scope(item, grant)
            if current != part['base']:
                self.block(item, 'upstream_changed')
                raise ToolError(3, 'Upstream base changed; inspect and explicitly abandon, preserving the correction')
            for existing in self.remote(item, 'pulls_for', part['branch']):
                if 'novel-retro-contribution:' + part['public_id'] in existing['body']:
                    return self.published(item, existing, base)
            request = self.comparison_request(item, current, candidates, snapshot)
            if request:
                return request
            worktree = self.worktree(item)
            if part['commit'] is None:
                self.require(item)
                name = storage.git(grant['checkout_root'], 'config', 'user.name').decode().strip()
                self.require(item)
                email = storage.git(grant['checkout_root'], 'config', 'user.email').decode().strip()
                if not name or not email or any(c in name + email for c in '\r\n\x00'):
                    raise ToolError(4, 'Existing Git author identity is required')
                privacy_check(name + '\n' + email, private_values=self.private_values())
                part['commit'] = self.git(item, worktree, '-c', 'user.name=' + name, '-c', 'user.email=' + email,
                    'commit-tree', approved['tree'], '-p', part['base']['sha'],
                    input=(approved['title'] + '\n').encode()).decode().strip()
                self.save_run(item)
                self.require(item)
                self.git(item, worktree, 'update-ref', 'refs/heads/' + part['branch'], part['commit'], part['base']['sha'])
            if self.git(item, worktree, 'rev-parse', part['commit'] + '^{tree}').decode().strip() != approved['tree']:
                raise ToolError(3, 'Intended commit does not contain the validated tree')
            remote = self.remote(item, 'remote_sha', part['branch'])
            if remote and remote != part['commit']:
                raise ToolError(3, 'Unexpected remote branch identity')
            if not remote:
                part['stage'] = 'push_intent'
                item['status'] = 'publishing'
                self.save_run(item)
                self.access(item)
                try:
                    self.remote(item, 'push', worktree, part['branch'], part['commit'])
                except (ToolError, OSError) as error:
                    self.block(item, 'push_outcome_unknown')
                    raise ToolError(5, 'Push outcome is uncertain; resume existing intent') from error
            if self.remote(item, 'remote_sha', part['branch']) != part['commit']:
                self.block(item, 'push_unconfirmed')
                raise ToolError(5, 'Pushed commit is not confirmed')
            part['stage'] = 'pushed'
            self.save_run(item)
            self.access(item)
            body = approved['body'] + '\n\n<!-- novel-retro-finding:' + part['fingerprint'] + \
                   ' -->\n<!-- novel-retro-contribution:' + part['public_id'] + ' -->\n'
            part['stage'] = 'create_intent'
            self.save_run(item)
            try:
                self.require(item)
                pr = self.github.create(part['branch'], part['base']['branch'], approved['title'], body,
                                        lambda reference: self.observed_reference(item, reference))
            except (ToolError, OSError) as error:
                if part['stage'] == 'remote_observed':
                    self.block(item, 'remote_verification_unavailable')
                    raise ToolError(5, 'Known PR result is retained; resume its exact reference') from error
                part['stage'] = 'publication_unknown'
                self.block(item, 'publication_unknown')
                raise ToolError(5, 'Draft outcome is uncertain; resume to reconcile without another create') from error
            return self.published(item, pr, base)

    def resume(self, run_id, *, abandoning=False):
        grant = self.require()  # No framework access when disabled.
        item = self.run(run_id)
        if item['bindings'] != {k: grant[k] for k in item['bindings']} or item['grant_id'] != grant['grant_id']:
            raise ToolError(3, 'Recovery authorization bindings differ')
        if item['status'] in ('published', 'abandoned', 'duplicate', 'no_action', 'insufficient_evidence'):
            self.inspect_dead_lock(item, grant)
        if item['authorization_generation'] != grant['generation']:
            # Explicit resume adopts the re-enabled generation, never enable itself.
            base = guarded(Path(grant['git_common_dir']) / 'novel-creator-retro')
            expected = document('owner', run_id=item['run_id'], grant_id=item['grant_id'], novel_root=str(self.root))
            with self.run_lock(run_id), lock(base / 'operation.lock', owner=expected):
                self.current_run(item)
                if self.require() != grant:
                    raise ToolError(3, 'Recovery authorization changed; retry explicit recovery')
                owner = load(base / 'owner.json', 'owner')
                if owner and (owner['run_id'] != run_id or owner['grant_id'] != item['grant_id'] or owner['novel_root'] != str(self.root)):
                    raise ToolError(6, 'A different contribution owns the repository')
                item['authorization_generation'] = grant['generation']
                self.save_run(item)
        if item['status'] in ('published', 'abandoned', 'duplicate', 'no_action', 'insufficient_evidence'):
            return self.terminal_result(item)
        with self.repository_operation(item) as (_, base):
            self.access(item)
            if item['contribution'] and item['contribution']['stage'] != 'not_started':
                return self.reconcile_publication(item, base, abandoning=abandoning)
            part = item['contribution']
            if (item['status'] == 'blocked' and item['reason_code'] == 'operation_unavailable' and
                    item['finding'] and not item.get('remote_outcome') and
                    (part is None or (part['commit'] is None and part['validation'] is None))):
                # A failed dispatch retains the selected finding and durable
                # allocation. Resume only restores the local continuation; prepare
                # verifies the recorded path/branch/base before any Git mutation.
                if part and Path(part['worktree']).exists():
                    self.worktree(item)
                item.update(status='preparing' if part else 'selected', reason_code='')
                self.save_run(item)
                return {'run_id': run_id, 'status': item['status'], 'next_operation': 'prepare'}
            return {'run_id': run_id, 'status': item['status']}

    def release(self, run_id):
        grant = self.require()
        original = self.run(run_id)
        if original['status'] in ('published', 'abandoned', 'duplicate', 'no_action', 'insufficient_evidence'):
            return self.resume(run_id)
        self.inspect_dead_lock(original, grant)
        self.resume(run_id, abandoning=True)
        item = self.run(run_id)
        if item['status'] in ('published', 'abandoned', 'duplicate', 'no_action', 'insufficient_evidence'):
            return self.terminal_result(item)
        with self.repository_operation(item) as (_, base):
            self.access(item)
            if item['contribution'] and item['contribution']['stage'] in ('create_intent', 'publication_unknown'):
                raise ToolError(3, 'Cannot abandon an uncertain publication')
            item['status'] = 'abandoned'
            self.save_run(item)
            self.release_owner(item, base)
            return {'run_id': run_id, 'status': 'abandoned'}

    def inspect_dead_lock(self, item, grant):
        self.require()  # Reject invalid persisted storage bindings before creating an inspection guard.
        self.separate_repository_path(grant['git_common_dir'])
        base = guarded(Path(grant['git_common_dir']) / 'novel-creator-retro')
        with inspection_guard(base):
            self._inspect_dead_lock(item, grant, base)

    def _inspect_dead_lock(self, item, grant, base):
        path = guarded(base / 'operation.lock')
        if not path.exists():
            return
        owner = load(base / 'owner.json', 'owner')
        expected = document('owner', run_id=item['run_id'], grant_id=item['grant_id'], novel_root=str(self.root))
        if owner is not None and owner != expected:
            raise ToolError(6, 'Held operation lock does not belong to the requested run')
        try:
            holder = records.loads(guarded(path / 'holder.json').read_bytes())
            if (set(holder) not in ({'retro_version','document','pid','token'}, {'retro_version','document','pid','token','owner'}) or holder['retro_version'] != 1 or
                holder['document'] != 'lock' or type(holder['pid']) is not int or holder['pid'] <= 0):
                raise ValueError()
            identifier(holder['token'])
            if ('owner' in holder and holder['owner'] != expected) or (owner is None and holder.get('owner') != expected):
                raise ValueError()
        except (OSError, ValueError, TypeError) as error:
            raise ToolError(6, 'Held operation lock lacks verifiable ownership') from error
        if process_alive(holder['pid']):
            raise ToolError(6, 'Operation owner is live or cannot be proven dead')
        if set(p.name for p in path.iterdir()) != {'holder.json'}:
            raise ToolError(6, 'Held operation lock has unexpected contents')
        self.require()
        inspected = guarded(base / ('inspected-' + holder['token']))
        if inspected.exists():
            raise ToolError(6, 'Inspected lock identity conflicts')
        path.rename(inspected)  # Atomic claim of this exact, proven-dead lock; never age based.
        guarded(inspected / 'holder.json').unlink()
        inspected.rmdir()


def dispatch(args):
    service = Retro(args.novel)
    try:
        return _dispatch(service, args)
    except (ToolError, OSError) as error:
        # Operational failures must be available to the next saved reply, not an
        # unsaved suffix. Do not replace the original error if journaling is held.
        run_id = getattr(args, 'run', None)
        if not isinstance(error, StaleRunError) and run_id and args.action in ('compare', 'prepare', 'validate', 'publish', 'resume', 'release'):
            try:
                with lock(service.path('state.lock')), service.run_lock(run_id):
                    item = service.run(run_id)
                    if item['status'] not in ('published', 'abandoned', 'duplicate', 'no_action',
                                               'insufficient_evidence', 'blocked'):
                        service.block(item, 'operation_unavailable')
            except (ToolError, OSError):
                pass  # The caller still receives the original failure, never success.
        raise


def _dispatch(service, args):
    if args.action == 'status':
        return service.status(args.run)
    if args.action == 'enable':
        return service.enable(args.checkout, authorize=args.authorize_draft_prs)
    if args.action == 'disable':
        return service.disable()
    if args.action == 'notices':
        action = args.notice_action
        if action == 'pending':
            return service.notices_pending(getattr(args, 'language', None))
        if action == 'reserve':
            return service.notices_reserve(input_file(service, args.input))
        return getattr(service, 'notices_' + action)(args.reservation)
    if args.action == 'begin':
        return service.begin(input_file(service, args.input))
    if args.action == 'review':
        return service.review(args.run, input_file(service, args.input))
    if args.action == 'compare':
        return service.compare(args.run, input_file(service, args.input))
    if args.action == 'validate':
        return service.validate_contribution(args.run, input_file(service, args.input))
    return getattr(service, args.action)(args.run)


def input_file(service, value):
    path = service.body_path(value)
    try:
        return records.loads(path.read_bytes())
    except (ValueError, UnicodeError) as error:
        raise ToolError(2, 'Retrospective input must be strict UTF-8 JSON') from error
