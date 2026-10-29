# Partitioned full-history reads: initial candidate, not retained

2026-10-22, T149 continuation against unchanged verified source `6ec58b45314b7a99877220452367f6b89b532bed2fe3b3c842f0272a9aba1f5a`.
Novice evaluations remain deferred/unverified. Production continues to use its
existing single full-history batch request. The retained parallel final-byte
check optimization is a separate change documented in
[its verified report](windows-parallel-hash-20261022.md).

This external prototype partitions immutable captured blob-OID requests into
contiguous chunks. Each child uses the existing Git wrapper and `cat-file
--batch`, preserving `check=False`. All children join before any blob is yielded.
The prototype parses each child's stdout separately and yields blobs in original
path order. Existing `_read_snapshot` still checks each actual blob hash on
certified reads, JSON, schema version, filename binding and unchanged validation
or certified indexing. No runtime file, cache policy, authoritative record,
private index, candidate/CAS or recovery implementation is changed.

## Timing evidence

One ordinary-layout disposable Windows/PowerShell fixture contains all 100
sessions, 5,000 exchanges, 10,000 assertions and 26,215,716
JSON bytes, fully validated before timing. Four balanced full-history snapshot
reads per configuration measure median 3.853349350s serial,
1.856889300s with two requests and 1.474333450s with four. Every snapshot
has 5,000 exchanges, 15,101 records and an authenticated cache hit. These timers
include original parsing, actual-blob hashing and index reconstruction; they
exclude context formatting and complete saves. This is component evidence,
not a 30-run fresh-worker p95 measurement.

A subsequent ABBA/ABBA comparison retains payload-preparation history for both
variants and times complete saves, with the existing initial overlapping guard,
final parallel byte guard, candidate checks, CAS and cleanup all active. Four
samples per variant measure 5.399026300s median serial versus
5.505927300s with four history requests. All eight saves succeed at
sequences 5001–5008 with no cleanup requirement. Git invocations rise from 25 to
28. The component gain does **not** establish a complete-save benefit; this small
save comparison is slightly slower and noisy. No explanation of that difference
is established, and no p95 compliance is claimed.

## Safeguard review: correction required before adoption

Independent read-only review found that a later chunk's launch/worker exception
is propagated before earlier blobs are parsed. It can therefore mask earlier
damaged history and its verified-prefix checkpoint. Separately, parsing each
chunk's stdout in isolation would ignore trailing output before a chunk boundary
that the original single-stream parser would encounter. These are unretained
prototype design gaps; production still uses the original reader.

A correction must preserve the single-stream framing and error/checkpoint order.
One bounded option is to join all started workers and fall back once to the
original serial request on a worker/submission failure, before yielding anything.
Successful chunk stdout can be concatenated in original order and fed through the
unchanged single-stream parser, at the cost of an additional raw-output allocation.
Nonzero process exit with usable stdout must retain the original parsing policy.
No corrected implementation or corresponding performance is claimed here.

Before adoption, SHA-1/SHA-256 regressions must cover malformed earlier history
versus a later launch failure and simultaneous guard conflict; missing, truncated
or invalid-header objects on both sides of chunk boundaries; complete/partial
stdout with nonzero status; worker/thread-start failures and cleanup; cached and
uncached equality; and explicit snapshot binding after HEAD advances. Read-only
context performance and two-worker complete-save behavior are also unmeasured.
These remain independent possible next experiments, without substituting one
passing target for T149's two required targets.

[Snapshot-read samples](windows-parallel-history-diagnostic-20261022.txt),
[executed snapshot script](windows-parallel-history-diagnostic-source-20261022.txt),
[complete-save samples and traces](windows-parallel-history-save-comparison-20261022.txt),
[executed save script](windows-parallel-history-save-comparison-source-20261022.txt).
All diagnostic handles are terminal with exit 0. No broad suite or p95 is rerun
for these source-free experiments. The retained source's full suites and Windows
p95 5.110137800s read / 6.566394800s save remain current. T149 stays unchecked;
host/human/language/release evidence is neither fabricated nor waived.
