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
def repository(unborn=False, object_format=None, prefix="novel-test-", parent=None):
    with tempfile.TemporaryDirectory(prefix=prefix, dir=parent) as directory:
        # Windows temp locations may resolve through an alias/junction. Pass a
        # canonical root without relaxing production traversal/symlink checks.
        root = Path(directory).resolve()
        git(root, "init", "-b", "main", *(['--object-format=' + object_format] if object_format else []))
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


def held_conflict_transition(root=None, disposition='deferred'):
    """A blocked proposal and a later acceptance with no conflict resolution."""
    first = envelope(root)
    proposal = idea(first)
    finding = record(first, 'finding', category='knowledge', assessment='conflict',
        severity='significant', affected_refs=[{'id': proposal['id']}],
        explanation='Knowledge arrives too late', consequences=[], resolution_options=[],
        disposition=disposition, decision_ids=[], narrative_explanation=None)
    first = seal(dict(first, record_versions=[proposal, finding]))
    exchange = envelope(root, previous=first)
    exchange['messages'][0]['text'] = 'Accept the proposal.'
    source = {'type': 'message', 'exchange_id': exchange['exchange_id'],
              'message_id': exchange['messages'][0]['message_id']}
    decision = record(exchange, 'decision', action='accept', user_message_ref=source,
        span={'start': 0, 'end': 19}, target_refs=[{'id': proposal['id'], 'revision': 2}],
        selected_parts=[], prior_refs=[], result_refs=[], reason='Accept proposal only',
        affected_refs=[], review_required_refs=[], source_refs=[source], origin='supplied')
    accepted = dict(proposal, revision=2, previous_revision=1, status='accepted',
                    decision_ids=[decision['id']], source_refs=[source], origin='supplied')
    exchange['record_versions'] = [accepted, decision]
    return first, exchange, finding
