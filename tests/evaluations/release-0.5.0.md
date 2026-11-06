# Novel Creator 0.5.0 release evidence

**Status: verified published release, 2026-11-06.** The public PyPI wheel and
source archive match the exact automated Windows/Linux qualified candidate.
Independent clean public named-package installation and Windows/Linux public CI
checks passed, selecting the wheel. Native Desktop acceptance remains unverified.
The [release notes](../../docs/releases/0.5.0.md) describe changes and compatibility.
The [machine-readable candidate record](release-0.5.0-candidate.json) retains
selected public facts without raw logs, signed download URLs or private paths.

## Immutable candidate

- Repository: `bjarkig82/novel-creator`.
- Source: `7b314f725a26d778ca0153761e1773428f6858f2`.
- [Package release run 42228146377, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/42228146377/attempts/1): completed successfully.
- Candidate artifact: `13505594099`, named `candidate-42228146377-1`.
- Artifact ZIP SHA-256: `ff1aca198ede61914cdff7b5d2f87cd0dca41f74ccf4d127f20470b20becb253`.

| Distribution | SHA-256 |
| --- | --- |
| `novel_creator-0.5.0-py3-none-any.whl` | `8d2e981294b7d4e11bb47f286f98c75b18d7a5f24e8803b5ce30374bee4ecd9b` |
| `novel_creator-0.5.0.tar.gz` | `c6e9396ee1bf23e3d51a4cf2954aad14814d2a7876c20011aa18b95f12bf929d` |

## Qualification results

| Platform | Full suite | Other required candidate checks |
| --- | --- | --- |
| [Windows job 127926963083](https://github.com/bjarkig82/novel-creator/actions/runs/42228146377/job/127926963083) | Passed; 418 tests in 3110.940 seconds, 0 skipped | Manifest identity/hashes, strict wheel bytes and legacy journeys, clean wheel installation and clean source archive installation passed. |
| [Linux job 127926963069](https://github.com/bjarkig82/novel-creator/actions/runs/42228146377/job/127926963069) | Passed; 418 tests in 349.105 seconds, 3 skipped | The same checks and the literal Bash getting-started guide passed. |

The candidate build and package metadata checks passed. Independent artifact
download verified the ZIP digest and distribution manifest hashes. All 75 checked
packaged source files, including the six native agent TOML definitions, matched
the reviewed source. The remote release verifier passed against the actual
completed run, attempt, platform jobs, artifact, source identity and hashes,
retaining false native Windows/Linux host flags. These checks bind qualification
to this candidate rather than a later checkout or rebuilt distribution.

The [focused writing-agent evidence](writing-agents.md) separately records
implementation checks and selected disposable workflow scenarios. Those records
do not establish target Desktop behavior. Historical 0.4.1 evidence remains
unchanged and applies to its own source and artifact identities.

## Verified publication and public installation

[Publication run 42237043344](https://github.com/bjarkig82/novel-creator/actions/runs/42237043344)
was dispatched from documentation commit
`5a92fb351c34ce80f8c11c56e71a6260c3ba97bc` with the qualified artifact unchanged.
The integration initially received HTTP 403, `Resource not accessible by
integration`, when requesting protected `pypi` environment approval. The writer
then approved through the GitHub interface. Publish job `127957259898` succeeded
on attempt 1; no upload failure is claimed. Environment protection and the
[release workflow](../../.github/workflows/package-release.yml) remained unchanged.

PyPI reports wheel upload `2026-11-06T15:08:28.777549Z` and source archive upload
`2026-11-06T15:08:30.442627Z`. Both public SHA-256 hashes match the qualified
manifest above. [Novel Creator 0.5.0](https://pypi.org/project/novel-creator/0.5.0/)
was independently verified as the latest public release.

An independent clean installation of `novel-creator==0.5.0`, without inherited
dependencies, passed production verification, including English/Icelandic notebook
initialization and installed writing resources. It selected the public wheel and
verified its hash against the candidate manifest. Both published file hashes were
verified; this check did not install the public source archive. Candidate clean
source archive installations had already passed on Windows and Linux above.

Both first-attempt public CI jobs received PyPI version-JSON HTTP 404 seconds after
successful upload. Exact public availability and hashes were verified before
rerunning only the failed check jobs in
[attempt 2](https://github.com/bjarkig82/novel-creator/actions/runs/42237043344/attempts/2).
Attempt 2 completed successfully: the
[Linux public check job 127970049761](https://github.com/bjarkig82/novel-creator/actions/runs/42237043344/job/127970049761)
and [Windows public check job 127970050246](https://github.com/bjarkig82/novel-creator/actions/runs/42237043344/job/127970050246)
both passed named production installation and selected archive hash checks. No
second upload or artifact rebuild occurred.

Documentation and evidence commits after the selected source do not replace or
rebuild the qualified artifact. Publication retained the source, candidate run,
attempt, artifact and distribution hashes above and preserved the workflow gates.

## Scope and remaining limits

Qualification is automated-only. Native Windows/Linux Codex Desktop discovery,
delegation and persistent direct specialist controls remain unverified; both
native host evidence flags are false. A same-chat role does not establish a
native specialist, and self-review does not establish independent review. See
the [native host checkpoint](writing-agents-host.md).

Windows automated CLI/install checks do not establish a literal PowerShell guide
journey. Linux CLI/package checks do not establish Linux Codex writing behavior;
macOS support remains deferred. Structural checks and disposable scenarios do
not establish literary quality, exhaustive continuity or full English/Icelandic
literary parity. Live voice capture, spoken fidelity and direct native-user
legacy update behavior remain outside this release's observed scope.
