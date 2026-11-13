"""Explicit, local-only session diagnostics, independent of story authority."""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import hashlib
from importlib.resources import files as resources
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import subprocess
import sys
import tempfile
import time
import uuid
import zipfile

from . import __version__
from .cli import ToolError

_VERSION = 1
_ACTIVE = ContextVar('novel_creator_debug', default=None)
_POINTER = (b'<!-- novel-creator-debug:start -->\n## Optional session debugging\n\n'
            b'On an explicit request to start debugging or export a debug report, follow '
            b'[session debugging](.novel-notebook/workflows/debugging.md). '
            b'Debugging is off unless explicitly started for this writing session.\n'
            b'<!-- novel-creator-debug:end -->\n')


def _now():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')


def _json(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8')


def _loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    def reject(value):
        raise ValueError('Non-finite JSON number')
    return json.loads(raw.decode('utf-8'), parse_constant=reject, object_pairs_hook=pairs)


def _guard(path):
    """Check existing ancestors as well as leaves, including Windows junctions."""
    path = Path(path).absolute()
    if '..' in path.parts:
        raise ToolError(2, 'Debug paths cannot traverse parent segments')
    for part in (*reversed(path.parents), path):
        try:
            mode = part.lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(mode.st_mode) or
                getattr(mode, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT or
                not (stat.S_ISDIR(mode.st_mode) or stat.S_ISREG(mode.st_mode))):
            raise ToolError(2, 'Debug paths cannot use redirected or special files')
    return path


def _git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_TERMINAL_PROMPT'] = '0'
    try:
        result = subprocess.run(['git', '-C', str(root), *args], env=env,
                                capture_output=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.decode('utf-8', 'replace').strip() if result.returncode == 0 else None


def _project(novel):
    root = _guard(novel)
    if not root.is_dir() or not _guard(root / '.git').is_dir():
        raise ToolError(2, 'Debugging requires an existing independent novel Git root')
    actual = _git(root, 'rev-parse', '--show-toplevel')
    if actual is None or Path(actual).resolve() != root:
        raise ToolError(2, 'Debugging requires an existing independent novel Git root')
    if _guard(root / '.novel-creator/manifest.json').is_file():
        kind, base = 'legacy', '.novel-creator/local/debug'
    elif (_guard(root / 'notebook/project.md').is_file() and
          _guard(root / '.novel-notebook/workflows').is_dir()):
        kind, base = 'novel-notebook', '.novel-notebook/local/debug'
    else:
        raise ToolError(2, 'No supported notebook or legacy novel was found')
    return root, kind, _guard(root / base)


def _identifier(value):
    try:
        valid = str(uuid.UUID(value)) == value
    except (ValueError, TypeError, AttributeError):
        valid = False
    if not valid:
        raise ToolError(2, 'Expected a canonical debug-session UUID')
    return value


def _session(novel, identifier):
    root, kind, base = _project(novel)
    directory = _guard(base / _identifier(identifier))
    if not directory.is_dir():
        raise ToolError(2, 'Debug session was not found in the selected novel')
    return root, kind, directory


def _write_json(path, value):
    path = _guard(path)
    descriptor, temporary = tempfile.mkstemp(prefix='prepare-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(_json(value) + b'\n')
            stream.flush()
            os.fsync(stream.fileno())
        _guard(path)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def _lock(directory):
    path = _guard(directory / 'session.lock')
    with path.open('a+b') as stream:
        if stream.seek(0, 2) == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _metadata(directory):
    try:
        value = _loads(_guard(directory / 'session.json').read_bytes())
        if (not isinstance(value, dict) or value.get('debug_version') != _VERSION or
                value.get('debug_session') != directory.name or
                value.get('state') not in ('recording', 'stopped') or
                not isinstance(value.get('environment'), dict) or
                not all(isinstance(k, str) and isinstance(v, str) for k, v in value['environment'].items()) or
                not isinstance(value.get('started_at'), str) or
                value.get('stopped_at') is not None and not isinstance(value['stopped_at'], str) or
                not isinstance(value.get('initial_git_checkpoint'), str)):
            raise ValueError()
        return value
    except (ValueError, UnicodeError, TypeError, RecursionError) as error:
        raise ToolError(4, 'Debug session metadata is damaged or unsupported') from error


def _events(directory):
    path = _guard(directory / 'events.jsonl')
    raw = path.read_bytes() if path.exists() else b''
    events, warnings = [], []
    previous = 0
    for number, line in enumerate(raw.splitlines(keepends=True), 1):
        try:
            event = _loads(line)
            if (not line.endswith(b'\n') or not isinstance(event, dict) or
                    event.get('debug_version') != _VERSION or
                    event.get('debug_session') != directory.name or
                    type(event.get('sequence')) is not int or event['sequence'] != previous + 1 or
                    not isinstance(event.get('files', []), list) or
                    not all(isinstance(ref, dict) and isinstance(ref.get('path'), str) and
                            ref.get('phase') in ('before', 'after', 'context')
                            for ref in event.get('files', [])) or
                    'content' in event and not isinstance(event['content'], dict) or
                    not all(isinstance(event.get(k), str) for k in ('timestamp', 'operation', 'source', 'outcome'))):
                raise ValueError()
            previous = event['sequence']
            events.append(event)
        except (ValueError, UnicodeError, TypeError, RecursionError):
            warnings.append(f'Damaged or incomplete event line {number}; original bytes retained in events.jsonl.')
    return events, warnings, raw


def _reconcile_stop(info, events):
    stopped = next((event for event in reversed(events) if event['operation'] == 'debug.stopped'), None)
    if stopped is not None:
        info = dict(info, state='stopped', stopped_at=stopped['timestamp'])
    return info


def _append(directory, event):
    events, warnings, _ = _events(directory)
    if warnings:
        raise ToolError(4, 'Debug log is damaged; export its partial evidence before starting a new session')
    item = dict(event, debug_version=_VERSION, debug_session=directory.name,
                timestamp=_now(), sequence=len(events) + 1)
    raw = _json(item) + b'\n'
    with _guard(directory / 'events.jsonl').open('ab') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return item


def _ignored(root, base):
    relative = (base / 'probe.json').relative_to(root).as_posix()
    if _git(root, 'check-ignore', '--no-index', '--', relative) is None:
        raise ToolError(3, 'Debug local directory must be Git-ignored; run debug setup for a notebook')
    if _git(root, 'ls-files', '--', base.relative_to(root).as_posix()):
        raise ToolError(3, 'Debug local files are already tracked; preserve them and remove tracking explicitly')


def setup(novel):
    root, kind, base = _project(novel)
    if kind != 'novel-notebook':
        raise ToolError(3, 'Legacy debugging support uses the existing explicit framework-update route')
    resource = resources('novel_creator.notebook_resources').joinpath('workflows/debugging.md').read_bytes().replace(b'\r\n', b'\n')
    workflow = _guard(root / '.novel-notebook/workflows/debugging.md')
    agents = _guard(root / 'AGENTS.md')
    ignore = _guard(root / '.gitignore')
    original_agents = agents.read_bytes() if agents.exists() else b''
    original_ignore = ignore.read_bytes() if ignore.exists() else b''
    if workflow.exists() and workflow.read_bytes() != resource:
        raise ToolError(3, 'Existing debugging guidance differs; preserve it and reconcile explicitly')
    if b'<!-- novel-creator-debug:' in original_agents and _POINTER not in original_agents:
        raise ToolError(3, 'Existing debugging instruction block differs; preserve it and reconcile explicitly')
    additions = []
    if not workflow.exists():
        additions.append((workflow, resource))
    if b'.novel-notebook/workflows/debugging.md' not in original_agents:
        additions.append((agents, original_agents + (b'\n' if original_agents and not original_agents.endswith(b'\n') else b'') + b'\n' + _POINTER))
    if b'.novel-notebook/local/' not in original_ignore.splitlines():
        additions.append((ignore, original_ignore + (b'\n' if original_ignore and not original_ignore.endswith(b'\n') else b'') + b'.novel-notebook/local/\n'))
    for path, raw in additions:
        _guard(path).write_bytes(raw)
    _ignored(root, base)
    return {'format': kind, 'changed_paths': [p.relative_to(root).as_posix() for p, _ in additions],
            'ready': True, 'committed': False}


def start(novel):
    root, kind, base = _project(novel)
    _ignored(root, base)
    identifier = str(uuid.uuid4())
    directory = _guard(base / identifier)
    directory.mkdir(parents=True)
    info = {'debug_version': _VERSION, 'debug_session': identifier, 'format': kind,
            'state': 'recording', 'started_at': _now(), 'stopped_at': None,
            'environment': {'package_version': __version__, 'python_version': platform.python_version(),
                            'git_version': _git(root, '--version') or 'unknown',
                            'platform': platform.system(), 'platform_release': platform.release(),
                            'host': 'unknown', 'model': 'unknown'},
            'initial_git_checkpoint': _git(root, 'rev-parse', '--verify', 'HEAD') or 'unknown'}
    with _lock(directory):
        _write_json(directory / 'session.json', info)
        _append(directory, {'operation': 'debug.started', 'source': 'package-measured', 'outcome': 'success'})
    return dict(info, directory=str(directory))


def status(novel, debug_session=None):
    if debug_session is None:
        _, _, base = _project(novel)
        sessions = []
        if base.exists():
            for path in sorted(base.iterdir()):
                try:
                    _identifier(path.name)
                except ToolError:
                    continue
                _guard(path)
                if path.is_dir():
                    sessions.append(status(novel, path.name))
        return {'sessions': sessions, 'automatic_activation': False}
    _, _, directory = _session(novel, debug_session)
    with _lock(directory):
        info = _metadata(directory)
        events, warnings, _ = _events(directory)
    return dict(_reconcile_stop(info, events), event_count=len(events), warnings=warnings, directory=str(directory))


def _reference(root, reference):
    if not isinstance(reference, dict) or set(reference) - {'path', 'phase'}:
        raise ToolError(2, 'File snapshots require path and phase')
    relative, phase = reference.get('path'), reference.get('phase', 'context')
    if not isinstance(relative, str) or phase not in ('before', 'after', 'context'):
        raise ToolError(2, 'Invalid snapshot path or phase')
    path = PurePosixPath(relative)
    if (not relative or str(path) != relative or path.is_absolute() or '\\' in relative or ':' in relative or
            '..' in path.parts or any(ord(c) < 32 for c in relative) or
            path.parts[0] not in ('notebook', 'manuscript', 'research', 'reviews', 'story') or
            any(part.startswith('.') or part.endswith((' ', '.')) or
                part.lower() in ('credentials', 'secrets', 'private') for part in path.parts) or
            path.suffix.lower() not in ('.md', '.txt', '.json') or
            any(word in path.name.lower() for word in ('credential', 'secret', 'password', 'token'))):
        raise ToolError(2, 'Snapshot is outside supported public story files')
    target = _guard(root / relative)
    return relative, phase, target


def _snapshot(root, directory, reference):
    relative, phase, target = _reference(root, reference)
    if not target.exists():
        return {'path': relative, 'phase': phase, 'exists': False}
    if not target.is_file():
        raise ToolError(2, 'Snapshot requires an ordinary file')
    raw = target.read_bytes()
    try:
        raw.decode('utf-8')
    except UnicodeError as error:
        raise ToolError(2, 'Snapshot must contain UTF-8 text') from error
    return dict(_attachment(directory, raw, '.txt'), path=relative, phase=phase, exists=True)


def _attachment(directory, raw, suffix):
    digest = hashlib.sha256(raw).hexdigest()
    relative = 'attachments/' + digest + suffix
    path = _guard(directory / relative)
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        if path.read_bytes() != raw:
            raise ToolError(4, 'Debug attachment content does not match its digest')
    else:
        with path.open('xb') as stream:
            stream.write(raw)
    return {'attachment': relative, 'sha256': digest, 'bytes': len(raw)}


def _check_public(value):
    private = {'reasoning', 'hidden_reasoning', 'analysis', 'environment', 'env', 'credentials',
               'secret', 'password', 'token', 'api_key', 'access_token', 'authorization',
               'private_transcript', 'private_host_storage'}
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key.casefold().replace('-', '_') in private:
                raise ToolError(2, 'Debug events cannot contain private structured fields')
            _check_public(item)
    elif isinstance(value, list):
        for item in value:
            _check_public(item)


def _record(novel, debug_session, payload, source):
    root, _, directory = _session(novel, debug_session)
    events = payload.get('events') if isinstance(payload, dict) and 'events' in payload else [payload]
    if not isinstance(events, list) or not events:
        raise ToolError(2, 'Debug input requires an event or a nonempty events array')
    prepared = []
    for value in events:
        if not isinstance(value, dict) or set(value) - {'operation', 'outcome', 'metadata', 'correlation_ids', 'observed_at', 'content', 'files', 'duration_ms'}:
            raise ToolError(2, 'Unsupported debug event fields')
        operation = value.get('operation')
        if not isinstance(operation, str) or not operation.strip() or operation.startswith('debug.'):
            raise ToolError(2, 'Debug event requires a nonreserved operation name')
        if ('duration_ms' in value and (source != 'package-measured' or
                type(value['duration_ms']) not in (int, float) or
                not math.isfinite(value['duration_ms']) or value['duration_ms'] < 0)):
            raise ToolError(2, 'Only measured package events carry duration_ms')
        if not isinstance(value.get('outcome', 'success'), str):
            raise ToolError(2, 'Debug outcome must be a string')
        for name in ('metadata', 'correlation_ids'):
            if name in value and not isinstance(value[name], dict):
                raise ToolError(2, 'Debug metadata and correlation_ids must be objects')
        if 'observed_at' in value:
            try:
                if not isinstance(value['observed_at'], str) or datetime.fromisoformat(value['observed_at'].replace('Z', '+00:00')).tzinfo is None:
                    raise ValueError()
            except (ValueError, TypeError) as error:
                raise ToolError(2, 'observed_at must be a supplied timestamp with timezone') from error
        if not isinstance(value.get('files', []), list):
            raise ToolError(2, 'Debug files must be an array')
        try:
            _json(value)
            _check_public(value)
            for reference in value.get('files', []):
                _reference(root, reference)
        except (ValueError, TypeError, UnicodeError, RecursionError) as error:
            raise ToolError(2, 'Debug events must be strict UTF-8 JSON values') from error
        prepared.append(value)
    with _lock(directory):
        info = _metadata(directory)
        existing, warnings, _ = _events(directory)
        if info['state'] != 'recording' or any(e['operation'] == 'debug.stopped' for e in existing):
            raise ToolError(3, 'Debug session is stopped; start a new session explicitly')
        if warnings:
            raise ToolError(4, 'Debug log is damaged; export partial evidence instead of appending')
        saved = []
        attached = []
        for value in prepared:
            event = {k: v for k, v in value.items() if k not in ('content', 'files')}
            event.update(source=source, outcome=value.get('outcome', 'success'))
            if 'content' in value:
                event['content'] = _attachment(directory, _json(value['content']), '.json')
            event['files'] = [_snapshot(root, directory, ref) for ref in value.get('files', [])]
            attached.append(event)
        for event in attached:
            saved.append(_append(directory, event)['sequence'])
    return {'debug_session': debug_session, 'recorded_sequences': saved}


def record(novel, debug_session, payload):
    return _record(novel, debug_session, payload, 'agent-recorded')


def stop(novel, debug_session):
    _, _, directory = _session(novel, debug_session)
    with _lock(directory):
        info = _metadata(directory)
        events, warnings, _ = _events(directory)
        reconciled = _reconcile_stop(info, events)
        if reconciled != info:
            info = reconciled
            _write_json(directory / 'session.json', info)
        if info['state'] != 'stopped':
            event = _append(directory, {'operation': 'debug.stopped', 'source': 'package-measured', 'outcome': 'success'})
            info.update(state='stopped', stopped_at=event['timestamp'])
            _write_json(directory / 'session.json', info)
    return info


def _report(info, events, warnings):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', ' ')
    state = 'Stopped' if info['state'] == 'stopped' else 'Partial — session was still recording at export'
    lines = ['# Session debugging report', '', f"Session: `{info['debug_session']}`", '',
             f'Status: {state}', '', f"Started: {info['started_at']}",
             f"Stopped: {info.get('stopped_at') or 'unknown'}", '', '## Environment', '']
    lines.extend(f'- {cell(k)}: {cell(v)}' for k, v in info['environment'].items())
    lines.extend(['', f"Initial Git checkpoint: {info['initial_git_checkpoint']}", '',
                  '## Capture limits', '',
                  'Package-measured events describe observed package operations. Agent-recorded events describe supplied public observations; they are not an exhaustive host transcript. Missing host/model data remains unknown.', '',
                  'Durations measure individual operations using a monotonic clock. Gaps between timestamps are elapsed gaps, not measured work or evidence of their cause. Nested durations overlap. Debugging adds file, hashing and logging overhead.', '',
                  'Content includes the captured working set only. Hidden reasoning, private host storage and environment dumps are not collected. This archive may contain private story and conversation text; no upload is performed.', ''])
    lines.extend(['## Capture warnings', ''] + (['- ' + w for w in warnings] or ['No damaged records detected. Missing observations may still exist.']))
    changed = sorted({ref['path'] for e in events for ref in e.get('files', []) if ref.get('phase') in ('before', 'after')})
    lines.extend(['', '## Touched files', ''] + (['- ' + cell(p) for p in changed] or ['No file-change snapshots recorded.']))
    lines.extend(['', '## Timeline', '', '| Time (UTC) | Source | Operation | Outcome | Measured ms |', '| --- | --- | --- | --- | --- |'])
    for event in events:
        lines.append('| ' + ' | '.join(cell(event.get(k, '')) for k in ('timestamp', 'source', 'operation', 'outcome', 'duration_ms')) + ' |')
    lines.extend(['', 'See events.jsonl for correlation IDs, metadata and attachment references. Content bytes live under attachments/.', ''])
    return '\n'.join(lines).encode('utf-8')


def export(novel, debug_session, output=None):
    _, _, directory = _session(novel, debug_session)
    target = _guard(output) if output is not None else _guard(directory / 'report.zip')
    if not target.parent.is_dir():
        raise ToolError(2, 'Export requires an existing parent directory')
    with _lock(directory):
        info = _metadata(directory)
        events, warnings, raw = _events(directory)
        info = _reconcile_stop(info, events)
        attachments = {}
        for event in events:
            refs = list(event.get('files', []))
            if isinstance(event.get('content'), dict):
                refs.append(event['content'])
            for ref in refs:
                name = ref.get('attachment')
                if name is None:
                    continue
                if not isinstance(name, str) or not re.fullmatch(r'attachments/[a-f0-9]{64}\.(txt|json)', name):
                    warnings.append('Unsafe attachment reference omitted.')
                    continue
                try:
                    data = _guard(directory / name).read_bytes()
                    if hashlib.sha256(data).hexdigest() != ref.get('sha256'):
                        raise ValueError()
                    attachments[name] = data
                except (OSError, ValueError, ToolError):
                    warnings.append('Missing, redirected or damaged attachment: ' + name)
        if target.exists():
            raise ToolError(3, 'Export destination already exists; choose a new path')
        created = False
        try:
            with target.open('xb') as stream:
                created = True
                with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                    archive.writestr('report.md', _report(info, events, warnings))
                    archive.writestr('session.json', _json(dict(info, exported_at=_now(), partial=info['state'] != 'stopped', warnings=warnings)) + b'\n')
                    archive.writestr('events.jsonl', raw)
                    for name, data in attachments.items():
                        archive.writestr(name, data)
        except BaseException:
            if created:
                target.unlink()
            raise
    return {'debug_session': debug_session, 'output': str(target), 'partial': info['state'] != 'stopped', 'warnings': warnings}


def dispatch(args):
    action = args.debug_action
    if action in ('setup', 'start'):
        return globals()[action](args.novel)
    if action == 'status':
        return status(args.novel, args.debug_session)
    if action == 'record':
        try:
            payload = _loads(_guard(args.input).read_bytes())
        except (ValueError, UnicodeError, RecursionError) as error:
            raise ToolError(2, 'Debug input must be strict UTF-8 JSON') from error
        return record(args.novel, args.debug_session, payload)
    if action == 'stop':
        return stop(args.novel, args.debug_session)
    if action == 'export':
        return export(args.novel, args.debug_session, args.output)
    raise ToolError(2, 'Unknown debug action')


def _warning():
    print('Warning: debug capture failed; writing result is unchanged and the report may have gaps.', file=sys.stderr)


def capture(operation, *, content=None, metadata=None, files=None, outcome='success', correlation_ids=None):
    active = _ACTIVE.get()
    if active is None:
        return
    event = dict(operation=operation, outcome=outcome)
    for key, value in (('content', content), ('metadata', metadata), ('files', files), ('correlation_ids', correlation_ids)):
        if value is not None:
            event[key] = value
    try:
        _record(*active, event, 'package-measured')
    except Exception:
        _warning()


@contextmanager
def span(operation, metadata=None):
    active = _ACTIVE.get()
    if active is None:
        yield
        return
    started = time.perf_counter()
    outcome = 'success'
    details = dict(metadata or {})
    try:
        yield
    except BaseException as error:
        outcome = 'failure'
        details['exception_type'] = type(error).__name__
        if isinstance(error, ToolError):
            details['error_code'] = error.code
            if error.checkpoint is not None:
                details['last_confirmed_checkpoint'] = error.checkpoint
            if error.pending is not None:
                details['pending_exchange_id'] = error.pending
        raise
    finally:
        try:
            _record(*active, {'operation': operation, 'metadata': details, 'outcome': outcome,
                             'duration_ms': (time.perf_counter() - started) * 1000}, 'package-measured')
        except Exception:
            _warning()


@contextmanager
def activate(novel, debug_session, operation):
    if debug_session is None:
        yield
        return
    try:
        _record(novel, debug_session, {'operation': operation + '.started'}, 'package-measured')
    except Exception:
        _warning()
        token = _ACTIVE.set(None)
        try:
            yield
        finally:
            _ACTIVE.reset(token)
        return
    token = _ACTIVE.set((novel, debug_session))
    try:
        with span(operation):
            yield
    finally:
        _ACTIVE.reset(token)
