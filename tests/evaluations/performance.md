# Performance — reference results and remaining Windows limits

**Current policy, 2026-10-28:** the owner withdrew all latency targets and
requested functional delivery before further optimization. Existing measurements
remain unchanged; historical target misses are not relabeled passes. Current
read/save timings are informational. Operation errors, incomplete runs and hangs
remain failures; the worker deadline is an execution bound, not a latency goal.
See [final functional qualification](final-functional-qualification-20261028.md).

The latest retained ordinary-layout 30-read/30-save run completes without errors
or timeouts: read p95 1.028736700s and save p95 3.067419500s. The sections below
preserve earlier source-specific evidence and the targets applicable at the time.

The [single-user POC small-history run](windows-poc-small-performance-20261023.md)
completes 30 reads and saves without errors/timeouts over ten sessions, 100
exchanges, 200 assertions and 1,048,668 bytes. Read p95 0.579379300s passes;
save p95 1.983323900s still misses 1s. This is functional POC responsiveness
evidence, not replacement evidence for the full-scale limits below. Novice/manual
testing is not a POC gate under the owner's latest scope instruction.

The [current delegated-provenance source measurement](windows-delegated-provenance-performance-20261023.md)
completes all 30 reads (p95 3.453516100s; 2s target unmet). Save completes 26
attempts before attempt 27 times out at the unchanged 30s worker deadline;
save p95 is unavailable and the 1s target remains unmet. Both suites and host
tasks were idle during measurement. No worker remained after exit. Preserve
the raw timeout; do not replace it with a successful or extrapolated duration.

Historical-source [2026-10-23 packed/direct-Git measurements](windows-performance-continuation-20261023.md)
complete 30 reads and 30 saves without errors: read p95 0.824995800s passes,
save p95 1.971346700s misses the unchanged 1s target. This explicitly packed,
process-local direct-Git configuration remains separate from the ordinary
PowerShell results below. The GIL-policy diagnostic regresses ordinary layouts
and is not adopted. T157 remains open. The subsequent
[Git blob identity repair](git-blob-integrity-20261023.md) changes storage checks;
these earlier timings do not establish performance for that source.

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


Measured on 2026-10-21 and 2026-10-22 against the complete fixture: 100 sessions, 5,000
exchanges, 10,000 active assertions and at least 25 MiB of UTF-8 JSON. Exact byte counts
are retained in each raw result. Each result
contains 30 warm read and 30 validation/local-save samples; p95 uses nearest rank.
Targets are <=2 seconds for reads and <=1 second for validation/local save.

| Configuration | First read (s) | Read p95 (s) | Save p95 (s) | Both targets |
|---|---:|---:|---:|---|
| [Linux/WSL2, full validation](linux-performance-scale-30.json) | 1.692 | 1.695 | 2.011 | UNMET |
| [Linux/WSL2, opt-in authenticated cache, 2026-10-21 reference](linux-performance-trusted-cache-30.json) | 1.616 | 0.826 | 0.982 | PASS |
| [Windows, full validation](windows-performance-scale-30.json) | 2.439 | 2.683 | 8.650 | UNMET |
| [Windows, opt-in authenticated cache](windows-performance-trusted-cache-30.json) | 2.517 | 1.745 | 6.771 | UNMET |
| [Windows, cache plus guard metadata reuse](windows-performance-guard-reuse-30.json) | 3.071 | 1.597 | 3.846 | UNMET |
| [Windows, cache plus batched candidate verification, 2026-10-22](windows-performance-candidate-30-20261022.json) | 3.587 | 3.253 | 5.907 | UNMET |
| [Windows, cache plus root-bound relative file checks, ordinary fixture, 2026-10-22](windows-history-default-30-20261022.json) | 2.354 | 1.715 | 3.398 | UNMET |
| [Windows, same source/cache, explicitly packed fixture, 2026-10-22](windows-history-packed-30-20261022.json) | 1.913 | 1.020 | 2.739 | UNMET |
| [Windows, cache plus save-snapshot metadata reuse, ordinary fixture, 2026-10-22](windows-snapshot-reuse-default-30-20261022.json) | 4.720 | 3.545 | 6.626 | UNMET |
| [Windows, save-snapshot reuse/cache, explicitly packed fixture, 2026-10-22](windows-snapshot-reuse-packed-30-20261022.json) | 4.780 | 2.277 | 4.562 | UNMET |
| [Windows, first-guard overlap/cache, ordinary PowerShell fixture](windows-guard-overlap-default-30-20261022.json) | 2.672 | 2.015 | 2.733 | UNMET |
| [Windows, first-guard overlap/cache, packed PowerShell fixture](windows-guard-overlap-packed-30-20261022.json) | 1.978 | 1.045 | 2.209 | UNMET |
| [Windows, first-guard overlap/cache, packed Git Bash fixture](windows-guard-overlap-git-bash-packed-30-20261022.json) | 2.226 | 0.943 | 1.719 | UNMET |
| [Linux/WSL2, first-guard overlap/cache, ext4 runtime/fixture](linux-guard-overlap-reference-30-20261022.json) | 2.171 | 1.153 | 1.072 | UNMET |
| [Windows, path-allocation/cache, packed Git Bash fixture](windows-path-allocation-packed-30-20261022.json) | 3.201 | 1.587 | 3.646 | UNMET |
| [Windows, combined ref queries/cache, ordinary PowerShell fixture](windows-ref-query-default-30-20261022.json) | 4.238 | 5.107 | 3.613 | UNMET |
| [Windows, parallel final hashes/cache, ordinary PowerShell fixture](windows-parallel-hash-default-30-20261022.json) | 5.185 | 5.110 | 6.566 | UNMET |
| [Windows, partitioned public history/cache, ordinary PowerShell fixture](windows-history-read-default-30-20261022.json) | 2.486 | 1.788 | 9.220 | UNMET |
| [Windows, balanced save readers/cache, ordinary PowerShell fixture](windows-balanced-save-default-30-20261022.json) | 2.289 | 2.289 | 9.241 | UNMET |
| [Windows, native bundle metadata/cache, ordinary PowerShell fixture](windows-native-bundle-mode-default-30-20261022.json) | 1.999 | 1.321 | 3.292 | UNMET |
| [Windows, four save-history readers/cache, ordinary PowerShell fixture](windows-four-history-readers-default-30-20261022.json) | 1.984 | 1.183 | 2.857 | UNMET |

The **2026-10-21 Ubuntu/WSL2 reference run passed both targets**. It remains
historical evidence; the first-guard-overlap Linux source later missed save at
1.072006791s. The current four-history-reader source passes all 150 Linux tests,
but Linux performance has not been remeasured for it. No current-source
configuration has established both targets. The newest
[four-reader report](windows-four-history-readers-20261022.md) records current-source
Windows default-layout measurements, complete checks, source fingerprints and
separate diagnostic comparisons. Earlier configurations remain pinned to their
recorded sources and are not substituted for the new measurement.
Full validation
without the optional cache remains correct and has the separate timings above.
These results establish the planned reference measurement, not uniform performance
across all operating systems or macOS support.

The earlier root-bound-path ordinary-layout Windows run completes all 30 reads and saves without
operation errors/timeouts: read p95 **1.715363500s**, save p95 **3.398351400s**.
Read meets its target; save remains unmet and the benchmark correctly exits 1.
The final matched four-sample comparison shows guard median 0.762s -> 0.532s and
whole-save median 4.315s -> 3.646s. These diagnostics do not establish p95
compliance or a portable percentage gain. The earlier 3.253s/5.907s candidate
run is historical; cross-run differences do not isolate source effects.
See [current safeguards and measured configurations](windows-history-guard-optimization-20261022.md)
and [earlier candidate evidence](windows-candidate-optimization-20261022.md).

The earlier root-bound-path packed disposable fixture completes 30 reads/saves without errors
or timeouts: read p95 1.020150600s and save p95 2.739170400s, exit 1. Its
4.742777600s maintenance time is excluded and separately recorded. No automatic
packing is added to the product; this configuration does not establish ordinary-
layout performance or a packing-only save gain. The matched-layout diagnostic
shows faster reads but no save improvement. Both full-scale configurations keep
the 1s save gate unmet. Use `--pack-fixture` to reproduce this explicit benchmark
configuration; omit it for ordinary layout.

The earlier save-snapshot reuse source completes all 30 ordinary-layout reads and
saves without operation errors/timeouts: first read 4.719507600s, read p95
3.545458500s and save p95 6.626094600s, exit 1, both targets unmet. The change
removes one duplicate immutable tree query. Matched diagnostic medians are
5.859s before/4.449s after, but the omitted query itself measures about 0.071s;
the larger observed difference cannot be attributed wholly to this change.
The cause of higher fresh-process p95 versus earlier dated results is not
established; historical comparisons cannot isolate the source change. The
final-source packed run also completes 30 reads/saves without errors/timeouts:
first read 4.780076500s, read p95 2.277303600s, save p95 4.562267800s, exit 1.
Its 6.001285800s packing time is separately excluded. Both targets are unmet in
both of those configurations. See [snapshot-reuse verification and limits](windows-snapshot-reuse-20261022.md).

The first-guard overlap source completes all 30 reads/saves in each of
three Windows configurations without operation errors/timeouts. Ordinary
PowerShell read/save p95 2.014926100s/2.733241800s both miss; packed PowerShell
1.045105700s/2.209314500s passes read only; packed native Windows Git Bash
0.942910200s/1.719383700s also passes read only. Packing times 4.524228100s and
2.971372300s are separately excluded. Each result records the selected Git
executable. No machine PATH change, product selector or automatic packing is
introduced. Shell/layout results do not replace ordinary/default performance.

The earlier overlap-source Linux/ext4 reference completes all 30 reads/saves without operation
errors/timeouts: first read 2.171033683s, read p95 1.153318426s, save p95
1.072006791s, exit 1. A controlled eight-save-per-variant Linux comparison lowers
median 0.948s -> 0.789s but does not establish passing p95 or explain the tail.
Windows's final matched diagnostic lowers median 3.014s -> 2.673s. These
diagnostics do not substitute for the complete measurements. See
[overlap source, race semantics, raw samples and manifests](windows-guard-overlap-20261022.md).

The earlier controlled alternating comparison isolated a 14.36% median save
reduction from the guard metadata change; the larger difference from the older
6.771s p95 was not attributed entirely to that optimization.
See [earlier diagnosis and safeguards](windows-save-optimization.md).

## Reference hardware and environments

[Observed hardware](performance-reference-hardware.json): LENOVO 22AWS00800,
33,847,832,576 bytes physical RAM, eight logical CPUs. Windows 11 build
10.0.26300 used Python 3.13.13 and Git 2.53.0.windows.3. Ubuntu 24.04.4 LTS
under WSL2 kernel 6.6.87.2-microsoft-standard-WSL2 used Python 3.12.3,
Git 2.43.0 and ext4 for the source copy and disposable fixtures. This is WSL2
structural evidence; physical power-loss guarantees have not been measured.

## Reproduction and measurement boundary

```powershell
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/performance-local.json
# Full-validation comparison:
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --no-validation-cache --output tests/evaluations/performance-uncached-local.json
```

On Linux use the local virtual environment's `python`. Fixtures must be on a
writable filesystem outside every Git repository. Normal filesystem access is
needed where Windows sandbox policy denies hard-link publication. The harness
creates only disposable repositories and local test identities. Threshold failure
returns exit 1 while retaining every actual sample or explicit timeout.

Successful operation timers exclude interpreter imports and model latency. Save
payload preparation is outside its timer; the save's own committed-history read,
validation, file/index guards, local Git publication and cleanup are included.
Each operation uses a fresh subprocess. The first read is separate and is not a
controlled OS page-cache flush. Each warm save appends one exchange, so later
samples have a slightly larger history. Timeout deadlines include worker startup;
partial sets have null p95 values and never become a passing measurement.

## Optional cache and trust boundary

Caching requires `NOVEL_CREATOR_VALIDATION_KEY_FILE` to identify an existing
private 32-byte cache key at an absolute path outside the novel. The application
only reads this explicit runtime configuration. It never creates/modifies that
key or writes outside novel-local managed paths. The benchmark creates/removes
its own private key in a separate temporary directory. Product caching is off
until an operator supplies trusted configuration.

Ignored `.novel-creator/local/cache/validation.json` contains an HMAC-authenticated
proof bound to Git HEAD, journal paths/modes/object IDs, schemas and runtime.
It contains no story records. Warm reads fetch every blob from Git, verify its
actual Git object hash and reconstruct current record indexes. Every new exchange
receives full schema/source/authority/hold/transition validation. Missing keys,
novel-provided keys, changed HEAD/schema/runtime, forged or tracked proofs and
cache deletion cause full validation. Cache failures do not change read/save
outcomes. Structural proof does not establish creative acceptance meaning,
literary consistency, language quality or human approval.

## Changes and verification

Profiling identified repeated prefix folding/deepcopy, per-exchange/per-file Git
processes, interpreted schema validation, Python file-open overhead and repeated
path processing. Changes use incremental indexes, batched Git reads/hashes,
compiled checks of the same Draft 2020-12 schemas, complete path-component checks
with fewer temporary objects and the optional authenticated proof. The reference
validator remains for detailed failures and backend parity tests across all nine
record kinds. No model runtime, database or story-state cache was introduced.

Real-Git regressions cover cache deletion/rebuild, forged/tracked proofs, actual
installed-schema changes, changed Git object bytes under the same object ID,
novel-supplied keys, current canon authorization, both Git object formats,
same-size/same-timestamp edits and existing publication/recovery fault windows.
[Linux full-suite evidence](linux-trusted-cache-final-tests.txt) and the final
Windows suite record structural outcomes separately from host/human judgments.

The [initial timeout](performance-scale.json), profiling logs and uncached runs
are retained as prior evidence. `linux-performance-local-key-prototype-30.json`
is an early experiment excluded from the delivered trust design. The final
external-key result is `linux-performance-trusted-cache-30.json`.

T062/T063/T081/T096/T109/T122/T132 complete the measured reference scope.
Current Windows and Linux save p95 remain explicit performance limitations.
Earlier completed reference tasks retain their historical scope. T125-T130/T133
retain actual-host, human, bilingual, Linux/Windows and overall release obligations.
macOS support and verification are deferred from the current release.

Further current-source diagnostics do not replace these 30-run results:
[critical-path events and rejected JSON/parallel-metadata candidates](windows-save-critical-path-20261022.md).
No new runtime, safeguard, benchmark policy or performance threshold is retained
from that investigation. Source remains the verified path-allocation version;
T149 and release remain incomplete, with novice evaluations deferred/unverified.


## Partitioned public history reads — 2026-10-22

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

See [source and diagnostic evidence](windows-history-read-20261022.md). Novice evaluations remain deferred/unverified.


## Balanced save readers — 2026-10-22

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

See [source and all diagnostics](windows-balanced-save-20261022.md).

## Phase 22 ordinary-layout qualification — 2026-10-28

The current full-scale Windows run completes all 30 reads and 30 saves without errors or timeouts at 100 sessions, 5,000 exchanges, 10,000 active assertions and 26,215,716 JSON bytes. First read 1.740510000s; read p95 1.028736700s passes <=2s; save p95 3.067419500s misses <=1s. The default Git executable and ordinary layout request no packing; the opt-in temporary private cache key is outside the novel. No runtime/safeguard/target change is adopted. Four controlled diagnostic saves retain both full guards, six full-content hash partitions and 29 Git calls; new-record validation is about 0.2ms. T172 remains incomplete. See windows-phase22-performance-20261028.md for exact environment, raw timings and overlapping stage measurements. The usable POC is separate from this qualification.

### T172 follow-up: rejected save scheduling alternatives — 2026-10-28

Twenty additional fresh-worker saves on full-scale ordinary-layout fixtures
test reduced concurrency and history-first preparation. Four-save medians are
3.052792150s for the current policy, 4.330007750s for one history reader and
3.224343650s for one initial hash reader. A separate matched schedule comparison
measures 3.087430600s with the current overlap versus 3.309358300s history-first.
All saves succeed with both complete guards and counted history/byte reads.
None demonstrates a gain; no production or harness change is retained.
The independent 30-run p95s above remain authoritative and independently
reverify. T172 and dependent T173 remain unchecked. See
[investigation, exact samples and verifier](windows-phase22-save-investigation-20261028.md).

### T172 private tree construction — 2026-10-28

The next distinct recorded cost, candidate `write-tree` (0.196–0.348s), is
investigated with eight balanced full-scale ordinary-layout fresh-worker saves.
Command-local `core.fscache=true` yields no gain: traced write-tree medians
0.440671700/0.503973800s and complete-save medians 5.589910350/6.019328800s
for control/option. Separate activation tracing proves `write-tree` does not
activate this cache, while a `status` positive control does. Do not interpret
these instrumented medians as a causal slowdown or replacement p95. Internal
tree-update medians are 0.219981000/0.267330000s; index I/O is comparatively small.
Both variants reject missing objects for SHA-1/SHA-256; all full-scale saves
retain complete guards and counted history/hash reads. No production change is
retained. T172/T173 remain open. See
[source, traces, activation control and verification](windows-phase22-write-tree-20261028.md).

### T172 deeper components and lexical-prefix prototype — 2026-10-28

Four complete guarded saves plus eight identical pre-write private-index replays
retain ordinary object-existence checks. Fresh tree-update median is
0.322688500s; existing-tree median is 0.339142500s, with strongly overlapping
ranges and three/zero native hardware flushes respectively. Separate verified
tree-byte compression, object/type/access and scratch-fsync probes have explicit
non-additive limits; exact native subcall decomposition remains unmeasured.
A sampled 100% CPU load and about 2.8 GiB free memory document contention without
attributing every timing difference to it. See
[component measurements and verifier](windows-phase22-tree-components-20261028.md).

An additional distinct lexical-parent-prefix prototype is tested in eight
balanced fresh-worker full-scale saves. Current/prototype medians are
7.865432450/12.297503250s with broad ranges; no improvement is demonstrated.
All saves retain two guards, counted full history/hash reads and fresh native
leaf queries. The prototype is not retained. See
[exact samples, source and verification](windows-phase22-parent-prefix-20261028.md).
No product/harness change or new qualification p95 is claimed. The original
30-run read/save result remains authoritative; T172 and T173 remain open.

### T172 isolated matching-source native Git profiler — 2026-10-28

Built an unmodified control and opt-in owner-thread native timer variant from
Git for Windows v2.53.0.windows.3, exact commit
f8165afd89b0c190677a093f20894f5fce12f97a, using existing MSVC and isolated
CMake/zlib dependencies. Source build and installed distribution remain distinct.
All eight SHA-1/SHA-256 variant checks match tree OIDs and reject missing objects.
Sixteen fresh-worker full-scale guarded saves complete, four per variant, with
every original guard/hash count and source/binary identity retained.

Four native profiles directly record tree-update regions of 29.4009–80.6564ms;
median exclusive lookup/buffer/object-write-remainder/deflate/flush times are
6.72455/1.28755/12.92005/7.67705/9.73975ms, with explicit nesting/clock/compiler
limits. The initial quiet-load gate passes, but all four profile command windows
subsequently exceed its CPU criterion. A stricter follow-up fails its preflight
quiet gate without a new fixture or timing sample. No stable low-load timing,
optimization or p95 pass is claimed. Installed Git and product runtime remain
unchanged; original 30-run qualification and open T172/T173 remain authoritative.
See [builds, native measurements and verifier](windows-phase22-native-profile-20261028.md).


### Phase 23 checked-Git stderr pipes — 2026-10-28

A source-free prototype reduces checked-call pipe/thread overhead, while retaining
unchecked stderr and all save guards. Eight small-command batches per variant
show medians 0.602102700/0.538249500s; eight matched full-scale fresh-worker saves
show no demonstrated complete-save gain (current/prototype medians
6.261266500/6.255118250s, high variable CPU load). All normal-access saves pass
exact guard/hash/object counts; SHA-1/SHA-256 input/output/error checks pass.
No runtime change, new 30-run p95, broad suite or wheel result is claimed.
The retained ordinary-layout read/save p95 are 1.028736700/3.067419500s; save
<=1s remains unmet. T174/T175 remain open. See
[full observations and reproduction](windows-phase23-stderr-pipe-20261028.md).
