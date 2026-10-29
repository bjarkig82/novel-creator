# Independent release verification — 2026-10-22

Release remains incomplete. This pass preserves all existing performance work,
story data, checklist markers and release targets. T143–T150 remain open.

## Observed defect and correction

An isolated installed-wheel run exposed JSON written with Windows-1252 instead
of UTF-8. Other Unicode characters can make both success and error output fail
with UnicodeEncodeError. The CLI now configures stdout and stderr as UTF-8 at
entry, including installed novel launchers. Embedded text streams without
reconfigure remain supported. No record or transaction behavior changed.

The installed-launcher regression forces ASCII and Windows-1252, disables
Python UTF-8 mode, and verifies success and unavailable-record errors containing
Icelandic, Japanese and an emoji. Before the fix all four cases fail; after the
fix the regression plus existing CLI/portable-install tests pass: 11 tests in
44.697s, zero skips. [Red log](cli-utf8-red-20261022.txt),
[green log](cli-utf8-green-20261022.txt).

## Built distribution

Build command: `.venv/Scripts/python.exe -m pip wheel . --no-deps --wheel-dir dist --disable-pip-version-check`.
Artifact: `dist/novel_creator-0.1.0-py3-none-any.whl`, SHA-256
`9d65691505d0bc102f1ce47dc82df199ee193fb2fb5052aa3c70a23bcbab6880`.
The wheel is a local ignored build output; it was not published.

`python tests/verify_wheel.py dist/novel_creator-0.1.0-py3-none-any.whl`
passes on Windows and Linux/WSL. It checks 25 production/resource source files
against wheel bytes, installs the wheel with pip into a disposable environment,
checks imported product module locations, invokes the installed console command,
and initializes both an unknown brief and a supplied Icelandic brief. The pinned
novel launcher validates, inspects, lists sessions, reports saved recovery state,
saves a prepared Unicode exchange, and reopens the confirmed checkpoint.
Isolated child interpreters force ASCII stdout/stderr for successful reads and
Unicode unavailable-record errors. Prepared exchanges are structural evidence.

The verifier reuses the calling environment's package directories, including pip,
without executing that environment's editable-install .pth files. Every loaded
product module in the distribution probe must come from the disposable installed
wheel, and the save probe checks the pinned novel module location. This does not
establish a clean download/resolution test of the dependency lock.

[Windows result](windows-wheel-verification-20261022.json),
[Linux result](linux-wheel-verification-20261022.json),
[reusable verifier](../verify_wheel.py).
An initial Linux attempt could not seed pip because ensurepip was absent. The
final verifier creates an unseeded environment and reuses existing pip; no system
package was installed. Earlier harness attempts are excluded from product results.

## Regression and tooling verification

Linux/WSL: 151 tests in 60.432s, all pass, zero skips.
Command: `PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp /home/bjarki/.cache/novel-creator-verification/run.I6IApw/.venv/bin/python -B -m unittest discover -v`.
[Full log](linux-cli-utf8-full-tests-20261022.txt).

Windows: 151 tests in 514.344s, 149 pass, two explicit real-symlink privilege
skips, zero failures/errors, exit 0. Command: `.venv/Scripts/python.exe -B -m unittest discover -v`,
with `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=src`, using normal
filesystem access for disposable Git publication.
[Full log](windows-cli-utf8-full-tests-20261022.txt).
Linux's corresponding full-suite exit code is also 0. The CLI production source
and regression test were unchanged throughout these final suites. The standalone
wheel verifier was subsequently strengthened and rerun on both platforms.
Earlier pre-fix full runs passed 150 tests on each platform; they are superseded
for this change by the final 151-test runs above.

Spec Kit Bash smoke checks pass on Git Bash and Linux/WSL using existing local
jq binaries. Linux's initial PATH lacked jq; the successful run includes
`/home/bjarki/.cache/novel-creator-verification/run.I6IApw` in PATH. No binary was
downloaded for these smoke checks.
[Git Bash log](bash-independent-release-smoke-20261022.txt),
[Linux log](linux-independent-release-smoke-20261022.txt).
The requirements checklist remains 16/16 satisfied for specification quality;
no marker was changed. No extension hooks are configured.

Read-only independent review found no blocking correctness issue. Its suggested
portable isolated legacy-stream check was incorporated in the wheel verifier.

## Remaining boundaries

No new performance measurement was made. The previously recorded Windows save
p95 of 2.856806500s still exceeds the unchanged 1s target; its read p95 is
1.183358100s against 2s. Those measurements describe the earlier source-specific
performance run, not a benchmark of this CLI fix.

Genuine novice observations, product-host creative guidance/capture/resumption,
authority/continuity judgments, bilingual semantic outcomes and dependent final
release review remain incomplete. The existing capture capability gate remains
scoped to its recorded host. No synthetic exchange substitutes for those results.
Physical crash durability, voice and additional hosts receive no new claim;
macOS remains deferred. No commit, push, provider call or publication was made.
