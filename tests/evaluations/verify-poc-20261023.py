"""Reconcile the automated single-user POC without inventing manual evidence."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
base = root / "tests/evaluations"
run = base / "poc-runs/20261023T223255Z"
previous = json.loads((base / "delegated-input-support-manifest-20261023.json").read_bytes())
runtime = {p: digest for p, digest in previous["files"].items() if p.startswith("src/")}
for path, digest in runtime.items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest, path
checks = {}
for platform in ("windows", "linux"):
    raw = (base / f"{platform}-poc-workflows-20261023.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"Ran (\d+) tests in ([0-9.]+)s\s+OK\s*$", raw)
    assert match and int(match[1]) == 14, platform
    wheel = json.loads((base / f"{platform}-poc-wheel-20261023.json").read_bytes())
    assert wheel["ok"] and wheel["verified_source_files"] == 26
    archive = root / "dist/poc-20261023" / wheel["wheel"]
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == wheel["wheel_sha256"]
    checks[platform] = {"affected_tests": 14, "seconds": float(match[2]), "wheel_sha256": wheel["wheel_sha256"]}
assert checks["windows"]["wheel_sha256"] == checks["linux"]["wheel_sha256"]
workflows = json.loads((run / "workflow-verification.json").read_bytes())
assert workflows["ok"] and len(workflows["results"]) == 2
cases = json.loads((run / "case-verification.json").read_bytes())
assert cases["ok"] and len(cases["cases"]) == 8
expected = {(case["case_id"], language) for path in run.glob("*-driver.json")
            for case in [json.loads(path.read_bytes())] for language in case["inputs"]}
observed = {(c["case_id"], c["language"]) for c in cases["cases"]}
assert observed == expected and len(observed) == 8
for result in cases["cases"]:
    assert result["source_type"] == "delegated" and not result["novice_evidence"]
    assert result["exact_input_saved"] and result["exact_response_saved_and_displayed"] and result["save_precedes_display"]
performance = json.loads((base / "windows-poc-small-30-20261023.json").read_bytes())
assert performance["fixture"]["fully_validated"]
assert performance["fixture"]["exchanges"] == 100 and performance["fixture"]["sessions"] == 10
assert performance["fixture"]["active_assertions"] == 200
assert performance["read"]["completed_runs"] == 30 and performance["save"]["completed_runs"] == 30
paths = {p.relative_to(root).as_posix() for folder in ("src", "workflows", "schemas", "adapters/codex")
         for p in (root / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts}
paths.update(p.relative_to(root).as_posix() for p in run.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
paths.update(p.relative_to(root).as_posix() for p in base.glob("*poc*20261023*")
             if p.is_file() and p.name != "poc-manifest-20261023.json")
paths.update(("README.md", "docs/poc-quickstart.md", "docs/testing-and-completion-guide.md",
              "specs/001-novel-initialization-brainstorming/spec.md", "specs/001-novel-initialization-brainstorming/plan.md"))
output = {"ok": True, "scope": "single-user automated POC", "manual_tests_required": False,
    "novice_testers_in_scope": False, "human_or_native_outcomes_inferred": False,
    "full_semantic_matrix_complete": False, "large_fixture_performance_qualified": False,
    "checks": checks, "installed_host_observations": 8, "runtime_unchanged_from_full_suite": True,
    "small_fixture_performance": performance,
    "small_fixture_targets_met": performance['read']['passes'] and performance['save']['passes'],
    "files": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(paths)}}
(base / "poc-manifest-20261023.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in output.items() if k not in ("files", "small_fixture_performance")}, indent=2))

