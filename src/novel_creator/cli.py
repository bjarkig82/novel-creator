"""UTF-8 JSON command boundary. No subprocess shell interpolation."""
import argparse
import json
import sys


class ToolError(Exception):
    def __init__(self, code, message, *, affected_refs=None, checkpoint=None, pending=None,
                 expected_head=None, actual_head=None):
        super().__init__(message)
        self.code, self.checkpoint, self.pending = code, checkpoint, pending
        self.affected_refs = affected_refs or []
        self.expected_head, self.actual_head = expected_head, actual_head

    def result(self):
        result = {"ok": False, "error": {"code": self.code, "message": str(self),
                "affected_refs": self.affected_refs, "retryable": self.code in (3, 5, 6)},
                "last_confirmed_checkpoint": self.checkpoint, "pending_exchange_id": self.pending}
        if self.expected_head is not None or self.actual_head is not None:
            result["error"].update(expected_git_head=self.expected_head, actual_git_head=self.actual_head)
        return result


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ToolError(2, message)


class Once(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            raise ToolError(2, 'Supply ' + option_string + ' only once')
        setattr(namespace, self.dest, values)


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
    init = commands.add_parser("init", epilog='Getting started: ' + guide,
        description='Create an independent novel with init NAME; creative choices can wait.')
    init.add_argument('name', nargs='?', help='Novel folder name and provisional working title')
    init.add_argument("--path", action=Once, help='Full destination; defaults to current directory/NAME')
    init.add_argument("--brief-file", action=Once, help='Legacy UTF-8 brief; requires --path and no NAME')
    init.add_argument('--title', action=Once, help='Working title; defaults to NAME')
    init.add_argument('--language', action=Once, choices=('en', 'is'), help='Manuscript language; defaults to en')
    capture = commands.add_parser('input').add_subparsers(dest='action', required=True).add_parser('capture')
    capture.add_argument('--capture-file', required=True)
    capture.add_argument('--source', choices=('native_user', 'delegated'), required=True)
    capture.add_argument('--thread-id', required=True)
    capture.add_argument('--turn-id', required=True)
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
                          revision=getattr(args, 'revision', None))
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
        if missing.name not in ('jsonschema', 'jsonschema_rs'):
            raise
        error = ToolError(4, 'Required validator dependency is unavailable; use the configured Novel Creator Python environment or repair its package installation')
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
