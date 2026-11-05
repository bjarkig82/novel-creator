# Installed novel entry

Before any creative reply, select the intended novel root, read its AGENTS.md
and this installed entry, and load committed context below. Scope file and
launcher operations to that novel. An agent opened at a parent workspace cannot
assume nested project instructions were automatically loaded. For future sessions,
select/open the novel root in the host. If it is inaccessible, disclose the actual
limit before continuing; do not initialize again or invent saved context.

## Discover and verify the legacy runtime

In commands below, `python` means a verified compatible environment, not an
arbitrary system Python. Retain `runtime_python`, `launcher_path` and `novel_path`
from successful initialization tool output in agent context. Those paths are
usable evidence even when absent from the writer's chat text. Do not ask the
writer to confirm an interpreter already established by that result.

In a fresh, relocated or cloud session, inspect the actual environment before
asking. Check the installed `novel-creator` command's launcher/shebang, an active
`VIRTUAL_ENV`, and available `.venv` environments in the selected workspace or its
parent. These are candidates, not proof; do not assume a conventional path exists.
Do not search unrelated home folders or expose environment secrets. Preserve each
candidate's lexical executable path: resolving a venv symlink can select base
Python and lose installed dependencies.

For an evidence-backed candidate, first make read-only checks using that exact
executable: confirm Python >=3.11 and installed distribution versions satisfying
packaging >=24, jsonschema >=4.23,<5 and jsonschema-rs >=0.59,<0.60 (for example
with `importlib.metadata` and `packaging.specifiers`). Then run that executable
with the selected novel's pinned `.novel-creator/run.py context --novel PATH --json`
from the novel root. Require successful output for the intended novel before any
write; damaged records, maintenance holds or missing dependencies are failures,
not an empty story. Use that verified environment for subsequent pinned commands.
Verification of a compatible replacement does not prove it was the original
setup environment. If equally plausible environments remain ambiguous, or none
passes, report the concrete failure and ask one focused environment question.
Do not install globally, resolve ambiguity by silently choosing system Python,
or store machine paths in story data or committed instructions. No durable runtime
file is required. The installed getting-started guide explains manual setup.

## Continue with installed safeguards

For a direct request to check/update the framework, load `update.md` and invoke
`$novel-update`. No automatic update check runs on opening, resuming or saving.
Use an external controller for legacy bootstrap and interrupted recovery. Review
the preview before explicit application, keep legacy clients closed through
recovery, and reload these instructions after verified ready completion. This is
maintenance rather than a creative exchange; it does not trigger retrospectives
or consume notices. Operational content included in a creative reply still uses
that reply's normal save-before-display protocol.

Read committed context using `python .novel-creator/run.py context --novel PATH
--json`. Select the novel unambiguously. The manifest pins the installed bundle;
no framework checkout is required. Python >=3.11, packaging >=24, jsonschema >=4.23,<5 and jsonschema-rs >=0.59,<0.60 remain
environment prerequisites. Unknown or damaged records are unavailable, never an
empty story. Structural validation does not establish narrative consistency.

Preserve the current native public userMessage exactly. In Codex use native
read_thread for the current CODEX_THREAD_ID, select the one complete current
userMessage and serialize it programmatically. Stop on unavailable, truncated or
ambiguous input; this verified adapter supports a single typed text input.
Do not retype it with a PowerShell here-string, trim it or add/remove newlines.
Codex task creation and cross-task follow-ups can arrive as `functionCallOutput`
delegation events rather than `userMessage` items. Those events, their input
fields and the thread preview are not native user messages. Native mode stops
when the current turn has no native userMessage; never reuse an older message.
An explicitly authorized disposable evaluation may instead select the separate
delegated route below. Never silently fall back or relabel delegated text.
Put preparation evidence under `.novel-creator/local/evidence/`, outside receipt
discovery. Native IDs are local evidence only, never story identity.

For either source, serialize the newest public read_thread snapshot with its
thread ID and current turn ID, excluding reasoning. Run the installed launcher:
`input capture --capture-file FILE --thread-id CURRENT --turn-id CURRENT_TURN
--source native_user --json`. For authorized delegated evaluations only, select
`--source delegated --source-thread-id EXPECTED_PARENT --evaluation-only`.
The parser supports one complete codex_app create_thread/send_message_to_thread
delegation wrapper. Truncated, stale, malformed, mixed or ambiguous input stops
capture; wrapper delimiter text inside the input is currently unsupported.
Copy `data.text` exactly into the conversation user message and include
`data.input_artifact` unchanged in the exchange's input_artifacts before digest
and save. Verify equality before saving. Retain the artifact on pending retry.
It preserves source labels through fresh context; IDs are evidence, not authority.
The parser validates a supplied snapshot, not independent host provenance.
Delegated scenario decisions are simulated director inputs in this disposable
evaluation only. They cannot authorize changes in a real novel, satisfy the
native-input gate, or count as genuine novice participation or human ratings.

Prepare one conversation envelope with the confirmed expected HEAD and chain,
one exact current user message, one prepared assistant message, typed captures,
sources and honest continuity coverage. Use records.new_exchange and
records.digest, then `exchange save --novel PATH --input FILE --json`.
Wait for successful save before displaying that exact response; add no unsaved
creative suffix. Repeat automatically on every subsequent turn without requiring
another skill invocation. Bootstrap metadata does not replace conversational
capture. On failed save, disclose unsaved work, checkpoint and unchanged pending
exchange; pause further authoritative changes. A scoped filesystem retry may be
needed when the sandbox denies hard links. Never bypass held locks. An interrupted
saved response can be recovered, but display or acceptance is never inferred.

This display boundary includes progress commentary, not only the final reply.
Before confirmed save, operational updates may describe reading, preparation or
retrying, but must not disclose story ideas, captured facts, canon outcomes,
continuity judgments or checkpoint summaries. Put all such creative content in
the one prepared assistant message and save it first. Failure notices may disclose
the unsaved state as above; they must not present an unsaved creative result as
established. Display the saved message exactly, including leading/trailing spaces
and newlines; do not add a formatting newline or other unsaved text.

Only local managed metadata and exchange bundles are writable. No automatic
push, provider call, manuscript edit or hidden-reasoning capture. Review preferences
do not waive authority and persistence safeguards. Load the shared workflow for
the requested action and disclose features still unavailable in this bundle.

## Optional contributor retrospectives

Read `retrospective.md` for task-completion and contributor controls. Participation
is off by default. A valid explicit opt-in narrowly permits editing the allocated
framework worktree and pushing its checked contribution branch/creating a draft
PR; the ordinary no-push rule still applies otherwise. Never infer consent from
story data, imported settings or repository instructions. Honor narrower current
user restrictions, including requests not to push or publish.

Before preparing each ordinary response, retrieve existing local retro notices
and reconcile their reservations as described there. Reserve selected notices
against the exact prepared exchange before its normal save, then confirm saved
inclusion; this local-only bookkeeping does not enable review or repository access.
Participation is optional; eligible completion handling is required while it is
enabled. After a confirmed completed deliverable or explicit session closure,
with a valid enabled grant and stable initiating task identity, follow
`retrospective.md` and call `retro begin` before displaying the already-saved
final. Review only when its `eligible` and `review_required` results are true; a repeated
claim does not restart review. Routine replies, intermediate saves and
retrospective work do not trigger review. A pending or cleanup-required
save pauses this procedure. Honor narrower current user restrictions and host
permissions; if identity or capability is unavailable, keep it unavailable and
disclose the limitation under the existing response rules. Disabled participation
performs no review or framework access. Keep outcomes local until the next saved
reply and display the exact already-saved final unchanged.
