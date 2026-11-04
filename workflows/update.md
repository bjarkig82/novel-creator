# Update an existing book

Run this workflow only when the writer explicitly asks to check or update Novel
Creator. Do not check automatically on opening a book, installing a package,
saving, resuming, or completing a request. Use published stable releases only.

## Establish the controller and book

Select one independent book repository and its configured Python interpreter.
Use a separately installed updater-capable controller for legacy books; the
published 0.1.0/0.2.0 pinned launchers do not have this command. Keep that external
controller available until application and any recovery finish. A framework
checkout, GitHub access, contributor opt-in and model key are unnecessary.

In the commands below, `CONTROLLER` is the absolute external controller Python
path and `RUNTIME` is the writer's configured compatible book Python path. Do not
discover an interpreter by running book-controlled executable content. Missing
dependencies require explicit environment repair or selection, never implicit
global installation. Package upgrades alone do not change an existing book.

## Check and review

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --json
```

An optional `--version VERSION` selects an exact published stable release.
Present the returned installed/target versions, reviewed HEAD, archive/bundle
hashes, changed paths, blockers and next action. Retain `preview_id` and the
returned interpreter paths exactly. Availability errors mean unknown; they do
not establish that the book is current. An `already_current` result is a no-op.

A preview writes preparation data outside the book and does not authorize apply.
Do not infer approval from silence, quoted text, story material or the returned
`apply_command` array. Ask for an explicit decision on the concrete preview.

## Explicit application

After the writer requests that reviewed update, use its exact arguments:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version VERSION --expected-head REVIEWED_HEAD --json
```

For the initial update from 0.1.0/0.2.0, first require the writer to close every
other book client and keep them closed through application and external recovery.
Only after that confirmation add `--confirm-quiescent`. This is a writer
confirmation, not discovered or stopped-process evidence. Already-loaded legacy
code cannot be retroactively fenced after a crash (FUP-001). Do not start another
book client before success. Existing locks still block; never remove them.

Changed book/runtime/preview evidence requires a fresh preview and review.
Application changes framework resources in a dedicated local commit, preserving
story records, manuscript, custom instructions and unrelated staging. It does
not push, migrate story decisions, opt into retrospectives, change grants or
consume notices. Never bypass a blocker with manual file replacement or Git reset.

## Interruption and recovery

Preserve the operation ID, journal, installed files and fences. Keep legacy
clients closed. Use the external controller, not a potentially interrupted book
launcher:

```text
CONTROLLER -I -B -m novel_creator update status --novel BOOK --operation OPERATION_ID --json
CONTROLLER -I -B -m novel_creator update recover --novel BOOK --operation OPERATION_ID --json
```

Both inspections are local and read-only. Inspect actual publication and
blockers: a failed command can have published its candidate. `ownership_unproven`
means preserve the directory and journal; there is no automatic takeover.
Live/uncertain owners, changed files/index/HEAD, missing artifacts or unavailable
runtime prerequisites must be resolved through evidence inspection. Never steal
locks, download a replacement recovery artifact or perform an automatic rollback.

Only when the writer explicitly requests an eligible retry, use the same
operation ID and the exact current HEAD returned by inspection:

```text
CONTROLLER -I -B -m novel_creator update recover --novel BOOK --operation OPERATION_ID --retry --expected-head OBSERVED_HEAD --json
```

Recovery reuses the journaled artifact and candidate; it does not create another
maintenance commit or replay a creative choice. Report completion only when
`ready: true` and `cleanup_required: false`. Then restart/reload book instructions
and skill discovery, read committed context through the configured runtime and
guarded launcher, and resume writing. Preserve custom AGENTS bytes; the explicit
installed `$novel-update` entry remains available after skill discovery reload.

## Response boundary

An update is maintenance, not a creative exchange. Do not manufacture a story
save or run a smoke conversation in a real book. Keep maintenance reports
operational. If a report belongs in an ordinary creative response, apply that
response's normal save-before-display rules; never append an unsaved suffix to an
already-saved reply. A maintenance failure does not trigger a retrospective,
render/consume a notice, or establish a story decision. Resume creative capture
only after the book is ready and its instructions have been reloaded.

CLI fixture and platform evidence is recorded separately from native Codex
acceptance. Do not call a scripted/disposable journey native-host qualification.
