# Allocation and garbage-collection diagnostics — 2026-10-22

T149 investigation. Garbage-collection experiments change no production policy.
The separate path-allocation candidate is retained and described below. Save
safeguards, the benchmark harness, thresholds and novice-evaluation status remain
unchanged. Previous-source results remain documented in
[the overlap report](windows-guard-overlap-20261022.md). T149 remains unmet.

## Garbage collection and benchmark preparation

[Raw diagnostic](windows-save-gc-diagnostic-20261022.txt) uses the complete validated
100-session / 5,000-exchange / 10,000-assertion / 26,215,716-byte synthetic fixture.
It explicitly packs only the disposable repository. Four balanced samples per
variant run in one native Windows Git Bash process. These are diagnostic medians,
not fresh-process p95 results and not directly comparable with the release series.

| Preparation graph retained | Collection policy | Save median seconds |
| --- | --- | ---: |
| Yes | Default | 3.492866000 |
| No | Default | 3.544690750 |
| No | Disabled during save, full collection inside timer | 3.346301000 |
| Yes | Disabled during save, full collection inside timer | 4.242131750 |

All saves completed without cleanup being required. Deferred collection's final
samples varied up to 5.98s. This does not establish a reliable benefit. No
production GC policy is changed: GC state is process-global, while the writer
lock covers one novel, and independent callers could interleave state changes.
The experimental finally block restores the initially enabled/disabled state;
its deferred full collection is included in each reported save duration.

The existing benchmark retains a preparation-only journal while timing save.
The CLI loads a payload and then saves; save independently rereads the complete
authoritative chain. Releasing the preparation graph could be a defensible harness
correction, but this experiment shows no latency improvement. Preparation also
warms caches and allocation state, so releasing it does not recreate a fresh CLI
invocation. No harness change or replacement of previous failed results is made.

Profiles were collected with concurrent work running. Their cumulative times can
overlap and cannot be summed to explain wall time. They suggest repeated path
processing as a candidate for an independent experiment, not proof of a speedup.

The first attempt failed before constructing a fixture because an external script
could not import tests.helpers; the script's repository import path was corrected.
The original [setup error](windows-save-gc-setup-error-20261022.txt) is preserved.

## Reproduction and frozen source

The external script is diagnose_save_gc.py in this chat's writable visualization
folder. It runs through Git for Windows bin/bash.exe with PYTHONPATH=src,
PYTHONUTF8=1 and PYTHONDONTWRITEBYTECODE=1, using the repository .venv Windows
Python. Temporary repositories and the trusted validation-cache key live outside
any real novel. No provider calls or machine settings are involved.

GC-diagnostic baseline storage SHA-256: 16de2fab76922e9252924eada706c7a8d5071875c68e155279192edd749b5828.
Benchmark SHA-256: 7f69593cbee6330af1cb67261f662db8d186cc6d00787d3710d002a8430650f2.
Novice evaluations remain deferred/unverified; no human result is inferred.

## Canonical-path allocation candidate

The [preserved experiment source](windows-path-allocation-experiment-source-20261022.txt)
loads a separate experimental storage module; it does not switch product code
between timed operations. The original source fingerprint is 16de2fab...;
experimental candidate SHA-256 is
7a582f109473c0e9715027854dc59e6aef107cd0ca1c4779d21d1c75934d7219.
The [raw comparison](windows-path-allocation-diagnostic-20261022.txt) records
four samples per variant in ABBA/ABBA order, with the same full validated packed
fixture. The fixture generator graph and preparation-only history are released
consistently for both variants; no collection policy changes. Guard-only median
is 0.726769250s baseline / 0.575608300s candidate (20.8% lower). Whole-save median
is 3.015941150s / 2.446908700s (18.9% lower), with visibly variable samples.
Neither comparison is a p95 result or a causal explanation of differences from
earlier benchmark runs. Every candidate save completed without cleanup required.

The retained implementation factors validation into a string-returning private
helper. The public safe_path wrapper keeps its original explicit keyword-only
signature and returns a Path. check_managed needs only validation and avoids
constructing then discarding a Path for each managed file. The exact canonical
exchange regex guarantees relative, slash-separated components with no traversal,
empty component or control character, so matching names use split('/') directly.
All other inputs retain the former PurePosixPath validation and allowlist path;
non-string inputs follow the former evaluation rather than entering the regex.

Both complete guards still check the live index and fresh filesystem state,
including each leaf mode and directory/symlink checks. Directory metadata is only
shared within an individual guard. Every byte is still hashed with explicit
GIT_WORK_TREE binding. Full authoritative history reading, object hashes,
validation-cache authentication, authority/hold validation, candidate checks,
conditional publication, fsync and recovery are unchanged. The previously
disclosed first-guard overlap race semantics remain unchanged.

An independent read-only review found no safety defect for supported string
paths. The broader public signature and non-string fallback were retained after
review. A new regression matrix exercises canonical accepted names, all setup
allowlist groups and malformed near-misses: dot/traversal/empty components,
absolute paths, backslashes, NUL/newline/CR, case, digit-count and UUID changes.
It passes before optimization and after it; it establishes behavior, not speed.
The initial sandbox run failed only while cleaning its temporary directory;
[the original error](windows-path-allocation-baseline-sandbox-20261022.txt) and
[successful normal-access baseline](windows-path-allocation-baseline-20261022.txt)
are both preserved. Existing byte, index, root-redirection, concurrent guard,
candidate and recovery regressions remain in place.

Final retained storage SHA-256:
69ff00ee3e3a864a458f8c26074e241932911f58c654551afb1b22285eba3035.
This differs from the experimental candidate only in comments, explicit public
signature and preserving the original non-string fallback. The benchmark harness
is unchanged. No persistent caches, dependency, automatic packing or machine Git
selector is introduced. Packing remains explicit disposable-fixture setup.

Replaying the historical experiments requires their pinned baseline, not the
new retained source: [baseline storage bytes](windows-path-allocation-baseline-source-20261022.txt)
(SHA-256 16de2fab76922e9252924eada706c7a8d5071875c68e155279192edd749b5828)
and [GC script](windows-save-gc-experiment-source-20261022.txt) are preserved as
text evidence. Use a disposable source checkout with that baseline at
src/novel_creator/storage.py, then the recorded script and environment. The path
script constructs its experimental module from this baseline; running it against
the retained helper layout is unsupported. Do not replace current working code
to replay a historical measurement.

## Final-source verification and measurement

Final retained-source tests: Windows 126 tests in 373.021s, 124 passed and
two explicit Windows symlink-privilege skips, exit 0; Linux all 126 pass in
82.276s, zero skips, exit 0. The Windows and Linux manifests record the source
fingerprints; Windows before/after hashes match across tests and measurements.

Final-source Windows Git Bash, explicitly packed disposable fixture: first read
3.200534500s, read p95 1.587495700s, validation/local-save p95 3.645534700s.
All 30 reads and 30 saves succeed without timeouts or operation errors. Read
passes its 2s target; save misses its 1s target. Exit 1 records the unmet threshold.
Packing takes 5.748657100s outside operation timers and is fixture preparation,
not product behavior. This configuration does not establish ordinary-layout
performance. Linux performance has not been rerun for this path-allocation source;
previous overlap-source measurements remain historical and source-pinned.

Raw evidence: [Windows full suite](windows-path-allocation-full-tests-20261022.txt),
[Linux full suite](linux-path-allocation-full-tests-20261022.txt),
[30-run samples](windows-path-allocation-packed-30-20261022.json),
[progress](windows-path-allocation-packed-progress-20261022.txt),
[Windows frozen-source manifest](windows-path-allocation-verification-20261022.json) and
[Linux source manifest](linux-path-allocation-verification-20261022.json).

Different source/runtime runs are not matched trials. Their p95 differences
do not establish a causal speedup or regression from this narrow path change.
The limited matched diagnostic supports retaining the smaller allocation work;
the full 30-run result still leaves T149 and release incomplete. No novice, host
or bilingual semantic evidence is invented or waived.

Measured Windows environment: Windows-11-10.0.26300-SP0, Python 3.13.13, git version 2.53.0.windows.3.
Git executable: C:\Program Files\Git\mingw64\bin\git.EXE. Canonical disposable repositories are
on Windows NTFS; read cold means first fixture read, not an OS cache flush.
The temporary external validation key is removed after measurement.
The existing [hardware inventory](windows-performance-hardware-20261022.json)
records the same local machine. Linux verification uses the existing WSL2
Ubuntu environment and canonical /tmp fixtures; no Linux timing claim is made.
