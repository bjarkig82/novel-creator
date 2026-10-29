# Overlap complete first guard with history validation — 2026-10-22

T149 continuation; novice evaluations remain deferred/unverified. Earlier source
results remain in the [snapshot-reuse report](windows-snapshot-reuse-20261022.md).
The 2s read/1s validation-local-save targets remain unchanged.

## Retained candidate and safety boundary

Under the same writer lock, an established commit's first complete managed-file
guard may run while the main thread reads and validates every history blob.
Both consume the exact same captured immutable tree metadata. The complete
first-guard result is required at its original position, after history, pending,
stale, record and manifest validation and before writing transaction receipts
or preparing candidates. The second guard remains fresh immediately before
publication. Bootstrap with absent HEAD and existing-path retries use the prior
serial behavior. No guard, object-byte hash, file/index/path check, schema,
authority/hold check, candidate verification, CAS, fsync or recovery is removed.

The executor exits before the writer lock, even after a validation error. It
shares no mutable validation state and leaves no background work after return.
If both history and background guard fail, the earlier history validation error
and its last valid checkpoint retain precedence.

Earlier first-guard sampling changes a permitted race outcome: a persistent edit
made after the background guard completes but while validation is still running
can leave a pending receipt/candidate before the second guard rejects it. The
serial path might reject this same timing before preparation. Neither path
publishes changed managed bytes. Pending work remains explicitly unconfirmed and
recoverable; no automatic retry or disposition is added.

Two coordinated real-Git regressions exercise that exact race and simultaneous
unreadable history/background guard failure for SHA-1 and SHA-256. They assert
unchanged HEAD/user index, preserved external bytes, truthful checkpoint/pending
recovery, no leaked writer lock and no new pending files for unreadable history.
The serial baseline cannot exercise the coordination and fails the wait
conditions (four subcases); this is not evidence of an authority bug in that
baseline. After implementation, all five focused race/root/index/bootstrap/retry
tests pass in 23.715s. A read-only review finds no actionable issues while
explicitly identifying the pending-race timing difference above.
[Coordination red](windows-guard-overlap-red-20261022.txt),
[focused green](windows-guard-overlap-focused-20261022.txt).

Before source SHA-256:
`57ba0d7f4dbb3c3ac68a70a74559236c36dadfad07713550f7970369f739a59b`.
Current candidate:
`16de2fab76922e9252924eada706c7a8d5071875c68e155279192edd749b5828`.
[Frozen inputs](windows-guard-overlap-verification-20261022.json).
The frozen Windows suite runs 125 tests in 318.673s: 123 passed, two explicit
real-symlink privilege skips, no failures/errors, exit 0.
[Windows log](windows-guard-overlap-full-tests-20261022.txt).
Linux/WSL2 passes all 125 in 36.951s with zero skips, exit 0, including both
coordinated races and symlink cases.
[Linux log](linux-guard-overlap-full-tests-20261022.txt).
Fresh-process measurements are in progress; no new compliance claim is made
before they complete.

## Initial disposable diagnostics

The complete 100-session/5,000-exchange/10,000-active-assertion/26,215,716-byte
fixture is fully validated. Four alternating whole saves per variant show
median 3.263001450s serial and 2.803969000s with overlap (14.1% lower). This is
an initial same-process prototype, not p95 or final-source measurement.
[Raw samples](windows-guard-overlap-diagnostic-20261022.txt).

A separate same-source diagnostic compares installed Git 2.53.0.windows.3's
46,464-byte `cmd/git.exe` launcher and 4,344,704-byte direct executable.
Sixteen alternating samples per variant show HEAD-query median 0.035645100s ->
0.019727950s and live-index-query median 0.035392050s -> 0.020348700s. Four
whole saves per variant show median 3.044177150s -> 2.794276850s. No PATH,
machine setting, product executable selector or dependency was changed.
[Raw samples](windows-git-launcher-diagnostic-20261022.txt).

Git for Windows documents the [wrapper and supported direct invocation](https://gitforwindows.org/git-wrapper.html).
Git Bash on this installed system selects `/mingw64/bin/git`; PowerShell selects
the wrapper under `cmd`. The benchmark now records `git_executable`. A separate
Git Bash packed-fixture configuration will measure this normal native Windows
runtime selection without replacing the ordinary-layout/default-shell result,
persistently changing PATH, or substituting Linux performance.

The final-source matched diagnostic completes four alternating saves per variant
with medians 3.014429850s serial and 2.673034800s overlapping (11.3% lower).
These are same-process diagnostics, not p95 compliance or a portable speedup.
Every variant retains 24 Git calls, including four live-index, four hash-object
and two cat-file calls; overlapping work does not remove these checks.
[Final-source timings and command traces](windows-guard-overlap-comparison-20261022.txt).

## Final Windows full-scale measurements

All three sequential fresh-process configurations use the complete fully
validated fixture and an opt-in authenticated cache with a temporary private
key outside the novel. Each completes 30 reads and 30 saves without operation
errors/timeouts. Nearest-rank p95:

| Native Windows configuration | First read | Read p95 | Save p95 | Targets |
|---|---:|---:|---:|---|
| PowerShell, ordinary fixture, Git launcher | 2.672014s | 2.014926s | 2.733242s | Both unmet |
| PowerShell, packed fixture, Git launcher | 1.977750s | 1.045106s | 2.209314s | Read passes; save unmet |
| Git Bash, packed fixture, direct Git | 2.225943s | 0.942910s | 1.719384s | Read passes; save unmet |

Packing takes 4.524228100s in the PowerShell packed run and 2.971372300s in the
Git Bash run, separately recorded and excluded from operation latency. These
sequential independent runs cannot isolate a packing-only or launcher-only
effect. Each configuration remains separately labeled: Git Bash is native
Windows Python/Git on NTFS, not a replacement Linux result or proof of default
PowerShell/ordinary-layout performance. No automatic packing, persistent PATH
change, product executable selector or new dependency is introduced.

The ordinary read misses 2s by about 0.015s; it is not rounded into a pass.
Every Windows configuration misses the 1s save gate and correctly exits 1.
T149 remains unchecked. Historical p95 differences cannot isolate source effects;
the matched comparison above separately measures the retained code change.

Raw data: [ordinary](windows-guard-overlap-default-30-20261022.json),
[packed PowerShell](windows-guard-overlap-packed-30-20261022.json),
[packed Git Bash](windows-guard-overlap-git-bash-packed-30-20261022.json).
Each records the selected Git executable. The
[verification manifest](windows-guard-overlap-verification-20261022.json)
confirms unchanged source/test/benchmark inputs across both full suites, the
matched diagnostic and all three Windows configurations.

## Linux reference and paired follow-up

The current source and schema bytes are copied identically into a disposable
ext4 runtime tree, with fixtures/private cache key on /tmp ext4. The runner
asserts that both loaded storage and schema resources come from that copy.
Ubuntu 24.04.4/WSL2, Python 3.12.3, Git 2.43.0 at `/usr/bin/git`, same laptop.
No source or framework Git authority is changed. The source remains identical
after measurement. See [source manifest](linux-guard-overlap-source-manifest-20261022.json).

The complete fixture is fully validated and all 30 reads/saves succeed without
operation errors/timeouts. First read 2.171033683s; read p95 **1.153318426s**
passes 2s, save p95 **1.072006791s** misses 1s; exit 1. Thus the historical
Linux 0.826s/0.982s reference pass is preserved as historical evidence, not
claimed for this current-source run.
[Raw result](linux-guard-overlap-reference-30-20261022.json),
[progress](linux-guard-overlap-reference-progress-20261022.txt).

To investigate the miss, an additional same-fixture ext4 comparison executes
eight alternating saves per variant: serial median 0.948380694s, overlapping
median 0.788780154s (16.8% lower). This supports a component/median benefit but
does not establish passing p95 or explain the full-run tail. It is not substituted
for the failing 30-run result. Both exact source versions and byte-copy status
are recorded in the [paired-source manifest](linux-guard-overlap-paired-source-20261022.json),
with [all paired timings](linux-guard-overlap-paired-20261022.txt).

## Reproduction and remaining gates

From the repository root, using normal filesystem access and temporary fixture
directories outside every Git checkout:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -v
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/performance-local.json
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --pack-fixture --output tests/evaluations/performance-packed-local.json
```

For the Git Bash configuration run the last benchmark command in Git Bash,
using its normal PATH selection; it still launches native Windows Python/Git.
For Linux use the local Python environment with runtime/schema bytes and
fixtures on ext4, recording their actual loaded locations. No packing was
requested in the Linux reference run. The benchmark retains first-read timing,
per-operation deadlines, full samples and nearest-rank p95; imports/model latency
remain outside operation timers as documented in [performance.md](performance.md).

Windows 11 build 10.0.26300, Python 3.13.13, Git 2.53.0.windows.3; LENOVO
22AWS00800, Core Ultra 7 268V, eight logical CPUs, 33,847,832,576 bytes RAM,
fixtures on C: NTFS. [Hardware](windows-performance-hardware-20261022.json).
Benchmark SHA-256:
`7f69593cbee6330af1cb67261f662db8d186cc6d00787d3710d002a8430650f2`.

T149 remains unchecked: no measured current-source configuration passes both
targets. Novice evaluations remain deferred/unverified, other host/semantic
gates remain unverified, and release is incomplete. No guard or target is
weakened; no actual novel, dependency, schema, machine setting, spec/plan,
checklist or manuscript is changed. Existing dirty work is preserved. No
provider call, commit or push occurs. No extension hooks are configured.
