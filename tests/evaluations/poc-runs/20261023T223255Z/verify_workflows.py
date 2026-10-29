"""Check actual POC question captures and visible resumption references."""
import json
import hashlib
import re
from pathlib import Path
import sys

folder = Path(__file__).resolve().parent
root = folder.parents[3]
sys.path.insert(0, str(root / "src"))
from novel_creator import records, storage
from novel_creator.install import bundle_files

def question_check(exchange):
    reply = exchange["messages"][1]
    questions = [r for r in exchange["record_versions"] if r["kind"] == "question"]
    assert questions, "New open question was displayed without a question record"
    session = next(r for r in exchange["record_versions"] if r["kind"] == "session")
    for q in questions:
        assert q["state"] == "open" and q["id"] in session["unresolved_question_ids"]
        assert q["text"] in reply["text"]
        refs = [s for s in q["source_refs"] if s.get("type") == "message"
                and s.get("exchange_id") == exchange["exchange_id"] and s.get("message_id") == reply["message_id"]]
        assert refs, q["id"]
        for source in refs:
            if "range" in source:
                span = source["range"]
                assert reply["text"][span["start"]:span["end"]] == q["text"]
    return [q["id"] for q in questions]

if sys.argv[1:] == ["--baseline"]:
    before = root / "tests/evaluations/product-host-runs/20261023T202447Z/case-bundles/G01-is.json"
    question_check(json.loads(before.read_bytes()))
    raise SystemExit("Unexpected baseline pass")

run = json.loads((folder / "run.json").read_bytes())
verified = json.loads((folder / "case-verification.json").read_bytes())
assert {(v["case_id"], v["language"]) for v in verified["cases"]} == {
    (case, lang) for case in ("SETUP", "QUESTION", "PROPOSAL", "RESUME") for lang in ("en", "is")}
results = []
for language, task in run["tasks"].items():
    novel = Path(task["novel_path"])
    for path, expected in bundle_files().items():
        assert (novel / path).read_bytes() == expected, path
    manifest = json.loads((novel / ".novel-creator/manifest.json").read_bytes())
    for relative, digest in manifest['checksums'].items():
        assert hashlib.sha256((novel / relative).read_bytes()).hexdigest() == digest, relative
    setup = json.loads((folder / f"case-bundles/SETUP-{language}.json").read_bytes())
    assert setup["messages"][1]["text"] == "POC capture ready."
    question_ids = {}
    for case in ("QUESTION", "PROPOSAL"):
        exchange = json.loads((folder / f"case-bundles/{case}-{language}.json").read_bytes())
        question_ids[case] = question_check(exchange)
    history = storage.read_history(novel)
    state = records.fold(history)
    resumed = json.loads((folder / f"case-bundles/RESUME-{language}.json").read_bytes())
    reply = resumed["messages"][1]["text"]
    relevant = [r for r in state.values() if r["kind"] in ("idea", "question")]
    assert relevant
    for r in relevant:
        assert r["id"][:8] in reply, ("Missing visible record reference", r["id"])
    previous = history[history.index(resumed) - 1]
    checkpoint_named = (resumed["expected_git_head"][:8] in reply or previous['exchange_id'][:8] in reply
        or re.search(r'(?:checkpoint|varðstöð)\s*[:#]?\s*' + str(previous['sequence']) + r'\b', reply, re.I))
    assert checkpoint_named, "Missing visible checkpoint"
    results.append({"language": language, "current_bundle_verified": True,
        "manifest_version": manifest["bundle_version"], "captured_question_ids": question_ids,
        "visible_summary_references": [{"id": r["id"], "revision": r["revision"]} for r in relevant],
        "source_type": "delegated", "native_user_input": False, "novice_evidence": False,
        "revision_citation_semantics": "Agent assessment recorded separately; IDs/checkpoint checked here"})
output = {"ok": True, "results": results}
(folder / "workflow-verification.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2))

