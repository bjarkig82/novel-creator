"""Disposable repositories: never writes global Git configuration."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import uuid
from contextlib import contextmanager


def uid():
    return str(uuid.uuid4())


def git(root, *args, env=None, check=True):
    return subprocess.run(["git", "-C", str(root), *args], env=env, check=check,
                          capture_output=True, text=True).stdout.strip()


@contextmanager
def repository(unborn=False):
    with tempfile.TemporaryDirectory(prefix="novel-test-") as directory:
        root = Path(directory)
        git(root, "init", "-b", "main")
        git(root, "config", "user.name", "Disposable Test")
        git(root, "config", "user.email", "test@example.invalid")
        (root / ".novel-creator/local").mkdir(parents=True)
        (root / ".novel-creator/manifest.json").write_text(json.dumps({"novel_id": uid(), "schema_version": "1.0"}))
        (root / ".gitignore").write_text(".novel-creator/local/\n")
        if not unborn:
            git(root, "add", ".gitignore", ".novel-creator/manifest.json")
            git(root, "commit", "-m", "Fixture installation")
        yield root


def envelope(root=None, previous=None, **updates):
    novel_id = (json.loads((root / ".novel-creator/manifest.json").read_text())["novel_id"] if root else uid())
    data = {"schema_version": "1.0", "novel_id": novel_id,
            "exchange_id": uid(), "sequence": 1,
            "previous_exchange_id": None, "previous_digest": None,
            "session_id": None, "expected_git_head": None,
            "recorded_at": "2026-10-21T12:00:00Z", "operation": "bootstrap",
            "messages": [], "input_artifacts": [], "record_versions": [],
            "continuity_review": {"coverage": "not_applicable", "reviewed_record_refs": [],
             "unavailable_refs": [], "canon_hold_refs": [], "finding_ids": [], "summary": "Fixture only"}}
    if root:
        data["expected_git_head"] = git(root, "rev-parse", "--verify", "HEAD", check=False) or None
    if previous:
        data.update(novel_id=previous["novel_id"], sequence=previous["sequence"] + 1,
                    previous_exchange_id=previous["exchange_id"], previous_digest=previous["payload_digest"],
                    operation="conversation", messages=[{"message_id": uid(), "role": "user", "text": "Explore Þóra."},
                    {"message_id": uid(), "role": "assistant", "text": "What does Þóra want?"}])
    data.update(updates)
    return seal(data)


def seal(data):
    data = copy.deepcopy(data)
    data.pop("payload_digest", None)
    data["payload_digest"] = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
    return data


def record(bundle, kind="idea", **fields):
    data = {"id": uid(), "kind": kind, "revision": 1, "previous_revision": None,
            "created_exchange_id": bundle["exchange_id"], "source_refs": [], "origin": "system_default"}
    data.update(fields)
    return data


def idea(bundle, **fields):
    return record(bundle, statement="Possibility", status="proposed", related_element_ids=[],
                  alternative_group_id=None, selected_parts=[], decision_ids=[], resulting_assertion_ids=[], **fields)


class FailAt:
    def __init__(self, point):
        self.point = point

    def __call__(self, point):
        if point == self.point:
            raise OSError("Injected failure: " + point)
