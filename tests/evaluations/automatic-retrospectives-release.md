# Automatic retrospectives: 0.2.0 release

The maintainer authorized merging the completed feature to main and publishing a
PyPI update on 2026-11-03. Target version: **0.2.0**. Publication is pending until
the protected workflow completes and public archive hashes are verified.

The release includes the completed default-off retrospective feature and the
reviewed documentation correction from draft PR #2. The earlier synthetic
transport-smoke PR remains separate. The feature's 68 tasks and independent
zero-finding convergence are recorded in its qualification matrix and ledger.

The existing protected workflow builds an immutable wheel/sdist artifact, runs
Windows and Linux validation, and publishes only the selected successful artifact
without rebuilding. Release checks use the documented UTF-8 Python environment,
including child interpreters. Candidate checks also cover clean sdist installation
and the literal Bash getting-started guide.

The version and installation documentation change for this release. Native-host
evidence is reused only for unchanged behavior/components; it is not represented
as a new conversation against the release archives. Exact candidate archive,
source/resource, installation and workflow identities will be recorded below.
Linux Codex integration remains unverified. Existing novels retain their pinned
bundles and participation stays disabled until explicit contributor opt-in.

Historical failures, partials, earlier candidate identities and private local
evidence are preserved. Private filesystem prefixes in the new public ledger are
replaced with repository-relative paths; the original ledger remains local.

## Candidate identity and verified scope

Candidate [run 41697714816](https://github.com/bjarkig82/novel-creator/actions/runs/41697714816),
attempt 1, artifact **13262337033**, source
`7334f5867d462911084693dbaf61841dc0601ac8` contains exactly:

| Archive | SHA-256 |
| --- | --- |
| `novel_creator-0.2.0-py3-none-any.whl` | `9872b3aa9a4a1629d4b6c50a1672f5acbd376130f08f9c7edcd0492381c632fa` |
| `novel_creator-0.2.0.tar.gz` | `aec018f3b7e5156971f313b33b02bde78cee425dd13a13f4259da5c5edab4703` |

All 31 candidate code/resource entries match the downloaded wheel. Against the
native-qualified candidate, 29 are byte-identical; the other two change only the
package version and getting-started release target/link from 0.1.0 to 0.2.0.
[Exact resource binding](automatic-retrospectives-release-source.json) records
both identities and the scope of native evidence reuse. No new native chat or
saved/displayed response is claimed for these release archives.

Local Windows verification passed the 13 focused package/bundle tests, exact
wheel resources and isolated pinned save/reopen checks, clean installation with
independent dependencies, and the documented setup/inspection/optional Icelandic
settings/default-off walkthrough plus all six troubleshooting cases. The first
archive harness invocation stopped because its reused environment lacked pip;
the unchanged check passed in a new pip-enabled environment. Both results are
retained privately.

Linux candidate validation passed all 295 tests with three platform-specific
skips, exact wheel checks, clean wheel and sdist installation, and the literal
Bash guide including all six troubleshooting categories. Windows CI results and
publication/public-install verification are recorded after completion below.

## Candidate passed and main merged

The candidate workflow completed successfully. Windows ran all **295 tests with
zero skips**; Linux ran **295 tests with three platform-specific skips**. Both
platforms passed exact wheel/resource/pinned save-and-reopen verification and
clean installations from the unchanged wheel and sdist. The Bash guide passed on
Linux. The local Windows guide/default-off/troubleshooting checks also passed.

The documentation correction was merged through [PR #2](https://github.com/bjarkig82/novel-creator/pull/2).
The feature and release preparation were merged through [PR #3](https://github.com/bjarkig82/novel-creator/pull/3)
at main commit `e0e5b315b4643675bd36cfdfe6d4870545224ec2`. Its Git tree is identical to
the tested candidate source. Release tag `v0.2.0` identifies that exact candidate
source. The earlier synthetic transport-smoke PR is not part of this merge.

Protected publication selects run 41697714816, attempt 1 and artifact 13262337033;
the workflow verifies the source/archive/evidence bindings before uploading the
existing files. Native Windows declarations explicitly reuse unchanged-component
evidence, supported by the two release-only deltas and fresh archive/guide checks;
they do not claim a new native conversation. Linux host qualification remains
false. Production named-install and public hash results follow after publication.
