# Tasks: Novel Initialization and Guided Brainstorming

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts](contracts/cli.md), and [quickstart.md](quickstart.md).
**Governance**: Constitution 1.0.0. No implementation or product verification has
occurred. Every checkbox starts unchecked.

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
