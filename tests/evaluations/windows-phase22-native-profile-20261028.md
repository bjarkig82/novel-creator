# T172 isolated native Git instrumentation — 2026-10-28

The matching-source Windows Git builds and native counters work. Sixteen guarded
full-scale saves complete, including four instrumented native tree updates.
Stable low-load timings remain unavailable: every instrumented command window
exceeds the selected CPU threshold, and a stricter follow-up fails its preflight
load gate without creating a new fixture. No optimization or performance pass
is claimed. Production runtime, installed Git and all save safeguards remain
unchanged; T172 and dependent T173 remain open.

## Pinned, isolated builds

The installed release tag v2.53.0.windows.3 resolves to upstream commit
`f8165afd89b0c190677a093f20894f5fce12f97a` (annotated tag object
`519fd13b0a97e5dc114b98a3092c0c37b1f111d0`). Its shallow checkout and all build
outputs live under ignored `.tools/t172-git-native-20261028/`. No source checkout,
novel, executable, package, PATH or Git setting is installed or changed globally.

The existing Visual Studio 2026 compiler is MSVC 19.51.36257.0, x64, with Windows
SDK 10.0.26100.0. Portable CMake 4.4.4 is downloaded from its
[official release](https://github.com/Kitware/CMake/releases/tag/v4.4.4) and checked
against the publisher's SHA-256 list:
`bace36e94b31c68ab6fa295f26dfa11219e0701cf7c94b0284a7d1cb13dac536`.
The isolated zlib 1.3.1 source archive from
[upstream](https://github.com/madler/zlib/tree/v1.3.1) has recorded SHA-256
`50b24b47bf19e1f35d2a21ff36d2a366638cdf958219a66f30ce0861201760e6`.
It is built locally and linked statically; project dependencies do not change.

The upstream CMake build uses Release mode with vcpkg bootstrap disabled.
Optional curl, expat, iconv and translations are excluded. This preserves the
local tree-command paths required by the diagnostic, but is not a binary-identical
rebuild of the installed distribution. Compiler, optional-feature and library
differences prevent substituting these timings for installed-Git qualification.

The first configure attempt fails because Windows sort precedes shell sort and
an upstream dashed-link option produces an empty CMake output list. Its
[failure log](windows-phase22-native-git-baseline-build-20261028.txt) is preserved.
A fresh build directory, process-local tool ordering and the ordinary dashed-link
option produce the [successful unmodified build](windows-phase22-native-git-baseline-build-v2-20261028.txt).
That executable is preserved as `baseline/git.exe` before instrumentation.
The [instrumented rebuild](windows-phase22-native-git-profile-build-20261028.txt)
also succeeds. Compilation warnings are retained in the logs.

[Configure/build command source](windows-phase22-native-git-configure-source-20261028.txt),
[incremental rebuild command source](windows-phase22-native-git-rebuild-source-20261028.txt),
[portable-tool identity](windows-phase22-native-git-portable-tools-20261028.json).
The command files are intended to be saved in the diagnostic root, where their
relative paths resolve. The unmodified checkout must be built/preserved before
running the instrumentation preparation script.

## Native instrumentation and correctness

The opt-in `GIT_T172_PROFILE=1` instrumentation activates only in the thread
executing `cache_tree_update`. It records native wall-clock time for object
existence calls, tree-buffer assembly, object writing, deflate calls and flushes.
A thread-local nesting stack records inclusive and exclusive totals; nested
compression and flush time is excluded from the object-write remainder. The
remainder still includes hashing, setup, file I/O, close/rename and other object
write work. Uninstrumented traversal/bookkeeping remains outside these categories.

Original function bodies, arguments, calls, return values, failure paths and
errno are preserved. The same ordinary object-existence checks and durable
writes execute. Instrumentation adds measurement overhead: counters report 1,000
empty clock pairs as a calibration observation, not a correction to subtract.
Timers include preemption; they are not CPU-time measurements. One summary is
written to stderr after the measured region, with no per-file story output.

[Preparation/replay script](prepare-phase22-native-profile-20261028.py),
[tracked-source patch](windows-phase22-native-git-instrumentation-20261028.patch),
[new diagnostic header](windows-phase22-native-git-header-20261028.txt),
[before/after source hashes](windows-phase22-native-git-instrumentation-20261028.json).
The preparation script creates the header as well as applying tracked-source
changes; the patch alone omits the new header.

Installed Git, the unmodified MSVC build, instrumented build with timers off and
instrumented build with timers on produce identical tree OIDs in SHA-1 and
SHA-256 fixtures with Unicode paths. All eight format/variant combinations reject
a deliberately missing object with exit 128. These are scoped equivalence and
failure checks, not general Git-release or physical power-loss qualification.

## Full-scale execution and load

The fully validated ordinary-layout fixture has 100 sessions, 5,000 exchanges,
10,000 active assertions and 26,215,716 JSON bytes. No packing/maintenance is
requested. The optional private validation key is temporary and outside the
disposable novel. Sixteen fresh-worker saves use symmetric order twice, four
samples per installed/baseline/profile-off/profile-on variant. Only the private
candidate's normal `write-tree` selects a diagnostic executable; every other
Git call uses installed Git. No PATH selector is introduced.

All saves retain full history/object hashes, two complete root/path/reparse/type/
live-index/byte guards, private candidate verification, fresh branch/CAS, receipts,
fsync, cache, cleanup/recovery and original worker/lock lifetimes. For saved
sequence N, each verifies two guards and 2*N bulk file hashes/batch objects.
Every worker retains a 30-second deadline. All sixteen complete without timeout,
operation error or cleanup warning. Source and executable hashes match before
and after the run.

After fixture preparation, measurement waits for three five-second samples at
<=40% CPU and >=2 GiB available physical memory. This initial gate passes after
eight samples. Per-command CPU sampling uses documented
[GetSystemTimes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getsystemtimes)
semantics; kernel time includes idle time. All raw load windows remain recorded.
The four instrumented command windows subsequently measure 70.83–100% CPU, so
none meets the quiet-window criterion. Available memory also falls below the
threshold later. The gate cannot guarantee conditions remain quiet afterward.

## Direct native observations, under these limits

| Exclusive category | Median (ms) | Range (ms) |
|---|---:|---:|
| Object existence lookups | 6.72455 | 2.6770–15.6324 |
| Tree buffer assembly | 1.28755 | 1.0262–5.5666 |
| Object-write remainder | 12.92005 | 10.6206–31.5303 |
| Deflate | 7.67705 | 6.7276–13.0967 |
| Flush calls | 9.73975 | 5.0870–16.3791 |

The complete native tree-update region is 29.4009–80.6564ms, median 38.65915ms.
The separately summarized medians must not be added to reconstruct a median
sample. Per-sample exclusive totals and nesting arithmetic are independently
checked. The four profiles count N+5 object lookups, N+4 buffer assemblies,
three object writes, 72 deflate calls and three flushes each.

These are direct subcall timings in the pinned-source MSVC build, rather than
the earlier independent Python/component probes. They do not establish stable
installed-distribution costs, instrumentation overhead or a causal speedup among
variants. The absolute tree region remains small relative to these multi-second
instrumented saves; no universal lower bound or justification for skipping checks
or durability follows. All variant timings and CPU/memory windows remain raw.

[Primary runner](phase22-native-profile-20261028.py),
[complete primary observations](windows-phase22-native-profile-20261028.jsonl).

## Stricter follow-up and qualification

A [separate follow-up runner](phase22-native-profile-settled-20261028.py) requires
quiet conditions before fixture creation and again before each tree command.
Its preflight fails over twelve five-second samples, with 92.01–100% CPU.
Available memory varies and falls below 1 GiB in later samples. It records
[not_measured](windows-phase22-native-profile-settled-20261028.jsonl), creates no
new fixture and supplies no new timings. No user applications, machine power or
security settings are changed to force a result. Had it run, waits would remain
inside diagnostic save time and its 120-second worker limit would be explicitly
separate from qualification; neither would replace the 30-second benchmark policy.

The [independent verifier](verify-phase22-native-profile-20261028.py), exit 0,
checks pinned source identity against Git objects, baseline/instrumented/current
executable hashes, all guarded save counts/sequences, eight correctness cases,
the initial gate, category/nesting arithmetic and the follow-up non-measurement.
[Verification output and artifact hashes](windows-phase22-native-profile-verification-20261028.json).
Primary execution exits 0 with empty stderr. Follow-up stderr is empty; its
quiet-gate stop is not a product-save failure or a passing measurement.

No product/runtime/resource/benchmark change invalidates prior source-specific
Windows/Linux tests or independent wheel evidence. No new broad suite or wheel
build is claimed. The unchanged ordinary-layout 30-run qualification remains
read p95 1.028736700s (<=2s passes), save p95 3.067419500s (<=1s unmet).
No new 30-run candidate benchmark is justified by a diagnostic build or noisy
timings alone. T172/T173 remain unchecked; stable low-load native measurements
and a justified production optimization remain outstanding.
