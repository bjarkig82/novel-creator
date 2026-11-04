# Implementation Plan: Agent-Maintained Story Notebook

**Feature**: 005-agent-story-notebook | **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)

**Input**: Approved notebook direction; clarified first delivery supports new novels only.

## Summary

Make Codex instructions and native file editing the writing workflow. The agent maintains Markdown topic notes and a derived working summary, saves meaningful changes automatically, and gives topic-focused briefs only on request. No exchange archive, schema gate before replies, scheduler or routine Python save process is involved.

Add an explicit notebook creation route alongside the existing legacy initializer. Python is used only for one-time scaffolding through the existing package; no Python sources or launcher are copied into notebook novels. Keep legacy commands, installed novels and update resource selection unchanged.

## Technical Context

**Language/Version**: Markdown for instructions and story content; existing Python >=3.11 for setup and structural verification; Git >=2.39 for history.

**Primary Dependencies**: Native Codex filesystem/Git capabilities, Python standard library for new setup logic. No new dependencies, model API, database or orchestration. Existing distribution dependencies remain for legacy support.

**Storage**: Independent Git repository containing project brief, topic notes and derived summary. Small JSON metadata blocks provide a versioned machine-readable contract within Markdown.

**Testing**: Existing unittest tooling, disposable repository integration tests, installed wheel/sdist verification, and actual Codex host journeys in English and Icelandic.

**Target Platform**: Windows Codex Desktop first; Windows and Linux setup/structural tests. Linux host behavior remains unverified until exercised. No new macOS support claim.

**Project Type**: Agent workflow resources plus an additive setup command.

**Performance Goals**: No numeric latency targets. Read relevant notes rather than the whole book; avoid writes on content-free turns.

**Constraints**: New novels only; no migrations, manuscript writes, automatic recap, external push or global Git configuration. Save meaningful content by the end of its turn or disclose failure. No atomic multi-file or exact-transcript recovery guarantee.

**Scale/Scope**: One writer and one active writing agent per novel, with successive sessions. Simultaneous writing agents are unsupported; detected external changes are preserved and reconciled.

## Constitution Check

Pre-research gate: PASS for the proposed direction. Stable structured Markdown, concise decision origins and Git history can satisfy the constitution without exact exchanges. No amendment is assumed.

| Principles | Design evidence |
| --- | --- |
| I, II, XI: simplicity, native agents, incremental delivery | Native editing and a small setup-only module; no new writing runtime. |
| III, V: creative authority and collaboration | Guided brainstorming is the default and freeform exploration is available on request; clear acceptances need no repeated approval; no forced questionnaire or recap. |
| IV: continuity and traceability | Stable references, decision context, impact review and recoverable revisions; no exhaustive consistency claim. |
| VI: portable structured versioned data | Explicit Markdown/JSON contract and development checks; one owner for each fact; separate Git repository. |
| VII: language independence | Dedicated English/Icelandic guidance and scoped host evaluation. |
| VIII, X: separation and dashboard | No dashboard or manuscript workflow in this slice; content independently readable. |
| IX: verification | Separate structural tests, real host behavior evidence and subjective literary quality. |

Post-design gate: PASS at design level against the contracts and data model. This is not runtime verification. If actual-host results cannot maintain key invariants, revise instructions or document a concrete need before adding a save helper.

## Project Structure

### Documentation (this feature)

- plan.md: this plan.
- research.md: choices, evidence and rejected alternatives.
- data-model.md: entities, state and ownership.
- contracts/notebook-format.md: versioned note grammar and save behavior.
- contracts/setup-and-host.md: creation and native-host boundaries.
- quickstart.md: proposed commands and acceptance journeys.
- tasks.md: generated implementation checklist following the planning phase.

### Planned source changes

- src/novel_creator/cli.py: additive notebook init route.
- src/novel_creator/notebook.py: setup only, no conversation/save engine.
- src/novel_creator/install.py and src/novel_creator/update_release.py: matching exclusions of the setup-only module from pinned legacy exports and verified inventories.
- adapters/codex/notebook/AGENTS.md: thin Codex-specific entry pointing to shared installed guidance.
- notebook/__init__.py: resource package marker, mapped to novel_creator.notebook_resources.
- notebook/workflows/: conversation and format guidance.
- notebook/languages/: dedicated en.md and is.md.
- notebook/templates/: project and working-summary seeds.
- pyproject.toml: explicit notebook package-data coverage.
- tests/unit/test_notebook_contract.py: meaningful format/reference fixtures.
- tests/integration/test_notebook_init.py: setup safety and compatibility.
- tests/integration/test_notebook_package.py: installed artifact verification.
- tests/fixtures/notebook/: structural and behavioral fixtures.
- tests/evaluations/agent-story-notebook.md: observed host evidence.
- README.md and workflows/start-here.md: new route and legacy distinction.

**Structure Decision**: Shared conversation/format guidance, language resources and seeds live under notebook/, mapped explicitly to the resource-only package novel_creator.notebook_resources. The Codex adapter contains only its thin root-instruction entry. Setup copies shared resources to .novel-notebook/ and the selected adapter to root AGENTS.md. Package-data configuration covers these two resource owners explicitly; shared content stays outside legacy workflow/language packages and update export. Do not change legacy AGENTS.production.md, entry skills or update activation. No new skill needs invoking every turn.

## Delivery Sequence

1. Define templates and dedicated instructions against the contracts. Exercise a disposable manually scaffolded notebook to identify instruction problems early.
2. After shared conversation, format, language, template and adapter resources exist, add isolated setup and packaging. Verify Unicode, paths, refusal cases, partial failures and installed artifacts.
3. Exercise automatic maintenance, focused briefs, decisions, revisions, staged/external edits and fresh-session recall in actual Codex sessions.
4. Update onboarding and evidence. Keep legacy novel behavior intact.

Generate implementation tasks before production coding. This phase creates design artifacts only.

## Compatibility and Failure Boundaries

Existing init, update, recovery, inspection and retrospective contracts remain legacy behavior. Notebook creation does not call legacy initialize/bootstrap/bundle_files or storage.save. Notebook resources and the setup-only module must not enter legacy update export. The shared CLI omits notebook setup in the pinned-launcher layout while the full package exposes it; exporter and verifier inventories use the same exclusion. A real initialized legacy-launcher regression checks this boundary.

Any existing destination is refused, including an empty folder or completed notebook. Partial setup is preserved and reported, not overwritten, automatically deleted or managed with a new recovery ledger.

File-save success and Git-checkpoint success are separate outcomes. If checkpointing fails, disclose pending history and retain replaced accepted prose in a historical revision section until recoverable through Git.

Native multi-file edits are not atomic. Update primary notes before derived summaries; disclose incomplete changes and never treat a stale summary as canon.

## Verification and Completion

Map SC-001 through SC-009 to quickstart journeys. Structural tests verify setup safety, reference grammar and packaging. Actual host journeys verify observed creative interpretation, automatic maintenance and preservation. Unavailable host/platform evidence remains unverified. No new latency target or subjective quality guarantee is introduced.

## Complexity Tracking

No constitutional exceptions proposed. The resource-only package supplies a platform-independent ownership boundary, not a new runtime abstraction. One setup module is justified by safe scaffolding and packaging. No runtime save helper, archive ledger, custom agent runtime, migration controller or validator service.
