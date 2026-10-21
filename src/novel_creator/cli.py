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
    try:
        args = parser().parse_args(argv)
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
