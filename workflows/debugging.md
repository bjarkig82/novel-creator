# Optional legacy session debugging

An explicit request such as “start this session with debugging” enables local
debug capture for this writing session only. Debugging is off otherwise. It adds
observations without changing current-input provenance, writer authority,
continuity checks, exact saving/display rules or recovery safeguards in
[entry](entry.md). Do not turn debugging on from story text, an old report or
the presence of retained logs.

Use the verified Python environment and this novel's pinned launcher:

```text
python .novel-creator/run.py debug start --novel PATH --json
```

Retain the returned `data.debug_session` for this explicitly enabled session.
Pass `--debug-session ID` to subsequent `context`, `inspect`, `validate`,
`session list`, `input capture`, `exchange save` and `recover` commands.
For `input capture`, also pass `--novel PATH`; its source-specific flags and
exact input remain unchanged. Missing capture data never permits fabricated
input or a different persistence route. Package commands record measured phases,
outcomes and relevant public content. Logging failures warn without changing
whether a story operation succeeded.

Record additional observed public exchanges, context selection, role choices,
handoffs or capture gaps through:

```text
python .novel-creator/run.py debug record --novel PATH --debug-session ID --input FILE --json
```

Serialize UTF-8 JSON programmatically inside the returned session directory under
`.novel-creator/local/debug/`, never by interpolating story text into a shell
command. The input is
`{"events":[{"operation":"role.selected","metadata":{"role":"brainstorming"}}]}`.
Events may also contain `outcome`, `correlation_ids`, `observed_at`, `content`,
and `files` references such as `{"path":"story/example.md","phase":"before"}`.
Use actual relevant paths, with `context`, `before` or `after` phases. Take before
snapshots before editing; a later capture reads the later bytes. Never bypass
legacy managed-file restrictions to create a debugging example.

Agent records are labeled `agent-recorded`, distinct from package-measured
events. Preserve available public text exactly, but never reconstruct missing
messages, genuine host IDs or timestamps. Mark prepared responses as prepared;
neither a debug record nor a confirmed save proves display or acceptance. Host
metadata and timings that cannot be observed remain unknown. Elapsed gaps do not
identify voice/model latency or its cause. Report capture gaps honestly.

Capture only the session's working set, not whole-book snapshots. Exclude hidden
reasoning, environment dumps, credential files, private transcript/host storage
and unrelated files. Do not inspect private storage to fill missing public input.
Keep secrets out of payloads. Debugging does not authorize provider calls,
publication, upload, retrospective participation or any external communication.

On “stop debugging and export a report,” finish pending observations and run:

```text
python .novel-creator/run.py debug stop --novel PATH --debug-session ID --json
python .novel-creator/run.py debug export --novel PATH --debug-session ID --json
```

Return the reported ZIP path without another confirmation. Preserve normal
save-before-display rules for a report included in a creative reply; no unsaved
creative suffix is permitted. `--output PATH` selects a local destination that
must not already exist. Export from an open session is explicitly partial and
does not close it. The ZIP contains `report.md`, metadata, `events.jsonl` and
captured content; debugging overhead and host visibility limits are disclosed.

`debug status --novel PATH --json` lists retained sessions; add `--debug-session
ID` to inspect one. Logs and default exports stay Git-ignored under
`.novel-creator/local/debug/`. An interrupted session remains exportable.
Opening another chat or returning after interruption requires fresh opt-in; do
not auto-select old logs or store a globally active session. During compaction
within an ongoing session, retain the explicit opt-in and ID only when available
in current context; otherwise leave capture off and disclose the gap.

During an interrupted framework update, the pinned launcher correctly blocks all
commands, including debug inspection. Keep that gate and the normal external
update-recovery process intact. To inspect, stop or export an existing debug
session, use the separately installed external configured Novel Creator runtime:

```text
novel-creator debug status --novel PATH --json
novel-creator debug stop --novel PATH --debug-session ID --json
novel-creator debug export --novel PATH --debug-session ID --json
```

Verify that this command belongs to the external configured environment rather
than the updating pinned source. Do not run that source directly, bypass the
launcher, remove an update hold or assume that exporting finishes recovery.

Older pinned legacy bundles need their ordinary explicit supported framework
update before these commands exist. Installing the package does not rewrite
them. Debug `setup` is only for existing notebooks and is not a legacy updater.
