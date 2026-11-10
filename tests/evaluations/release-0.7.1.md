# 0.7.1 patch release evidence

Status: corrected immutable candidate qualified; protected publication awaits owner approval. Not yet published.
See the [current candidate record](release-0.7.1-candidate.json),
[first candidate record](release-0.7.1-first-candidate.json) and
[release notes](../../docs/releases/0.7.1.md).

## Corrected candidate

- Source: `56ed3de1ba5aa26b6d129a6f767e16e260177c22`, pushed to main.
- [Candidate run 42854055221, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/42854055221/attempts/1).
- Artifact: `13780539173`, `candidate-42854055221-1`.
- ZIP SHA-256: `33433f826747fcbd49b61c3164ad4d9e5df74654a1692a64f954780ccf29cfb0`, verified against GitHub.
- Wheel SHA-256: `cbbd487cee102003160f1966b5748efac73ac9733532744b015abb1f9e6393ba`.
- Source archive SHA-256: `c829fa31229cdcb122f4172a4ec3906ce6ce4517b91cb7dc1318864fdb8fdfd3`.

Manifest identity and archive hashes passed. The new early project-upgrade guard
passed on both Windows and Linux before their full suites began. Every existing
release gate and the conservative Windows selection policy is preserved. The corrected Linux full suite passed 453 tests in 604.141 seconds, 3 skipped,
and all package/install/Bash gates passed. The corrected local full suite passed 453 tests in 1036.417 seconds, 3 skipped.
Full Windows qualification passed all 453 tests in 3639.574 seconds, 0 skipped,
followed by all required wheel/legacy and clean wheel/source installation checks.
The remote verifier passed against the exact completed candidate and required
platform jobs.

## Reviews and first candidate

Requirements and code-quality reviews passed. Overall review found valid CRLF and
tilde metadata fences were rejected, and CRLF routing conversion was treated as a
customization conflict. Those issues were fixed and regression-tested before the
first candidate. Focused checks passed (initial 45 tests, subsequent 19 tests,
coordinator 14 tests), as did isolated wheel/source package probes and historical
legacy update preservation. Structural tests are distinct from native discovery.

The first candidate used source `a51d28969a9f3a7e8cf351b08bb693fe084d811d`,
[run 42843370361](https://github.com/bjarkig82/novel-creator/actions/runs/42843370361),
artifact `13775779042`. Its Linux full suite passed 453 tests in 515.211 seconds,
3 skipped, followed by all required Linux package/install/Bash checks. Its local
full suite passed 453 tests in 1013.606 seconds, 3 skipped. An earlier nonfinal
local attempt was interrupted to fix the metadata issue and is not qualification.

Windows ran all 453 tests in 3579.853 seconds with one failure: the new recovery
test used a POSIX separator string for fault injection, so Windows did not raise
the expected ToolError. This was identified during review before the job ended.
A cancellation request subsequently found the failed run already complete; no
cancellation occurred. That candidate was never published or tagged.

The corrective commit changes the test to native Path.parts matching and adds
an unconditional upgrade check on both platforms before the expensive full suite.
No product runtime code changed in that correction. Independent corrective review
passed, along with 19 focused tests, 13 release-contract tests and the 14-test
upgrade guard. New artifacts and complete qualification are bound to the corrected
source; the failed candidate's successes do not authorize publication.

## Artifact and upgrade coverage

The exact corrected candidate passed independent verification for source bytes,
installed/pinned module origins, context views, new notebook resources, installed
retrofit CLI behavior and historical legacy update/save/reopen journeys. Clean
wheel/source installation and actual published 0.7.0 legacy / 0.6.0 notebook
upgrade probes also passed against the corrected artifacts. Their
current results and exact archive hashes are in the candidate record.

All probes use disposable synthetic projects, never a real novel. The older
published wheels are hash-verified. Notebook cases cover English and Icelandic;
checks preserve project and instruction bytes, history, staged entries and
unstaged writer content. Installed product origins are checked outside the source
checkout. The wheel verifier reuses dependency directories; clean install probes
do not. No scripted exercise establishes native Codex acceptance.

## Protected publication and limits

Protected publication, public artifact/install verification and remote
annotated-tag verification remain pending. The tag must be `v0.7.1` at
`56ed3de1ba5aa26b6d129a6f767e16e260177c22`, never a later evidence commit.

Native Codex Desktop menu discovery, skill invocation and specialist interaction
remain unverified. Structural checks do not establish literary quality, exhaustive
continuity or voice responsiveness. No real novel was changed. Notebook retrofit
is additive and does not stage/commit. Partial additions are preserved for fresh
preview/retry; a partially written conflicting resource requires inspection.


Publication was dispatched once from the corrected source, bound to the exact
candidate, attempt, artifact and hashes above. [Publish run 42865746897](https://github.com/bjarkig82/novel-creator/actions/runs/42865746897)
is waiting for the existing protected pypi environment review by bjarkig82.
The integration approval POST returned HTTP 403, Resource not accessible by
integration. No protection was changed, no upload started and no version tag was
created. User action in GitHub is required before publication can continue.
