# Windows performance continuation — 2026-10-23

T157 remains incomplete. Production code, safeguards and performance targets are
unchanged from the [verified junction correction](windows-junction-boundary-20261023.md).
These measurements use storage source SHA-256
`a4cc5cba1ffd7f3885610ed98b8e0b965b16d3ed14ead91e73e8b58c7cab88d3`.
No prior uncommitted work was replaced.

## Current packed/direct-Git configuration

Thirty fresh-worker reads and thirty complete validation/local saves use the
full 100-session, 5,000-exchange, 10,000-active-assertion fixture, 26,215,716 JSON
bytes. All operations succeed without timeouts or cleanup warnings. Results:

| Measurement | Seconds | Target | Outcome |
|---|---:|---:|---|
| First fixture read | 1.667932500 | Report separately | Completed |
| Warm read p95 | 0.824995800 | <=2 | Pass |
| Warm validation/local-save p95 | 1.971346700 | <=1 | Unmet |

The harness exits 1 because the save target is unmet. The disposable fixture is
explicitly packed before the cold read; packing takes 5.228656900s and is reported
separately. An opt-in temporary private validation key is outside the novel.
Every operation still reads the full captured history and reconstructs its
ephemeral indexes; saves retain both complete metadata/index/byte guards,
candidate verification, conditional publication and cleanup.

Only this command's child-process PATH selects
`C:\Program Files\Git\mingw64\bin\git.EXE`, Git 2.53.0.windows.3. No machine
PATH, real novel, Git setting or repository history was changed. Runtime:
Windows 11 build 26300, Python 3.13.13, eight logical processors, Intel64 Family
6 Model 189 Stepping 1. Current [hardware/filesystem details](windows-performance-hardware-20261023.json)
identify a Lenovo 22AWS00800, Core Ultra 7 268V, 33,847,832,576 bytes RAM and NTFS
on C:. This configuration is distinct from the previous ordinary
PowerShell/wrapper measurement; no causal speedup over that measurement is claimed.
Neither this run nor packing closes the default Windows performance gap.

Command from the checkout, with PYTHONPATH=src, UTF-8/bytecode-disabled execution
and the process-local direct-Git PATH:

```powershell
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --pack-fixture --progress --output tests/evaluations/windows-junction-packed-direct-30-20261023.json
```

[Full result and environment](windows-junction-packed-direct-30-20261023.json),
[operation progress](windows-junction-packed-direct-progress-20261023.txt).

## Remaining stages

Two lightly traced complete saves, bracketed by two untraced controls on another
full packed fixture, take 1.827012000s and 1.805551200s. Untraced controls take
1.923283300s and 1.772664800s. Thread timings overlap and are not additive or p95.

The first complete guard takes 0.8695–0.8925s, overlapping the full history read
for 0.5033–0.5265s. The final guard takes 0.3598–0.4223s. New-exchange structural
validation takes about 0.0002s; candidate verification about 0.053–0.054s; managed
index cleanup about 0.066–0.073s. Each save retains 29 Git commands. Receipt/fsync
operations remain; removing them would not address the dominant observed cost.

The initial metadata loop has about 0.512–0.533s wall time against 0.172–0.266s
thread CPU time, while the final metadata loop is about 0.101–0.191s. This motivates
the GIL-handoff experiment below, rather than a change to validation semantics.

[Raw stage events](windows-packed-direct-stages-20261023.jsonl),
[executed profile source](windows-packed-direct-stages-source-20261023.txt).

## Metadata GIL policy experiment — rejected

A diagnostic compares the existing WinDLL call with a PyDLL call that retains the
Python GIL during each fresh GetFileAttributesW query. It is restricted to Windows
x64's unified calling convention; no production callable or selection changes.
Each layout uses eight fresh-worker complete saves in ABBA/ABBA order, four per
variant. Every worker counts both original metadata passes and all six root-bound
full-content hash partitions; no cached attributes or skipped check substitutes
for the normal call. Both layouts use direct Git and the full fixture.

| Layout | Existing median (s) | Hold-GIL median (s) | Diagnostic outcome |
|---|---:|---:|---|
| Ordinary | 1.928849400 | 2.025946900 | About 5.03% slower |
| Packed | 1.837499050 | 1.634014500 | About 11.07% faster |

The layout-dependent result does not justify a global policy change or a new
layout-sensitive metadata abstraction. The packed median still exceeds 1s and
these four-sample medians do not establish a p95 result. The experiment exits 0,
all saves complete, and the storage source fingerprint is unchanged. No production
change is retained; the existing full-suite and wheel evidence stays applicable.

[Raw comparison](windows-metadata-gil-diagnostic-20261023.jsonl),
[executed experiment source](windows-metadata-gil-source-20261023.txt).

## Boundaries

The requirement checklist and T151–T158 remain unchanged. These diagnostics add
no novice observations, actual product-host semantic results, bilingual approval
or release approval. No provider call, dependency installation, security-setting
change, commit, push or publication was performed. Human/host evaluation remains
separate from deterministic storage and performance evidence.
