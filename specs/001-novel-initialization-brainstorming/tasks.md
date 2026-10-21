# Tasks: Novel Initialization and Guided Brainstorming

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts](contracts/cli.md), and [quickstart.md](quickstart.md).
**Governance**: Constitution 1.0.0. No implementation or product verification has
occurred. Every checkbox starts unchecked.

Execution status: T001–T011 implemented; T012 actual-host evidence remains
unverified. T013 records a **BLOCKED** gate decision, not a positive gate pass.
No T014+ work has begun; see implementation-ledger.md and
../../tests/evaluations/host-capture.md.

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
- [ ] T012 Define and execute the actual Codex spike in tests/evaluations/host-capture.md: save before display, at least two further automatic turns without reinvocation, fresh-chat recovery, interruption after commit/before display, identical retry and failed-save disclosure; record host/model/version, messages, receipts and commit checkpoints. Mark unavailable evidence unverified; mocks alone do not pass (FR-008–009, FR-014, FR-025; SC-009).
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

- [ ] T014 [P] [US1] Write initialization contract tests in tests/contract/test_initialize.py covering empty/unknown preferences, supplied original concept versus interpretation, stable identity after title change and exact CLI responses (FR-001–003; SC-002).
- [ ] T015 [P] [US1] Write installation integration tests in tests/integration/test_install.py for independent Git roots, nested-repository rejection, recognized-novel continuation, unrelated content preservation, partial bootstrap retry, existing AGENTS.md and missing prerequisites/Git identity (FR-003, FR-025).
- [ ] T016 [US1] Implement Novel Project/bootstrap validation against foundation schemas in src/novel_creator/validation.py: stable UUID, BCP-47 manuscript language en default/is supported, state: unknown for skipped answers, original concept retained as a preserved bootstrap input artifact, valid field JSON Pointer/digest sources, explicit system defaults and actual message-only canon authorization. Enforce routine_checkpoint on_request/session_close/every_exchange without waiving safeguards (FR-001–003, FR-013).
- [ ] T017 [US1] Implement independent-repository initialization and manifest/checksum bundle copying in src/novel_creator/install.py, including the installed .novel-creator/run.py launcher, resources, ignores and line-ending configuration; preserve existing content/AGENTS.md and report partial initialization without inventing a confirmed checkpoint (FR-003, FR-022, FR-025).
- [ ] T018 [US1] Wire init and project-setting revisions through src/novel_creator/cli.py and src/novel_creator/records.py; accept unknowns, persist supplied preferences without re-questioning, preserve identity through title changes and offer recognized-novel continuation rather than recreation (FR-001–003).
- [ ] T019 [US1] Author conversational setup in workflows/initialize.md and adapters/codex/skills/novel-init/SKILL.md covering all FR-002 preferences, bundled answers, skipped uncertainty, temporary title, no inferred canon, save-before-emit and optional brainstorming after successful initialization (FR-001–003, FR-025).
- [ ] T020 [US1] Execute the independent initialization journey in tests/integration/test_initialize_journey.py using no-concept and supplied-concept fixtures, reopen/settings changes and interrupted bootstrap; verify tests T014–015 pass and no inferred facts become canon (SC-002, SC-009).
- [ ] T021 [US1] Add slice onboarding in README.md and run/record SC-001 in tests/evaluations/novice-initialization.md: at least 4 of 5 novice evaluators reach the brainstorming invitation within 10 minutes without outside assistance; unavailable human results remain unverified (FR-026).

**Checkpoint**: US1 is demonstrable; brainstorming is offered, not required.

## Phase 4: US2 — Develop Ideas through Creative Conversation (P1)

**Goal**: Guided/open exploration adapts to preferences and the user's next-turn
direction, without requiring later drafting or full resumption features.
**Independent test**: From a prepared brief/session fixture, explore premise,
character and setting; switch modes, redirect topic and reduce suggestions.

- [ ] T022 [P] [US2] Write mode/redirection workflow tests in tests/contract/test_guidance.py using prepared sessions, asserting guided default, next-response switching, topic changes and preserved prior records (FR-004–006; SC-007).
- [ ] T023 [P] [US2] Define guidance evaluation scenarios in tests/evaluations/guidance-cases.md for constructive challenge, novice explanations, proportional suggestions, host-provided voice transcription, genre/complexity/style adaptation and requests for fewer suggestions (FR-005–007).
- [ ] T024 [US2] Implement Brainstorming Session lifecycle/mode behavior against T006 schemas in src/novel_creator/records.py: mode guided/open, state open/closed, guided default, saved mode on resume and explicit reopen request; test transitions without introducing later-phase schema dependencies (FR-004, FR-008).
- [ ] T025 [US2] Author shared guidance and initial English resources in workflows/brainstorm.md and languages/en.md; normally ask one focused question, offer meaningful alternatives without prescribing methodology, honor redirection/reduced suggestions and accept host voice transcriptions as text (FR-004–007).
- [ ] T026 [US2] Implement the thin brainstorming entry in adapters/codex/skills/novel-brainstorm/SKILL.md using shared resources, prepared context and production exchange save; keep novelist/coach/Guardian as responsibilities rather than an agent scheduler (FR-004–007, FR-009, FR-025).
- [ ] T027 [US2] Run/record actual host guidance cases in tests/evaluations/guidance-results.md and tests/integration/test_guidance_journey.py; every mode/topic request affects the next saved/displayed response, with no lost work and no unsaved creative suffix (SC-007).
- [ ] T028 [US2] Document brainstorming usage in README.md and record the five-novice usefulness/control evaluation in tests/evaluations/novice-guidance.md; require at least 4 of 5 ratings >=4/5 and distinguish human evidence from automated assertions (FR-026; SC-007).

**Checkpoint**: US2 works against prepared records independently of later stories.

## Phase 5: US3 — Resume without Retelling the Story (P1)

**Goal**: Automatically capture and inspect sourced story information, manage
multiple sessions and recover through fresh interactions/failures.
**Independent test**: Start with two saved sessions, reopen in a fresh interaction,
resume one, create another and recover all designated records with sources.

- [ ] T029 [P] [US3] Write session/context/inspection CLI tests in tests/contract/test_context.py for list/start/resume/close, duplicate names, session focus/mode, source links, derived summaries and explicit incomplete coverage (FR-008–010, FR-019–020).
- [ ] T030 [P] [US3] Write recovery integration tests in tests/integration/test_recovery.py for pending save inspection/retry, lost receipts, interrupted display, stale locks, published-ref index cleanup without decision replay, save-failure pauses and preserving unrelated Git changes; no silent overwrite, rollback or inferred acceptance (FR-014; SC-009).
- [ ] T031 [US3] Implement typed Idea, Story Element, Relationship and Unresolved Question record handling against T006 schemas in src/novel_creator/records.py: statuses proposed/accepted/rejected/unresolved/superseded, element_type character/location/event/plot_thread, question state open/resolved, nullable alternative_group_id, explicit relationship direction and sourced time/perspective. Allow duplicate names; never reject unselected alternatives implicitly (FR-009–010, FR-019–020).
- [ ] T032 [US3] Implement sourced extraction/correction instructions in workflows/brainstorm.md and typed revision support in src/novel_creator/records.py; capture conversations, ideas, characters, relationships, plot/world/event details, alternatives, questions and decisions every exchange, retaining erroneous versions and never promoting unaccepted captures (FR-009–010, FR-012).
- [ ] T033 [US3] Implement committed session listing, focused context and source-backed history/connection inspection in src/novel_creator/context.py and src/novel_creator/cli.py; summaries are derived with source/checkpoint references, cannot hide open contradictions, and missing records return unavailable coverage (FR-008, FR-019, FR-022).
- [ ] T034 [US3] Implement recover inspection and explicit unchanged-payload retry in src/novel_creator/storage.py and src/novel_creator/cli.py according to contracts/cli.md and contracts/storage.md; distinguish committed/pending/cleanup-needed work, safely synchronize only managed index entries for published saves without replay or ref reset, reject stale changed retries and lift write pauses only after successful recovery (FR-014).
- [ ] T035 [US3] Author fresh-chat resumption/inspection in workflows/resume.md, adapters/codex/skills/novel-resume/SKILL.md and adapters/codex/skills/novel-inspect/SKILL.md; recover saved focus, mode, decisions and questions without requesting retelling; offer interrupted saved responses without claiming they were seen (FR-008, FR-019, FR-025).
- [ ] T036 [US3] Execute resumption/capture/correction integration and real-host cases in tests/integration/test_resume_journey.py and tests/evaluations/resume-results.md: three sessions plus a fresh interaction recover all 20 designated ideas, 10 explicit decisions and 5 questions with correct state/source; run T029–030 and distinguish structural results from host judgments (SC-003, SC-009).
- [ ] T037 [US3] Document session listing/resume/close, inspecting knowledge and safe recovery in README.md; include last-confirmed checkpoint examples, save-before-continuation behavior and clear failure disclosure (FR-026).

**Checkpoint**: Full persistence/resumption slice works; prepared acceptance
records can support testing before US4 semantic acceptance integration.

## Phase 6: US4 — Establish and Revise Canon (P1)

**Goal**: Natural, unambiguous acceptance establishes only selected facts;
revision/reversal retains history, impact and protected authority.
**Independent test**: Prepared canon/proposals test clear, ambiguous, partial and
rejected acceptance, explicit revisions and protected-direction conflicts.

- [ ] T038 [P] [US4] Write authority/review tests in tests/unit/test_authority.py covering ambiguous/partial/clear acceptance, sourced revision/reversal and manuscript protection. Test each routine_checkpoint value, default on_request, requested and session-close triggers, every-exchange summaries, pause/continuation and no delay to saves or repeated canon approval (FR-010–013).
- [ ] T039 [P] [US4] Author acceptance fixtures in tests/fixtures/en/acceptance.json with at least 12 clear-acceptance and 12 non-acceptance cases, expected selected propositions and source spans; include explicit direction conflicts and five deliberate canon revisions for later bilingual pairing (SC-004, SC-006).
- [ ] T040 [US4] Implement Creative Decision/Revision handling against T006 schemas in src/novel_creator/records.py and src/novel_creator/validation.py: action accept/reject/correct/revise/reverse/resolve/defer, actual user_message_ref plus precise span, selected/prior/result/affected refs and retained origins; artifact provenance alone never authorizes canon (FR-011–013).
- [ ] T041 [US4] Add deterministic authorization, partial-selection and supersession checks in src/novel_creator/validation.py and src/novel_creator/records.py; require sourced decisions for every canon-affecting element/relationship/assertion, retain prior/current states, exclude superseded facts from current canon, and prevent preferences from waiving protected direction or manuscript safeguards (FR-010–013).
- [ ] T042 [US4] Implement direct-dependency impact traversal and revision inspection in src/novel_creator/context.py; expose prior/result refs and all directly linked affected elements without claiming detection of unrecorded dependencies or modifying linked manuscripts (FR-012–013).
- [ ] T043 [US4] Author workflows/authority.md and integrate workflows/brainstorm.md: clear identifiable acceptance/revision needs no repeated approval, ambiguity asks one focused question and protected-direction conflicts require clarification. Implement routine checkpoints on_request (default), session_close and every_exchange with summaries of proposals/decisions/questions and a pause of agent-initiated exploration until user direction; checkpoints never delay saving or reapprove accepted facts (FR-011–013, FR-017).
- [ ] T044 [US4] Execute acceptance/revision journeys in tests/integration/test_canon_journey.py and tests/evaluations/authority-results.md using T039; verify intended selected facts, rejection/alternatives, five revisions with origin/impact/history and unchanged approved manuscript hashes; report agent judgments separately (SC-004, SC-006).
- [ ] T045 [US4] Document accepting, correcting, revising/reversing and inspecting canon in README.md with explicit protected-direction and manuscript boundaries; link source/impact examples without implying future drafting exists (FR-026).

**Checkpoint**: Canon transitions have observable authority, source and history.

## Phase 7: US5 — Catch Continuity Problems during Exploration (P1)

**Goal**: Significant conflicts interrupt the next response with evidence;
intentional techniques and unreadable context preserve creative control.
**Independent test**: Prepared conflicts across six categories and recorded lies,
unknown timing and reader revelations exercise all resolution dispositions.

- [ ] T046 [P] [US5] Write perspective/time/hold tests in tests/unit/test_continuity.py for author truth, character knowledge/belief and reader revelation, unknown versus false/absent information, canon mutation holds, deferred conflicts and safe proposal-only continuation (FR-015–018, FR-021).
- [ ] T047 [P] [US5] Author sourced six-category contradiction/intentional-technique fixtures in tests/fixtures/en/continuity.json covering motivation, chronology, knowledge, plot dependency, world rules and relationships, with expected next-response intervention and non-blocking opportunities (FR-015–019; SC-005).
- [ ] T048 [US5] Implement assertion/time/finding typed handling against foundation schemas in src/novel_creator/records.py and src/novel_creator/validation.py: perspective author_truth/character_knowledge/character_belief/reader_revelation, required character holder/reader audience, truth_state affirmed/denied/unknown, chronology/revelation precision known/partial/unknown with null unknown bounds, nullable supersedes, finding assessment conflict/uncertainty/opportunity, severity significant/advisory, all dispositions and complete/incomplete/not_applicable review coverage (FR-015–018, FR-021).
- [ ] T049 [US5] Implement availability scope, continuity review and hold enforcement in src/novel_creator/context.py and src/novel_creator/validation.py; significant/deferred conflicts block affected promotion, unreadable relevant canon holds affected changes until restoration, unknown scope holds all canon, and unsafe journal predecessors reject all saves (FR-016–018; SC-009).
- [ ] T050 [US5] Author workflows/continuity.md and integrate Guardian-before-development in workflows/brainstorm.md; cite sources/consequences, distinguish uncertainty from proven conflict, offer reject/revise/canon-change/intentional/defer resolutions, honor unambiguous revision authorization and keep opportunities non-blocking (FR-015–019).
- [ ] T051 [US5] Execute fault/continuity integration in tests/integration/test_continuity_journey.py using T047 and temporary damaged/restored records; verify affected-canon holds, safe proposal saving, no unsafe-chain append and revalidation before lifting holds (SC-005, SC-009).
- [ ] T052 [US5] Execute real-host continuity evaluation in tests/evaluations/continuity-results.md: every designated significant conflict interrupts conflicting development in the next response, every intentional technique remains distinguishable, resolutions persist and no opportunity becomes canon without acceptance (SC-005).
- [ ] T053 [US5] Document resolving/defering contradictions, incomplete checks and restored-context resumption in README.md; state agent-judgment limits and unavailable information explicitly (FR-026).

**Checkpoint**: Core US1–5 loop works with authority-preserving continuity.

## Phase 8: US6 — Retain Language and Platform Independence (P2, release-required)

**Goal**: Full English/Icelandic workflows and independently readable, connected,
versioned story information without Codex or a dashboard.
**Independent test**: Paired language journeys and an independent consumer recover
all designated structured information without interpreting conversation prose.

- [ ] T054 [P] [US6] Write Unicode/version/bundle-independence tests in tests/contract/test_portability.py for Icelandic names/characters, mixed language, duplicate names, unknown language-specific assumptions, unsupported schemas and framework-checkout removal (FR-020–025).
- [ ] T055 [P] [US6] Pair English acceptance/continuity fixtures in tests/fixtures/is/acceptance.json and tests/fixtures/is/continuity.json; preserve meanings/source spans, include Icelandic false friends/diacritics and mixed-language examples, and cover setup/guidance/capture/acceptance/continuity with no English-only assumptions (FR-024).
- [ ] T056 [US6] Implement languages/is.md and modular language-resource selection in src/novel_creator/context.py and workflows/initialize.md; preserve configured manuscript language, honor interaction-language requests, default to en when unspecified and keep all core schemas genre/language independent (FR-024–025).
- [ ] T057 [US6] Document serialized ownership, references, schema readability and explicit future incompatible-migration/recovery requirements in docs/record-format.md; implement unsupported-version errors/holds in src/novel_creator/validation.py, retaining IDs/history and requiring a preserved Git checkpoint before any future migration (FR-022–023).
- [ ] T058 [US6] Build an independent consumer in tests/integration/independent_reader.py and tests/integration/test_consumer.py without importing the production reducer; recover every designated entity, relationship, event ordering, perspective/timing, current/history and decision source from committed bundles, including cache deletion and missing/unsupported records (SC-008).
- [ ] T059 [US6] Validate installed-bundle operation after removing framework-path access in tests/integration/test_portable_install.py and run paired language journeys in tests/integration/test_languages.py; verify novel records need neither original agent nor dashboard and T054–055 cases preserve Unicode/meaning (SC-002, SC-008).
- [ ] T060 [US6] Execute/record full English/Icelandic host evaluations in tests/evaluations/language-results.md, reusing T023/T039/T047 expectations and SC-002–007 counts; record host/model/version and separate structural checks, agent judgments and human approvals, marking unsupported/unavailable runs unverified (FR-024, FR-026).
- [ ] T061 [US6] Publish portable record/host/language onboarding in README.md and docs/record-format.md, including installed resources, dependencies, no automatic pushes, host voice responsibility and platform-specific support limitations; do not claim untested language or host support (FR-022–026).

**Checkpoint**: US6 is required before release despite P2 delivery order.

## Phase 9: Polish and cross-cutting release verification

- [ ] T062 Add representative dataset generation and repeatable benchmarks in tests/performance/benchmark_records.py: 100 sessions, 5,000 exchanges, 10,000 active assertions, 25 MiB JSON, 30 warm read/save runs with p95 read <=2s and validate+local-save <=1s excluding model latency; report cold reads and hardware/OS/Python/Git details in tests/evaluations/performance.md (plan performance targets).
- [ ] T063 Optimize only demonstrated bottlenecks in src/novel_creator/context.py and src/novel_creator/storage.py; if caches are needed, label them derived, bind to schema/HEAD, prove deletion/rebuild/staleness handling in tests/integration/test_cache.py and rerun T062 without creating competing authority.
- [ ] T064 Validate installation, JSON CLI, locks, interruption/durability and language fixtures on Linux/macOS/Windows in tests/evaluations/platform-results.md; record exact host/OS/filesystem versions and unsupported flush guarantees, and restrict claimed support to verified combinations (FR-014, FR-024–026).
- [ ] T065 Run the full automated suite, existing tests/speckit-smoke.sh and every quickstart.md scenario; record actual commands/results, all Story 1–6 acceptance cases and SC-001–009 outcomes in tests/evaluations/release-readiness.md, keeping unavailable human/host/performance evidence unverified and release-blocking where required.
- [ ] T066 Review constitution 1.0.0 compliance and close coverage/authority/portability gaps in tests/evaluations/release-readiness.md; explicitly preserve future-work boundaries for drafting, dashboard, additional hosts and incompatible migrations, with no implicit waiver of mandatory gates.
- [ ] T067 Update README.md and specs/001-novel-initialization-brainstorming/quickstart.md to match verified commands, install prerequisites, recovery and limitations; remove design-time runnable-status disclaimers only for actually delivered/verified behavior, and report remaining unmet release gates honestly.

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
- [ ] T069 CRITICAL [F4] Complete the actual Codex host-capture evaluation in tests/evaluations/host-capture.md and record the resulting gate decision in docs/development.md, including exact save-before-display text, two subsequent automatic turns, genuine fresh-chat recovery, interrupted display, identical retry and visible failure disclosure with real host/model/version and checkpoint evidence; retain BLOCKED/unverified status if evidence is unavailable, and return to adapter planning before any T014+ work. Finish T012 and reassess T013 per FR-009, FR-025, SC-009 and plan: blocking native-host capability spike (partial).
- [ ] T070 CRITICAL [F5] After the host gate passes, deliver the missing initialization slice in src/novel_creator/install.py, src/novel_creator/cli.py, src/novel_creator/validation.py, workflows/initialize.md and adapters/codex/skills/novel-init/SKILL.md, with tests/contract/test_initialize.py and tests/integration/test_install.py plus test_initialize_journey.py; complete T014–T021 for skipped/combined preferences, preserved original brief, stable identity/settings changes, independent pinned installation, existing-content protection and optional brainstorming. The init dispatch currently returns unavailable. Trace to FR-001–003, US1/AC1–5 and SC-002 (missing).
- [ ] T071 CRITICAL [F6] After the host gate passes, deliver shared guidance in workflows/brainstorm.md and languages/en.md, the thin adapters/codex/skills/novel-brainstorm/SKILL.md entry and session-mode behavior in src/novel_creator/records.py; complete T022–T028 with tests/contract/test_guidance.py, tests/integration/test_guidance_journey.py and actual guidance evaluations for guided defaults, next-response switches/redirection, reduced suggestions, accessible constructive coaching and host-provided transcription. These production resources are absent. Trace to FR-004–007, US2/AC1–4 and SC-007 (missing).
- [ ] T072 CRITICAL [F7] After the host gate and prerequisite session behavior pass, implement committed session listing, start/resume/close transitions, focused context and source/history inspection in src/novel_creator/context.py, src/novel_creator/cli.py and src/novel_creator/records.py, with workflows/resume.md and adapters/codex/skills/novel-resume/SKILL.md and novel-inspect/SKILL.md; finish T029, T033, T035–T037 using tests/contract/test_context.py and tests/integration/test_resume_journey.py, proving recovery of 20 ideas, 10 decisions and 5 questions across three sessions and a fresh interaction. Current context/inspect/session-list commands are placeholders. Trace to FR-008, FR-019, FR-022, US3/AC2–3 and SC-003 (missing).
- [ ] T073 CRITICAL [F10] After the original authority prerequisites pass, implement the missing Continuity Guardian workflow in workflows/continuity.md and workflows/brainstorm.md and scope/hold enforcement in src/novel_creator/context.py and src/novel_creator/validation.py; complete T046–T053 with tests/unit/test_continuity.py, six-category fixtures, tests/integration/test_continuity_journey.py and real-host continuity-results.md. Distinguish perspectives, unknown timing, intentional techniques, deferred conflicts and non-blocking opportunities; interrupt conflicting development in the next response, hold affected canon on unreadable context, hold all canon for unknown scope and reject unsafe journal extension. Trace to FR-015–019, FR-021, US5/AC1–5 and SC-005/009 (missing).
- [X] T074 HIGH [F2] Harden committed-history input handling in src/novel_creator/storage.py and CLI error conversion in src/novel_creator/cli.py, with regressions in tests/integration/test_storage.py and tests/contract/test_cli.py for non-object committed JSON and malformed local recovery metadata; a committed exchange containing [] currently raises an uncaught AttributeError. Return one structured unavailable-context/error result with affected scope and no authoritative mutation, rather than a traceback, completing T010's error contract per FR-014, SC-009 and plan: machine-readable CLI boundary (partial).
- [X] T075 HIGH [F3] Preserve the last verifiable journal checkpoint and explicit damaged/unsupported references when committed-history validation fails in src/novel_creator/storage.py, surfacing them through src/novel_creator/cli.py; add tests/integration/test_storage.py and tests/contract/test_cli.py cases with a valid bootstrap followed by a damaged or unsupported successor. The current unsupported-successor probe returns last_confirmed_checkpoint: null despite the valid prefix. Never report the invalid successor as saved or allow unsafe extension. Trace to FR-014, SC-009, T010 and plan: unavailable-context recovery boundary (partial).
- [ ] T076 HIGH [F8] After the original capture prerequisites pass, complete sourced extraction/correction in workflows/brainstorm.md and src/novel_creator/records.py, reusing the existing schemas and reducer; finish T031–T032 and their T036 journey coverage for ideas, characters, plot/world details, relationships, events, alternatives, questions and decisions on every exchange, preserving prior erroneous captures and source/status distinctions. Structural record support alone does not implement automatic capture. Trace to FR-009–010, FR-012 and US3/AC1/4 (partial).
- [ ] T077 HIGH [F9] After the original canon prerequisites pass, complete authority semantics in src/novel_creator/validation.py, src/novel_creator/records.py and src/novel_creator/context.py and shared workflows/authority.md and workflows/brainstorm.md; finish T038–T045 using tests/unit/test_authority.py, acceptance fixtures and tests/integration/test_canon_journey.py. Cover precise partial selection, ambiguous/non-acceptance, revision/reversal with supersession and directly linked impact, explicit-direction clarification and on_request/session_close/every_exchange summaries and pauses without repeated approval or manuscript edits. The foundation checks sources but lacks this full workflow and evidence. Trace to FR-010–013, US4/AC1–5 and SC-004/006 (partial).
- [ ] T078 HIGH [F11] After the host gate passes and within the original recovery slice, implement recover inspection and explicit unchanged-payload retry/managed-index cleanup in src/novel_creator/storage.py and src/novel_creator/cli.py, with tests/integration/test_recovery.py; complete T030/T034 for pending/published/cleanup-needed states, lost receipts, stale-lock inspection, original checkpoints, unrelated index/worktree preservation and lifting write pauses only after safe recovery. The command currently returns unavailable and published cleanup can leave writes paused indefinitely. Trace to FR-014, SC-009 and contracts/storage.md recovery requirements (missing).
- [ ] T079 HIGH [F12] After core stories pass, add modular language resources in languages/en.md and languages/is.md and resource selection in src/novel_creator/context.py and workflows/initialize.md; finish T054–T056, T059–T060 with paired tests/fixtures/en/ and tests/fixtures/is/ acceptance/continuity examples, tests/integration/test_languages.py and real bilingual evaluations. Verify setup, guidance, capture, acceptance and continuity, preserved names/meaning and mixed-language requests; Unicode serialization alone is insufficient. Trace to FR-024, US6/AC1, SC-002/004/005/007 and plan: bilingual release requirement (partial).
- [ ] T080 HIGH [F13] Complete independent reconstruction and portability verification in tests/integration/independent_reader.py, tests/integration/test_consumer.py, tests/integration/test_portable_install.py and tests/contract/test_portability.py, with docs/record-format.md covering ownership, references, schema compatibility and future incompatible-migration/recovery guidance; finish T054, T057–T059 and T061. Recover designated entities, event order, perspectives, sources and decision/current/history states without production-reducer imports, conversation re-extraction, framework access or a dashboard. Existing schemas and the disposable installed fixture are only partial evidence. Trace to FR-020–023, US6/AC2–3, SC-008 and plan: independent pinned novel bundle (partial).
- [ ] T081 HIGH [F14] Add tests/performance/benchmark_records.py and tests/evaluations/performance.md and complete T062–T063 against 100 sessions, 5,000 exchanges, 10,000 active assertions and 25 MiB JSON with 30 warm read/save runs, documented hardware/OS/Python/Git and separate cold results; meet p95 read <=2s and validate+local-save <=1s excluding model latency. Optimize only observed bottlenecks in src/novel_creator/context.py and src/novel_creator/storage.py; prove derived cache rebuild/staleness behavior if caches are justified. No benchmark or scale evidence exists. Trace to plan: performance goals and scale/scope (missing).
- [ ] T082 HIGH [F15] After the original story and performance prerequisites pass, complete T064–T066 in tests/evaluations/platform-results.md and tests/evaluations/release-readiness.md, recording Linux/macOS/Windows installation, JSON CLI, filesystem durability, locks/interruption, bilingual flows, all Story 1–6 acceptance cases and SC-001–009 outcomes; include actual novice initialization/guidance evidence from T021/T028, quickstart scenarios and constitution review. Current evidence covers the structural foundation only. Keep unavailable host/human/platform/performance results explicitly unverified and required unmet gates release-blocking. Trace to FR-026, SC-001–009, Constitution IX/XI and plan: release verification (partial).
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
- [ ] T089 HIGH [F4] Obtain genuine automatic-turn, save-before-display, fresh-chat, interruption, identical-retry and failure-disclosure evidence in tests/evaluations/host-capture.md and record the gate decision in docs/development.md; retain BLOCKED and revisit adapter planning when any required evidence is unavailable; fulfill the complete scope, prerequisites and acceptance evidence of T069 per FR-009, FR-025, SC-009, plan: blocking native-host capability spike (partial).
- [X] T090 HIGH [F18] Preserve failure context for a held novel writer lock in src/novel_creator/storage.py and src/novel_creator/cli.py: return the attempted exchange ID and last independently verifiable committed checkpoint when available, without stealing/removing the lock or mutating journal, receipts, HEAD or user index. Add real-repository and JSON CLI regressions in tests/integration/test_storage.py and tests/contract/test_cli.py for a saved bootstrap followed by a held-lock save, plus unborn/unreadable context where no checkpoint can safely be claimed. The current probe returns null for both fields despite a known confirmed save. Treat this as foundation remediation of T010 per FR-014, SC-009 and plan: truthful save-failure disclosure (partial).
- [ ] T091 HIGH [F8] Complete sourced automatic extraction and correction in workflows/brainstorm.md and src/novel_creator/records.py, preserving all required capture kinds, status and prior versions; fulfill the complete scope, prerequisites and acceptance evidence of T076 per FR-009–010, FR-012, US3/AC1/4 (partial).
- [ ] T092 HIGH [F9] Complete precise acceptance, revision/reversal, impact and review-checkpoint behavior in workflows/authority.md, src/novel_creator/validation.py, src/novel_creator/records.py and src/novel_creator/context.py; fulfill the complete scope, prerequisites and acceptance evidence of T077 per FR-010–013, US4/AC1–5, SC-004/006 (partial).
- [ ] T093 HIGH [F11] Implement safe pending/published/cleanup-needed inspection and unchanged-payload retry in src/novel_creator/storage.py and src/novel_creator/cli.py with tests/integration/test_recovery.py; fulfill the complete scope, prerequisites and acceptance evidence of T078 per FR-014, SC-009, plan: safe recovery (missing).
- [ ] T094 HIGH [F12] Complete modular English/Icelandic workflow resources, paired fixtures and actual bilingual evaluations in languages/, tests/fixtures/en/, tests/fixtures/is/ and tests/evaluations/language-results.md; fulfill the complete scope, prerequisites and acceptance evidence of T079 per FR-024, US6/AC1, SC-002/004/005/007 (partial).
- [ ] T095 HIGH [F13] Complete independent record reconstruction, installed-bundle portability and compatibility/recovery documentation in tests/integration/independent_reader.py, tests/integration/test_consumer.py, tests/integration/test_portable_install.py and docs/record-format.md; fulfill the complete scope, prerequisites and acceptance evidence of T080 per FR-020–023, US6/AC2–3, SC-008 (partial).
- [ ] T096 HIGH [F14] Build and measure the planned representative dataset and p95 read/save targets in tests/performance/benchmark_records.py and tests/evaluations/performance.md, optimizing only demonstrated bottlenecks; fulfill the complete scope, prerequisites and acceptance evidence of T081 per plan: performance goals and scale/scope (missing).
- [ ] T097 HIGH [F15] Complete actual platform, novice, story acceptance and release evidence in tests/evaluations/platform-results.md and tests/evaluations/release-readiness.md, keeping unavailable mandatory results unverified and release-blocking; fulfill the complete scope, prerequisites and acceptance evidence of T082 per FR-026, SC-001–009, Constitution IX/XI (partial).
