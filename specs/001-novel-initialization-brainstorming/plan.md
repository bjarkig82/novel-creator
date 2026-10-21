# Implementation Plan: Novel Initialization and Guided Brainstorming

**Branch**: `work` (execution checkout; clarified spec pushed to `main` at `4393b94`)
**Feature selector**: `specs/001-novel-initialization-brainstorming`
**Date**: 2026-10-21 | **Spec**: [spec.md](spec.md)

## Summary

Deliver an independent Git-backed novel workspace with conversational setup,
guided/freeform brainstorming, persistent sessions, automatic per-exchange capture,
explicit canon acceptance/revision, and continuity intervention. Support English
and Icelandic before release. Codex skills load shared workflows and invoke a
small deterministic Python tool; no model API, custom AI runtime or dashboard.
Immutable exchange bundles own conversation and structured record revisions.
Current canon is derived from their validated committed chain. Preserve both
clarifications: save each exchange before continuing, and pause affected canon
changes while relevant canon is unreadable, permitting proposals where safe.

## Technical Context

**Language/Version**: Python >=3.11; Markdown workflows; UTF-8 JSON records.
**Primary Dependencies**: Git >=2.39; jsonschema >=4.23,<5; supported Codex host.
Lock resolved versions during implementation; no provider credentials in tool.
**Storage**: Independent local Git repository per novel; immutable JSON exchange
bundles with full structured record versions, local commit per confirmed save; prepare commits
with a private index and publish via an atomic expected-parent ref update.
Caches and summaries are explicitly derived; no database.
**Testing**: unittest, temporary real Git repositories, JSON Schema validation,
fault injection and subprocess contract tests; actual Codex bilingual scenarios
and five novice evaluators for the human success criteria.
**Target Platform**: Linux and Windows with Python and Git; capability
verification for each supported Codex host/version before claiming support.
macOS support and verification are deferred from the current release by the
user's scope decision on 2026-10-21.
**Project Type**: Installable local tooling and native agent skills.
**Performance Goals**: Deterministic read p95 <=2s and validation/local save p95
<=1s, 30 warm runs on a documented laptop and representative dataset; host model
latency excluded, cold-read time reported independently.
**Constraints**: No approved manuscript edits, no inferred approval, no automatic
push, no shared mandatory database/server, no novel dependence on framework path
or dashboard. Single director; reject stale/conflicting writes. See storage
contract for confirmed-save and recovery boundaries.
**Scale/Scope**: 100 sessions, 5,000 exchanges, 10,000 active assertions, 25 MiB
fixture; all six stories, 26 functional requirements and nine success criteria.

## Constitution Check

Gate evaluated before research and re-evaluated after Phase 1 design. PASS here
means design conformance, not implemented or tested product behavior.

| Principle | Pre-research gate | Post-design evidence / disposition |
|---|---|---|
| I. Simplicity | Native host; bounded local tool | PASS: no server, database, scheduler; journal justified by atomic save requirement |
| II. Platform independence | Shared workflows separated | PASS: adapter contract; no required Codex IDs in records; actual capture is a release gate |
| III. Human authority | Explicit decisions only | PASS: sourced decisions, legal state transitions, direction conflict holds; manuscript paths excluded |
| IV. Consistency/traceability | Distinct perspectives/history | PASS: assertions, temporal references, findings and impact links in data model |
| V. Guided collaboration | Guided default, resumable context | PASS: workflow contract specifies modes, redirection, suggestions and session recovery |
| VI. Portable Git data | Independent repository, clear owner | PASS: committed bundles sole authority; schema/version/recovery contract; derived caches disposable |
| VII. Languages/genres | English/Icelandic required | PASS: language resources and bilingual evaluation; no prescribed story structure |
| VIII. Responsibilities | Methodology/data/adapter distinct | PASS: source layout and read interfaces; dashboard/prompt-generation consumers deferred |
| IX. Verification | Structural and semantic evidence separate | PASS: quickstart maps SC-001–009; no drafting claims; host spike blocks release if unsuccessful |
| X. Accessible dashboard | No dashboard in this feature | Not applicable to dashboard delivery; text/host transcription interaction retained |
| XI. Incremental delivery | Usable workflow before dashboard | PASS: staged vertical slices below; onboarding and fresh-install validation required |

No violations or amendments. A failed host capability spike or incompatible
schema change must be resolved explicitly, not waived by this plan.

## Project Structure

### Documentation (this feature)

```text
specs/001-novel-initialization-brainstorming/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    ├── cli.md
    ├── storage.md
    └── agent-workflow.md
```

`tasks.md` is subsequent `$speckit-tasks` output and is not generated here.

### Planned framework source (not created by planning)

```text
pyproject.toml
src/novel_creator/
├── __main__.py
├── cli.py
├── install.py
├── records.py
├── storage.py
├── validation.py
└── context.py
schemas/v1/
├── exchange.schema.json
└── records.schema.json
workflows/
├── initialize.md
├── brainstorm.md
├── resume.md
├── authority.md
└── continuity.md
languages/
├── en.md
└── is.md
adapters/codex/
├── AGENTS.fragment.md
└── skills/novel-{init,brainstorm,resume,inspect}/SKILL.md
tests/
├── unit/
├── contract/
├── integration/
├── fixtures/{en,is}/
├── evaluations/
└── speckit-smoke.sh
```

**Structure Decision**: Source tooling validates and persists; shared resources
control creative procedure; Codex adapters only discover context and invoke
contracts. Existing Spec Kit scripts/skills remain development tooling. Novel
repositories receive a pinned `.novel-creator/` bundle, adapter skill entries,
bootstrap metadata, and `story/exchanges/` as detailed in the storage contract.

## Workflow and delivery sequence

Shared schema prerequisites: define all record types (including decisions,
assertions and timing) in the foundation before any story fixtures use them.
Story phases implement their behavior and evaluators against those existing
contracts; prepared fixtures do not bypass production schema validation.
Bootstrap retains the supplied brief with typed artifact/JSON Pointer provenance.
Routine checkpoint defaults/triggers are specified in data-model.md and FR-013.

1. Prove the save-before-emit Codex capability with a minimal installed tool and
   exact visible conversation capture, a second turn, fresh-chat resumption,
   interrupted display and failed save. This is the first integration spike.
2. Deliver initialize → brief → optional brainstorm → save → resume with stable
   identities, explicit unknowns and independent repository/bundle installation.
3. Add structured captures, explicit acceptance/rejection, revisions and sourced
   history with deterministic transition validation and impact references.
4. Add continuity responsibilities, perspective/timing distinctions, conflict
   dispositions and unreadable-context holds; measure agent judgments separately.
5. Complete Icelandic parity, portability consumer tests, fault/overlap exercises,
   scale measurements and novice evaluation. Stories 1–5 are the core loop;
   Story 6 remains mandatory for release.

Each slice adds tests for its observable invariants and onboarding instructions.
No drafting, dashboard, graph engine or additional host work is implied.

## Verification and risks

[quickstart.md](quickstart.md) defines planned commands and evidence. CLI and
schema commands are future implementation contracts, not available commands today.
Critical risks: host adherence to per-turn save protocol, exact visible response
capture, semantic acceptance/continuity quality in both languages, Git commit
failure and filesystem interruption. The design exposes failures instead of
claiming unsaved or unchecked work succeeded. The small journal is justified by
atomicity; avoid extending it into generic orchestration.

## Complexity Tracking

No constitutional deviations. The journal/reducer, JSON Schema dependency and
per-novel installed bundle each address an explicit atomicity, interoperability
or portability requirement; alternatives and tradeoffs are in [research.md](research.md).
