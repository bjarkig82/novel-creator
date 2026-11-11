# 0.7.2 release evidence

Status: qualified unpublished candidate; protected PyPI publication awaits
owner approval. No 0.7.2 artifacts have been published yet.

The release adds suggested answers and custom typed answers to notebook and
legacy clarification. Existing notebooks need a reviewed update that recognizes
the original published 0.7.0/0.7.1 clarification resources and preserves customized
files. Legacy projects retain their supported framework update path.

## Source and focused checks

The initial clarification guidance passed independent requirement, quality and
overall reviews. Before release preparation, five tests passed in
`tests.contract.test_clarify_suggestions` and
`tests.contract.test_legacy_focused_methods`; two targeted notebook initialization
and update tests passed, covering English and Icelandic. `git diff --check`
passed. These checks establish resource contracts, not native host behavior.

Release preparation includes additional updater ownership/preservation tests,
actual previous-release upgrades, complete candidate qualification, clean wheel
and source installation, public verification and an annotated source-bound tag.
Completed qualification results and immutable identities are recorded below;
public verification and the source-bound version tag remain pending publication.

The completed local preflight passed 54 tests in these focused modules:
`tests.contract.test_clarify_suggestions`,
`tests.contract.test_legacy_focused_methods`,
`tests.contract.test_notebook_package_verifier`,
`tests.integration.test_notebook_update` and
`tests.integration.test_notebook_init`. Independent updater review found and
resolved an edit-during-final-HEAD-check race; its regression passed separately.

Both local preflight archives passed clean installation and actual published
0.7.1 project upgrades. Notebook cases covered English/Icelandic original-file
refreshes, links, suggestions, custom directions, story bytes, history and partial
staging. Legacy cases retained pinned runtime origins, save/reopen behavior and
the new clarification files. These are preflight artifacts, not the immutable
CI candidate or publication evidence.

Package-verifier review additionally required binding the prior-upgrade target
wheel to the actual installed controller, including source-install probes that
use the sibling wheel. The verifier now compares all product filenames and
hashes before upgrading. Its updated 13-test contract module passed, the combined
package-verifier/release contract selection passed 22 tests, and the final
installed preflight matched 94 product files before passing both notebook and
legacy prior-release upgrade checks. Independent final review found no remaining
issues. Complete candidate qualification subsequently passed as recorded below.

## Immutable candidate

- Source: `ecf9bffcd6081c3e764fc81d2f7b717eeedb6d7d`, pushed to main.
- [Candidate run 43030156340, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43030156340/attempts/1).
- Artifact: `13858838946`, `candidate-43030156340-1`.
- ZIP SHA-256: `44ad8680cf00eac15ee9be2bb49228689525c32055cf33aa471fc15e317e1db0`, matched GitHub metadata.
- Wheel SHA-256: `8ee343c10bfcc8129d860a8502c669856deaa92f62b5059f915a4027fc11c9f5`.
- Source archive SHA-256: `a4f92f7426c0a0069dcd4814bb749216675080e02568f3e997842957ccfad02d`.

The downloaded manifest identity and both archive hashes passed verification.
All 94 wheel product files matched the committed source exactly. The existing
Windows selection policy required full qualification. Both Windows/Linux early
project-upgrade guards passed 21 tests (Linux 2.942 seconds; Windows 39.302 seconds).
Linux's full suite passed 465 tests in 524.093 seconds, with 3 platform skips.
Windows' full suite passed all 465 tests in 3504.374 seconds, with no skips.

Both platforms passed wheel byte/legacy journey verification, clean wheel
installation and clean installation from the source archive. These installed
artifact checks exercised actual hash-bound public 0.7.1 upgrades of legacy
projects and English/Icelandic notebooks, including the existing clarification
resources, links, story/history/custom-instruction and staging preservation.
The literal Bash getting-started guide also passed on Linux.

The remote release verifier passed against the completed candidate, immutable
artifact, exact source, archive hashes and required successful platform steps.
The [candidate record](release-0.7.2-candidate.json) records those identities and
actual results. These checks are automated package qualification, not native
Codex conversation or menu evidence.

## Protected publication

[Publish run 43040427236](https://github.com/bjarkig82/novel-creator/actions/runs/43040427236)
was dispatched once with the exact candidate run/attempt, artifact, source and
hashes above. Immediately before dispatch, PyPI's 0.7.2 JSON endpoint returned
404. The run is waiting for the existing protected `pypi` environment review by
`bjarkig82` (environment `25700067917`). Although the pending-review API reports
that the current user can approve, the integration's approval POST returned
HTTP 403, `Resource not accessible by integration`. This was a GitHub permission
failure, not an automatic approval-review rejection. No protection was changed.

No upload has started. Owner action in GitHub is required before the normal
publication workflow can proceed. This chat has no browser controls with which
to complete that owner review. Public artifact/hash and named-install checks
remain pending. The annotated `v0.7.2` tag must be created only after verified
publication and must point to `ecf9bffcd6081c3e764fc81d2f7b717eeedb6d7d`,
not a later evidence commit. Never repeat the upload or move an existing tag to
resolve uncertainty; inspect the existing workflow and public package first.

## Previous published release

PyPI metadata observed on 2026-11-11 confirms 0.7.1 was published on 2026-11-10.
Its wheel SHA-256 is
`cbbd487cee102003160f1966b5748efac73ac9733532744b015abb1f9e6393ba`;
its source archive SHA-256 is
`c829fa31229cdcb122f4172a4ec3906ce6ce4517b91cb7dc1318864fdb8fdfd3`.
[Publish run 42865746897](https://github.com/bjarkig82/novel-creator/actions/runs/42865746897)
completed successfully, including Windows/Linux public checks. The earlier 0.7.1
candidate records retain their original preparation-time status.

## Limits

All project probes use disposable synthetic writing. Native Codex skill
discovery, widgets, conversations, literary quality and voice behavior remain
unverified. No real novel or global installation is changed by release work.
