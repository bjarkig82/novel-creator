# Story notebook: 0.4.0 release preparation

**Status: replacement candidate verified; Linux qualification passed; Windows CI and native-host evidence pending; not published.** The published stable release
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
At the final snapshot, Windows CI remained in its full unit suite. The replacement
workflow has not been cancelled and can continue without local monitoring.

Native Windows Codex Desktop notebook acceptance remains unavailable and
unverified. The release cannot proceed to publication until the candidate-bound
Windows host and guide evidence is supplied and the normal protected environment
review is completed. The user was asked for Windows environment access or existing
verification results; none were available during this attempt. Linux Desktop
remains explicitly unverified under the existing scope. No publication was
attempted, and PyPI 0.4.0 is not claimed published.

The first candidate and its failed/cancelled results remain historical. Resume
from this replacement run after the required input is available; inspect its
current Windows result rather than assuming success or rebuilding unnecessarily.
