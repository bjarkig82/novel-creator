"""Require complete observed pairs and pin this additional delegated evidence."""
import hashlib
import json
from pathlib import Path

folder = Path(__file__).resolve().parent
cases = json.loads((folder / "case-verification.json").read_bytes())
assert cases["ok"]
expected = {(d["case_id"], language) for path in folder.glob("*-driver.json")
            if "case_id" in (d := json.loads(path.read_bytes())) for language in d["inputs"]}
observed = {(c["case_id"], c["language"]) for c in cases["cases"]}
assert observed == expected, {"missing": sorted(expected - observed), "extra": sorted(observed - expected)}
assert len(observed) == len(cases["cases"])
for case in cases["cases"]:
    assert case["source_type"] == "delegated" and case["novice_evidence"] is False
    assert case["exact_input_saved"] and case["exact_response_saved_and_displayed"] and case["save_precedes_display"]
fresh = json.loads((folder / "resumption-verification.json").read_bytes())
assert fresh["ok"] and len(fresh["results"]) == 2
assert all(r["all_preexisting_records_recovered"] for r in fresh["results"])
files = {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(folder.rglob("*")) if p.is_file() and p.name != "evidence-manifest.json" and "__pycache__" not in p.parts}
output = {"ok": True, "task": "T163", "source_type": "delegated", "native_input_requirement_retained": True,
          "novice_requirement_retained": True, "case_observations": len(observed), "fresh_host_tasks": 2,
          "full_acceptance_matrix_complete": False, "human_semantic_review": False,
          "interrupted_before_display_observed": False, "files": files}
(folder / "evidence-manifest.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in output.items() if k != "files"}, indent=2))
