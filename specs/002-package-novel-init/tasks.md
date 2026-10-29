# Tasks: Package Installation and Simple Novel Initialization

**Input**: Design documents in `specs/002-package-novel-init/`: [spec](spec.md), [plan](plan.md), [research](research.md), [data model](data-model.md), [CLI contract](contracts/cli.md), [distribution/documentation contract](contracts/distribution-and-docs.md), and [validation guide](quickstart.md).

**Prerequisites**: Constitution 1.0.0; existing Python/Git initializer and test infrastructure. Execute from repository root using the session shell. Paths below are repository-relative. Feature 001 final functional qualification remains historical evidence; do not reopen retired latency or novice/manual gates.

**Tests**: Included because the specification explicitly requires automated acceptance matrices and guide verification. Add behavior/regression tests before the corresponding implementation; observe a relevant failure, then make them pass. Existing safeguards should already pass and must stay passing. Do not write tests that merely mirror helpers.

**Format**: `- [ ] TNNN [P?] [USn?] Description with exact file paths`. `[P]` means independent files/work after the stated prerequisites, not permission to run dependent operations concurrently. Story numbers match the spec; phase order follows priority: US1, US3, US4 (P1), then US2 (P2). All tasks start unchecked.

## Phase 1: Setup — Existing State and Release Prerequisites

**Purpose**: Establish traceable scope without changing runtime code or external accounts.

- [X] T001 Record current source revision, dirty changes, active feature, checklist status, existing test entry points and feature-001 final task/ledger disposition in `specs/002-package-novel-init/implementation-ledger.md`; create an FR-001–FR-018/SC-001–SC-008 evidence index and preserve all existing work and historical limits.
- [X] T002 [P] Perform read-only release preflight and record actual PyPI name/version visibility, available evidence of maintainer control, absent licensing decisions and publisher prerequisites in `specs/002-package-novel-init/release-preflight.md`; inspect `pyproject.toml` and existing license files, do not infer ownership from an absent listing, choose a license, reserve names, create accounts or publish. Unavailable external prerequisites block T031/T036–T039 as applicable, not local implementation.

## Phase 2: Foundational — Compatibility, Version and Installation Harness

**Purpose**: Shared foundations required before story implementation. Depends on Phase 1 assessment, not on obtaining external account access.

- [X] T003 Capture existing legacy init JSON with/without `--json`, exit categories, raw brief provenance, defaults and safe empty-unborn-repository/metadata allowances in `tests/contract/test_cli.py` and `tests/contract/test_initialize.py`; retain baseline cases for recognized projects and cleanup-required success, without freezing incidental IDs/timestamps.
- [X] T004 Establish one offline-readable release version source in `src/novel_creator/__init__.py`, `pyproject.toml` and `src/novel_creator/install.py` for distribution metadata, future `--version` and newly generated manifest bundle_version; keep “Schema version is independent” and “Never rewrite old novel manifests during a package upgrade.” Verify source/wheel/novel-local version availability without installed-distribution metadata dependence.
- [X] T005 Create a reusable installed-package acceptance harness in `tests/verify_package_install.py` supporting explicit candidate-wheel and published-name/version modes, clean user-owned venvs, subprocess argument arrays, external disposable novel roots, dependency/version/hash evidence and explicit failure/skips; do not inherit checkout imports, PYTHONPATH or dependency site directories, change global configuration, run a provider, or publish.

**Checkpoint**: Legacy behavior is characterized; version source and clean-install harness are available. Stories may now extend the same initializer safely.

## Phase 3: User Story 1 — Install and Start a Novel (P1, Local MVP)

**Goal**: One name-only command creates an independent novel and gives an explicit runtime/Codex handoff.

**Independent Test**: Install a candidate in a clean environment outside the checkout, run name-only init, validate/read the pinned novel, and invoke its installed setup entry with the printed interpreter. Public named installation is independently tested after publication in T038/T039; local success does not complete FR-001 or SC-001.

### Tests

- [X] T006 [P] [US1] Add command contract cases in `tests/contract/test_simple_init_cli.py` for positional NAME, legacy mode exclusivity, default cwd/NAME target, help/version no-write behavior, duplicate/unknown arguments, UTF-8 readable shorthand output versus one-envelope JSON, and unchanged legacy output; quote the model constraint “nonempty, non-whitespace single filesystem component, not . or .., without slash/backslash, NUL, control characters or platform-invalid spelling” in validation coverage.
- [X] T007 [P] [US1] Add disposable name-only/bootstrap and separate-interpreter integration cases in `tests/integration/test_simple_initialize.py` proving title-from-name, default en, unknown remaining choices, independent Git root, no provider/network during init, complete resources, and novel-local module imports without the framework checkout.

### Implementation

- [X] T008 [US1] Implement the name-only parser path and pre-write mode/name validation in `src/novel_creator/cli.py`, preserving the legacy path/brief route; normalize title-from-NAME and deterministic UTF-8 effective brief, with “title is explicit title or NAME; include manuscript_language only when explicitly supplied” as the final normalization contract (optional values are enabled in T028); add `--version` from T004.
- [X] T009 [US1] Extend bootstrap/initialization in `src/novel_creator/install.py` to accept optional shorthand request evidence, append the second existing-schema artifact with “request_type: cli_init_v1”, name/resolved_destination/title_argument/language_argument and “absent arguments are null”; preserve the first brief artifact and project JSON-pointer sources, deterministic text/SHA-256 digest, “No database or story-schema migration”, and saved original bundle identity. Do not add arbitrary fields to `novel_project` or pretend parsed arguments preserve shell keystrokes.
- [X] T010 [US1] Add shorthand result/rendering in `src/novel_creator/cli.py` using confirmed initializer outcomes: output-only data.novel_path/runtime_python/launcher_path/getting_started_path/ready, exact sys.executable, Codex `$novel-init` next action and UTF-8 diagnostics; enforce “ready requires a confirmed bootstrap, verified required resources, and no cleanup requirement.” Preserve “Saved-but-cleanup-required remains exit 0 with ready false” and legacy rendering/exit categories.
- [X] T011 [US1] Add an initial install/name-only/runtime-handoff section in `workflows/getting-started.md`, shipped through existing resources in `src/novel_creator/install.py` and `pyproject.toml`; document the external venv and exact interpreter before `$novel-init`, unknown creative choices and no API key. Mark unverified publication honestly; US4 expands this same canonical file, not a duplicate guide.
- [X] T012 [US1] Extend `tests/verify_wheel.py` to check name-only console invocation, release version, request artifact, guide/resource bytes and pinned launcher outside checkout while retaining all legacy/source-identity checks; keep its inherited-dependency mode labeled separately from the clean harness in T005.
- [X] T013 [US1] Run the US1 contracts/integration cases and candidate installed-package checks, recording version/source/resource hashes, actual outcomes and unavailable platforms in `tests/evaluations/package-init-us1.md`; do not report public installation, host operation or readiness from structural evidence alone.

**Checkpoint**: Demonstrable local MVP: name-only setup plus installed resources and runtime guidance. Not a public feature-release completion claim.

## Phase 4: User Story 3 — Preserve Existing Work and Recover Safely (P1)

**Goal**: Shorter syntax retains safe recognition, original-input retries, transaction identity and legacy behavior.

**Independent Test**: Snapshot disposable existing content/history, exercise repeat/conflict/fault/retry/access/concurrency cases, then compare preserved bytes, identities, checkpoints and diagnostics.

### Tests

- [X] T014 [P] [US3] Add baseline name-only fault/retry cases in `tests/integration/test_simple_init_recovery.py` for unchanged request, presentation-only changes, equivalent resolved default targets, changed files/evidence, cross-mode legacy retry and concurrent reservation; assert “reuse the saved bundle”, same IDs/resources and exactly one bootstrap. Do not add optional-setting cases here: T027 adds those tests before T028 implements the flags.
- [X] T015 [P] [US3] Extend `tests/integration/test_install.py` with same-name shorthand recognized-novel unchanged settings/history/resources, occupied/nested/alias/root guards, missing Git/identity/access, held-lock and published-cleanup cases; retain legacy allowed metadata/unborn targets and verify no global settings, unrelated instructions, manuscript or remote changes. Replacement-option cases belong to T027 after the baseline slice.

### Implementation

- [X] T016 [US3] Bind partial shorthand retry to the canonical request plus brief in `src/novel_creator/install.py`, retain immutable setup reservation and original transaction, reject changed NAME/settings even when effective brief matches, and leave “Legacy partial state without request artifact” on unchanged legacy retry only; preserve recognized-novel checksum verification/continuation and all storage/root/index/reparse/lock protections.
- [X] T017 [US3] Refine prerequisite/access/conflict/recovery diagnostics and continuation rendering in `src/novel_creator/cli.py` and `src/novel_creator/install.py`; explain unapplied flags on recognized novels, preserve original receipts/checkpoints and code categories, show recovery rather than ready when cleanup remains, and never configure identity, bypass permissions or delete evidence.
- [X] T018 [US3] Run T003/T014/T015 baseline name-only and legacy cases plus affected existing recovery/path/storage tests; record byte/history snapshots, original IDs, exit/output outcomes, fault boundaries and actual skips in `tests/evaluations/package-init-us3.md`. This baseline gate has no dependency on T028 and must pass without skipping future-feature tests. T027 creates optional-setting recovery cases later; T029 executes them after T028 and extends this evidence for complete FR-010–013/SC-003/004/006 coverage. Do not reopen retired timing targets.

**Checkpoint**: Baseline name-only/legacy safety passes. Optional-setting recovery tests are not yet added and do not block this checkpoint; T027/T028/T029 add, implement and verify that separate slice.

## Phase 5: User Story 4 — Follow a Complete Getting-Started Guide (P1)

**Goal**: Writers can discover one guide and reach a first saved exchange, inspect state, and return later.

**Independent Test**: Start at README/help/completion in each supported environment, use only guide/linked references through first save and resumption in a fresh Codex project, and check the six troubleshooting categories. Optional-setting walkthroughs finalize after US2.

### Tests

- [X] T019 [US4] Add documentation/discovery contract cases in `tests/contract/test_getting_started.py` for canonical packaged/installed guide identity, working README/help/completion routes, shell-labeled minimal steps and expected results, separate optional reference, no-idea sample, six troubleshooting categories, and no required screenshots/API keys/developer checkout; include a pre-feature bundle without a guide, verified package-guide fallback/label, unchanged novel bytes/history/manifest and readiness based on its original resource set, plus missing-fallback diagnostics. Test observable routes/content rather than exact prose.

### Implementation

- [X] T020 [P] [US4] Expand `workflows/getting-started.md` into the canonical writer guide: Python/Git/Codex/identity prerequisites, safe parent, user-owned venv/pip by-name acquisition, version/help, one init command, correct Codex folder/exact interpreter, sample no-story-idea request, confirmed save, inspect/resume, optional destination/title/en/is with spaces/Unicode, and six safe troubleshooting entries. Explain where commands run, replaceable values, expected output, reactivation/explicit-interpreter alternatives and support limits; do not weaken PowerShell execution policy or claim unverified release availability.
- [X] T021 [P] [US4] Align `workflows/initialize.md`, `workflows/entry.md`, `adapters/codex/AGENTS.production.md` and `adapters/codex/skills/novel-init/SKILL.md` with the printed-interpreter handoff and pinned novel-local launcher; retain legacy brief path, save-before-display, current-input evidence, unknown choices and optional brainstorming. Commit no absolute local runtime paths and do not change old novels.
- [X] T022 [US4] Connect help and shorthand completion to verified guide copies in `src/novel_creator/cli.py` and `src/novel_creator/install.py`: prefer the recognized novel's pinned guide, otherwise label and return the installed-package guide for pre-feature novels without modifying their files/manifest/history. Evaluate their readiness against the original manifest, explain fallback does not upgrade workflows, and report missing fallback resources instead of a nonexistent path. Validate new-novel, old-novel and cleanup-required discovery; preserve legacy output and satisfy T019 after T020/T021.
- [X] T023 [US4] Make `README.md` lead writers to `workflows/getting-started.md`; reconcile `docs/poc-quickstart.md` and `docs/development.md` so contributor/historical instructions stay labeled and do not conflict with the package route. Prepare absolute release-tag documentation URLs for the published README, retaining honest support/evidence limits.
- [X] T024 [US4] Execute guide shell examples and optional/reference/troubleshooting checks using `tests/verify_package_install.py` on Windows PowerShell and Linux Bash, recording actual commands/results and unavailable cases in separate `tests/evaluations/package-init-guide-windows.md` and `tests/evaluations/package-init-guide-linux.md`; defer optional flag execution until T028, not the guide's writing. Verify all three discovery paths and no undocumented steps.
- [X] T025 [US4] Follow the completed guide in actual fresh Codex novel projects with the printed venv interpreter through `$novel-init`, an exact saved first exchange, inspection and `$novel-resume`; record source/bundle/runtime identity, save-before-display/current-input evidence and each supported host/platform outcome in `tests/evaluations/package-init-host-guide.md`. Use disposable novels, distinguish fixtures/agent host evidence/human approval, and leave required unavailable combinations unverified rather than inventing passes; final optional flows depend on T028/T030.

**Checkpoint**: Canonical guide, adapters and discovery are implemented. Documentation completion still requires the full Windows/Linux and actual-host evidence, including optional forms once US2 is implemented.

## Phase 6: User Story 2 — Supply Optional Setup Choices (P2)

**Goal**: Select destination, title and manuscript language while preserving exact supplied input and unknowns.

**Independent Test**: Initialize disposable default/optional novels; compare saved settings/request artifacts against supplied en/is and Unicode values, then verify invalid forms make no writes.

### Tests

- [X] T026 [P] [US2] Extend `tests/contract/test_simple_init_cli.py` for `--path`, `--title`, `--language en|is`, full-target rather than parent semantics, explicit/omitted defaults, duplicate/mixed/unsupported flags, empty title, and no-separator usage; enforce the model constraints “language_argument (optional en/is)”, “--path is the complete destination, not a parent to append NAME to” and preserve invalid-input no-write behavior.
- [X] T027 [P] [US2] Extend `tests/contract/test_initialize.py` with optional-setting artifact/source assertions: “title is explicit title or NAME; include manuscript_language only when explicitly supplied”, “absent arguments are null”, distinct NAME/title, exact Icelandic/spaces, unknown other preferences, no invented messages/canon, unchanged original_concept and explicit-en versus default provenance. Add optional recovery/continuation tests in `tests/integration/test_simple_init_recovery.py` for changed NAME with same explicit title, explicit-en versus omitted language, equivalent reordered option inputs/resolved explicit destinations and ignored replacement options on recognized novels. These tests are introduced here, must expose the missing flag behavior, and are made passing by T028/T029, never required by T018.

### Implementation

- [X] T028 [US2] Enable optional destination/title/language parsing and normalization in `src/novel_creator/cli.py` using T009/T016 request serialization, exact supplied strings and existing English/unknown defaults; preserve “presentation (human/json; excluded from authoritative setup identity)” and existing legacy modes. Integrate any necessary request handling in `src/novel_creator/install.py` without schema or creative-authority changes.
- [X] T029 [US2] Reconcile optional forms, defaults, shell quoting and failure examples in `workflows/getting-started.md` with T028 and `specs/002-package-novel-init/contracts/cli.md`; run T026/T027 plus the T014/T015 baseline regressions after T028. Extend `tests/evaluations/package-init-us3.md` with optional recovery/continuation outcomes and separate baseline/optional checkpoints, confirming no skipped future-feature cases were used to pass T018.
- [X] T030 [US2] Execute the default/destination/separate-title/en/is/spaces/Unicode acceptance matrix using `tests/verify_package_install.py`; record exact settings/artifact/source and refusal outcomes in `tests/evaluations/package-init-us2.md`, completing SC-002 and releasing the optional-example dependencies of T024/T025.

**Checkpoint**: All four stories can now be fully validated against one candidate. US1/US3 baseline tests and US4 guide evidence must remain consistent after optional flags.

## Phase 7: Polish, Release and Cross-Cutting Verification

**Purpose**: Produce a reviewable release candidate, then publish and prove named installation. Tasks below are later implementation/release actions, not actions performed by task generation.

- [ ] T031 Finalize next unused version, distribution-name control and accurate metadata/project/readme URLs in `pyproject.toml`, version source in `src/novel_creator/__init__.py`, and `specs/002-package-novel-init/release-preflight.md`; retain model constraint “requires_python (>=3.11)” and existing `jsonschema>=4.23,<5`/`jsonschema-rs>=0.59,<0.60` dependency bounds. Apply only maintainer-approved licensing to `LICENSE`/metadata if required, never invent a license. If name/version/license decisions are unavailable, record the exact external dependency and keep release steps unchecked while finishing unaffected local work.
- [X] T032 Implement `.github/workflows/package-release.yml` with distinct manual `candidate`/`publish` modes: candidate builds once from an immutable source commit and uploads wheel/sdist plus manifest as one immutable artifact identified by repository/run ID/run attempt/artifact ID. Candidate jobs and host checks bind their evidence to it. Publish mode accepts that identity, downloads and verifies manifest fields/file hashes and all required evidence, then uploads without a build step; fail closed on changed/missing/expired artifacts or mismatched evidence. Include protected/scoped OIDC publishing and post-publish checks; pin actions, forbid push/PR publishing, and validate identity/hash rejection paths without publishing.
- [X] T033 Run final suites/metadata checks, then, once repository workflow availability and candidate dispatch are explicitly authorized, execute only the workflow's `candidate` mode and retrieve its immutable artifact. Record repository/run ID/run attempt/artifact ID/source commit/distribution/version/filenames/SHA-256 in `tests/evaluations/package-init-release-manifest.json`. Run the exact-source wheel verifier and separate clean sdist rebuild/install checks against these stored inputs, recording outcomes in `tests/evaluations/package-init-candidate.md`; rebuilt test wheels never replace release bytes. T034/T035 and final T024/T025 evidence must consume/bind to this artifact. Local development builds alone cannot complete this task; unavailable repository dispatch leaves the gate open while unaffected local work continues.
- [X] T034 [P] Execute final clean Windows candidate/dependency/runtime/guide acceptance using `tests/verify_package_install.py` and [quickstart.md](quickstart.md), recording exact interpreter/dependency and artifact/source identities in `tests/evaluations/package-init-candidate-windows.md`; no inherited checkout/site packages or unverified host claims. Depends on T033 and completion of all stories.
- [X] T035 [P] Execute the same final clean Linux Bash candidate/dependency/runtime/guide acceptance using `tests/verify_package_install.py` and [quickstart.md](quickstart.md), recording filesystem/WSL status, versions, hashes and skips in `tests/evaluations/package-init-candidate-linux.md`; retain independently labeled host evidence. Depends on T033 and completion of all stories.
- [X] T036 After verified candidate evidence and explicit maintainer authorization for external release setup, configure the PyPI/GitHub trusted publisher and protected release environment matching `.github/workflows/package-release.yml`; record nonsecret repository/workflow/environment identity and authorization evidence in `specs/002-package-novel-init/release-preflight.md`. Do not request/paste/log API secrets, silently create accounts or assume local ownership evidence authorizes account mutation.
- [ ] T037 After T031–T036 and final T024/T025/T030 evidence pass, invoke only the workflow's `publish` mode under explicit maintainer release authorization, selecting T033's exact candidate run/attempt/artifact ID. Download stored wheel/sdist, verify source/distribution/version/file hashes and all candidate-bound evidence, and upload without rebuilding. Missing/expired/mismatched input fails closed and requires a new verified candidate. Record publishing run, production URLs/version/hashes and original candidate identity separately in `tests/evaluations/package-init-release-manifest.json`; never substitute local/staging output or reuse a conflicting version.
- [ ] T038 [P] Verify the exact published package by name on clean Windows using `tests/verify_package_install.py` with production PyPI/no local links or cache; compare public version/metadata/artifact hashes with the release manifest, resolve declared dependencies and repeat new-novel entry/guide discovery in `tests/evaluations/package-init-public-windows.md`. Depends on T037; failure remains a release failure.
- [ ] T039 [P] Verify the same exact published package by name on clean Linux using `tests/verify_package_install.py`, production-only package acquisition and independent evidence in `tests/evaluations/package-init-public-linux.md`; compare hashes/version and repeat new-novel entry/guide discovery without checkout/dependency inheritance. Depends on T037; record unsupported/unavailable cases honestly.
- [ ] T040 Reconcile every FR-001–FR-018/SC-001–SC-008 and constitution boundary against actual candidate/public/docs/host results in `tests/evaluations/package-init-readiness.md` and `specs/002-package-novel-init/implementation-ledger.md`; update current status/limits in `README.md` only from confirmed evidence. Keep missing publication/platform/host gates open, distinguish agent checks from human approval, preserve old evaluation history and withdrawn timing/manual requirements, and mark feature complete only when required evidence exists.

## Dependencies and Execution Order

```text
Phase 1 assessments → Phase 2 foundations → US1 local candidate → US3 safety
                                                           → US4 guide/adapters
                                                           → US2 optional settings
US2 → finish US4 optional examples/host checks
Story code/docs + local checks → release metadata/workflow → immutable candidate artifact
Candidate artifact → final guide/host evidence + Windows/Linux candidate checks
Verified candidate checks + explicit release setup authority → publisher setup
All required candidate/guide/host gates + release authority → publish
Publish → Windows + Linux public named installs → readiness reconciliation
```

Phase headings group ownership by story; the dependency arrows control execution, not an assumption that every task in a phase must be completed before any work in a later phase. In particular, T024/T025 optional-flow completion waits for T028/T030; implement US2 rather than blocking indefinitely at the documentation phase. The baseline US1/US3 slice is independently demonstrable, and each subsequent story has its own acceptance cases. The full feature is intentionally more than that local MVP.

Specific edges: T006/T007 precede T008–T012; T009 precedes T016; baseline T014/T015 precede T016/T017/T018 with no optional-flag dependency. T019 precedes T020/T021, which may proceed together; T022 integrates their results. T026/T027 introduce optional tests before T028; T028 precedes T029/T030 and final T024/T025. T031/T032 require settled story contracts; after authorized workflow availability/dispatch, T033 produces the immutable candidate identity. T034/T035 consume those exact bytes. Final T024/T025 host/guide evidence must identify the same candidate, repeating affected checks if earlier local builds differed. T036 requires candidate passes plus setup authorization; T037 waits for candidate-bound evidence and downloads that artifact without rebuilding. T038/T039 consume the same published release; T040 consumes all gates. Source or release-artifact changes require a new candidate identity and affected verification, never publication under old evidence.

Shared-file writers serialize: CLI tasks T008/T010/T017/T022/T028, installer tasks T009/T016/T017/T022/T028, guide tasks T011/T020/T029, and README tasks T023/T040. Tests modifying the same files in different stories also serialize. `[P]` never overrides these edges. No subagent dispatch is required by this task list.

## Parallel Examples per Story

| Story | Independent work after prerequisites | Integration boundary |
| --- | --- | --- |
| US1 | T006 CLI contract file and T007 integration file | Both precede implementation; T012 wheel checks wait for code/resources. |
| US3 | T014 retry tests and T015 safety tests in distinct files | T016/T017 then make the relevant new cases pass. |
| US4 | After T019, T020 canonical guide and T021 adapter/workflow updates | T022 discovery and T023 links consume final guide paths; execute optional examples after US2. |
| US2 | T026 option contracts and T027 provenance contracts in different files | T028 parser integration, then T029/T030 validation. |

Release matrices T034/T035 and T038/T039 use distinct environments/evidence files and can run concurrently after their respective candidate/publication barriers. T001 baseline and T002 read-only preflight also use different files. These opportunities do not authorize external publication or messaging.

## Requirement Coverage

| Requirement / outcome | Primary tasks |
| --- | --- |
| FR-001 public named distribution; SC-001 | T002, T004/T005, T031–T039 |
| FR-002 name-only setup | T006–T013 |
| FR-003 destination; FR-005 defaults/options; SC-002 | T008/T009, T026–T030 |
| FR-004 independent bundled workflows | T007/T009/T011/T012, T021, T033–T035 |
| FR-006 exact input/provenance/unknowns | T009, T014/T016, T027–T030 |
| FR-007 no creative/provider setup | T007/T011, T020/T021, T024/T025 |
| FR-008 help/validation | T006/T008, T019/T022, T026/T028 |
| FR-009 saved/readiness handoff; SC-005 | T010, T015/T017, T021/T025 |
| FR-010–FR-013 safe repeat/retry/legacy; SC-003/004/006 | T003, T014–T018, T026–T030 |
| FR-014 both shells | T024, T034/T035, T038/T039 |
| FR-015 discovery/first save | T019–T025 |
| FR-016 examples/unknowns/options | T020/T024, T026–T030 |
| FR-017 inspection/resume | T020/T021/T025 |
| FR-018 troubleshooting/consistent guides | T017/T020/T023/T024 |
| SC-007 complete documented journey; SC-008 discovery/failures | T019–T025, T029/T030, T034/T035, T040 |

## Implementation Strategy

1. Complete setup/foundations, then demonstrate US1 name-only setup against an installed candidate. This is the smallest useful local MVP, retaining all existing safety checks; US3 verifies the extended recovery boundaries before release.
2. Deliver US3 safeguards and US4 core guide before optional refinements. Write optional reference from the contract, then implement US2 and finish the deferred guide/host matrix. Do not claim a guide is verified while its commands are merely planned.
3. Finish local code/docs/tests and produce a concrete reviewed candidate before external release actions. Missing license/name/publisher decisions do not stop unrelated local implementation. Seek only the specific missing maintainer decision/authorization when actually required.
4. Publish the exact validated artifacts only within explicit release authorization, then prove production named installs. A public package is a required final outcome, not an optional stretch goal.
5. Record completion incrementally with source/artifact/evidence identities. Never infer literary quality, novice approval, universal host support or retired performance targets from structural success. No runtime implementation or external changes occur merely by generating this file.

## Generation Validation

40 unique sequential tasks: Setup 2, Foundational 3, US1 8, US3 5, US4 7, US2 5, Release/Polish 10. Each task has a valid marker, ID and concrete file path; all story-phase tasks carry their original US label. Thirteen `[P]` tasks identify the constrained opportunities above. Pre/post task hooks are skipped because `.specify/extensions.yml` is absent. Requirements checklist remains specification-quality evidence, not executed task evidence.

## Implementation status — 2026-10-29

39 of 48 tasks are complete. T031, T037–T040, T043, T045, T046 and T048 remain unchecked. Partial local verification does not satisfy remote candidate, actual-host or public-release gates. See [implementation-ledger.md](implementation-ledger.md) and [readiness](../../tests/evaluations/package-init-readiness.md). The maintainer explicitly selected intentionally unlicensed; do not reopen license selection as an unanswered question.

## Phase 8: Convergence

Assessment date: 2026-10-29. Intent: spec.md, plan.md and existing tasks, governed by the constitution. Inspected current implementation and retained evidence without branch/history comparisons or executing tests. Checked 18 FRs, 8 SCs, 20 acceptance scenarios, 7 edge cases, 6 component-design decisions and 11 constitution principles. Findings F1–F5: one contradicts gap and four partial gaps, all HIGH; no direct constitution MUST violation identified. Prior completed markers remain historical implementation checkpoints, not proof that the entire requirement is satisfied.

- [X] T041 HIGH [F1] Reject explicitly empty shorthand destinations in `src/novel_creator/cli.py` before initialization writes instead of treating `--path ''` as omission through `Path(args.path or name)`. Add regression coverage in `tests/contract/test_simple_init_cli.py` showing empty explicit destination returns code 2, never calls the initializer and creates no default NAME folder; retain valid omitted/default, explicit relative/absolute, Unicode/spaces and legacy destination behavior. Recheck affected command/installed cases per FR-003, FR-008 and US2/AC1/AC5 (contradicts).
- [X] T042 HIGH [F2] Bind public installation to the actual product distribution selected by pip in `tests/verify_package_install.py`, `tests/contract/test_package_release.py` and `.github/workflows/package-release.yml`. Preserve the named production-index installation route, but capture pip's installation report and verify the selected normalized product name/version and download archive SHA-256 against the approved candidate wheel or supported source artifact. Downloading/hash-checking the expected files before a separate install is insufficient: add a rejection case where expected public files validate but pip selects another same-version/platform-specific artifact, plus a matching-selection success case. Record the selected artifact/hash in output and ensure mismatches fail before reporting validation success per T038/T039, SC-001 and plan: exact public artifact identity (partial).
- [ ] T043 HIGH [F3] Finish or reuse the still-open T031/T033 work in `pyproject.toml`, `specs/002-package-novel-init/release-preflight.md`, `.github/workflows/package-release.yml`, `tests/evaluations/package-init-release-manifest.json` and `tests/evaluations/package-init-candidate.md`: verify public distribution-name control and unused version, finalize truthful release README/documentation URLs and metadata, and, only after explicit authorization for repository availability/dispatch, produce and retrieve the immutable remote candidate from the corrected source. Record repository, source commit, run ID/attempt, artifact ID, wheel/sdist names/hashes and metadata/source/resource/sdist verification. Retain the maintainer's intentionally-unlicensed decision; do not reopen licensing or infer name control from a 404. Missing account/access/authorization remains an explicit open gate, never a fabricated identity. Do not publish in this task per FR-001, US1/AC1, T031/T033 and plan: immutable candidate handoff (partial).
- [X] T044 HIGH [F4] Finish or reuse T024/T025 against T043's candidate in `workflows/getting-started.md`, `tests/evaluations/package-init-guide-windows.md`, `tests/evaluations/package-init-guide-linux.md` and `tests/evaluations/package-init-host-guide.md`. Execute the literal guide route with documented prerequisites, shell quoting/activation or explicit-interpreter alternative, defaults/options and all six troubleshooting categories; then perform actual fresh Codex setup, confirmed exact first exchange, inspection and resumption on the required host/platform combinations. Bind evidence to candidate artifact/runtime identity, preserve real input/source/save-before-display boundaries and old-novel fallback, and distinguish shell/structural tests from actual host evidence. Record unavailable checks honestly without inventing human/novice approval or adding a new manual-rating gate per FR-014–FR-018, US4/AC1–AC5, SC-005/SC-007/SC-008 and plan: guide verification (partial).
- [ ] T045 HIGH [F5] Complete or reuse T034–T040 after T041–T044 in `.github/workflows/package-release.yml`, `tests/verify_package_install.py`, `specs/002-package-novel-init/release-preflight.md`, `tests/evaluations/package-init-candidate-windows.md`, `tests/evaluations/package-init-candidate-linux.md`, `tests/evaluations/package-init-release-manifest.json`, `tests/evaluations/package-init-public-windows.md`, `tests/evaluations/package-init-public-linux.md`, `tests/evaluations/package-init-readiness.md`, `specs/002-package-novel-init/implementation-ledger.md` and `README.md`. Verify the same immutable candidate on both platforms, configure trusted publishing/protected environment only under explicit maintainer authorization, and publish only those verified bytes without rebuilding once required guide/host evidence exists. Run both public named-install checks with T042's actual-selection hash proof, reconcile every FR/SC and current-source evidence, and update status only from confirmed outcomes. If already published, verify that release rather than republishing; if external gates remain unavailable, preserve the partial status. Do not revive retired latency/novice gates or claim full delivery from local passes per FR-001, SC-001, T034–T040 and plan: production delivery and final verification (partial).

Execution dependencies: fix and verify T041/T042 before any new T033 candidate or T037 publication; source/package changes invalidate affected earlier candidate evidence. T043 produces the candidate before T044's final candidate-bound walkthroughs. Both-platform candidate checks from T034/T035 may run alongside T044 after that candidate exists, but publication in T045 waits for all required candidate/guide/host gates and explicit release authorization. Reuse verified existing work and evidence rather than repeating account setup, rebuilding approved artifacts or publishing twice. These convergence tasks consolidate the remaining original work; they do not authorize pushes, workflow dispatches, account changes or publication. Original task IDs, markers, phase text and requirements checklist remain unchanged by convergence.


## Phase 9: Convergence

Assessment date: 2026-10-29. Reassessed current code and retained evidence against spec.md, plan.md and tasks.md under constitution 1.0.0. Inspected 18 functional requirements, 8 success criteria, 20 acceptance scenarios, 7 edge cases, 6 component-design decisions and 11 constitution principles. No test execution, branch comparison or history inspection was performed. Requirements-quality checklist remains 16/16 checked and is unchanged. Implementation has run against the complete task list; T041/T042 now have current code, regression coverage and labeled local installed-package evidence. The empty-destination and actual pip-selection gaps are closed. Three HIGH partial findings remain, retaining stable F3/F4/F5 references; no additional implementation contradiction or direct constitution MUST conflict was identified. Prior local passes do not establish remote candidate, actual host or public delivery.

- [ ] T046 HIGH [F3] Complete or reuse T043 and T031/T033 in `pyproject.toml`, `src/novel_creator/__init__.py`, `specs/002-package-novel-init/release-preflight.md`, `.github/workflows/package-release.yml`, `tests/evaluations/package-init-release-manifest.json` and `tests/evaluations/package-init-candidate.md`: establish distribution-name control and an unused release version, finalize truthful metadata and release README/documentation URLs, then obtain the immutable remote candidate from the corrected source only after explicit repository availability/push/dispatch authorization. Record repository/source commit/run ID/attempt/artifact ID and wheel/sdist names/hashes; verify metadata, exact-source/resources and separate sdist rebuild/install without replacing approved bytes. Preserve the intentionally-unlicensed decision. A missing listing is not name control; missing authorization/access stays an open gate. Reuse an already verified candidate if available, and do not publish in this task per FR-001, US1/AC1, T031/T033/T043 and plan: immutable candidate handoff (partial).
- [X] T047 HIGH [F4] Complete or reuse T044 and T024/T025 against T046's verified candidate in `workflows/getting-started.md`, `tests/evaluations/package-init-guide-windows.md`, `tests/evaluations/package-init-guide-linux.md` and `tests/evaluations/package-init-host-guide.md`: execute the literal Windows PowerShell/Linux Bash guide with documented prerequisites, quoting, activation or explicit interpreter, discovery/defaults/options and all six troubleshooting categories; perform actual fresh Codex setup, a confirmed exact first exchange, inspection and resumption on both required host/platform combinations. Record candidate/runtime/source identities, current-input provenance and save-before-display evidence. Existing clean-install fixtures are supporting command evidence, not the missing actual-host walkthrough. Preserve older novels and their labeled guide fallback; retain unavailable checks honestly and do not add human/novice approval or latency gates per FR-014–FR-018, US4/AC1–AC5, SC-005/SC-007/SC-008, T024/T025/T044 and plan: guide and separate-host verification (partial).
- [ ] T048 HIGH [F5] Complete or reuse T045 and T034–T040 after T046/T047 in `.github/workflows/package-release.yml`, `tests/verify_package_install.py`, `specs/002-package-novel-init/release-preflight.md`, `tests/evaluations/package-init-candidate-windows.md`, `tests/evaluations/package-init-candidate-linux.md`, `tests/evaluations/package-init-public-windows.md`, `tests/evaluations/package-init-public-linux.md`, `tests/evaluations/package-init-release-manifest.json`, `tests/evaluations/package-init-readiness.md`, `specs/002-package-novel-init/implementation-ledger.md` and `README.md`: bind both-platform checks to the immutable candidate; configure trusted publishing/protected environment only under explicit setup authorization; publish the verified bytes without rebuilding only after required candidate/guide/host gates and explicit release authorization. If already published, verify the existing release rather than republishing. Execute both production named installs with T042's selected normalized name/version/filename/archive SHA-256 proof; reconcile each FR/SC and evidence limits before claiming delivery. Missing account, authorization, candidate, host or public evidence leaves the relevant tasks open per FR-001, SC-001, T034–T040/T045 and plan: production delivery and final verification (partial).

Execution dependencies: reuse T041/T042's verified fixes; do not repeat their implementation unless new evidence reveals a regression. T046 produces the remote candidate; final T047 evidence consumes it. T048's candidate platform checks may run alongside T047 once that candidate exists, but publisher setup/publication follows the established gates and explicit authorizations. These are follow-through tasks for the same remaining work, not permission to repeat external actions, invent evidence or reopen licensing. Existing task IDs/markers, artifacts and application files are unchanged by this assessment. No extension hooks are configured.


## Owner-approved host verification amendment — 2026-10-29

The owner explicitly authorized disposable Codex evaluation chats/sessions, then selected "Amend to Windows Codex + Linux CLI". For T024/T025/T037/T040/T043–T048, apply the spec amendment: actual Windows Codex Desktop setup/first-save/inspection/resume and both-platform guide/CLI/troubleshooting/public-install evidence are required; Linux Codex host behavior stays explicitly unverified and is no longer a 0.1.0 release gate. Earlier task wording is retained as history and must not cause a fabricated linux_host pass. Exact input provenance, save-before-display, resource/identity binding, safety, public artifact hashes and separate release approval remain in force.
