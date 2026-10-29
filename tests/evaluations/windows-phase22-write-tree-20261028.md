# T172 private-candidate tree investigation — 2026-10-28

T172 and dependent T173 remain open. No production, benchmark, dependency or
safeguard change is retained. Existing dirty work and rejected experiments are
preserved. This investigation targets a distinct measured stage rather than
repeating reduced-reader, deferred-guard, parser, native-binding, metadata-thread,
GIL, launcher, packing, queued-protocol or byte-hash cache experiments.

## Measured hypothesis

The existing [save-stage profile](windows-phase22-performance-20261028.md) records
private-candidate `write-tree` at 0.196035300s and 0.348039900s. The new hypothesis
is that command-local Git for Windows `core.fscache=true` could reduce repeated
filesystem work during that command while keeping normal object-existence
checks. The historical fscache experiment concerned the byte-hash guard, not
private tree construction.

Git for Windows documents its [filesystem cache](https://gitforwindows.org/diagnosing-performance-issues.html).
The shell sees system `core.fscache=true`, but the runtime's existing
`GIT_CONFIG_NOSYSTEM=1` environment excludes system settings; its effective
disposable-repository query returns unset (exit 1). Only the diagnostic candidate's
`write-tree` receives `-c core.fscache=true`. No persistent configuration changes.

## Full-scale diagnostics and result

Eight fresh-worker saves use balanced ABBA/ABBA order on a fully validated
ordinary-layout fixture: 100 sessions, 5,000 exchanges, 10,000 active assertions,
26,215,716 JSON bytes. No packing/maintenance is requested. The optional private
validation key is temporary and outside the disposable novel. The same-day
[hardware inventory](windows-phase22-hardware-20261028.json) identifies the Lenovo
Core Ultra 7 268V laptop, eight logical CPUs, NTFS C:. Windows 11 build 26300,
Python 3.13.13 and `C:/Program Files/Git/cmd/git.EXE` 2.53.0.windows.3 remain the
recorded environment. UTF-8 and disabled bytecode are process-local; normal
filesystem access permits disposable temporary keys and hard-link publication.

| Four-sample median | Control | Command-local cache option |
|---|---:|---:|
| Complete save, seconds | 5.589910350 | 6.019328800 |
| `write-tree` wall time, seconds | 0.440671700 | 0.503973800 |
| Internal `cache_tree` update, seconds | 0.219981000 | 0.267330000 |

All eight saves succeed, with two complete guards and verified counts of all
bulk hashes/history objects. Save timers include normal history validation,
private candidate verification, fresh branch/CAS, receipts, fsync and cleanup;
payload preparation/imports remain excluded. Each worker has a 30-second
deadline. Every tree trace records a successful exit and three hardware flushes.
Git index-read/write regions are small relative to the tree-update region.

Both variants enable Git Trace2 performance output for `write-tree`. Trace output
includes process-ancestry collection and other overhead; these samples must not
replace the existing untraced 30-run p95s. Ambient activity and instrumentation
are uncontrolled, and differences from previous runs do not establish a source
regression. Four samples per variant do not establish p95 or portable speedups.

[Executed full-scale runner](phase22-write-tree-20261028.py),
[all raw samples and source hashes](windows-phase22-write-tree-20261028.jsonl).
Eight individual trace files are named in the samples and verification manifest.

## Activation check: ineffective option, not a causal slowdown

A separate small disposable-repository check uses `GIT_TRACE_FSCACHE` with the
same command-local option. `write-tree` emits no cache-activation trace; `status`
emits activation/deactivation and request counters, proving the instrumentation
works on this installed Git version. Thus the measured option does not activate
the proposed cache during tree construction. The higher sample medians are not
evidence that active caching slows `write-tree`.

This agrees with the inspected version-pinned
[`write-tree` command path](https://github.com/git-for-windows/git/blob/v2.53.0.windows.3/builtin/write-tree.c)
and the separately enabled
[cache implementation](https://github.com/git-for-windows/git/blob/v2.53.0.windows.3/compat/win32/fscache.c).
The [tree-update implementation](https://github.com/git-for-windows/git/blob/v2.53.0.windows.3/cache-tree.c)
places object/tree construction inside the measured update region; the trace
does not isolate each individual object lookup, compression or durable write.

[Activation check source](phase22-tree-cache-activation-20261028.py),
[result and positive control](windows-phase22-fscache-activation-20261028.json),
[positive-control raw trace](windows-phase22-fscache-activation-status-20261028.txt).
Both diagnostic processes exit 0 with empty stderr. Do not repeat this option
experiment for the same command/version as though it enabled a cache.

## Safeguards and qualification

Four preliminary cases verify that ordinary `write-tree` and the command-local
option both reject a deliberately unavailable object in SHA-1 and SHA-256
private indexes (exit 128). The full-scale wrapper asserts the candidate index,
unmodified `write-tree` arguments apart from the local option, two complete
guards, explicit real-root binding for byte hashing and complete object counts.
No checks move or disappear. In particular, `--missing-ok` is not tested or
adopted as an optimization: it disables the normal referenced-object existence
check, as the [official command documentation](https://git-scm.com/docs/git-write-tree)
states. All root/path/reparse/live-index guards, actual blob hashes, authority,
cache, worker/lock lifetime, candidate checks, publication and recovery remain.

The [reproducible verifier](verify-phase22-write-tree-20261028.py), exit 0,
checks exact fixture size/order, all eight save sequences, object/hash/guard
counts, missing-object cases, trace durations/flushes, medians, activation control
and unchanged production/benchmark source hashes. Its
[output and artifact hashes](windows-phase22-write-tree-verification-20261028.json)
preserve the result. No runtime/resource/test edit invalidates previous
source-specific platform or independent-wheel evidence; broad suites and builds
are not repeated for diagnostic-only files.

No promising candidate remains from this hypothesis, so no new candidate
30-read/30-save qualification is claimed. The existing ordinary-layout benchmark
remains read p95 1.028736700s (<=2s passes), save p95 3.067419500s (<=1s unmet).
Its full raw-sample arithmetic is reverified separately by the unchanged
save-investigation verifier. T173's release assessment remains provisional.
Further tree optimization must preserve referenced-object existence validation
and durable tree writes; this trace does not justify bypassing either.
