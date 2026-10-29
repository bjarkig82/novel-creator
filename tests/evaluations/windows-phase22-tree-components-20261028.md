# T172 deeper tree-component investigation — 2026-10-28

Existing work and all production safeguards are preserved. T172 is not qualified
by these diagnostics; dependent T173 remains open. This pass separates what the
installed Git can measure directly from independent component probes. It does
not claim an exact additive decomposition of native function time.

## Method and safeguards

The ordinary-layout fixture is fully validated at 100 sessions, 5,000 exchanges,
10,000 active assertions and 26,215,716 JSON bytes. No packing or maintenance is
requested. The temporary private validation key is outside the disposable novel.
Four complete saves execute in one diagnostic process. Each retains two complete
guards, fresh metadata/live-index checks, every actual history/object hash,
private candidate verification, fresh branch/CAS, receipts, fsync and cleanup.

Immediately before each save's ordinary `write-tree`, the runner copies its
invalid private index to an external scratch directory. The original command
runs normally, with Trace2 output. Only after the complete save succeeds does
the runner replay the identical pre-write index twice using separate scratch
indexes. Those commands reconstruct the same tree with the same referenced-
object existence checks, now with already-existing tree objects. They neither
use `--missing-ok` nor bypass cache-tree invalidation. Both replay OIDs must
equal the original tree OID. Confirmed HEAD and the live user index hash must
remain unchanged by all probes.

Separate probes measure native `cat-file --batch-check` over every private-index
blob, Python `os.access` over every ordinary loose-object path, SHA-1 plus zlib
level-1 compression over hash-verified serialized tree bytes, and scratch-file
write/fsync over compressed tree payloads. The batch query reads object type
information and is heavier than an existence check. Python access includes
Python/OS overhead. The compression probe excludes native tree assembly; the
scratch flushes are not timings of Git's own flush calls. The four tree payloads
include the unchanged metadata subtree, whereas the fresh native operation
creates three new trees. Do not add or subtract these independent measurements
to manufacture exact native phase costs or a save speedup.

The version-pinned [tree update source](https://github.com/git-for-windows/git/blob/v2.53.0.windows.3/cache-tree.c)
checks object existence, builds tree buffers and writes objects in one update
region. Its [loose-object lookup path](https://github.com/git-for-windows/git/blob/v2.53.0.windows.3/object-file.c)
uses filesystem access checks. These sources explain the selected probes;
source inspection alone is not a Windows timing measurement.

## Observed results and limits

All four saves and eight same-index tree replays succeed. Original tree traces
record three hardware flushes each; existing-tree replays record zero. Thus the
fresh/existing classification is observable, with ordinary existence checks
retained on both paths.

| Measurement | Median (s) | Range (s) | Scope |
|---|---:|---:|---|
| Fresh native tree-update region | 0.322688500 | 0.274909–0.473938 | Four actual candidate constructions |
| Existing native tree-update region | 0.339142500 | 0.262662–0.464009 | Eight same-index replays |
| Native batch object/type query | 2.547398150 | 2.117913–4.255470 | Four independent, heavier queries |
| Python loose-object access pass | 1.065670750 | 0.247573–2.289205 | Sixteen independent full passes |
| Verified tree-byte hash/compression | 0.049779500 | 0.009964–0.106192 | Sixteen independent passes; assembly excluded |
| Individual scratch-file fsync | 0.002209250 | 0.001765–0.066082 | Sixteen independent flushes |

The fresh and existing update ranges overlap substantially. Removing fresh
writes from a component replay does not establish a latency reduction in this
run. No conclusion that object checks alone dominate, or that compression or
fsync removal would meet the save target, follows from these probes. Exact
native lookup/serialization/write subcall timing remains unmeasured.

During this run a [load sample](windows-phase22-components-load-20261028.json)
records 100% CPU load and 2,941,332 KiB free physical memory (about 2.8 GiB).
This is a sampled condition, not proof of the load throughout every operation
or the cause of each outlier. Instrumented saves take 9.328–12.467s; these are
same-process diagnostics, not fresh-worker qualification samples. The previous
ordinary-layout read/save p95s are not replaced or compared causally against
them. No machine power, security, process or Git settings are changed.

[Executed runner](phase22-tree-components-20261028.py),
[all raw samples](windows-phase22-tree-components-20261028.jsonl),
[verifier](verify-phase22-tree-components-20261028.py),
[verified arithmetic and artifact hashes](windows-phase22-tree-components-verification-20261028.json).
The verifier exits 0 and checks all counts, sequences, native trace durations,
flush classifications, unchanged source identity and probe HEAD/index assertions.
The diagnostic process exits 0 with empty stderr. No source-level product
change is justified by these measurements alone.
