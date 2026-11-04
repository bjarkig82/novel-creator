# Update CLI Contract

**Status**: Protocol 1 implemented in the unreleased development controller; qualification evidence is tracked separately. Existing commands and error shapes remain compatible.

## Public commands

```text
novel-creator update --novel PATH [--version VERSION] [--python ABSOLUTE_INTERPRETER] [--json]
novel-creator update --novel PATH --apply --preview UUID --version VERSION --expected-head HEAD [--confirm-quiescent] [--json]
novel-creator update status --novel PATH [--operation UUID] [--json]
novel-creator update recover --novel PATH --operation UUID [--retry --expected-head HEAD] [--json]
```

- Default `update` checks and prepares a read-only preview. No prompt implicitly authorizes installation. Latest stable selection excludes yanked/prerelease/development/local versions; no downgrade or automatic compatible-version fallback. Same-version selection returns `already_current`, without a new operation or commit.
- `--python` chooses the configured book runtime interpreter for dependency validation and target preparation; default is the controller's `sys.executable`. Return its absolute `runtime_python` path. Bind that interpreter and its dependency fingerprint into the preview; apply/recovery reuse it and refuse changed or unavailable prerequisites. Do not infer an interpreter from book-controlled executable content or modify a global environment.
- `--apply` requires all of preview ID, exact version and expected HEAD; reject duplicated/conflicting arguments using the CLI's existing strict patterns. Missing/changed preview or state is a conflict. A changed release listing cannot change the pinned artifact. Initial 0.1.0/0.2.0 application also requires `--confirm-quiescent`, confirming other book clients have been closed and will stay closed through application and external recovery, then restart through the guarded launcher as required by FR-009. Explain FUP-001 and reject existing locks regardless of that flag; do not present confirmation as discovered/stopped-process evidence.
- Check/preview may read/download public releases and write only the external private cache. Status/recovery inspection perform no network calls and do not change files, fence ownership, notice inclusion or grants.
- Retry uses the exact journaled artifacts/candidate and external controller. Missing or changed recovery artifacts require preservation and inspection, not an unrequested new download. `--retry` without `--expected-head`, or expected-head without retry, is invalid.
- There is no `--force`, automatic rollback, lock-stealing, custom index URL, checkout input, arbitrary download URL or migration option. No push, credential setup or contribution API is exposed.

## JSON result

Use existing `ok`, `operation`, `novel_id`, `checkpoint`, `warnings`, `data` conventions. `operation` is `update.preview`, `update.apply`, `update.status` or `update.recover`.

`data` includes `state`, `installed_version`, `target_version` (null when unknown), `preview_id`, `operation_id`, `changes` (relative path/action), `blockers`, `ready`, `cleanup_required`, `next_action`. IDs may be null before preparation. A preview additionally exposes the release archive digest, bundle digest and reviewed HEAD; it does not expose private cache paths in release requests. Status distinguishes no operation, pending, published/cleanup-needed, conflict and complete observations.

Errors use `ToolError.result()` with affected refs, last confirmed checkpoint and expected/actual HEAD when relevant. Do not put an update operation ID into `pending_exchange_id`; include it under `data.operation_id` as an additive error field. Avoid dumping subprocess stderr, auth headers or private documents.

| Exit | Meaning |
| --- | --- |
| 0 | Successful check/status, already-current no-op, or verified ready update/recovery. |
| 2 | Invalid arguments, malformed public input or unsupported version selection. |
| 3 | Conflicting ownership/checkpoint/evidence or unresolved operation; no conflicting overwrite. |
| 4 | Unsupported protocol/schema/runtime prerequisite, unavailable selected release or unsupported artifact. |
| 5 | Network/I/O/preparation/verification failure, or published update still needing cleanup; preserve evidence and report actual publication. |
| 6 | Held lock or unavailable operation exclusion; never steal ownership. |

An acquisition interrupted before the matching owner metadata and confirmed journal checkpoint are durable reports `blockers: [{"reason": "ownership_unproven", "path": ".novel-creator/local/write.lock"}]`, exit 6 and `ready: false`. Preserve the existing directory and journal, direct the writer to owner/evidence inspection and refuse automatic retry/takeover. A prepared journal, unacknowledged owner file or dead PID alone never clears this blocker. This outcome occurs before any launcher/framework/index/ref mutation, as required by Story 3.8.

Failure exit does not imply nothing was published. If the ref already points to the candidate, return `state: published`, `ready: false`, confirmed candidate checkpoint and the cleanup/recovery instruction. Only verified completion with released fences returns ready.

## Host workflow

The new `$novel-update` skill loads shared `workflows/update.md`. It checks only on direct request, presents the selected version/changes/blockers, then applies only when the writer requests that reviewed update. Use the configured interpreter and exact returned IDs; do not replace command arguments with conversation-derived guesses.

Legacy books bootstrap via separately installed updater-capable tooling, without a framework clone. Close other book sessions before first update and retain the external recovery command/interpreter. Custom AGENTS content stays untouched; skill discovery remains available through installed explicit entry points. After success reload book instructions before writing. Do not automatically start a retrospective for the update operation or treat the update as a creative exchange.

Operational reports must obey the existing save-before-display boundary when included in a creative exchange. A maintenance failure never appends an unsaved notice to an already-saved response or consumes retrospective notices.
