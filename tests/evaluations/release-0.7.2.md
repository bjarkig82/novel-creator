# 0.7.2 release evidence

Status: published and verified on 2026-11-11. Qualified archive hashes, public
Windows/Linux installation checks, independent clean installation and the
remote annotated source tag are verified.

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
Completed qualification, public verification, immutable identities and the
source-bound version tag are recorded below.

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

## Publication and public checks

[Publish run 43040427236](https://github.com/bjarkig82/novel-creator/actions/runs/43040427236)
was dispatched once with the exact candidate run/attempt, artifact, source and
hashes above. Immediately before dispatch, PyPI's 0.7.2 JSON endpoint returned
404. The run initially waited for the existing protected `pypi` environment review
by `bjarkig82` (environment `25700067917`). Although the pending-review API reported
that the current user could approve, the integration's approval POST returned
HTTP 403, `Resource not accessible by integration`. This was a GitHub permission
failure, not an automatic approval-review rejection. No protection was changed.

The owner subsequently approved in GitHub and the original publish job
`130590436719` succeeded, completing at 14:44:59 UTC on 2026-11-11. PyPI's wheel
and source archive were uploaded at 14:44:55 and 14:44:56 UTC, respectively. Both
public archive identities exactly match the qualified hashes above.

The initial Linux public check (`130594110413`) failed because the newly uploaded
version was not yet exposed through the PyPI simple index to pip. Windows public
check `130594110507` passed on the first attempt. After index propagation, only
the failed Linux job was rerun: `130595577834` passed at 14:48:19 UTC. The workflow
completed successfully on attempt 2. The already successful upload and Windows
check were carried forward; neither was executed again.

Independent `tests/verify_package_install.py --package novel-creator==0.7.2
--manifest /tmp/novel-072-candidate/manifest.json` verification passed on the
third normal named-package attempt, after two initial pip index-propagation
failures. It downloaded and hashed both public distributions, checked pip's
selected wheel origin/hash, installed clean dependencies, exercised new project
initialization, and passed actual 0.7.1 legacy/notebook upgrade probes. All 94
installed product files matched the upgrade target. No alternate index, product
change, installation-check bypass or repeated upload was used.

## Annotated version tag

The annotated `v0.7.2` tag was created after verified publication and pushed to
origin. Remote tag object `f627a3389ca023d6af4ac2095b5af953215ae886` peels to
qualified source `ecf9bffcd6081c3e764fc81d2f7b717eeedb6d7d`, rather than a later
evidence commit. GitHub's tag API independently confirmed the annotation,
commit object type and target. The annotation is “Novel Creator 0.7.2:
clarification suggestions and custom answers”; its tagger date is
2026-11-11T14:49:41Z. No existing tag was moved or overwritten.

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
