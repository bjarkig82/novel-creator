# Implementation Plan: Update Novel Creator in Existing Books

**Branch**: actual checkout `main`; Spec Kit feature identifier `004-update-novel-creator` | **Date**: 2026-11-03 | **Spec**: [spec.md](spec.md)

**Input**: `specs/004-update-novel-creator/spec.md`

## Summary

Provide an explicit check/preview/apply workflow from separately installed updater tooling. Resolve a published stable release, prepare its verified wheel outside the book, validate ownership and compatibility, then publish one framework-only Git commit through a recoverable transaction. Preserve story bytes, custom instructions, staging and retrospective authority. Older books bootstrap from the external updater; the pinned launcher is not the recovery dependency.

This is a design, not implemented behavior. No feature code, tasks, dependency installation, book mutation, publication or release qualification is performed by this planning run.

## Technical Context

**Language/Version**: Python >=3.11; Markdown shared workflows and Codex adapter.

**Primary Dependencies**: Git >=2.39; existing jsonschema/jsonschema-rs; add `packaging>=24` for public PEP 440 version/prerequisite handling. Use standard-library HTTPS, venv, hashing and ZIP support plus pip available in the configured interpreter. No model runtime or GitHub dependency for updating.

**Storage**: Existing independent Git repository and story schema 1.0; additive installation metadata format 2; ignored versioned operational JSON under `.novel-creator/local/update/`; external private preview/package cache. Story schema and retrospective grant schemas remain unchanged.

**Testing**: Existing unittest contract/integration style, real disposable Git repos, fake release transport, historical wheel fixtures, isolated-process hard-interruption tests and extended wheel verification. Separate actual Codex host evaluation, using the delegated route explicitly selected/approved by the user on 2026-11-04; direct native-user input and unavailable platform checks remain unverified.

**Target Platform**: Windows PowerShell and Linux command workflow; initial Codex adapter. Native Linux Codex integration remains unverified until separately exercised.

**Project Type**: Packaged CLI, pinned book runtime and installed agent workflows.

**Performance Goals**: None; network/process timeouts and byte-count bounds protect against hangs/resource exhaustion only.

**Constraints**: Explicit check/application; public stable wheel releases; no downgrades or automatic migrations; exact release/checkpoint binding; no private uploads; no global package/Git changes; no automatic contribution work. Legacy bootstrap requires quiescent sessions and has the documented FUP-001 qualification boundary.

**Scale/Scope**: Single writer, one independent book per operation, one active update per book. Source books 0.1.0 and 0.2.0; targets must support update protocol 1. No dashboard, scheduler, provider calls or source-checkout installation.

## Constitution Check

Pre-research and post-design checks PASS for the bounded design below; they are not runtime qualification. No amendment or deviation is proposed.

| Principles | Design evidence |
| --- | --- |
| I, XI: simplicity and incremental delivery | Reuse CLI, bundle inventory, Git transaction primitives and existing test harness. One justified version library; no new service. |
| II, VIII: integration separation | Deterministic controller and host-neutral workflow; Codex skill is an adapter. No model provider or dashboard dependency. |
| III, IV, V: creative authority and provenance | No maintenance exchange, canon mutation or test save in a real book. Preserve exact records and existing save-before-display boundaries. |
| VI: ownership and portability | Dedicated framework commit; additive installation metadata, unchanged story schema, preserved prior history and external recovery controller. |
| VII: language independence | Preserve manuscript/interaction settings; verify English/Icelandic, Unicode paths and content separately. |
| IX: verification | Checkpoint, ownership, privacy, staging, failure-injection and historical-process scenarios in quickstart. Native-host results reported separately. |
| X: accessibility | Text command/host guidance; no visual-only controls or dashboard changes. |

FUP-001 is a foundational investigation gate before maintenance or transaction implementation, and must be rechecked during qualification: already-loaded legacy code cannot be retroactively taught a maintenance marker. FR-009 explicitly requires closed book clients through initial legacy application and external recovery, followed by restart through the guarded launcher; SC-005 tests that lifecycle and the unsupported preloaded-client case separately. If investigation or qualification cannot establish the supported boundary, dependent work/delivery is blocked rather than claiming FR-009/FR-010 passed.

## Project Structure

### Documentation (this feature)

`spec.md`, `checklists/requirements.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/update-cli.md`, `contracts/maintenance-protocol.md`, `quickstart.md`, `follow-ups.md`.

`tasks.md` tracks the dependency-ordered implementation and qualification checkpoints.

### Source Code (repository root)

Planned source boundaries:

- `src/novel_creator/update.py`: preview, apply/recovery orchestration and transaction state. `update_release.py`: public release transport, verified artifact cache and isolated bundle/probe process. `maintenance.py`: durable pending-state check and lock/fence coordination independent of CLI imports.
- Extend `cli.py`, `install.py`, `storage.py`, `context.py`, `retro.py`: dispatch/guards, ownership-aware continuation, replacement-aware index helper and direct-service mutation protection. Keep existing outputs compatible.
- Add `schemas/v1/update.schema.json` for operational records; package update protocol metadata/resources, shared `workflows/update.md` and `adapters/codex/skills/novel-update/SKILL.md`; extend entry guidance, onboarding, English/Icelandic resources and wheel verification.
- New update-focused contract/integration tests; extend storage/recovery, install, retrospective preservation/notice tests and historical portable-install cases. Native-host evidence belongs under `tests/evaluations/`.

**Structure Decision**: Keep the existing package/resource mapping. New modules isolate release I/O and maintenance coordination from story transactions and contributor publication. Do not introduce a generic command execution or remote-repository service.

## Design and Delivery Sequence

1. **Selection and read-only preview**: expose the CLI in its contract, use public release metadata and verified wheel inventory, keep package preparation/cache outside the book. Record a private immutable preview bound to normalized root, branch/HEAD, source manifest, interpreter, full nonignored worktree/index fingerprint and relevant operational-state fingerprint. Current-version checks are no-ops; failed discovery is unknown, not current. Never silently fall back from incompatible latest to a different release.
2. **Ownership/compatibility**: verify legacy exclusive resources against committed installation hashes and source-release inventory. Preserve custom instruction bytes; replace only a verified generated default. Append only missing shared rules, blocking staged affected shared files. New installation metadata separates exclusive checksums from shared rules. Target probes validate existing committed records and retrospective documents read-only; unsupported protocols/schemas/prerequisites refuse before mutation.
3. **Recoverable Git application**: prepare target and exact candidate before replacement. Acquire all fences, revalidate preview, durably save old/new bytes and index baselines. Install a maintenance launcher before package files, apply additions/replacements/removals with expected-before checks and atomic writes, conditionally publish the candidate and synchronize affected index entries only. Verify target resources and read-only usability, then install the final launcher and mark complete before releasing the owned fence. No story save, stash/reset, global setting or push.
4. **Maintenance integration and recovery**: bridge legacy writer/retro locks; add guards to new CLI and direct mutation entrypoints before any failure journaling. Interrupted operations retain the writer fence and standalone launcher. Recovery uses an external controller and pinned local artifacts, inspecting actual refs rather than trusting flags. A published candidate requires cleanup/verification, never a second commit. Unknown ownership/live holders/changed evidence stop recovery. No forced repair or automatic rollback in v1.
5. **Host/documentation and verification**: bootstrap old books through the separately installed controller, require explicit legacy quiescence confirmation and instruct Codex to reload after verified success. Preserve retrospective states without calling grant or notice mutation APIs. Exercise quickstart matrix and revisit FUP-001 before qualification. Update source documentation only when implemented behavior is available.

Before step 3, directory creation alone must never be mistaken for durable fence ownership. No installed-file, index or ref mutation starts before the ownership file and parent are durable and the journal subsequently confirms that checkpoint with `ownership_confirmed: true`. A crash in that acquisition window produces an `ownership_unproven` blocker, preserves the directory/journal and leaves installed files unchanged; it never enables automatic lock removal. Test both sides of the ownership-publication/durability checkpoint. Independently, the foundational FUP-001 investigation must pass before implementing step 3 or its maintenance integration.

Step 1 includes the complete local read-only `status()` service before its CLI route; synthetic journals/refs cover its full observation contract. Step 4 reuses that inspector for recovery eligibility and real interruption evidence. Package preparation in step 1 must install the verified product wheel into its private venv even when the selected interpreter inherits the same version (`--ignore-installed --no-index --no-deps --no-compile`), verify product module origins and exact installed resource bytes before probes, and preserve inherited distributions. Dependency reuse never authorizes inherited product code.

Details and rejected alternatives are in [research.md](research.md), persisted fields in [data-model.md](data-model.md), public and internal boundaries in [contracts/](contracts/), and validation scenarios in [quickstart.md](quickstart.md).

## Verification and Compatibility

| Requirements | Planned evidence |
| --- | --- |
| FR-001-FR-004 / SC-001-SC-002 | Release selection, no-network default paths, exact preview binding, stale worktree/index/operational state and idempotent apply contract tests. |
| FR-005-FR-008 / SC-003-SC-004 | Historical manifests/wheels, custom shared files, removals/collisions, target record probes, prerequisite failures, partial staging and private-index preservation. |
| FR-009-FR-012 / SC-004-SC-005 | Actual legacy subprocess lock bridge, durable fences, injected crashes around every durable transition, ref/index races and published-cleanup recovery. |
| FR-013-FR-014 / SC-006-SC-007 | 0.1.0/0.2.0 bootstrap and post-update context/resume/save in disposable books; all retrospective grant/run/notice states preserved. |
| FR-015-FR-017 / SC-008-SC-009 | Outgoing request capture with seeded private values, isolated package operations, English/Icelandic and Windows/Linux CLI matrix; separate Codex qualification. |

Retain existing save/recovery regressions. Extend index merging for deleted resources without changing existing save semantics. Re-run continuation on custom shared files under ownership format 2. Artifacts and source-origin wheel hashes must be recorded with each acceptance run. No product tests were run as part of this documentary planning phase.

## Complexity Tracking

No constitutional violations. The journal, persistent legacy fence, temporary launcher and external controller are needed to recover a runtime that is replacing itself while retaining old-book compatibility. The small `packaging` dependency avoids duplicating standard version semantics. The legacy lock bridge is limited to documented 0.1.0/0.2.0 contracts; arbitrary external Git/file writers remain conflict sources, not cooperating clients.

No before/after planning hooks are configured (`.specify/extensions.yml` absent). Research decisions are resolved; FUP-001 remains a named implementation/qualification follow-up, with an explicit supported-use constraint and failure gate.
