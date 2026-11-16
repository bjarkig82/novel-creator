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

Each `operation` must be a nonempty, nonblank string. The exact, case-sensitive `debug.`
prefix is reserved for package lifecycle events; use labels such as
`context.read`, `message.user`, `message.assistant.prepared` or `capture.gap`.
File references use project-relative forward-slash paths under `notebook/`,
`manuscript/`, `research/`, `reviews/` or `story/`, with `.md`, `.txt` or `.json`
extensions (case-insensitive). Phases are `context`, `before` and `after`;
omitting a phase defaults to `context`. Supported missing paths record
`exists: false`, which can describe creation or deletion without inventing bytes.

Absolute paths, `..` traversal, backslashes, colons, control characters, hidden
components, trailing dots/spaces, symlinks, junctions and special files are
excluded. Components named `credentials`, `secrets` or `private`, and filenames
containing `credential`, `secret`, `password` or `token` are excluded
(case-insensitive). These rules also exclude instructions, tool source and local
debug files outside the story roots. Do not relocate unsupported files to evade
these limits or bypass legacy managed-file restrictions. Payloads must never
contain credentials, private host/transcript data or hidden reasoning.

### Executable file-based recording recipe

Use native file tools to save the following helper as `record-observation.py`
inside the **returned current session directory**. Also put any exact available
public text in a UTF-8 `public-text.txt` there, preserving its original Unicode,
apostrophes, typography, line endings and whitespace. These are local diagnostic
inputs, outside story notes. Do not type story text into shell command strings.
The helper serializes one event as UTF-8 JSON and uses a subprocess argument list;
it does not change the recorder API, start a session or edit story files.

<!-- record-observation.py -->
```python
import argparse
import json
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("novel")
parser.add_argument("debug_session")
parser.add_argument("--operation", default="context.read")
parser.add_argument("--text-file")
parser.add_argument("--file")
parser.add_argument("--phase", choices=("context", "before", "after"), default="context")
parser.add_argument("--launcher")
args = parser.parse_args()
event = {"operation": args.operation}
if args.text_file:
    event["content"] = Path(args.text_file).read_bytes().decode("utf-8")
if args.file:
    event["files"] = [{"path": args.file, "phase": args.phase}]
input_file = Path(__file__).with_name("observation.json")
input_file.write_text(json.dumps({"events": [event]}, ensure_ascii=False,
                                allow_nan=False), encoding="utf-8")
command = [sys.executable, args.launcher] if args.launcher else [sys.executable, "-m", "novel_creator"]
completed = subprocess.run(command + ["debug", "record", "--novel", args.novel,
    "--debug-session", args.debug_session, "--input", str(input_file), "--json"],
    capture_output=True, text=True, encoding="utf-8")
result = json.loads(completed.stdout)
sequences = result.get("data", {}).get("recorded_sequences", [])
if completed.returncode != 0 or result.get("ok") is not True or len(sequences) != 1:
    raise SystemExit("Capture unconfirmed; disclose the gap. " + completed.stdout + completed.stderr)
print(json.dumps(result, ensure_ascii=False))
```

Run from PowerShell with the verified runtime and this novel's pinned launcher.
Replace only these path/ID placeholders; choose an actual relevant supported
story file for `$workingFile`. The helper does not edit that managed file:

```powershell
$runtimePython = "C:\verified-runtime\python.exe"
$novel = "C:\books\My Novel"
$session = "RETURNED-DEBUG-SESSION-ID"
$recordScript = "RETURNED-SESSION-DIRECTORY\record-observation.py"
$publicText = "RETURNED-SESSION-DIRECTORY\public-text.txt"
$workingFile = "story/example.json"
$launcher = Join-Path $novel ".novel-creator/run.py"
& $runtimePython $recordScript $novel $session --launcher $launcher --text-file $publicText --file $workingFile --phase before
if ($LASTEXITCODE -ne 0) { throw "Before capture unconfirmed; disclose the gap before proceeding." }
```

Keep `--launcher $launcher` on subsequent legacy helper calls. The launcher keeps
its update hold; do not silently fall back to source imports or a different runtime
to force recording through. External-runtime inspection/export during recovery
is described below and does not permit bypassing the update gate for story work.

Before any authorized edit, require a zero exit status, `ok: true` and the
expected `data.recorded_sequences` entry. Only then is that before snapshot
confirmed. After the edit, run the helper again with `--phase after`; for reading
context use `--phase context`. Omit `--text-file` for a file-only observation,
or omit `--file` for a public-message observation and choose its exact operation
with `--operation`. Use only genuinely available public text, not a reconstruction.

If capture fails, report it concisely and continue the ordinary writing safeguards;
debugging failure does not authorize a different save route or block otherwise
authorized writing. If recording becomes available, record `capture.gap` using
`--operation capture.gap --text-file PATH_TO_UTF8_GAP_DESCRIPTION` without
`--file`. Describe only the known missing scope, not guessed original content.
If writing proceeded before a successful snapshot, record the later file as
`context` or `after` and disclose the missing original. Never retry it as an
original `before` snapshot: the recorder reads bytes at command time and does not
verify the truth of a supplied phase label. If the gap itself cannot be recorded,
state it in the conversation/report and do not claim that any record was saved.

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

## Local notebook retrospective

For an explicitly requested retrospective or current-session opt-in at explicit
session closure, follow the [retrospective workflow](retrospective.md). Stop
known current debugging before review and keep it off. Select exact local
evidence; no log auto-selection, story save, commit, fix or PR. Sharing defaults
to generalized findings; any publication/upload needs current author approval
of the complete actual outgoing material. Debug capture consent never implies
sharing consent. Existing notebooks need explicit `retro issue setup` preview
and application before this new issue workflow is available.
