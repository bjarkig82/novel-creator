# Story notebook: 0.4.0 release preparation

**Status: corrected candidate verified; Windows and Linux CI qualification running; not published.** The published stable release
remains 0.3.0. Version 0.4.0 is the next minor release because the published
0.3.0 archives cannot be replaced.

The [notebook evidence ledger](agent-story-notebook.md) records Linux structural
checks and the remaining native-host gaps. The integrated local suite passed
with three skips before this release metadata preparation. These results do not
establish Windows Codex Desktop notebook acceptance. New Windows native notebook
acceptance evidence is required before publication; record the actual journeys,
results, scope, provenance and binding to the candidate source and artifact.
Linux Codex Desktop remains unverified under T028 and is not a new mandatory gate.

The existing package-release workflow builds an immutable wheel and source
archive, runs structural checks on Windows and Linux, and requires candidate-bound
host declarations and the protected PyPI environment for publication. Record the
candidate identity, archive hashes and platform results when available. Publish
only the exact qualified candidate, then verify the public named installations and
archive hashes. No tag or PyPI publication is claimed here.

## First immutable candidate — qualification failed

The [candidate workflow](https://github.com/bjarkig82/novel-creator/actions/runs/41927760131) built version 0.4.0 from
source `06c35470ebc4b1c765e02f140cef26b35c52be7b`, attempt 1.
Artifact `13368909938` was independently downloaded through the
GitHub connector after command-line storage redirects returned HTTP 403. Its ZIP
digest matches GitHub metadata; its manifest matches the expected repository,
source, run and attempt, and both distribution hashes were checked.

| Distribution | SHA-256 |
| --- | --- |
| novel_creator-0.4.0-py3-none-any.whl | `0e307a484601b25299246f356047153ac09c929f447861354e6b2f0944152ccc` |
| novel_creator-0.4.0.tar.gz | `3db59e353e0a765f0444be6675f085edf33d7c05bfe7f01a0b1f6325ba1edd4d` |

Linux candidate qualification completed 401 tests with one error and three skips.
The only error was the legacy notebook boundary fixture: it set Git identity
through inherited environment variables, which production Git helpers deliberately
ignore, so the clean CI host had no identity. The Windows job was cancelled after
that failure because this candidate cannot be published. Artifact verification
remains valid, but this run and its archives are ineligible for release.

A test-only correction now isolates a temporary home with explicit-config-only
identity and sets local identity in the disposable repository before initialization.
It reproduced the original failure without a developer identity, then passed 25
focused notebook/legacy checks. Independent review confirmed production safeguards
and all launcher/export assertions remain intact. A fresh immutable candidate is
required after committing that correction; no existing failed run will be treated
as passing.

Successful runner checks do not establish Windows Codex Desktop notebook
acceptance. The release remains blocked on that native evidence and the normal
protected PyPI review.

## Replacement immutable candidate

The [replacement workflow](https://github.com/bjarkig82/novel-creator/actions/runs/41929443036) built the fixture-corrected
source `f0379dd8cdef8062680f33301cea5fe43571b666`, attempt 1, artifact
`13372020036`. Independent verification checks the GitHub ZIP digest,
strict source/run/attempt identity, version and both archive hashes.

| Distribution | SHA-256 |
| --- | --- |
| novel_creator-0.4.0-py3-none-any.whl | `a6a387d328e8534b1d333f377d837e7ff6d7a9303dc593dd92cee60694fa115f` |
| novel_creator-0.4.0.tar.gz | `04f770a9ead9ac09e685cb8ab0194a2e77c987aa6ca367e76c81e0fc86fdca14` |

Linux structural qualification passed, including the full unit suite, wheel
verification, clean wheel and source installations, and literal Bash guide checks.
Windows CI subsequently completed its full suite with 401 tests and one failure:
the proxy forwarding test expected uppercase and lowercase proxy names to retain
different values, which is impossible in a Windows case-insensitive environment.
The failure is recorded in the Windows job linked by the candidate JSON. This
replacement candidate is therefore ineligible for publication despite its valid
archive hashes and passing Linux qualification.

Native Windows Codex Desktop notebook acceptance remains unavailable and
unverified. The release cannot proceed to publication until the candidate-bound
Windows host and guide evidence is supplied and the normal protected environment
review is completed. The user was asked for Windows environment access or existing
verification results; none were available during this attempt. Linux Desktop
remains explicitly unverified under the existing scope. No publication was
attempted, and PyPI 0.4.0 is not claimed published.

The first candidate and this failed replacement remain historical and must not
be published. Use only the corrected candidate identified below after its own
Windows and Linux qualification succeeds; do not resume either failed run.

## Windows proxy regression correction — November 5, 2026

The test now exercises uppercase and lowercase proxy settings in separate real
subprocesses on every platform, retaining a simultaneous distinct-value case on
systems that support case-sensitive environment names. Inherited proxy aliases
are cleared for each case and the host environment is restored afterward.
Production transport and its proxy/certificate allowlist are unchanged; certificate
and filtering checks are retained. Thirteen focused transport/GitHub/CLI/mutation
tests passed locally, and independent review found no material issue. A new
immutable candidate and actual Windows CI validation are required after the fix.
Native Codex Desktop notebook acceptance remains separately unverified.

## Corrected Windows proxy candidate

The [fresh candidate workflow](https://github.com/bjarkig82/novel-creator/actions/runs/41989002817)
built source `a495c0b9a94e4cf982f40317c2a784f0293ac560`, attempt 1, artifact
`13397352646`. Independent verification checked the GitHub ZIP
digest, repository/source/run/attempt/version binding and exact distribution hashes.

| Distribution | SHA-256 |
| --- | --- |
| novel_creator-0.4.0-py3-none-any.whl | `848e9bd71f09d618f7de564454383480330e39953e6587f084348fae63cf08eb` |
| novel_creator-0.4.0.tar.gz | `b687597c4fba1ee1b3f56e148ea3adca892c2b16314dfa4fd227837a2792a90c` |

Linux CI qualification passed. Windows passed all 401 unit tests, including the
proxy regression, but wheel verification then failed because notebook resource
bytes differed from the Windows checkout. This candidate is ineligible for
publication; a corrected candidate must pass its own checks. Actual native Windows
Codex Desktop notebook acceptance remains separately unverified; runner checks
cannot substitute for it. No publication was attempted.

## Windows checkout resource correction

The notebook resource directory was missing from the release-resource LF rules
in `.gitattributes`. A Windows checkout with `core.autocrlf=true` converted its
Markdown bytes to CRLF while the immutable wheel built on Linux retained LF.
The directory now uses the same LF rule as the other packaged resources. Strict
wheel/source byte comparison is unchanged. A real Git checkout regression fails
without the rule and passes with it; all five focused verifier tests pass. An
independent review found no material issue. The corrected source needs a fresh
candidate run; previous failed candidates remain ineligible for publication.
