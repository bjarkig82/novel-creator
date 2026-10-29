# Windows candidate verification — 2026-10-22

T149 continuation. Novice evaluations are deferred at the user's request and
remain unverified; no acceptance or release requirement is waived. The existing
uncommitted guard optimization is the baseline for this pass, not a newly
delivered change. Neither the 1s save target nor the 2s read target changes.

## Diagnosis and discarded experiment

[Fresh profile](windows-save-profile-normal-access-20261022.txt) uses the complete
100-session/5,000-exchange/10,000-active-assertion/26,215,716-byte fixture and an
external temporary trusted cache key. The profiled save takes 4.609s; the worker
also prepares its payload outside that timer. Its 31 Git calls include preparation,
so their total must not be labeled save-only cost. History reads, two complete
managed-file guards and separate Git plumbing commands remain the main costs.
Profiling adds overhead and is not a release p95 measurement.

[Buffered-read experiment](windows-buffer-comparison-20261022.txt) alternates
eight unbuffered and eight buffered bulk reads in the same repository. Every
sample returns the same 5,000 blobs and aggregate SHA-256. Medians are 0.582097s
without buffering and 0.597421s with `cat-file --buffer`. The subsequent four
saves per variant also show no consistent benefit. No buffering or transport
change is retained. Earlier six-sample save diagnostics are in the profile log.

The initial [sandbox attempt](windows-save-profile-20261022.txt) stops at the
existing Windows `os.link` denial (WinError 5); it is environment evidence, not
a product timing or regression result. Subsequent saves use normal filesystem
access and disposable repositories outside Git repositories.

## Candidate verification change

The former candidate check used separate `diff-tree`, `rev-list`, `show` and
candidate `ls-tree` processes. The replacement uses one candidate tree read and
one batched read of the commit and exchange blob. It compares the full tree's
path/mode/object-ID delta against the explicit write allowlist, validates the
commit object hash and exact parent list, then verifies the exact exchange and
payload digest. Parsed objects retain binary byte-length framing checks.

Candidate tree metadata is immutable and reused for subsequent new-file hashing
and managed-index cleanup. Both managed working-file guards still inspect paths,
the live index and every file's complete bytes. The private index, expected-parent
CAS, receipt/fsync sequence, recovery and authority/hold validation are unchanged.
No new dependency, machine configuration or provider operation is involved.

The new real-Git tests cover SHA-1/SHA-256, unexpected additions, unrelated file
modification/deletion, wrong parents, altered exchange JSON, malformed JSON,
truncated/forged batch objects and preservation of HEAD/index/manuscript bytes.
The focused test first failed on the missing verifier, then passed after the
implementation. See [red](windows-candidate-red-20261022.txt) and
[focused green](windows-candidate-green-20261022.txt). Full suites cover bootstrap,
installed commands, races, mode/path guards, cache attacks and recovery.

A separate read-only reviewer found no concrete correctness or safety findings;
it did not run tests or measurements.

## Controlled comparison

[Alternating comparison](windows-candidate-comparison-20261022.txt) uses the same
fully validated scale fixture, Python process, filesystem and optional-cache
configuration. The baseline is the pre-turn storage.py snapshot (SHA-256
`023c90a5dd7c07dc1df308e3f74c9d5b02abb2638d54d7493bc53ce9f597ed4c`),
which already includes the earlier uncommitted guard optimization. The new source
hash is `f1d19709666eba8678ba496c0ec7418c723e4211d0e96a4b819549b2aa809e90`.
No earlier improvement is attributed to this pass.

Six alternating checks per implementation, all against the identical immutable
candidate and tree, reduce candidate-verification median from **0.227261500s to
0.110481450s** (51.4%). Returned tree metadata is identical. A subsequent four
whole saves per implementation measure medians of **3.115621350s before and
3.147080250s after**. Therefore these samples establish the component saving,
but do **not** establish an end-to-end latency reduction. They are diagnostics,
not fresh-process p95 evidence.

## Regression verification

Windows: `.venv/Scripts/python.exe -B -m unittest discover -v` runs **120 tests in
377.170s, 118 passed and two explicit symlink-privilege skips, zero failures or
errors, exit 0**. [Full log](windows-candidate-full-tests-20261022.txt).
`PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1` and TEMP/TMP point to this chat's
canonical external visualization directory. Normal filesystem access is required
for the real hard-link publication operation.

Linux: `wsl.exe --cd C:\Users\BjarkiGunnarsson\source\repos\Personal\novel-creator
--exec /usr/bin/env PYTHONPATH=src PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1
/home/bjarki/.cache/novel-creator-verification/run.I6IApw/.venv/bin/python -B -m
unittest discover -v` runs **120 tests in 56.558s, all passed, zero skips, exit 0**.
[Full log](linux-candidate-full-tests-20261022.txt). Disposable repositories use
Linux `/tmp`; the interpreter is the existing Python 3.12.3 verification
environment. Both real-symlink cases execute on Linux. These are regression
results, not new Linux performance measurements or additional host support.

## Required 30-run measurement

Command: `.venv/Scripts/python.exe -B -m tests.performance.benchmark_records
--runs 30 --progress --output
tests/evaluations/windows-performance-candidate-30-20261022.json`, with the same
UTF-8/bytecode/TEMP/TMP configuration as the Windows tests, normal filesystem
access and no concurrent regression tests or other agent performance work.
The harness creates/removes its own temporary external 32-byte trusted cache key;
each read/save runs in a fresh Python process. Targets and timers are unchanged.

[Raw samples](windows-performance-candidate-30-20261022.json) and
[progress/output](windows-performance-candidate-progress-20261022.txt) record:

| Measurement | Result | Target | Status |
|---|---:|---:|---|
| First read | 3.587267600s | Report separately | Observed |
| Warm read p95, 30/30 | 3.252935300s | <=2s | UNMET |
| Validation/local-save p95, 30/30 | 5.907091200s | <=1s | UNMET |

All 60 measured operations succeed; no operation errors, timeouts or cleanup
warnings occur. Exit 1 correctly reports failed thresholds. The fixture is fully
validated and retains 100 sessions, 5,000 initial exchanges, 10,000 active
assertions and 26,215,716 JSON bytes. Each warm save appends one exchange.

Environment: Windows 11 build 10.0.26300, Python 3.13.13, Git
2.53.0.windows.3. [Fresh hardware/filesystem observation](windows-performance-hardware-20261022.json)
confirms LENOVO 22AWS00800, Intel Core Ultra 7 268V, eight logical CPUs,
33,847,832,576 bytes RAM and C: NTFS.

Samples vary substantially, with both low and high timings retained. The earlier
3.845654300s save p95 remains historical evidence; this pass does not establish
why the latest p95 is higher or attribute that change to the verifier. The
matched whole-save comparison likewise does not establish a save-speed gain.
Only the isolated candidate-verification improvement is demonstrated.

Ruling: retain the two-process verifier based on its measured component benefit,
full delta/parent/digest checks and green regression suites. Cost if wrong:
additional parser/refactoring complexity without a demonstrated whole-save gain.
Further progress toward 1s requires addressing the measured full-history and
full-file-guard costs while preserving their authority and race protections.

T149 remains unchecked. T143/T144 novice observations are deferred and unverified;
host/bilingual and final release obligations remain open. No spec/plan, schema,
dependency, threshold, machine security setting, manuscript, commit or push was
changed. No extension hooks are registered.
