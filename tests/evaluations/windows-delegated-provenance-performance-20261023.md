# Current-source Windows measurement - incomplete save sample

The final delegated-provenance source was measured after both full suites
completed and while the two evaluation tasks were idle. Runtime/test source
was unchanged. This is an ordinary Git layout, no explicit packing or runtime
Git substitution. Model latency is excluded. A temporary private validation
key outside the disposable novel explicitly enables the optional proof cache.

| Measurement | Observed result | Unchanged target |
| --- | --- | --- |
| First fixture read | 3.429102800s | Report separately; no OS cache flush claimed |
| Warm read | 30/30 complete; p95 3.453516100s | <=2s; unmet |
| Warm save | 26 complete; attempt 27 exceeds 30s worker deadline | <=1s; unmet; p95 unavailable |

The timeout reports 31.763974200s wall time; no completed duration or success is
invented for that operation. The remaining save attempts were not run. Completed
save durations span 3.051311500s to 5.842525700s, but these incomplete samples
are not promoted to a p95. Benchmark exit 1 preserves both unmet gates.

Fixture: 100 sessions, 5,000 exchanges, 10,000 active assertions and 26,215,716
JSON bytes. Environment: Windows 11 build 26300, Python 3.13.13, Git
2.53.0.windows.3 at Program Files/Git/cmd/git.EXE, eight logical CPUs and
Intel family 6 model 189. No benchmark worker remained after the harness exit;
the post-run read-only disk observation found 24,492,625,920 free C-drive bytes.
These observations do not attribute the timeout to a specific cause.

Raw data: windows-delegated-provenance-default-30-20261023.json and
windows-delegated-provenance-default-progress-20261023.txt. Product source
fingerprints match the delegated-input-support manifest; storage.py remains
40c7c1ef61af98e9c1e04292d2befc963bd48bbd45196ce8cbf91576f3ee771b.
No threshold, safeguard, deadline, dependency or machine setting was changed.
Earlier differently configured/source-specific timings are historical and do
not establish a causal regression or current compliance. T157 remains open.
