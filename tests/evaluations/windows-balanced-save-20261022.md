# Balanced Windows save readers — 2026-10-22

T149 continuation. Storage SHA-256:
`9bbcb0acb6442ef45ce564d4b9980abe5889fbd0373d14acb2387ae429bf2a44`.
Novice evaluations remain deferred/unverified. T149 remains unchecked.

## Retained policy and safeguards

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

## Verification and complete required benchmark

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

The fixture contains 100 sessions, 5,000 exchanges, 10,000 active assertions
and 26,215,716 UTF-8 JSON bytes. Every timed operation uses a
fresh worker; import time and save payload preparation are excluded. Complete
save history/validation, local publication and cleanup remain included. First
read is fixture-cold rather than an OS page-cache flush. Cache trust uses a
temporary private key outside the novel, not a novel-provided key.
Hardware: Lenovo 22AWS00800, Intel Core Ultra 7 268V, eight logical CPUs,
33,847,832,576 memory bytes, C: NTFS. Windows-11-10.0.26300-SP0; Python
3.13.13; git version 2.53.0.windows.3. Git executable:
`C:\Program Files\Git\cmd\git.EXE`. PYTHONUTF8=1, PYTHONPATH=src,
PYTHONDONTWRITEBYTECODE=1. Suites run concurrently; the benchmark and each
subsequent diagnostic run separately after both suites finish. Other machine
activity is uncontrolled; differences from dated historical p95 runs do not
isolate this policy's effect. Disk space was freed before verification resumed.

[Windows full suite](windows-balanced-save-full-tests-20261022.txt),
[Linux full suite](linux-balanced-save-full-tests-20261022.txt),
[raw 30-run result](windows-balanced-save-default-30-20261022.json),
[operation progress](windows-balanced-save-default-progress-20261022.txt),
[hardware](windows-history-read-hardware-20261022.json).

## Matched final-source comparison

Eight fresh-worker complete saves use balanced ABBA/ABBA order on one ordinary
complete fixture, four samples per policy. Identical final source selects one
history/one first-guard reader for controls and two/two for the retained policy;
public payload preparation and four final hash readers remain unchanged. All
saves succeed at sequences 5001–5008 with no cleanup; Git calls are 25/27.
Control median 3.509755100s; two/two median 3.061612450s (12.77% lower).
Control range 3.300296400–3.594787400s; retained-policy range
2.859302900–3.339475700s. These small variable samples support
policy assessment; they are not p95, a portable speedup or release compliance.
[Raw final-source samples](windows-balanced-save-comparison-20261022.txt).
The [earlier external candidate](windows-balanced-save-readers-20261022.md)
measured medians 5.669104200s/4.856166300s; it did not verify production adoption.

## Current save stages

Two untraced controls surround two lightly traced complete saves on one ordinary
full fixture. Payload-preparation history remains retained, matching the benchmark.
Thread durations overlap and must not be added as though serial. This diagnostic
does not replace the 30-save p95. [All events](windows-balanced-save-stages-20261022.jsonl).

Untraced save 5001: 4.642043100s.

Traced save 5002: 5.051923600s; history 1.655906000s; first guard 2.432966300s; final guard 1.488390200s; first-guard/history overlap 1.655906000s.

Traced save 5003: 5.140352500s; history 1.838221800s; first guard 2.605543700s; final guard 1.408892000s; first-guard/history overlap 1.838221800s.

Untraced save 5004: 4.529389500s.

## Regression and review evidence

The initial five-method red run failed on 17 missing-policy cases before runtime
changes. Eight focused methods subsequently pass in 85.046s. Five combined
production regressions cover Windows/non-Windows policy, small bootstrap/retry,
earlier malformed history versus later worker/nonzero failure and failed first
guard, first-guard launch/process/count/partial-thread-submit failures with all
workers joined under the lock, real-root same-stat tampering despite a decoy,
post-first-guard edits caught by the final guard, recoverable pending work and
unchanged retry publishing once with identical history. Existing binary framing
cases exercise both two and four history readers. Both full suites include them.
Read-only review of the minimal delta found no actionable issue.

The preceding source's [138-test verification and 1.787683800s/9.219870400s p95](windows-history-read-20261022.md)
remain source-specific historical evidence. The original Windows 3.845654300s
save miss remains historical unmet evidence. No threshold is lowered or Linux
result substituted for Windows. Novice evaluations remain deferred/unverified;
other host, bilingual semantic, durability and release gates remain open.
No provider call, commit or push is performed.

[Source, executed scripts and artifact hashes](windows-balanced-save-evidence-manifest-20261022.json).
