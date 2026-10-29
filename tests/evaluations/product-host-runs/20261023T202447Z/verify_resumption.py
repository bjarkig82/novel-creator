"""Read baseline or verify actual fresh tasks against pre-resumption checkpoints."""
import json
from datetime import datetime
from pathlib import Path
import subprocess
import sys

folder = Path(__file__).resolve().parent
root = folder.parents[3]
sys.path.insert(0, str(root / "src"))
from novel_creator import storage

run = json.loads((folder / "run.json").read_bytes())
if sys.argv[1:] == ["--prepare"]:
    for language, task in run["tasks"].items():
        command = [sys.executable, "-I", "-B", str(Path(task["novel_path"]) / ".novel-creator/run.py"),
                   "context", "--novel", task["novel_path"], "--json"]
        result = subprocess.run(command, capture_output=True, encoding="utf-8", check=True)
        context = json.loads(result.stdout)
        assert context["ok"]
        (folder / f"resumption-baseline-{language}.json").write_text(result.stdout, encoding="utf-8")
    print(json.dumps({"ok": True, "scope": "pre-resumption installed CLI baselines"}))
    raise SystemExit()

results = []
for language, fresh in run["fresh_tasks"].items():
    original = run["tasks"][language]
    novel = Path(original["novel_path"])
    evidence = novel / ".novel-creator/local/evidence/fresh-resumption" / fresh["thread_id"]
    before = json.loads((evidence / "before-context.json").read_bytes())
    baseline = json.loads((folder / f"resumption-baseline-{language}.json").read_bytes())
    # PowerShell's JSON date conversion can remove trailing fractional zeros.
    # Preserve that observed transformation; compare every other value exactly.
    transformations = []
    compared = json.loads(json.dumps(before))
    for observed, expected in zip(compared['data']['exchanges'], baseline['data']['exchanges']):
        if observed['recorded_at'] != expected['recorded_at']:
            assert datetime.fromisoformat(observed['recorded_at']) == datetime.fromisoformat(expected['recorded_at'])
            transformations.append({'exchange_id': observed['exchange_id'],
                'field': 'recorded_at', 'observed': observed['recorded_at'], 'original': expected['recorded_at']})
            observed['recorded_at'] = expected['recorded_at']
    assert compared == baseline, language
    assert before["data"]["saved_response_display"] == "unconfirmed"
    current = {r["id"]: r for r in before["data"]["records"]}
    assert len(current) == len(before["data"]["records"])
    history = storage.read_history(novel)
    resumed = [e for e in history if e["input_artifacts"] and
               e["input_artifacts"][0]["parsed_value"].get("thread_id") == fresh["thread_id"]]
    assert len(resumed) == 1
    exchange = resumed[0]
    assert exchange["expected_git_head"] == baseline["checkpoint"]["git_head"]
    assert exchange["previous_exchange_id"] == baseline["checkpoint"]["exchange_id"]
    assert all(r["kind"] == "session" for r in exchange["record_versions"]), language
    session_ids = {s["id"] for s in before["data"]["sessions"]}
    assert exchange["session_id"] in session_ids
    for r in exchange["record_versions"]:
        assert r["id"] == exchange["session_id"] and r["mode"] == current[r["id"]]["mode"]
    assert all(e["input_artifacts"][0]["parsed_value"]["source_type"] == "delegated"
               for e in resumed)
    (folder / f"fresh-before-context-{language}.json").write_text(
        json.dumps(before, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    results.append({"language": language, "thread_id": fresh["thread_id"],
        "all_preexisting_records_recovered": True, "record_count": len(current),
        "before_context_exactly_equal": before == baseline,
        "equivalent_timestamp_serializations": transformations,
        "prior_checkpoint": baseline["checkpoint"], "exchange_id": exchange["exchange_id"],
        "saved_mode_preserved": True, "session_id_preserved": True,
        "last_saved_response_exposed_display_unconfirmed": True,
        "no_creative_record_changes": True, "source_type": "delegated", "novice_evidence": False})
output = {"ok": True, "scope": "actual fresh delegated tasks reading committed context",
          "interrupted_before_display_observed": False, "full_three_session_capture_matrix_complete": False,
          "results": results}
(folder / "resumption-verification.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2))

