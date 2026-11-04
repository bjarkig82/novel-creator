# Update Compatibility Follow-ups

## FUP-001 - Legacy runtimes cannot enforce a new durable update pause

**Recorded**: 2026-11-03

**Status**: Foundational investigation completed on 2026-11-03; product qualification remains open. Actual historical subprocess probes support the documented closed-client/guarded-launcher design. They do not qualify a production updater, which is not yet implemented.

**Finding**: The 0.1.0/0.2.0 book runtimes predate update journals. Their story writer honors `.novel-creator/local/write.lock`, but `storage.writer_lock()` removes that directory on normal context exit. A new updater journal alone cannot pause those runtimes. In 0.2.0, retrospective authorization and notice operations use separate locks and do not all honor the story writer lock.

**Evidence**: Source inspection of `src/novel_creator/storage.py` (`writer_lock`, `_save`) and `src/novel_creator/retro.py` (`lock`, `enable`, `disable`, notice operations, `dispatch`). Existing retrospective bookkeeping guards release automatically when a process dies. This is structural evidence, not a reproduced failure of a shipped updater; existing-book updating is not yet implemented.

**Impact**: An interrupted updater could leave mixed framework files usable by an older launcher, and a previously loaded legacy process could continue retrospective mutations after updater locks release. A new journal check in future code does not retrofit that check into already-loaded old code.

**Planning response**: Require a quiescent legacy book before bootstrap; retain an updater-owned persistent writer fence and install a standalone launcher maintenance gate before changing package modules. Bridge the existing retrospective locks during live application and preserve authorization/run/notice bytes. Future runtimes must check durable maintenance state before mutation, including before retrospective failure journaling. Recover through the external updater, not partially replaced book modules.

The supported lifecycle is now explicit in FR-009, Story 4.7 and SC-005: other book clients stay closed through update/external recovery and then restart through the guarded launcher. Confirmation does not prove process exclusion. Separately, a directory created before durable ownership metadata is published is `ownership_unproven`; its prepared journal cannot authorize takeover. Preserve that lock and block automatic recovery with installed files unchanged (Story 3.8, FR-011, SC-004).

**Revisit/acceptance**:

- Exercise actual 0.1.0 and 0.2.0 subprocesses during live apply and after hard interruption; distinguish fresh launcher processes from already-loaded legacy clients.
- Verify fresh launches pause, story saves remain blocked, and recovery continues the exact selected release without duplicate commits or lost work.
- Interrupt lock acquisition before ownership-file publication and before its durability acknowledgement. Verify the unproven-ownership blocker preserves the directory/journal, changes no launcher/framework/index/ref and never auto-removes the lock; verify matching durable ownership permits the later exact-operation recovery cases.
- Exercise 0.2.0 enable/disable, notices, unfinished contributions and failure journaling without unauthorized external access or state changes.
- Do not claim crash-safe exclusion of arbitrary already-loaded legacy clients. If the quiescent-bootstrap requirement cannot be established for supported use, stop delivery and resolve the compatibility design before claiming the spec is satisfied.

This follow-up does not authorize product fixes, publication, changes to a real book, or changes to existing retrospective grants.

## T004 investigation evidence - 2026-11-03

- `tests/integration/test_update_legacy.py` runs pinned modules from exact public 0.1.0 and 0.2.0 wheels. Source wheel SHA-256 identities are checked before each disposable book is initialized.
- Both historical versions refuse a new story save while the persistent writer-lock directory exists; confirmed history, file bytes and semantic index remain unchanged.
- Fresh processes running the test-only standalone launcher gate refuse with code 6 before importing product modules; only the launcher bytes change in the synthetic book.
- Actual 0.2.0 state-lock contention blocks a notice-language mutation. Killing the lock-holder process releases its OS guard; an already-loaded legacy client can then change the notice despite the writer-lock directory. This reproduces the excluded preloaded-client case and confirms why closed sessions are required, rather than suggesting a new marker fixes old in-memory code.
- A hard-stopped child after directory creation leaves an empty writer lock with no ownership claim and unchanged installed bytes/index/HEAD. The legacy save still refuses. The new updater's `ownership_unproven` status/retry behavior remains for T025/T026; this probe does not claim it is implemented.
- Final command: `.venv/Scripts/python.exe -X utf8 -m unittest tests.contract.test_update_fixtures tests.integration.test_update_legacy -v`; 7 tests passed on Windows. Linux and native Codex results are not claimed.
- Initial sandbox attempts failed at temporary filesystem/hard-link boundaries. A fixture-method placement error was corrected and the final complete seven-test run passed with the filesystem access required for disposable historical repositories.

**Gate decision**: Proceed with the bounded design in FR-009/SC-005. Keep FUP-001 open for T029/T031 and final qualification against actual updater interruption, authorization, notice and launcher behavior. No real book, machine grant or GitHub operation was involved.

## Actual updater qualification checkpoint - 2026-11-03

- The implemented updater passed real hard-process termination and exact-candidate
  recovery across 12 durable transition checkpoints, live-owner refusal and both
  pre-confirmation ownership windows. Unconfirmed directories and journals were
  retained with unchanged installed bytes/index/HEAD and no automatic takeover.
- A separate subprocess matrix recovered after every changed resource action in
  that target fixture (13 paths), and another hard-stop case recovered an obsolete
  resource deletion, including index removal. The matrix will be rerun when the
  final packaged resource inventory changes; these counts describe this checkpoint.
- Actual public 0.1.0/0.2.0 modules attempted saves after an updater hard stop and
  received code 6. Fresh guarded launchers paused. External recovery reused the
  exact candidate; guarded restart and a sealed synthetic subsequent save passed
  for English/Icelandic source books with isolated product origins.
- Grant/notice preservation passed for absent, disabled, revoked and mismatched
  states; the enabled case initially found a Windows slash-normalization bug in
  the common-directory comparison, which was corrected and passed a focused
  rerun. No contributor service or real GitHub operation was used. Unfinished
  runs, reserved notices, unknown schemas, uncertain publication and retained
  terminal ownership are tested as blockers.
- Fixture-only failures were corrected separately: read-only Git-object cleanup
  during resource-matrix restoration, and an unsealed synthetic conversation.
  Neither is evidence of lost book data or a waived updater requirement.

**Follow-up remains documented**: the supported closed-client lifecycle is now
exercised against actual updater interruptions. This does not solve or qualify
arbitrary already-loaded legacy clients after OS guards release. Keep that
limitation and the requirement to retain external recovery tooling visible.
Cross-platform and native-host qualification are recorded in the feature ledger;
these Windows CLI results do not close native Codex acceptance.

## Final Linux delivery evidence - 2026-11-03

The frozen delivery suite passed 366 tests with three Windows-junction skips on
Ubuntu/WSL Python 3.13.13. The final resource matrix recovered after all 20 changed
resource actions, and all 12 durable transition checkpoints recovered the exact
candidate. Actual legacy-origin guarded restart/save, ambiguous-ownership refusal
and grant/notice preservation also passed in that suite. Both distribution and
historical-update verifiers passed against the final hash-bound artifacts recorded
in `tests/evaluations/existing-book-update-qualification.md`.

This adds Linux command evidence for the supported lifecycle. It does not qualify
an already-loaded legacy runtime after OS guards release, or replace native Codex
acceptance. FUP-001 remains open for that compatibility limitation.

## Final Windows delivery evidence - 2026-11-04

The same frozen inputs passed the full Windows suite: 366 tests, two explicit
real-symlink privilege skips, exit 0. All 20 changed-resource checkpoints and 12
durable transition checkpoints passed, as did obsolete-resource deletion, actual
legacy guarded restart/save, ownership refusal and grant/notice preservation.
Final distribution and historical-update verifiers also passed on Windows. The
qualification ledger records the exact artifact hashes and cross-platform results.
The supported closed-client lifecycle is qualified at the command level; native
Codex acceptance and arbitrary already-loaded legacy clients remain unqualified.

## FUP-002: completed status after ordinary writer progress

**Observed and closed 2026-11-04 after corrected-artifact qualification.** Independent host
verification found that an explicitly inspected completed operation returned
`checkpoint_changed`/cleanup-required after a valid subsequent conversation save.
The book remained valid and all writer data was intact; the defect was the
historical operation's status classification.

Completed, released operations now accept proven descendant commits on the
original branch, retaining every manifest/resource integrity check. Pending work
still requires exact checkpoints. Ancestry ignores replacement objects; unrelated
history and changed installed resources remain blockers. The reproduction failed
before the correction and all 11 CLI/status tests pass after it. Distribution
verification now asserts complete status and no-op application after a real saved
exchange. A historical recovery retry after later writer progress must still
refuse changed recovery evidence without mutation (FR-011); its prior overbroad
verifier expectation was corrected, without relaxing product guards. Both
corrected-source platform suites passed all 368 cases (Windows two explicit
symlink-privilege skips; Linux three Windows-junction skips). Distribution and
historical-update verifiers passed corrected artifacts on both platforms;
independent actual-host evidence reconciliation also passed.

The actual Codex host's original approved target was preserved. Its external
controller alone was upgraded and correctly reports the completed update ready
at the subsequent writer HEAD without any book/Git byte or staging change.
This correction does not close FUP-001's preloaded-legacy-client limitation.

### Windows qualification access context

Read-only diagnostics observed identical configured interpreter, dependencies,
site paths and wheel tags but `platform_machine=AMD64` with scoped access versus
an empty marker in the default sandbox. Matching the preview's scoped invocation
allowed the approved transaction; no runtime fingerprint or guard was bypassed.
Use the same access context for check/apply/recovery. The specific platform-query
mechanism was not established; do not claim WMI causation from these observations.
