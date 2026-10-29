# Platform verification

**Current policy (owner, 2026-10-28):** no latency acceptance targets apply.
Optimization is deferred; prior timing outcomes remain historical evidence.
Current functional/install checks and supported-platform limits are consolidated
in [final functional qualification](final-functional-qualification-20261028.md).
All platform skips, native/delegated input distinctions and durability limits
remain explicit. Earlier claims that timing misses block delivery are superseded.

The [explicit delegated-input extension](delegated-input-support-20261023.md)
adds a separately labeled evaluation route while retaining native/human gates.
Its source-specific regressions, final wheel checks and observed delegated gates
supersede earlier runtime verification for the changed CLI/validation sources.
Final full suites run 165 tests each: Windows 163 pass with two explicit
real-symlink privilege skips; Linux 162 pass with three Windows-only skips.
The same offline wheel verifies all 26 source/resource files on both platforms.

The [Git blob identity repair](git-blob-integrity-20261023.md) supersedes earlier
storage-source verification. Final suites pass 158 tests on each platform,
with two Windows symlink-privilege skips and three Linux Windows-only skips.
Both independent wheel checks pass and compare all 25 source/resource files.
The source-pinned manifest distinguishes final from intermediate evidence.

The [2026-10-23 delegated-input probes](product-host-runs/20261023T095949Z/README.md)
find native capture unavailable for both task creation and follow-up API inputs.
The direct typed-user scope remains distinct. Clarified instructions pass 14
focused installation/resource tests on each platform and independent wheel
verification on Windows and Linux. No creative, novice or fresh-resumption case
ran through the unsupported task-to-task route.

The [2026-10-23 performance continuation](windows-performance-continuation-20261023.md)
records historical-source packed/direct-Git Windows results: all 30 reads and saves
succeed; read p95 passes and save p95 remains unmet. No runtime change is retained
for that performance investigation. Later storage changes have separate evidence.

The [2026-10-23 junction boundary correction](windows-junction-boundary-20261023.md)
rejects Windows directory junctions and other reparse points in managed paths
and Git metadata. Its source-specific results supersede earlier regression
evidence for the changed storage checks; earlier performance measurements remain
historical and the release gates remain open.

The [independent distribution/UTF-8 verification](independent-release-verification-20261022.md)
records the latest CLI fix, cross-platform wheel checks, full regression results
and Bash smoke checks. The built wheel uses each platform's existing dependency
environment; this adds no host, semantic, physical-durability or macOS claim.

Latest four Windows save-history readers verification — 2026-10-22

Windows: 150 tests in 439.660s, 148 passed,
2 explicit real-symlink privilege skips, exit 0.
Linux/WSL: all 150 tests pass in 50.762s, zero skips,
exit 0. Six source/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Ordinary Windows PowerShell fixture: first read 1.984177600s; read p95
1.183358100s (PASS, target 2s); validation/local-save p95
2.856806500s (UNMET, target 1s). All 30 reads and 30 saves succeed without operation
errors or timeouts. Benchmark exit 1 records unmet performance thresholds.
No explicit Git packing or maintenance was requested. Linux performance was
not remeasured for this source; previous Linux timings remain historical.

[Source-specific evidence](windows-four-history-readers-20261022.md). T149 remains open; novice evaluations remain deferred/unverified.

Following evidence records earlier source-specific checkpoints.

Latest native bundle metadata verification — 2026-10-22

Windows: 150 tests in 453.334s, 148 passed,
2 explicit real-symlink privilege skips, exit 0.
Linux/WSL: all 150 tests pass in 48.573s, zero skips,
exit 0. Six source/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Ordinary Windows PowerShell fixture: first read 1.998505000s; read p95
1.320975200s (PASS, target 2s); validation/local-save p95
3.292486500s (UNMET, target 1s). All 30 reads and 30 saves succeed without operation
errors or timeouts. Benchmark exit 1 records unmet performance thresholds.
No explicit Git packing or maintenance was requested. Linux performance was
not remeasured for this source; previous Linux timings remain historical.

[Source-specific evidence](windows-native-bundle-mode-production-20261022.md). T149 remains open; novice evaluations remain deferred/unverified.

Following evidence records earlier source-specific checkpoints.

## Balanced Windows save readers — 2026-10-22

Windows full suite: 143 tests in 567.082s, 141 passed,
2 explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 143
pass in 58.745s, zero skips, exit 0. The same five source/test/harness/
helper fingerprints match before and after both suites and the benchmark.

Ordinary-layout Windows PowerShell with the optional authenticated cache:
first read 2.288559600s; read p95 2.289081100s; validation/local-save p95
9.240644400s. All 30 reads and 30 saves succeed without operation errors or timeouts.
Read misses the unchanged 2s target; save misses the unchanged 1s target.
Benchmark exit 1 records that unmet threshold. No explicit packing/maintenance
is requested. Linux performance has not been remeasured for this source;
its earlier reference results remain historical evidence.

Large Windows saves use two history readers and two first-guard full-byte
readers while the original operations overlap. The final full-byte guard and
public history reads retain up to four readers. Each existing 1,024-item
threshold independently keeps small inputs serial; non-Windows defaults remain
one. All metadata/index/path/symlink/mode checks precede each guard's hashing.
All actual blob/digest/schema/authority/hold checks, both complete root-bound
byte guards, private candidate verification, original first-guard error/await
position, worker/lock lifetime, fresh branch/CAS, receipts and recovery remain.
History outputs keep ordered single-stream framing and one full serial fallback
on worker/submission/nonzero exit failure. No check is skipped or moved.

[Current source evidence](windows-balanced-save-20261022.md). T149 remains open; novice evaluations remain deferred/unverified.

Following sections are source-specific historical checkpoints.


## Partitioned public Windows history reads — 2026-10-22

Windows: 138 tests in 704.102s, 136 passed and two explicit real-symlink
privilege skips, exit 0. Linux/WSL2: all 138 pass in 229.403s, zero skips,
exit 0. All five runtime/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 2.486383800s; read p95 1.787683800s; validation/local-save p95
9.219870400s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read passes its 2s target; save misses its 1s target. Exit 1
records the unmet save threshold. No explicit Git packing/maintenance is requested.
Linux performance has not been remeasured for this source; earlier reference
results remain historical evidence.

Large public Windows reads (>=1,024 exchanges) fetch captured immutable blob
OIDs in at most four contiguous requests using the existing Git wrapper. Every
worker joins before parsing or returning. Successful outputs form one original-order
binary stream. Any worker/submission exception or nonzero child exit triggers one
full original serial request before parsing, preserving partial stdout, earlier
damaged-history errors and verified-prefix checkpoints. Small public reads and
non-Windows runtime stay serial. Save history remains serial: measured parallel
save variants provided no gain. All history/blob/schema/digest/authority/hold,
path/symlink/mode/live-index, both complete root-bound byte guards, private
candidate, fresh branch/CAS, receipt and recovery safeguards remain. The
previous parallel final-byte guard is unchanged.

[Current evidence](windows-history-read-20261022.md). T149 remains open; novice evaluations remain deferred/unverified.

Following sections preserve source-specific historical checkpoints.

## Parallel final-guard hashing — 2026-10-22

Final-source Windows suite: 133 tests in 571.309s, 131 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 133 pass in
75.471s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 5.184642400s; read p95 5.110137800s; validation/local-save p95
6.566394800s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records threshold status. No explicit Git packing/maintenance is requested.
This is the default fixture layout; earlier packed/native-Git results describe
their own source and configuration. Linux performance has not been remeasured
for this source; historical Linux/earlier Windows data is retained.

Large Windows final guards use at most four root-bound complete-byte readers
after every metadata/index check, joining every worker before publication or
error cleanup. Small saves, first guards and non-Windows runtime remain serial.
All candidate/CAS and recovery safeguards remain. See the
[source-specific report](windows-parallel-hash-20261022.md). T149 remains open;
novice evaluations remain deferred/unverified.

## Combined branch/OID query — 2026-10-22

Final-source Windows suite: 129 tests in 457.064s, 127 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 129 pass in
85.357s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 4.237690400s; read p95 5.106631200s; validation/local-save p95
3.612526000s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records unmet thresholds. No explicit Git packing/maintenance is requested.
This is the default fixture layout; prior packed/native-Git results describe
their own source and configuration, not this source. Linux performance has not
been remeasured for this source; historical Linux/earlier Windows data is kept.

The ordinary path uses 22 Git processes instead of 24. Both full-byte guards,
fresh live-index/path/root checks, private candidate/CAS and recovery remain.
New same-OID branch-switch tests reject before publication and return saved with
cleanup after publication, preserving the user index. One query is not an atomic
reference snapshot. T149/release remain incomplete; novice evaluations are
deferred/unverified. See the [source-specific report](windows-ref-query-20261022.md).

## Canonical path allocations — 2026-10-22

Final retained-source tests: Windows 126 tests in 373.021s, 124 passed and
two explicit Windows symlink-privilege skips, exit 0; Linux all 126 pass in
82.276s, zero skips, exit 0. The Windows and Linux manifests record the source
fingerprints; Windows before/after hashes match across tests and measurements.

Final-source Windows Git Bash, explicitly packed disposable fixture: first read
3.200534500s, read p95 1.587495700s, validation/local-save p95 3.645534700s.
All 30 reads and 30 saves succeed without timeouts or operation errors. Read
passes its 2s target; save misses its 1s target. Exit 1 records the unmet threshold.
Packing takes 5.748657100s outside operation timers and is fixture preparation,
not product behavior. This configuration does not establish ordinary-layout
performance. Linux performance has not been rerun for this path-allocation source;
previous overlap-source measurements remain historical and source-pinned.

Full history, both fresh guards, index/root/content checks, candidate verification,
CAS and recovery remain intact. Novice evaluations remain deferred/unverified.
T149 and release remain incomplete. See the
[latest source-specific report](windows-allocation-investigation-20261022.md).

## First-guard overlap — 2026-10-22

Frozen Windows suite: 125 tests in 318.673s, 123 passed/two explicit real-symlink
privilege skips, zero failures/errors, exit 0. Linux/WSL2: all 125 pass in
36.951s with zero skips, including coordinated validation-time edits and competing
history/guard failures. Both full guard passes and publication/recovery checks
remain. The first guard may finish earlier; an edit during validation can leave
truthful pending work before the second guard rejects it. No changed bytes are
published. See [current safety and verification report](windows-guard-overlap-20261022.md).

All complete-fixture configurations finish 30 reads/saves without operation
errors/timeouts. Windows read/save p95: ordinary PowerShell 2.014926100s/
2.733241800s (both unmet), packed PowerShell 1.045105700s/2.209314500s (read
passes), packed native Windows Git Bash 0.942910200s/1.719383700s (read passes).
Packing is separately timed; no PATH or product selector change is retained.
The Git Bash benchmark does not establish another full installation/host gate.

Current Linux reference uses identical runtime/schema bytes on ext4 and records
read/save p95 1.153318426s/1.072006791s: read passes, save misses. The older
Linux reference pass remains historical. A paired Linux median improvement does
not replace that current p95 miss. Frozen input/source manifests match after
all verification and measurements. T149 remains unchecked; no current-source
configuration passes both targets. Novice evaluations remain deferred/unverified;
semantic host, macOS and physical power-loss claims are not inferred from tests.
Earlier sections below retain their historical source/configuration scope.

## Save snapshot reuse — 2026-10-22

The frozen Windows suite passes 123 tests in 405.898s: 121 passed, two explicit
real-symlink privilege skips, no failures/errors, exit 0. Linux/WSL2 passes all
123 in 68.212s with zero skips. Both Git object formats, bootstrap/retry,
root/index/same-stat tampering, immutable snapshots and recovery remain covered.
[Windows](windows-snapshot-reuse-full-tests-20261022.txt),
[Linux](linux-snapshot-reuse-full-tests-20261022.txt).

Save now reuses its exact immutable tree metadata between full history reading
and the first guard; every blob and both live byte/index guards remain checked.
The ordinary-layout opt-in-cache benchmark completes 30 reads/saves without
operation errors/timeouts, but read p95 3.545458500s and save p95 6.626094600s
both miss their unchanged targets. The final matched trace removes exactly one
duplicate tree query; timing variability prevents attributing whole-run
differences solely to that query. T149 remains unchecked. See
[current source and configuration evidence](windows-snapshot-reuse-20261022.md).
The packed configuration completes 30 reads/saves without operation failures,
with read p95 2.277303600s and save p95 4.562267800s, also both unmet. Packing
time 6.001285800s is excluded and separately recorded; no actual novel is packed.
Frozen source/test/benchmark inputs match after all verification/measurements.
Earlier sections below remain historical. No Linux timing, human/novice,
semantic host, macOS or physical durability result is inferred from these tests.

## Full-history and file-check continuation — 2026-10-22

Final Windows suite: 122 tests in 326.671s, 120 passed, two explicit real-symlink
privilege skips, no failures/errors, exit 0. Linux/WSL2: 122 passed in 60.080s,
zero skips; both final focused guard fixtures also pass after the deterministic
index-fixture correction. The retained relative-path guard explicitly binds
Git's worktree root and preserves complete path, byte and live-index checks.

The ordinary-layout, opt-in-cache Windows benchmark completes 30 reads and saves
without operation errors/timeouts. Read p95 1.715363500s meets its 2s target;
save p95 3.398351400s misses 1s. T149 remains open. See
[current report, logs and separate packing measurements](windows-history-guard-optimization-20261022.md).
The explicitly packed disposable fixture records read/save p95 1.020150600s/
2.739170400s, with 4.742777600s maintenance separately excluded; it also misses
the save target and does not establish default-layout performance.
No new Linux performance, macOS, actual-host, novice or durability claim is made.
Novice observations remain deferred/unverified; earlier sections are historical.

## Windows candidate verification — 2026-10-22

The full Windows suite runs 120 tests: 118 passed, two explicit real-symlink
privilege skips, zero failures/errors, exit 0 (377.170s).
[Windows log](windows-candidate-full-tests-20261022.txt). Linux/WSL2 runs all 120
successfully with zero skips, exit 0 (56.558s), including both symlink cases.
[Linux log](linux-candidate-full-tests-20261022.txt). These verify the batched
candidate tree/parent/content checks and retained transaction/recovery safeguards.

The fresh Windows 30-run benchmark completes without operation errors/timeouts,
but read p95 3.252935300s and save p95 5.907091200s both miss their unchanged
targets. Candidate verification is faster in isolation; whole-save improvement
is not established. See [current evidence](windows-candidate-optimization-20261022.md).
Earlier Linux performance and scoped native-host capture evidence remain
historical reference results. No new Linux timing, host, macOS or durability
claim is made. Novice observations are deferred and remain unverified.

## Current performance continuation — 2026-10-21

Ubuntu 24.04.4 under WSL2, Python 3.12.3, Git 2.43.0, disposable fixtures on
ext4: **118 tests in 51.548s, all passed, zero skips**. This includes installed
CLI journeys, locks/recovery, real symlinks, byte-hash guards for both Git object
formats, incremental/schema parity and authenticated-cache adversarial cases.
See [full log](linux-save-optimization-full-tests.txt). Linux installation testing
exposed framework CRLF and fixture executable-mode defects; both were corrected
and verified. Original user source bytes remain preserved.

Full Spec Kit Bash smoke passes under Ubuntu and Windows Git Bash with jq
1.8.2; release binaries were SHA-256 verified. Windows JSON constructor calls
disable MSYS argument conversion to preserve paths. See [Linux smoke](linux-trusted-cache-bash-smoke.txt)
and [Windows smoke](bash-smoke-performance-pass.txt).

The reference Linux performance targets pass with the explicitly configured
external trusted-key cache. Windows cached reads pass, while its latest 3.846s save
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

## Phase 22 source-bound platform evidence — 2026-10-28

Current actual evaluation uses Codex desktop on Windows 11 build 26300 and NTFS, with Python 3.13.13/Git 2.53.0.windows.3; inputs are explicitly delegated evaluation-only and model/app version is unavailable. Nine updated collector methods pass on Windows and Linux/WSL2 (Python 3.12.3, Git 2.43.0, jsonschema 4.26.0/jsonschema-rs 0.59.0). Earlier 22 affected installed checks and independent wheel verification on both platforms remain source-identical evidence; they are not newly rerun full suites. Prior Windows real-symlink privilege skips stay explicit, Linux real-symlink evidence stays separate, and normal scoped filesystem access remains needed for sandbox-denied Windows hard links/Git. Current ordinary-layout full-scale reads pass but saves miss 1s, so broader qualification is open. Physical power-loss durability, untested host/filesystem combinations and deferred macOS are not claimed. Novice/manual prerequisites are excluded by the current owner scope. See phase22-release-assessment-20261028.md.


### Source identity after T172 component/prototype diagnostics — 2026-10-28

The deeper tree probes and unretained lexical-prefix comparison edit no runtime,
resource, dependency or benchmark file. Existing Windows/Linux installed-wheel
identity and source-specific tests remain their original evidence; they are not
newly rerun suites. New diagnostics use Windows/NTFS with scoped normal access,
no packing or global setting changes. Their variable instrumented timings and
sampled CPU saturation do not replace the ordinary-layout qualification p95 or
establish another supported host/filesystem. Prior explicit skips and physical
durability limits remain. T172/T173 stay open; see
windows-phase22-tree-components-20261028.md and
windows-phase22-parent-prefix-20261028.md.


### Isolated native Git build scope — 2026-10-28

The diagnostic MSVC/zlib1.3.1 build pins the same Git release source commit and
passes scoped SHA-1/SHA-256 tree/missing-object checks plus guarded Windows/NTFS
save runs. It is not binary-identical to installed Git and is not installed as a
supported backend. Native timers remain opt-in, isolated and subject to clock,
compiler and host-load limits. No installed Git/global setting/product runtime
change or new Linux/wheel qualification is claimed. Prior skips/durability limits
and open T172/T173 remain. See windows-phase22-native-profile-20261028.md.


## Current functional qualification — complete, 2026-10-28

All latency targets are withdrawn by the owner; optimization is deferred.
Windows: 176 passed, two real-symlink privilege skips. Linux: 175 passed,
three Windows-only junction skips. Both suites contain 178 tests and exit 0.
Offline wheel source/install/save/reopen verification passes on both platforms,
and Spec Kit Bash smoke passes. T172/T174 are retired requirements, not
performance passes; T173/T175 close the current functional scope. Earlier
native/human/subjective unknowns remain explicit and do not become passes.
See [the final report](final-functional-qualification-20261028.md) and
[the source/evidence manifest](final-functional-manifest-20261028.json).
