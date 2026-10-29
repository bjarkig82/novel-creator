# Parallel final-guard byte reads — 2026-10-22

T149 continuation. Novice evaluations remain deferred/unverified. Read/save
targets remain 2s/1s p95. The retained source SHA-256 is
`6ec58b45314b7a99877220452367f6b89b532bed2fe3b3c842f0272a9aba1f5a`.

## Retained change and safeguards

Large Windows saves use at most four native Git content readers in the final
guard. At least 1,024 managed files are required. Small fixtures, the initial
guard that overlaps full-history reading, and non-Windows runtime policy retain
the serial content reader. There is no persistent executor or background work
after guard exit. The threshold is a conservative measured policy, not a proven
optimal cutoff across Windows machines or file sizes.

The complete original live-index snapshot and path/parent/leaf/mode checks finish
before any content worker is submitted. Contiguous partitions cover the exact
validated managed list once each, including installed resources and the manifest.
Every child uses the existing environment-sanitizing Git wrapper, relative-path
C quoting, explicit `GIT_WORK_TREE` binding and `hash-object --no-filters
--stdin-paths` without writing objects. Hashing samples every byte, including
same-size/same-timestamp changes.

Workers return output in original partition order. Every process and output
count must succeed before any OID conflict comparison. The executor joins all
workers on success or error before the writer lock can be released. Thread-start
runtime errors become structured code-5 failures; existing Git/metadata/content
errors retain their codes and checkpoint semantics. No work is published after
a failed final guard.

Full-history reading/validation, current-user authority and holds, new-bundle
validation, private candidate index, full candidate verification, fresh branch
check, separate new-input hashes, conditional ref publication, receipts, fsync
and index cleanup/recovery remain in place. Parallel content reads change
sampling order within the already non-atomic content phase. They do not make an
atomic filesystem snapshot or move content reads before the metadata phase.
No machine Git selector, packing, schema/dependency change or safeguard waiver
is introduced. Linux retains its serial policy; its historical performance
reference is preserved as historical evidence.

## Measured policy

The [candidate-stage investigation](windows-history-hash-candidates-20261022.md)
preserves its exact source, scripts, all raw samples and failure checks. Its
four-save-per-variant packed native-Windows/Git-Bash diagnostic measured medians
3.245158150s serial, 3.005366000s with two hash processes and 2.469268600s with
four. That is a small diagnostic, not a p95 or a default-layout result.

Additional fully validated smaller fixtures compare complete guards with serial
and four-process hashing, four balanced samples per configuration:

| Exchanges | Serial guard median (s) | Four-process guard median (s) |
| --- | ---: | ---: |
| 64 | 0.079599300 | 0.123323150 |
| 256 | 0.093100550 | 0.107311900 |
| 1,024 | 0.210275100 | 0.173006550 |

Small guards get slower with extra processes. The first measured larger point
and full-scale diagnostic motivate keeping the parallel policy above the
1,024-file threshold. These are guard-only medians with variable individual
samples, not a universal crossover estimate. Each fixture's byte size and exact
sample list are in [the raw threshold results](windows-parallel-hash-threshold-20261022.txt).

## Production regressions and review

Four new test methods cover SHA-1/SHA-256 exact path coverage and root binding,
all metadata before hashing, serial fallback on small fixtures, incomplete
output/Git failure/OS process-launch failure/thread-start failure, conflict-error
precedence, complete worker cleanup, unchanged HEAD/user index, pending receipts,
same-stat tampering with a decoy worktree, and successful unchanged-payload retry
after restoration. The existing ancestor-worktree/index-prefix decoy regression
now also forces the parallel policy. Tests force the threshold and worker policy
in small disposable repositories; they do not pretend to be scale measurements.

[Initial missing-behavior red run](windows-parallel-hash-production-red-20261022.txt)
fails four tests with 11 missing-feature errors. The
[resource/error-path red run](windows-parallel-hash-production-resource-red-20261022.txt)
exposes the thread-start RuntimeError and a test trace-count assumption. The
implementation now maps the resource error after executor cleanup; the trace
uses the explicit prepublication phase rather than assuming preparation runs on
the main thread. The [final focused run](windows-parallel-hash-production-final-focused-20261022.txt)
passes all five selected regressions in 54.214s, exit 0.

Independent read-only review against frozen `47c6...` source, then a follow-up
review of the worker-resource mapping and strengthened tests, found no actionable
findings. Reviews did not run tests or establish performance, atomic snapshots,
human outcomes or release approval.

## Final-source verification and default-layout benchmark

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

The complete fixture contains 26,215,716 UTF-8 JSON bytes.
Hardware remains the recorded eight-logical-CPU Core Ultra 7 268V Windows 11
build 26300 host, Python 3.13.13, Git 2.53.0.windows.3 and NTFS. The actual
Git executable is `C:\Program Files\Git\cmd\git.EXE`. Each operation
runs in a fresh subprocess. Save timers include full committed-history reads,
validation, both guards, candidate construction/publication and cleanup; payload
preparation and interpreter startup are excluded. Cold means first fixture read,
not a controlled OS page-cache flush. Optional trust keys remain explicitly
outside the disposable novel. No model/provider call or real novel is used.

[Windows full suite](windows-parallel-hash-full-tests-20261022.txt),
[Linux full suite](linux-parallel-hash-full-tests-20261022.txt),
[all 30 read/save samples](windows-parallel-hash-default-30-20261022.json),
[measurement progress](windows-parallel-hash-default-progress-20261022.txt),
[Windows verification manifest](windows-parallel-hash-verification-20261022.json),
[Linux verification manifest](linux-parallel-hash-verification-20261022.json),
[retained source](windows-parallel-hash-retained-source-20261022.txt).
P95 was independently recomputed using nearest rank 29 of 30, with no samples
excluded. Independent prior series do not establish the source's causal gain.
T149 and release verification remain incomplete; novice evaluations remain
explicitly deferred/unverified, with other missing host/human/language evidence
neither invented nor waived.

The first full Windows runner omitted the documented `PYTHONUTF8=1` setting.
Its 133-test run ended with one installation-test error and two explicit
symlink skips in 461.316s. The subprocess reader failed decoding Windows-code-
page `Þóra` output as UTF-8; the same isolated test reproduced the failure.
With the documented UTF-8 environment restored, that isolated test passes in
15.546s. No runtime/test source is changed for this correction. The initial
[full log](windows-parallel-hash-full-tests-nonutf8-20261022.txt),
[verification manifest](windows-parallel-hash-verification-nonutf8-20261022.json),
[isolated reproduction](windows-parallel-hash-installation-recheck-20261022.txt)
and [UTF-8 recheck](windows-parallel-hash-installation-utf8-recheck-20261022.txt)
are preserved. That failed full run did not start a benchmark. A complete rerun
with the corrected environment is required; the isolated recheck does not
replace it or establish broader default-code-page support.


## Matched retained-source comparison

Four complete saves per variant on one ordinary-layout Windows/PowerShell fixture
use balanced ABBA/ABBA order, with payload-preparation history retained for both.
The frozen pre-parallel 47c6 source measures median 6.313554450s;
retained 6ec5 source measures 5.400350250s, about 14.5% lower.
All eight saves succeed without cleanup at sequences 5001–5008. Each baseline
save makes 22 Git invocations and each retained save makes 25: four versus seven
hash invocations, respectively. Both retain two cat-file invocations and every
original guard. These are invocation counts, not counts of OS launcher children.

This small matched diagnostic supports retaining the optimization. It is not
p95 compliance or an exact universal effect estimate. The independent full-run
p95 changed from 3.612526000s on the earlier source/run to 6.566394800s here;
those different runs do not isolate the source effect. No cause for that
cross-run difference is established. The default-layout measurements remain
unmet and are not replaced by the lower matched median or packed-fixture data.

The first full-history cat-file invocation has median 2.116440050s
before and 1.994884450s after in these traces. Its wall time includes
Git startup, object reading and capture, not disk-only or JSON-validation time.
This identifies a substantial remaining full-history read cost for the next
isolated experiment. No history content read or validation has been skipped.

[All source-matched samples and command traces](windows-parallel-hash-retained-comparison-20261022.txt),
[executed source](windows-parallel-hash-retained-comparison-source-20261022.txt),
[threshold experiment source](windows-parallel-hash-threshold-source-20261022.txt),
[Windows verification runner](windows-parallel-hash-verification-source-20261022.txt),
[Linux verification runner](linux-parallel-hash-verification-source-20261022.txt).

The threshold samples used native Windows Git Bash, while the retained comparison
and full benchmark use PowerShell's recorded cmd/git.EXE launcher. The small
threshold diagnostic does not establish the precise crossover for every Git
launcher, hardware configuration or file size. Current full-scale performance
remains a release blocker. All reported process handles are terminal.

[Evidence hashes and independently checked medians](windows-parallel-hash-evidence-manifest-20261022.json).
