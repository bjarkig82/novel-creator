# Full-history reads and file checks — 2026-10-22

T149 continuation explicitly authorized by the user. Novice evaluations remain
deferred/unverified. The baseline already contains the earlier guard metadata
reuse and batched candidate verifier; none of their benefits is attributed to
this pass. The 2s read and 1s validation/local-save targets are unchanged.

## Diagnostics

Disposable, fully validated fixtures contain 100 sessions, 5,000 exchanges,
10,000 active assertions and 26,215,716 JSON bytes. All compared bulk reads return
the same 5,000 blobs and aggregate byte digest. All compared guards check the
complete managed-file population against the same immutable tree and live index.
These same-process component timings are not release p95 measurements.

| Experiment | Baseline median | Variant median | Disposition |
|---|---:|---:|---|
| Bulk Git read, 1 MiB Windows pipe | 0.597082s | 0.543435s | Discarded: modest gain does not justify custom Windows handle/thread lifecycle |
| Full-file guard, validated relative paths | 0.451940s | 0.404684s | Retained: same checks and hashes, less path reconstruction |
| Bulk Git read, requests ordered by object ID | 0.587412s | 0.615729s | Discarded: no benefit |
| Full-file guard, command-local Git fscache | 0.746914s | 0.764162s | Discarded: no benefit; no configuration change retained |
| Bulk Git read after disposable object packing | 0.587412s | 0.276538s | Separate layout experiment; no automatic maintenance added |

Raw samples: [pipe/path comparison](windows-history-file-experiments-20261022.txt)
and [object access/layout comparison](windows-history-access-experiments-20261022.txt).
The packing component is a sequential before/after observation; subsequent
matched-layout and fresh-process measurements are reported separately below.

## Retained implementation and safeguards

`check_managed` still calls `safe_path` for every managed file on each guard
pass. Parent-directory checks are fresh per pass; every leaf's regular-file and
symlink checks remain. Each pass reads the live Git index and hashes every byte
with `git hash-object --no-filters --stdin-paths`. Only its path representation
changes: canonical validated repository-relative strings replace reconstructed
absolute `Path` strings. The bulk hash call explicitly supplies trusted
`GIT_WORK_TREE=NOVEL_ROOT`; `git -C` alone is insufficient when local
`core.worktree` changes after root validation. The existing Git runner strips
inherited `GIT_*` overrides before applying this trusted binding. JSON/C quoting still protects
spaces, Unicode and other supported path characters.

There is no metadata-only shortcut, extra cache, skipped history, custom pipe,
parallel guard or persistent Git setting. Source/authority/hold validation,
both guard passes, private-index candidate construction, parent/delta/digest
checks, CAS publication, receipts/fsync and recovery are retained.

A new regression covers Unicode/spaced roots and managed filenames for SHA-1
and SHA-256, a decoy current directory and inherited Git overrides, same-size/
same-mtime tampering, and staged changes. It passes on the baseline as an
existing invariant and must continue passing after the optimization.
[Baseline test log](windows-relative-guard-baseline-tests-20261022.txt).

## Explicit packing measurement

The benchmark adds `--pack-fixture`, which runs `git repack -ad` only in its
disposable fixture before cold-read timing. It verifies unchanged HEAD and full
path/mode/OID tree, records the selected configuration and packing duration,
then performs the same validation, reads, full file checks and saves. Default
fixture layout and operation timers are unchanged. Packing time is reported
separately, not included in read/save latency. Packed results do not establish
default-layout performance. No actual novel repository is packed or modified.

A separate read-only review initially found no issues, then identified a P1
root-binding issue during focused follow-up. A changed ancestor `core.worktree`
and duplicated index prefix could mask same-size/mtime byte tampering in the
relative-path prototype. The real-Git regression failed for SHA-1 and SHA-256
before the fix, then passed after explicit trusted worktree binding. HEAD and
the externally modified index must remain unchanged on rejection. See
[red](windows-worktree-guard-red-20261022.txt) and
[focused green](windows-worktree-guard-green-20261022.txt).

The staged-change fixture also now writes its known changed blob directly to
the index: Git add may skip a same-stat change, so relying on it made the fixture
nondeterministic. The assertion and guard are unchanged. Early 121-test runs and
[prototype timings](windows-history-guard-comparison-20261022.txt) predate this
root-binding fix; final verification and timings below use the corrected source.

## Final regression verification

The frozen Windows run executes 122 tests in 326.671s: 120 pass, two explicit
real-symlink privilege skips, no failures/errors, exit 0. Linux/WSL2 executes all
122 in 60.080s with no skips. After correcting the deterministic staged-index
fixture, both focused guard tests pass again on Linux against the final files.
The earlier broad Windows fixture failure is preserved separately; it does not
count as passing verification.

Evidence: [Windows](windows-history-guard-final-tests-20261022.txt),
[Linux full suite](linux-history-guard-final-tests-20261022.txt),
[Linux final fixtures](linux-history-guard-final-focused-20261022.txt), and
[frozen input manifest](windows-history-guard-verification-manifest-20261022.json).
Storage SHA-256 is
`593b46960df2316ea058f03840bb8ac011a716e3c3dd516c8297d0fc91265322`;
the manifest also fingerprints the helper, regression tests and benchmark.

## Final matched diagnostics

The final alternating comparison uses the pre-turn storage snapshot
`f1d19709666eba8678ba496c0ec7418c723e4211d0e96a4b819549b2aa809e90`
and the final root-bound source above, in the same process/configuration.
Four samples per variant show full-file-guard median 0.762300100s before and
0.532218250s after (30.2% lower), and whole-save median 4.314992800s before
and 3.646429000s after (15.5% lower). These limited component/whole-operation
diagnostics do not establish p95 compliance or a portable percentage gain.

A separate matched-layout diagnostic clones an identical already validated
snapshot at 5,008 exchanges into ordinary and packed repositories. Read medians
are 2.263453150s ordinary and 1.534817100s packed; save medians are 3.777716700s
ordinary and 3.868343500s packed. Thus this diagnostic supports a read benefit
from packing, but no save improvement. It is not the canonical fresh 5,000-
exchange, 30-run benchmark. Earlier exploratory prototype timings are not
substituted for these final-source measurements.
[All final matched samples](windows-history-guard-comparison-final-20261022.txt).

## Final full-scale fresh-process measurements

Both configurations use the complete fully validated 100-session/5,000-exchange/
10,000-active-assertion/26,215,716-byte fixture and an opt-in authenticated cache
with a temporary private key outside the novel. Each completes 30 warm reads and
30 saves, with no operation errors/timeouts. Nearest-rank p95 and first read:

| Fixture layout | First read | Read p95 | Save p95 | Result |
|---|---:|---:|---:|---|
| Ordinary, no explicitly requested maintenance | 2.354371s | 1.715364s | 3.398351s | Read passes; save unmet |
| Explicitly packed disposable fixture | 1.913063s | 1.020151s | 2.739170s | Read passes; save unmet |

Packing takes **4.742777600s**, excluded from operation latency. This separate
layout result does not establish default performance or a packing-only save
gain: the matched diagnostic above did not show a save benefit, and these full
runs execute sequentially on separate fresh fixtures. Cross-run changes from
earlier dated results likewise cannot isolate source effects. Both benchmarks
correctly exit 1 for the unmet save threshold; T149 remains unchecked.

Raw data: [ordinary](windows-history-default-30-20261022.json),
[packed](windows-history-packed-30-20261022.json),
[summary](windows-history-performance-summary-20261022.json),
[ordinary progress](windows-history-default-progress-20261022.txt),
[packed progress](windows-history-packed-progress-20261022.txt).
The frozen input manifest confirms unchanged inputs after all measurements.

Reproduce from the repository root with normal filesystem access and a temporary
directory outside every Git repository:

```powershell
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/performance-local.json
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --pack-fixture --output tests/evaluations/performance-packed-local.json
```

Environment: Windows 11 build 10.0.26300, Python 3.13.13, Git 2.53.0.windows.3;
LENOVO 22AWS00800, Core Ultra 7 268V, eight logical CPUs, 33,847,832,576 bytes
RAM, disposable fixtures on C: NTFS. See [hardware](windows-performance-hardware-20261022.json).
Benchmark SHA-256:
`0130b52a323d4b955f0f66ebb42e93464cac6e8de314b9fe185e8d7227171656`.
No new Linux performance measurement was made; its earlier opt-in-cache result
remains historical reference evidence. Novice observations, semantic host cases
and final release verification remain unverified. No actual novel, threshold, dependency,
schema, machine setting or manuscript was changed; no commit/push was performed.

## Subsequent diagnostics — no runtime change retained

The continuing T149 investigation uses the same source SHA above and complete,
fully validated disposable fixtures. Fresh directory-enumeration metadata
reduces four-sample guard median 0.838214800s -> 0.772965800s, while whole-save
median is 4.046034200s -> 3.967549300s with substantial variation. This does not
justify added metadata-path complexity; no directory-enumeration shortcut is
retained. [Samples and current-source profile](windows-scandir-diagnostic-20261022.txt).
The profile includes payload preparation outside the save timer; its cumulative
worker time must not be substituted for validation/local-save latency.

Queued `cat-file --batch-command --buffer` requests followed by `flush` return
the same 5,000 blobs and aggregate byte digest. Bulk-read medians are
0.657076700s -> 0.649685500s. Whole-save medians are 5.314088150s ->
4.383178300s, but individual samples span 3.604s-7.701s and the component result
does not isolate that apparent whole-save difference. No queued protocol change
is retained on this evidence. [Raw samples](windows-batch-queue-diagnostic-20261022.txt).
These diagnostics are not new 30-run p95 measurements. The final verified source,
ordinary/packed p95 results, safeguards, T149 open status and novice deferral above
remain unchanged.
