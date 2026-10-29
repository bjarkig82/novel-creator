# Small-history Windows POC measurement

Fixture: ten sessions, 100 exchanges, 200 active assertions, 1,048,668 JSON bytes.
All 30 warm reads and 30 warm saves complete without failures or timeouts.
First read 0.715602800s; warm read p95 0.579379300s; save p95 1.983323900s.
The read target passes; the unchanged one-second save target remains unmet.
This is small-history responsiveness evidence, not large-fixture compliance.

Reproduce from the configured dependency environment with PYTHONPATH=src:

```powershell
python -B -m tests.performance.benchmark_records --sessions 10 --exchanges 100 --assertions 200 --mib 1 --runs 30 --progress --output tests/evaluations/windows-poc-small-30-20261023.json
```

The run uses the ordinary Git layout and harness-generated private temporary
validation key; no explicit packing, direct-Git override, machine setting,
deadline or safeguard changes. All automated host tasks and test jobs were idle.
No worker remained afterward. Windows 11 build 26300, Python 3.13.13, Git
2.53.0.windows.3 and CPU details are in the raw JSON. Model latency is excluded;
cold means first fixture read, not an OS page-cache flush. The operation timer
uses the unchanged benchmark method, not an end-to-end model-response timer.

Raw samples: windows-poc-small-30-20261023.json; progress:
windows-poc-small-progress-20261023.txt. Runtime source remains byte-identical to
the previous full-suite source, with only POC workflow resources updated. The
broader fixture's timeout and unmet targets remain visible in performance.md.
