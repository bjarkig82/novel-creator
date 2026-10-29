# Large public Windows history reads — 2026-10-22

T149 continuation. Storage SHA-256:
`9b9092130ff0ee2768ba739cdb9ae28613010ed82b4a9eeb70bb9b342b080ffc`.
Novice evaluations remain deferred/unverified. T149 stays unchecked.

## Behavior and safeguards

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

## Complete verification and required measurement

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

Fixture: 100 sessions, 5,000 exchanges, 10,000 active assertions,
26,215,716 JSON bytes. Fresh process per sample; interpreter
imports and save payload preparation excluded; complete save validation/history,
local publication and cleanup included. First read is fixture-cold, not a
controlled OS page-cache flush. Cache key is temporary/private/outside the novel.
Hardware: Lenovo 22AWS00800, Intel Core Ultra 7 268V, eight logical CPUs,
33,847,832,576 physical-memory bytes, C: NTFS. Windows-11-10.0.26300-SP0,
Python 3.13.13, git version 2.53.0.windows.3.
Git executable: `C:\Program Files\Git\cmd\git.EXE`.
Windows runner: PYTHONUTF8=1, PYTHONPATH=src, PYTHONDONTWRITEBYTECODE=1.
Full suites ran concurrently; benchmark and subsequent diagnostics ran separately
after both suites finished. Other machine activity is uncontrolled. Historical
p95 differences do not isolate source effects or establish a regression/gain.

[Windows suite](windows-history-read-full-tests-20261022.txt),
[Linux suite](linux-history-read-full-tests-20261022.txt),
[raw 30-run result](windows-history-read-default-30-20261022.json),
[progress](windows-history-read-default-progress-20261022.txt),
[hardware](windows-history-read-hardware-20261022.json).

## Matched final-source read comparison

Four balanced fresh-process context reads per policy use identical final source
and an ordinary complete fixture, switching only public-read workers one/four.
All eight return 15,101 records and an authenticated cache hit. Serial median
5.125521150s versus four-worker 2.825309150s (44.88% lower).
The samples are variable; this small comparison does not establish a portable
speedup, p95 compliance or save improvement.
[Matched samples](windows-history-read-comparison-20261022.txt).

Earlier corrected-prototype context medians were 2.052871050s / 1.586789600s /
1.432398200s with one/two/four readers; saves were 4.529989250s / 4.567219250s /
5.588813600s (four samples each). Threshold checks showed no benefit at 256
exchanges; at 1,024, serial/four medians were 0.648670600s/0.565530500s.
That prototype predates the nonzero chunk-boundary fallback correction. Its
valid-data timings informed policy, not current failure-behavior verification.
[Earlier pending checkpoint](windows-history-partition-pending-20261022.md).

## Current save-stage diagnosis

Two untraced controls surround two lightly traced complete saves on one ordinary
full-scale validated fixture. Preparation history remains retained as in the
benchmark. Timings overlap across threads and cannot be added as serial costs.
This is diagnostic evidence, not a replacement for the save p95 above.
[All stage events](windows-history-read-save-stages-20261022.jsonl).

Untraced save 5001: 6.344414200s.

Traced save 5002: 6.435668300s; history 2.928981100s; first guard 2.885872500s; final guard 1.907177300s; first-guard/history overlap 2.885742200s.

Traced save 5003: 8.542812200s; history 3.655283200s; first guard 3.659839100s; final guard 2.256989700s; first-guard/history overlap 3.655283200s.

Untraced save 5004: 7.352925500s.

## Regression coverage and boundaries

Five focused methods pass in 31.152s. Both full suites include SHA-1/SHA-256
cached/uncached equality, captured snapshots after HEAD advances, binary framing,
missing/truncated/header errors, complete/partial nonzero exits on chunk boundaries,
earlier damaged history versus later worker/guard errors, partial submission
cleanup, small-read fallback and serial-save policy. Review caught six failing
nonzero-boundary cases; final focused and full runs include the correction.
Final read-only review found no remaining actionable issue.

The failed disk-full run is preserved separately from its passing retry. After
the user freed space, verification resumed with about 9.9 GB available. An editing
helper's temporary Unicode recoding was reversed: the original test body was
reconstructed exactly to baseline SHA-256 7536bdfb... before verification.

The pending runtime verification is finished; T149's save gate remains unmet.
The original Windows 3.845654300s miss remains historical unmet evidence. No
threshold is lowered; no Linux result substitutes for Windows. Host, human,
bilingual semantic, physical durability and final release gates stay separate.
No provider call, commit or push is performed.

All current artifacts and executed scripts are hashed in the
[evidence manifest](windows-history-read-evidence-manifest-20261022.json).
