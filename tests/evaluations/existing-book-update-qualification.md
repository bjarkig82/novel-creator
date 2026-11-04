# Existing-book Update Qualification

## Status - 2026-11-04 (qualification began 2026-11-03)

Preview, application, durable recovery, ownership guards and historical-book
integration are implemented. All 41 tasks are complete in the user-approved
delegated host-evaluation scope. Corrected-source Windows/Linux suites and both
platforms' distribution/historical-update verifiers passed. Final independent
verification confirmed the actual host journey, corrected status after writer
progress, exact saved/public response, preservation and artifact identities.
This is an unreleased
implementation, not a release-readiness claim.

The actual Windows Codex host completed the user-approved delegated evaluation:
human approval bound the exact preview; a real after-publication process stop
was inspected and recovered; a fresh host discovered the new update skill; and
one delegated continuation was captured, saved and compared with its actual
public dispatch. The corrected external controller subsequently reported that
same completed operation ready after the writer commit, with the entire book
unchanged. The host report retains identities, artifacts, failures and scope.

The milestone sections below retain earlier evidence and its limits. This current
status and the delivery checkpoint supersede their then-pending implementation
and Linux statements. Actual Windows host evaluation uses explicitly approved
delegation; direct native-user input and Linux host evidence remain unavailable.

## Qualified post-save status correction

The host completed its approved update/recovery and one saved continuation.
Independent verification confirmed the exact saved input/artifact/public reply,
two original exchanges and writer work, 39 installed resource checksums, and one
maintenance commit followed by one conversation commit. It then found that
explicit historical operation status incorrectly reported `checkpoint_changed`
after the legitimate conversation advanced HEAD. Ordinary pinned validation
still reported all three exchanges valid; no data or ownership was lost.

The status fix accepts proven descendant commits only for already-complete,
released operations on the original branch, with all installed-resource checks
retained. Pending/incomplete transactions remain bound to exact checkpoints.
Ancestry checks ignore replacement objects; unrelated rewritten history and
modified exclusive resources remain blockers. The reproduction failed before
the fix, and the complete 11-test CLI/status group passed after it. The installed
update verifier now checks status and idempotent apply after a real saved
exchange, plus safe recovery refusal when that later work changes the original
recovery checkpoint. The corrected artifacts and successful platform runs below
supersede the earlier delivery checkpoint for current automated qualification.

## Corrected frozen delivery - qualified 2026-11-04

The corrected snapshot contains 368 discovered tests and the same 182 input
paths, retained as `existing-book-update-statusfix-source-snapshot.json` beside
this ledger. Its SHA-256 is
`1513f5d4fc8e7423bb37870c46c220f618e88aa8a9564c36755fb09d458dbba4`.
Relative to the original snapshot, changes are limited to `update.py`, its CLI
regressions, `verify_update.py` and the final README qualification guidance.
All code/test/resource inputs are frozen during this qualification.

| Corrected artifact | SHA-256 | Scope |
| --- | --- | --- |
| Actual development wheel, version label 0.2.0 | `6ac0cdce204eb838950f0139bc02fa73cd14f292e40f81bce0ac4fe2ca4654af` | Unreleased current code; distinct from both published 0.2.0 and the earlier development wheel. |
| Controlled unpublished 0.3.0 target | `a8afa7652f4fbc84933ef0613f6d66854ae8926adae5b452ce79dd0437f1145a` | Only `novel_creator/update.py` differs among product files from the earlier controlled target. |

These artifacts are retained under `.tools/update-finalized/`. The full Windows
suite is partitioned into three independent processes: core 211, retrospective
86 and update 71 cases. Core passed 211 cases with two explicit symlink-privilege
skips; retrospective passed all 86 cases; updates passed all 71 cases without skips.
`windows-statusfix-discovery.json` lists every original
discovery position and its group; `windows-statusfix-aggregate.json` proves all
368 positions executed exactly once, without omissions, failures or errors.
Linux runs the complete unsharded
`unittest discover` suite against a fresh private installation.
Linux's complete 368-test run passed with three Windows-junction skips, exit 0
(2157.501s, informational). Both platform distribution verifiers passed corrected
wheel `6ac0cdce...`, and both historical-origin matrices passed controlled target
`a8afa765...`, including complete status after a new save and safe refusal of
changed recovery evidence. Windows group durations were 1582.106s, 2165.613s
and 5289.821s respectively; all durations are informational.

The first corrected-artifact verifier attempt expected recovery retry to accept
later writer progress. That expectation contradicted FR-011's unchanged-recovery-
evidence requirement; both platform artifact verifiers refused it safely. The
verifier was corrected to assert error 3 and unchanged book state for that retry,
while still requiring complete status and no-op application after the writer
commit. Product code, all 368 discovered test cases and their imported helpers
were unchanged. No discovered test module imports the artifact verifiers.
`verifier-only-snapshot-delta.json` records the single changed artifact-verifier
file; the original corrected snapshot above is retained. The final composite
snapshot is `existing-book-update-finalized-source-snapshot.json`, SHA-256
`8d5624d2b8623fdd563e4eac9649ab2adc5d7fd1cfa63a83c9783bb54eb75c03`.
Fresh artifact-verifier results use distinct `windows-finalized-*` and
`linux-final_statusfix_*` files; earlier failed outputs are retained rather than
reported passing. All product and full-suite inputs stayed frozen throughout.

The actual host's approved book remains on its original controlled artifact
`a1a12064...`; no different target was silently applied. The completed journey
used that exact reviewed artifact. The later external controller alone was
upgraded to corrected wheel `6ac0cdce...`; its read-only completed-status check
passed at the same saved HEAD with all 192 book/Git file hashes/modes, semantic
staging, target manifest and 39 exclusive checksums unchanged. The corrected
target's installation paths are qualified separately by the fresh platform
matrix. This is layered evidence for a status-only code correction, not a claim
that the human approved another target or that the book was reapplied.

## Original frozen delivery checkpoint (before status correction)

The final inputs comprise 182 hashed source/resource/test/configuration files and
366 discovered tests. `tests/evaluations/existing-book-update-source-snapshot.json`
retains the snapshot (also used locally as
`.tools/update-qualification/delivery-source-snapshot.json`);
`freeze.py check` confirmed all 182 inputs unchanged after both full suites.
Planning and evidence documents are outside that executable snapshot.
The retained snapshot SHA-256 is
`15ed167a691844a33f95d70f73b0ece7df0a062110ab5c07a5797a2b2e941aa4`.
Both platforms use Python 3.13.13 and packaging 26.3. Windows reports
`Windows-11-10.0.26300-SP0` and Git `2.53.0.windows.3`. Linux is Ubuntu 24.04.4
LTS under WSL2 (`6.6.87.2-microsoft-standard-WSL2`, glibc 2.39), Git `2.43.0`.
Durations are informational, not performance acceptance targets.

| Artifact | SHA-256 | Scope |
| --- | --- | --- |
| Actual built development wheel, version label 0.2.0 | `64bdd4a9de1962eb84f6be442ea6011c9c58c598682602b2b6ea9cf64320b286` | Current checkout built with setuptools; distinct from the approved published 0.2.0 archive below. |
| Controlled 0.3.0 target fixture | `a1a12064c8b029b48693a10c4871c516d4215e06a55aeb6ed3666f5f621997d2` | Unpublished test target; fixed fake public transport, never a claim that 0.3.0 exists publicly. |

Artifacts are retained in `.tools/update-delivery/`. No release was published,
global environment changed, real book updated, provider invoked or real GitHub
contribution made.

| Final check | Windows | Linux/WSL | Evidence/scope |
| --- | --- | --- | --- |
| `tests/verify_wheel.py` actual development wheel | Passed, exit 0 | Passed, exit 0 | `windows-delivery-wheel.json`, `linux-final_wheel.json`: 38 exact source-file identities, packaged resources/protocol, private product origins, English/Icelandic bootstrap/pinned saves, name-only initialization and historical 0.1.0-to-development-0.2.0 update. |
| `tests/verify_update.py` controlled newer target | Passed, exit 0 | Passed, exit 0 | `windows-delivery-update.json`, `linux-final_update.json`: approved 0.1.0/en and 0.2.0/is origins, read-only preview, one update commit, preserved writer work/history, restored guided session, pinned origins and subsequent synthetic save. |
| Final focused metadata, CLI and transaction guard group | 19 release/CLI tests passed; late-readiness/cache/Git checks passed in focused runs | 24 tests passed, exit 0 | `linux-final_guard.log` includes late resource/readiness edits, tampered preview cache, unsupported installation format and Git prerequisite checks plus full release/CLI contracts. |
| Full frozen delivery suite | Passed, 366 tests, two real-symlink privilege skips, exit 0 | Passed, 366 tests, three Windows-junction skips, exit 0 | `windows-delivery.log`, `linux-delivery.log`; Windows duration 4978.226s and Linux duration 1593.583s are informational. |

Named logs/JSON files above reside under `.tools/update-qualification/`. They are
local ignored outputs, and this ledger records their durable outcome and artifact
identities. Verifiers use disposable books, isolated installed controllers and
fake transport; they explicitly report that they are not native semantic/human
acceptance.

Linux's three skips are the Windows directory-junction regressions. Those three
cases passed in the Windows delivery run. Real-symlink tests passed on Linux;
Windows reports privilege-1314 skips where creating a real symlink is unavailable.

Both complete suites passed recovery at all 20 changed-resource checkpoints and
all 12 durable transaction checkpoints, plus obsolete-resource deletion, actual
historical-client guarded restart/save, live-owner refusal, unconfirmed-ownership
preservation and the retrospective state matrix. Linux completed on 2026-11-03;
Windows completed on 2026-11-04. Final artifact/snapshot hashes still match the
values above. `pip check` passed after the final dependency/code changes.

### Corrections and superseded runs

- A clean earlier Linux full suite passed 362 tests with three Windows-junction
  skips (`linux-final.log`) against development wheel
  `276ab8ab7878586fb4535288d3d2b001f4942a29fe38807017dd5e5be6647f23`.
  It predates final metadata/prerequisite regressions and does not replace the
  366-test delivery run.
- An earlier Linux run failed because two test harnesses prepended source-only
  imports over the installed package's resource modules. Those overrides were
  removed; targeted CLI/host tests and the clean full Linux suite passed.
- An earlier Windows suite was stopped and retained as incomplete after spanning
  a preview-cache format change: its parent held old code while subprocesses read
  new code. It is neither a passing run nor final-source product-failure evidence.
  Explicit UTF-8 fixture subprocess decoding was also corrected. The isolated
  legacy guarded-restart/save case subsequently passed for both source versions.
  Final delivery runs started only after source/test freeze.
- Real late-readiness regression tests initially failed. Final validation now
  rechecks exact resources, story/index state and launcher before owned-fence
  release, including after completion bookkeeping. The focused regressions pass.
- Same-version private installation is forced; product origins and bytes are
  verified before and after probes. Malformed release metadata and unsupported
  internal templates now return bounded structured errors. Repository hooks are
  suppressed for private updater Git operations; unrelated staging is preserved.

### Requirement evidence map

| Requirements / outcomes | Implementation and automated evidence | Remaining limit |
| --- | --- | --- |
| FR-001–FR-003; SC-001 | Release/preview/CLI contracts, fixed-source transport and explicit target/preview binding. | Controlled transport does not certify future public releases. |
| FR-004–FR-007; SC-002–SC-003 | Ownership/apply integration, partial staging, shared instructions/rules, obsolete-resource removal, pinned runtime and verifier save journeys; actual delegated Windows host reload/save verified. | Direct native-user input and Linux host remain unverified. |
| FR-008; SC-006 | Release prerequisites, wheel inventory/origin/hash checks, exact historical artifacts and both platform verifiers. | Only recorded artifacts/interpreters are qualified. |
| FR-009–FR-012; SC-004–SC-005 | Maintenance exclusion, live/dead owner tests, hard-process termination at durable and per-resource boundaries, offline exact-candidate recovery and idempotency. | FUP-001 excludes already-loaded legacy clients after OS guards release; close them before apply. |
| FR-013 | Historical-origin continuation and private installed-controller/package journeys on both platforms; fresh actual Windows host discovered all five installed skills including novel-update. | Linux host discovery remains unverified. |
| FR-014; SC-007 | Absent/disabled/enabled/revoked/mismatched grant preservation, unfinished/publication/notice blockers, retained contribution inspection. | No real GitHub publication exercised or authorized. |
| FR-015; SC-008 | Adversarial transport, seeded private values, inherited pip/Git/Python environment isolation and hook tests. | No provider or private upload involved. |
| FR-016 | Operational workflows, explicit apply/recovery arguments, structured CLI errors, en/is operational copy; human-approved preview, actual apply/recovery/reload and exact saved/public response verified in delegated Windows host evaluation. | Direct native-user input and Linux host remain unverified. |
| FR-017; SC-009 | Both full 368-test platform suites, corrected historical/distribution verifiers, final source freeze and independent actual delegated-host evidence reconciliation passed. | Qualification is limited to recorded artifacts and approved delegated host scope; no release/publication claim. |

All 17 functional requirements and nine success criteria map to tasks; the
read-only artifact consistency recheck found no new ambiguity, duplication,
unmapped task or constitutional conflict. The scoped runtime evidence above
supports task completion; mapping alone is not runtime qualification.
Requirements checklist remains 16/16.
No `.specify/extensions.yml` hooks are configured.

## Historical artifact identity

| Origin | Approved wheel SHA-256 |
| --- | --- |
| 0.1.0 | `cc8645556f74190dee9ac7527c3e66c0bc71574913b5bbae5ddff7516b8817a8` |
| 0.2.0 | `9872b3aa9a4a1629d4b6c50a1672f5acbd376130f08f9c7edcd0492381c632fa` |

Exact public archives are retained under `tests/fixtures/releases/` for offline
tests. Source identity comes from the existing release evidence cited there;
rebuilt tags are not substituted. The runtime is Windows Python 3.13.13 with
packaging 26.3, matching the newly declared/pinned prerequisite.

## Completed checks

| Check | Result | Scope |
| --- | --- | --- |
| `tests.contract.test_update_fixtures` | 3 tests passed | Exact artifact identity, disposable Unicode books, partial staging snapshots and explicit offline/private-value transport. |
| `tests.integration.test_update_legacy` | 4 tests passed | Historical writer fence, test-only standalone launcher, hard-stopped directory-only fence and real legacy retrospective OS-lock behavior. |
| Final combined command | 7 tests passed | `.venv/Scripts/python.exe -X utf8 -m unittest tests.contract.test_update_fixtures tests.integration.test_update_legacy -v` on Windows; no skips. |

The final combined run passed after a fixture-method placement error was corrected.
Earlier restricted runs could not create the temporary directories/hard links
required by historical initialization. The passing run used filesystem access
for disposable temporary repositories; no real book or global Git configuration
was changed. Tests make no release-service or GitHub requests.

FUP-001's foundational investigation permits implementing the bounded closed-client
design. Its observed preloaded-client limitation remains explicit; the investigation
does not qualify future updater crash safety. See the detailed gate decision in
`specs/004-update-novel-creator/follow-ups.md`.

## Still unverified

All update protocol/ownership/preview/apply/recovery product behavior, product
interruption tests, authorization-state matrix, package verification of the new
feature, Windows native Codex journey and Linux CLI/native-host behavior remain
unverified. A passing fixture/probe does not mark SC-001-SC-009 passed.

## Maintenance/protocol foundation

- Operational schema, target bundle export and read-only committed-record/retro
  compatibility probe: 4 contract tests passed. Unsupported metadata and early
  ownership confirmation are rejected; no retrospective service is constructed.
- New maintenance tests cover confirmed/unproven ownership, direct-service and
  pre-failure-journal exclusion, legacy bookkeeping lock bridging, and shared
  ordinary/exclusive maintenance access. The final focused run including the
  existing held-writer regression passed 7 tests.
- The first affected storage/install/portable/recovery run executed 77 tests:
  one held-lock test failed in two subcases and two real-symlink tests were
  skipped because Windows privilege 1314 was unavailable. The failure was a new
  empty lease file created before refusing an existing lock. Read-only preflight
  was corrected; that entire held-lock test passed on targeted rerun. The 77-test
  command has not been rerun in full since the correction.
- Retrospective authorization, controls, failure notices, notice reservations,
  preservation and transport mutation regressions: 19 tests passed. Revocation
  remains independent of ordinary in-flight contribution work.
- `pip check` passed. An offline local foundation wheel built successfully and
  `tests/verify_wheel.py` passed exact 35-file identity, isolated package origins,
  English/Icelandic initialization, pinned saves/reopens and name-only setup.
  Its SHA-256 is `4b3b72a01410a85e727e37e758c0c914cfff9c4bff1ac16f7a4f806be45a41c6`.
  This is an unreleased development artifact, not the published 0.2.0 wheel.
- Restricted build attempts failed in sandbox temporary/cache directories; the
  successful offline build/verifier used the same scoped filesystem access as
  the disposable-repository tests. No package was published or installed into a
  global environment.

These results qualify the listed foundation checks only. Updater ownership
classification, release preparation, preview, application/recovery transactions,
their full failure matrix, Linux and native-host delivery remain unverified.

## Read-only preview and status milestone

T010-T016 are implemented for the preview/status delivery boundary. The public
CLI exposes explicit `update` preview and `update status` only; apply/recovery
retry remain unavailable until the real interruption gates in T025-T031 pass.
The original foundation-only statements above describe their earlier checkpoint.

- Release, CLI/status and protocol run: 15 tests passed on Windows Python 3.13.13.
  This includes actual forced private installation over a different-byte,
  noneditable inherited package with the same version, pre/post origin/inventory
  verification, immutable-record probing, modified-product refusal, omitted-export
  refusal, malformed archives/prerequisites, and read-only status observations.
- Preview integration run: 6 tests passed. Exact published 0.1.0 and 0.2.0 source
  wheels were inspected against disposable installed books; controlled unpublished
  0.3.0 target wheels exercised preparation and schema probes. Book snapshots,
  custom instructions and partial unrelated staging were preserved. A distinct
  selected interpreter was propagated and bound; concurrent book mutation refused
  the preview. Cache-inside-book and modified-exclusive-resource cases refused.
- Maintenance regression after canonical grant selection and raw machine-grant
  digest binding: 6 tests passed.
- One initial CLI test fixture lacked its journal parent directory; fixed the
  fixture and reran the entire release/CLI/protocol group successfully.

No public target release, actual update transaction, recovery retry, Linux or
native Codex journey has been qualified by these results. The interpreter binding
is verified through preparation/preview; application/recovery enforcement and
operation-aware CLI errors remain T021-T031 responsibilities.
