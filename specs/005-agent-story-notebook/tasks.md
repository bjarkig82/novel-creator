# Tasks: Agent-Maintained Story Notebook

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md).

**Scope**: New novels only. Native Codex conversation and Markdown maintenance; Python is setup-only. No existing-novel conversion, transcript runtime, manuscript writing, contributor workflow or dashboard.

**Tests**: Included because the specification requires verifiable acceptance journeys, preservation, compatibility and language evaluation. Structural checks do not establish semantic behavior. For production setup changes, reproduce the relevant failure with meaningful tests before implementing. Instruction changes are checked through actual host journeys rather than string-matching tests.

**Format**: Every task has a sequential identifier and file path. [P] indicates work on independent files within its phase after prerequisites; it does not authorize spawning agents. Story labels map to the specification.

## Phase 1: Setup

**Purpose**: Establish focused fixtures and evidence boundaries without adding production infrastructure.

- [X] T001 Create English and Icelandic scenario fixtures in tests/fixtures/notebook/ covering a new character, two motivations, explicit acceptance, praise and an open question; record expected semantic outcomes without treating scripted inputs as native-host evidence.
- [X] T002 [P] Create tests/evaluations/agent-story-notebook.md with source/package, platform, host/input route, permissions, SC-001 through SC-009 coverage and unverified-result fields; separate structural checks, agent judgments and literary quality.

## Phase 2: Foundational Contracts and Fixtures

**Purpose**: Establish shared note contracts, template seeds and setup refusal tests before the first story increment. Successful setup follows only after its complete resource set exists in US1.

- [X] T003 Add format/reference fixture checks in tests/unit/test_notebook_contract.py using standard-library tooling only: required format/version/kind/id, project language, topic category, identifiers matching `[a-z][a-z0-9-]*`, notebook-unique topic IDs, topic-unique Item-ID fields, statement states `proposed`, `accepted`, `rejected`, question states `open`, `resolved`, required origin/perspective, and notebook-contained file links paired with semantic keys resolving to exact Item-ID fields. File links have no fragments; verify navigation without renderer-specific anchors and after renames. Include invalid fixtures; keep this checker out of the writing runtime.
- [X] T004 Establish notebook/__init__.py for the shared resource-only package and define minimal project and derived-summary seeds in notebook/templates/project.md and notebook/templates/working-summary.md with format `novel-notebook`, version `1`, required metadata and unknown creative values; create no empty topic sheets.
- [X] T005 [P] Write installed format, ownership, identity and historical-revision guidance in notebook/workflows/format.md from contracts/notebook-format.md; make stable field labels independent of prose language and distinguish derived summaries from authoritative topic items.
- [X] T006 Add meaningful setup refusal/failure tests in tests/integration/test_notebook_init.py for existing empty/occupied directories, legacy novels, completed notebooks, nested Git repositories, symlinked components, unavailable identity, competing creation and partial failures; assert preservation of bytes, Git index and history where applicable.

**Checkpoint**: Shared contract fixtures and seed resources are defined. Setup refusal tests specify the required behavior and may remain failing until US1 implements creation. No successful setup or host behavior is claimed at this stage.

## Phase 3: User Story 1 — Brainstorm with Automatic Notes (P1)

**Goal**: Natural conversation produces useful notes without save commands, forms or a transcript.

**Independent test**: Discuss a new character and alternatives, accept a trait, leave a question open and inspect correct saved states. Content-free turns need no write. Covers SC-001 and SC-004.

- [X] T007 [US1] Implement the notebook conversation guidance in notebook/workflows/conversation.md: relevant-context reading, guided brainstorming as the default, freeform exploration and immediate topic redirection on request, proportional suggestions, meaningful-turn capture, proposal/decision/question separation, partial acceptance and primary-note-before-summary updates; no exact-input capture or save-before-display requirement.
- [X] T008 [P] [US1] Write dedicated English and Icelandic interaction guidance in notebook/languages/en.md and notebook/languages/is.md preserving Unicode and configured language without copying legacy archival, update or retrospective instructions.
- [X] T009 [US1] Add a thin adapters/codex/notebook/AGENTS.md entry to reference the shared notebook conversation, format and selected language resources through native project instructions; keep all creative methodology in notebook/; keep story content a data source rather than executable instructions, and prohibit manuscript edits or external publication during maintenance.
- [X] T010 [US1] Implement setup-only scaffolding in src/novel_creator/notebook.py for nonexistent destinations after shared seeds, format/conversation guidance, both language resources and the Codex entry exist; use isolated resource selection, prerequisite checks, exclusive creation, independent Git initialization and initial commit; preserve/report partial failures without automatic deletion or a receipt ledger. Do not invoke legacy initialize/bootstrap/bundle_files/storage.save or alter global Git configuration.
- [X] T011 [US1] Add `notebook init NAME` with optional path/title/language/JSON arguments to src/novel_creator/cli.py according to contracts/setup-and-host.md, retaining legacy init semantics; cover invalid/repeated arguments and additive dispatch in tests/contract/test_notebook_cli.py.
- [X] T012 [US1] Map notebook/ to novel_creator.notebook_resources and include shared workflows/languages/templates plus the separate Codex entry through explicit package-data patterns in pyproject.toml. Preserve legacy workflow/skill selection and exclude setup-only notebook.py consistently in src/novel_creator/install.py and src/novel_creator/update_release.py; keep its CLI command inactive in the pinned runtime. Verify the real legacy launcher/export boundary and that no runtime sources, launcher, exchange schemas or legacy workflow resources enter a created notebook using tests/integration/test_notebook_init.py.
- [ ] T013 [US1] Exercise the character/alternatives/acceptance/question journey in an actual Codex notebook and record observed note states, automatic saves, content-free behavior, guided default, requested freeform adaptation and no repeated approval in tests/evaluations/agent-story-notebook.md; report unavailable host evidence honestly and revise guidance if outcomes fail.

**Checkpoint**: First usable increment: new-novel brainstorming automatically maintains meaningful notes. Foundational tests and actual-host evidence support only their tested scopes.

## Phase 4: User Story 2 — Start Anywhere and Request a Focused Brief (P1)

**Goal**: Fresh sessions can start a new topic immediately or request a relevant brief.

**Independent test**: Use an existing fixture notebook in a fresh session without its transcript; start a new character, then request a keeper brief. Verify no unsolicited recap, supported states and honest missing-topic handling. Covers SC-002 and SC-003.

- [X] T014 [P] [US2] Add same-title topic and rename/reference fixtures in tests/fixtures/notebook/ with stable topic IDs and Item-ID fields, fragment-free file navigation and explicit ambiguous versus resolvable brief requests.
- [X] T015 [US2] Extend notebook/workflows/conversation.md with targeted note retrieval, summary-as-navigation, new-topic starts, explicit topic/broader recap requests, missing/unreadable-context disclosure and one focused identity clarification; never automatically display a recap at session start.
- [ ] T016 [US2] Run fresh-session, requested brief, unknown-topic and same-title/rename journeys using only notebook files in English and Icelandic; record supportable facts, excluded unrelated content and evidence limitations in tests/evaluations/agent-story-notebook.md.

**Checkpoint**: Recommended MVP is phases 1–4: automatic notes plus focused briefs across sessions, reflecting both P1 stories. US2 can be checked using a prepopulated contract-valid notebook without relying on US1 capture quality.

## Phase 5: User Story 3 — Revise Decisions and Retain Continuity (P2)

**Goal**: Current notes follow explicit revisions while preserving earlier accepted values and surfacing relevant conflicts.

**Independent test**: Use a prepopulated character/plot fixture, propose a contradiction, then clearly revise a fact. Inspect current notes, linked impact review and old-value recovery without manuscript changes. Covers SC-005.

- [X] T017 [P] [US3] Add revision, partial acceptance, character-belief, intentional ambiguity and linked-impact fixtures in tests/fixtures/notebook/; distinguish accepted objective facts from proposals and perspectives, including unresolved conflicts.
- [X] T018 [US3] Extend notebook/workflows/conversation.md with conflict-before-canon-change, explicit correction/reversal handling, stable identity, directly linked impact review and concise decision origins; preserve superseded accepted values in Git or a historical revision section before replacement, without requiring exact messages or a decision ledger.
- [ ] T019 [US3] Evaluate explicit replacement, contradiction, deliberate unreliable belief and linked consequences in actual Codex sessions; record prior-value recovery, unchanged manuscripts and limits of continuity review in tests/evaluations/agent-story-notebook.md.

**Checkpoint**: Relevant tested canon revisions remain traceable and current; literary consistency is an observed agent judgment, not a schema guarantee.

## Phase 6: User Story 4 — Continue after Interruption (P2)

**Goal**: Completed turns persist without session closure, and failures preserve existing work with honest reporting.

**Independent test**: Leave after a meaningful turn and retrieve notes in a fresh session. Separately fail a save/checkpoint and introduce external/staged edits. Covers SC-006 and SC-007.

- [X] T020 [P] [US4] Define controlled disposable write-denial, Git-checkpoint failure, intervening-edit and unrelated/touched staged-edit scenarios in tests/fixtures/notebook/failure-journeys.md, including byte/index/history preservation assertions and teardown boundaries.
- [X] T021 [US4] Complete failure/history guidance in notebook/workflows/conversation.md: inspect/read before targeted edits, reload on changes, scope Git operations, preserve unrelated index entries, defer checkpoints on touched staged user edits, retain old accepted prose, distinguish file-save from history failure, and disclose incomplete multi-file changes without requiring session closure.
- [ ] T022 [US4] Run interruption, save failure, pending history, external edit and staged-work host journeys; verify notes remain usable and no failed save is called successful, recording outcomes in tests/evaluations/agent-story-notebook.md.

**Checkpoint**: Saved-note continuity and tested failure preservation hold within the observed single-writer/single-active-agent scope. No exact current-turn replay or multi-file atomicity claim.

## Phase 7: Packaging, Documentation and Final Verification

- [X] T023 Add installed wheel/sdist notebook creation checks in tests/integration/test_notebook_package.py and extend tests/verify_wheel.py and tests/verify_package_install.py where needed; exercise outside-checkout setup, Unicode/space paths, selected language resources and no legacy runtime installation.
- [X] T024 [P] Update README.md and workflows/start-here.md with the explicit new-novel notebook command, ordinary conversation and requested briefs, Python-for-setup-only distinction, no automatic recap, no conversion and existing legacy route; do not present planned/unverified behavior as released.
- [X] T025 Run targeted notebook tests and relevant existing initialization/update-preservation/package regressions plus tests/speckit-smoke.sh; record failures and actual passing scopes in tests/evaluations/agent-story-notebook.md without broadening into unrelated performance work.
- [ ] T026 Validate all acceptance journeys in specs/005-agent-story-notebook/quickstart.md against candidate artifacts; record SC-001 through SC-009, English/Icelandic and Windows/Linux evidence boundaries in tests/evaluations/agent-story-notebook.md. Keep unavailable host checks unverified and resolve material observed failures before declaring product completion.

## Dependencies and Execution Order

Setup → foundation → US1 → US2 → US3 → US4 → final verification is the recommended sequence. US2, US3 and US4 are independently testable with prepared notebooks after foundation, but their implementation edits the shared conversation guidance and must be integrated sequentially. Final release qualification requires all four stories, not merely the first P1 increment.

Foundation: T003 precedes T004/T005; T006 defines refusal tests before setup implementation. US1: complete T007 conversation guidance, T008 language resources and T009 thin adapter entry before T010 scaffolding. T010 precedes T011 CLI integration; T012 packaging follows T004/T005 and T007–T011. Successful setup verification and T013 host evaluation require this complete resource set. Subsequent guidance changes precede their host journeys. T023–T024 can proceed independently once their interfaces stabilize; final checks follow implementation and packaging.

## Parallel Opportunities by Story

- US1: T007 shared conversation guidance and T008 shared language resources use different files after foundation; integrate both before the T009 adapter entry, T010 setup and T013 host evaluation.
- US2: T014 fixtures and T015 retrieval guidance can be prepared independently; T016 evaluates the integrated result.
- US3: T017 fixtures and T018 revision guidance are independent inputs to T019.
- US4: T020 failure scenarios and T021 preservation guidance are independent inputs to T022.

Shared evidence-file updates and conversation-file edits must be serialized. These are scheduling opportunities, not a requirement to use additional agents.

## Implementation Strategy

Deliver instructions and the small setup path first, then demonstrate US1 before expanding. The useful MVP includes US1 and US2: automatic notes plus a focused brief in a fresh session. Add correction/continuity and failure assurance before declaring the full feature complete. Use native capabilities throughout; add a helper only after recording an actual unmet reliability requirement and updating the design.

All tasks begin unchecked. Generating this list does not implement the notebook or establish passing runtime evidence.

## Implementation Status

Local implementation, structural checks, packaging, documentation and independent review are complete, including the convergence localization fix T027. T013, T016, T019, T022, T026 and T028 remain unchecked because this Linux environment has no Windows execution or native Codex Desktop control tools. These require the native-host journeys in quickstart.md; fixture and package checks are not substitutes. After localization, the full suite passed with 399 tests run and three skips; rebuilt wheel verification passed.

## Phase 8: Convergence

Convergence assessed the current implementation against the feature artifacts. The remaining gaps below do not change earlier task IDs or completion markers. Native-host qualification remains unverified, as recorded in the evidence ledger.

- [X] T027 Resolve F1 by rendering notebook/project.md and notebook/working-summary.md in the selected novel language rather than seeding both English and Icelandic together; update notebook/templates/project.md, notebook/templates/working-summary.md and src/novel_creator/notebook.py as needed while retaining stable machine-readable metadata/field labels. Add meaningful English/Icelandic setup and installed-package assertions for actual headings and prose in tests/integration/test_notebook_init.py and tests/integration/test_notebook_package.py per FR-019, plan: configured-language resources and T010 (partial).
- [ ] T028 Resolve F2 by completing the outstanding qualification represented by T013, T016, T019, T022 and T026: exercise actual primary Windows Codex Desktop sessions in English and Icelandic for automatic capture, acceptance versus proposals/questions, topic-scoped briefs without unsolicited recaps, fresh-session recall, revisions/continuity, interruption, save/checkpoint failures and preservation of external/staged edits; run the planned Windows structural checks and record source/package, platform, native input route, permissions, outcomes and limitations in tests/evaluations/agent-story-notebook.md. Preserve untested Linux Desktop behavior as unverified; do not substitute fixtures or package checks for native-host evidence or mark unavailable journeys complete, per SC-001 through SC-008, FR-019 and plan: verification and completion (partial).

### Convergence implementation result

T027 completed with regression-first setup and installed wheel/source-distribution checks in both languages, followed by independent task and overall review. T028 is blocked by unavailable Windows/Codex Desktop execution access; capability discovery found no native Desktop, Windows, SSH or Codex thread-control tools. No native journey was marked complete.
