# 0.7.2 release evidence

Status: unpublished candidate preparation. No 0.7.2 artifacts have been
qualified or published yet.

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
Results and immutable identities will be recorded after those checks finish.

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
issues. Full release checks remain pending below.

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
