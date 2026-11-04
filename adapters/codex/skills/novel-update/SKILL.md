---
name: novel-update
description: Explicitly check, review, apply or recover a published Novel Creator update in an existing book.
---

Load `.novel-creator/workflows/update.md` from the selected book. For a legacy
book that does not contain it, load the updater controller's packaged shared
workflow and disclose that this is external maintenance tooling. Do not require
a framework checkout or run a package upgrade as though it updated the book.

Check only on the writer's direct request. Use the configured runtime and an
external updater-capable controller. Present a concrete preview, then apply only
after the writer explicitly requests that reviewed version/HEAD/preview ID.
Retain the returned controller/runtime paths and operation ID for recovery.

Initial 0.1.0/0.2.0 application requires closed book clients through application
and external recovery; explain FUP-001 and add `--confirm-quiescent` only after
the writer confirms that lifecycle. Confirmation never bypasses a held lock.
Never replace interpreter paths or operation arguments with guesses.

On interruption inspect locally before offering exact-operation retry. Preserve
unproven ownership, unexpected evidence, grants, notices and unrelated work.
Do not steal locks, reset/stash, auto-rollback, push or start a retrospective.
Report ready only after verified completion, then reload book instructions and
read committed context before writing. Keep operational maintenance separate
from creative authority and honor the shared save-before-display boundary.
