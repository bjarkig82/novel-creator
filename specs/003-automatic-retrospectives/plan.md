# Implementation Plan: Automatic Contributor Retrospectives

**Branch**: actual checkout `codex/package-novel-init`; Spec Kit feature identifier `003-automatic-retrospectives` | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: `specs/003-automatic-retrospectives/spec.md`

## Summary

Deliver an optional contributor workflow in newly initialized novels. The active host agent recognizes task completion, confirms the exact writing exchange was saved, then reviews public evidence and may prepare one focused fix in an isolated framework worktree. A small deterministic Python boundary owns local authorization, receipts, validation of publication inputs, Git operations, and GitHub draft publication. The host owns semantic review, synthetic reproduction, and code changes. No scheduler or model API is introduced.

This document is a design, not implemented behavior. No tasks, feature code, pushes, or PRs are produced by this planning run.

## Technical Context

**Language/Version**: Python >=3.11; Markdown shared workflows and Codex adapters.

**Primary Dependencies**: Existing jsonschema/jsonschema-rs and Git >=2.39. Optional GitHub CLI `gh` for opted-in contributors; no new mandatory Python dependency.

**Storage**: Versioned local JSON under ignored `.novel-creator/local/retro/`; per-user machine authorization binding outside the novel; isolated worktree and lock metadata under the configured framework Git common directory. No story-schema changes.

**Testing**: Existing unittest contract/integration patterns, disposable Git repositories, fake GitHub transport, wheel verification, separate native-host acceptance.

**Target Platform**: Windows PowerShell and Linux CLI; Codex is the first host adapter. Verify Windows native-host automation separately; Linux host behavior remains unclaimed until exercised.

**Project Type**: Packaged CLI and installed agent workflow.

**Performance Goals**: None. One initial review and at most one fix per task; timeouts protect against hangs only.

**Constraints**: Default off, explicit novel-specific authorization, private material stays local, no automatic merge/deploy, fail closed before external mutation, preserve exact saved responses and unrelated work.

**Scale/Scope**: Single contributor, configured checkout, one active contribution per configured repository. Newly initialized bundles only; no cloning, forks, old-bundle migration, dashboard, background runtime, or credential management.

## Constitution Check

Pre-research and post-design gates both PASS at the design level:

| Principles | Design evidence |
| --- | --- |
| I, XI: simplicity and incremental delivery | Existing Python/host workflows; optional gh transport; one contribution per run. Local state machine is needed for authorization and uncertain publication recovery. |
| II, VIII: independence and separation | Host-neutral review protocol; Codex adapter recognizes completion; Python handles deterministic operations. No provider runtime or dashboard. |
| III, IV, V: creative authority and traceability | Only confirmed saves are eligible; no story mutations or canon promotion; receipt references existing saved evidence. |
| VI: portable story ownership | Story schema and Git history unchanged. Machine-bound opt-in is explicitly local operational state, not novel authority. |
| VII: language independence | Unicode evidence and English/Icelandic operational messages tested; upstream examples use synthetic content and do not change manuscript language. |
| IX: verification | Privacy, revocation, duplicate publication, and crash recovery have contract and integration scenarios; semantic and native-host claims require separate evidence. |
| X: accessibility | Text CLI and host responses; no dashboard changes or visual-only controls. |

No constitutional deviations or amendments are needed. Pre/post checks establish design compliance, not passing feature tests. Specification checklist is complete. No before/after plan hooks are configured (`.specify/extensions.yml` absent).

## Project Structure

### Documentation (this feature)

`spec.md`, `checklists/requirements.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/retro-cli.md`, `contracts/host-workflow.md`, and `quickstart.md`. `tasks.md` is reserved for a later `$speckit-tasks` invocation.

### Source Code (repository root)

Planned changes only:

- `src/novel_creator/retro.py`: local state, claims, authorization and guarded contribution operations; `retro_github.py`: optional Git/gh transport. Extend `cli.py` dispatch without changing existing command outputs.
- `workflows/retrospective.md`, `workflows/entry.md`, and Codex adapter instructions: completion protocol and narrow opt-in exception to the current no-push rule. Extend onboarding and English/Icelandic resources.
- Add separately versioned retro JSON schemas under the existing packaged schema resource tree. Extend installer/wheel checks so new modules, schemas, and workflows are pinned in new novels. No automatic change to existing novels.
- Contract tests for CLI/state/privacy boundaries and integration tests with disposable repositories and fake gh; extend portable-install verification and add native-host evaluation fixtures.

**Structure Decision**: Keep the current Python package and resource layout. Reuse safe local path checks and atomic-file patterns, but do not reuse the story transaction or expose a generic shell execution API.

## Design and Delivery Sequence

1. Implement default-off status and explicit enable/disable with checkout and machine binding. Network probes are only permitted during explicit enablement or an enabled run. Read-only status never contacts GitHub. Disabled resume/release returns local re-enablement-required without framework/GitHub access; explicit re-enablement permits subsequent inspected recovery but never starts edits or publication automatically.
2. Add task claiming and local review outcomes. Host completion identifies one initiating public turn and confirmed finishing exchange; repeated signals return the existing receipt and never rerun semantic review.
3. Discover and fetch the upstream default branch before allocating its isolated worktree, then add synthetic-only validation, publication gating, and durable intent/reconciliation. Read repository instructions in the worktree; validate against the fetched upstream default-branch commit. Use explicit argv subprocess calls, never shell interpolation.
4. Add installed host workflow and packaging. After saving completion, claim/review/contribute before displaying the already-saved response. PR and problem outcomes queue a brief notice for automatic inclusion in the next normally saved reply; no-action outcomes remain local unless requested. Interrupted review cannot invalidate that writing checkpoint.
5. Verify acceptance coverage and document limitations. No distribution release is authorized by this plan.

For notices, expose local pending/reserve/confirm/reconcile operations. Reserve notice IDs against the prepared exchange/message IDs, expected HEAD, payload/message digests and notice byte spans before saving. Confirm only from verified committed content; reconcile save-success/acknowledgement crashes using that durable reservation. Pending or uncertain saves retain ownership of their notices; confirmed-unsaved attempts may release the reservation without discarding notices. These operations read/write only local operational state and existing saved history, including when participation has since been disabled, and require no story-schema changes.

## Verification and Compatibility

Run the scenarios and proposed test entry points in [quickstart.md](quickstart.md). FR-001–FR-003/FR-015 map to authorization tests; FR-004–FR-008 to completion/review tests; FR-009–FR-013 to preparation/publication/privacy tests; FR-014/FR-016 to receipts and preservation tests; FR-017 to install/old-bundle tests. FR-018/SC-008 map to pending-notice inclusion, failed-save retention and exact-response tests. SC-001–SC-008 are the acceptance outcomes.

Existing story schemas, receipt discovery, context outputs, and recovery commands remain compatible. Retro state has its own version and fails closed on unknown versions. Disablement retains local receipts and unfinished work. No automatic cleanup deletes worktrees, branches, or remote PRs.

## Complexity Tracking

No constitutional violations. The machine grant, repository lock, and publication-intent receipt are the minimum extra state needed to reject copied opt-ins, serialize cooperating runs, and avoid blind retry after uncertain publication. Semantic privacy review remains an agent judgment; automated scanning is defense in depth, not proof.

## Convergence implementation refinements (2026-10-29)

The public comparison route is explicit and snapshot-bound (`retro compare`) before allocation/publication; the host assesses current upstream and open/merged PR scope. Stable per-outcome notice identities and OS advisory local bookkeeping locks close hard-interruption gaps. Repository operation holders include exact run/grant/root binding for terminal cleanup after owner unlink. Observed canonical PR references are saved before follow-up metadata reads and distinguished from verified success and genuinely unknown creation. Transport guards recheck authorization between requests/fetches. Validation streams private diagnostics to ignored local storage with durable tree-bound attempts, preserving failure/interruption evidence. These refine the existing safety requirements without a scheduler, provider API, old-bundle upgrade or new external authorization.
