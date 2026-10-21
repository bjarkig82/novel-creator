# Codex save-before-emit capability gate

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
