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


def parser():
    p = Parser(prog="novel-creator")
    commands = p.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--path", required=True)
    init.add_argument("--brief-file", required=True)
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
            try:
                raw = Path(args.brief_file).read_bytes().decode('utf-8', errors='strict')
            except UnicodeError as error:
                raise ToolError(2, 'Brief must be strict UTF-8 JSON') from error
            result = initialize(args.path, raw)
            print(json.dumps(result, ensure_ascii=False, allow_nan=False))
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
    except OSError:
        error = ToolError(5, "Local input or filesystem operation failed")
        print(json.dumps(error.result(), ensure_ascii=False))
        print(str(error), file=sys.stderr)
        return error.code
    except ToolError as error:
        print(json.dumps(error.result(), ensure_ascii=False, allow_nan=False))
        print(str(error), file=sys.stderr)
        return error.code
