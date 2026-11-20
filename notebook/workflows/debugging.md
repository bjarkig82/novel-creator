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

Run from PowerShell with the verified runtime and returned ID/directory. Replace
only these path/ID placeholders; `$workingFile` is a supported path relative to
the novel root. A plugin runtime uses its verified `runtime_python` here:

```powershell
$runtimePython = "C:\verified-runtime\python.exe"
$novel = "C:\books\My Novel"
$session = "RETURNED-DEBUG-SESSION-ID"
$recordScript = "RETURNED-SESSION-DIRECTORY\record-observation.py"
$publicText = "RETURNED-SESSION-DIRECTORY\public-text.txt"
$workingFile = "notebook/project.md"
& $runtimePython $recordScript $novel $session --text-file $publicText --file $workingFile --phase before
if ($LASTEXITCODE -ne 0) { throw "Before capture unconfirmed; disclose the gap before proceeding." }
```


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

Use `content` for available public text or structured public observations, and
`files` for project-relative working-file references with `phase` of `context`,
`before` or `after`. Batch compatible observations, but take before snapshots
before changing files. Preserve observed Unicode and whitespace. Record a prepared
assistant message as prepared, not proof of actual display. Capture an actual
public message only if available; do not reconstruct missing text from memory.

Use distinct descriptive operations such as `message.user`, `message.assistant`
and `message.assistant.prepared`; a prepared response is not an observed displayed
message. Record an observed capture limitation as `capture.gap`, with only its
known scope in a public observation. These are observation labels, not new required
fields or evidence that all messages or gaps were captured. Approval, verified
file-save and verified Git-checkpoint observations must stay distinct, including
voice/role handoffs. Explicit debugging consent still permits local diagnostic
capture of available public draft text. It does not approve that text as canon or
authorize saving chat-only drafts into story notes, summaries or authoring files.

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

The readable report counts exact operations and operation/source pairs, including
separate user, assistant, prepared-message and explicit gap labels. It also counts
availability of nonempty observation timestamps and correlation-ID objects,
without reproducing their values or message content in that summary. These are
counts of readable recorded evidence only. Zero events with a label cannot prove
an action was absent; other labels are not silently reclassified. Stopped/partial
is a recording-lifecycle label, never a completeness assessment. An ingestion
timestamp cannot substitute for an unavailable observation timestamp.


## Local notebook retrospective

For an explicitly requested retrospective or current-session opt-in at explicit
session closure, follow the [retrospective workflow](retrospective.md) for
stopping debugging or taking an explicitly requested live snapshot. Select exact
local evidence. Retro uses no log auto-selection, story save, commit, fix or PR.
Sharing defaults to generalized findings. Publication and uploads need current
author approval of the complete outgoing material. Debug capture consent never
implies sharing consent. Existing notebooks need explicit `retro issue setup` preview
and application before this new issue workflow is available.
