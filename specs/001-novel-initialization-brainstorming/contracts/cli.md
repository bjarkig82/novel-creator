# Local CLI Contract v1

Status: planned interface. Commands below become runnable during implementation.
Use `python -m novel_creator` from the framework environment or the installed
novel-local launcher `python .novel-creator/run.py`. No server or model key.
Paths are arguments, never shell-interpolated user story text. UTF-8 JSON input
files avoid shell quoting problems for Icelandic and multiline conversation.

## Operations

| Command | Inputs | Result / authoritative effect |
|---|---|---|
| `init --path PATH --brief-file FILE --json` | Explicit target; brief with unknowns allowed | Independent Git root, versioned bundle, project bootstrap; no invented canon |
| `input capture --capture-file FILE --thread-id ID --turn-id ID --source native_user --json` | Exactly one current public read_thread turn | Exact text and source evidence artifact; no novel write or authority effect |
| `input capture --capture-file FILE --thread-id ID --turn-id ID --source delegated --source-thread-id PARENT --evaluation-only --json` | Explicitly authorized disposable evaluation and complete supported delegation event | Delegated text/provenance; never native input, real human approval or novice evidence |
| `session list --novel PATH --json` | Novel | Session identities/topics/modes/status; read-only |
| `context --novel PATH --session ID --json` | Optional session/focus refs | Confirmed head, relevant records/sources, open questions, findings and availability |
| `exchange save --novel PATH --input FILE --json` | Complete exchange envelope and expected HEAD | Validate and commit exactly once; session create/mode/close changes are typed record versions |
| `inspect --novel PATH --kind KIND --id ID --json` | Filters; optional historical revision | Records and history with source links; no modification |
| `validate --novel PATH --json` | Novel | Schema/chain/references/transitions and availability report, not narrative verdict |
| `recover --novel PATH --exchange ID --json` | Pending transaction or interrupted saved response | Report pending/published/cleanup-needed state and safe next action; no silent overwrite, rollback or canon change |
| `recover --novel PATH --exchange ID --retry --expected-head SHA --json` | Explicit retry of unchanged validated pending payload | Finish original transaction or managed-index cleanup without replay; reject stale/conflicting work |

`context` without a session returns novel overview and sessions for selection.
Session creation/closure use the same exchange transaction as the conversation,
so a second independently writable session store is unnecessary.

## Machine-readable output

Every `--json` invocation emits one JSON object to stdout; diagnostics go to
stderr without leaking story contents unnecessarily. Success contains
`ok: true`, `operation`, `novel_id`, `data`, `warnings` and `checkpoint`.
Checkpoint contains committed `git_head`, last `exchange_id` and sequence.
The non-novel `input capture` operation returns only `ok` and `data`, containing
exact `text`, `source_type` and `input_artifact`; it neither reads nor writes a
novel and therefore supplies no saved checkpoint. The caller includes the
artifact unchanged in the prepared exchange. Conversation validation allows
exactly one such evidence artifact, validates its event/labels/message binding,
and excludes it from bootstrap creative-source lookup. Existing no-artifact
conversations and initialization artifacts retain their prior semantics.
After successful conditional ref publication, index synchronization failure returns
`ok: true`, `data.saved: true`, `data.cleanup_required: true` and a warning,
with exit code 0 and the published checkpoint. Pause subsequent writes until
`recover` safely synchronizes managed entries; do not replay or roll back the save.
A read may return available data with `coverage: incomplete` and unavailable
references; it must not silently claim complete context.

Failure contains `ok: false`, `error: {code, message, affected_refs, retryable}`,
`last_confirmed_checkpoint` and `pending_exchange_id` where applicable. Exit codes:
0 success, 2 invalid arguments/schema/reference/transition, 3 existing-content or
stale-write conflict, 4 unavailable context/unsupported schema, 5 filesystem/Git
save failure, 6 lock held. An identical committed retry returns 0 with
`already_saved: true`; altered payload with the same ID returns conflict.

## Initialization boundaries

Do not create nested novel repositories inside the framework or another Git
repository. A new/empty directory is safe; an existing recognized novel returns
its identity and continuation instructions without recreating it. Unrelated
nonempty directories or repositories return conflict and offer a separate path;
never overwrite, move or import their contents implicitly. Verify prerequisites
and Git identity before creating the first confirmed checkpoint; report a partial
bootstrap as incomplete and support retry without erasing content.

Install the managed bundle with manifest checksums. Preserve existing AGENTS.md;
add a marked discoverability section only with installation scope authorization,
or provide a separate file with explicit entry instructions. Never replace its
contents. The creative brief is source input; it is not acceptance of inferred
facts. Preserve the original supplied brief as a bootstrap input artifact, with
its parsed value and digest; source references identify artifact fields via JSON
Pointers, never invented conversation messages. System defaults have explicit
default origin. Only actual user messages can authorize later canon transitions.
The agent offers optional brainstorming after successful setup.

## Save authorization and write boundary

Only novel-local managed metadata, installed resources during explicit setup or
upgrade, and exchange bundles are writable. Exchanges cannot supply arbitrary
filesystem destinations or Git options. Resolve root containment, reject traversal
and symlink escapes, and never write manuscript paths. A canon revision may
produce references needing review; it cannot edit those referenced artifacts.
Saving errors pause further authoritative changes until recovery succeeds.
No command pushes a remote or changes host account settings.
