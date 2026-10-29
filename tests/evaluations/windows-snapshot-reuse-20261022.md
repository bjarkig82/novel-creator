# Save snapshot metadata reuse — 2026-10-22

T149 continuation; novice evaluations remain deferred/unverified. This report
tracks a narrow follow-up to the [full-history/file-check work](windows-history-guard-optimization-20261022.md).
The additional directory-scan, queued batch and native binding experiments are
documented [separately](windows-native-git-investigation-20261022.md); none is
retained in the product or its dependency files.

## Change and invariant boundary

Previously `read_snapshot` read a commit tree, then the first managed-file guard
read the same immutable tree again. Save now captures that tree once under the
writer lock and passes its path/mode/OID metadata to the full history reader and
first guard. The second guard already reused the same immutable baseline.
Public `read_snapshot` retains its two-value result and captures its own tree.
No metadata persists across calls, and no history blob or working-file byte
read is removed. Bootstrap's captured absent HEAD remains an empty tree.

Both managed guards still inspect current directories/leaves and the live index,
then hash every managed file's complete bytes. Explicit trusted `GIT_WORK_TREE`
binding remains. All object-byte hashes, schema/source/authority/hold validation,
private candidate index, parent/tree/digest verification, CAS publication,
receipt/fsync ordering and recovery are retained. Optional authenticated-cache
configuration and trust scope are unchanged.

The new real-Git regression verifies reading an explicit prior commit after HEAD
advances for SHA-1 and SHA-256. It passes on the baseline (17.826s), then all five
focused snapshot/root/index/same-stat/bootstrap/retry regressions pass after the
change (68.004s). A read-only review against the exact baseline finds no
actionable issues; it is not runtime or performance verification.

Source SHA-256 before:
`593b46960df2316ea058f03840bb8ac011a716e3c3dd516c8297d0fc91265322`.
After:
`57ba0d7f4dbb3c3ac68a70a74559236c36dadfad07713550f7970369f739a59b`.
Evidence: [baseline invariant](windows-snapshot-reuse-baseline-20261022.txt),
[focused regressions](windows-snapshot-reuse-focused-20261022.txt),
[frozen source/test manifest](windows-snapshot-reuse-verification-20261022.json).

The final frozen Windows suite passes 123 tests in 405.898s: 121 passed, two
explicit real-symlink privilege skips, no failures/errors, exit 0.
[Full Windows log](windows-snapshot-reuse-full-tests-20261022.txt).
Linux/WSL2 passes all 123 tests in 68.212s, zero skips, exit 0.
[Full Linux log](linux-snapshot-reuse-full-tests-20261022.txt).

## Matched diagnostics

Four alternating samples per variant on a fully validated full-size fixture
show save medians 5.859287100s before and 4.449307250s after. Individual saves
range 4.095s-7.009s. This does not establish a causal 24% whole-save gain or p95
compliance. The specific removed tree query takes 0.068s-0.092s in the baseline
trace (median 0.070551150s); it cannot explain the entire observed difference.

The command trace confirms 25 -> 24 Git calls and three -> two tree reads per
save. Four live-index calls, four hash-object calls (including both full bulk
guards) and two cat-file calls (full history plus candidate verification) remain
in every sample. No candidate/publication/cleanup command is removed. This is
diagnostic evidence of reduced duplicate work, not a substitute for adversarial
tests or a passing release measurement.
[All paired timings and command traces](windows-snapshot-reuse-comparison-20261022.txt).

## Final full-scale measurements

Both sequential fresh-process runs use the fully validated 100-session,
5,000-exchange, 10,000-active-assertion, 26,215,716-byte fixture and an explicitly
configured temporary private cache key outside the novel. Both complete 30 reads
and 30 saves with no operation errors/timeouts. Nearest-rank p95:

| Layout | First read | Read p95 | Save p95 | Both targets |
|---|---:|---:|---:|---|
| Ordinary fixture | 4.719508s | 3.545459s | 6.626095s | UNMET |
| Explicitly packed fixture | 4.780077s | 2.277304s | 4.562268s | UNMET |

Packing takes **6.001285800s**, recorded separately and excluded from read/save
latency. It is only an explicit disposable-fixture configuration; no automatic
maintenance or actual-novel packing is added. Sequential independent layout
runs cannot isolate a packing-only effect. Both benchmarks correctly exit 1 for
unmet thresholds. The cause of the higher p95 versus earlier dated results is
not established; historical comparisons cannot isolate this source change.
No 1s save or 2s read compliance is claimed for the final source in either run.

Raw data: [ordinary](windows-snapshot-reuse-default-30-20261022.json),
[packed](windows-snapshot-reuse-packed-30-20261022.json),
[ordinary progress](windows-snapshot-reuse-default-progress-20261022.txt),
[packed progress](windows-snapshot-reuse-packed-progress-20261022.txt).
The [verification manifest](windows-snapshot-reuse-verification-20261022.json)
confirms source/test/benchmark inputs remained unchanged through both suites,
the matched diagnostic and both full benchmarks. Earlier 122-test source results
are preserved as historical evidence, not current-source verification.

Reproduce from the repository root with normal filesystem access and disposable
temporary repositories outside every Git checkout:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -v
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/performance-local.json
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --pack-fixture --output tests/evaluations/performance-packed-local.json
```

Windows 11 build 10.0.26300, Python 3.13.13, Git 2.53.0.windows.3; LENOVO
22AWS00800, Core Ultra 7 268V, eight logical CPUs, 33,847,832,576 bytes RAM,
fixtures on C: NTFS. [Hardware](windows-performance-hardware-20261022.json).
Linux tests use Ubuntu 24.04.4/WSL2, Python 3.12.3, Git 2.43.0 and /tmp ext4;
no new Linux performance measurement is made. Benchmark source SHA-256:
`0130b52a323d4b955f0f66ebb42e93464cac6e8de314b9fe185e8d7227171656`.

T149 remains unchecked; targets and all save safeguards remain unchanged.
Novice observations, semantic host cases and final release verification remain
unverified. No actual novel, dependency file, schema, machine security setting,
specification, plan, checklist or manuscript was modified. No commit/push or
provider activity occurred. Existing unrelated dirty work is preserved.
