# Platform verification

## Current performance continuation — 2026-10-21

Ubuntu 24.04.4 under WSL2, Python 3.12.3, Git 2.43.0, disposable fixtures on
ext4: **112 tests in 21.138s, all passed, zero skips**. This includes installed
CLI journeys, locks/recovery, real symlinks, byte-hash guards for both Git object
formats, incremental/schema parity and authenticated-cache adversarial cases.
See [full log](linux-trusted-cache-final-tests.txt). Linux installation testing
exposed framework CRLF and fixture executable-mode defects; both were corrected
and verified. Original user source bytes remain preserved.

Full Spec Kit Bash smoke passes under Ubuntu and Windows Git Bash with jq
1.8.2; release binaries were SHA-256 verified. Windows JSON constructor calls
disable MSYS argument conversion to preserve paths. See [Linux smoke](linux-trusted-cache-bash-smoke.txt)
and [Windows smoke](bash-smoke-performance-pass.txt).

The reference Linux performance targets pass with the explicitly configured
external trusted-key cache. Windows cached reads pass, while its 6.771s save
p95 remains above target. See [measured configurations](performance.md).
macOS, physical power-loss guarantees, actual creative/bilingual host cases and
five-person novice observations remain unverified. WSL structural tests do not
extend the separately recorded Windows Desktop capture gate. Earlier sections
below retain historical results and do not supersede this current scope.

## Revised native-message input — 2026-10-21

The full Windows suite after the T116 adapter/helper change ran 55 tests in
121.279s: 54 passed and one explicit symlink-privilege skip, zero failures/errors.
See [input-boundary evidence and limitations](native-message-input.md) and
[the full test log](windows-native-message-tests.txt). No new platform, actual
host or complete gate support is inferred from that structural result.

## Windows foundation remediation — 2026-10-21

Scope: T102/T111 foundation only. Full feature/release, native-host capture,
bilingual semantics and physical crash durability remain unverified. Linux and
macOS have not been rerun for this change; no new platform support claim is made.

Production change: storage.sync_index now opens its index-lock descriptor with
write access before fsync. A new real-Git regression failed before the fix for
both existing and unborn repositories because cleanup_required was true.
Afterward, the focused clean-save/continuation/identical-retry regression passed.
The sandbox initially denied os.link (WinError 5); the meaningful red/green runs
used normal filesystem access and new disposable repositories outside the
framework. No retained host-test repository was repaired, reset or deleted.

The installed-fixture assertion subsequently exposed universal-newline
normalization in its expected text. Production correctly retained CRLF. The test
now compares decoded UTF-8 bytes, and explicitly requires clean bootstrap and
conversation saves. This is a test portability correction, not a transcript
format change.

Test helpers resolve temp roots to canonical paths. Real symlink creation denied
with Windows error 1314 is explicitly skipped, leaving real-symlink rejection
unverified on this machine; traversal/payload rejection remains exercised.

Environment observed in this session: Windows 11 build 10.0.26300, NTFS on C:,
Python 3.13.13 from the checkout's .venv, Git 2.53.0.windows.3 and jsonschema
4.26.0. TEMP/TMP pointed to the writable task visualization directory on C:,
outside all Git repositories. PYTHONUTF8=1 and PYTHONDONTWRITEBYTECODE=1 were set
for child processes. Git identities were repository-local and disposable.

Commands:

```powershell
.\.venv\Scripts\python.exe -B -m unittest tests.integration.test_storage.StorageTests.test_clean_save_continuation_and_retry_leave_managed_index_synchronized -v
.\.venv\Scripts\python.exe -B -m unittest discover -v
git diff --check
```

The initial full-suite run loaded the old installed-fixture assertion before
its correction: 54 tests, one CRLF expectation failure and one privilege skip
in 213.950s. All storage/checkpoint cases passed, including the previously failing
unreadable-successor checkpoint cases. Its [log](windows-foundation-initial-tests.txt)
is retained separately. The [final log](windows-foundation-tests.txt) is the
subsequent run against the corrected test source.

All checked-in .specify/scripts/bash/*.sh passed bash -n under Git Bash with
normal filesystem access. The sandbox prevented MSYS startup; that is excluded
as product evidence. Full tests/speckit-smoke.sh was not run because jq is
unavailable in that Bash environment. Git diff whitespace checks passed.

Final full-suite result: **54 tests run in 187.144s, 53 passed, one skipped,
zero failures/errors; exit 0**. The skip is only the explicit Windows real-symlink
privilege case. Clean bootstrap/continuation/retry, installed bundle, lost
receipts, checkpoint disclosure, conflict/fault windows and unrelated staged
work/manuscript preservation pass on this run. This closes T102/T111 only.

The actual Codex host gate T012/T069/T089/T103 remains **BLOCKED/unverified**.
No genuine host conversations, observed display timing, fresh-chat recovery or
display interruption were exercised by these subprocess tests. Dependent story
tasks and full platform/release verification T064/T110 remain open. A new
human-driven fixture experiment is next; the retained failed fixture is unchanged.


## Latest Windows verification — native evidence path

Final full suite after the local/evidence native-source regression: **55 tests
in 216.277s, 54 passed, one explicit Windows symlink-privilege skip, zero failures
or errors; exit 0**. Same canonical external temp directory, Python UTF-8 and
normal filesystem access as above. [Full log](windows-native-evidence-path-tests.txt).
No additional physical durability, platform or semantic language claim is made.

The separate actual Desktop gate now passes in its tested native-tool/text-input/
scoped-approval scope: [actual host report](host-capture-runs/20261021T171237Z-spike-03/README.md).
Earlier BLOCKED statements above describe historical assessments. Story delivery
and full platform/release readiness remain incomplete.


## Story implementation regression — latest run

90 tests in 304.636s: **89 passed, one explicit Windows symlink-privilege skip,
zero failures/errors; exit 0**. [Final log](windows-story-final-tests.txt).
Command: python -B -m unittest discover -v, using the same canonical external
TEMP/TMP root, Python UTF-8, disabled bytecode and normal filesystem access.
This includes initialized/installed journeys, focused sessions, unchanged recovery,
five canon revisions, manuscript protection, damaged/restored history, language
resource selection, independent consumer and isolated installed-module paths.

Intermediate logs are retained: windows-story-foundation-tests.txt contains a
known test-fixture argument collision; windows-story-core-tests.txt passed 87
tests with one skip before the final language/portability additions. A setuptools
wheel build and resource inspection also succeeded. Actual product-host/human,
semantic bilingual, performance and untested platform/durability gates remain
open; see release-readiness.md. No new remote/provider/release claim is made.

## Final Windows performance regression suite — 2026-10-21

112 tests in 268.801s: **111 passed, one real-symlink privilege skip, zero
failures/errors; exit 0**. [Full log](windows-performance-final-tests.txt).
Python 3.13.13, Git 2.53.0.windows.3, Windows 11 build 10.0.26300; UTF-8 and
bytecode-disabled execution with canonical external temporary repositories and
normal filesystem access for hard-link publication. This does not establish
physical power-loss durability or the untested host/human/macOS gates.

## Platform scope decision — 2026-10-21

The user deferred macOS support for now. macOS is outside the current release
scope and is not a release blocker; no macOS support or verification is claimed.
This supersedes earlier macOS gate references in this document. Linux and Windows
remain in scope. Actual host/bilingual evaluations, five novice observations,
Windows save performance and the remaining release checks are still required.
