# Novel Creator 0.5.0 release evidence

**Status: qualified but unpublished candidate.** Automated Windows/Linux release
qualification passed. Publication has not been dispatched; PyPI availability and
public installation checks have not been verified. No publication date is claimed.
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

## Publication pending

No publication workflow has been dispatched for this candidate. The existing
[release workflow](../../.github/workflows/package-release.yml) must publish the
same qualified artifact through the protected `pypi` environment and then run
public package checks. Candidate qualification does not establish a public PyPI
installation. Add a publication date and availability claims only after verifying
the public distribution hashes and installation results.

Documentation and evidence commits after the selected source do not replace or
rebuild the qualified artifact. Publication must retain the source, run, attempt,
artifact and distribution hashes above and preserve the workflow gates.

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
legacy update behavior remain outside this candidate's observed scope.
