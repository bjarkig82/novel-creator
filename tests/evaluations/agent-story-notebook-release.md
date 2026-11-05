# Story notebook: 0.4.0 release preparation

**Status: automated-only replacement candidate built and independently verified; Windows/Linux qualification running; not published.** The published stable release
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

## Successful LF-corrected candidate — November 5, 2026

[Candidate qualification](https://github.com/bjarkig82/novel-creator/actions/runs/42002561962)
completed successfully for source `dc5dd1b36341b92144ad40f32cfc6cba72971659`,
attempt 1. The independently downloaded artifact `13402977775` matched its GitHub
ZIP digest, manifest identity and both distribution hashes. Exact bindings and
results are retained in `agent-story-notebook-040-lf-candidate.json`.

Windows passed 402 tests without skips, strict wheel byte verification and clean
wheel and source-distribution installation checks. Linux passed 402 tests with
three skips, the same package checks and the literal Bash getting-started guide.
The workflow and both platform jobs were independently confirmed successful.

This supersedes the failed structural candidates above. Native Windows Codex
Desktop notebook acceptance remains unverified and publication was not attempted.
The successful runner checks do not replace that protected release requirement.


## Outline and adaptive brainstorming release preparation — November 5, 2026

Release notes now compare the complete 0.4.0 candidate with published 0.3.0,
including new notebooks, explicit outlines, adaptive brainstorming, legacy
compatibility and the post-publication pinned installation command. The successful
LF-corrected candidate above predates these added resources and cannot qualify
this release source. A new immutable candidate is required after committing this
preparation. Native Windows notebook acceptance is still unavailable; no old host
evidence is carried forward or represented as candidate-bound. Publication remains
unattempted and blocked on actual native acceptance and the protected PyPI review.


## Immutable outline and adaptive brainstorming candidate

[Candidate qualification](https://github.com/bjarkig82/novel-creator/actions/runs/42042388364)
built source `2f625d799b0ec397340b1a2743ab3454256d7af6`, attempt 1, artifact
`13424285380`. The artifact was independently downloaded through the GitHub
connector. Its ZIP SHA-256 matches GitHub metadata:
`5d43198bfc788a3e7f43b23d392e88e1508abacbd9f79e0e5ece1bb28a11d172`.
Manifest verification checked repository, full source commit, run, attempt,
distribution/version and both exact archive hashes.

| Distribution | SHA-256 |
| --- | --- |
| novel_creator-0.4.0-py3-none-any.whl | `85afd9150b6f862a9d4df977bfaad67c76c7cb83e4ad90371c3bd8d630330ad3` |
| novel_creator-0.4.0.tar.gz | `3db59346732c10703895b4f954482c79a19ec8bba04da6438388ae934e33bcb3` |

Windows and Linux qualification are running. Exact bindings and current results
are retained in [candidate evidence](agent-story-notebook-040-brainstorming-candidate.json).
Native Windows Codex Desktop notebook acceptance and the literal Windows guide
journey remain unverified. Linux Desktop stays explicitly unverified. A Windows
evaluator must use this exact candidate, record actual journeys and outcomes with
traceable HTTPS evidence, and retain the candidate source/run/attempt/artifact and
archive hashes. See the [native acceptance coverage](agent-story-notebook.md#acceptance-coverage)
and [brainstorming scenarios](brainstorming.md); include explicit outline behavior,
English/Icelandic notes, interruptions and honest persistence failures. Runner
checks alone cannot establish these conversational outcomes. No publish workflow
has been dispatched. Protected PyPI environment review remains required after
all actual evidence is available.


## Owner-approved automated-only qualification — November 5, 2026

The owner explicitly chose publication after automated checks pass, with native
Windows notebook behavior clearly documented as unverified. This supersedes the
manual native-acceptance publication requirement recorded above; it does not mark
any native conversation or Windows literal guide journey passed. Both Windows and
Linux Desktop remain unverified. The release verifier now requires explicit false
native-host declarations and queries actual successful candidate-bound Windows and
Linux jobs and required steps. Immutable source/run/attempt/artifact/hash checks,
full platform suites, wheel/source installations, Linux literal guide and protected
PyPI review remain mandatory. Windows automated CLI coverage retains its actual
scope. See the [publication contract](../../docs/testing-and-completion-guide.md#automated-package-publication-contract).

The prior brainstorming candidate above does not contain this contract change and
must not be published with invented host declarations. A fresh immutable candidate
will be built after the reviewed workflow/verifier change is committed. Historical
candidate and native-evidence records remain intact.


## Automated-only immutable candidate

The superseded brainstorming candidate was cancelled before qualification finished;
it remains historical and must not be published. The reviewed automated-only
contract is now included in [replacement candidate qualification](https://github.com/bjarkig82/novel-creator/actions/runs/42044371273),
source `abaca5ff90ce1adc90274e5515209a87bf6c58f7`, attempt 1, artifact
`13423358339`. Independent connector download verified its GitHub ZIP digest
`26ad6d07f7ff56c7b307d6e3e484b6dfa19bda14f6421c1ca73c5ca2ac2d69ab`,
strict manifest identity, version 0.4.0 and both archive hashes:

| Distribution | SHA-256 |
| --- | --- |
| novel_creator-0.4.0-py3-none-any.whl | `1e6d7db9fd9b2356563afaa776625d90a41bc909786a52d517a1566d40115bb3` |
| novel_creator-0.4.0.tar.gz | `8025ff396c9a9d1c547603ccd3819ee3076e855b434eb3cf2d5534eb78708713` |

Both platform jobs are running full automated qualification. Current exact results
are retained in [automated candidate evidence](agent-story-notebook-040-automated-candidate.json).
Native Windows/Linux Desktop behavior and the Windows literal PowerShell guide
remain unverified. Publication has not been attempted; successful complete automated
qualification and the existing protected PyPI review are still required.
