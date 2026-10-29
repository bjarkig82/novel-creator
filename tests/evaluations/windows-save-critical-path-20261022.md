# Current Windows save critical path — 2026-10-22

T149 continuation. No runtime, benchmark, schema or save-policy change is retained
from this investigation. The prior turn retained the path-allocation change and
verified it; see [final source and 30-run result](windows-allocation-investigation-20261022.md).
Its packed Windows save p95 remains 3.645534700s against the unchanged 1s target.
Novice evaluations remain deferred/unverified. This is diagnostic evidence,
not a replacement p95 run, passing release gate or hardware lower-bound proof.

All diagnostics use storage SHA-256
69ff00ee3e3a864a458f8c26074e241932911f58c654551afb1b22285eba3035.
[Exact retained source bytes](windows-path-allocation-retained-source-20261022.txt)
are preserved for replay in an isolated source copy. Source remains unchanged.

## Combined JSON decoding — rejected

A parser-only experiment serializes the full 5,000-exchange fixture, validates
its complete chain through ExchangeValidator, then compares 5,000 individual
json.loads calls with one combined array decode. Array assembly is included in
timing. Four balanced samples per variant preserve the default GC policy.

Individual median: 0.196569300s. Combined median: 0.201880000s, slightly slower.
Separate untimed tracemalloc profiles show individual retained/peak Python
allocations 82,543,361/82,550,179 bytes versus combined 66,739,628/92,943,602 bytes.
These profiles start collection outside timing solely for memory measurement;
no production collection policy is changed. Retained memory falls, but peak
memory rises by about 10.4 MB and no latency gain is established. The combined
parser is not implemented in storage; authenticated per-blob checks, parsing and
checkpoint/error-prefix semantics remain unchanged. Neither parser-only result
establishes a whole-save improvement.

[Raw samples](windows-json-batch-parser-diagnostic-20261022.txt) and
[executed script](windows-json-batch-parser-source-20261022.txt).

## Lightweight current-source save stages

The full fixture is 100 sessions, 5,000 exchanges, 10,000 active assertions,
26,215,716 JSON bytes, fully validated before timing, explicitly packed only in
the disposable repository. The temporary trusted key is outside that repository.
Git is the native Git Bash-selected Windows executable. Two untraced saves
surround two traced saves on the same fixture; payload preparation remains
outside the save timer and its history is retained, matching the benchmark.

Untraced controls: 2.133770300s and 2.177321700s. Traced calls: 2.320780900s and
2.226877300s. This small comparison bounds neither overhead nor p95; unlike the
earlier concurrent cProfile output, events record explicit start/end/thread IDs,
so overlapping stages are not added as though serial.

| Stage | Traced save 5002 (s) | Traced save 5003 (s) |
| --- | ---: | ---: |
| Full history snapshot, including authenticated cache/blob checks | 0.927 | 0.901 |
| Complete first managed-file guard | 0.862 | 0.657 |
| First-guard/history overlap | 0.861 | 0.657 |
| Complete second managed-file guard, after candidate and before publication | 0.660 | 0.549 |
| Candidate verification | 0.069 | 0.074 |
| Managed index synchronization | 0.079 | 0.090 |
| New exchange validation | 0.000256 | 0.000355 |

The first guard is almost completely hidden under history validation. The second
complete guard is a material serial cost. Both traced saves execute 24 Git
commands: two complete hash-object --stdin-paths passes, two cat-file requests,
and the existing candidate/index/publication commands. The raw ordered events
show each individual command and its thread. Aggregate command/stage durations
overlap; their sum must not be presented as total save latency. Path counters
include all managed safe-path checks on that thread, including setup/receipt
calls on the main thread; they are not isolated lstat timings.

Durable atomic JSON writes take only a few milliseconds each in these samples.
Removing receipt writes or fsync would not address the dominant observed costs;
no durability or recovery-stage change is justified or made. The separate
30-run p95 remains authoritative for that earlier measured configuration;
two controls near 2.2s do not replace it or establish a source regression/speedup.

[Raw stage events](windows-current-save-stages-20261022.jsonl) and
[executed script](windows-current-save-stages-source-20261022.txt).

## Content-hash pipelining — not adopted

A reviewed design would start hashing an early file after that file's own mode,
path and index checks, while later files' metadata checks continue. It could
preserve every check and root binding, but would move an early byte sample ahead
of the existing all-metadata-before-content phase boundary in the final guard.
It would also add child-process/pipe cleanup and error-precedence complexity.
Independent review identified requirements for complete ordered hashes, process
reaping, metadata error precedence and explicit trusted GIT_WORK_TREE binding.
Given the user's instruction to preserve safeguards, this timing change is not
adopted or implemented. The existing complete bulk-hash phase remains after all
metadata checks. No claim of identical race sampling is made for that rejected
design. The next experiment parallelizes only metadata checks and joins them
before the same complete hash operation, preserving this phase boundary.

## Parallel metadata checks — rejected

A separate external experiment divides the original committed-entry order into
contiguous chunks. Each worker performs every original managed allowlist,
parent/leaf lstat, committed mode and captured live-index check, with its own
fresh directory set. Futures are consumed in original chunk order and all
workers join before the existing complete root-bound byte-hash phase. No
production change is made. Four balanced full-guard samples per configuration
use the same complete validated packed fixture, not a reduced metadata mock.

| Metadata configuration | Complete guard median (s) |
| --- | ---: |
| Current serial metadata checks | 0.466594300 |
| Two metadata workers | 0.446331050 |
| Four metadata workers | 0.563382300 |

The two-worker difference is only about 4.3% and individual samples overlap;
four workers are about 20.7% slower. These results do not justify nested thread
pools, more path-check interleavings and exception-order maintenance. No parallel
metadata implementation or threshold is retained. This is guard-only evidence,
not a whole-save or p95 measurement. A reduced first-guard duration would also
mostly overlap existing full-history work; the experiment does not demonstrate
an end-to-end win. No further broad test or p95 rerun is needed because runtime,
harness and test source are unchanged from the verified 69ff00ee... source.

[Raw samples](windows-parallel-metadata-diagnostic-20261022.txt) and
[executed experiment](windows-parallel-metadata-source-20261022.txt). All diagnostic
process handles are terminal with exit 0. Previous source-pinned full suites and
the 30-run gate failure remain current; T149 remains unchecked, and novice
observations remain explicitly deferred/unverified.
