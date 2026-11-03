# Research: Automatic Contributor Retrospectives

**Date**: 2026-10-29. All decisions below are planning decisions. No authentication, remote access probe, fetch, push, or publication was performed.

## 1. Host completion and exact display

**Decision**: The active host identifies task completion, with stable initiating public turn identity and the successfully saved finishing exchange. Claim once after confirmed save, perform review before returning the already-saved final, and keep results local. Routine turns and retrospective work itself are ineligible. An interrupted claim resumes existing work rather than repeating review.

**Rationale**: `workflows/entry.md` requires exact input capture and exact saved response display, including the commentary boundary; `workflows/brainstorm.md` already distinguishes explicit session closure. There is no background scheduler. A retrospective result cannot be appended to the saved final. The next reply uses metadata-only pre-save notice reservations and local pending/reserve/confirm/reconcile operations; exact committed exchange/message digests and UTF-8 spans resolve save-success/acknowledgement crashes without changing story schemas. Following the 2026-10-29 clarification, a PR or problem outcome is automatically included as a brief notice in the next normally saved reply; no status request is required. No-action outcomes remain available through status.

**Alternatives considered**: Every-turn review creates noise; session-close-only misses completed tasks; asynchronous services introduce a new runtime; a second assistant message invents an exchange not supported by the current input contract.

## 2. Explicit opt-in and copied settings

**Decision**: Require an explicit enable action with a confirmation flag or equivalent direct host invocation after a public user opt-in. Bind a novel-local grant ID to a per-user machine registry entry keyed by canonical novel root, novel ID, framework Git common-directory identity, and GitHub login/repository. Missing/mismatched binding means disabled. Use the platform user config location (Windows LOCALAPPDATA; Linux XDG_CONFIG_HOME with ~/.config fallback). Store no token.

**Rationale**: `install.py` installs portable bundles and ignores `.novel-creator/local/`. A novel-local boolean alone would allow copied settings to establish authorization. The registry prevents ordinary copied-novel activation without changing story formats. It cannot authenticate human intent against malicious code running as the same OS user; the host must distinguish public direction from quoted story data.

**Alternatives considered**: A tracked preference leaks machine paths and portability assumptions; a copied local boolean violates FR-002; custom credentials or signing infrastructure adds unnecessary complexity.

## 3. Deterministic tool boundary

**Decision**: Add Python retro operations and a narrow GitHub CLI transport; host does semantic review and code work. Transport requires existing authentication and write access to the designated upstream repository, supports direct upstream branches only, and never forks or changes credentials. Optional gh absence blocks participation, not writing.

**Rationale**: `cli.py` already provides strict UTF-8 JSON and ToolError codes; `storage.py` provides safe path and atomic-write patterns. Local `gh pr create --help` confirms explicit --draft, --head, --base, --repo and --body-file; explicit --head avoids implicit push/fork behavior. `--dry-run` may push and must not be used as a harmless test. Local `gh api --help` confirms explicit request methods; all metadata checks use GET.

**Alternatives considered**: Host-only instructions cannot reliably reconcile partial publication; a GitHub Python SDK adds a mandatory dependency; connector-only publication is less portable across installed CLI environments. Optional Codex PR attachment is used after successful creation when that host tool exists.

## 4. Isolation, privacy, and publication

**Decision**: Fetch only after opt-in, create a `codex/retro-<opaque-run-id>` branch/worktree from the observed upstream default branch, and serialize cooperating runs with a lock under the configured Git common directory. Generalize locally before entering the contribution worktree; no novel mounts or transcript copies. Validate an exact diff/tree and publication payload with synthetic reproductions, privacy scan plus semantic review, then persist publication intent before push/create. Use a private temporary body file, explicit remote/base/head, no auto-fill, no private IDs in remote markers, and sanitized errors.

**Rationale**: The configured checkout may have unrelated staged files; a separate index/worktree preserves them. Generic Git helpers are insufficient for network safety because remote URLs, hooks, signing helpers and command output may expose private data. Use canonical token-free github.com transport, disable hooks for tool-owned Git mutation, do not inherit arbitrary GIT_/GH_ repository overrides, and never log authentication output. Project checks are executed only in the synthetic worktree with a minimal environment and no novel evidence paths.

**Alternatives considered**: Editing the configured working tree risks unrelated work; publishing raw evidence violates privacy; pattern redaction alone cannot prove safe generalization.

## 5. Uncertain publication and revocation

**Decision**: Persist the intended head ref, commit and public contribution marker before network mutation. Query exact head and all-state PR history before each retry; search relevant open contributions by generalized finding fingerprint too. Unknown create outcome is publication_unknown; do not send another create request until a prior request can be reconciled. If absence cannot be established confidently, remain blocked for inspection. Recheck enabled grant before each tool-owned mutation and publication; disable invalidates the grant without waiting for the run lock.

**Rationale**: Git and GitHub cannot form one atomic transaction with local receipts. Conservative uncertainty is necessary to avoid duplicate PRs. Revocation prevents subsequent operations, but cannot cancel a request already in flight. Already published work is retained. Disabled resume/release performs no framework or GitHub access and returns re-enablement-required. Explicit successful re-enablement with matching bindings permits a directly requested recovery to adopt its new grant generation; enablement itself starts no editing or publication. Local handling of existing notices remains available while disabled.

**Alternatives considered**: Blind retry duplicates requests; deleting local state loses recovery identity; silently aborting a push does not prove no remote effect.

## 6. Packaging and qualification

**Decision**: Bundle modules/workflows/schemas using current installer resource discovery and package-data rules. New novels only; keep story schema 1.0 unchanged, retro contract version 1 separately. Validate fake-transport journeys, Unicode and Windows path redirection, exact-source wheel installation, then a separate installed native-host journey. Live test PR publication requires its own explicit execution authorization.

**Rationale**: `install.py:bundle_files` pins package modules and recursively copies resources; existing manifests detect changes and do not silently upgrade. `tests/verify_wheel.py` checks resource bytes outside the framework. This was a planning-time limitation; see the implementation ledger for later scoped test evidence.

**Alternatives considered**: Updating old bundles expands scope and violates FR-017; passing mocks cannot establish native-host completion or actual GitHub permissions.

## Resolution

All design unknowns are resolved for this scope. Host task-completion judgments, privacy judgments, actual GitHub access, and native integration remain implementation qualification obligations, not unresolved product choices or claims of verification.
