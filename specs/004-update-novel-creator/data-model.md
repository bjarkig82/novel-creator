# Data Model: Existing-book Updates

All proposed operational documents use strict UTF-8 JSON, reject duplicate keys/unknown versions, validate paths and UUIDs, and are written atomically with file/directory durability. They contain no story authority. Story `schema_version` remains `1.0`; existing retrospective schemas and grants are not migrated.

## PublishedRelease / PreparedBundle

- `project`: fixed normalized `novel-creator`; normalized `version` and parsed stability.
- `artifact`: HTTPS URL, filename, declared size, SHA-256, wheel tags, Python requirement and yanked state.
- `protocol_version`: integer 1; supported source installation formats and record/retro schema versions, obtained from packaged `update-release.json`.
- `bundle_digest`: SHA-256 of the canonical sorted path/mode/content-digest inventory exported by the verified isolated target package; includes a final pinned launcher and all exclusive resource paths.
- `dependencies`: target requirements checked against the selected original interpreter; target preparation cannot repair them implicitly.
- `prepared_origin`: the private venv interpreter/site-packages root and verified installed product module/resource inventory. Existing dependency packages may be reused, but every loaded product module must originate under that private root and match the selected wheel. A same-version inherited product distribution cannot satisfy preparation.

Artifact identity includes archive bytes, not just version text. No target without a compatible wheel/protocol is automatically coerced. Exported inventory must agree with verified wheel resources and the controller's allowlist. Source 0.1.0/0.2.0 inventory adapters may read their historical packaging layouts; they do not require those releases to expose protocol 1.

## BookInstallation

Existing fields remain: `novel_id`, story `schema_version`, `bundle_version`, `managed_paths`, `checksums`. Add `installation_format: 2` and `ownership` with `exclusive` and `shared` entries.

- Exclusive entries hold canonical relative path, regular-file mode and content SHA-256. `checksums` covers exclusive resources only in format 2; `managed_paths` identifies those exclusive resources. The manifest itself is verified against its committed blob and journal, never self-hashed.
- Shared entries identify a file role (`instructions`, `ignore_rules`, `attributes`) and required framework rule lines, not a claim to all file bytes. Optional verified-generated-default identity permits full default instruction replacement. Custom content has no framework replacement grant.
- Legacy format 1 has no ownership field. Classify fixed package paths using the historical source archive and treat shared files conservatively. New format 2 continuation uses ownership-aware validation rather than the legacy all-file checksum rule.

Installation format is distinct from the story schema. Changing metadata cannot change the novel UUID, grant identity or stored creative records. Do not embed a second creative brief.

## UpdatePreview (external private cache)

- `document_version: 1`, `preview_id` UUID, canonical `novel_root`, `novel_id`, creation time (informational).
- Source branch ref, Git HEAD, source manifest digest and installed version.
- Full semantic index fingerprint (paths, stages, modes, object IDs), tracked worktree bytes/modes plus nonignored untracked inventory, and relevant save/retro operational-state fingerprint. Exclude the updater's own lock files and ignored package caches, but include existing journal/notice/grant evidence.
- Original interpreter absolute path, version, dependency inventory fingerprint.
- Exact release artifact and prepared bundle identity, affected-path operations, expected source/target hashes, shared-file actions, blockers, compatibility result and next action.

Preview lives outside the book so checks remain read-only there. Private root paths never enter release requests. A modified/forged/missing cache entry or changed bound state requires a fresh preview. A cached preview is not permission by itself: apply needs explicit arguments. Cache directories are user-private; do not accept arbitrary preview paths or executable commands from the book.

## UpdateOperation (ignored book-local journal)

Location: `.novel-creator/local/update/operations/<operation_id>/journal.json`; blobs and verified target artifacts in that operation's private directory. `.novel-creator/local/update/active.json` identifies the one active operation. Neither goes at `local/*.json`, which legacy saves parse as story receipts.

Fields:

- `document_version: 1`, UUID `operation_id`, `preview_id`, `novel_id`, canonical root.
- Expected branch ref/parent HEAD; source/target versions and manifest digests; exact artifact/bundle identity and candidate commit/tree ID.
- `changes`: path, action (`add`, `replace`, `remove`), old/new blob IDs, byte digests, file mode, affected index baseline, last durable progress. Null old/new means absence; an absent target is represented explicitly for index deletion.
- Durable private copies of old/new resource bytes and original/final launchers; enough verified wheel/controller inputs for offline exact retry. Never persist a copied story transcript as updater state.
- `fence`: owning operation token, owner PID/process identity, `ownership_confirmed` (false while prepared, true only in a durable `fenced` or later checkpoint after the owner file and parent flush), maintenance launcher digest and confirmation of legacy quiescence. PID alone is not proof of ownership/death. `ownership_unproven` is a derived blocker, not a successful journal transition.
- State, publication observation, cleanup/verification outcomes and last confirmed checkpoint. Failure diagnostics remain local and redact credentials in public output.

### State transitions

`prepared -> fenced -> replacing -> candidate_published -> verifying -> complete`.

Any non-complete state can return a conflict/blocked result while retaining its durable evidence; this does not overwrite the last safe progress state. The candidate may already be published even when the last journal state is earlier: inspect actual ref equality and candidate identity. If HEAD is neither the expected parent nor the candidate, stop with conflict rather than replay against an advanced branch.

Before `fenced`, failures release only temporary locks whose ownership is proven and leave installed files unchanged. A persistent fence is proven only when matching ownership metadata and its parent have been durably flushed and the journal subsequently records `ownership_confirmed: true` in `fenced` or a later state. A prepared token alone never proves that an existing directory belongs to that operation, even if an owner file appeared before the confirmed checkpoint. A stop between directory creation and that checkpoint leaves `ownership_unproven`: retain the directory and journal and block automatic retry/takeover, with launcher/framework/index/HEAD unchanged. Once ownership is proven, retain the owned persistent fence on failure; explicit verified recovery covers subsequent interruptions, including before the launcher swap. Never infer ownership from directory age or presumed PID death.

Candidate creation precedes resource replacement. While `replacing`, the worktree may contain only expected old bytes, target bytes or the recorded maintenance launcher at its one allowed path. Unexpected bytes/modes/index changes are conflicts. Before publication, all non-launcher affected paths must be target bytes; the recorded launcher stub is the sole planned temporary exception.

After publication, cleanup merges affected index entries to candidate values, including zero-mode removals. Read-only target probes verify installed imports/resources and committed context without creating a story save. Restore the final candidate launcher last, recheck its digest and normal read-only launch readiness under a controller-owned verification mode, mark complete durably, then release only the verified owned fence. A crash between completion and fence release remains cleanup-needed and must not produce a second commit.

## ExistingRetrospectiveState

Local authorization, claim index, run files, notices/reservations and matching machine grants retain their exact bytes and meaning. Reads for compatibility use JSON/schema inspection, not service calls that render notices or reconcile state. Hash relevant local/machine evidence before and after apply; no grant registry writes.

Absent/disabled/revoked/unbound grants permit no external checkout access. Valid enabled grants permit only the minimal existing checkout guard inspection needed for exclusion, with no network requests or contributor ownership changes. Any nonterminal/unknown run, unresolved publication, required cleanup or pending notice reservation blocks application. A terminal run with outstanding repository ownership is not treated as clean. Unreserved pending notices and terminal receipts are preserved if their schemas remain compatible.

## Derived result

Public results report state, installed/target version, preview/operation ID, candidate/confirmed checkpoint, affected paths, `ready`, `cleanup_required`, blockers and `next_action`. These are operational observations, never a second source of story truth. `ready` requires verified target installation, no unresolved journal/cleanup and released maintenance fences.

The local read-only status inspector is implemented and tested in US1 using synthetic valid/invalid journals and actual disposable refs. US3 recovery inspection consumes that same inspector and adds retry eligibility; it must not introduce a later-only status implementation or change the observation meanings.
