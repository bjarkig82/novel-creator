# Novel Creator 0.4.1 release evidence

**Status: qualified but unpublished candidate.** Automated qualification passed;
PyPI publication and public installation checks remain pending. The
[release notes](../../docs/releases/0.4.1.md) describe changes and compatibility.
The [machine-readable candidate record](release-0.4.1-candidate.json) retains
the selected public evidence without raw logs or private environment details.

## Immutable candidate

- Repository: `bjarkig82/novel-creator`.
- Source: `8d8c099004ab83b95f40fcb080730ea1530a363c`.
- [Package release run 42089185677, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/42089185677/attempts/1): completed successfully.
- Candidate artifact: `13442949549`.
- Artifact ZIP SHA-256: `8e43a7ce8233c2ee745ed65cd1a0b3c85bddfaca24c547cd876d49a7e1add8ae`.

| Distribution | SHA-256 |
| --- | --- |
| `novel_creator-0.4.1-py3-none-any.whl` | `b5662f70f657f9ebb1921c165665e74be8aa2dd30ef3233dfd48a45827673223` |
| `novel_creator-0.4.1.tar.gz` | `3350736bb7bd5a2a89ec4d474f81b8fea6471b9f303912756747330b162d91ee` |

## Qualification results

| Platform | Full suite | Other required candidate checks |
| --- | --- | --- |
| Windows | Passed; 417 tests run, 0 skipped | Manifest identity/hashes, strict wheel bytes and legacy journeys, clean wheel install and clean source archive install passed. |
| Linux | Passed; 417 tests run, 3 skipped | The same candidate checks and the literal Bash getting-started guide passed. |

The candidate build and package metadata checks passed. Independent download
verified the artifact ZIP digest and distribution manifest hashes; affected
packaged bytes matched the selected source. The exact source's remote release
verifier passed against the live candidate run, attempt, platform jobs and
artifact identity. The candidate run's `publish` and `public-checks` jobs were
skipped, so this record does not establish publication or public installation.

## Publication awaiting protected environment review

[Publication run 42098634966](https://github.com/bjarkig82/novel-creator/actions/runs/42098634966)
was dispatched and is waiting for approval of the protected `pypi` environment
configured in the [release workflow](../../.github/workflows/package-release.yml).
GitHub reports that the current user can approve, but the authorized integration
could not submit the review: `Resource not accessible by integration`. Approval
through the GitHub interface remains pending; the upload has not started.
No public 0.4.1 availability or public installation checks have been verified.
The candidate remains qualified but unpublished, with no publication date.

## Scope and remaining limits

Qualification is automated-only. Windows automated CLI/install checks do not
establish a literal PowerShell guide journey. Native Windows/Linux Codex notebook
conversations, live host realtime voice capture, spoken fidelity and direct
native-user update behavior remain unverified. Linux CLI/package checks do not
establish Linux Codex writing behavior; macOS support remains deferred.
Transcription, exact current-wrapper availability, native chat tools and genuine
stable host identity remain host dependencies. Structural checks do not establish
literary quality.

Documentation/evidence updates after the selected source do not replace or
rebuild this candidate. Publication must use the qualified artifact and preserve
the existing workflow gates. Add publication status/date only after verifying
PyPI availability and the public distribution hashes and installation checks.
