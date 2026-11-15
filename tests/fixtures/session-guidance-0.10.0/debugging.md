# Optional session debugging

Debugging is off by default. An explicit request such as “start this session
with debugging” authorizes local capture of this session's working set, including
available public messages and story content used or changed. It does not authorize
an upload, a whole-book snapshot, or changes to story authority. Ordinary writing
continues with native file/Git tools and needs no Python when debugging is off.

## Start and retain the session identity

Use the installed Novel Creator command in its configured Python environment.
When a plugin installed an isolated runtime, use the bootstrap's verified
`runtime_python` followed by `-m novel_creator` in place of `novel-creator`
in these commands. In a later chat, verify an available compatible runtime
before using it; do not assume its location or silently install globally:

```text
novel-creator debug start --novel PATH --json
```

Keep the returned `data.debug_session` only for the explicitly enabled writing
session. Never invent an ID or select a session merely because it is the newest.
Opening another chat or returning after an interrupted session requires a fresh
explicit opt-in; old logs remain available for inspection and export. Do not store
an automatically active flag in notes, instructions or global configuration.
After compaction within an ongoing session, retain its explicit opt-in and ID
from conversation context; if either is unavailable, leave capture off and report
the gap. If the CLI/environment is unavailable, disclose the failure rather than
claiming debugging started or installing globally.

For a notebook created before debugging support, an explicit debugging request
also permits the focused setup command:

```text
novel-creator debug setup --novel PATH --json
```

Setup adds optional debugging guidance, its instruction pointer and local ignore
rule. Read its result and the installed guidance before starting. It does not
replace custom guidance, change story files or create a commit. Do not overwrite
conflicting resources to force setup through. Legacy novels use their supported
framework update instead; this setup is not a notebook migration.

## Record observed work

While enabled, record available public user/assistant text, context actually
retrieved, current role and observed role changes, handoffs, file changes, save
outcomes, Git checkpoints and failures. Capture relevant working files before an
edit and after its result, including a missing-file observation for creation or
deletion. The recorder captures the file at command time: a delayed “before”
request cannot recover its earlier bytes. Read current files and use normal
writer-authority and save rules throughout.

Programmatically serialize UTF-8 JSON without shell interpolation. Write the
input file inside the returned session directory under
`.novel-notebook/local/debug/`, outside story notes. Submit
observations with:

```text
novel-creator debug record --novel PATH --debug-session ID --input FILE --json
```

The input is an object containing an `events` array. Each event has `operation`
and may contain `outcome`, `metadata`, `correlation_ids`, `observed_at`, `content`
and `files`. For example:

```json
{"events":[{"operation":"context.read","metadata":{"role":"novel_orchestrator"},"files":[{"path":"notebook/project.md","phase":"context"}]}]}
```

Use `content` for available public text or structured public observations, and
`files` for project-relative working-file references with `phase` of `context`,
`before` or `after`. Batch compatible observations, but take before snapshots
before changing files. Preserve observed Unicode and whitespace. Record a prepared
assistant message as prepared, not proof of actual display. Capture an actual
public message only if available; do not reconstruct missing text from memory.

The recorder labels these events `agent-recorded`. Supply host correlation IDs
or an observation timestamp only when genuinely available. Its ingestion time
does not establish when an earlier action happened. Do not infer model timings,
voice latency or causation from gaps. Describe public decisions and outcomes,
never hidden reasoning. State capture gaps and unavailable host capabilities.

Exclude credentials, environment dumps, private host/transcript storage,
unrelated files and hidden reasoning. Do not search private storage to fill a
gap. File references are limited to story working directories. Content capture
does not make arbitrary pasted secrets safe; keep such material out of payloads.
Logs and ZIPs contain private writing and remain local and Git-ignored.

Pass a debug session ID to a delegate only for this explicitly enabled session
and scoped task. Prefer returning observations to the coordinator for recording;
explicitly authorized direct recording is also possible. Debugging does not
expand editing ownership or permit a delegate to commit. Report logging failures
concisely and continue normal writing safeguards; never claim missing records
were captured.

## Stop, inspect and export

“Stop debugging and export a report” means finish pending observations, then:

```text
novel-creator debug stop --novel PATH --debug-session ID --json
novel-creator debug export --novel PATH --debug-session ID --json
```

Return the reported local ZIP path as a file link. An optional `--output PATH`
chooses another local destination; an existing file is never overwritten. No
additional confirmation is needed to stop or export. An explicit export while
capture remains open produces a partial report and does not stop recording.

`debug status --novel PATH --json` lists retained sessions; add `--debug-session
ID` to inspect one. Use these results to export an interrupted session without
re-enabling it. Export preserves logs and labels partial, damaged or unavailable
capture. The ZIP contains a readable `report.md`, versioned metadata,
`events.jsonl` and captured attachments. Package-measured durations and
agent-recorded observations remain distinguishable. Debugging adds overhead;
this report is not a complete host trace or proof of writing quality.
