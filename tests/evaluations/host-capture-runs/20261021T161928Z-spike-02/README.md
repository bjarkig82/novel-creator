# Actual Desktop host capture — BLOCKED on user-message parity

Date: 2026-10-21, Atlantic/Reykjavik (UTC). Fixture:
`C:\Users\BjarkiGunnarsson\novel-creator-host-tests\spike-02`.

This was a real user-driven Desktop experiment, not synthetic model input.
The user supplied ordinary follow-ups, opened a fresh chat, observed responses
and reported successfully pressing Stop before the final response. The
coordinator inspected committed records and performed the B/F identical retries
and the documented empty-lock injection/removal. No messages were injected into
the test chats by the coordinator.

## Observed environment and sources

- Installed Windows Store package: OpenAI.Codex 26.1016.6573.0, read using
  Get-AppxPackage. This is the package version; current About build unmeasured.
- Model selector: GPT-6.1 Sol Medium, visible in the user's screenshot.
  Underlying model revision unavailable, not inferred.
- Windows 11 10.0.26300, NTFS, Python 3.13.13, Git 2.53.0.windows.3,
  jsonschema 4.26.0. Interpreter: framework `.venv\Scripts\python.exe`.
- All 13 installed manifest checksums verified. Final fixture Git status clean.
- Source chats: `01a15f44-b3d0-7c12-882b-a0d35ac96ba4` and genuinely new
  `01a15f5a-17e7-72e3-9b46-e1c5bf30d155`.

[Native host observations](native-host-observations.json) retain public user and
assistant text, save-command results, turn status and deliberate waits. Hidden
reasoning and unrelated tool commands are excluded. This uses the supported
read_thread tool, not private transcript/database scraping. Native event order
supports save-before-final ordering; user screenshots/reports supply separate
human observations. No independent screen recording was supplied.

[Fixture snapshot](fixture-snapshot.json) preserves validated committed exchanges,
local receipts, payload hashes, case observations and checkpoint comparisons.
These exported copies are review evidence; the independent fixture's committed
Git chain remains authoritative. [Manifest](manifest.json) describes the pinned
installation. Stored data was not rewritten to make any comparison pass.

## Results

| Case | Result | Evidence |
|---|---|---|
| A: initial turn plus two automatic follow-ups | PARTIAL; exact user capture unresolved | Initial sandbox save failed safely, then scoped normal-access retry saved sequence 2. Ordinary follow-ups saved sequences 3/4 automatically. Native successful save events precede finals; displayed assistant text matches committed text exactly. All submitted user texts have an extra terminal LF relative to stored text. |
| B: unchanged committed retry | PASS | Sequence 4 repeat returned already_saved, same HEAD and unchanged commit/exchange counts. |
| C: saved before interrupted final | PASS | Sequence 7 committed at 21a88fd7cc5a8b7584df4e51b95c625bc4478b7b. Turn 01a15f57-dfbb-7763-b4f0-df610c2a26d2 is interrupted after success and operational Saved/Stop commentary, with no final. User reported stopping at the intended point. |
| D: genuine fresh-chat recovery | PASS with approval/retry limitation | New chat recovered sequence 7 and exact saved text without receiving it in its prompt, explicitly retained unconfirmed display status. Its own first save failed; unchanged scoped retry committed sequence 8. |
| E: visible failed-save disclosure/pause | PASS | Coordinator created only the absent empty write.lock. Native error code 6 and visible user-pasted disclosure reported pending ID and sequence 8 checkpoint; HEAD remained unchanged and no new exchange file/receipt existed. |
| F: unchanged failed-attempt retry | PASS | After removal of only the verified injected empty lock, host saved original payload as sequence 9. Its parent is the original failure checkpoint. Coordinator's identical repeat returned original success without another commit or exchange. |

The two earlier 45-second interruption attempts reached final display and do
not establish case C. The later indefinite 30-second-interval wait was stopped
by the user and provides the successful case. Expected operational progress
messages are distinct from story responses.

Final checkpoint: sequence 9, exchange `3c5fb0fc-83b2-4e57-839a-d6b534eac869`,
commit `aefc319663a948fcce1ec06d4f1097e084f864fc`.

## Remaining gate issue

[Exact user comparison](user-message-parity.json) checks all eight conversation
exchanges without whitespace normalization: zero exact matches, eight matches
only after adding one terminal LF to stored user text. Seven displayed final
assistant responses match committed responses exactly; the eighth was the
deliberately interrupted response, which had no final display.

The native user-message record includes a terminal LF that the host-prepared
here-string inputs omit. This could reflect capture loss or a host record
boundary convention; its origin is not yet independently established. Neither
possibility may silently waive FR-009's exact capture requirement. Do not call
raw submitted-user-text parity verified, edit committed messages, normalize
away the discrepancy or regenerate prior payloads under the same IDs.

Next adapter work: establish the native current-message boundary, preserve its
exact text including intentional trailing line breaks, add a regression and run
a focused actual-host comparison. If the LF is a host-only envelope delimiter,
document that using authoritative host evidence before excluding it. No repeat
of the human Stop-button exercise is presently needed.

Both initial/fresh-chat saves also hit sandbox denial of os.link (WinError 5).
The chats disclosed failure and paused; scoped normal-filesystem retries passed
without changing the pending payloads. Default-sandbox unattended operation is
not established. Native adapter planning must account for this permission
boundary; no broad sandbox disablement or custom runtime is authorized.

**T012/T069/T089/T103 remain unverified; T013 remains BLOCKED.** No supported-host
or full feature/release claim follows. B/C/D/E/F evidence is retained so the
remaining adapter investigation can be narrow. Prior failed fixtures remain
untouched; only this run's deliberately injected empty lock was removed.
