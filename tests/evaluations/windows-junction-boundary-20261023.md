# Windows junction boundary correction — 2026-10-23

Release remains incomplete. This pass repairs an observed storage boundary defect
under the existing path-safety requirements. Existing uncommitted work is retained.

## Defect and correction

Windows directory junctions expose a directory mode through `os.lstat`; checking
only `S_ISLNK` accepts them. Before the correction a real `.git` junction passed
`root_path`, and a `story` junction reached the save path instead of being rejected
at its managed boundary. Mocked file reparse points also passed regular-leaf checks.
The normal-access [red regression](windows-junction-red-20261023.txt) records six
failures across three methods. An earlier sandbox attempt could not create or
clean up its temporary fixtures and is excluded from product results.

The shared lstat mode helper now classifies `FILE_ATTRIBUTE_REPARSE_POINT` as a
redirected path. Managed components reject it with exit code 2; redirected `.git`
directories reject it with exit code 3. This applies to both guard passes, setup
paths and receipt/cache paths that use the shared allowlist. The Windows ordinary
bundle optimization retains its fresh attribute query and uses the corrected
lstat fallback for reparse or special attributes. No metadata result is cached.

Four regression methods cover file/directory attributes under both metadata
policies, real `story` and `.git` junctions, and an exchange-directory junction
inserted after candidate construction. The late-insertion case checks unchanged
branch history and retained pending work. Fixture cleanup removes only junctions
before restoring or deleting disposable directories; it never recurses through a
junction target.

This correction does not claim protection against arbitrary filesystem replacement
between a successful check and subsequent access. The tool's writer lock still
serializes cooperating writers only. No schema, authority rule, byte guard,
candidate verification, compare-and-swap, recovery rule or target is relaxed.

## Verification

The initial focused Windows run passes all 10 path-boundary/native-metadata
methods in 15.117s, before adding the fourth late-insertion regression.
See [focused log](windows-junction-focused-20261023.txt).

Linux/WSL full suite: 155 tests in 69.759s, 152 pass, three explicitly Windows-only
junction methods skipped, zero failures/errors, exit 0. Linux's existing real
symlink tests pass. Command from the checkout:

```bash
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp /home/bjarki/.cache/novel-creator-verification/run.I6IApw/.venv/bin/python -B -m unittest discover -v
```

See [Linux log](linux-junction-full-tests-20261023.txt).
Windows full suite: 155 tests in 503.662s, 153 pass, two explicit real-symlink
privilege skips, zero failures/errors, exit 0. All three physical junction
regressions pass without symlink privileges. Command from the checkout, with
`PYTHONPATH=src`, `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1` and normal filesystem
access to disposable temporary repositories:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -v
```

See [Windows log](windows-junction-full-tests-20261023.txt). Windows uses Python
3.13.13 and Git 2.53.0.windows.3 on Windows 11 build 26300. Linux uses Python
3.12.3 and Git 2.43.0 on WSL2 kernel 6.6.87.2, with Linux `/tmp` fixtures.
The storage and new regression source hashes match their pre-suite fingerprints
after both full suites and both wheel checks. The
[verification manifest](junction-boundary-verification-20261023.json) records
source/artifact hashes and outcomes. Whitespace checks pass.

The updated wheel passes `tests/verify_wheel.py` on Windows and Linux. Both
checks compare all 25 production/resource files to current source bytes, verify
isolated module origins, initialize unknown and supplied Icelandic briefs, save
through the pinned novel runtime, reopen state, inspect recovery and exercise
UTF-8 success/error output under isolated legacy streams. See the
[Windows result](windows-junction-wheel-20261023.json) and
[Linux result](linux-junction-wheel-20261023.json).

Build: the existing bundled Python runtime with setuptools 84.0.0 invokes
`setuptools.build_meta.build_wheel('dist/junction-20261023')` offline. Neither
project verification environment had setuptools installed; those initial offline
pip build attempts are excluded from successful build evidence. The bundled
backend creates the wheel without installing packages or changing dependencies.
See the [build log](junction-wheel-build-20261023.txt). The ignored artifact is
`dist/junction-20261023/novel_creator-0.1.0-py3-none-any.whl`; the earlier wheel is
preserved and neither artifact is published.

Wheel SHA-256: `fbd67c26ec0fff54f1daeb1be7e1bbf33b6ca41b3ad313266a1f967af19e5323`.

Read-only independent code review found no actionable issue in the scoped fix.
It noted preexisting check/access races and late Git-directory replacement as
outside this correction; neither receives a stronger guarantee here.

## Remaining release work

T151–T158 remain open. Genuine novice observations and product-host guidance,
capture/resumption, authority, continuity and bilingual semantic evaluations cannot
be substituted with these deterministic fixtures. The previous Windows save p95
of 2.856806500s remains historical unmet evidence against the unchanged 1s target;
this correction has not remeasured performance. No host, human, semantic parity,
physical-crash durability or release approval is inferred. No provider call,
commit, push or publication is performed.
