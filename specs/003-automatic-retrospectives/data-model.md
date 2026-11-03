# Data Model: Retrospective Operational State v1

These are proposed JSON contracts, not story records. All persisted retro records carry `retro_version: 1`; unknown versions block use rather than being migrated silently. Use strict UTF-8 JSON, schema validation, atomic replacement, safe ordinary-file paths, and an authorization lock separate from the novel writer lock. Reject symlinks, junctions, path escapes, malformed IDs and unknown fields.

## Participation grant

Novel-local path: `.novel-creator/local/retro/authorization.json`.

| Field | Meaning |
| --- | --- |
| enabled | Boolean; absence is disabled. |
| grant_id, generation | Random UUID and monotonic integer; enable, disable, or rebind changes generation. |
| novel_id, novel_root | Manifest novel UUID and canonical real novel path. |
| checkout_root, git_common_dir | Canonical configured framework checkout and repository identity. Neither may overlap the novel directory. |
| repository, github_login | Fixed `bjarkig82/novel-creator` target and verified authenticated account. |
| authorization_source | `direct_cli` or public host turn reference for explicit opt-in; source text itself is not copied here. |

A matching machine registry entry under `LOCALAPPDATA/NovelCreator/retro/grants/` on Windows or `$XDG_CONFIG_HOME/novel-creator/retro/grants/` (fallback `~/.config/...`) on Linux contains grant ID, generation, and the same canonical bindings. Valid authorization requires both copies to match. No credential is stored. Copying a novel, checkout configuration, or grant file to another root or machine does not enable it. A path move requires explicit re-enable; do not transfer grants automatically.

Enable writes both records under the authorization lock, publishing enabled state last. Partial writes fail disabled. Disable first invalidates the local enabled state/generation under that lock, then invalidates the registry entry; partial disable stays disabled. Same-user malicious filesystem mutation is outside the provenance guarantee; ordinary file validation is not human authentication.

## Completed task claim

Path: `.novel-creator/local/retro/runs/<run_id>.json`.

- `run_id`: opaque random UUID, never derived from story text.
- `task_key`: local digest of novel ID, host kind, host thread ID and initiating public turn ID. One request may span several turns; its initial turn remains the key. Session closure is its own explicit task. Missing stable identity blocks claiming.
- `completion_exchange_id`, `checkpoint`: existing saved exchange UUID and Git commit proving the completed deliverable. Reject pending/cleanup-required saves and a checkpoint not in confirmed history. At resume verify that original checkpoint remains reachable and that current history has no persistence pause; a later valid save does not invalidate the claim.
- `grant_id`, `authorization_generation`: bound opt-in snapshot, rechecked for mutations.
- `status`, `reason_code`: lifecycle and sanitized diagnostic.
- `evidence_refs`: local saved exchange/message identifiers relevant to the finding. No hidden reasoning. Do not duplicate raw transcripts into retro payloads.
- `finding`: optional generalized category (`workflow`, `documentation`, `test`, `runtime`), public-safe problem and synthetic reproduction; raw evidence remains in existing local records.
- `contribution_id`: optional reference to the contribution receipt.
- `notice`: for each PR/problem outcome, opaque `notice_id`, brief operational text, its SHA-256 UTF-8 digest, optional PR URL, state `pending`, `reserved`, or `included`, optional reservation and optional `included_exchange_id`. Operational notice text is rendered with `retro notices pending --language en|is` before reservation, independently of manuscript language; unreserved rendering updates its text digest. Notices have `language`, `notice_kind` and sanitized `reason_code` fields and independent journal files, so a later outcome cannot overwrite a reserved notice. No-action outcomes need no automatic notice. Keep pending through failed saves; reconcile interrupted bookkeeping against the saved exchange before including it again. Saved inclusion is not proof of display or acceptance.

A per-novel claim index under the same local lock maps task_key to exactly one run. Claim and index writes must be recoverable: create run before publishing index; on interruption reconcile orphan run identity before admitting another claim. Repeated begin returns existing run with `review_required: false`; `resume` continues its state rather than restarting semantic review.

## Notice reservation and reconciliation

The independent notice journal is the authority for pending/reserved/included state. A run's embedded `notice` is a derived snapshot of its latest generated outcome, not an acknowledgement ledger; confirmation always reads the independent notice and reservation records.

Before saving a reply containing notices, atomically reserve all selected pending notice IDs under the novel-local retro lock. A reservation stores its opaque UUID, prepared exchange UUID, assistant message UUID, expected HEAD, exchange payload digest, exact assistant-text SHA-256, and each notice's nonoverlapping half-open UTF-8 byte span and text digest. It stores metadata only, not a copy of the conversation. Use a separate reservation file plus notice references; publish the complete reservation before changing notice states, and reconcile a partially written batch before admitting another reservation. A notice may belong to only one unresolved reservation. Repeated identical reserve requests are idempotent; conflicting targets fail closed.

After save, confirm reads the exact exchange from confirmed reachable history, verifies the recorded payload/message digests and that each span contains the expected notice bytes, then marks inclusion with its exchange ID. If acknowledgement is interrupted, reconcile performs the same checks and completes local bookkeeping without another story save. Do not infer inclusion from similar text or a matching PR URL elsewhere.

If the target exchange has no published save and no pending receipt or uncertain storage state, reconcile may return its notices to pending for a newly prepared exchange. If the save remains pending/uncertain, preserve the reservation, return persistence-paused, and follow existing story recovery before preparing a replacement. Mismatched published content is a conflict, not a release condition. An included notice is never automatically repeated; normal saved-response recovery can display its original exchange. These local notice operations are allowed after disablement, never access the framework/GitHub, and confer no contribution authorization.

## Contribution receipt

Stored with the run or referenced by opaque UUID within the same retro directory:

- Public opaque contribution ID; generalized finding fingerprint; repository and GitHub account.
- Fetched default branch/base commit, tool-owned worktree identity, head branch, commit and tree SHA.
- Validation checks: command argv, exit result and local log reference, approved tree SHA; logs remain local and sanitized when displayed.
- Privacy approval: exact tree SHA, public title/body hashes, synthetic fixture hashes, scanner result and explicit host semantic approval. No false assertion of a complete privacy proof.
- Publication intent: target/base/head, commit SHA, public marker, body/title hashes, and stage (`not_started`, `push_intent`, `pushed`, `create_intent`, `publication_unknown`, `remote_observed`, `published`).
- Remote result: PR URL/number, head SHA and draft status, or existing equivalent PR reference. Never embed a novel/task ID or private path in the remote marker.

Changing the tree or public payload invalidates validation/privacy approvals and requires repeating affected checks. Unknown publication state cannot be cleared by deleting the receipt or making a new run.

## State transitions

`claimed -> reviewing -> no_action | insufficient_evidence | selected`

`selected -> preparing -> prepared -> validating -> validated -> publishing -> published`

Any nonterminal stage may become `blocked` or `disabled`; an existing equivalent contribution ends as `duplicate` with its reference. Persist the last safe stage for resumption. `publication_unknown` is a blocked publication substate and requires remote reconciliation. Terminal outcomes do not start a new review for the same task. A blocked run can resume the existing finding; it never silently selects a second fix.

Authorization is re-read before each tool-owned mutation, worktree edit phase, validation process, push, and PR request. An already in-flight operation may complete after disablement; record and reconcile its effect without issuing another mutation. Repository locks serialize cooperating runs across novels and are never silently stolen. Novel writer locks are held only for existing story operations, never across retrospective work.

For a dispatch-journaled `operation_unavailable` preparation failure, the existing finding and absent contribution or `not_started` allocation (no commit/validation/remote outcome) identify the last safe stage. Enabled explicit resume checks ownership/access, restores `selected`/`preparing`, and returns `next_operation: prepare`. Recorded worktree identity is verified if present; prepare checks its exact path/branch/base before reuse or creation. Durable publication intent and other blocked reasons do not use this continuation.

Each subsequent framework Git process has a fresh authorization check, including reads between mutations and transport verification-to-fetch/push. The control lock is held only by enable/disable writes, never through subprocess waits or contribution operations. Dispatch after a successful check begins an in-flight operation; revocation prevents later dispatch, without cancellation or rollback of that operation. Existing durable allocation/commit/publication intents and diagnostic attempts reconcile effects, so no new competing in-flight authority record is needed. Completed commit identities, diagnostics and known PR results are saved before the next authorization boundary. This is cooperative process fencing, not a sandbox for arbitrary trusted repository code.

## Repository ownership and lock recovery

Separate a durable active-contribution claim from short-lived operation locks under the configured Git common directory. The claim binds run ID, grant ID, canonical novel root, worktree and contribution identity; it persists across CLI process exits. The same run may reenter after verifying its receipt. Other runs stop while this claim exists. Short-lived operation locks serialize atomic claim/receipt changes and mutating tool operations; host edit phases honor the durable owner claim.

Terminal published, duplicate, and no_action outcomes release the active claim, without removing the worktree or receipts. Blocked, disabled, and publication_unknown outcomes retain it for inspected recovery. Disabled resume/release returns re-enablement-required using local receipts only, with no framework repository or GitHub access. After explicit successful re-enablement with the same novel/root/repository/account bindings, a directly requested resume/release may adopt the new grant generation for this existing run after verifying its receipt; enablement itself starts no contribution work. Changed bindings block adoption. Reconciliation then precedes any further mutation.

Short operation locks record a process ID and random holder token. An enabled explicit release can inspect a lock bound to this run; only a positively proven dead holder and an otherwise intact holder-only directory permits atomic lock quarantine/removal. Live, inaccessible, ambiguous or malformed ownership stays blocked; no age heuristic applies. and no publication effect remains uncertain. It marks the run abandoned (a terminal outcome), preserves all work, and never deletes remote or local contributions. A dead short-lock owner is cleared only through this inspected recovery path, never by an elapsed-time heuristic. When remote read access is unavailable or a create result is unresolved, release stays blocked. No disabled recovery operation probes or mutates the repository, even if its prior publication intent is uncertain.

## Compatibility and ownership

Novel content and authoritative history continue to use schema 1.0. Retro state is machine-local, ignored operational state; losing it disables participation and requires conservative inspection of existing remote contributions before a new publication. No automatic deletion of worktrees, branches, PRs or unfinished receipts. Reinitialization and package upgrades do not modify old pinned novel bundles.

## Convergence receipt additions

Version 1 accepts older receipts without the following additive fields. Missing/stale comparison requires host review before allocation/publication; older successful validation receipts remain readable. `comparison` binds snapshot/approved/equivalent-PR/upstream-fix judgment to the finding, fetched base and public open/merged PR set. `remote_outcome` retains equivalent/observed/verified kind and actual public PR metadata (state and merged identity included), or a canonical URL/number while metadata remains unavailable. Observation precedes strict success verification.

Contribution `diagnostics` appends validation attempts with UUID, exact tree, state and checks. Each check stores argv, nullable exit result, state, and stdout/stderr relative references with SHA-256 digests (null until finalized). States: running, passed, failed, unavailable, interrupted. Paths are durable before start and output streams directly into ignored novel-local files. A successful validation optionally references its attempt UUID; ordinary status omits raw paths/content. No log is an approved public payload.

Operation-lock holder metadata optionally carries exact owner binding, permitting proven-dead inspection after owner removal; legacy holder metadata still requires an existing matching owner. Local bookkeeping uses OS advisory locks, which release on process death. Outcome notice UUIDs are stable per run/kind/reason/URL; retries reuse journal state and never reset acknowledgement. Missing previously confirmed history conflicts instead of returning the notice to pending.
