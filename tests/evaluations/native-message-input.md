# Exact native-message input remediation — T116

## Current decision: PASS — focused spike-03 confirmation

The actual Desktop capture gate is passed for the tested Windows Desktop
native-tool, single typed-text input and scoped filesystem approval combination.
Native source, prepared payload and committed user text match exactly, including
the ending LF; the displayed reply matches the saved assistant text, and the
save event precedes display. [Actual run and scope](host-capture-runs/20261021T171237Z-spike-03/README.md).

Spike-02 supplies the retained automatic-turn, interruption, fresh-chat,
failure-disclosure and unchanged-retry evidence. Spike-03 resolves its manual
here-string input loss using the original native userMessage text. Capture
source JSON belongs under `.novel-creator/local/evidence/`, outside root receipt
discovery. No old exchange or payload ID was rewritten.

T012/T069/T089/T103/T116 are complete; T013's current decision is PASS. No further
manual host test is required for this change. Dependent story implementation may
begin. Product workflows, release readiness, voice, other hosts and unattended
default-sandbox operation remain unverified.

The earlier assessments and procedures below are retained as historical records.
Their BLOCKED/pending statements are superseded by this decision; their test
counts describe their respective runs.

## Historical assessments and procedures

2026-10-21. This is a foundation/adapter remediation; dependent story work has
not begun. T116/T103/T012 remain unchecked and T013 BLOCKED until the focused
actual-host comparison passes. Do not turn structural tests into host proof.

## Boundary and change

Spike-02's eight stored user messages differ by one terminal LF from native
public user-message readback. The chats wrote manually reconstructed PowerShell
here-strings to input files. A direct PowerShell probe confirms that a here-string
containing Þóra before the closing-marker newline has length four and no ending
LF. Existing fixture preparation already reads raw bytes without trimming.
No claim is made that every host/user input ends in LF or that a host-only
delimiter may be discarded.

The revised Desktop adapter uses the selected current public userMessage from
native read_thread, identified through CODEX_THREAD_ID. It serializes that
object directly to a local JSON source and invokes fixture-prepare.py
--user-message-file. The helper takes content[0].text verbatim and rejects wrong
roles, missing IDs, multiple text inputs and non-text sources. Native IDs remain
ignored local source evidence, outside the platform-independent story schema.
The legacy exact-byte --user-file mode remains for structural fixtures.

The official [App Server item contract](https://learn.chatgpt.com/docs/app-server#items)
describes userMessage content as user inputs. It does not establish a newline
stripping convention. This adapter preserves the provided text rather than
inferring such a convention. No private conversation database, transcript
scraper, model API, new runtime or schema migration was introduced. Application
resource inspection was read-only and did not modify the installed app.

Native read_thread can read an active turn in this session. The current realtime
turn contains two user items from steering, so it is not used as text-only story
evidence. Ambiguous current messages must stop capture. The follow-up fixture
requires one ordinary typed input and available native tools, not voice/steering
or unsupported multi-input capture.

## Red/green and verification

The new installed-fixture regression failed before implementation because the
native-message option did not exist. Afterward it passed four independently
specified exact-text cases: one LF, leading spaces plus three trailing LFs,
leading/trailing CRLF with Icelandic text, and no ending newline. Real installed
CLI saves and context readbacks retain exact user/assistant text. Wrong-role,
multi-text and image-only native items return code 2 without a traceback or
prepared output.

Final complete command, using normal filesystem access and canonical disposable
temp repositories outside the framework:

```powershell
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
.\.venv\Scripts\python.exe -B -m unittest discover -v
```

**55 tests in 121.279s: 54 passed, one explicit Windows symlink-privilege skip,
zero failures/errors, exit 0.** [Full log](windows-native-message-tests.txt).
Git diff whitespace checks pass. Bash files were not changed; their earlier
syntax evidence stands, while full Bash smoke remains unavailable without jq.
No new Linux/macOS, physical durability or semantic language claim is made.

## Focused real-host follow-up

New fixture: `C:\Users\BjarkiGunnarsson\novel-creator-host-tests\spike-03`.
[Preflight](native-message-preflight.json) confirms clean bootstrap, no cleanup
warning, all 13 pinned checksums and matching revised AGENTS instructions.
Bootstrap checkpoint: `4ad16e6c487ce31d13beb5bc4cec54bebc4f222d`, sequence 1.
No conversation has been run in it yet.

Open spike-03 as the test workspace, start one fresh chat and send one typed
capture prompt using the framework .venv interpreter. The chat must serialize
its actual native current user item, prepare/save the reply, and display only
the saved reply. Review source text, payload, committed user text and native
final response with no whitespace normalization. If a required filesystem
operation is sandbox-blocked, retain the payload and request scoped approval;
held locks must not be removed or bypassed.

Preserve spike-02 and its B/C/D/E/F evidence unchanged. The input-only adapter
change does not require another human Stop-button exercise. Only a focused
real-host input comparison remains; there is no passing gate decision yet.
