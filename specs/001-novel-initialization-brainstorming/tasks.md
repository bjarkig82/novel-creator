# Tasks: Novel Initialization and Guided Brainstorming

## Current execution scope — owner amendment, 2026-10-28

The owner withdrew **all time-related performance targets** and requested
functional completion before further optimization. Read/save timings are
informational; no latency optimization or fresh scale benchmark is required to
close this delivery. Operation errors, incomplete runs and hung tests still fail;
all storage, creative-authority, source, recovery and manuscript safeguards remain.

T172 and the optimization portion of T174 are retired by this amendment, not
measured performance passes. T173/T175 now reconcile functional delivery under
this policy. Earlier unchecked tasks and historical convergence phases preserve
their original evidence/scope; Phase 21's novice/manual exclusions and completed
T168-T171 automate the current six-story scope. Historical native/human/subjective
unknowns do not become passes. Use this section and the final qualification
checkpoint below as the active execution scope, rather than reopening superseded
latency or novice/manual work.

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts](contracts/cli.md), and [quickstart.md](quickstart.md).
**Governance**: Constitution 1.0.0. Checkboxes retain source-specific completion
or explicit retirement; historical unchecked markers do not override the current
execution scope above.

**Historical execution summary (superseded by the current scope and final checkpoint):**

Execution status: T001–T011 implemented. T012/T069/T089/T103/T116 now pass
within the tested Windows Desktop native-tool/text-input/scoped-approval scope.
T013 records the latest **PASS** gate decision. Story implementation has resumed;
initialization, installed reads/session helpers, recovery and shared workflow
resources are delivered with the checked tasks below. Full story/release
evaluations and remaining implementation tasks are still incomplete. Earlier BLOCKED assessments below are historical;
see implementation-ledger.md and ../../tests/evaluations/host-capture.md.

**Tests**: Required by the specification's acceptance scenarios, SC-001–009,
FR-026 and constitution IX. Write applicable behavioral tests before implementing
the corresponding behavior, observe meaningful failure, then implement and verify.
Host/model judgments and human evaluations are distinct from automated tests.

## Format and path conventions

`- [ ] T### [P?] [US#?] Description with exact file paths`.
Paths are relative to the framework repository root unless explicitly marked as
novel-installed paths. `[P]` means disjoint files and no dependency between the
named sibling tasks, after their shared prerequisites. It does not authorize
parallel edits to shared schema/CLI modules. Run other tasks sequentially within
their phase. References to `data-model.md` below mean the feature design document.

## Phase 1: Setup

**Purpose**: Package the small local Python tool without adding an AI runtime.

- [X] T001 Create Python >=3.11 packaging and resource installation configuration in pyproject.toml and src/novel_creator/__init__.py; declare jsonschema >=4.23,<5 and a test extra usable by the quickstart, with Git >=2.39 documented as an external prerequisite.
- [X] T002 Create the module entry point and CLI command skeleton in src/novel_creator/__main__.py and src/novel_creator/cli.py using contracts/cli.md; support one UTF-8 JSON stdout result, stderr diagnostics, documented exit codes 0/2/3/4/5/6, and subprocess argument arrays rather than shell interpolation.
- [X] T003 [P] Add unittest discovery packages and disposable real-Git-repository/fault-injection helpers in tests/__init__.py, tests/unit/__init__.py, tests/contract/__init__.py, tests/integration/__init__.py and tests/helpers.py; configure only temporary repository identities and never modify global Git settings.
- [X] T004 [P] Record reproducible dependency resolution and development prerequisites in requirements-lock.txt and docs/development.md; cover Python/Git versions, active-environment commands, fixture cleanup, no model credentials and separate claimed-host support evidence.

**Checkpoint**: CLI help and test discovery work; no story capabilities claimed.

## Phase 2: Foundation and blocking Codex capability gate

**Purpose**: Establish the atomic persistence primitive and prove native host
capture before building the full story workflows. The spike uses a minimal
installed fixture, not a dependency on completed US1/US3 features.

- [X] T005 Write schema/digest/chain/CLI result contract tests in tests/contract/test_exchange.py and tests/unit/test_digest.py covering null bootstrap predecessor, unknown versions, malformed UTF-8/JSON, NaN/Infinity, duplicate IDs, valid/invalid bootstrap artifact digests and JSON Pointer sources, forbidden artifact-only canon authorization and consistent error checkpoints (FR-009, FR-014, FR-022).
- [X] T006 Define all shared record and exchange schemas in schemas/v1/records.schema.json and schemas/v1/exchange.schema.json from data-model.md before any story fixture runs: common UUID IDs, positive revisions, null creation predecessor, sequence starting at 1, schema_version "1.0", nullable bootstrap session/HEAD, operation bootstrap/conversation/maintenance, exact visible messages, and every Novel Project, Session, Idea, Story Element, Relationship, Assertion/time, Decision, Question and Finding field/enum/conditional constraint. Include typed message/bootstrap_artifact sources, preserved input_artifacts with digest and JSON Pointer validation, explicit default origins, and routine_checkpoint on_request (default)/session_close/every_exchange; bootstrap artifacts cannot authorize canon and maintenance cannot introduce it (FR-002, FR-009–013, FR-020–023).
- [X] T007 Implement canonical serialization, immutable full-record revision folding and foundational source/reference/authorization checks in src/novel_creator/records.py and src/novel_creator/validation.py; SHA-256 excludes payload_digest, sorts keys, uses compact UTF-8 JSON and preserves arrays; validate exact previous revisions, typed source ranges/JSON Pointers, bootstrap artifact digests, same-bundle forward references, actual user-message canon authorization and cross-novel exclusion before atomically applying a bundle (FR-009–013, FR-020–023).
- [X] T008 Write transaction and protected-path tests in tests/integration/test_storage.py for private-index candidate construction, conditional update-ref publication, unborn-branch bootstrap, lock conflicts, same-ID retries, filesystem/ref/receipt fault windows, and managed-index cleanup after publication. Inject a competing commit immediately before publication: assert rejected candidate absent from branch history/current canon and competing HEAD plus user index unchanged; also test traversal/symlink rejection and manuscript hashes (FR-009, FR-013–014; SC-009).
- [X] T009 Implement contracts/storage.md in src/novel_creator/storage.py: lock, expected hashes, temporary bundle flush/publication, private Git index and commit-tree candidate with verified explicit-path delta/parent, then compare-and-swap update-ref against expected local branch HEAD (absent ref for bootstrap). Preserve pending work on rejection, safely synchronize only managed index entries after successful publication, report cleanup failures as saved-with-cleanup-needed, never reset/amend/stage everything/push, and pass T008 (FR-009, FR-014).
- [X] T010 Implement foundational exchange save dispatch and structured checkpoint/errors in src/novel_creator/cli.py; keep the same exchange ID/digest on retry, return original success for committed identical payloads, reject changed payloads, return explicit saved/cleanup_required warnings after published-ref index failures, and pause further writes until safe recovery (FR-009, FR-014).
- [X] T011 Build a disposable minimal installed-bundle fixture and save-before-emit Codex adapter in tests/fixtures/host-spike/ and adapters/codex/AGENTS.fragment.md; use production storage, fixture-only launcher/context and exact visible response text without hidden reasoning, transcript scraping, post-response hooks or a custom chat runtime (FR-009, FR-025).
- [X] T012 Define and execute the actual Codex spike in tests/evaluations/host-capture.md: save before display, at least two further automatic turns without reinvocation, fresh-chat recovery, interruption after commit/before display, identical retry and failed-save disclosure; record host/model/version, messages, receipts and commit checkpoints. Mark unavailable evidence unverified; mocks alone do not pass (FR-008–009, FR-014, FR-025; SC-009).
- [X] T013 Record the spike gate decision in tests/evaluations/host-capture.md and docs/development.md; proceed to user-story implementation only after T012 demonstrates the protocol, otherwise stop dependent implementation and revisit the adapter through planning without weakening FR-009 or silently adding an AI runtime.

All story record schemas are complete at T006; later story tasks add behavior,
not schema prerequisites. Bootstrap provenance and routine checkpoint settings
are covered by foundation contracts before story-level evaluations.

**Checkpoint**: Atomic tool primitive tested and actual native-host capture proven.
No story phase starts before T013 passes. The tool lock does not claim to control
arbitrary external Git processes; preserve evidence and return conflict on races.

## Phase 3: US1 — Start a Novel from Any Starting Point (P1, initial MVP)

**Goal**: A novice can initialize with a concept or none and reopen a revisable
brief independently of brainstorming.
**Independent test**: Initialize separate novels from no concept and supplied
concept, reopen each, rename/change preferences, repeat setup at an existing
location and verify identity/references/content preservation.

- [X] T014 [P] [US1] Write initialization contract tests in tests/contract/test_initialize.py covering empty/unknown preferences, supplied original concept versus interpretation, stable identity after title change and exact CLI responses (FR-001–003; SC-002).
- [X] T015 [P] [US1] Write installation integration tests in tests/integration/test_install.py for independent Git roots, nested-repository rejection, recognized-novel continuation, unrelated content preservation, partial bootstrap retry, existing AGENTS.md and missing prerequisites/Git identity (FR-003, FR-025).
- [X] T016 [US1] Implement Novel Project/bootstrap validation against foundation schemas in src/novel_creator/validation.py: stable UUID, BCP-47 manuscript language en default/is supported, state: unknown for skipped answers, original concept retained as a preserved bootstrap input artifact, valid field JSON Pointer/digest sources, explicit system defaults and actual message-only canon authorization. Enforce routine_checkpoint on_request/session_close/every_exchange without waiving safeguards (FR-001–003, FR-013).
- [X] T017 [US1] Implement independent-repository initialization and manifest/checksum bundle copying in src/novel_creator/install.py, including the installed .novel-creator/run.py launcher, resources, ignores and line-ending configuration; preserve existing content/AGENTS.md and report partial initialization without inventing a confirmed checkpoint (FR-003, FR-022, FR-025).
- [X] T018 [US1] Wire init and project-setting revisions through src/novel_creator/cli.py and src/novel_creator/records.py; accept unknowns, persist supplied preferences without re-questioning, preserve identity through title changes and offer recognized-novel continuation rather than recreation (FR-001–003).
- [X] T019 [US1] Author conversational setup in workflows/initialize.md and adapters/codex/skills/novel-init/SKILL.md covering all FR-002 preferences, bundled answers, skipped uncertainty, temporary title, no inferred canon, save-before-emit and optional brainstorming after successful initialization (FR-001–003, FR-025).
- [X] T020 [US1] Execute the independent initialization journey in tests/integration/test_initialize_journey.py using no-concept and supplied-concept fixtures, reopen/settings changes and interrupted bootstrap; verify tests T014–015 pass and no inferred facts become canon (SC-002, SC-009).
- [ ] T021 [US1] Add slice onboarding in README.md and run/record SC-001 in tests/evaluations/novice-initialization.md: at least 4 of 5 novice evaluators reach the brainstorming invitation within 10 minutes without outside assistance; unavailable human results remain unverified (FR-026).

**Checkpoint**: US1 is demonstrable; brainstorming is offered, not required.

## Phase 4: US2 — Develop Ideas through Creative Conversation (P1)

**Goal**: Guided/open exploration adapts to preferences and the user's next-turn
direction, without requiring later drafting or full resumption features.
**Independent test**: From a prepared brief/session fixture, explore premise,
character and setting; switch modes, redirect topic and reduce suggestions.

- [X] T022 [P] [US2] Write mode/redirection workflow tests in tests/contract/test_guidance.py using prepared sessions, asserting guided default, next-response switching, topic changes and preserved prior records (FR-004–006; SC-007).
- [X] T023 [P] [US2] Define guidance evaluation scenarios in tests/evaluations/guidance-cases.md for constructive challenge, novice explanations, proportional suggestions, host-provided voice transcription, genre/complexity/style adaptation and requests for fewer suggestions (FR-005–007).
- [X] T024 [US2] Implement Brainstorming Session lifecycle/mode behavior against T006 schemas in src/novel_creator/records.py: mode guided/open, state open/closed, guided default, saved mode on resume and explicit reopen request; test transitions without introducing later-phase schema dependencies (FR-004, FR-008).
- [X] T025 [US2] Author shared guidance and initial English resources in workflows/brainstorm.md and languages/en.md; normally ask one focused question, offer meaningful alternatives without prescribing methodology, honor redirection/reduced suggestions and accept host voice transcriptions as text (FR-004–007).
- [X] T026 [US2] Implement the thin brainstorming entry in adapters/codex/skills/novel-brainstorm/SKILL.md using shared resources, prepared context and production exchange save; keep novelist/coach/Guardian as responsibilities rather than an agent scheduler (FR-004–007, FR-009, FR-025).
- [ ] T027 [US2] Run/record actual host guidance cases in tests/evaluations/guidance-results.md and tests/integration/test_guidance_journey.py; every mode/topic request affects the next saved/displayed response, with no lost work and no unsaved creative suffix (SC-007).
- [ ] T028 [US2] Document brainstorming usage in README.md and record the five-novice usefulness/control evaluation in tests/evaluations/novice-guidance.md; require at least 4 of 5 ratings >=4/5 and distinguish human evidence from automated assertions (FR-026; SC-007).

**Checkpoint**: US2 works against prepared records independently of later stories.

## Phase 5: US3 — Resume without Retelling the Story (P1)

**Goal**: Automatically capture and inspect sourced story information, manage
multiple sessions and recover through fresh interactions/failures.
**Independent test**: Start with two saved sessions, reopen in a fresh interaction,
resume one, create another and recover all designated records with sources.

- [X] T029 [P] [US3] Write session/context/inspection CLI tests in tests/contract/test_context.py for list/start/resume/close, duplicate names, session focus/mode, source links, derived summaries and explicit incomplete coverage (FR-008–010, FR-019–020).
- [X] T030 [P] [US3] Write recovery integration tests in tests/integration/test_recovery.py for pending save inspection/retry, lost receipts, interrupted display, stale locks, published-ref index cleanup without decision replay, save-failure pauses and preserving unrelated Git changes; no silent overwrite, rollback or inferred acceptance (FR-014; SC-009).
- [ ] T031 [US3] Implement typed Idea, Story Element, Relationship and Unresolved Question record handling against T006 schemas in src/novel_creator/records.py: statuses proposed/accepted/rejected/unresolved/superseded, element_type character/location/event/plot_thread, question state open/resolved, nullable alternative_group_id, explicit relationship direction and sourced time/perspective. Allow duplicate names; never reject unselected alternatives implicitly (FR-009–010, FR-019–020).
- [ ] T032 [US3] Implement sourced extraction/correction instructions in workflows/brainstorm.md and typed revision support in src/novel_creator/records.py; capture conversations, ideas, characters, relationships, plot/world/event details, alternatives, questions and decisions every exchange, retaining erroneous versions and never promoting unaccepted captures (FR-009–010, FR-012).
- [X] T033 [US3] Implement committed session listing, focused context and source-backed history/connection inspection in src/novel_creator/context.py and src/novel_creator/cli.py; summaries are derived with source/checkpoint references, cannot hide open contradictions, and missing records return unavailable coverage (FR-008, FR-019, FR-022).
- [X] T034 [US3] Implement recover inspection and explicit unchanged-payload retry in src/novel_creator/storage.py and src/novel_creator/cli.py according to contracts/cli.md and contracts/storage.md; distinguish committed/pending/cleanup-needed work, safely synchronize only managed index entries for published saves without replay or ref reset, reject stale changed retries and lift write pauses only after successful recovery (FR-014).
- [X] T035 [US3] Author fresh-chat resumption/inspection in workflows/resume.md, adapters/codex/skills/novel-resume/SKILL.md and adapters/codex/skills/novel-inspect/SKILL.md; recover saved focus, mode, decisions and questions without requesting retelling; offer interrupted saved responses without claiming they were seen (FR-008, FR-019, FR-025).
- [ ] T036 [US3] Execute resumption/capture/correction integration and real-host cases in tests/integration/test_resume_journey.py and tests/evaluations/resume-results.md: three sessions plus a fresh interaction recover all 20 designated ideas, 10 explicit decisions and 5 questions with correct state/source; run T029–030 and distinguish structural results from host judgments (SC-003, SC-009).
- [X] T037 [US3] Document session listing/resume/close, inspecting knowledge and safe recovery in README.md; include last-confirmed checkpoint examples, save-before-continuation behavior and clear failure disclosure (FR-026).

**Checkpoint**: Full persistence/resumption slice works; prepared acceptance
records can support testing before US4 semantic acceptance integration.

## Phase 6: US4 — Establish and Revise Canon (P1)

**Goal**: Natural, unambiguous acceptance establishes only selected facts;
revision/reversal retains history, impact and protected authority.
**Independent test**: Prepared canon/proposals test clear, ambiguous, partial and
rejected acceptance, explicit revisions and protected-direction conflicts.

- [ ] T038 [P] [US4] Write authority/review tests in tests/unit/test_authority.py covering ambiguous/partial/clear acceptance, sourced revision/reversal and manuscript protection. Test each routine_checkpoint value, default on_request, requested and session-close triggers, every-exchange summaries, pause/continuation and no delay to saves or repeated canon approval (FR-010–013).
- [X] T039 [P] [US4] Author acceptance fixtures in tests/fixtures/en/acceptance.json with at least 12 clear-acceptance and 12 non-acceptance cases, expected selected propositions and source spans; include explicit direction conflicts and five deliberate canon revisions for later bilingual pairing (SC-004, SC-006).
- [ ] T040 [US4] Implement Creative Decision/Revision handling against T006 schemas in src/novel_creator/records.py and src/novel_creator/validation.py: action accept/reject/correct/revise/reverse/resolve/defer, actual user_message_ref plus precise span, selected/prior/result/affected refs and retained origins; artifact provenance alone never authorizes canon (FR-011–013).
- [ ] T041 [US4] Add deterministic authorization, partial-selection and supersession checks in src/novel_creator/validation.py and src/novel_creator/records.py; require sourced decisions for every canon-affecting element/relationship/assertion, retain prior/current states, exclude superseded facts from current canon, and prevent preferences from waiving protected direction or manuscript safeguards (FR-010–013).
- [X] T042 [US4] Implement direct-dependency impact traversal and revision inspection in src/novel_creator/context.py; expose prior/result refs and all directly linked affected elements without claiming detection of unrecorded dependencies or modifying linked manuscripts (FR-012–013).
- [ ] T043 [US4] Author workflows/authority.md and integrate workflows/brainstorm.md: clear identifiable acceptance/revision needs no repeated approval, ambiguity asks one focused question and protected-direction conflicts require clarification. Implement routine checkpoints on_request (default), session_close and every_exchange with summaries of proposals/decisions/questions and a pause of agent-initiated exploration until user direction; checkpoints never delay saving or reapprove accepted facts (FR-011–013, FR-017).
- [ ] T044 [US4] Execute acceptance/revision journeys in tests/integration/test_canon_journey.py and tests/evaluations/authority-results.md using T039; verify intended selected facts, rejection/alternatives, five revisions with origin/impact/history and unchanged approved manuscript hashes; report agent judgments separately (SC-004, SC-006).
- [X] T045 [US4] Document accepting, correcting, revising/reversing and inspecting canon in README.md with explicit protected-direction and manuscript boundaries; link source/impact examples without implying future drafting exists (FR-026).

**Checkpoint**: Canon transitions have observable authority, source and history.

## Phase 7: US5 — Catch Continuity Problems during Exploration (P1)

**Goal**: Significant conflicts interrupt the next response with evidence;
intentional techniques and unreadable context preserve creative control.
**Independent test**: Prepared conflicts across six categories and recorded lies,
unknown timing and reader revelations exercise all resolution dispositions.

- [ ] T046 [P] [US5] Write perspective/time/hold tests in tests/unit/test_continuity.py for author truth, character knowledge/belief and reader revelation, unknown versus false/absent information, canon mutation holds, deferred conflicts and safe proposal-only continuation (FR-015–018, FR-021).
- [X] T047 [P] [US5] Author sourced six-category contradiction/intentional-technique fixtures in tests/fixtures/en/continuity.json covering motivation, chronology, knowledge, plot dependency, world rules and relationships, with expected next-response intervention and non-blocking opportunities (FR-015–019; SC-005).
- [ ] T048 [US5] Implement assertion/time/finding typed handling against foundation schemas in src/novel_creator/records.py and src/novel_creator/validation.py: perspective author_truth/character_knowledge/character_belief/reader_revelation, required character holder/reader audience, truth_state affirmed/denied/unknown, chronology/revelation precision known/partial/unknown with null unknown bounds, nullable supersedes, finding assessment conflict/uncertainty/opportunity, severity significant/advisory, all dispositions and complete/incomplete/not_applicable review coverage (FR-015–018, FR-021).
- [X] T049 [US5] Implement availability scope, continuity review and hold enforcement in src/novel_creator/context.py and src/novel_creator/validation.py; significant/deferred conflicts block affected promotion, unreadable relevant canon holds affected changes until restoration, unknown scope holds all canon, and unsafe journal predecessors reject all saves (FR-016–018; SC-009).
- [X] T050 [US5] Author workflows/continuity.md and integrate Guardian-before-development in workflows/brainstorm.md; cite sources/consequences, distinguish uncertainty from proven conflict, offer reject/revise/canon-change/intentional/defer resolutions, honor unambiguous revision authorization and keep opportunities non-blocking (FR-015–019).
- [ ] T051 [US5] Execute fault/continuity integration in tests/integration/test_continuity_journey.py using T047 and temporary damaged/restored records; verify affected-canon holds, safe proposal saving, no unsafe-chain append and revalidation before lifting holds (SC-005, SC-009).
- [ ] T052 [US5] Execute real-host continuity evaluation in tests/evaluations/continuity-results.md: every designated significant conflict interrupts conflicting development in the next response, every intentional technique remains distinguishable, resolutions persist and no opportunity becomes canon without acceptance (SC-005).
- [X] T053 [US5] Document resolving/defering contradictions, incomplete checks and restored-context resumption in README.md; state agent-judgment limits and unavailable information explicitly (FR-026).

**Checkpoint**: Core US1–5 loop works with authority-preserving continuity.

## Phase 8: US6 — Retain Language and Platform Independence (P2, release-required)

**Goal**: Full English/Icelandic workflows and independently readable, connected,
versioned story information without Codex or a dashboard.
**Independent test**: Paired language journeys and an independent consumer recover
all designated structured information without interpreting conversation prose.

- [X] T054 [P] [US6] Write Unicode/version/bundle-independence tests in tests/contract/test_portability.py for Icelandic names/characters, mixed language, duplicate names, unknown language-specific assumptions, unsupported schemas and framework-checkout removal (FR-020–025).
- [ ] T055 [P] [US6] Pair English acceptance/continuity fixtures in tests/fixtures/is/acceptance.json and tests/fixtures/is/continuity.json; preserve meanings/source spans, include Icelandic false friends/diacritics and mixed-language examples, and cover setup/guidance/capture/acceptance/continuity with no English-only assumptions (FR-024).
- [X] T056 [US6] Implement languages/is.md and modular language-resource selection in src/novel_creator/context.py and workflows/initialize.md; preserve configured manuscript language, honor interaction-language requests, default to en when unspecified and keep all core schemas genre/language independent (FR-024–025).
- [X] T057 [US6] Document serialized ownership, references, schema readability and explicit future incompatible-migration/recovery requirements in docs/record-format.md; implement unsupported-version errors/holds in src/novel_creator/validation.py, retaining IDs/history and requiring a preserved Git checkpoint before any future migration (FR-022–023).
- [X] T058 [US6] Build an independent consumer in tests/integration/independent_reader.py and tests/integration/test_consumer.py without importing the production reducer; recover every designated entity, relationship, event ordering, perspective/timing, current/history and decision source from committed bundles, including cache deletion and missing/unsupported records (SC-008).
- [ ] T059 [US6] Validate installed-bundle operation after removing framework-path access in tests/integration/test_portable_install.py and run paired language journeys in tests/integration/test_languages.py; verify novel records need neither original agent nor dashboard and T054–055 cases preserve Unicode/meaning (SC-002, SC-008).
- [ ] T060 [US6] Execute/record full English/Icelandic host evaluations in tests/evaluations/language-results.md, reusing T023/T039/T047 expectations and SC-002–007 counts; record host/model/version and separate structural checks, agent judgments and human approvals, marking unsupported/unavailable runs unverified (FR-024, FR-026).
- [X] T061 [US6] Publish portable record/host/language onboarding in README.md and docs/record-format.md, including installed resources, dependencies, no automatic pushes, host voice responsibility and platform-specific support limitations; do not claim untested language or host support (FR-022–026).

**Checkpoint**: US6 is required before release despite P2 delivery order.

## Phase 9: Polish and cross-cutting release verification

- [X] T062 Add representative dataset generation and repeatable benchmarks in tests/performance/benchmark_records.py: 100 sessions, 5,000 exchanges, 10,000 active assertions, 25 MiB JSON, 30 warm read/save runs with p95 read <=2s and validate+local-save <=1s excluding model latency; report cold reads and hardware/OS/Python/Git details in tests/evaluations/performance.md (plan performance targets).
- [X] T063 Optimize only demonstrated bottlenecks in src/novel_creator/context.py and src/novel_creator/storage.py; if caches are needed, label them derived, bind to schema/HEAD, prove deletion/rebuild/staleness handling in tests/integration/test_cache.py and rerun T062 without creating competing authority.
- [ ] T064 Validate installation, JSON CLI, locks, interruption/durability and language fixtures on Linux/Windows in tests/evaluations/platform-results.md; record exact host/OS/filesystem versions and unsupported flush guarantees, and restrict claimed support to verified combinations (FR-014, FR-024–026).
- [ ] T065 Run the full automated suite, existing tests/speckit-smoke.sh and every quickstart.md scenario; record actual commands/results, all Story 1–6 acceptance cases and SC-001–009 outcomes in tests/evaluations/release-readiness.md, keeping unavailable human/host/performance evidence unverified and release-blocking where required.
- [ ] T066 Review constitution 1.0.0 compliance and close coverage/authority/portability gaps in tests/evaluations/release-readiness.md; explicitly preserve future-work boundaries for drafting, dashboard, additional hosts and incompatible migrations, with no implicit waiver of mandatory gates.
- [X] T067 Update README.md and specs/001-novel-initialization-brainstorming/quickstart.md to match verified commands, install prerequisites, recovery and limitations; remove design-time runnable-status disclaimers only for actually delivered/verified behavior, and report remaining unmet release gates honestly.

## Dependencies and execution order

```text
Setup T001–T004
  → Foundation T005–T013 (real host spike blocks full story development)
    → US1 T014–T021 (initial workspace MVP)
    → US2 T022–T028 (prepared brief/session fixtures)
    → US3 T029–T037 (prepared multi-session/canon fixtures)
    → US4 T038–T045 (prepared proposals/canon fixtures)
    → US5 T046–T053 (prepared facts/knowledge/conflict fixtures)
    → US6 T054–T061 (integrates all stories for bilingual/portable release)
      → Cross-cutting T062–T067
```

Arrows after the foundation show recommended serial integration order. Prepared
fixtures let US1–US5 tests run without requiring every other story to be complete.
Production integration dependencies are explicit:

| Work | Prerequisites |
|---|---|
| T003 and T004 | T001–T002; disjoint work can proceed together |
| Foundation | Setup; T005→T006→T007, T008→T009→T010→T011→T012→T013 |
| US1 | Foundation; tests T014/T015 before implementation T016–T020 |
| US2 | Foundation; T022/T023 before T024–T027; prepared brief/session replaces US1 during isolated tests |
| US3 | Foundation schemas already include decisions/assertions; production US2 session behavior T024 before T031–T036; prepared novel fixtures replace US1 |
| US4 | Foundation plus T031 record types for production; foundation assertion/time schemas support prepared idea/canon fixtures that isolate authority tests; T038/T039 before T040–T044 |
| US5 | Foundation plus US4 authorization for production; T046/T047 before T048–T052; shared assertion/time/finding schemas already exist from T006; explicit canon revision semantics reuse T041/T043 |
| US6 | US1–US5 complete; T054/T055 before T056–T060; independent reader does not import product reducer |
| Release | US1–US6 complete; T062→T063→T064→T065→T066→T067 |

No same-file implementation tasks are marked parallel. T063 may be completed
with documented no-change evidence if T062 already meets targets; no speculative
cache implementation. Human and actual-host evaluation tasks cannot be marked
complete from generated fixtures or simulated evaluator results.

## Parallel execution examples

Each pair is eligible only after the phase prerequisites above. These are work
organization examples, not instructions to launch agents in this planning run.

| Story | Independent work example |
|---|---|
| US1 | T014 CLI tests alongside T015 installation tests |
| US2 | T022 mode tests alongside T023 guidance evaluation definitions |
| US3 | T029 context contracts alongside T030 recovery integration tests |
| US4 | T038 transition tests alongside T039 acceptance fixtures |
| US5 | T046 perspective/hold tests alongside T047 continuity fixtures |
| US6 | T054 portability tests alongside T055 Icelandic fixture pairing |

## Requirement and outcome coverage

These mappings describe planned work, not proven compliance.

| Requirement | Task IDs |
|---|---|
| FR-001 | T014, T016, T018–T021 |
| FR-002 | T014, T016, T018–T021 |
| FR-003 | T015–T020 |
| FR-004 | T022, T024–T027 |
| FR-005 | T023, T025–T028 |
| FR-006 | T022–T023, T025–T027 |
| FR-007 | T023, T025–T027, T061 |
| FR-008 | T012, T024, T029, T033, T035–T036 |
| FR-009 | T005–T012, T026, T031–T032, T036 |
| FR-010 | T031–T032, T038–T041, T044 |
| FR-011 | T038–T044 |
| FR-012 | T032, T038–T044 |
| FR-013 | T008–T009, T038–T045 |
| FR-014 | T008–T013, T030, T034, T036–T037, T064 |
| FR-015 | T046–T052 |
| FR-016 | T046–T053 |
| FR-017 | T041, T043, T046–T052 |
| FR-018 | T046–T052 |
| FR-019 | T029, T031, T033, T035, T047, T050–T052 |
| FR-020 | T006–T007, T031, T048, T054, T058–T059 |
| FR-021 | T046, T048–T052, T058 |
| FR-022 | T006–T009, T017, T033, T054, T057–T059, T061 |
| FR-023 | T007, T054, T057–T059 |
| FR-024 | T054–T056, T059–T061, T064 |
| FR-025 | T011–T013, T017, T019, T026, T035, T059, T061 |
| FR-026 | T021, T028, T037, T045, T053, T060–T061, T065–T067 |
| SC-001 | T021, T065 |
| SC-002 | T014, T020, T054–T055, T059–T060, T065 |
| SC-003 | T036, T060, T065 |
| SC-004 | T039, T044, T055, T060, T065 |
| SC-005 | T047, T051–T052, T055, T060, T065 |
| SC-006 | T039, T042, T044, T060, T065 |
| SC-007 | T022–T023, T027–T028, T060, T065 |
| SC-008 | T054, T058–T059, T065 |
| SC-009 | T008–T013, T020, T030, T034, T036, T049, T051, T064–T065 |

## Implementation strategy

First complete setup and the minimal host/persistence capability spike. Deliver
US1 as the initial demonstrable workspace MVP, then add US2/US3 for the usable
brainstorm/save/resume loop, US4 for explicit canon authority, and US5 for
continuity intervention. Treat US1 alone as an incremental demo, not the feature
release. US6 and all required evidence remain mandatory before release.

At each slice checkpoint, run its independent tests and update user instructions.
Preserve source/user data, keep record changes within managed paths, and distinguish
agent judgments from automated invariants and human approvals. Do not implement
a dashboard, drafting engine, additional host adapter or schema migration engine.
After task generation, run `$speckit-analyze` before `$speckit-implement`.


## Phase 10: Convergence

Assessment of the current implementation against spec.md, plan.md, tasks.md and
constitution 1.0.0. Existing task text and completion markers are unchanged.
These tasks make the remaining obligations explicit; reuse the referenced original
tasks and their acceptance tests rather than implementing parallel alternatives.
T012 remains unverified and T013 remains a BLOCKED decision. Complete foundation
remediation and the actual-host gate before dependent story implementation; this
phase does not waive the original prerequisites or permit invented host evidence.
Severity ordering below is review priority, not a replacement dependency order.

Coverage: 26 functional requirements, 9 success criteria, 26 acceptance scenarios,
12 plan decisions and 10 applicable constitution principles; dashboard-specific
Principle X is outside this feature. Findings: 6 missing, 10 partial,
1 contradicts and 0 unrequested; 6 CRITICAL, 9 HIGH and 2 MEDIUM.
Existing structural verification: 41 unittest tests and Bash smoke checks passed
in an isolated installed environment. This is not actual-host or semantic evidence.

- [X] T068 CRITICAL [F1] Bind canon-authorizing decisions in src/novel_creator/validation.py to the current conversation's actual user message, rather than accepting any earlier message resolved from history; add regression coverage in tests/contract/test_exchange.py for replayed prior authorization after a contrary current direction while preserving historical provenance and legitimate unchanged-proposal acceptance. The current validator reproducibly accepts a new canon transition sourced only from an earlier exchange. Complete as foundation remediation of T007 per Constitution III, FR-011, FR-013 and adapters/codex/AGENTS.fragment.md (contradicts).
- [X] T069 CRITICAL [F4] Complete the actual Codex host-capture evaluation in tests/evaluations/host-capture.md and record the resulting gate decision in docs/development.md, including exact save-before-display text, two subsequent automatic turns, genuine fresh-chat recovery, interrupted display, identical retry and visible failure disclosure with real host/model/version and checkpoint evidence; retain BLOCKED/unverified status if evidence is unavailable, and return to adapter planning before any T014+ work. Finish T012 and reassess T013 per FR-009, FR-025, SC-009 and plan: blocking native-host capability spike (partial).
- [ ] T070 CRITICAL [F5] After the host gate passes, deliver the missing initialization slice in src/novel_creator/install.py, src/novel_creator/cli.py, src/novel_creator/validation.py, workflows/initialize.md and adapters/codex/skills/novel-init/SKILL.md, with tests/contract/test_initialize.py and tests/integration/test_install.py plus test_initialize_journey.py; complete T014–T021 for skipped/combined preferences, preserved original brief, stable identity/settings changes, independent pinned installation, existing-content protection and optional brainstorming. The init dispatch currently returns unavailable. Trace to FR-001–003, US1/AC1–5 and SC-002 (missing).
- [ ] T071 CRITICAL [F6] After the host gate passes, deliver shared guidance in workflows/brainstorm.md and languages/en.md, the thin adapters/codex/skills/novel-brainstorm/SKILL.md entry and session-mode behavior in src/novel_creator/records.py; complete T022–T028 with tests/contract/test_guidance.py, tests/integration/test_guidance_journey.py and actual guidance evaluations for guided defaults, next-response switches/redirection, reduced suggestions, accessible constructive coaching and host-provided transcription. These production resources are absent. Trace to FR-004–007, US2/AC1–4 and SC-007 (missing).
- [ ] T072 CRITICAL [F7] After the host gate and prerequisite session behavior pass, implement committed session listing, start/resume/close transitions, focused context and source/history inspection in src/novel_creator/context.py, src/novel_creator/cli.py and src/novel_creator/records.py, with workflows/resume.md and adapters/codex/skills/novel-resume/SKILL.md and novel-inspect/SKILL.md; finish T029, T033, T035–T037 using tests/contract/test_context.py and tests/integration/test_resume_journey.py, proving recovery of 20 ideas, 10 decisions and 5 questions across three sessions and a fresh interaction. Current context/inspect/session-list commands are placeholders. Trace to FR-008, FR-019, FR-022, US3/AC2–3 and SC-003 (missing).
- [ ] T073 CRITICAL [F10] After the original authority prerequisites pass, implement the missing Continuity Guardian workflow in workflows/continuity.md and workflows/brainstorm.md and scope/hold enforcement in src/novel_creator/context.py and src/novel_creator/validation.py; complete T046–T053 with tests/unit/test_continuity.py, six-category fixtures, tests/integration/test_continuity_journey.py and real-host continuity-results.md. Distinguish perspectives, unknown timing, intentional techniques, deferred conflicts and non-blocking opportunities; interrupt conflicting development in the next response, hold affected canon on unreadable context, hold all canon for unknown scope and reject unsafe journal extension. Trace to FR-015–019, FR-021, US5/AC1–5 and SC-005/009 (missing).
- [X] T074 HIGH [F2] Harden committed-history input handling in src/novel_creator/storage.py and CLI error conversion in src/novel_creator/cli.py, with regressions in tests/integration/test_storage.py and tests/contract/test_cli.py for non-object committed JSON and malformed local recovery metadata; a committed exchange containing [] currently raises an uncaught AttributeError. Return one structured unavailable-context/error result with affected scope and no authoritative mutation, rather than a traceback, completing T010's error contract per FR-014, SC-009 and plan: machine-readable CLI boundary (partial).
- [X] T075 HIGH [F3] Preserve the last verifiable journal checkpoint and explicit damaged/unsupported references when committed-history validation fails in src/novel_creator/storage.py, surfacing them through src/novel_creator/cli.py; add tests/integration/test_storage.py and tests/contract/test_cli.py cases with a valid bootstrap followed by a damaged or unsupported successor. The current unsupported-successor probe returns last_confirmed_checkpoint: null despite the valid prefix. Never report the invalid successor as saved or allow unsafe extension. Trace to FR-014, SC-009, T010 and plan: unavailable-context recovery boundary (partial).
- [ ] T076 HIGH [F8] After the original capture prerequisites pass, complete sourced extraction/correction in workflows/brainstorm.md and src/novel_creator/records.py, reusing the existing schemas and reducer; finish T031–T032 and their T036 journey coverage for ideas, characters, plot/world details, relationships, events, alternatives, questions and decisions on every exchange, preserving prior erroneous captures and source/status distinctions. Structural record support alone does not implement automatic capture. Trace to FR-009–010, FR-012 and US3/AC1/4 (partial).
- [ ] T077 HIGH [F9] After the original canon prerequisites pass, complete authority semantics in src/novel_creator/validation.py, src/novel_creator/records.py and src/novel_creator/context.py and shared workflows/authority.md and workflows/brainstorm.md; finish T038–T045 using tests/unit/test_authority.py, acceptance fixtures and tests/integration/test_canon_journey.py. Cover precise partial selection, ambiguous/non-acceptance, revision/reversal with supersession and directly linked impact, explicit-direction clarification and on_request/session_close/every_exchange summaries and pauses without repeated approval or manuscript edits. The foundation checks sources but lacks this full workflow and evidence. Trace to FR-010–013, US4/AC1–5 and SC-004/006 (partial).
- [X] T078 HIGH [F11] After the host gate passes and within the original recovery slice, implement recover inspection and explicit unchanged-payload retry/managed-index cleanup in src/novel_creator/storage.py and src/novel_creator/cli.py, with tests/integration/test_recovery.py; complete T030/T034 for pending/published/cleanup-needed states, lost receipts, stale-lock inspection, original checkpoints, unrelated index/worktree preservation and lifting write pauses only after safe recovery. The command currently returns unavailable and published cleanup can leave writes paused indefinitely. Trace to FR-014, SC-009 and contracts/storage.md recovery requirements (missing).
- [ ] T079 HIGH [F12] After core stories pass, add modular language resources in languages/en.md and languages/is.md and resource selection in src/novel_creator/context.py and workflows/initialize.md; finish T054–T056, T059–T060 with paired tests/fixtures/en/ and tests/fixtures/is/ acceptance/continuity examples, tests/integration/test_languages.py and real bilingual evaluations. Verify setup, guidance, capture, acceptance and continuity, preserved names/meaning and mixed-language requests; Unicode serialization alone is insufficient. Trace to FR-024, US6/AC1, SC-002/004/005/007 and plan: bilingual release requirement (partial).
- [ ] T080 HIGH [F13] Complete independent reconstruction and portability verification in tests/integration/independent_reader.py, tests/integration/test_consumer.py, tests/integration/test_portable_install.py and tests/contract/test_portability.py, with docs/record-format.md covering ownership, references, schema compatibility and future incompatible-migration/recovery guidance; finish T054, T057–T059 and T061. Recover designated entities, event order, perspectives, sources and decision/current/history states without production-reducer imports, conversation re-extraction, framework access or a dashboard. Existing schemas and the disposable installed fixture are only partial evidence. Trace to FR-020–023, US6/AC2–3, SC-008 and plan: independent pinned novel bundle (partial).
- [X] T081 HIGH [F14] Add tests/performance/benchmark_records.py and tests/evaluations/performance.md and complete T062–T063 against 100 sessions, 5,000 exchanges, 10,000 active assertions and 25 MiB JSON with 30 warm read/save runs, documented hardware/OS/Python/Git and separate cold results; meet p95 read <=2s and validate+local-save <=1s excluding model latency. Optimize only observed bottlenecks in src/novel_creator/context.py and src/novel_creator/storage.py; prove derived cache rebuild/staleness behavior if caches are justified. No benchmark or scale evidence exists. Trace to plan: performance goals and scale/scope (missing).
- [ ] T082 HIGH [F15] After the original story and performance prerequisites pass, complete T064–T066 in tests/evaluations/platform-results.md and tests/evaluations/release-readiness.md, recording Linux/Windows installation, JSON CLI, filesystem durability, locks/interruption, bilingual flows, all Story 1–6 acceptance cases and SC-001–009 outcomes; include actual novice initialization/guidance evidence from T021/T028, quickstart scenarios and constitution review. Current evidence covers the structural foundation only. Keep unavailable host/human/platform/performance results explicitly unverified and required unmet gates release-blocking. Trace to FR-026, SC-001–009, Constitution IX/XI and plan: release verification (partial).
- [X] T083 MEDIUM [F16] Align README.md, docs/development.md and specs/001-novel-initialization-brainstorming/quickstart.md with the actually delivered slice and verified setup/usage/recovery commands, completing T067 and the original slice documentation obligations as their features land; immediately distinguish the implemented persistence foundation from unavailable init/session/context/recovery and unverified host support. README.md currently states the framework is unselected despite the Python foundation. Trace to FR-026 and plan: incremental onboarding and support limitations (partial).
- [X] T084 MEDIUM [F17] Add separate expected and actual Git heads to structured stale-write and conditional-publication conflict diagnostics in src/novel_creator/storage.py and src/novel_creator/cli.py, with tests/integration/test_storage.py and tests/contract/test_cli.py regressions preserving pending payload, competing HEAD and unrelated index entries; the current stale-checkpoint error only supplies a generic message. Complete the remaining T009 diagnostic obligation per FR-014 and contracts/storage.md: stale expected parent (partial).


## Phase 11: Convergence

Current-state reassessment after the foundation implementation pass. Checked
26 functional requirements, 9 success criteria, 26 acceptance scenarios,
12 plan decisions and 10 applicable constitution principles; dashboard-specific
Principle X remains outside this feature. All 50 structural tests pass.
T068, T074, T075, T083 and T084 satisfy their assessed foundation obligations
and produce no remaining findings in this pass. Structural results do not prove
semantic correctness, actual-host capture or release readiness.

Remaining findings: 6 missing, 7 partial, 0 contradicts, 0 unrequested;
4 CRITICAL and 9 HIGH. F18 is newly identified: a real held-lock save after a
confirmed bootstrap returns code 6 with both last_confirmed_checkpoint and
pending_exchange_id null. Twelve other gaps remain from the earlier assessment.
F4 is HIGH under the partial-gap severity rule; its mandatory dependency gate
is unchanged. No new constitution contradiction was established.

Carry-forward tasks reference their earlier unchecked task and retain its full
scope and acceptance evidence. They are the same outstanding obligation, not
separate implementations: satisfy and close both task references together.
T090 is foundation remediation that can proceed before the actual-host gate.
T012/T069 and the new T089 remain blocked/unverified; T013 is a stop decision.
All dependent story/release work retains the original execution prerequisites.
This append does not change earlier tasks, markers, specification or plan.

- [ ] T085 CRITICAL [F5] Deliver novel initialization, pinned independent installation and revisable settings in src/novel_creator/install.py, src/novel_creator/cli.py and workflows/initialize.md; fulfill the complete scope, prerequisites and acceptance evidence of T070 per FR-001–003, US1/AC1–5, SC-002 (missing).
- [ ] T086 CRITICAL [F6] Deliver guided/open brainstorming, next-response mode/topic changes and thin host entry in workflows/brainstorm.md, languages/en.md and adapters/codex/skills/novel-brainstorm/SKILL.md; fulfill the complete scope, prerequisites and acceptance evidence of T071 per FR-004–007, US2/AC1–4, SC-007 (missing).
- [ ] T087 CRITICAL [F7] Deliver session lifecycle, committed context, sourced inspection and fresh-chat resumption in src/novel_creator/context.py, src/novel_creator/cli.py and workflows/resume.md; fulfill the complete scope, prerequisites and acceptance evidence of T072 per FR-008, FR-019, FR-022, US3/AC2–3, SC-003 (missing).
- [ ] T088 CRITICAL [F10] Deliver Guardian review, perspective/time distinctions, conflict dispositions and safe availability holds in workflows/continuity.md, src/novel_creator/context.py and src/novel_creator/validation.py; fulfill the complete scope, prerequisites and acceptance evidence of T073 per FR-015–019, FR-021, US5/AC1–5, SC-005/009 (missing).
- [X] T089 HIGH [F4] Obtain genuine automatic-turn, save-before-display, fresh-chat, interruption, identical-retry and failure-disclosure evidence in tests/evaluations/host-capture.md and record the gate decision in docs/development.md; retain BLOCKED and revisit adapter planning when any required evidence is unavailable; fulfill the complete scope, prerequisites and acceptance evidence of T069 per FR-009, FR-025, SC-009, plan: blocking native-host capability spike (partial).
- [X] T090 HIGH [F18] Preserve failure context for a held novel writer lock in src/novel_creator/storage.py and src/novel_creator/cli.py: return the attempted exchange ID and last independently verifiable committed checkpoint when available, without stealing/removing the lock or mutating journal, receipts, HEAD or user index. Add real-repository and JSON CLI regressions in tests/integration/test_storage.py and tests/contract/test_cli.py for a saved bootstrap followed by a held-lock save, plus unborn/unreadable context where no checkpoint can safely be claimed. The current probe returns null for both fields despite a known confirmed save. Treat this as foundation remediation of T010 per FR-014, SC-009 and plan: truthful save-failure disclosure (partial).
- [ ] T091 HIGH [F8] Complete sourced automatic extraction and correction in workflows/brainstorm.md and src/novel_creator/records.py, preserving all required capture kinds, status and prior versions; fulfill the complete scope, prerequisites and acceptance evidence of T076 per FR-009–010, FR-012, US3/AC1/4 (partial).
- [ ] T092 HIGH [F9] Complete precise acceptance, revision/reversal, impact and review-checkpoint behavior in workflows/authority.md, src/novel_creator/validation.py, src/novel_creator/records.py and src/novel_creator/context.py; fulfill the complete scope, prerequisites and acceptance evidence of T077 per FR-010–013, US4/AC1–5, SC-004/006 (partial).
- [X] T093 HIGH [F11] Implement safe pending/published/cleanup-needed inspection and unchanged-payload retry in src/novel_creator/storage.py and src/novel_creator/cli.py with tests/integration/test_recovery.py; fulfill the complete scope, prerequisites and acceptance evidence of T078 per FR-014, SC-009, plan: safe recovery (missing).
- [ ] T094 HIGH [F12] Complete modular English/Icelandic workflow resources, paired fixtures and actual bilingual evaluations in languages/, tests/fixtures/en/, tests/fixtures/is/ and tests/evaluations/language-results.md; fulfill the complete scope, prerequisites and acceptance evidence of T079 per FR-024, US6/AC1, SC-002/004/005/007 (partial).
- [ ] T095 HIGH [F13] Complete independent record reconstruction, installed-bundle portability and compatibility/recovery documentation in tests/integration/independent_reader.py, tests/integration/test_consumer.py, tests/integration/test_portable_install.py and docs/record-format.md; fulfill the complete scope, prerequisites and acceptance evidence of T080 per FR-020–023, US6/AC2–3, SC-008 (partial).
- [X] T096 HIGH [F14] Build and measure the planned representative dataset and p95 read/save targets in tests/performance/benchmark_records.py and tests/evaluations/performance.md, optimizing only demonstrated bottlenecks; fulfill the complete scope, prerequisites and acceptance evidence of T081 per plan: performance goals and scale/scope (missing).
- [ ] T097 HIGH [F15] Complete actual platform, novice, story acceptance and release evidence in tests/evaluations/platform-results.md and tests/evaluations/release-readiness.md, keeping unavailable mandatory results unverified and release-blocking; fulfill the complete scope, prerequisites and acceptance evidence of T082 per FR-026, SC-001–009, Constitution IX/XI (partial).


## Phase 12: Convergence

Assessment: current source and artifacts, 2026-10-21. The implementation ledger
confirms prior implement passes; the actual-host gate remains BLOCKED. Checked
26 functional requirements, 26 acceptance scenarios, nine success criteria,
eight edge-case groups and 12 plan decisions. Reviewed all 11 constitution
principles, with dashboard-specific obligations deferred by the feature scope.
Findings: six missing, eight partial; four CRITICAL, nine HIGH, one MEDIUM;
no separate contradicts or unrequested findings.

Current verification: 18 digest/exchange-contract tests passed. An isolated
Windows probe of storage.sync_index (Git interactions mocked, disposable file)
reproduced OSError errno 9 at the read-only index-lock fsync; a descriptor probe
failed with rb and succeeded with r+b. This establishes the descriptor issue,
not end-to-end recovery correctness. The retained Windows preflight reports
52 tests with eight failures and one symlink-privilege error; those are prior
recorded results, not a fresh full-suite run. This session's default sandbox
temp-file probe was denied; no new real-Git integration pass is claimed.

Execution order differs from severity order: remediate the foundation with
T102 and T111 first, then complete T103's actual-host gate. Do not begin dependent
story work until T012/T013 genuinely pass. Existing pending T085-T089 and
T091-T097 remain unsatisfied; the corresponding tasks below carry forward their
complete original scope, prerequisites and acceptance evidence. Do not count
repeated descriptions as separate product requirements. Preserve the retained
host-test fixture, history and receipts; do not repair it manually or reuse it
to manufacture a passing evaluation. Future slice documentation remains part
of its original task scope even where the foundation-only T083 is checked.

- [ ] T098 CRITICAL [F1] Deliver novel initialization, pinned independent installation and revisable settings in src/novel_creator/install.py, src/novel_creator/cli.py, workflows/initialize.md and adapters/codex/skills/novel-init/SKILL.md after the actual-host gate passes; complete the full original T070/T085 scope, tests and onboarding, including skipped/combined preferences, original brief provenance, stable identity, existing-content preservation and optional brainstorming per FR-001-003, US1/AC1-5 and SC-002 (missing).
- [ ] T099 CRITICAL [F2] Deliver guided/open brainstorming, next-response mode/topic changes, reduced suggestions and thin native-host entry in workflows/brainstorm.md, languages/en.md, src/novel_creator/records.py and adapters/codex/skills/novel-brainstorm/SKILL.md after the actual-host gate passes; complete the full T071/T086 scope and guidance evidence, including accessible constructive coaching and host-provided transcription per FR-004-007, US2/AC1-4 and SC-007 (missing).
- [ ] T100 CRITICAL [F3] Deliver session listing/start/resume/close, focused committed context and sourced history/connection inspection in src/novel_creator/context.py, src/novel_creator/cli.py, src/novel_creator/records.py, workflows/resume.md and the resume/inspect adapters after their original prerequisites pass; complete T072/T087 and prove recovery of 20 ideas, 10 decisions and five questions across three sessions and a genuine fresh interaction per FR-008, FR-019, FR-022, US3/AC2-3 and SC-003 (missing).
- [ ] T101 CRITICAL [F4] Deliver Guardian-before-development review in workflows/continuity.md and workflows/brainstorm.md, with scope/hold enforcement in src/novel_creator/context.py and src/novel_creator/validation.py after the original authority prerequisites pass; complete T073/T088, six-category fixtures and real-host evidence for perspective/time distinctions, intentional techniques, dispositions, deferred conflicts, unavailable-context holds and non-blocking opportunities per FR-015-019, FR-021, US5/AC1-5 and SC-005/009 (missing).
- [X] T102 HIGH [F5] Repair Windows managed-index synchronization in src/novel_creator/storage.py as foundation remediation of T009 before repeating the host spike: storage.sync_index opens index.lock with rb immediately before os.fsync, and the isolated current Windows probe raises errno 9 for that descriptor while r+b succeeds. Select a supported flush/access strategy without weakening truthful saved/cleanup_required results, index locking, unrelated staged/worktree preservation or publication boundaries. Add a focused regression in tests/integration/test_storage.py and verify clean bootstrap, continuation, identical retry and lost-receipt behavior through tests/contract/test_cli.py and tests/integration/test_host_fixture.py on a new disposable canonical Windows path. Reassess the retained checkpoint-test failures after fixing cleanup, investigating any residual failure rather than assuming a common cause; record actual results in tests/evaluations/platform-results.md and docs/development.md per FR-014, SC-009, T008-010 and plan: Windows local-Git transaction support (partial).
- [X] T103 HIGH [F6] Complete the actual Codex save-before-display capability evaluation in tests/evaluations/host-capture.md and record the gate decision in docs/development.md only after foundation preflight is clean; fulfill T069/T089 with exact visible messages, automatic subsequent turns, fresh-chat recovery, display interruption, unchanged retry and visible failure disclosure, real host/model/version and checkpoint evidence. Keep BLOCKED/unverified and revisit adapter planning whenever required evidence is unavailable; structural tests and the isolated Windows descriptor probe do not pass this gate per FR-009, FR-025, SC-009 and plan: blocking native-host capability spike (partial).
- [ ] T104 HIGH [F7] Complete sourced automatic extraction and correction in workflows/brainstorm.md and src/novel_creator/records.py after the original capture prerequisites pass; fulfill T076/T091 for every required capture kind, statuses, alternatives, retained prior erroneous versions and sources, with complete journey evidence rather than schema-only claims per FR-009-010, FR-012 and US3/AC1/4 (partial).
- [ ] T105 HIGH [F8] Complete precise partial acceptance/non-acceptance, revision/reversal, supersession, direct impact traversal and routine checkpoint summaries/pauses in workflows/authority.md, workflows/brainstorm.md, src/novel_creator/validation.py, src/novel_creator/records.py and src/novel_creator/context.py; fulfill T077/T092 and their complete test/evaluation scope after original prerequisites pass, retaining current-user authorization, no redundant approval and approved-manuscript protection per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [X] T106 HIGH [F9] Implement safe pending/published/cleanup-needed recovery inspection and explicit unchanged-payload retry in src/novel_creator/storage.py and src/novel_creator/cli.py with tests/integration/test_recovery.py after the original gate/prerequisites pass; fulfill T078/T093 including lost receipts, stale-lock inspection, original checkpoints, unrelated index/worktree preservation and lifting pauses only after verified cleanup, without replaying decisions or resetting refs per FR-014, SC-009 and plan: safe recovery (missing).
- [ ] T107 HIGH [F10] Complete modular English/Icelandic resources and selection in languages/en.md, languages/is.md, workflows/initialize.md and src/novel_creator/context.py, paired fixtures and actual bilingual evaluations after core prerequisites pass; fulfill T079/T094 for setup, guidance, capture, acceptance and continuity, preserved names/meaning and mixed-language requests in tests/fixtures/en/, tests/fixtures/is/, tests/integration/test_languages.py and tests/evaluations/language-results.md per FR-024, US6/AC1 and SC-002/004/005/007 (partial).
- [ ] T108 HIGH [F11] Complete independent record reconstruction, installed-bundle portability and compatibility/recovery documentation in tests/integration/independent_reader.py, tests/integration/test_consumer.py, tests/integration/test_portable_install.py, tests/contract/test_portability.py and docs/record-format.md; fulfill T080/T095 after original prerequisites pass, recovering all designated entities, relationships, event order, perspectives, sources and current/history decisions without production-reducer imports, conversation re-extraction, framework access or a dashboard per FR-020-023, US6/AC2-3 and SC-008 (partial).
- [X] T109 HIGH [F12] Build the planned representative dataset and measure 30 warm p95 read/save runs in tests/performance/benchmark_records.py and tests/evaluations/performance.md after the original prerequisites pass; fulfill T081/T096 for 100 sessions, 5,000 exchanges, 10,000 active assertions and 25 MiB JSON, documented hardware/OS/Python/Git, separate cold results, read <=2s and validate/local-save <=1s excluding model latency; optimize only demonstrated bottlenecks and prove any justified derived-cache rebuild/staleness behavior per plan: performance goals and scale/scope (missing).
- [ ] T110 HIGH [F13] Complete actual platform, novice, story acceptance, onboarding and release verification in tests/evaluations/platform-results.md, tests/evaluations/release-readiness.md, README.md and specs/001-novel-initialization-brainstorming/quickstart.md as the original slices land; fulfill T082/T097 and remaining T067 documentation obligations, including all story/SC cases, quickstart, Bash smoke, five-novice evidence, applicable durability and constitution review after their prerequisites pass. Keep unavailable mandatory host/human/language/performance/platform evidence unverified and release-blocking per FR-026, SC-001-009, Constitution IX/XI and plan: verified incremental onboarding/release (partial).
- [X] T111 MEDIUM [F14] Make foundation-test filesystem prerequisites portable in tests/helpers.py and tests/integration/test_storage.py, documenting invocation and limitations in docs/development.md: use canonical disposable paths compatible with root_path without weakening production traversal/symlink rejection; capability-check real symlink creation so Windows WinError 1314 is explicitly reported as unavailable coverage, retaining meaningful rejection coverage where supported. Verify focused and full test commands on the claimed environments, distinguish sandbox access failures from product failures, and do not mark skipped privilege/durability exercises passing per T003, T008, T064, FR-026 and plan: Linux/macOS/Windows verification (partial).


Implementation assessment (2026-10-21, actual spike-02): T103 remains unchecked.
B/C/D/E/F have real user-driven evidence; remaining A fidelity work is to establish
the native current-user-message boundary and resolve the extra terminal LF in
native public readback versus all eight stored user messages. Preserve intentional
line breaks; prove any host-only delimiter convention rather than normalizing it
away. Also retain the scoped-filesystem-approval limitation. See
../../tests/evaluations/host-capture-runs/20261021T161928Z-spike-02/README.md.
The user completed the requested hands-on checks; do not ask to repeat the Stop
exercise without a new evidence-based need. No task or dependent-story gate is
marked passed by these partial results.


## Phase 13: Convergence

Assessment: current implementation and actual spike-02 evidence, 2026-10-21.
Checked 26 functional requirements, 26 acceptance scenarios, nine success
criteria, eight edge-case groups, 12 plan decisions and 11 constitution
principles; dashboard-specific obligations remain deferred by this feature.
Findings: six missing, six partial; four CRITICAL and eight HIGH. No separate
contradicts or unrequested finding was established. T102/T111 are satisfied
and are not carried forward. The recorded final foundation run was 54 tests,
53 passed and one explicit Windows symlink-privilege skip; this assessment did
not rerun the suite or claim fresh integration verification.

The user completed the requested hands-on host exercises. B/C/D/E/F evidence,
seven exact displayed assistant replies and the saved-but-undisplayed response
are retained in tests/evaluations/host-capture-runs/20261021T161928Z-spike-02/.
The remaining gate issue is the terminal-LF difference between native public
user-message readback and all eight stored user messages. Its origin remains
unestablished; do not call it proven storage corruption or silently normalize it
away. Scoped normal-access retries were required after sandbox hard-link denial.
T012/T013 must genuinely pass before dependent story work begins. Resolve T116
first; do not repeat the human Stop exercise without a new evidence-based need.
Existing pending tasks retain their full scope and dependencies; carry-forward
items below do not introduce duplicate product requirements.

- [ ] T112 CRITICAL [F1] Deliver initialization, pinned independent installation and revisable settings in src/novel_creator/install.py, src/novel_creator/cli.py, workflows/initialize.md and adapters/codex/skills/novel-init/SKILL.md after the actual-host gate passes; fulfill the full T098/T070 scope, prerequisites, tests and onboarding for skipped/combined preferences, original brief provenance, stable identity, content protection and optional brainstorming per FR-001-003, US1/AC1-5 and SC-002 (missing).
- [ ] T113 CRITICAL [F2] Deliver shared guided/open brainstorming, next-response mode/topic changes, reduced suggestions, accessible coaching and native host entry in workflows/brainstorm.md, languages/en.md, src/novel_creator/records.py and adapters/codex/skills/novel-brainstorm/SKILL.md after the original gate/prerequisites pass; fulfill T099/T071 and all guidance/transcription evidence per FR-004-007, US2/AC1-4 and SC-007 (missing).
- [ ] T114 CRITICAL [F3] Deliver committed session listing/start/resume/close, focused context and sourced inspection in src/novel_creator/context.py, src/novel_creator/cli.py, src/novel_creator/records.py, workflows/resume.md and resume/inspect adapters after the original prerequisites pass; fulfill T100/T072, including production recovery of 20 ideas, 10 decisions and five questions across three sessions and a fresh interaction per FR-008, FR-019, FR-022, US3/AC2-3 and SC-003 (missing).
- [ ] T115 CRITICAL [F4] Deliver Guardian-before-development review, perspective/time distinctions, conflict dispositions and availability holds in workflows/continuity.md, workflows/brainstorm.md, src/novel_creator/context.py and src/novel_creator/validation.py after original authority prerequisites pass; fulfill T101/T073 with six-category fixtures, unreadable-context/deferred-conflict enforcement and actual semantic evaluations per FR-015-019, FR-021, US5/AC1-5 and SC-005/009 (missing).
- [X] T116 HIGH [F5] Resolve the native user-message boundary and complete the remaining actual-host gate in adapters/codex/AGENTS.fragment.md, tests/fixtures/host-spike/, tests/integration/test_host_fixture.py, tests/evaluations/host-capture.md and docs/development.md: establish why native public user readback has one terminal LF absent from all eight saved messages, preserve exact intentional leading/trailing line breaks, add regression coverage and obtain a focused actual-host parity comparison. Prove any host-only delimiter convention with authoritative host evidence before excluding it; never silently strip whitespace, rewrite saved exchanges or regenerate prior IDs. Retain the successful spike-02 B/C/D/E/F and exact-assistant evidence and document the scoped-filesystem-approval limitation; repeat only cases invalidated by an adapter change. Finish T103/T069 and reassess T012/T013 without waiving the blocking spike or requiring an unsupported custom runtime per FR-009, FR-014, FR-025, SC-009 and plan: exact visible native-host capture (partial).
- [ ] T117 HIGH [F6] Complete automatic sourced extraction and corrections in workflows/brainstorm.md and src/novel_creator/records.py after original capture prerequisites pass; fulfill T104/T076 for every required capture kind, states, alternatives, retained prior versions and provenance with complete journey evidence per FR-009-010, FR-012 and US3/AC1/4 (partial).
- [ ] T118 HIGH [F7] Complete precise acceptance/non-acceptance, partial selection, revisions/reversals, supersession, direct impact and routine checkpoint summaries/pauses in workflows/authority.md, workflows/brainstorm.md, src/novel_creator/validation.py, src/novel_creator/records.py and src/novel_creator/context.py; fulfill T105/T077 after original prerequisites pass, retaining current-user authorization and manuscript boundaries per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [X] T119 HIGH [F8] Implement safe pending/published/cleanup-needed inspection and explicit unchanged-payload retry in src/novel_creator/storage.py and src/novel_creator/cli.py with tests/integration/test_recovery.py after original prerequisites pass; fulfill T106/T078 for stale locks, lost receipts, original checkpoints, unrelated index/worktree protection and verified pause lifting without decision replay or ref reset per FR-014, SC-009 and plan: safe recovery (missing).
- [ ] T120 HIGH [F9] Complete modular English/Icelandic resources, resource selection, paired fixtures and actual language evaluations in languages/, workflows/initialize.md, src/novel_creator/context.py, tests/fixtures/en/, tests/fixtures/is/, tests/integration/test_languages.py and tests/evaluations/language-results.md after core prerequisites pass; fulfill T107/T079 for setup, guidance, capture, authority, continuity, preserved names/meaning and mixed-language requests per FR-024, US6/AC1 and SC-002/004/005/007 (partial).
- [ ] T121 HIGH [F10] Complete independent reconstruction, installed-bundle portability and record compatibility/recovery documentation in tests/integration/independent_reader.py, tests/integration/test_consumer.py, tests/integration/test_portable_install.py, tests/contract/test_portability.py and docs/record-format.md after original prerequisites pass; fulfill T108/T080 without production-reducer imports, conversation re-extraction, framework access or a dashboard per FR-020-023, US6/AC2-3 and SC-008 (partial).
- [X] T122 HIGH [F11] Build and measure the representative dataset in tests/performance/benchmark_records.py and tests/evaluations/performance.md after original prerequisites pass; fulfill T109/T081 for 100 sessions, 5,000 exchanges, 10,000 active assertions, 25 MiB JSON, 30 warm runs, p95 read <=2s and validate/local-save <=1s excluding model latency, documented hardware/versions and separate cold results; optimize only demonstrated bottlenecks and verify any justified derived cache per plan: performance goals and scale/scope (missing).
- [ ] T123 HIGH [F12] Complete actual platform, novice, story acceptance, onboarding and release evidence in tests/evaluations/platform-results.md, tests/evaluations/release-readiness.md, README.md and specs/001-novel-initialization-brainstorming/quickstart.md after original prerequisites pass; fulfill T110/T082 and remaining T067 obligations, retaining successful foundation/host evidence while leaving unavailable mandatory results unverified and release-blocking per FR-026, SC-001-009, Constitution IX/XI and plan: incremental verified release (partial).


T116 implementation update (2026-10-21): native --user-message-file preparation
and revised Desktop source instructions are implemented; installed exact-text
regressions pass. Full suite: 54 passed, one explicit privilege skip. Fresh
spike-03 is prepared for one focused actual-host parity check. T116/T103 remain
unchecked until that check is supported; successful spike-02 B/C/D/E/F are retained.
See ../../tests/evaluations/native-message-input.md. No dependent story gate is waived.


Final gate assessment (2026-10-21, spike-03): T012/T069/T089/T103/T116 completed;
T013 latest decision PASS. Native source, payload and saved user text are exact,
including terminal LF; saved assistant text equals displayed final and successful
save precedes display. Retained spike-02 evidence covers automatic subsequent
turns, interruption, fresh-chat recovery, failure disclosure and unchanged retry.
Scope requires native tools, single typed text and scoped filesystem approval
when sandbox hard-link publication is denied. No dependent story checkbox is
changed. Full final suite: 55 tests, 54 passed, one symlink-privilege skip, exit 0.
See ../../tests/evaluations/host-capture-runs/20261021T171237Z-spike-03/README.md.


## Implementation continuation after T103 — 2026-10-21

Newly completed: T014–T020, T022–T026, T029–T030, T033–T035, T037, T039,
T042, T045, T047, T049–T050, T053, T056–T057, T061, T067 and the equivalent
recovery obligations T078/T093/T106/T119. Checkboxes represent only their
recorded scope; broader convergence tasks remain open when they include unmet
human/actual-host/semantic/performance evidence.

Implemented standalone pinned init, original brief provenance/unknowns/settings,
session lifecycle helpers, committed context/list/inspect/validate, explicit
unchanged recovery and safe published cleanup. Shared guidance/authority/
continuity workflows, four Codex entries and English/Icelandic resources are
installed. Added partial-selection/supersession/finding/time checks, source-backed
direct impact and checkpoint summaries. Independent-reader and isolated-bundle
journeys provide additional structural portability evidence.

Final suite: 90 tests in 304.636s; 89 passed, one explicit Windows symlink-privilege
skip; no errors/failures, exit 0. See ../../tests/evaluations/windows-story-final-tests.txt.
Prepared acceptance/continuity expectations are not executed literary judgments.
T021/T027/T028/T036/T044/T052/T060 and broad convergence tasks retain their
missing real-host/human/semantic requirements. The full consumer/version matrix,
performance and cross-platform/release checks also remain incomplete.
See ../../tests/evaluations/release-readiness.md for the evidence boundary.


## Phase 14: Convergence

Current-state assessment, 2026-10-21, after the recorded story implementation
continuation. Checked 26 functional requirements, 26 acceptance scenarios, nine
success criteria, eight edge-case groups, 12 plan decisions and 10 applicable
constitution principles; dashboard-specific Principle X remains outside scope.
The scoped native-host capture gate remains passed. Initialization, sessions,
recovery, shared authority/continuity workflows, language resources and the
independent reader now exist; earlier missing-code descriptions are historical.

Fresh verification: 25 authority/continuity/digest/exchange-contract tests passed
using `.venv/Scripts/python.exe -B -m unittest tests.unit.test_authority
tests.unit.test_continuity tests.unit.test_digest tests.contract.test_exchange -v`.
A separate in-memory production-validator probe reproduced F1: the unchanged
prior deferred significant conflict rejects promotion, but revising only its
severity to advisory, assessment to uncertainty, or affected_refs to the finding
itself permits the same promotion without a conflict-resolution decision.
The finding remains deferred in all three accepted cases. No novel or application
code was changed by these probes. No fresh full-suite, host, human, performance
or platform evaluation is claimed.

Findings: one contradicts, eight partial, one missing, zero unrequested;
one CRITICAL and nine HIGH. Carry-forward tasks describe only remaining work,
retain original prerequisites and refer to earlier open obligations rather than
requiring duplicate implementations. Existing checkboxes remain unchanged.

- [X] T124 CRITICAL [F1] Prevent unauthorized weakening or retargeting of existing open/deferred significant conflict holds in src/novel_creator/validation.py. Compute protection from the prior committed finding as well as its proposed revision, and require a sourced current user disposition authorizing any change that releases held canon; changing severity, assessment or affected_refs alone must not bypass it. Add regressions in tests/unit/test_continuity.py and tests/integration/test_continuity_journey.py for all three reproduced bypasses, unchanged authoritative state on rejection and legitimate user-directed resolutions/revisions without redundant approval. Complete the hold-enforcement portion of T115 per Constitution III/IV, FR-016-017, US5/AC2 and SC-009 (contradicts).
- [ ] T125 HIGH [F2] Complete the remaining initialization evaluation scope of T021/T112 in tests/evaluations/novice-initialization.md and tests/evaluations/release-readiness.md: observe five actual novices starting without a concept, skipping unknowns and reaching the optional brainstorming invitation, with at least four finishing unaided within ten minutes; check actual conversational combined-answer handling and preserved supplied meaning on reopening, coordinating paired-language evidence with T130. Preserve delivered initialization and stable-identity tests; do not recreate the slice or fabricate evaluator observations per FR-001-003, US1/AC1-5 and SC-001-002 (partial).
- [ ] T126 HIGH [F3] Execute the remaining G01-G12 product-host guidance cases and five-novice guidance evaluation in tests/evaluations/guidance-results.md and tests/evaluations/novice-guidance.md, completing T027/T028 and the remaining T113 scope. Record actual next-response guided/open switches, topic redirection, reduced suggestions, accessible constructive coaching, preference adaptation and supported host-transcription behavior; obtain at least four of five novice ratings >=4/5 for usefulness and creative control. Repair workflows/brainstorm.md or thin adapters only where observed failures require it per FR-004-007, US2/AC1-4 and SC-007 (partial).
- [ ] T127 HIGH [F4] Complete the remaining T031/T032/T036/T114/T117 automatic-capture and resumption evidence in tests/integration/test_resume_journey.py and tests/evaluations/resume-results.md using ordinary product-host conversation, including a genuine fresh interaction. Verify every required capture kind, alternatives/states/sources, correction with retained prior versions, and recovery of all 20 designated ideas, 10 decisions and five questions across three sessions without manual note-taking; preserve structural installed-reader coverage and distinguish it from host extraction judgment. Fix only observed workflow/capture gaps per FR-008-012, US3/AC1-4 and SC-003 (partial).
- [ ] T128 HIGH [F5] Complete the remaining T038/T040/T041/T043/T044/T118 authority coverage in tests/unit/test_authority.py, tests/integration/test_canon_journey.py and tests/evaluations/authority-results.md. Execute the actual semantic acceptance/non-acceptance set, partial selection, correction/revision/reversal, explicit-direction conflict clarification and all routine-checkpoint summary/pause modes; retain five-revision history/direct-impact and manuscript-preservation evidence. Coordinate bilingual cases with T130, record actual responses and saved states, and remedy observed gaps without repeated approval of clear authorized facts per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [ ] T129 HIGH [F6] Complete the remaining T046/T048/T051/T052/T115 continuity coverage in tests/unit/test_continuity.py, tests/integration/test_continuity_journey.py and tests/evaluations/continuity-results.md after T124. Execute actual product-host judgments for all six conflict categories, intentional mysteries/lies/unreliable viewpoints, uncertain conflicts and sourced non-blocking opportunities; verify next-response interruption, all user dispositions, deferred-state persistence, safe proposal exploration and revalidation before lifting unavailable-context holds. Record responses, sources, checkpoints and limits separately from structural checks per FR-015-019/021, US5/AC1-5 and SC-005/009 (partial).
- [ ] T130 HIGH [F7] Complete the remaining T054/T055/T059/T060/T120 bilingual coverage in tests/fixtures/en/, tests/fixtures/is/, tests/integration/test_languages.py and tests/evaluations/language-results.md. Review paired meanings, source spans, Icelandic false friends/diacritics and mixed-language cases, then run setup, guidance, automatic capture, acceptance, revisions and continuity through actual product-host workflows in both languages. Reuse T125-T129 evidence where applicable, record host/model/version and distinguish structural checks, agent judgments and human review; repair observed semantic gaps without treating Unicode round trips as parity per FR-024, US6/AC1 and SC-002/004/005/007 (partial).
- [X] T131 HIGH [F8] Finish the representative independent-consumer and portability matrix remaining in T054/T058/T059/T121 using tests/contract/test_portability.py, tests/integration/independent_reader.py, tests/integration/test_consumer.py and tests/integration/test_portable_install.py. Cover every designated entity/relationship, event order, all knowledge/timing distinctions, current and superseded history and decision origins, duplicate-name/rename identity, cache deletion, missing/damaged/unsupported records and operation without framework-path access. Retain the independent reader and isolated interpreter tests already delivered; align docs/record-format.md only if observed gaps require it per FR-020-023, US6/AC2-3 and SC-008 (partial).
- [X] T132 HIGH [F9] Implement tests/performance/benchmark_records.py and record tests/evaluations/performance.md to finish T062/T063/T122: generate 100 sessions, 5,000 exchanges, 10,000 active assertions and 25 MiB JSON, measure 30 warm read and validation/local-save runs, report p95 read <=2s and validation/local-save <=1s with separate cold results and hardware/OS/Python/Git details, excluding model latency. Optimize only demonstrated bottlenecks in src/novel_creator/context.py or src/novel_creator/storage.py; if a cache is justified, verify its derived authority, deletion/rebuild and staleness behavior per plan: performance goals and scale/scope (missing).
- [ ] T133 HIGH [F10] Complete the remaining T064-T066/T123 platform and release verification in tests/evaluations/platform-results.md and tests/evaluations/release-readiness.md after story/performance prerequisites pass: run Linux/Windows installation, JSON CLI, locks/interruption and applicable filesystem guarantees, the full automated suite, tests/speckit-smoke.sh with its prerequisites and all quickstart scenarios. Reconcile evidence for all story acceptance cases and SC-001-009, review all applicable constitution obligations and update onboarding/support claims only to verified scope. Retain the scoped capture-gate pass and existing structural results; keep missing human/host/language/performance/platform evidence explicitly unverified and release-blocking per FR-026, SC-001-009, Constitution IX/XI and plan: release verification (partial).


## Performance continuation — 2026-10-21

T062/T063/T081/T096/T109/T122/T132 are complete against the documented
Ubuntu 24.04.4/WSL2/ext4 reference configuration: 100 sessions, 5,000 exchanges,
10,000 active assertions, 26,215,716 JSON bytes, all 30 warm runs; read p95
0.826192151s and validation/local-save p95 0.982377050s. Both reference targets
pass with the optional authenticated validation proof cache and explicitly
configured temporary key outside the novel. Cold full read: 1.615959638s.
See ../../tests/evaluations/linux-performance-trusted-cache-30.json and
../../tests/evaluations/performance-reference-hardware.json.

Measured bottlenecks were removed through incremental validation, batched Git
reads/hashes, compiled schema checks and less redundant path processing. Optional
cache proofs bind HEAD/journal/schema/runtime and source object hashes, contain
no story records and cannot authorize new exchanges. Explicit runtime keys are
read-only and outside the novel; novel-supplied keys are rejected. Deletion,
rebuild, forgery, stale schemas/HEAD and source corruption are tested. The full
Linux suite passes 112 tests (final rerun: 21.138s), with Bash smoke passing as well.

These checkmarks establish the planned reference measurement, not universal
Windows/macOS latency. Windows limits are reported separately; macOS, actual
product-host creative/bilingual runs and five-novice observations remain open
under T125-T130/T133 and their original task references. No release gate is
waived. Earlier timeout and unmet-target assessments describe their own runs.


## Platform scope decision — 2026-10-21

The user deferred macOS support from the current release. T064/T082/T133 now
require Linux and Windows verification; macOS is outside the current release
gate and is neither tested nor claimed supported. Earlier macOS gate references
are historical and superseded by this decision. Remaining host, novice, bilingual,
Windows performance and release obligations are unchanged.

## Independent continuation — 2026-10-21

Added the structural installed-command portion of T027 in
tests/integration/test_guidance_journey.py: four saved turns preserve exact
messages, guided/open/guided changes, topic redirection, reduced-suggestion
preferences, prior proposals and current-message sources. Each context read uses
a fresh installed CLI process and matches the save checkpoint. Prepared replies
are test data; actual G01-G12 responses, display behavior and coaching judgments
remain unverified. T027/T071/T113/T126 remain unchecked because their complete
acceptance scope has not been met.

The user confirmed that novice observations are not available and requested
continued independent work. T021/T028/T125/T126 retain the five-person evidence
requirements. Current quickstart/release instructions now consistently exclude
deferred macOS support. No checklist markers or acceptance thresholds changed.

Fresh verification: Linux/WSL2 full suite 113/113 passed in 39.578s; Windows full
suite 112 passed plus one explicit symlink-privilege skip in 295.635s, zero
failures/errors. Git Bash smoke and whitespace checks pass. Full commands, logs
and remaining release boundaries are recorded in
../../tests/evaluations/release-readiness.md. No original task is newly marked
complete from this partial coverage, and no extension hooks are registered.

## Post-push bilingual continuation — 2026-10-21

The user authorized committing and pushing the pending implementation to main,
then continued work. Commit 50c035b was pushed and its full SHA matched the remote.
Subsequent local work adds eight paired language-pitfall cases for T055/T130 and
fixture-integrity contracts in tests/contract/test_language_fixtures.py. Corrected
two brass/copper translation mismatches in Icelandic A07/O01, including A07's
Unicode source range. The new corpus covers setup/guidance/capture/acceptance/
continuity, false friends, mixed language, diacritics, partial selection, quoted
dialogue and negation. Six fixture/portability contracts pass on each of Windows
and Linux/WSL2; git diff --check passes for the continuation.

These are authored inputs and structural checks plus a limited agent review,
not actual host judgments or human bilingual approval. T055/T060/T130 and the
other real-host/novice gates remain unchecked. See tests/evaluations/language-results.md
for input links, commands/results and evidence limits. No production code,
dependency, schema, checklist marker or acceptance threshold changed.

## Windows save performance continuation — 2026-10-21

The bilingual fixture work was committed/pushed to main as bd9f475 under the
user's explicit instruction. Subsequent performance changes remain local.
Fresh profiling on the representative dataset identified repeated Git metadata
reads and shared-directory path checks. A Git transport experiment did not show
consistent benefit and was discarded. The retained storage change checks shared
directories once within each guard pass, checks every file leaf and hashes every
file's bytes on both passes, reuses the initial immutable tree for the second
guard and the verified candidate tree for index cleanup. No path checks are
cached across passes/saves, and live-index checks are unchanged.

Five alternating old/new samples give save medians of 3.705116s and 3.173141s
(14.36% lower). The canonical 30-read/30-save Windows run completes without
operation errors/timeouts: cold read 3.070803300s, read p95 1.597038600s (PASS),
save p95 3.845654300s (UNMET, target still 1s, benchmark exit 1). The older
6.771s p95 is retained as historical evidence and is not a controlled baseline
for attributing all gains to this change. T133 remains unchecked; no release
gate or original task is newly completed from this partial improvement.

New regressions cover same-size/same-timestamp byte changes after candidate
construction for SHA-1/SHA-256 and fresh shared-directory symlink checks on
successive guard passes. Full Linux/WSL2 verification passes 118 tests, zero
skips. Windows results, raw timings, experimental limits and exact commands are
recorded in ../../tests/evaluations/windows-save-optimization.md. Dependencies,
schemas, transaction/authority rules and checklist markers are unchanged.

Final verification: Linux full suite 118 passed in 51.548s, zero skips; Windows
full suite 116 passed plus two explicit real-symlink privilege skips in 303.150s,
zero failures/errors, exit 0. Both real-symlink cases pass on Linux. Whitespace
checks pass and no extension hooks are registered. The local performance change
remains uncommitted/unpushed; bd9f475 remains the pushed main checkpoint.


## Phase 15: Convergence

Assessment date: 2026-10-21. Intent: spec.md, plan.md, tasks.md and constitution
1.0.0. Implementation has run on this task list. This assessment inspects the
present files without a branch/history comparison. Existing task markers and
prior convergence phases remain unchanged; carry-forward items below describe
only their remaining scope, not a request to rebuild delivered capabilities.

Coverage: 26 functional requirements, nine success criteria, 26 user-story
acceptance scenarios, eight edge cases, ten plan obligations and all eleven
constitution principles. Dashboard delivery under principle X is outside this
feature. No post-launch business metrics were added. Nine findings: eight
partial, one contradicts, zero missing/unrequested; all HIGH. No new deterministic
constitution/safety contradiction was reproduced in the inspected validators.

Fresh read-only checks: `.venv/Scripts/python.exe -B -m unittest
 tests.unit.test_continuity tests.unit.test_authority tests.contract.test_exchange
 tests.contract.test_language_fixtures tests.contract.test_portability -q`
with PYTHONDONTWRITEBYTECODE=1 and PYTHONUTF8=1: 29 tests passed in 0.082s,
zero skips. This checks the existing validators/fixtures, not host creative
judgment or human approval. Broader integration/platform results were inspected
as recorded evidence and were not rerun for this assessment. The scoped native
capture gate and T124/T131 structural results remain retained. The recorded
Windows 30-run save p95 is 3.845654300s against 1s; it was not remeasured.
macOS remains deferred under the current plan. No extension hooks are registered.

- [ ] T134 HIGH [F1] Complete only the outstanding T125/T021/T112 initialization evaluation in tests/evaluations/novice-initialization.md and tests/evaluations/release-readiness.md: collect five actual novice no-concept journeys, record skipped unknowns, assistance, elapsed times, displayed optional invitation and saved checkpoints, and require at least four unaided completions within ten minutes. Verify actual combined-answer handling and supplied meaning after reopen, sharing bilingual observations with T139. Preserve the delivered initialization/settings/install tests; keep unavailable observations unverified and repair workflows/initialize.md or adapters/codex/skills/novel-init/SKILL.md only for observed failures per FR-001-003, US1/AC1-5 and SC-001-002 (partial).
- [ ] T135 HIGH [F2] Finish the outstanding T126/T027/T028/T113 guidance evidence in tests/evaluations/guidance-results.md and tests/evaluations/novice-guidance.md: execute actual product-host G01-G12 cases with native inputs, exact saved/displayed replies, checkpoints and host/model/version; verify immediate guided/open and topic switches, reduced suggestions, constructive accessible preference adaptation, supported host-transcription input and checkpoint pauses. Collect five genuine novice usefulness/control ratings with at least four qualifying >=4/5. Retain tests/integration/test_guidance_journey.py as structural evidence and remedy only observed workflow/adapter defects per FR-004-007, US2/AC1-4 and SC-007 (partial).
- [ ] T136 HIGH [F3] Finish the outstanding T127/T031/T032/T036/T114/T117 capture, correction and resumption evidence in tests/evaluations/resume-results.md and tests/integration/test_resume_journey.py using ordinary product-host conversation and a genuine fresh interaction. Demonstrate automatic sourced capture of each required story kind, alternatives and states, a correction retaining its prior version, and recovery of all 20 ideas, ten decisions and five questions across three sessions without user note-taking. Keep the existing fresh-interpreter/installed-reader tests distinct from host extraction and repair only observed gaps in workflows/brainstorm.md, workflows/resume.md or typed record handling per FR-008-012, US3/AC1-4 and SC-003 (partial).
- [ ] T137 HIGH [F4] Complete the outstanding T128/T038/T040/T041/T043/T044/T118 authority evaluation in tests/evaluations/authority-results.md with actual semantic outcomes for at least 12 clear-acceptance and 12 non-acceptance examples across both languages, precise partial selection, rejection/alternatives, correction/revision/reversal, explicit-direction conflict clarification and every routine-checkpoint summary/pause mode. Preserve the existing five-revision history/direct-impact/manuscript tests in tests/unit/test_authority.py and tests/integration/test_canon_journey.py; record sources, actual replies, resulting states and checkpoints, and fix only observed defects without repeated approval of clear authorized facts. Share bilingual runs with T139 per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [ ] T138 HIGH [F5] Complete the outstanding T129/T046/T048/T051/T052/T115 real-host continuity evaluation in tests/evaluations/continuity-results.md after retaining T124 hold protection: execute motivation, chronology, knowledge, plot-dependency, world-rule and relationship conflicts plus intentional mystery/lie/unreliable-viewpoint cases, uncertain significance and sourced advisory opportunities. Record next-response interruption, source evidence, all user dispositions including persistent deferral, safe proposal-only exploration and restoration/revalidation before held canon changes resume. Retain tests/unit/test_continuity.py and tests/integration/test_continuity_journey.py; repair only observed semantic/structural defects per FR-015-019/021, US5/AC1-5 and SC-005/009 (partial).
- [ ] T139 HIGH [F6] Complete the outstanding T130/T055/T059/T060/T120 bilingual evaluation in tests/evaluations/language-results.md using actual installed English and Icelandic setup, guidance, capture, acceptance, revision and continuity workflows; reuse T134-T138 observations. Review paired meanings/source spans in tests/fixtures/en/ and tests/fixtures/is/, including the authored false-friend, diacritic, mixed-language, partial-selection, quotation and negation cases. Record actual host/model/version, responses and checkpoints; separate structural fixture checks, agent judgments and any human review without inferring semantic parity from Unicode round trips. Repair only observed resources/workflow defects per FR-024, US6/AC1 and SC-002/004/005/007 (partial).
- [ ] T140 HIGH [F7] Close the remaining Windows performance gap in src/novel_creator/storage.py or src/novel_creator/context.py based on measured bottlenecks, retaining the existing Linux reference pass and T132 benchmark tooling. The recorded Windows save p95 is 3.845654300s, exceeding the unchanged one-second goal. After any justified optimization, rerun tests/performance/benchmark_records.py for the complete 100-session/5,000-exchange/10,000-active-assertion/25-MiB dataset with 30 warm reads and saves; record raw results, cold read, hardware/OS/Python/Git and cache configuration in tests/evaluations/performance.md. Require read p95 <=2s and validation/local-save p95 <=1s; retain full byte-hash/path/live-index guards, private-index/CAS publication, source/authority/hold validation, cache invalidation and recovery regressions. Keep unmet results explicit and do not change thresholds or claim the Linux pass covers Windows per plan: performance goals, target platforms and scale/scope (partial).
- [X] T141 HIGH [F8] Correct contradictory current onboarding in README.md, docs/development.md and docs/testing-and-completion-guide.md: README.md says recover is not yet implemented, development.md calls implemented product commands placeholders, and the completion guide tells users to stop because production cleanup recovery is unimplemented, despite src/novel_creator/cli.py dispatching to storage.recover. Document the delivered read-only inspection and explicit unchanged-payload or published-index cleanup retry, required expected-head/unborn arguments, stale/conflicting payload behavior and write pauses; align current Linux/Windows support with deferred macOS while distinguishing historical fixture instructions from current product steps. Verify documented examples against the CLI and focused existing recovery/installed-command tests without weakening genuine host/human/performance limitations per FR-014/026, T037/T061/T133 and plan: verified onboarding (contradicts).
- [ ] T142 HIGH [F9] Finish the remaining T133/T064-T066/T123 release verification after T134-T141 prerequisites: reconcile all six story acceptance cases and SC-001-009 evidence in tests/evaluations/release-readiness.md and tests/evaluations/platform-results.md, run the full automated suite, tests/speckit-smoke.sh and every applicable quickstart scenario on the claimed Linux/Windows combinations, and record exact commands/versions/filesystems, skips, scoped host support and unsupported durability guarantees. Retain verified structural consumer/portability and native-capture results; keep actual host, human, bilingual and Windows-performance gaps explicitly release-blocking until satisfied. Review applicable constitution obligations and align onboarding/support claims only with observed results; do not reintroduce deferred macOS, drafting, dashboard, extra hosts or incompatible migrations per FR-026, SC-001-009, Constitution IX/XI and plan: incremental verified release (partial).


## Phase 16: Convergence

Execution steering — 2026-10-22: the user explicitly deferred novice evaluations
because participants are unavailable and authorized continued Windows save
performance work (T149). Novice initialization/guidance evidence remains
unverified; T143/T144 and their earlier carry-forward tasks stay unchecked.
This deferral does not waive acceptance criteria or establish release readiness.

Assessment date: 2026-10-21. This follows implementation on the Phase 15 task
list. Intent remains spec.md, plan.md, tasks.md and constitution 1.0.0. The
assessment uses current source/workflows and recorded evaluation evidence,
without Git history or branch comparisons. Existing content and markers are
preserved; the items below carry forward only outstanding scope, not additional
implementations or new acceptance thresholds.

Checked: 26 functional requirements, nine success criteria, 26 acceptance
scenarios, eight edge cases, ten plan obligations and all eleven constitution
principles. Principle X dashboard delivery is outside this feature. Findings:
eight partial, zero missing/contradicts/unrequested; all HIGH. No new deterministic
safety or constitutional contradiction is identified in the inspected code.
Unavailable judgments remain unverified rather than passing or assumed failures.

T141 is satisfied: README.md, docs/development.md and the completion guide now
match implemented recovery, expected-head/unborn, unchanged pending retries and
published-index cleanup without replay. Recorded six-test recovery/portable
verification and installed CLI checks support that result; the documentation
finding is not carried forward. T124 hold protection and T131 independent-reader
coverage remain retained. The scoped native capture pass does not establish
product creative behavior. The existing Windows benchmark reports save p95
3.845654300s against 1s; Linux's optional-cache reference pass does not close that
Windows gap. No tests, host sessions or timing measurements were rerun here.
macOS remains deferred. No extension hooks are registered.

- [ ] T143 HIGH [F1] Finish only the remaining T134/T125/T021/T112 initialization evaluation in tests/evaluations/novice-initialization.md and tests/evaluations/release-readiness.md: collect five genuine novice no-concept journeys with skipped answers, elapsed times, assistance, saved checkpoints and the optional invitation; require at least four unaided completions within ten minutes. Verify actual combined-answer handling and supplied meaning after reopening, reusing T148 bilingual evidence. Retain delivered initialization/settings/install tests and fix workflows/initialize.md or its thin Codex entry only for observed defects; keep absent observations unverified per FR-001-003, US1/AC1-5 and SC-001-002 (partial).
- [ ] T144 HIGH [F2] Finish only the remaining T135/T126/T027/T028/T113 guidance evaluation in tests/evaluations/guidance-results.md and tests/evaluations/novice-guidance.md: execute actual G01-G12 product-host cases, recording host/model/version, native inputs, saved/displayed replies and checkpoints. Verify immediate mode/topic changes, reduced suggestions, accessible constructive preference adaptation, host-provided transcription where supported and checkpoint pauses. Collect five genuine novice usefulness/control ratings with at least four qualifying >=4/5. Preserve tests/integration/test_guidance_journey.py as structural evidence and repair shared workflows/adapters only for observed failures per FR-004-007, US2/AC1-4 and SC-007 (partial).
- [ ] T145 HIGH [F3] Complete the remaining T136/T127/T031/T032/T036/T114/T117 automatic capture, correction and resumption evidence in tests/evaluations/resume-results.md and tests/integration/test_resume_journey.py through ordinary product-host conversation, including a genuine fresh interaction. Verify every required capture kind, alternative/status/source distinction, correction with retained erroneous versions, and recovery of all 20 designated ideas, ten decisions and five questions across three sessions without manual note-taking. Retain the existing installed-reader and fresh-interpreter coverage; record actual replies/checkpoints and repair only observed capture/workflow defects per FR-008-012, US3/AC1-4 and SC-003 (partial).
- [ ] T146 HIGH [F4] Complete the remaining T137/T128/T038/T040/T041/T043/T044/T118 authority evaluation in tests/evaluations/authority-results.md using actual semantic outcomes for at least 12 clear acceptances and 12 non-acceptances spanning both languages, partial selection, rejection/alternatives, correction/revision/reversal, explicit-direction conflicts and all routine-checkpoint summary/pause modes. Preserve existing tests/unit/test_authority.py and tests/integration/test_canon_journey.py evidence for five revisions, source/history/direct-impact and manuscript preservation. Record actual responses, states, sources and checkpoints, share language runs with T148 and fix only observed gaps without redundant approval per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [ ] T147 HIGH [F5] Complete the remaining T138/T129/T046/T048/T051/T052/T115 product-host continuity evaluation in tests/evaluations/continuity-results.md while retaining T124 protection and existing tests/unit/test_continuity.py and tests/integration/test_continuity_journey.py. Execute all six conflict categories, intentional mysteries/lies/unreliable viewpoints, uncertain significance and sourced advisory opportunities; record next-response interruption, sources, all user dispositions, persisted deferral, safe proposal exploration and restoration/revalidation before canon holds lift. Repair only observed workflow/validator defects and distinguish literary judgments from structural holds per FR-015-019/021, US5/AC1-5 and SC-005/009 (partial).
- [ ] T148 HIGH [F6] Complete the remaining T139/T130/T055/T059/T060/T120 bilingual evaluation in tests/evaluations/language-results.md through actual installed English and Icelandic setup, guidance, automatic capture, acceptance, revisions and continuity; reuse T143-T147 runs. Review paired meaning/source spans in tests/fixtures/en/ and tests/fixtures/is/, including false friends, diacritics, mixed-language requests, negation, quotation and partial selection. Record actual host/model/version, responses and checkpoints; separate structural checks, agent judgments and any human review without claiming semantic parity from Unicode preservation. Repair only observed language/workflow defects per FR-024, US6/AC1 and SC-002/004/005/007 (partial).
- [ ] T149 HIGH [F7] Close the remaining T140 Windows performance gap using measured bottlenecks in src/novel_creator/storage.py or src/novel_creator/context.py. Preserve the documented Linux reference pass, original targets and all validation/authority/hold, byte-hash/path/live-index, private-index/CAS, cache and recovery safeguards. After justified optimization, run tests/performance/benchmark_records.py against the complete 100-session/5,000-exchange/10,000-active-assertion/25-MiB dataset for 30 warm reads and saves, documenting raw samples, cold read, hardware/OS/Python/Git and optional-cache configuration in tests/evaluations/performance.md. Require read p95 <=2s and validation/local-save p95 <=1s; keep the recorded 3.845654300s Windows save p95 explicitly unmet until measured compliance, without substituting Linux results or lowering thresholds per plan: performance goals, target platforms and scale/scope (partial).
- [ ] T150 HIGH [F8] Finish remaining T142/T133/T064-T066/T123 release verification after T143-T149 prerequisites: reconcile all six stories' acceptance cases and SC-001-009 outcomes in tests/evaluations/release-readiness.md and tests/evaluations/platform-results.md, run the full automated suite, tests/speckit-smoke.sh and applicable quickstart scenarios on claimed Linux/Windows combinations, and record commands, versions/filesystems, scoped host support, skips and unsupported durability guarantees. Retain T141's corrected onboarding, passing structural recovery/consumer/portability evidence and scoped capture gate. Keep missing host/human/bilingual observations and Windows performance release-blocking; update support claims only to verified scope and review applicable constitution obligations without adding deferred macOS, drafting, dashboard, additional hosts or incompatible migrations per FR-026, SC-001-009, Constitution IX/XI and plan: incremental verified release (partial).

### T149 continuation — 2026-10-22

The user authorized performance work while novice evaluations stay deferred.
Retained batched candidate verification after real-Git adversarial tests and an
independent review: its controlled component median falls from 0.227261500s to
0.110481450s (51.4%), with the complete path/mode/OID delta, parent, commit hash
and exchange digest verified. Full byte/path/live-index guards, private-index/CAS
and recovery protections remain. No buffering experiment was retained.

Whole-save medians in the alternating diagnostic are 3.115621350s before and
3.147080250s after; no end-to-end gain is established. The full fresh-process
30-read/30-save benchmark completes with no operation errors/timeouts but records
read p95 3.252935300s and save p95 5.907091200s, both unmet. Its exit 1 is a
threshold result, not an operation failure. T149 stays unchecked; earlier
3.845654300s evidence is historical and not silently replaced or waived.

Windows full suite: 120 total, 118 passed plus two explicit symlink-privilege
skips, exit 0. Linux full suite: 120 passed, zero skips, exit 0. See
[evidence and limits](../../tests/evaluations/windows-candidate-optimization-20261022.md).
T143/T144 remain deferred/unverified, and final release verification remains open.

### T149 full-history and file-check continuation — 2026-10-22

Retained validated relative guard paths with explicit trusted Git worktree-root
binding; every path, live-index entry and file byte remains checked on both guard
passes. Follow-up review found a root-redirection defect in the prototype; a
SHA-1/SHA-256 adversarial regression demonstrated it before the fix and passes
afterward. No custom pipe, skipped history, new cache or automatic maintenance
is retained. The final matched diagnostic lowers guard median 0.762s -> 0.532s
and whole-save median 4.315s -> 3.646s; these are not p95 claims.

Full-scale ordinary-layout Windows read p95 **1.715363500s** passes; save p95
**3.398351400s** remains unmet. Separately packed disposable fixture: read p95
1.020150600s, save p95 2.739170400s; maintenance takes 4.742777600s outside timers.
Both complete all 30 reads/saves without operation errors/timeouts and exit 1 for
the save threshold. Packing is an explicit benchmark layout only and does not
establish ordinary-layout performance or a packing-only save gain.

Windows full suite: 122 total, 120 passed/two explicit symlink-privilege skips;
Linux full suite: 122 passed/zero skips, plus both final focused guard fixtures.
Frozen inputs remain unchanged through verification and measurement. See
[report and raw evidence](../../tests/evaluations/windows-history-guard-optimization-20261022.md).
T149 stays unchecked. Novice evaluations stay deferred/unverified; release remains
incomplete. No performance target or save safeguard is relaxed.

### T149 save snapshot reuse — 2026-10-22

Further directory-scan, queued-batch and isolated native Git experiments are not
retained. Save instead reuses its exact captured immutable tree between full
history reading and the first guard. Every blob and both fresh byte/index/path
guards remain checked. A SHA-1/SHA-256 prior-snapshot regression passes before
and after the change; read-only review finds no actionable issues. Windows full
suite: 123 tests, 121 passed/two explicit privilege skips. Linux: 123 passed,
zero skips. Frozen inputs remain unchanged through all tests and measurements.

The matched trace removes one tree query (25 -> 24 Git calls); live-index,
hash-object and cat-file calls remain. The omitted query measures about 0.071s;
whole-save median differences are not attributed wholly to that change.
Final full-scale ordinary read/save p95 **3.545458500s/6.626094600s**; packed
**2.277303600s/4.562267800s**, with 6.001285800s maintenance separately excluded.
Each configuration completes all 30 reads/saves without operation errors/timeouts
and exits 1 because both targets are unmet. Cross-run timing variation does not
establish a source effect. T149 remains unchecked; novice evaluations remain
deferred/unverified and the full release goal is incomplete. See
[current evidence](../../tests/evaluations/windows-snapshot-reuse-20261022.md).

### T149 first-guard overlap — 2026-10-22

Complete history validation and the first full managed-file guard now overlap
under the writer lock; the complete guard result is required before receipts/
candidates. The second fresh guard stays before publication. Source/authority/
hold, byte/index/path, candidate/CAS, fsync and recovery checks remain. A
validation-time edit can leave truthful pending work before the second guard
rejects it; coordinated SHA-1/SHA-256 tests cover this timing and validation-error
precedence. Windows full suite: 125 tests, 123 pass/two explicit privilege skips;
Linux: 125 pass/zero skips. Read-only review finds no actionable issues.

Final paired diagnostics lower Windows save median 3.014s -> 2.673s and Linux
0.948s -> 0.789s; these are not p95 compliance. Full complete-fixture 30-run
read/save p95: ordinary PowerShell **2.014926100s/2.733241800s** (both unmet),
packed PowerShell **1.045105700s/2.209314500s** (read passes), packed native
Windows Git Bash **0.942910200s/1.719383700s** (read passes). Packing time is
separately excluded, no machine PATH or product selector change is introduced,
and Git Bash results do not replace ordinary/default performance. Current Linux
ext4 reference **1.153318426s/1.072006791s** passes read/misses save. Every run
completes 30 reads/saves without operation errors/timeouts and exits 1 for unmet
thresholds. The older Linux pass remains historical; no current-source
configuration passes both targets. Source/test/benchmark fingerprints remain
unchanged. See [full evidence and limits](../../tests/evaluations/windows-guard-overlap-20261022.md).
T149 stays unchecked; novice evaluations remain deferred/unverified, other host/
semantic gates stay open, and release remains incomplete. No target or save
safeguard is waived.

### T149 canonical path allocations — 2026-10-22

Retained a narrow optimization to managed-path processing: canonical exchange
names skip redundant PurePosixPath parsing, and check_managed validates a path
without constructing a discarded Path object. The public safe_path signature,
return type, general allowlist checks and non-string fallback are preserved.
Every fresh filesystem/index check and full root-bound content hash remains;
full-history validation, both guards, candidate verification, CAS and recovery
are unchanged. Independent review found no supported-string safety defect.

A full-fixture four-sample-per-variant diagnostic lowers guard median
0.726769250s -> 0.575608300s and save median 3.015941150s -> 2.446908700s;
these are noisy diagnostic medians, not p95 compliance. GC suppression and
releasing the benchmark preparation graph did not show a reliable benefit;
neither policy is changed. A canonical-path/allowlist regression matrix passes
on the prior implementation and the retained candidate. Full final-source Linux
suite: all 126 tests pass. Source-pinned Windows tests and the separate 30-run
benchmark are recorded in tests/evaluations/windows-allocation-investigation-20261022.md.
T149 remains unchecked. Novice evaluations remain deferred/unverified; no other
missing human/host evidence or release criterion is waived.

Final verification: Final retained-source tests: Windows 126 tests in 373.021s, 124 passed and
two explicit Windows symlink-privilege skips, exit 0; Linux all 126 pass in
82.276s, zero skips, exit 0. The Windows and Linux manifests record the source
fingerprints; Windows before/after hashes match across tests and measurements.

Final-source Windows Git Bash, explicitly packed disposable fixture: first read
3.200534500s, read p95 1.587495700s, validation/local-save p95 3.645534700s.
All 30 reads and 30 saves succeed without timeouts or operation errors. Read
passes its 2s target; save misses its 1s target. Exit 1 records the unmet threshold.
Packing takes 5.748657100s outside operation timers and is fixture preparation,
not product behavior. This configuration does not establish ordinary-layout
performance. Linux performance has not been rerun for this path-allocation source;
previous overlap-source measurements remain historical and source-pinned.

### T149 current-source critical-path diagnostics — 2026-10-22

No further runtime change is justified by these experiments. Combined JSON
parsing is slightly slower with greater peak memory. Ordered current-source
stage events place most first-guard work under full-history validation; the
complete final guard is a material serial cost. Pipelining its content samples
before all metadata checks is not adopted. Parallel metadata-only guards show
no convincing gain (two workers ~4.3% lower median, four ~20.7% slower) and are
not retained. All existing byte/path/index/root/authority/candidate/CAS/recovery
checks and source fingerprints remain unchanged; prior full suites and 30-run
p95 remain applicable. Evidence, executed scripts and exact source:
tests/evaluations/windows-save-critical-path-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified.


### T149 combined branch/OID queries — 2026-10-22

The reviewed helper combines the initial and postpublication branch/OID
reads; the fresh pre-CAS branch check, both complete managed-file guards, full
history/byte/index/path/root checks, private candidate/CAS and recovery remain.
Normal Git process count 24 -> 22; no atomic snapshot guarantee is introduced.
Permanent SHA-1/SHA-256 tests cover reference states, malformed fallback and
same-OID branch changes before and after publication with index preservation.

Final-source Windows suite: 129 tests in 457.064s, 127 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 129 pass in
85.357s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 4.237690400s; read p95 5.106631200s; validation/local-save p95
3.612526000s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records unmet thresholds. No explicit Git packing/maintenance is requested.
This is the default fixture layout; prior packed/native-Git results describe
their own source and configuration, not this source. Linux performance has not
been remeasured for this source; historical Linux/earlier Windows data is kept.

The small matched four-save-per-variant median 2.762793500s -> 2.336735950s
is diagnostic only. Complete evidence: tests/evaluations/windows-ref-query-20261022.md.
T149 remains unchecked; novice evaluations remain deferred/unverified.


### T149 history reconstruction and parallel hash candidates — 2026-10-22

External diagnostics against unchanged storage SHA-256 47c6eac0122d1076a91f21caeb253bf6721678f4e626fc0630ab069557e55304
reject a certified-history index rewrite: about 10ms absolute reconstruction
saving, excluding Git/JSON/full-save work. Four-worker final-guard hashing is a
promising candidate: four balanced complete saves per variant on the full
validated packed Windows/Git Bash fixture lower median 3.245158150s to
2.469268600s (23.9%); two workers measure 3.005366000s. All 12 saves succeed.
These are small diagnostic medians, not p95 compliance. All metadata precedes
hashing; every managed byte, root binding, result count and process status is
checked before OID comparison/publication. SHA-1/SHA-256 isolated candidate
checks pass; the initial insufficient-fixture runner failure is preserved.

No production change is retained from these experiments. Adoption still needs
production publication/error-path regressions, measured small-fixture/platform
policy and final-source full suites/30-run benchmarks. Exact scripts, samples,
source/evidence hashes and limitations are recorded in
tests/evaluations/windows-history-hash-candidates-20261022.md. Previous verified
129-test suites and ordinary-layout read/save p95 5.106631200s/3.612526000s
remain current. T149 stays unchecked; novice evaluations stay deferred/unverified.


### T149 parallel-hash production implementation — verification in progress

The measured candidate is now implemented in storage.py, SHA-256
6ec58b45314b7a99877220452367f6b89b532bed2fe3b3c842f0272a9aba1f5a.
Only final guards on Windows with >=1024 managed files use up to four complete
root-bound Git byte readers; initial guards, smaller saves and non-Windows
runtime remain serial. Every metadata/path/index check precedes hashing; all
process/count results precede OID comparisons, and workers join before lock
release. Worker-start failures become structured code-5 errors. Candidate,
CAS, full history, authority/holds and recovery safeguards are unchanged.

Five focused production regressions pass (54.214s). Linux full suite: all 133
pass in 75.471s, zero skips; source fingerprints remain unchanged. Read-only
review and follow-up report no actionable findings. The initial full Windows
run has one installation encoding error and two explicit symlink skips because
the runner omitted documented PYTHONUTF8=1. Isolated reproduction fails without
it and passes with it; all logs are preserved. The complete Windows suite and
30-run benchmark are being rerun with the corrected documented environment.
No new p95 compliance or completed Windows verification is claimed yet.

Evidence and limitations: tests/evaluations/windows-parallel-hash-20261022.md.
T149 remains unchecked; novice evaluations stay deferred/unverified.


### T149 retained parallel final-guard hashes — 2026-10-22

Final-source Windows suite: 133 tests in 571.309s, 131 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 133 pass in
75.471s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 5.184642400s; read p95 5.110137800s; validation/local-save p95
6.566394800s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records threshold status. No explicit Git packing/maintenance is requested.
This is the default fixture layout; earlier packed/native-Git results describe
their own source and configuration. Linux performance has not been remeasured
for this source; historical Linux/earlier Windows data is retained.

Large Windows final guards use up to four complete root-bound byte readers only
after all metadata/index/path checks succeed, at >=1024 managed files. First
guards, small saves and non-Windows runtime keep serial hashing. All worker
statuses/counts precede OID comparison; every worker joins before lock release.
Worker-start failures now return structured code-5 errors. Candidate/CAS,
authority/hold and recovery safeguards remain unchanged. Four new production
regressions and the existing ancestor-worktree/index-prefix regression cover
SHA-1/SHA-256 tampering, resource failures, error precedence, index/HEAD
preservation, pending receipts and successful unchanged retry. Independent review
found no actionable issues. Exact source, threshold samples, raw full-scale
measurements and manifests: tests/evaluations/windows-parallel-hash-20261022.md.
T149 stays unchecked. Novice evaluations remain deferred/unverified; other
host/human/language/release evidence is not invented or waived.


Matched final-source ordinary-layout Windows/PowerShell evidence subsequently
completes all eight saves: four per variant, balanced ABBA/ABBA, median
6.313554450s before versus 5.400350250s after (14.5% lower).
This supports retaining the full-byte optimization, not p95 compliance. Git
invocations are 22/25; full hashing remains, with bounded parallel readers.
The full-history batch remains substantial (1.994884450s median
invocation wall time). Detailed counter checks, limitations and raw traces are
recorded in tests/evaluations/windows-parallel-hash-20261022.md. T149 remains
unchecked; novice evaluations remain deferred/unverified.


### T149 partitioned history-read prototype — not retained

Source remains verified 6ec58b45... unchanged. External immutable-OID partitioning
reduces median full-history snapshot read 3.853349350s to 1.474333450s
(four samples/configuration), but complete-save ABBA/ABBA medians are
5.399026300s serial versus 5.505927300s with four requests.
No complete-save benefit is established. Review requires preserving earlier
malformed-history errors before later worker exceptions and preserving binary
framing across chunk boundaries. Production retains the original history reader.
Correction, fault regressions and further measurements remain necessary before
adoption; no fresh p95 claim is made. Raw samples, executed scripts, SHA-256
manifest and limitations: tests/evaluations/windows-parallel-history-candidate-20261022.md.
T149 remains unchecked; novice evaluations stay deferred/unverified.


### T149 corrected public history reader — full verification pending

The working source 9b909213... now uses up to four immutable-OID requests for
large public Windows reads (>=1024 exchanges). Ordered single-stream framing
and one complete serial fallback on any worker/submission/nonzero-exit failure
preserve error and prefix semantics. Saves keep serial history reads; all file
and publication safeguards remain intact. Five focused methods pass in 31.152s,
including SHA-1/SHA-256 boundary and failure regressions. Full suites and fresh
30-run p95 remain pending because C: repeatedly reached zero free bytes. Earlier
133-test and p95 results apply only to source 6ec58b45..., not this change.
Corrected small-sample diagnostics show a public-read gain but no save benefit;
they do not establish compliance. Source snapshots, scripts, results and hashes:
tests/evaluations/windows-history-partition-pending-20261022.md.
T149 stays unchecked. Novice evaluations remain deferred/unverified.


### T149 public history reads — full verification after disk cleanup

Windows: 138 tests in 704.102s, 136 passed and two explicit real-symlink
privilege skips, exit 0. Linux/WSL2: all 138 pass in 229.403s, zero skips,
exit 0. All five runtime/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 2.486383800s; read p95 1.787683800s; validation/local-save p95
9.219870400s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read passes its 2s target; save misses its 1s target. Exit 1
records the unmet save threshold. No explicit Git packing/maintenance is requested.
Linux performance has not been remeasured for this source; earlier reference
results remain historical evidence.

Large public Windows reads (>=1,024 exchanges) fetch captured immutable blob
OIDs in at most four contiguous requests using the existing Git wrapper. Every
worker joins before parsing or returning. Successful outputs form one original-order
binary stream. Any worker/submission exception or nonzero child exit triggers one
full original serial request before parsing, preserving partial stdout, earlier
damaged-history errors and verified-prefix checkpoints. Small public reads and
non-Windows runtime stay serial. Save history remains serial: measured parallel
save variants provided no gain. All history/blob/schema/digest/authority/hold,
path/symlink/mode/live-index, both complete root-bound byte guards, private
candidate, fresh branch/CAS, receipt and recovery safeguards remain. The
previous parallel final-byte guard is unchanged.

Matched final-source read medians 5.125521150s serial / 2.825309150s four
workers (44.88% lower; four samples/policy) are diagnostic, not p95.
Source, complete logs, raw measurements, hardware and stage events:
tests/evaluations/windows-history-read-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified and other release gates remain open.


### T149 balanced save-reader experiment — integration tests required

Production remains verified 9b909213... unchanged. An external current-source
ABBA/ABBA fresh-worker diagnostic changes only history/first-guard workers1/1
to 2/2, retaining final four and every safeguard. All eight saves succeed with 25/27 Git
calls. Four-sample medians 5.669104200s/4.856166300s (14.34% lower),
with substantial variability, support further integration tests, not p95 or
release compliance. Independent review requires combined worker/fallback,
error-prefix, lock/join, redirection/tampering, retry and platform-policy
regressions before adoption. Source, samples and hashes:
tests/evaluations/windows-balanced-save-readers-20261022.md. T149 remains
unchecked; novice evaluations remain deferred/unverified.


### T149 balanced-reader integration — full verification pending

Storage 9bbcb0ac... selects bounded two/two Windows save-history/first-guard readers,
keeping four public/final readers and existing small-input/non-Windows serial policy.
All checks, original first-guard await/error/prefix order and worker/lock/candidate/
CAS/recovery stages remain. Five new combined regressions and existing framing/
final-guard cases pass: 8 methods in 85.046s, exit 0. Review found no actionable issue.
Fresh full 143-test suites are running; fresh 30-run ordinary Windows measurement
remains required. Preceding 138-test/p95 evidence belongs to 9b909213... only.
Tests, exact source, red/green results and pending manifest:
tests/evaluations/windows-balanced-save-pending-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified.


### T149 balanced save readers — full verification

Windows full suite: 143 tests in 567.082s, 141 passed,
2 explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 143
pass in 58.745s, zero skips, exit 0. The same five source/test/harness/
helper fingerprints match before and after both suites and the benchmark.

Ordinary-layout Windows PowerShell with the optional authenticated cache:
first read 2.288559600s; read p95 2.289081100s; validation/local-save p95
9.240644400s. All 30 reads and 30 saves succeed without operation errors or timeouts.
Read misses the unchanged 2s target; save misses the unchanged 1s target.
Benchmark exit 1 records that unmet threshold. No explicit packing/maintenance
is requested. Linux performance has not been remeasured for this source;
its earlier reference results remain historical evidence.

Large Windows saves use two history readers and two first-guard full-byte
readers while the original operations overlap. The final full-byte guard and
public history reads retain up to four readers. Each existing 1,024-item
threshold independently keeps small inputs serial; non-Windows defaults remain
one. All metadata/index/path/symlink/mode checks precede each guard's hashing.
All actual blob/digest/schema/authority/hold checks, both complete root-bound
byte guards, private candidate verification, original first-guard error/await
position, worker/lock lifetime, fresh branch/CAS, receipts and recovery remain.
History outputs keep ordered single-stream framing and one full serial fallback
on worker/submission/nonzero exit failure. No check is skipped or moved.

Matched final-source medians: 3.509755100s control / 3.061612450s two/two,
four balanced samples per policy. This is diagnostic, not p95 compliance.
Source, full results, hardware, paired samples and stage traces:
tests/evaluations/windows-balanced-save-20261022.md. T149 remains unchecked;
novice evaluations remain deferred/unverified.


### T149 fresh native bundle-mode experiment — not adopted

Verified production 9bbcb0ac... remains unchanged. A strict-bundle-only fresh
GetFileAttributesW type query retains lstat for parents, non-bundles, special/
unknown/error attributes, with no metadata cache or skipped byte/index checks.
Review required NORMAL alone; a failing assertion and corrected 16-accepted/
21-fallback table are recorded. Eight complete fresh-worker saves all succeed
with 27 Git calls, counted native queries and six complete byte-hash partitions.
Four-sample medians 4.413188450s/3.816763250s (13.51% lower) are variable
diagnostics, not p95 compliance. Production-path compatibility/failure/tampering
regressions and fresh complete verification remain necessary before adoption.
Exact source, raw samples, review boundary and hashes:
tests/evaluations/windows-native-bundle-mode-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified.


### T149 native Windows bundle metadata: verification pending (2026-10-22)

T149, 2026-10-22. Fresh per-leaf GetFileAttributesW queries classify only ordinary
canonical bundle files. Normal attributes must stand alone; unusual, invalid,
missing or unavailable results fall back to the original lstat. Parents and all
non-bundle checks retain lstat. Full byte hashes, both complete guards, live index,
root binding, candidate verification, conditional publication and recovery remain.
Only the API callable is cached; file metadata is queried anew for every check.

Seven new tests cover API/fallback/type boundaries, Unicode and actual native
extended Windows paths, SHA-1/SHA-256 same-stat tampering, live-index changes,
pending receipts, exact retries and bootstrap/public-read boundaries. Initial
red: 7 tests, 125 missing-feature errors, 4.469s. Final focused verification:
9 tests, 25.960s, all pass, exit 0. Read-only review found no actionable production
issue. The full 150-test Windows/Linux suites and ordinary-layout 30-run Windows
benchmark are pending for this source. Prior 143-test evidence applies to the
balanced-reader source only. No performance gate or release approval is claimed.
Novice evaluations remain deferred and unverified.

Evidence: `tests/evaluations/windows-native-bundle-mode-production-pending-20261022.md`.


### T149 native Windows bundle metadata — full verification

Windows: 150 tests in 453.334s, 148 passed,
2 explicit real-symlink privilege skips, exit 0.
Linux/WSL: all 150 tests pass in 48.573s, zero skips,
exit 0. Six source/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Ordinary Windows PowerShell fixture: first read 1.998505000s; read p95
1.320975200s (PASS, target 2s); validation/local-save p95
3.292486500s (UNMET, target 1s). All 30 reads and 30 saves succeed without operation
errors or timeouts. Benchmark exit 1 records unmet performance thresholds.
No explicit Git packing or maintenance was requested. Linux performance was
not remeasured for this source; previous Linux timings remain historical.

Windows ordinary canonical bundle leaves use fresh GetFileAttributesW queries.
Only NORMAL alone or nonzero combinations of ARCHIVE/READONLY/HIDDEN/SYSTEM
classify regular files directly. Invalid, unknown, special, directory, reparse,
unavailable and exceptional results use the original lstat. Parents, other
managed paths, small bootstrap/write paths and non-Windows behavior retain
original checks. Only the API callable is cached; filesystem metadata is fresh.
Both complete live-index/path/type/byte guards, metadata-before-hash ordering,
root binding, full historical blob/digest/schema/authority/hold validation,
private candidate verification, worker joins under the lock, original error
ordering, fresh branch/CAS, receipts and recovery remain. No check is skipped.

See `tests/evaluations/windows-native-bundle-mode-production-20261022.md`. T149 remains unchecked; novice evaluations remain deferred/unverified.


### T149 full-history component profile and four-reader policy (verification pending)

2026-10-22: full-scale save profile attributes about 0.79-0.80s of 1.03-1.08s
history work to Git cat-file reads, 0.14-0.19s to JSON decoding, about 0.015s
to blob hash constructors and about 0.019s to certified index reconstruction.
Per-call tracing has overhead; threaded durations overlap. Eight matched fresh
complete saves on the verified native-metadata source, ABBA/ABBA with two/four
history readers, produce medians 2.544967200s/2.258775650s (11.25% lower).
All byte guards, native leaf queries, six hash partitions, and publication checks
remain. This is diagnostic evidence, not p95 or a portable speedup.

Runtime changes only the bounded large-Windows save-history policy from two to
four. Existing 1024 threshold, serial non-Windows/small histories, two initial
byte readers and four final byte readers remain. Regression policy and fallback
checks now exercise four children and preserve earlier damaged history, guard
error precedence, complete joins under the lock, exact retry and original state.
Default-policy red run fails 2 != 4 before the runtime edit. Focused/full suites
and a fresh required 30-run benchmark must verify this source. T149 remains open;
novice evaluations remain deferred/unverified.

Evidence: tests/evaluations/windows-history-components-20261022.jsonl and
tests/evaluations/windows-native-history-workers-20261022.txt.


### T149 four Windows save-history readers — full verification

Windows: 150 tests in 439.660s, 148 passed,
2 explicit real-symlink privilege skips, exit 0.
Linux/WSL: all 150 tests pass in 50.762s, zero skips,
exit 0. Six source/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Ordinary Windows PowerShell fixture: first read 1.984177600s; read p95
1.183358100s (PASS, target 2s); validation/local-save p95
2.856806500s (UNMET, target 1s). All 30 reads and 30 saves succeed without operation
errors or timeouts. Benchmark exit 1 records unmet performance thresholds.
No explicit Git packing or maintenance was requested. Linux performance was
not remeasured for this source; previous Linux timings remain historical.

Large Windows saves now use up to four history readers instead of two.
The existing 1,024-item threshold keeps small histories serial; non-Windows
keeps one reader. The initial full-byte guard retains two readers and the final
full-byte guard four. All history is read and hashed; JSON and ephemeral indexes
are rebuilt. Ordered framing, captured OIDs, original serial fallback, all child
joins, damaged-prefix/error precedence and lock lifetime remain. Fresh native
bundle metadata with conservative lstat fallback, parent checks, both complete
byte/live-index/path/type guards, candidate/tree/digest/parent verification,
authority/hold checks, fresh branch/CAS, receipts and recovery remain unchanged.
No check is skipped and no target is lowered.

See `tests/evaluations/windows-four-history-readers-20261022.md`. T149 remains unchecked; novice evaluations remain deferred/unverified.

### T150 independent distribution and UTF-8 continuation — 2026-10-22

The independent built-wheel check exposed legacy-encoding JSON output in the
installed CLI. The CLI now selects UTF-8 for stdout/stderr. A regression first
failed all four ASCII/Windows-1252 success/error cases; all 11 focused CLI and
portable-install tests pass after correction. The wheel verifier checks exact
source/resources, isolated module origins, console initialization, pinned novel
saves/reopens, recovery inspection and isolated legacy-stream Unicode errors on
Linux and Windows, reusing existing dependency packages without system changes.
Both Bash smoke checks pass using existing local jq binaries. Full-suite and
artifact details are recorded in tests/evaluations/independent-release-verification-20261022.md.

This is partial T150/FR-024 verification. T143–T150 remain unchecked: genuine
novice and product-host semantic evidence and the Windows save target are still
missing. No benchmark was rerun, target or safeguard lowered, checklist changed,
commit, push, provider call or publication performed. Existing dirty performance
work was preserved.


## Phase 17: Convergence

Present-state assessment after the independent distribution/UTF-8 implementation pass. The current core tooling, scoped native capture gate, 151-test Linux/Windows regression evidence, built-wheel portability and Bash smoke checks are retained. The eight remaining findings below carry forward only unmet product/human/bilingual/performance and dependent release work; all are partial/HIGH. No observed constitutional contradiction or unrequested implementation was identified. Spec, plan, existing task markers and earlier evidence remain unchanged.

- [ ] T151 HIGH [F1] Complete the remaining T143/T134/T125/T021 initialization evaluation in tests/evaluations/novice-initialization.md: record five genuine novice no-concept journeys with skipped answers, elapsed time, assistance, actual invitation and saved checkpoints; require at least four unaided completions within ten minutes. Verify actual combined-answer handling and supplied meaning after reopening with the T156 bilingual runs. Retain delivered initialization/settings/independent-install tooling and the passing wheel checks; repair workflows/initialize.md or adapters/codex/skills/novel-init/SKILL.md only for observed defects. Do not replace human observations with simulations per FR-001-003/026, US1/AC1-5 and SC-001-002 (partial).
- [ ] T152 HIGH [F2] Finish T144/T135/T126/T027/T028 guidance evaluation in tests/evaluations/guidance-results.md and tests/evaluations/novice-guidance.md: execute actual G01-G12 installed product-host cases with host/model/version, native inputs, exact saved/displayed replies and checkpoints. Verify immediate mode/topic changes, reduced suggestions, constructive accessible preference adaptation, checkpoint pauses and host-provided transcription where available. Collect five genuine novice usefulness/control ratings with at least four qualifying >=4/5. Retain tests/integration/test_guidance_journey.py as structural evidence; repair workflows/brainstorm.md, language resources or the thin adapter only for observed failures per FR-004-007/026, US2/AC1-4 and SC-007 (partial).
- [ ] T153 HIGH [F3] Complete T145/T136/T127/T031/T032/T036/T114/T117 automatic capture, correction and resumption evidence in tests/evaluations/resume-results.md through ordinary installed product-host conversation, including a genuine fresh interaction. Across three sessions recover all 20 designated ideas, ten explicit decisions and five questions without manual note-taking; verify every required capture kind, alternatives, state/source distinctions and corrections retaining erroneous versions. Record actual native inputs, responses, saved captures and checkpoints, retaining tests/integration/test_resume_journey.py and installed-reader coverage. Repair workflows/brainstorm.md, workflows/resume.md or record handling only for observed gaps per FR-008-012/019, US3/AC1-4 and SC-003/009 (partial).
- [ ] T154 HIGH [F4] Finish T146/T137/T128/T038/T040/T041/T043/T044/T118 authority evaluation in tests/evaluations/authority-results.md: record actual installed-host outcomes for at least 12 clear acceptances and 12 non-acceptances spanning both languages, partial selections, rejection/alternatives, correction/revision/reversal, protected-direction conflicts and all on_request/session_close/every_exchange summary/pause modes. Retain structural five-revision, source/history/direct-impact and unchanged-manuscript evidence in tests/unit/test_authority.py and tests/integration/test_canon_journey.py. Share bilingual runs with T156, and repair only observed workflow/validator defects without redundant canon approval per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [ ] T155 HIGH [F5] Complete T147/T138/T129/T046/T048/T051/T052/T115 installed product-host continuity evaluation in tests/evaluations/continuity-results.md. Exercise all six conflict categories, intentional mysteries/lies/unreliable viewpoints, uncertain significance and sourced advisory opportunities; record actual next-response interruptions, sources, every user disposition, persisted deferral, safe proposal-only exploration and restoration/revalidation before canon holds lift. Preserve T124 hold remediation and tests/unit/test_continuity.py and tests/integration/test_continuity_journey.py safeguards; fix only observed gaps and separate literary judgments from structural checks per FR-015-019/021, US5/AC1-5 and SC-005/009 (partial).
- [ ] T156 HIGH [F6] Finish T148/T139/T130/T055/T059/T060/T120 English/Icelandic product evaluation in tests/evaluations/language-results.md, sharing T151-T155 runs for setup, guidance, automatic capture, acceptance, revisions and continuity. Assess paired meaning and precise source spans, false friends, diacritics, mixed-language requests, negation, quoted dialogue and partial selection in tests/fixtures/en/ and tests/fixtures/is/. Record actual installed host/model/version, inputs, responses, states and checkpoints, separating structural checks, agent judgments and any human review. Retain authored pitfall fixtures, UTF-8 CLI regression and passing cross-platform wheel evidence; neither Unicode round trips nor prepared records establish semantic parity. Repair only observed language/workflow defects per FR-024, US6/AC1 and SC-002/004/005/007 (partial).
- [ ] T157 HIGH [F7] Close T149/T140 Windows save performance using measured bottlenecks in src/novel_creator/storage.py or src/novel_creator/context.py. The final delegated-provenance-source ordinary Windows run records read p95 3.453516100s (fails <=2s), 26 completed saves and a timeout on attempt 27; save p95 is unavailable. Earlier read/save p95 values are historical, not current compliance. Preserve all full-history validation, authority/holds, full byte hashes, path/type/live-index guards, root binding, private candidate verification, lock/worker lifetime, fresh branch/CAS, cache and recovery safeguards. After a justified change, run tests/performance/benchmark_records.py for 30 reads and saves over 100 sessions/5,000 exchanges/10,000 active assertions/at least 25 MiB, recording raw samples, cold read, hardware/OS/filesystem/Python/Git and cache configuration in tests/evaluations/performance.md. Retain the Linux reference evidence without substituting it for Windows compliance or lowering targets per plan: performance goals, target platforms and scale/scope (partial).
- [ ] T158 HIGH [F8] Complete T150/T142/T133/T064-T066/T123 final release reconciliation after T151-T157 prerequisites. In tests/evaluations/release-readiness.md and tests/evaluations/platform-results.md map all six stories' acceptance scenarios and SC-001-009 to actual evidence, complete remaining applicable quickstart scenarios and verify scoped Linux/Windows support, versions/filesystems, skips and unsupported durability guarantees. Reuse tests/evaluations/independent-release-verification-20261022.md: Linux 151 passing tests, Windows 149 passing plus two explicit symlink-privilege skips, passing wheel checks on both and passing Git Bash/Linux smoke checks; rerun affected/full checks when subsequent repairs invalidate this evidence. Preserve the scoped capture gate, recovery/consumer/portability evidence and corrected onboarding. Keep absent host/human/bilingual outcomes and unmet Windows performance release-blocking, review applicable constitution obligations and avoid deferred macOS, drafting, dashboard, additional hosts or incompatible migrations per FR-026, SC-001-009, Constitution IX/XI and plan: incremental verified release (partial).

## Phase 18: Observed Windows path-boundary correction

- [X] T159 Reject Windows directory junctions and other reparse points in managed paths and the novel's .git directory in src/novel_creator/storage.py under the existing storage path-safety contract. Reproduce the defect before correction; add mocked directory/file attributes, real story/.git junctions and post-candidate insertion regressions in tests/integration/test_path_redirection.py. Verify full Windows/Linux suites and the updated independent wheel, preserve pending work and all transaction safeguards, and record source-specific evidence in tests/evaluations/windows-junction-boundary-20261023.md. This completes the observed correction only; T151-T158 remain open.

### T157 continuation — 2026-10-23

Current-source packed/direct-Git Windows verification completes all 30 reads and 30 saves: read p95 0.824995800s passes; save p95 1.971346700s remains unmet. Packing is explicit and separately timed; default PowerShell/ordinary-layout compliance is not inferred. Metadata GIL diagnostics regress ordinary-layout saves and are not adopted. See tests/evaluations/windows-performance-continuation-20261023.md for raw samples, stage events, hardware and unchanged source identity. T157 remains unchecked.

The unexecuted prepared-host plan at tests/evaluations/product-host-run-plan-20261023.md covers the remaining English/Icelandic scenario evidence and fresh-task resumption. Task creation and follow-up messaging require explicit user authorization in the app; no evaluation tasks have been created or driven. Genuine novice observations and ratings remain separate. T151-T158 are unchanged.

## Phase 19: Observed delegated-input boundary

- [X] T160 Record the authorized English/Icelandic task-creation and follow-up input probes in tests/evaluations/product-host-runs/20261023T095949Z/: verify actual public event source types, exact delegated delivery and absent native userMessage items, preserve task reports without reasoning, and stop before installation/creative cases. Clarify the existing unavailable-input rule in workflows/entry.md, adapters/codex/AGENTS.fragment.md and docs/development.md; verify installation/resources and the updated wheel on Windows/Linux. This completes boundary evidence and instruction clarification only; no semantic, novice, bilingual or fresh-resumption task is completed.

The user authorized creation and follow-up driving of the four planned evaluation tasks. Two initial tasks and their four capture probes were executed; creation and follow-up APIs expose functionCallOutput delegation events rather than native userMessage input. The two fresh-resumption tasks were not created because the prerequisite gate could not pass. Authorization remains granted. T151-T158 remain unchecked, and no source/authority rule was weakened to continue the run. Actual supported native current-turn input is needed; repeating task-to-task messages does not supply it.

## Phase 20: Observed Git blob identity defects

- [X] T161 Reject corrupt equivalent-JSON Git blobs before candidate publication and history acceptance under every cache policy. Verify SHA-1/SHA-256 real-object regressions, unchanged HEAD/index/verified-prefix checkpoint/proof on failure, retained pending work and exactly-once retry after restoration. Record red/green evidence, final Windows/Linux full suites and independent wheel verification in tests/evaluations/git-blob-integrity-20261023.md and its source-pinned manifest. This repair adds no native-host, novice, bilingual, performance or release-completion evidence.

## Authorized follow-up: labeled delegated evaluation input

- [X] T162 Add explicit installed native/delegated input capture with current-thread/turn binding, fail-closed parsing and committed source provenance. Require evaluation-only opt-in for delegated input, preserve exact text and native/novice gates; verify parser, installed CLI and wheel behavior. Design/sequence: docs/delegated-input-plan.md.
- [X] T163 Resume the authorized prepared English/Icelandic host runs using the explicit delegated route. Independently verify source labels, exact saved/displayed text, checkpoints and fresh resumption where available; record delegated automated evidence separately and leave T151-T158 native/human/performance gates unchanged unless their actual criteria are met.

T163 closes only this additional delegated-evidence scope: two capture gates,
32 exact persistence/display case observations and two actual fresh-task
resumptions. Selected semantic observations, setup gaps and capture/citation
differences are recorded separately. It does not complete the full native-host,
three-session capture, acceptance, continuity, bilingual human or novice matrices.
See tests/evaluations/product-host-runs/20261023T202447Z/README.md and its
reproducible verifiers. T151-T158 remain unchecked.

## Phase 21: Single-user POC delivery

The owner explicitly excludes novice testers and requests a working POC without
manual testing; owner testing follows delivery. This supersedes novice/manual
prerequisites in historical tasks T151-T158 and earlier convergence phases for
POC delivery. Their old unchecked markers preserve uncollected evidence, not an
active demand for testers. SC-001/SC-007 and plan.md record the new scope.
Native/delegated source labels, authority, persistence and integrity requirements
are unchanged. Full-scale performance and subjective semantics retain honest
limitations; no unmeasured criterion is relabeled passed.

- [X] T164 Record the owner-authorized single-user POC scope in spec.md, plan.md, README.md and evaluation guidance; remove novice/manual testing as POC blockers without claiming human results or rewriting historical evidence.
- [X] T165 Tighten installed brainstorming question capture and resumption summary citations using the observed delegated-run gaps. Verify new questions, including preference prompts, remain source-backed and summaries cite current record revisions/checkpoints. Preserve exact source labels and all existing novel bundles; record automated installed-host regression evidence separately.
- [X] T166 Build the current offline POC wheel and verify it independently on Windows/Linux, run affected installed/integration checks, and prepare a directly usable single-user quickstart without providers, global configuration changes, real novel creation or framework-path dependence after installation.
- [X] T167 Reconcile POC functionality against automated evidence, record known performance/semantic/platform limits separately from POC readiness, and provide the artifact and starting instructions. Do not require manual tests, novice participants or ratings before delivering the POC.

POC outcome: all four tasks are complete. Fourteen affected checks pass on each
platform and the current wheel verifies on Windows/Linux against 26 files.
Eight current delegated installed-host observations verify both workflow repairs.
The small-history benchmark completes 30 reads/30 saves without failures or
timeouts; read p95 0.579379300s and save p95 1.983323900s retain the unmet save
target. Full scale, subjective semantics and broader release qualification are
not claimed. Start with docs/poc-quickstart.md; evidence and reproducible verifier:
tests/evaluations/poc-readiness-20261023.md and verify-poc-20261023.py.


## Phase 22: Convergence

Assessment scope: the completed Phase 21 single-user POC remains ready for owner
use. The following tasks carry forward broader automated scenario/scale and
release qualification gaps; they are not prerequisites for using the delivered
POC. Phase 21 supersedes historical novice/manual prerequisites. Do not recruit
novices, require owner/manual testing, infer human/native outcomes from delegated
input, or relabel unavailable subjective literary judgments as passing. Reuse
existing evidence only where its source/resource identity and scenario match;
share runs between tasks rather than duplicate them. Repair product behavior only
for observed defects while preserving all authority and persistence safeguards.

- [X] T168 HIGH [F1] Complete the automated installed-product capture/resumption matrix carried by T153 in tests/evaluations/resume-results.md: exercise three topic sessions with 20 designated ideas, ten explicit decisions and five unresolved questions, then recover them in a genuinely fresh host interaction. Include every capture kind, alternatives and a sourced correction retaining the erroneous version. The existing tests/integration/test_resume_journey.py proves prepared-record recovery, while product-host-runs/20261023T202447Z proves fresh resumption of one session per novel; neither proves the complete automatic extraction matrix. Use explicitly labeled authorized delegated evaluation input where applicable, compare exact saved/displayed exchanges and record sources/checkpoints, and retain native/manual observations as separately unmeasured per FR-008-012/019, US3/AC1-4 and SC-003/009 (partial).
- [X] T169 HIGH [F2] Complete automated installed-host authority and checkpoint response coverage carried by T154 in tests/evaluations/authority-results.md: at least 12 clear acceptances and 12 non-acceptances across English/Icelandic, partial selections, alternatives/rejection, five deliberate revisions with source/history/direct-impact inspection, protected-direction conflicts and all three routine checkpoint summary/pause modes. Retain passing tests/unit/test_authority.py and tests/integration/test_canon_journey.py as structural evidence; selected observed A01/A11/N04 replies do not complete the response matrix. Distinguish labeled agent interpretation from validator checks and unavailable human judgments, preserve manuscript bytes and avoid redundant approval for clear authorized facts per FR-010-013, US4/AC1-5 and SC-004/006 (partial).
- [X] T170 HIGH [F3] Complete the automated installed-host continuity response matrix carried by T155 in tests/evaluations/continuity-results.md: motivation/backstory, chronology, knowledge, plot dependencies, world rules and relationships, intentional mystery/lie/unreliable viewpoints, uncertainty, sourced advisory opportunities and every user disposition. Verify next-response interruption with evidence/resolutions, persisted deferral, safe proposal exploration and restored/revalidated context before affected holds lift. Existing hold/fault tests and selected sender-conflict/intentional-belief observations are scoped evidence only. Record agent judgments separately from structural checks and leave subjective literary qualification unmeasured where unavailable per FR-015-019/021, US5/AC1-5 and SC-005/009 (partial).
- [X] T171 HIGH [F4] Complete remaining paired English/Icelandic automated product cases carried by T156 in tests/evaluations/language-results.md, sharing T168-T170 observations. Map setup, guidance, capture, acceptance/revision and continuity to actual installed responses and saved states; cover the unexecuted tests/fixtures/en/ and tests/fixtures/is/ language-pitfall cases, false friends, mixed language, negation, quoted dialogue, partial selection and exact source spans. Record host/model/version and bundle identity, preserve exact source labels and distinguish fixture validation, scoped agent meaning judgments and unavailable subjective/human parity. Do not require a fluent human reviewer for POC delivery per FR-024/026, US6/AC1 and SC-002/004/005/007 (partial).
- [X] T172 RETIRED by owner decision 2026-10-28: all latency targets withdrawn; no performance pass is claimed. Historical optimization request retained for context: HIGH [F5] Continue T157's broader Windows scale qualification using measured bottlenecks in src/novel_creator/storage.py or src/novel_creator/context.py; retain all history validation, byte/object hashes, root/path/reparse/index guards, private-candidate checks, lock/worker lifetime, fresh branch/CAS, cache and recovery protections. The final ordinary-layout large run has read p95 3.453516100s and a save timeout on attempt 27 with no valid save p95; the separately recorded packed/direct-Git run and 100-exchange POC run do not establish ordinary-layout full-scale compliance. After justified repairs, run tests/performance/benchmark_records.py for 30 reads/30 saves at 100 sessions, 5,000 exchanges, 10,000 active assertions and at least 25 MiB; record cold read, raw timings, failures/timeouts, machine/runtime/filesystem and cache/packing configuration in tests/evaluations/performance.md against unchanged read <=2s/save <=1s targets. Keep this qualification separate from usable POC readiness per plan: performance goals, target platforms and scale/scope (partial).
- [X] T173 COMPLETED for the owner-amended functional scope (2026-10-28), without latency, novice/manual or universal-host qualification claims. Original reconciliation scope: MEDIUM [F6] Reconcile broader release qualification carried by T158 after T168-T172 in tests/evaluations/release-readiness.md and tests/evaluations/platform-results.md. Map all six stories, SC-001-009 and applicable quickstart scenarios to source-specific current evidence; retain the Phase 21 scope override excluding novice/manual prerequisites, separate POC readiness from scale/semantic/native qualification, and never convert unknown outcomes into passes. Verify affected Linux/Windows tests, independent wheel/resource identity, supported host/filesystem combinations and explicit skips/durability limits when changes invalidate prior evidence; review applicable constitution obligations and preserve deferred macOS, drafting, dashboard and additional hosts per FR-026, plan: incremental verified release and Constitution IX/XI (partial).


### T169 interruption checkpoint - 2026-10-27

T168 remains verified complete. T169 AUTH_PARTIAL was dispatched in both
languages, but supported public wait/read coordination calls timed out without
usable observations. Local Git inspection confirms the English save at sequence
8; its display remains unverified. Icelandic remains at the known fresh-resume
sequence 7 with an uncommitted pending receipt preserved. The child-reported
encoding concern is not corroborated by current snapshot/payload/receipt text.
No scenario was resent and no pending work was retried or replaced.
AUTH_NONACCEPT is prepared but unsubmitted. T169-T173 stay unchecked.
See tests/evaluations/phase22-status-20261027.md for evidence and safe resumption.

### T169–T173 continuation checkpoint — 2026-10-28

Public chat tools recovered. Existing outcomes were checked before further dispatch; the original English AUTH_PARTIAL was not replayed, and Icelandic recovered the same unchanged pending bundle once. T169, T170 and T171 are now complete for the explicitly authorized automated delegated scope. Original failures and source/display distinctions across automatic app continuations remain preserved. The full-scale ordinary-layout Windows run completes all 30 reads/30 saves without errors/timeouts: read p95 1.028736700s passes, save p95 3.067419500s misses <=1s. No production safeguard or target changes. T172 remains unmet; T173's source/platform/story/SC reconciliation is recorded provisionally without closing its unmet prerequisite. See tests/evaluations/phase22-resumption-20261028.md, windows-phase22-performance-20261028.md and phase22-release-assessment-20261028.md. No novice/manual recruitment is needed for the delivered POC.

### T172 profiling follow-up — 2026-10-28

Preserved existing dirty work and tested three source-free save scheduling
alternatives using 20 fresh-worker saves on full ordinary-layout fixtures.
Reducing history or initial hash concurrency and eliminating first-guard/history
overlap all fail to improve their matched controls. Both guards and counted
history/object/byte reads execute on every save. No runtime/harness change is
retained. The independent 30-read/30-save qualification re-verifies unchanged:
read p95 1.028736700s passes; save p95 3.067419500s misses <=1s. T172 and
dependent T173 remain unchecked. Exact samples, source identity, rejected
alternatives and reproducible verification are in
tests/evaluations/windows-phase22-save-investigation-20261028.md.

### T172 next bottleneck: private-candidate tree construction — 2026-10-28

Eight balanced fresh-worker full-scale ordinary-layout saves investigate the
recorded 0.196–0.348s `write-tree` stage. Command-local fscache shows no gain;
separate activation tracing finds no cache activation for this command, with a
passing `status` positive control. Trace2 narrows the internal cost to tree
updates; it does not justify removing object-existence checks or durable writes.
Missing-object rejection passes in SHA-1/SHA-256 with both command variants.
All eight saves succeed with complete guards and counted reads/hashes. No
production change is retained and no new p95 is claimed. T172 and T173 remain
unchecked. Evidence: tests/evaluations/windows-phase22-write-tree-20261028.md.

### T172 autonomous deeper investigation — 2026-10-28

Completed four guarded full-scale saves, eight same-index existing-tree replays
and independent lookup/type/access, hash/compression and scratch-durability
probes. Ordinary existence checks remain enabled; confirmed HEAD/live index are
unchanged by probes. Timings do not establish an additive native decomposition
or justify skipping writes/checks. A sampled saturated CPU and low available
memory are recorded with explicit limits. A distinct source-free lexical parent-
prefix prototype then completes eight full-scale fresh-worker saves with all
guard/hash/history/leaf counts retained, but demonstrates no improvement and is
not retained. No runtime/harness change or new p95 claim. T172 and T173 remain
unchecked; existing source-specific platform/wheel evidence stays unchanged.
See tests/evaluations/windows-phase22-tree-components-20261028.md and
windows-phase22-parent-prefix-20261028.md for executed sources and verifiers.

### T172 matching-source Windows Git instrumentation — 2026-10-28

Built isolated unmodified/instrumented Git controls from exact upstream release
commit f8165afd89b0c190677a093f20894f5fce12f97a. Eight SHA-1/SHA-256 checks
match tree identities and retain missing-object rejection. Sixteen full-scale
fresh-worker saves retain complete guards and hashes. Four native owner-thread
profiles separate lookup, buffer assembly, object-write remainder, deflate and
flush timing with nested exclusive accounting. These use MSVC/zlib1.3.1 and
are not installed-distribution qualification. Initial low-load gating succeeds
but no instrumented command stays within its CPU threshold; a stricter bounded
follow-up records not_measured before fixture creation. Build/replay tooling and
all raw source/executable identities are preserved. No product optimization,
new p95 pass or safeguard change; T172 and T173 stay unchecked. Evidence:
tests/evaluations/windows-phase22-native-profile-20261028.md.


## Phase 23: Convergence

Assessment date: 2026-10-28. The Phase 21 single-user POC remains usable;
T168-T171 retain their completed automated delegated scope. Historical novice
and manual prerequisites remain superseded for POC delivery. These tasks carry
forward the two remaining broader qualification gaps from T172/T173; they do
not authorize target relaxation, safeguard removal or relabeling unavailable
native/human/subjective evidence as passing. Current source/resource bytes match
the retained Phase 21 wheel. Retained 30-run arithmetic is rechecked here, not a
new benchmark or a fresh full-suite/host evaluation.

- [X] T174 RETIRED by owner decision 2026-10-28: all latency targets withdrawn; no performance pass is claimed. Historical optimization request retained for context: HIGH [F1] Complete the remaining Windows full-scale save qualification carried by T172 in src/novel_creator/storage.py or src/novel_creator/context.py and tests/evaluations/performance.md. The current ordinary-layout 30-read/30-save result has no operation failures/timeouts, read p95 1.028736700s passing <=2s, and save p95 3.067419500s missing <=1s; the subsequent scheduling, parent-prefix and native Git investigations retain no production optimization, and the stricter native profiling follow-up is not_measured. Use the recorded bottlenecks and rejected alternatives to justify any next optimization; retain complete history validation, object/byte hashes, path/reparse/root/index guards, private-candidate checks, lock/worker lifetime, fresh branch/CAS, recovery and cache protections. Verify affected invariants and repeat tests/performance/benchmark_records.py for 30 reads/30 saves at 100 sessions, 5,000 exchanges, 10,000 active assertions and >=25 MiB on the ordinary supported Windows layout, recording cold read, raw samples, failures/timeouts, source/runtime/hardware/filesystem and cache/packing configuration against unchanged targets. Keep diagnostic/custom-Git timings separate from supported-distribution qualification and POC usability per plan: performance goals, target platforms and scale/scope; T172 (partial).
- [X] T175 COMPLETED for the owner-amended functional scope (2026-10-28), without latency, novice/manual or universal-host qualification claims. Original reconciliation scope: MEDIUM [F2] Finalize broader release qualification carried by T173 after T174 in tests/evaluations/release-readiness.md and tests/evaluations/platform-results.md, using tests/evaluations/phase22-release-assessment-20261028.md as the provisional six-story/SC-001-009/quickstart mapping. Reconcile the resulting performance outcome and any changed runtime/resource identity with current Linux/Windows tests, independent wheel/bundle evidence, supported host/filesystem combinations, explicit skips and durability limits; rerun checks invalidated by repairs and record unresolved qualification honestly. Preserve the completed automated delegated scenario scope, distinguish native input, agent judgments and unavailable subjective/human results, retain the Phase 21 exclusion of novice/manual prerequisites, and keep macOS, drafting, dashboard and additional hosts deferred per FR-026, plan: incremental verified release, Constitution IX/XI; T173 (partial).


### T174 stderr-pipe investigation; T175 pending — 2026-10-28

Completed a distinct source-free experiment removing unused checked-Git stderr
capture while retaining unchecked diagnostics. Real SHA-1/SHA-256 stdout/binary-
input/sanitized-failure checks pass. Eight component batches per policy confirm
16 versus zero reader threads and medians 0.602102700/0.538249500s. Eight fresh-
worker full-scale ordinary-layout saves retain both complete guards and all
expected hashes/objects. Current/prototype medians 6.261266500/6.255118250s under
high, variable CPU load show no complete-save improvement. No runtime change is
retained. Preserve the original sandbox hard-link failure and corrected diagnostic
reader-count assumption separately. The successful normal-access run and read-only
verifier exit 0. No new qualification p95 or broader test/wheel claim; retained
read/save p95 remain 1.028736700/3.067419500s. T174 and dependent T175 remain
unchecked; T172/T173 are unchanged. Evidence and reproduction:
tests/evaluations/windows-phase23-stderr-pipe-20261028.md.


### Final functional qualification — complete, 2026-10-28

The owner withdrew all read/save latency targets and deferred optimization.
T172/T174 are explicitly retired requirements, not measured target passes;
T173/T175 are complete for the current single-user functional scope. Earlier
unchecked tasks retain historical native/human/scope evidence and do not reopen
retired timing or novice/manual prerequisites. No active POC delivery work remains.

Fresh corrected suites: Windows 178 total, 176 passed and two explicit real-
symlink privilege skips; Linux/WSL 178 total, 175 passed and three Windows-junction
skips. Both exit 0. The four policy regressions verify informational slow reads/
saves while keeping errors/timeouts failing. The same offline wheel independently
passes Windows/Linux source/resource identity and installed initialization/save/
reopen checks. Spec Kit Bash smoke passes with the existing cached jq. Initial
sandbox/temp-location/tool-PATH failures remain visible, separately from passing
final runs. No product runtime/resource/dependency or safeguard changes, new
performance qualification claim, provider call, real-novel edit, commit or push.

Current report: tests/evaluations/final-functional-qualification-20261028.md.
Source and evidence manifest: tests/evaluations/final-functional-manifest-20261028.json.
Start here: docs/poc-quickstart.md. All six stories and SC-001-SC-009 retain
source-specific structural and labeled delegated coverage; subjective literary
quality, broader native-host combinations and physical power-loss durability
remain unmeasured. macOS, additional hosts, dashboard and drafting remain deferred.
