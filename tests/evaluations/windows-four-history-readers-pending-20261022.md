### T149 full-history component profile and four-reader policy (verification pending)

2026-10-22: full-scale save profile attributes about 0.79-0.80s of 1.03-1.08s
history work to Git cat-file reads, 0.14-0.19s to JSON decoding, about 0.015s
to blob hash constructors and about 0.019s to certified index reconstruction.
Per-call tracing has overhead; threaded durations overlap. Eight matched fresh
complete saves on the verified native-metadata source, ABBA/ABBA with two/four
history readers, produce medians 2.544967200s/2.258775650s (11.25% lower).
All byte guards, native leaf queries, six hash partitions, and publication checks
remain. This is diagnostic evidence, not p95 or a portable speedup.

Runtime changes only the bounded large-Windows save-history policy from two to
four. Existing 1024 threshold, serial non-Windows/small histories, two initial
byte readers and four final byte readers remain. Regression policy and fallback
checks now exercise four children and preserve earlier damaged history, guard
error precedence, complete joins under the lock, exact retry and original state.
Default-policy red run fails 2 != 4 before the runtime edit. Focused/full suites
and a fresh required 30-run benchmark must verify this source. T149 remains open;
novice evaluations remain deferred/unverified.

Evidence: tests/evaluations/windows-history-components-20261022.jsonl and
tests/evaluations/windows-native-history-workers-20261022.txt.
