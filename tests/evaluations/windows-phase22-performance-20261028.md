# Windows scale qualification — 2026-10-28

T172 remains incomplete: the full-scale read target passes, but the save target
does not. All 30 reads and 30 saves complete without errors, timeouts or cleanup
warnings. No production source, safeguard, target, global setting or dependency
changed during this continuation.

| Measurement | Seconds | Target | Result |
|---|---:|---:|---|
| First fixture read | 1.740510000 | Report separately | Completed |
| Warm read p95 | 1.028736700 | <=2 | Pass |
| Warm validation/local-save p95 | 3.067419500 | <=1 | Unmet |

The fully validated synthetic fixture has 100 sessions, 5,000 exchanges,
10,000 active assertions and 26,215,716 JSON bytes. The ordinary harness layout
requests no Git packing/maintenance. The optional authenticated validation cache
uses a temporary private key outside the novel; it is not enabled globally.
Each operation uses a fresh subprocess, excludes interpreter import/model latency
from the measured operation, and retains its 30-second whole-worker deadline.
The first fixture read does not imply a flushed OS page cache. Payload preparation
is outside the save interval; committed-history validation, both complete guards,
candidate verification, conditional Git publication and cleanup remain inside it.
The evaluation chats were idle during measurement. The harness exits 1 for the
unmet save threshold, not an operation failure.

Windows 11 build 26300, PowerShell 7.6.5, Python 3.13.13 and Git
2.53.0.windows.3 use `C:/Program Files/Git/cmd/git.EXE`. The Lenovo 22AWS00800
has a Core Ultra 7 268V, eight logical processors and 33,847,832,576 bytes RAM;
the fixture volume is C: NTFS. [Current hardware](windows-phase22-hardware-20261028.json).
Source/configuration differences and ambient conditions prevent attributing
changes from historical measurements to a code optimization in this pass.

Command from the checkout with UTF-8, disabled bytecode, `PYTHONPATH=src` and
the external writable temporary directory:

```powershell
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/windows-phase22-ordinary-30-20261028.json
```

[All raw timings and environment](windows-phase22-ordinary-30-20261028.json),
[progress](windows-phase22-ordinary-progress-20261028.txt),
[stdout](windows-phase22-ordinary-stdout-20261028.txt).

## Focused save diagnosis

Two untraced controls bracket two lightweight traced saves on another fully
validated ordinary-layout fixture with the same scale, default Git executable
and cache policy. This is one-process diagnostic evidence, not a replacement
30-run p95 or a causal optimization comparison. The source fingerprint before
and after is unchanged: storage SHA-256
`40c7c1ef61af98e9c1e04292d2befc963bd48bbd45196ce8cbf91576f3ee771b`.
All four saves complete without cleanup warnings; the diagnostic exits 0.

| Stage | First traced save (s) | Second traced save (s) |
|---|---:|---:|
| Complete save | 3.447075 | 4.116955 |
| Full history snapshot | 0.729347 | 1.279955 |
| First complete guard | 1.095943 | 1.921666 |
| First-guard/history overlap | 0.729347 | 1.279955 |
| Second complete guard | 0.847362 | 0.541189 |
| Private-candidate verification | 0.127520 | 0.123573 |
| Managed index cleanup | 0.164518 | 0.122807 |
| New-exchange structural validation | 0.000238 | 0.000185 |

The controls take 2.888616s and 3.075985s. Each traced save retains two complete
guards, six root-bound full-content hash partitions and 29 Git calls. Stage
durations overlap and must not be added as independent serial costs. New-record
validation is a tiny part of this workload; removing durable receipts/fsync would
not address the dominant cost. Earlier metadata/GIL/parallel/hash experiments
remain separately recorded, including their rejected outcomes. These observations
do not justify removing checks or changing their race/error ordering to claim
the 1s target. No additional runtime change is adopted.

[Executed diagnostic source](phase22-save-stages-20261028.py),
[raw ordered events](windows-phase22-save-stages-20261028.jsonl).
The usable single-user POC remains separate from this unmet broader qualification.
