"""UTF-8 JSON command boundary. No subprocess shell interpolation."""
import argparse
import json
import sys


class ToolError(Exception):
    def __init__(self, code, message, *, affected_refs=None, checkpoint=None, pending=None,
                 expected_head=None, actual_head=None, data=None):
        super().__init__(message)
        self.code, self.checkpoint, self.pending = code, checkpoint, pending
        self.affected_refs = affected_refs or []
        self.expected_head, self.actual_head = expected_head, actual_head
        self.data = data

    def result(self):
        result = {"ok": False, "error": {"code": self.code, "message": str(self),
                "affected_refs": self.affected_refs, "retryable": self.code in (3, 5, 6)},
                "last_confirmed_checkpoint": self.checkpoint, "pending_exchange_id": self.pending}
        if self.expected_head is not None or self.actual_head is not None:
            result["error"].update(expected_git_head=self.expected_head, actual_git_head=self.actual_head)
        if self.data is not None:
            result['data'] = self.data
        return result


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ToolError(2, message)


class Once(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise ToolError(2, 'Supply ' + option_string + ' only once')
        setattr(namespace, self.dest, values)


class SwitchOnce(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise ToolError(2, 'Supply ' + option_string + ' only once')
        setattr(namespace, self.dest, True)


def _update_dispatch(args):
    from . import update
    if args.update_action == 'status':
        if any((args.version, args.python, args.apply, args.preview, args.expected_head, args.confirm_quiescent, args.retry)):
            raise ToolError(2, 'Update status accepts only --novel, --operation and --json')
        return update.status(args.novel, operation_id=args.operation)
    if args.update_action == 'recover':
        if not args.operation or any((args.version, args.python, args.apply, args.preview, args.confirm_quiescent)):
            raise ToolError(2, 'Update recovery requires --operation; inspection/retry cannot change release or runtime')
        if bool(args.retry) != (args.expected_head is not None):
            raise ToolError(2, 'Recovery retry requires --retry and --expected-head together')
        return update.recover(args.novel, operation_id=args.operation, retry=bool(args.retry), expected_head=args.expected_head)
    if args.operation is not None or args.retry:
        raise ToolError(2, '--operation/--retry require update status or recover')
    if args.apply:
        if not all((args.preview, args.version, args.expected_head)) or args.python is not None:
            raise ToolError(2, 'Apply requires --preview, --version and --expected-head; its runtime is already pinned')
        return update.apply(args.novel, preview_id=args.preview, version=args.version,
                            expected_head=args.expected_head, confirm_quiescent=bool(args.confirm_quiescent))
    if any((args.preview, args.expected_head, args.confirm_quiescent)):
        raise ToolError(2, 'Preview application arguments require --apply')
    return update.preview(args.novel, version=args.version, python=args.python)


def _init_request(args):
    from pathlib import Path
    import os
    import re
    import unicodedata
    if args.path is not None and args.path == '':
        raise ToolError(2, 'Destination must not be empty; omit --path to use NAME')
    if args.name is None:
        if args.title is not None or args.language is not None:
            raise ToolError(2, '--title and --language require NAME and cannot be mixed with --brief-file')
        if not args.path or not args.brief_file:
            raise ToolError(2, 'Use init NAME, or init --path PATH --brief-file FILE')
        return None
    if args.brief_file is not None:
        raise ToolError(2, 'Choose name-only initialization or --brief-file, not both')
    if args.title is not None and not args.title.strip():
        raise ToolError(2, 'Working title must not be empty')
    name = args.name
    if (not name.strip() or name in ('.', '..') or '/' in name or '\\' in name
            or any(unicodedata.category(c) == 'Cc' for c in name)):
        raise ToolError(2, 'Novel name must be a nonempty single folder name; use --path for its location')
    if os.name == 'nt' and (re.search(r'[<>:"|?*]', name) or name.endswith((' ', '.'))
            or re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', name, re.I)):
        raise ToolError(2, 'Novel name is not a valid Windows folder name')
    target = Path(args.path if args.path is not None else name).absolute()
    return {'request_type': 'cli_init_v1', 'name': name, 'resolved_destination': str(target),
            'title_argument': args.title, 'language_argument': args.language}


def parser():
    from importlib.resources import files
    from . import __version__
    try:
        guide = str(files('novel_creator.workflows').joinpath('getting-started.md'))
    except ModuleNotFoundError as error:
        if error.name != 'novel_creator.workflows':
            raise
        # Pinned novel layout keeps resources beside src, not in its package.
        from pathlib import Path
        guide = str(Path(__file__).resolve().parents[2] / 'workflows/getting-started.md')
    p = Parser(prog="novel-creator", epilog='Getting started: ' + guide)
    p.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    commands = p.add_subparsers(dest="command", required=True)
    # A pinned legacy launcher lives beside its src directory. It does not
    # contain the setup resources, even if an editable package is also installed.
    from pathlib import Path
    if not (Path(__file__).resolve().parents[2] / 'run.py').is_file():
        notebook = commands.add_parser('notebook', description='New novels with agent-maintained Markdown notes')
        notebook_actions = notebook.add_subparsers(dest='notebook_action', required=True)
        notebook_init = notebook_actions.add_parser('init')
        notebook_init.add_argument('name')
        notebook_init.add_argument('--path', action=Once)
        notebook_init.add_argument('--title', action=Once)
        notebook_init.add_argument('--language', choices=('en', 'is'), action=Once)
        notebook_init.add_argument('--host', choices=('codex', 'claude', 'both'), action=Once)
        notebook_init.add_argument('--skill-source', choices=('project', 'plugin'), action=Once)
        notebook_init.add_argument('--json', action=SwitchOnce)
        notebook_init.set_defaults(brief_file=None)
        notebook_update = notebook_actions.add_parser('update', description='Preview or explicitly add focused methods to an existing story notebook')
        notebook_update.add_argument('--path', required=True, action=Once)
        notebook_update.add_argument('--apply', action=SwitchOnce)
        notebook_update.add_argument('--preview', action=Once)
        notebook_update.add_argument('--expected-head', action=Once)
        notebook_update.add_argument('--json', action=SwitchOnce)
    update = commands.add_parser('update', description='Explicit published-release preview or local update status')
    update.add_argument('update_action', nargs='?', choices=('status', 'recover'))
    update.add_argument('--novel', required=True, action=Once)
    update.add_argument('--version', action=Once)
    update.add_argument('--python', action=Once)
    update.add_argument('--operation', action=Once)
    update.add_argument('--apply', action=SwitchOnce)
    update.add_argument('--preview', action=Once)
    update.add_argument('--expected-head', action=Once)
    update.add_argument('--confirm-quiescent', action=SwitchOnce)
    update.add_argument('--retry', action=SwitchOnce)
    update.add_argument('--json', action='store_true')
    retro = commands.add_parser('retro').add_subparsers(dest='action', required=True)
    for action in ('status', 'enable', 'disable', 'begin', 'review', 'compare', 'prepare',
                   'validate', 'publish', 'resume', 'release', 'notices'):
        target = retro.add_parser(action)
        targets = [target]
        if action == 'notices':
            notices = target.add_subparsers(dest='notice_action', required=True)
            targets = [notices.add_parser(name) for name in ('pending', 'reserve', 'confirm', 'reconcile')]
            for child in targets:
                if child.prog.endswith('pending'):
                    child.add_argument('--language', choices=('en', 'is'))
                if child.prog.endswith('reserve'):
                    child.add_argument('--input', required=True)
                if child.prog.endswith(('confirm', 'reconcile')):
                    child.add_argument('--reservation', required=True)
        for child in targets:
            child.add_argument('--novel', required=True)
            child.add_argument('--json', action='store_true')
        if action == 'enable':
            target.add_argument('--checkout', required=True)
            target.add_argument('--authorize-draft-prs', required=True, action='store_true')
        if action in ('begin', 'review', 'compare', 'validate'):
            target.add_argument('--input', required=True)
        if action in ('status', 'review', 'compare', 'prepare', 'validate', 'publish', 'resume', 'release'):
            target.add_argument('--run', required=action != 'status')
        if action == 'release':
            target.add_argument('--confirm-abandon', required=True, action='store_true')
    init = commands.add_parser("init", epilog='Getting started: ' + guide,
        description='Create an independent novel with init NAME; creative choices can wait.')
    init.add_argument('name', nargs='?', help='Novel folder name and provisional working title')
    init.add_argument("--path", action=Once, help='Full destination; defaults to current directory/NAME')
    init.add_argument("--brief-file", action=Once, help='Legacy UTF-8 brief; requires --path and no NAME')
    init.add_argument('--title', action=Once, help='Working title; defaults to NAME')
    init.add_argument('--language', action=Once, choices=('en', 'is'), help='Manuscript language; defaults to en')
    capture = commands.add_parser('input').add_subparsers(dest='action', required=True).add_parser('capture')
    capture.add_argument('--capture-file', required=True)
    capture.add_argument('--source', choices=('native_user', 'delegated', 'realtime_delegation'), required=True)
    capture.add_argument('--thread-id')
    capture.add_argument('--turn-id')
    capture.add_argument('--source-thread-id')
    capture.add_argument('--evaluation-only', action='store_true')
    capture.add_argument('--json', action='store_true')
    exchange = commands.add_parser("exchange").add_subparsers(dest="action", required=True)
    save = exchange.add_parser("save")
    save.add_argument("--input", required=True)
    session = commands.add_parser("session").add_subparsers(dest="action", required=True)
    operations = [save, session.add_parser("list")]
    for name in ("context", "inspect", "validate", "recover"):
        sub = commands.add_parser(name)
        operations.append(sub)
        if name == "context":
            sub.add_argument("--session")
            sub.add_argument('--view', choices=('current', 'working', 'full'), action=Once,
                             help='Context projection; defaults to full')
            sub.add_argument('--focus', action='append', metavar='ID', help='Working view: stable record ID; repeatable')
            sub.add_argument('--query', action=Once, metavar='TEXT', help='Working view: Unicode lexical search')
            sub.add_argument('--limit', action=Once, type=int, metavar='N',
                             help='Working view: 1–100 retrieved records; defaults to 12 (global warnings are additional)')
        if name == "inspect":
            sub.add_argument("--kind")
            sub.add_argument("--id")
            sub.add_argument("--revision", type=int)
        if name == "recover":
            sub.add_argument("--exchange", required=True)
            sub.add_argument("--retry", action="store_true")
            sub.add_argument("--expected-head")
    for sub in operations:
        sub.add_argument("--novel", required=True)
    for sub in [init, *operations]:
        sub.add_argument("--json", action="store_true")
    return p


def main(argv=None):
    # JSON is a UTF-8 interface regardless of terminal locale or Python's
    # UTF-8 mode (which isolated interpreters ignore in the environment).
    # Embedded callers may supply StringIO streams without reconfigure.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    try:
        args = parser().parse_args(argv)
        if args.command == 'notebook' and args.notebook_action == 'update':
            from .notebook import update
            if not args.path:
                raise ToolError(2, 'Notebook update requires a nonempty --path')
            result = update(args.path, apply=bool(args.apply), preview_id=args.preview,
                            expected_head=args.expected_head)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            else:
                data = result['data']
                print(('Notebook methods installed: ' if data['applied'] else 'Notebook update preview: ') + data['novel_path'])
                print('Reviewed HEAD: ' + data['reviewed_head'])
                print('Preview ID: ' + data['preview_id'])
                for change in data['changes']:
                    print(change['action'] + ': ' + change['path'])
                print(data['next_action'])
            return 0
        if args.command == 'notebook':
            from .notebook import initialize
            request = _init_request(args)
            result = initialize(request['resolved_destination'],
                                title=args.title if args.title is not None else args.name,
                                language=args.language or 'en',
                                host=args.host or 'codex', skill_source=args.skill_source or 'project')
            if args.json:
                print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            else:
                print('Story notebook ready: ' + result['data']['novel_path'])
                print('Format: ' + result['data']['format'] + ' version ' + str(result['data']['version']))
                print('Language: ' + result['data']['language'])
                print(result['data']['next_action'])
            return 0
        if args.command == 'update':
            try:
                result = _update_dispatch(args)
            except (ValueError, TypeError, KeyError, AttributeError, RecursionError) as malformed:
                raise ToolError(4, 'Unsupported or inconsistent update metadata; preserve the book and inspect its release/operation evidence',
                    data={'operation_id': args.operation, 'preview_id': args.preview, 'ready': False}) from malformed
            except OSError as failure:
                raise ToolError(5, 'Update filesystem/preparation operation failed; preserve the operation evidence before recovery',
                    data={'operation_id': args.operation, 'preview_id': args.preview, 'ready': False}) from failure
            except ToolError as error:
                if error.data is None:
                    error.data = {'operation_id': args.operation, 'preview_id': args.preview, 'ready': False}
                raise
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            return 0
        if getattr(args, 'novel', None) and args.command != 'update':
            from .maintenance import ensure_ready
            ensure_ready(args.novel, read_only=args.command in ('context', 'inspect', 'validate', 'session'))
        if args.command == 'retro':
            from .retro import dispatch
            result = dispatch(args)
            print(json.dumps({'ok': True, 'data': result}, ensure_ascii=False, allow_nan=False))
            return 0
        if args.command == 'input':
            from pathlib import Path
            from . import host_input, records
            try:
                data = host_input.capture(records.loads(Path(args.capture_file).read_bytes()),
                    thread_id=args.thread_id, turn_id=args.turn_id, source=args.source,
                    source_thread_id=args.source_thread_id, evaluation_only=args.evaluation_only)
            except (ValueError, TypeError) as error:
                raise ToolError(2, str(error)) from error
            print(json.dumps({'ok': True, 'data': data}, ensure_ascii=False, allow_nan=False))
            return 0
        if args.command == 'init':
            from pathlib import Path
            from .install import initialize
            request = _init_request(args)
            if request is None:
                try:
                    raw = Path(args.brief_file).read_bytes().decode('utf-8', errors='strict')
                except UnicodeError as error:
                    raise ToolError(2, 'Brief must be strict UTF-8 JSON') from error
                result = initialize(args.path, raw)
            else:
                brief = {'title': args.title if args.title is not None else args.name}
                if args.language is not None:
                    brief['manuscript_language'] = args.language
                raw = json.dumps(brief, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
                result = initialize(request['resolved_destination'], raw, request=request)
            if request is None or args.json:
                print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            else:
                data = result['data']
                status = 'Novel ready' if data['ready'] else 'Novel saved; recovery required'
                if data.get('already_initialized'):
                    status = 'Existing novel; settings and installed workflows preserved'
                print(status + ': ' + data['novel_path'])
                print('Python interpreter: ' + data['runtime_python'])
                print('Pinned launcher: ' + data['launcher_path'])
                print('Getting started: ' + data['getting_started_path'])
                for warning in result.get('warnings', []):
                    print('Note: ' + str(warning))
                print(data['next_action'])
            return 0
        if args.command == 'recover':
            from .storage import recover
            if args.retry and args.expected_head is None:
                raise ToolError(2, 'Recovery retry requires --expected-head (use unborn before the first commit)')
            result = recover(args.novel, args.exchange, retry=args.retry, expected_head=args.expected_head)
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            return 0
        if args.command in ('context', 'validate', 'inspect') or (args.command == 'session' and args.action == 'list'):
            from .context import read
            result = read(args.novel, operation=args.command, session=getattr(args, 'session', None),
                          kind=getattr(args, 'kind', None), identifier=getattr(args, 'id', None),
                          revision=getattr(args, 'revision', None), view=getattr(args, 'view', None) or 'full',
                          focus=getattr(args, 'focus', None), query=getattr(args, 'query', None),
                          limit=getattr(args, 'limit', None))
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            return 0
        if args.command == "exchange" and args.action == "save":
            from pathlib import Path
            from . import records, storage
            try:
                payload = records.loads(Path(args.input).read_bytes())
            except (ValueError, TypeError) as error:
                raise ToolError(2, "Input must be strict UTF-8 JSON") from error
            result = storage.save(args.novel, payload)
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
            return 0
        raise ToolError(4, "This operation is not yet implemented")
    except ModuleNotFoundError as missing:
        if missing.name not in ('jsonschema', 'jsonschema_rs', 'packaging'):
            raise
        error = ToolError(4, 'Required validator/version dependency is unavailable; use the configured Novel Creator Python environment or repair its package installation')
        print(json.dumps(error.result(), ensure_ascii=False))
        print(str(error), file=sys.stderr)
        return error.code
    except OSError as failure:
        message = ('Git executable is unavailable; install Git >=2.39 and check PATH'
                   if isinstance(failure, FileNotFoundError) and failure.filename == 'git'
                   else 'Local input or filesystem operation failed; check the selected file/path and permissions, preserve any partial initialization and retry unchanged')
        error = ToolError(5, message)
        print(json.dumps(error.result(), ensure_ascii=False))
        print(str(error), file=sys.stderr)
        return error.code
    except ToolError as error:
        print(json.dumps(error.result(), ensure_ascii=False, allow_nan=False))
        print(str(error), file=sys.stderr)
        return error.code
