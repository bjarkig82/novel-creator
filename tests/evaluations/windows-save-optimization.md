# Windows save optimization — 2026-10-21

The bilingual fixture changes were committed and pushed to main as `bd9f475`.
This subsequent performance work is local. The one-second Windows save target
has not been met by the diagnostic samples below; it is not relaxed or waived.

## Diagnosis and controlled comparison

[Current full-scale profile](windows-save-current-profile.txt): one profiled save
took 3.625s. The complete worker also prepared its payload outside the save timer.
Git subprocesses, journal reads and the two complete managed-file guards account
for most of the cost. The older 6.771s p95 run is retained, but changes in machine
conditions mean a later absolute timing difference cannot all be attributed to
this optimization.

[Transport experiment](windows-git-transport-experiment.txt) compared the original
pipes, suppressed stderr and temporary-file transports. Three samples per variant
did not show a consistent benefit. No transport change was retained in production.

[Controlled comparison](windows-save-before-after.txt) alternated five old and
five optimized saves in one process and one disposable full-scale repository.
The baseline module came from `bd9f475`; all other code and runtime settings were
shared. Median save time was **3.705116s before and 3.173141s after**, a **14.36%**
reduction. These are diagnostic medians, not the required fresh-process p95.
The fixture is 100 sessions, 5,000 initial exchanges, 10,000 active assertions
and 26,215,716 JSON bytes. Each sample appends one exchange. Diagnostic logs retain
the generator's initial `fully_validated: false` metadata; a successful cold read
validated the chain before measurement. The canonical benchmark reports its own
validation status independently.

## Retained change and safeguards

Within each managed-file guard, shared parent directories are checked once;
every file leaf is still checked and every file's complete bytes are hashed.
The second guard starts with a fresh directory set. Nothing is cached across
saves or treated as valid because size/timestamps match.

The second guard reuses the original commit's immutable tree entries, while
reading the live index and working bytes again. Index cleanup reuses the already
verified candidate tree. This removes two redundant Git tree reads. Recovery
retains its default fresh tree lookup. Both guard passes, source/authority
validation, private candidate index, parent/delta/digest verification, conditional
ref publication, flushes and managed-index cleanup remain in place.

A new real-Git regression changes a committed bundle after candidate construction
while preserving size and timestamp, for both SHA-1 and SHA-256 repositories. The
save must reject it without changing HEAD or the user index. A second regression
replaces a previously checked shared directory with a symlink between guard
passes. The later guard must reject the path; real Windows symlink creation is
unavailable on this host and remains explicitly skipped there.

## Reproduction

Use the same external temporary-directory setup documented in performance.md:

```powershell
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/windows-performance-guard-reuse-30.json
.venv/Scripts/python.exe -B -m unittest discover -v
```

No API, new dependency, background service, permanent story cache, manuscript edit
or acceptance-threshold change is involved. Actual host/human/language evaluation
and physical power-loss durability are separate gates.

## Canonical 30-run result

[Final fresh-process benchmark](windows-performance-guard-reuse-30.json) completes
30 reads and 30 saves on the fully validated representative dataset. Cold read:
3.070803300s. Warm read p95: **1.597038600s**, passing the 2s target. Validation
plus local save p95: **3.845654300s**, failing the unchanged 1s target. The command
exits 1 for that threshold failure; there are no operation errors or timeouts.
[Progress and actual exit-condition output](windows-performance-guard-reuse-progress.txt)
are retained. Python 3.13.13, Git 2.53.0.windows.3, Windows 11 build 10.0.26300
and the existing C: reference hardware/filesystem were used. No new Linux
performance measurement is claimed; the earlier Linux timings remain historical
reference evidence.

The final Linux/WSL2 full suite passes **118 tests in 51.548s, zero skips**,
including both new guard regressions and real symlink replacement/rejection.
See [full Linux log](linux-save-optimization-full-tests.txt). Earlier focused
Windows storage verification passed 26 tests with one explicit privilege skip
(27 total); its log predates the added directory-replacement case and remains
[focused evidence](windows-save-guard-tests.txt).

Final Windows full suite: **118 tests in 303.150s, 116 passed, two explicit
real-symlink privilege skips, zero failures/errors; exit 0**. The two skips
concern the existing path case and the new between-pass replacement case, both
requiring unavailable Windows symlink privilege (1314). Both execute successfully
in the Linux full run. See [full Windows log](windows-save-optimization-full-tests.txt).
Windows used UTF-8, disabled bytecode and the canonical task visualization
directory for TEMP/TMP outside Git repositories, with normal filesystem access
for hard-link publication. Linux used the existing Python 3.12.3 WSL environment,
PYTHONPATH=src and disposable `/tmp` repositories. No dependencies were changed.
`git diff --check` passes. No extension hooks are registered.
