# Implementation ledger

## 2026-10-29 — Baseline

- Starting revision: `2a15eccd04b59cc66006ecd738ad53a30e6e02f5` on main. Existing untracked feature-002 design artifacts are preserved.
- Requirements checklist: 16/16 checked; no extension hooks. Python ignore patterns already cover environments/build outputs/caches; no extra ignore files required for the Python project.
- Feature 001 remains functionally qualified under its owner-amended scope. No retired latency/novice/manual requirements are reopened.
- Python environment: `.venv/Scripts/python.exe`, Python 3.13.13, existing validator dependencies. Initial module discovery mistook local build/ for an installed build frontend; executable build/setuptools/twine were absent. Build-only tools and a YAML parser were subsequently installed in this venv, not system Python.
- Initial sandbox baseline failed on temporary Git repository access/cleanup. This is environmental evidence, not a passing or failing product baseline. Unchanged normal-access rerun requested.

## Evidence index

FR-001–FR-018 / SC-001–SC-008 map to tasks.md. Task markers change only when the corresponding work and required evidence are complete. Local candidate, public installation, actual host capture, and subjective human approval remain separate. Publication/account changes, license selection and workflow dispatch are not authorized by local implementation alone.

## Local delivery and task checkpoints

T001–T005: starting state, read-only public preflight, baseline contracts, shared offline version and clean-install harness complete. Requirements checklist stays read-only at 16/16. Initial sandbox Git/temp and build failures are environmental and retained separately from subsequent normal-access results.

T006–T013: name-only CLI, source artifact, readable/JSON output, guide scaffold and wheel verification complete. Test failures preceded parser/request/version implementation. Legacy JSON without --json preserves exact CRLF/Unicode brief text. Local package is provisional 0.1.0; no public install claimed.

T014–T018: original request/mode and brief equality, original transaction reuse, actual competing reservations, legacy safety, cleanup-required output and actionable diagnostics verified. Changed-name/same-brief retry initially failed its regression, then passed after request comparison. Missing-dependency/identity diagnostics also followed observed failing tests. Baseline and optional evidence checkpoints remain separate.

T019–T023: complete canonical guide, adapter/interpreter guidance, discovery and reconciled writer/developer docs delivered. Simulated pre-guide tests plus an actual archived wheel prove continuation does not change old novel resources. All 34 historical files/checkpoint remain intact. Missing fallback returns a diagnostic; old manifests are not upgraded. Actual guide-only host walkthroughs T024/T025 remain incomplete.

T026–T030: optional destination/title/language, exact Icelandic and spaces/defaults, separate request provenance and four installed invalid-input cases pass on both OSes. Optional CLI tests were observed failing before flag implementation.

T032: manual candidate/publish workflow is locally implemented, YAML/permissions/pins checked, and integrity/rejection tests pass. Official action commits were resolved read-only. No workflow availability/push/dispatch or remote success is claimed. Candidate identity/run/attempt/artifact and hashes are mandatory; publish never rebuilds. Public verification requires expected wheel/sdist hashes and actual public byte comparisons. Mocked checks are not public installation evidence.

Independent review identified and corrected interpreter symlink loss, cross-platform checkout line endings, missing public hash binding and cross-run artifact permission. Additional rejection tests exposed and closed wrong-attempt/artifact-ID/URL and empty-manifest cases. The maintainer explicitly instructed “keep it unlicensed for now”; no license was added.

## Final observed verification

- Earlier Windows broad suite: 191 total, 189 passed, two explicit privilege skips, exit 0. Final source changes have separate affected verification rather than being retroactively attributed to this run.
- Final affected Windows suite: 43 passed, exit 0; final fast contracts: 22 passed; supplementary provenance/fallback/reservation and legacy/continuation cases: three then two passed.
- Linux/WSL2 ext4 snapshot: 204 total, 201 passed and three Windows-only skips, exit 0. Later public empty-manifest guard separately passes fast contracts.
- Clean local-wheel installs/default/optional/refusal matrices pass on Windows and Linux, no inherited dependency sites, and reported interpreter executes pinned commands. Offline wheel identity/save/reopen and isolated sdist rebuild are distinct checks.
- PyPI read-only listing returned 404; name control/publisher access remains unverified. License selection is resolved as intentionally unlicensed, not an outstanding question.

Details and limits: [readiness](../../tests/evaluations/package-init-readiness.md). Local artifact/source hashes: [manifest](../../tests/evaluations/package-init-release-manifest.json). There is no remote candidate identity; no native Codex host walkthrough, human/novice approval, push or publication. T024/T025, T031 and T033–T040 remain unchecked. Do not mark full feature complete from local passes.

## Convergence implementation — 2026-10-29

T041 and T042 are complete. Three new regressions first failed on the empty destination and missing pip-selection binding. The CLI now rejects an explicitly empty destination before invoking initialization. Public verification records pip's installation report, accepts exactly one normalized product name/version, and binds the selected filename and SHA-256 to the approved wheel or source archive. Another same-version platform wheel is rejected before package validation. The workflow retains that selected identity in its uploaded JSON evidence.

Corrected local artifacts are in `dist/package-init-convergence`; their hashes and current source hashes are in the local-only manifest. Previous local hashes and logs remain historical. Windows affected contracts: 30 passed. Linux full suite: 208 total, 205 passed, three Windows-only skips. Clean installed default/options/refusal matrices pass on both platforms, now including empty destination as the fifth refusal case. Windows wheel resource identity and pinned save/reopen pass. Build, metadata checks and separate source-archive rebuild pass. See the convergence evidence section in readiness.

31/45 tasks are complete. T043–T045 remain open along with their original release/host prerequisites. No push, dispatch, publisher configuration, public install or publication occurred. Remote candidate creation requires explicit authorization and verified distribution control; actual Codex walkthrough evidence must follow that candidate. Intentionally unlicensed remains the settled decision. No extension hooks exist, and the requirements checklist remains unchanged.
