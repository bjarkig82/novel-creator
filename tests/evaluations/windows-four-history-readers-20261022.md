# Four Windows save-history readers — 2026-10-22

T149 remains open. Novice evaluations remain deferred and unverified.
Storage SHA-256: `2563aa5a257971a264d2a36094a818a528a561509e4f48d47ad24c6c708f4fb3`.

Large Windows saves now use up to four history readers instead of two.
The existing 1,024-item threshold keeps small histories serial; non-Windows
keeps one reader. The initial full-byte guard retains two readers and the final
full-byte guard four. All history is read and hashed; JSON and ephemeral indexes
are rebuilt. Ordered framing, captured OIDs, original serial fallback, all child
joins, damaged-prefix/error precedence and lock lifetime remain. Fresh native
bundle metadata with conservative lstat fallback, parent checks, both complete
byte/live-index/path/type guards, candidate/tree/digest/parent verification,
authority/hold checks, fresh branch/CAS, receipts and recovery remain unchanged.
No check is skipped and no target is lowered.

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

The fully validated synthetic fixture contains 100 sessions, 5,000 exchanges,
10,000 active assertions and 26,215,716 UTF-8 JSON bytes.
Fresh worker per operation; import time and payload preparation excluded;
full committed-history validation, local publication and cleanup included.
Cache uses a temporary private key outside the novel. First read is fixture-cold,
not a guaranteed OS-cache flush. Suites ran concurrently; benchmark and matched
comparison ran separately after suite completion. Other machine activity is
uncontrolled; historical p95 differences do not isolate this change's effect.
Windows-11-10.0.26300-SP0; Python 3.13.13; git version 2.53.0.windows.3.
Git: `C:\Program Files\Git\cmd\git.EXE`. Hardware remains the recorded Lenovo
22AWS00800, Intel Core Ultra 7 268V, 8 logical CPUs, 33,847,832,576 RAM bytes, NTFS C:.
PYTHONUTF8=1, PYTHONPATH=src, PYTHONDONTWRITEBYTECODE=1.

The baseline component profile attributes 0.79-0.80s of the 1.03-1.08s
history stage to Git cat-file reads, 0.14-0.19s to JSON decoding, about 0.015s
to blob hash constructors and 0.019s to certified index reconstruction. Per-call
tracing has overhead; threaded durations overlap and are not additive.
[Component profile](windows-history-components-20261022.jsonl).
An initial eight-save ABBA/ABBA comparison on that baseline produced medians
2.544967200s/2.258775650s for two/four history readers, an 11.25% lower median.
[Initial experiment](windows-native-history-workers-20261022.txt).

Matched final-source comparison: eight successful complete saves, fresh workers,
ABBA/ABBA, four per two/four history-reader policy, identical ordinary fixture
and public payload preparation. Two-reader median 2.423592550s; four-reader
median 2.358867650s (2.67% lower). All six complete root-bound hash
partitions and fresh native queries remain; Git calls are 27/29 per save.
These variable samples are diagnostic, not p95 or portable speedup evidence.

The default-policy red run fails 2 != 4 before the runtime edit. Ten focused
methods pass in 49.588s. Combined regressions exercise four history children
joining before serial fallback alongside the two-reader initial guard,
earlier malformed history versus later launch/nonzero failures and a failed
guard, guard failures/join-before-unlock, small bootstrap/identical retries,
SHA-1/SHA-256 native same-stat and live-index tampering, pending receipts and
exact retry publishing once. Full suites cover root redirection, captured
snapshots, framing and partial-submit errors. Read-only review against the exact
previous source found no actionable issue or important coverage gap.
Windows physical symlink cases remain explicit privilege skips, not passes.
No novice, host, bilingual semantic, durability or release approval is inferred.
The original 3.845654300s Windows save miss remains historical unmet evidence;
Linux reference results do not substitute for the Windows gate.
No provider call, commit or push was performed.

[Windows suite](windows-four-history-readers-full-tests-20261022.txt),
[Linux suite](linux-four-history-readers-full-tests-20261022.txt),
[30-run result](windows-four-history-readers-default-30-20261022.json),
[progress](windows-four-history-readers-default-progress-20261022.txt),
[matched samples](windows-four-history-readers-comparison-20261022.txt),
[hardware](windows-history-read-hardware-20261022.json),
[source and artifact hashes](windows-four-history-readers-evidence-manifest-20261022.json).

Final-source stage diagnostic: two lightly traced saves between two untraced controls; thread timings overlap and are not additive. These are not p95 samples.

Untraced save 5001: 2.207456900s.

Traced save 5002: 2.228005400s; history 0.891917000s; first guard 0.887920000s; final guard 0.458527700s; first-guard/history overlap 0.887855800s.

Traced save 5003: 2.323843700s; history 1.003161500s; first guard 1.028309400s; final guard 0.414592400s; first-guard/history overlap 1.003161500s.

Untraced save 5004: 2.344256100s.

[Stage events and per-thread path counters](windows-four-history-readers-stages-20261022.jsonl).
