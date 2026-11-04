# Tasks: Update Novel Creator in Existing Books

**Input**: Design documents in `specs/004-update-novel-creator/`.

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/update-cli.md`, `contracts/maintenance-protocol.md`, `quickstart.md`, `follow-ups.md`.

**Tests**: Required by FR-017, SC-001-SC-009 and the constitution. Write the listed assertions before their implementation, observe the expected failures, then implement and run relevant checks. All task boxes start unchecked; this document is not implementation evidence.

**Organization**: Shared setup/foundation, four user-story phases in specification priority order, then cross-cutting qualification. Paths below are repository-relative. `[P]` identifies different-file work that may run concurrently only after its stated prerequisites; it is not authorization to bypass review or launch agents.

## Phase 1: Setup (Shared Infrastructure)

**Goal**: Establish deterministic synthetic evidence and packaging prerequisites without changing a real book.

- [X] T001 Build historical 0.1.0/0.2.0 book fixtures and before/after byte, semantic-index, grant/notice snapshots in `tests/update_helpers.py`; require explicit verified wheel inputs and record SHA-256 rather than treating rebuilt tags as published artifacts (FR-013, FR-017; SC-003, SC-006).
- [X] T002 [P] Add fake public-release transport, hostile archive variants and subprocess durable-fault acknowledgements in `tests/update_release_helpers.py`; deny real outgoing traffic and seed private story/path/credential values for request assertions (FR-015; SC-008).
- [X] T003 Declare `packaging>=24` in `pyproject.toml` and refresh its pinned/transitive entries in `requirements-lock.txt` using the existing lock-file convention; retain Python >=3.11, Git >=2.39 and current validator constraints (FR-008).

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Establish metadata, guarded maintenance and isolated probes before exposing update mutation.

- [X] T004 Investigate FUP-001 using actual 0.1.0/0.2.0 subprocesses and isolated test-only maintenance/launcher probes in `tests/integration/test_update_legacy.py`, recording supported closed-client/fresh-launch behavior, live contention and unsupported preloaded clients in `specs/004-update-novel-creator/follow-ups.md`; resolve or explicitly block the design before any maintenance or transaction implementation, without calling documentary fixes runtime qualification (depends on T001, T002; FR-009-FR-010, FR-013; SC-004-SC-006).
- [X] T005 Add strict operational document validation in `schemas/v1/update.schema.json`: `document_version: 1`, UUID IDs, action `add`/`replace`/`remove`, explicit null old/new for absence, canonical safe paths and states `prepared`, `fenced`, `replacing`, `candidate_published`, `verifying`, `complete`; require `ownership_confirmed: true` only in fenced-or-later checkpoints and false while prepared, preserve story schema `1.0` and reject duplicate keys/unknown versions (FR-005, FR-010-FR-011).
- [X] T006 [P] Add failing metadata/export/probe tests in `tests/contract/test_update_protocol.py` covering protocol integer 1, inventory-wheel agreement, incompatible record/retro documents, no story repair, no transcript cache and no notice/grant mutation APIs (FR-008, FR-014, FR-015).
- [X] T007 Package `src/novel_creator/update-release.json` and export the versioned target inventory through `src/novel_creator/install.py` with matching `pyproject.toml` package-data rules; implement the controlled export/read-only probe boundary in `src/novel_creator/update_release.py` without arbitrary commands or novel-controlled interpreter discovery (depends on T003, T005, T006; FR-008, FR-013).
- [X] T008 Add nonblocking maintenance coordination, durable-active-state validation and updater-owned fence tokens in `src/novel_creator/maintenance.py`; implement confirmed durable ownership before any installed-file/index/ref mutation, return `ownership_unproven` with exit 6 and preserve ambiguous directories/journals, use the exact legacy lock order and never touch disabled/unbound external checkouts (depends on T004's foundational investigation gate; FR-009-FR-011, FR-014).
- [X] T009 Guard CLI dispatch before mutable imports/error journaling and direct service mutation routes in `src/novel_creator/cli.py`, `storage.py`, `install.py`, `context.py` and `retro.py`; distinguish local read-only status from notice rendering/reconciliation and retain existing command error contracts (depends on T008; FR-009, FR-010, FR-014, FR-016).

**Checkpoint**: Protocol/guard contract tests pass; no update apply route is exposed. Mutation-phase tests may start only after these foundations exist.

## Phase 3: User Story 1 - Check and Preview (Priority: P1, MVP)

**Goal**: Give the writer an accurate explicit release preview without modifying the book.

**Independent Test**: A real disposable recognized book plus fake release listings yields exact version/change/blocker results while before/after book files, index, HEAD and retrospective state are identical.

- [X] T010 [P] [US1] Add release-selection/integrity tests in `tests/contract/test_update_release.py`: latest/exact stable, already-current/unavailable, invalid selection/artifact/protocol/prerequisites and network/hash/identity/path/redirect failures; include a non-editable same-version inherited product with different bytes, require a new verified private installation with matching module/resource hashes and origins, preserve the inherited package and reject external origins/modified resources before book mutation (FR-001-FR-003, FR-008; SC-001).
- [X] T011 [P] [US1] Add preview/privacy tests in `tests/integration/test_update_preview.py`: external-only cache, unchanged book snapshots, full worktree/index/operational fingerprint, private request seeds and unchanged global package/Git settings (FR-003, FR-015; SC-001, SC-008).
- [X] T012 [P] [US1] Add preview/default/status contract tests in `tests/contract/test_update_cli.py`; exercise every read-only status observation using synthetic journals/refs with no directory creation or network, and distinct controller/`--python` interpreters through preparation/probes, returned `runtime_python` and apply/recovery binding; cover no automatic calls, no source/custom-index/force flags and no operation IDs in `pending_exchange_id` (FR-001-FR-003, FR-008, FR-010, FR-012, FR-016).
- [X] T013 [US1] Implement fixed public PyPI resolution/download and verified-wheel preparation in `src/novel_creator/update_release.py`; enforce `novel-creator`, exact archive SHA-256, stable selection, selected-interpreter prerequisites, `-I -B` children and private-venv pip `--ignore-installed --no-index --no-deps --no-compile` with `PIP_CONFIG_FILE=os.devnull`; verify private product origins and wheel-exact module/resource inventory before/after probes, rejecting inherited fallback without changing the configured interpreter's packages (depends on T010; FR-002, FR-008, FR-015).
- [X] T014 [US1] Implement `preview(novel, *, version=None, python=None, transport=None)` and `status(novel, *, operation_id=None)` in `src/novel_creator/update.py` before CLI exposure: propagate/pin the selected interpreter and verified private origin, classify legacy/exclusive/shared ownership, preserve custom bytes, validate additions/removals/collisions and refuse staged affected shared files; bind the external preview to exact branch/HEAD/file/index/operational state and implement local no-operation/pending/published-cleanup/conflict/complete observations from journals/refs without writes or network (depends on T011, T012, T013; FR-003-FR-005, FR-008, FR-010, FR-012).
- [X] T015 [US1] Expose check/preview and read-only status output in `src/novel_creator/cli.py` according to `contracts/update-cli.md`; provide exact target/hash/IDs/runtime interpreter, blockers and next action, while leaving application unavailable until US3's safety checkpoint (depends on T012, T013, T014; FR-001-FR-003, FR-016).
- [X] T016 [US1] Run T010, T011, T012 tests and document preview-only validation commands and actual limitations in `workflows/getting-started.md`; do not advertise an unimplemented apply command (FR-016, FR-017; SC-001, SC-008).

**Checkpoint**: US1 is the independently usable read-only MVP. No publication or real-book update is authorized by completing it.

## Phase 4: User Story 2 - Apply the Reviewed Update (Priority: P1)

**Goal**: Implement the internal success-path transaction with exact ownership, checkpoint and staging preservation. Public apply remains gated on US3.

**Independent Test**: Construct a valid preview in a disposable book and call the internal controller; verify one framework-only child commit, unchanged manuscript/exchanges/grants and identical unrelated staging.

- [X] T017 [P] [US2] Add transaction preservation tests in `tests/integration/test_update_apply.py`: exact selected artifact/parent, stale preview refusal, custom instructions, shared-rule additions, unchanged exclusive-resource removal, path collisions, partially staged unrelated work, changed index and idempotent second apply (FR-004-FR-007; SC-002-SC-004).
- [X] T018 [P] [US2] Add removed-path index merge regressions to `tests/integration/test_storage.py`; prove zero-mode deletions and affected-baseline checks preserve the latest unrelated index entries and existing story-save behavior (FR-007; SC-003).
- [X] T019 [US2] Implement format-2 `ownership.exclusive`/`ownership.shared` metadata in `src/novel_creator/install.py` and `update.py`; `checksums`/`managed_paths` cover exclusive resources, shared roles are `instructions`, `ignore_rules`, `attributes`, and continuation no longer treats legitimate shared custom edits as exclusive corruption (FR-005, FR-006).
- [X] T020 [US2] Factor replacement-aware worktree/index comparisons and deletion-capable `sync_index()` in `src/novel_creator/storage.py`; do not reuse new-exchange-only `check_managed()` for replacements or change ordinary save semantics (depends on T018; FR-005, FR-007).
- [X] T021 [US2] Implement durable prepared journal, private old/new resource blobs, exact candidate tree/commit and expected-before path actions in `src/novel_creator/update.py`; journals live below `local/update/`, never legacy `local/*.json`, and contain no copied story transcript (depends on T017, T019, T020; FR-006, FR-010, FR-015).
- [X] T022 [US2] Implement fenced replacement and conditional `update-ref` publication in `src/novel_creator/update.py`; persist intent before mutation, install the standalone maintenance launcher first, permit only that journaled temporary launcher exception and publish only the exact candidate with reviewed parent (depends on T008, T009, T021; FR-004, FR-006-FR-010).
- [X] T023 [US2] Implement index synchronization, target read-only verification, final-launcher restoration, durable completion and owned-fence cleanup in `src/novel_creator/update.py`; return `ready` only with released fences and no cleanup, never create a production smoke exchange or use stash/reset/amend/push (depends on T022; FR-007, FR-012).
- [X] T024 [US2] Run success-path/storage/continuation regressions and add custom-shared-file format-2 assertions in `tests/integration/test_install.py`; verify unchanged book identity/story bytes and no duplicate update commit (depends on T019, T020, T021, T022, T023; SC-002, SC-003).

**Checkpoint**: Internal success path is testable, but do not expose or qualify public apply until US3's crash/conflict/legacy gates pass.

## Phase 5: User Story 3 - Block Conflicts and Recover (Priority: P1)

**Goal**: Make failures inspectable and retries exact, including old-book clients and post-publication cleanup.

**Independent Test**: Kill real subprocesses after acknowledged durable transitions, inspect state without mutation/network, explicitly recover the recorded operation and verify preserved evidence, blocked mixed-runtime launches and at most one update commit.

- [X] T025 [P] [US3] Add real hard-interruption recovery tests in `tests/integration/test_update_recovery.py` before owner-file publication/flush and confirmed journal checkpoint, then launcher swap, each replacement/removal, ref publication, index sync, verification, completion and fence release; assert `ownership_unproven` preserves locks with no installed-file/index/HEAD changes, while proven ownership enables exact retry; distinguish hard death from in-process exceptions (FR-010-FR-012; SC-004-SC-005).
- [X] T026 [P] [US3] Extend `tests/contract/test_update_protocol.py` with read-only status/recovery, token/owner/death/PID-reuse checks, changed journal/artifacts/files/index/HEAD conflicts and no implicit network/rollback/lock theft; use the defined exit/state contract for published-but-unverified results (FR-009-FR-012).
- [X] T027 [US3] Implement inspect-only `recover()` in `src/novel_creator/update.py` by reusing T014's existing read-only status/evidence inspector; add retry-eligibility, actual parent/candidate ref, ownership and artifact checks without changing or duplicating status semantics, and exercise it against T025's real interruption states (depends on T014, T025, T026; FR-010-FR-012).
- [X] T028 [US3] Implement explicit `recover(..., retry=True, expected_head=...)` in `src/novel_creator/update.py`; resume only the recorded candidate/artifacts and positively owned dead-holder fence, preserve unexpected evidence, reconcile complete-but-fence-held state and never replay story decisions or duplicate commits (depends on T027; FR-007, FR-011-FR-012).
- [X] T029 [US3] Harden the legacy lock bridge and standalone launcher in `src/novel_creator/maintenance.py` and `install.py` from T004 results; enforce quiescence confirmation without bypassing held locks, retain the persistent fence after failure and keep arbitrary preloaded-client crash behavior an explicit qualification limit (FR-009-FR-010).
- [X] T030 [US3] Expose public apply/recovery argument validation and operation-aware errors in `src/novel_creator/cli.py` only after T025, T004, T026, T027, T028, T029 pass; enforce exact preview/version/HEAD, required legacy confirmation and offline read-only inspection, without routing maintenance refusals through retrospective failure journaling (FR-004, FR-009-FR-012, FR-016).
- [X] T031 [US3] Re-run legacy/recovery/apply tests and update `specs/004-update-novel-creator/follow-ups.md` with FUP-001's supported-boundary evidence or explicit blocker; do not close it from a mocked or exception-only test (depends on T004, T028, T029, T030; FR-009-FR-012, FR-017; SC-004-SC-005).

**Checkpoint**: Public apply is usable only within the demonstrated supported bootstrap boundary. An unresolved contradiction between that boundary and the specification blocks qualification, not an excuse to mark requirements passed.

## Phase 6: User Story 4 - Continue Older Books and Preserve Controls (Priority: P2)

**Goal**: Deliver old-book onboarding, host instructions and the full retrospective/portable runtime compatibility journey.

**Independent Test**: Both historical origins update to a controlled newer wheel and can inspect/resume/save through the isolated pinned launcher; 0.2.0 disabled/enabled/revoked/interrupted states retain their exact meaning and bytes.

- [X] T032 [P] [US4] Add grant/run/notice preservation and exclusion tests in `tests/integration/test_update_retro_preservation.py`; cover absent/disabled/revoked/generation-mismatched/enabled grants, unreserved queued notices, reserved notices, nonterminal/terminal-owner cleanup, unknown schemas and uncertain publication; assert no contributor API calls or disabled external checkout access (FR-009, FR-014; SC-007).
- [X] T033 [P] [US4] Extend `tests/integration/test_portable_install.py` for both historical-origin updated books, Unicode paths and English/Icelandic data; assert isolated product imports, restored session/context and a subsequent synthetic save without rewriting existing exchanges (FR-006, FR-013, FR-017; SC-003, SC-006, SC-009).
- [X] T034 [US4] Complete target-compatible retrospective snapshot checks and after-apply byte verification in `src/novel_creator/update.py`/`maintenance.py`; preserve machine grants, run evidence, notice reservations and revocation meanings while refusing incompatible unfinished work rather than enable/disable/resume/release/consume it (depends on T032; FR-014, FR-015).
- [X] T035 [US4] Add `workflows/update.md` and `adapters/codex/skills/novel-update/SKILL.md`, and integrate explicit discovery/reload guidance in `workflows/entry.md`, `adapters/codex/AGENTS.fragment.md` and `AGENTS.production.md`; require reviewed application, external recovery and no automatic retrospective trigger or unsaved creative-response suffix (depends on T030, T034; FR-013, FR-014, FR-016).
- [X] T036 [US4] Add English/Icelandic operational copy in `languages/en.md` and `languages/is.md` and writer bootstrap/check/apply/recovery examples in `workflows/getting-started.md` and `README.md`; use the returned runtime interpreter, retain manuscript/interaction-language independence and distinguish package install from book update (depends on T035; FR-013, FR-016).
- [X] T037 [US4] Implement `tests/verify_update.py` with repeatable `--source-wheel`, `--target-wheel`, `--json` and a private fake transport; extend `tests/verify_wheel.py` inventory/protocol/isolated update coverage and record actual historical wheel identities (depends on T033, T034, T035, T036; FR-013, FR-017; SC-006, SC-009).

**Checkpoint**: Old-book and retrospective preservation journeys pass in disposable environments. Native-host and cross-platform evidence are still required before claiming those capabilities qualified.

## Phase 7: Polish and Cross-Cutting Qualification

- [X] T038 [P] Add adversarial transport/environment leak and inherited pip/Git/Python injection assertions to `tests/contract/test_update_release.py`, using all seeded secrets/private paths from `tests/update_release_helpers.py`; verify fixed public HTTPS requests, zero private uploads and no global configuration changes (FR-015; SC-008).
- [X] T039 Execute the Windows/Linux CLI and historical-wheel matrix in `specs/004-update-novel-creator/quickstart.md`, including the full unittest suite, existing storage/retro regressions and distribution verifiers; record per-case outcomes, wheel hashes, interpreter/platform details and unavailable checks in `tests/evaluations/existing-book-update-qualification.md` (depends on T031, T037, T038; FR-017; SC-001-SC-009).
- [X] T040 Run separately scoped actual Codex host acceptance using the user-approved delegated evaluation route and record human preview approval, apply/recovery, custom instructions, actual host discovery/reload and exact save-before-display behavior in `tests/evaluations/existing-book-update-host.md`; retain direct native-user input and Linux Codex as unverified unless actually exercised, with no real contribution/publication side effects (depends on T035, T036, T037, T038, T039; FR-016-FR-017; SC-009).
- [X] T041 Reconcile actual evidence against FR-001-FR-017 and SC-001-SC-009 in `tests/evaluations/existing-book-update-qualification.md`, cross-reference FUP-001, and update `docs/development.md` and `README.md` to distinguish implemented, structurally verified, native-host verified and still-blocked behavior; no release/push/publish authorization is implied (depends on T039, T040).

Acceptance method selected by the user on 2026-11-04: after asking the coordinator
to run the check for them, the user approved the exact preview and the planned
interruption/recovery and delegated-save tests in the coordinating chat. T040
therefore exercises the actual Windows Codex host with explicitly labeled
delegated evaluation input. This replaces the originally planned manual typing
route for this execution; it does not claim the direct native-user input gate,
Linux host, human ratings or real publication passed. Human maintenance approval
still binds the concrete preview; source labels and saved-response checks remain.

## Dependencies and Execution Order

- Setup: T001, T002, T003. T001 and T002 are independent files; dependency changes in T003 do not authorize unrelated upgrades.
- Foundations: T004's historical-client investigation runs first after setup and blocks maintenance/transaction implementation until its supported lifecycle is demonstrated or a design blocker resolved. Then T005, T006, T007, T008, T009 complete; T005/T006 may proceed concurrently, T007 consumes both and T009 consumes T008. All finish before dependent story work.
- US1: T010, T011, T012 may run concurrently, then T013 -> T014 (both preview and local status) -> T015 (CLI exposure) -> T016. Preview/status-only MVP may stop here; all status states are covered by synthetic journals/refs before exposure.
- US2 consumes US1 previews and foundations. T017/T018 are independent tests. T019/T020 precede T021 -> T022 -> T023 -> T024. Successful internal apply is not a shippable mutation workflow until US3 is complete.
- US3 consumes the US2 journal/transaction, the foundational T004 investigation and US1's T014 status inspector. T025/T026 are independent test files after the transaction exists; T027 adds recovery inspection using that existing inspector, then T028, with T029 using T004 evidence; both precede T030 -> T031. Complete safety before exposing public application.
- US4 tests T032/T033 can be authored independently once fixtures exist; integration implementation follows US3. T034 -> T035 -> T036 -> T037. This story is tested against prepared historical books, not a requirement to recreate a book.
- Final qualification: T038 may run after release code stabilizes; T039 -> T040 -> T041 completes evidence review. Failed/unavailable mandatory evidence blocks the corresponding readiness claim.

### Parallel Examples

| Story | Safe parallel work after prerequisites |
| --- | --- |
| US1 | T010 release tests, T011 preview tests, T012 CLI tests use separate files. |
| US2 | T017 apply-preservation tests and T018 existing index regressions. |
| US3 | T025 hard-crash tests and T026 protocol/inspection tests; legacy investigation is an earlier foundational gate. |
| US4 | T032 retrospective state matrix and T033 isolated portable-runtime tests. |

Do not parallelize edits to shared `update.py`, `cli.py`, `install.py` or `maintenance.py`. References to future tests/artifacts are implementation destinations, not existing passing evidence.

## Requirement Coverage

| Requirement / outcome | Tasks |
| --- | --- |
| FR-001 | T010, T012, T015, T016 |
| FR-002 | T010, T013, T015 |
| FR-003 | T010, T011, T012, T013, T014, T015, T016 |
| FR-004 | T014, T017, T022, T030 |
| FR-005 | T005, T014, T017, T019, T020, T021, T022 |
| FR-006 | T019, T021, T022, T023, T024, T033 |
| FR-007 | T017, T018, T020, T021, T022, T023, T024, T028 |
| FR-008 | T003, T006, T007, T010, T012, T013, T014 |
| FR-009 | T008, T009, T022, T004, T026, T029, T030, T031, T032 |
| FR-010 | T004, T005, T009, T012, T014, T021, T022, T025, T027, T029, T030, T031 |
| FR-011 | T005, T008, T025, T026, T027, T028, T030, T031 |
| FR-012 | T012, T014, T023, T025, T026, T027, T028, T030, T031 |
| FR-013 | T001, T007, T004, T033, T035, T036, T037 |
| FR-014 | T006, T008, T009, T032, T034, T035 |
| FR-015 | T002, T006, T011, T013, T021, T034, T038 |
| FR-016 | T009, T012, T015, T016, T030, T035, T036, T040 |
| FR-017 | T001, T016, T031, T033, T037, T039, T040, T041 |
| SC-001 | T010, T011, T012, T013, T014, T015, T016, T039 |
| SC-002 | T017, T021, T022, T023, T024, T025, T028, T039 |
| SC-003 | T001, T017, T018, T019, T020, T021, T022, T023, T024, T033, T039 |
| SC-004 | T017, T025, T004, T026, T027, T028, T029, T030, T031, T039 |
| SC-005 | T025, T004, T026, T027, T028, T029, T030, T031, T039 |
| SC-006 | T001, T004, T033, T037, T039 |
| SC-007 | T032, T034, T039 |
| SC-008 | T002, T011, T013, T038, T039 |
| SC-009 | T033, T037, T039, T040, T041 |

## Implementation Strategy

Deliver read-only US1 first. Add internal transaction behavior, then complete interruption/recovery exclusion before making public apply available. Integrate historical onboarding/host behavior and run full qualification last. Stop for contradictory safety requirements or unresolved FUP-001 evidence rather than weakening preservation guarantees. Task completion is recorded in the checkboxes above. Task generation itself performed no implementation; subsequent verified work is recorded in tests/evaluations/existing-book-update-qualification.md. No real-book update or release/publication is authorized by these checkboxes.

No `.specify/extensions.yml` hooks were configured during generation or implementation. Preimplementation analysis was completed; use the checkboxes and qualification ledger for current implementation/evidence status.
