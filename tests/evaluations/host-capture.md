# Codex save-before-emit capability gate

## Delegated-task input route — unavailable, 2026-10-23

Four authorized task-creation/follow-up probes expose delegation tool output and
zero native userMessage items. The tasks stopped without installing or saving a
novel. See [actual observations](product-host-runs/20261023T095949Z/README.md).
This route-specific limit does not revoke or extend the direct typed-input
capability result below; product semantic evaluations remain pending.

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

## Revised exact-input adapter — focused host confirmation pending

T116 adds fixture-prepare.py --user-message-file and updates the Desktop adapter
to serialize the actual current native userMessage instead of retyping it with
a PowerShell here-string. Its native text is preserved verbatim, including LF,
CRLF, leading spaces and intentional trailing blank lines. No universal newline
normalization or host-delimiter exemption is introduced. Missing native tooling,
ambiguous/truncated sources or multi-input messages stop this text-only spike.

The new installed regression failed before implementation and passed afterward
for the exact whitespace cases and invalid-source rejection. The remaining gate
check is one focused real user turn under the revised pinned adapter: compare
selected native source, prepared payload, saved bundle and final displayed text
without normalization. Full suite results are recorded in the development
evidence. Existing spike-02 B/C/D/E/F remain valid and unchanged; do not repeat
the Stop exercise solely for this input-boundary change. T116/T103/T012 remain
unchecked and T013 BLOCKED until the actual-host comparison is supported.

## Actual Desktop experiment — 2026-10-21, spike-02

[Run report and evidence](host-capture-runs/20261021T161928Z-spike-02/README.md):
real ordinary follow-ups, a user-stopped saved response, genuine fresh-chat
recovery, an injected held-lock failure and unchanged retries were exercised.
B/C/D/E/F are supported, with scoped filesystem approval required after initial
and fresh-chat sandbox failures. Seven displayed finals match committed replies.

**Gate remains BLOCKED** on exact user-message parity: all eight captured user
messages omit the terminal LF present in native public user-message readback.
The source of that boundary difference must be established and capture corrected
or the host-only delimiter proven before exact text fidelity can pass. See the
run's unnormalized comparison. No human Stop-test repetition is currently needed.
Return to narrow native adapter planning; T012/T069/T089/T103 stay unchecked and
dependent story work remains blocked. Earlier unavailable-host assessments below
are historical; this run now supplies substantial real host evidence.

## Foundation remediation reassessment — 2026-10-21

The Windows index-flush defect is fixed under T102/T111; the final foundation
suite ran 54 tests (53 passed, one explicit symlink-privilege skip) with exit 0. See
[platform evidence](platform-results.md). Structural installed-fixture tests
are distinct from actual host behavior. The earlier Desktop fixture remains
untouched and must not be reused or manually repaired for a passing result.

T012/T069/T089/T103 remain unverified; T013 remains **BLOCKED**. This implementation
chat has not collected genuine subsequent story turns, human-observed
save-before-display timing, controlled display interruption or fresh-chat
recovery evidence. No host/model/version support is established by a clean
subprocess fixture. The next experiment must use a new fixture after clean
foundation preflight, then follow the existing actual-host procedure with real
user participation. Return to that adapter evaluation before dependent T014+
or their convergence equivalents; no custom runtime or weaker gate is substituted.

## Windows Desktop preflight — 2026-10-21

[Run evidence](host-capture-runs/20261021T154100Z/README.md): Desktop
26.1016.51333 build 21161; user-reported GPT-6.1 Sol, Medium. The new independent
fixture committed bootstrap but returned `cleanup_required: true`. The requested
safeguard requires stopping and preserving receipts/history. Cases A–F have not
started; no display-order, interruption or fresh-chat result is claimed.
T012/T069/T089 remain unverified; **T013 remains BLOCKED**. See the run report
and retained test logs for baseline failures and environment limitations.

## Decision: BLOCKED — actual host evidence unavailable

Recorded 2026-10-21. T012 is **unverified**, not passed. T013's decision is to
stop dependent T014+ implementation and return to adapter planning/actual-host
evaluation. FR-009 remains unchanged. No Codex host/version is claimed supported.
No custom runtime, transcript scraper, post-response hook or model credentials
were added as a substitute.

The execution environment exposes shell/subprocess operations but no actual
interactive Codex session creation/continuation, user-turn injection, fresh-chat
control, or display-interruption control. The coordinator independently confirmed
that thread/interactive host tools are unavailable. This worker's implementation
turn and synthetic subprocess inputs cannot establish those capabilities.

| Required actual-host evidence | Result | Evidence limitation |
|---|---|---|
| Current user message and exact prepared response saved before display | Unverified | Installed fixture tested with synthetic input only |
| Two further automatic turns without reinvocation | Unverified | No actual subsequent host/user conversation exercised |
| Fresh-chat context recovery | Unverified | Subprocess context reader is not a fresh host chat |
| Interruption after commit and before visible display | Unverified | Storage fault windows tested; actual host display not controlled |
| Identical retry with original checkpoint/no duplicate application | Structural pass; host unverified | Real-Git CLI tests only |
| Failed-save disclosure and pause | Storage/CLI pass; visible host disclosure unverified | No actual host response to failure observed |

Host distribution/version: unavailable. Model identifier/version: unavailable.
Actual host messages, receipts, Git checkpoints and display timings: **none**.
Do not fill these with generated results or infer them from the adapter text.
The installed fixture's checksum manifest and local receipts are structural test
artifacts only. Human/semantic quality evaluations have not been conducted.

## Reproducible structural fixture

Requires the active Python environment with installed compatible dependencies.
Use a **new disposable path outside any actual Git repository**:

```bash
python tests/fixtures/host-spike/setup.py --path /absolute/new-disposable-spike
python /absolute/new-disposable-spike/.novel-creator/src/fixture-context.py
```

This fixture contains pinned copies of production source/schema resources, a
local launcher, experimental AGENTS instructions and fixture-only preparation/
context helpers. It uses a disposable repository-local Git identity. It does not
implement the novel initialization/session/resumption stories. It creates no canon.
Do not use it on real writing or reuse an existing directory.

Write the exact visible current user message and prepared response into separate
UTF-8 files; retain all line endings/text that will be displayed. Prepare once:

```bash
python /absolute/new-disposable-spike/.novel-creator/src/fixture-prepare.py --user-file /absolute/user.txt --response-file /absolute/response.txt
python /absolute/new-disposable-spike/.novel-creator/run.py exchange save --novel /absolute/new-disposable-spike --input /path/returned/as/payload_file --json
```

Only a saved receipt permits display of that exact response. Keep the prepared
payload file and exchange ID unchanged for retries. Context returns committed
messages with `display_confirmed: false`, because storage cannot know visibility.
Do not regenerate a different payload for the same exchange identity.

Automated evidence on Linux, Python 3.12.14, Git 2.52.0 and jsonschema 4.26.0:
`python -m unittest discover -v`. Installed-fixture tests run the local launcher
and schema resources from an outside directory, preserve Icelandic text and
trailing newlines, and read committed messages back. Storage tests exercise
candidate rejection on an external commit, pending fault windows, cleanup
warnings, unchanged retries and manuscript/index preservation. These results
are intentionally distinct from the unverified actual-host rows above. Windows,
macOS, physical power-loss durability and performance targets remain unverified.

## Actual-host execution procedure to unblock

Convergence implementation reassessment (2026-10-21): **still BLOCKED**. The
current session provides shell/subprocess tools and thread-status readers, but
no callable facility to create/drive genuine fresh host conversations, inject
real subsequent user turns or interrupt and measure actual response display.
No actual-host messages, timings or host/model/version receipts were collected
by this reassessment. T012 and T069 remain unchecked; T013 remains a stop decision.
Foundation fixes and passing structural tests do not waive the gate.

1. Record the real host distribution/version, model/version, OS/filesystem,
   Python/Git/validator versions, fixture installation manifest and starting Git
   checkpoint. Open the fixture in that host and explicitly start the protocol.
2. Provide a real initial user turn. Capture exact visible user/assistant text,
   save receipt and committed bundle. Verify the save precedes display and that
   no creative suffix was emitted without saving.
3. Provide at least two more real user turns without invoking the entry again.
   Record each response, receipt, digest/sequence and checkpoint; compare exact
   visible text with committed messages. Any missed automatic save fails the gate.
4. Deliberately interrupt the actual host after confirmed save but before display.
   Preserve the receipt and timing evidence; start a genuine fresh chat using
   the installed adapter/context. Recover the saved response without claiming it
   was seen or accepted. Record fresh-chat messages and recovered checkpoint.
5. Retry the exact unchanged payload; verify original checkpoint and unchanged
   exchange/decision count. Do not use a newly generated response under that ID.
6. In the disposable fixture only, induce a held writer lock or unavailable Git
   identity. Verify the host visibly discloses unsaved work, pending exchange and
   last confirmed checkpoint, and pauses authority. Remove only the test-induced
   fault and retry the unchanged payload. Preserve all visible evidence.
7. Review every row against actual artifacts. If any row fails/is unavailable,
   keep the gate blocked and revisit adapter planning. Only a complete actual
   pass permits T014+ implementation; it does not establish later story quality.

## Live experiment attempt — 2026-10-21 13:35 UTC

A disposable installed fixture and partial current-chat capture were prepared;
see [20261021T133322Z run evidence](host-capture-runs/20261021T133322Z/README.md).
Codex CLI 0.163.0 was discovered, but a real native launch failed with a
read-only app-server state directory before any model response. One current
user utterance/prepared reply was saved and read back exactly; identical retry
returned the original checkpoint. Display observation, further automatic turns,
fresh-chat recovery, controlled interruption and visible failure handling remain
unverified. Earlier unavailable-environment notes above describe their original
assessment; this run establishes only the limited observations listed here.
The host gate remains BLOCKED and all related task markers remain unchecked.
# Explicit delegated extension - 2026-10-23

The user selected a separately labeled delegated evaluation route, retaining
all native-input and novice requirements. See
[implementation evidence](delegated-input-support-20261023.md) and
[independent observed gate verification](product-host-runs/20261023T202447Z/gate-verification.json).
Both English/Icelandic delegated gates preserve exact observed input and saved/
displayed response, with save preceding display and fresh CLI reopening.
These results do not convert delegation into native user input. Earlier
unavailable-native observations below remain valid for their tested scope.
