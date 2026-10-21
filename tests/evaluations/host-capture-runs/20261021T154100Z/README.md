# Windows Desktop preflight — BLOCKED

Date: 2026-10-21, Atlantic/Reykjavik (UTC). Cases A–F were not started.
The user explicitly required stopping if `cleanup_required` is true. Setup
returned that condition after committing bootstrap. No cleanup was attempted.

## Observed environment

- Desktop version 26.1016.51333, build 21161, prod channel, obtained from the
  app's `check_app_update` tool. This is Desktop evidence, not a CLI version.
- Model selector: **GPT-6.1 Sol, Medium**, reported by the user in this chat.
  Model revision/build unavailable; no identifier inferred from the agent identity.
- Windows 11, OS build 10.0.26300; filesystem type unverified.
- Python 3.13.13, Git 2.53.0.windows.3, jsonschema 4.26.0.
- Interpreter: `C:\Users\BjarkiGunnarsson\source\repos\Personal\novel-creator\.venv\Scripts\python.exe`.
- Pinned dependencies installed in a new isolated `.venv`; `pip check` passed.
  Default Python is an unconfigured pyenv shim; `py` is absent. Bundled Python
  3.12.14 was also found, but was not used for the fixture.

## Fixture and retained artifacts

Exact fixture folder:
`C:\Users\BjarkiGunnarsson\novel-creator-host-tests\spike-20261021T154100Z`

Created using the unchanged `tests/fixtures/host-spike/setup.py`. The helper
rejects existing paths and paths inside existing repositories. It configured
only this disposable repository's Git identity. No push or global config change.

Evidence is in `.novel-creator/local/evidence/preflight/` inside that fixture,
including observations, manifest copy, checksum verification, original local
receipt copy, HEAD/log/status/context readbacks and test logs. Extra JSON is
inside `evidence/`, not directly in `local/`. The production receipt is retained.
All 13 installed manifest checksums matched.

Setup stdout returned `ok: true`, `data.saved: true`, `already_saved: false`,
**`cleanup_required: true`**, warning `Saved; managed index recovery required`.
Checkpoint verified through normal-access Git and fixture context:

- HEAD: `411b27a2635c1d6394d55f624c87f85b75f6ae60`
- Exchange: `126934f0-4f30-464b-8988-3aa6a289f706`
- Sequence: 1 (bootstrap), no saved user/assistant messages.
- Context reports `display_confirmed: false`.
- Git status reports the bootstrap exchange staged as deleted and its worktree
  directory untracked, consistent with incomplete managed-index synchronization.
  This observation does not identify the root cause.

A sandboxed context read returned null checkpoint while Git reported permission
denied. That read is excluded as checkpoint evidence; normal-access readback
verified the actual committed bootstrap above.

## Baseline checks

The first sandboxed run completed 52 tests with 5 failures and 32 errors in
105.501 seconds. Its temp directory was inside the framework and sandbox
restrictions affected execution. A targeted run using the default Windows temp
path failed with `Symlink or traversing novel root is not allowed`. These are
retained diagnostics, not evidence that the baseline passes.

A second full baseline used a fresh canonical temp folder outside repositories
with normal filesystem access: **52 tests in 260.827 seconds; 8 failures and
1 error**, process exit 1. See `automated-tests-native-temp.txt` for full output.
Failures include installed-fixture continuation (code 3: prior transaction
requires recovery), managed-index cleanup/retry expectations and last-verifiable
checkpoint reporting. The error is Windows symlink creation privilege
(`WinError 1314`). Root causes of the assertion failures remain unverified;
they must not all be attributed to the sandbox. No product or test code was
changed to make tests pass. Optional Bash smoke checks were not run after this
mandatory baseline failure and fixture stop condition.

## Gate review

| Case | Result | Actual input/response/receipt/display evidence |
|---|---|---|
| A — initial and two automatic turns | Unverified | Not started; bootstrap cleanup blocks writes |
| B — identical retry | Unverified | No conversation payload prepared or retried |
| C — interrupted display | Unverified | No interruption attempt or timing observation |
| D — fresh-chat recovery | Unverified | No new fixture chat opened; subprocess readback is not this case |
| E — visible failure | Unverified | No test lock injected; bootstrap warning is not the required code-6 exercise |
| F — failed-attempt recovery | Unverified | No failed conversation payload exists; no lock or receipt removed |

No screenshots, display-order observations or human interruption observations
were collected. No assumptions about display or acceptance are made. There is
no genuine conversation payload to compare with visible final text yet.

**T012/T069/T089 remain unchecked and unverified. T013 remains BLOCKED.**
The setup cleanup warning independently requires stopping under the user's
safeguard. Preserve the fixture, receipts and history; investigate through a
separately authorized foundation/adapter task before a new experiment. No
dependent story implementation, history reset, manual index repair, receipt
deletion, custom runtime, transcript scraping or model API call was performed.

No Desktop action is currently needed. Resume the human-driven A–F sequence only
after the blocker is resolved and preflight supports a clean fixture. Retain this
fixture as evidence; do not reuse or erase it to force a passing outcome.
