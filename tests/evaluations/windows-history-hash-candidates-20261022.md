# Full-history reconstruction and parallel byte-hash candidates

T149 continuation, 2026-10-22. These are external experiments against unchanged
storage source `47c6eac0122d1076a91f21caeb253bf6721678f4e626fc0630ab069557e55304`.
No runtime, test, benchmark, cache, dependency or transaction policy is changed.
Novice evaluations remain deferred/unverified. T149 remains unchecked.

## Certified history index reconstruction: reject

Unrolling the existing certified-record index updates produced equal private
indices and retained owned-record identity across the fully validated fixture.
Four balanced samples per variant, with default garbage collection, measured
median reconstruction time of 0.019371750s versus 0.009222550s. This excludes
JSON decoding, Git reads and complete saves. The approximately 10ms absolute
gain does not justify changing this trusted-history path.

[Raw samples](windows-certified-indexes-diagnostic-20261022.txt),
[executed source](windows-certified-indexes-source-20261022.txt).

## Parallel full-byte hashes: candidate only

The experiment copies the current complete guard and changes only its content
hash phase. Every path/parent/leaf/mode and captured live-index check finishes
before any hash worker starts. Contiguous partitions cover every validated
managed path exactly once. Each worker uses the existing Git wrapper with
`hash-object --no-filters --stdin-paths`, identical C quoting and explicit
`GIT_WORK_TREE` root binding. No object is written. Futures are consumed in
original partition order; all workers join on success or failure. All process
statuses and output counts must succeed before any OID comparison.

This changes sampling order within the existing non-atomic content-read phase.
It does not provide an atomic filesystem snapshot or alter the separate
metadata-before-content phase boundary. Adoption would require production
publication-race, error-path and portability regressions, a justified small-
fixture/platform policy and fresh final-source suite and p95 measurements.

Guard-only medians, four balanced samples per variant:

| Hash processes | Complete guard median (s) |
| --- | ---: |
| Serial | 0.804349400 |
| Two | 0.491227500 |
| Four | 0.399464650 |

[Guard samples](windows-parallel-hashes-diagnostic-20261022.txt),
[executed source](windows-parallel-hashes-source-20261022.txt).

The complete-save comparison keeps the first guard serial while it overlaps
history reads. Only the final guard uses parallel hashes. It uses native Windows
Git Bash, a disposable explicitly packed fixture, and the existing optional
trusted cache setup. All 100 sessions, 5,000 exchanges, 10,000 assertions and
26,215,716 JSON bytes are validated before measurement. This configuration is
distinct from the ordinary-layout PowerShell release benchmark. Payload
preparation is outside each save timer; full authoritative-history reading and
validation inside save remain included. Twelve sequential saves use the balanced
order `[serial, two, four, four, two, serial]` twice, four samples per variant.

| Final-guard hash processes | Complete save median (s) | Git calls/save |
| --- | ---: | ---: |
| Serial | 3.245158150 | 22 |
| Two | 3.005366000 | 23 |
| Four | 2.469268600 | 25 |

All 12 saves succeed at sequences 5001–5012 without cleanup requirements. The
four-worker median is about 23.9% lower in this small comparison. Individual
timings vary; this is a promising candidate, not a p95 result or a precise causal
effect estimate. Extra processes are explicitly counted. No safeguard is removed.

[Save samples and command traces](windows-parallel-hash-saves-diagnostic-20261022.txt),
[executed source](windows-parallel-hash-saves-source-20261022.txt).

Isolated guard checks pass for SHA-1 and SHA-256: exact managed path coverage,
explicit root binding, incomplete-output and process-failure precedence over an
earlier content conflict, worker joining, and unsafe-leaf rejection before any
hash process starts. These are candidate checks, not production save regression
coverage. The first check runner mistakenly had only one managed file and could
not inject a second-partition failure; its failed assertion is retained. The
corrected runner explicitly commits eight additional guard-only byte fixtures
and tests all nine managed files. These small byte fixtures are not represented
as semantically valid history or performance-scale fixtures.

[Initial runner failure](windows-parallel-hash-candidate-checks-20261022.txt),
[corrected passing checks](windows-parallel-hash-candidate-checks-final-20261022.txt),
[corrected source](windows-parallel-hash-candidate-checks-source-20261022.txt).

The [evidence manifest](windows-parallel-hash-diagnostics-manifest-20261022.json)
records unchanged source fingerprints, raw/script SHA-256 hashes, independently
recomputed medians, sample counts and Git command-count assertions. All diagnostic
processes exited; the corrected checks and comparisons exit 0. No broad suite or
p95 is rerun for these source-free experiments. The previous verified source's
[129-test suites and ordinary-layout p95 failures](windows-ref-query-20261022.md)
remain the current production evidence: read 5.106631200s and save 3.612526000s.
The 2s/1s targets and all remaining human/host/language/release gates stay open.
