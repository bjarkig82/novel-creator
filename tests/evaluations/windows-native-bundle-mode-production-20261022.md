# Native Windows bundle metadata production verification — 2026-10-22

T149 remains open. Novice evaluations remain deferred and unverified.
Storage SHA-256: `6d1b50fe2d7af827d0ebebac12b8538c525081d40bab74cdf00febe2968adf60`.

Windows ordinary canonical bundle leaves use fresh GetFileAttributesW queries.
Only NORMAL alone or nonzero combinations of ARCHIVE/READONLY/HIDDEN/SYSTEM
classify regular files directly. Invalid, unknown, special, directory, reparse,
unavailable and exceptional results use the original lstat. Parents, other
managed paths, small bootstrap/write paths and non-Windows behavior retain
original checks. Only the API callable is cached; filesystem metadata is fresh.
Both complete live-index/path/type/byte guards, metadata-before-hash ordering,
root binding, full historical blob/digest/schema/authority/hold validation,
private candidate verification, worker joins under the lock, original error
ordering, fresh branch/CAS, receipts and recovery remain. No check is skipped.

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

Matched final-source comparison: eight successful complete saves, fresh workers,
ABBA/ABBA, four per native policy on/off, identical ordinary fixture and retained
public payload preparation. Control median 2.815003650s; native median
2.426111300s (13.81% lower). All 27 Git calls and six complete root-bound
hash partitions are retained per save. Every native leaf query is counted anew.
These variable samples are diagnostic, not p95 or portable speedup evidence.

Seven new regressions cover all accepted attribute combinations, conservative
fallback and original exceptions, typed optional API failures, fresh leaf-only
queries, Unicode and real extended Windows paths, both Git object formats,
same-stat byte tampering, live-index tampering, pending receipts, exact retries
publishing once, bootstrap/public-read boundaries. Initial red: seven tests,
125 missing-feature errors, 4.469s. Final focused: nine tests, 25.960s, exit 0.
Read-only production review found no actionable issue. Existing Windows physical
symlink cases remain explicit privilege skips; they are not reported as passes.
No novice, host, bilingual semantic, durability or release approval is inferred.
No provider call, commit or push was performed.

[Windows suite](windows-native-bundle-mode-full-tests-20261022.txt),
[Linux suite](linux-native-bundle-mode-full-tests-20261022.txt),
[30-run result](windows-native-bundle-mode-default-30-20261022.json),
[progress](windows-native-bundle-mode-default-progress-20261022.txt),
[matched samples](windows-native-bundle-mode-production-comparison-20261022.txt),
[hardware](windows-history-read-hardware-20261022.json),
[source and artifact hashes](windows-native-bundle-mode-production-evidence-manifest-20261022.json).

Final-source stage diagnostic: two lightly traced saves between two untraced controls; thread timings overlap and are not additive. These are not p95 samples.

Untraced save 5001: 2.944902100s.

Traced save 5002: 2.530748700s; history 1.135110500s; first guard 0.877956200s; final guard 0.406415400s; first-guard/history overlap 0.877838100s.

Traced save 5003: 2.341749100s; history 1.061177600s; first guard 0.645508300s; final guard 0.381091300s; first-guard/history overlap 0.645443600s.

Untraced save 5004: 2.502154500s.

[Stage events and per-thread path counters](windows-native-bundle-mode-production-stages-20261022.jsonl).
