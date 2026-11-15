# 0.10.1 release evidence

Status on 2026-11-15: **verified published on PyPI; both public installation
checks and the annotated source tag verified**. Full Linux and full Windows
qualification passed. The [release notes](../../docs/releases/0.10.1.md)
describe changes from 0.10.0 and explicit project upgrade steps.

The [machine-readable candidate record](release-0.10.1-candidate.json) preserves
the observed source, artifact, platform, publication and tag identities. They
refer to the qualified source below, never a later documentation commit.

## Immutable qualified source and distributions

- Qualified source: `01fe9bf0ff033d690fda4343fbff1839842af2af`.
- [Candidate run 43721068384, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43721068384/attempts/1): successful.
- Artifact: `14164582133`, `candidate-43721068384-1`.
- Downloaded artifact ZIP SHA-256: `19f2fc48edc44265661070c2bc80d9fcf163056803c2ab40866b14f0961fdd87`.
- Windows policy: `full`, reason “Manual full qualification requested”, baseline `8df4ca09e58f71d800211a4dad794dd6c1f0c610`.

| Distribution | Qualified and public SHA-256 |
| --- | --- |
| `novel_creator-0.10.1-py3-none-any.whl` | `6721c5a527f1b7e567743f2760ec5e13aec2d0394f520913e98589ac54b8b11a` |
| `novel_creator-0.10.1.tar.gz` | `82779fca16314ce90df295faf1065b5db115e5baf00b589018854344fa44bf8a` |

The candidate manifest binds the exact run, attempt, source and distribution
hashes. The source-bound remote release verifier passed after both required
platforms completed. Independent archive inspection matched 101 wheel product
files and 129 tracked source-distribution files to the qualified Git source;
private or untracked source was excluded. Published artifacts retain those
qualified bytes. This later evidence/documentation update does not rebuild or
replace them.

## Full platform qualification

| Platform | Full suite | Other required gates |
| --- | --- | --- |
| [Linux](https://github.com/bjarkig82/novel-creator/actions/runs/43721068384/job/132833043352) | 571 tests in 658.389 seconds, OK (4 skipped) | Passed, including the literal Bash guide |
| [Windows](https://github.com/bjarkig82/novel-creator/actions/runs/43721068384/job/132833043392) | 571 tests in 2782.372 seconds, OK (0 skipped) | Passed; Bash-only guide step not applicable |

Both platforms passed manifest verification, project skill upgrades, plugin
runtime installation, previous published compatibility, complete wheel-byte and
legacy journeys, clean wheel installation and clean installation from the
candidate source distribution. Windows ran full qualification rather than the
reduced compatibility suite. Counts and times above are observed candidate job
results, not a local documentation-only rerun.

Previous-release compatibility retained public 0.7.2, 0.8.0 and 0.9.0 cases and
added upgrades from the actual public 0.10.0 wheel using both candidate artifact
runtimes. For 0.10.0
notebooks, the gate exercises the exact documented session-guidance procedure
across Codex/Claude Code/both, project/plugin skills and English/Icelandic under
installed candidate wheel and source-distribution runtimes. Checks cover actual
skills and linked workflows, root routing, current retries, stale/custom/unsafe
path refusals and story/custom-instruction/skill/role/history/index preservation.
New legacy setup and explicit previous-release legacy framework updates remain
separate from notebook semantics. All projects used for qualification are
disposable synthetic fixtures.

The [first candidate, run 43720005746 attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43720005746/attempts/1),
at `837938804a67ba3fe99b21ba3000cd801f312003`, failed because a new synthetic
legacy fixture lacked its local Git identity. The production identity guard
correctly refused it. A test-harness-only repair preceded the fresh successful
candidate above; the failed candidate is superseded and was not published.

## Publication, public checks and annotated tag

[Publish run 43726705586, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43726705586/attempts/1)
published the exact successful candidate at the same qualified source.
[Publish job 132850102873](https://github.com/bjarkig82/novel-creator/actions/runs/43726705586/job/132850102873)
succeeded with the existing protected publication workflow and gates preserved.

| Public PyPI file | Size | Upload time (UTC) |
| --- | --- | --- |
| Wheel | 266973 bytes | `2026-11-15T14:53:47.788173Z` |
| Source archive | 238534 bytes | `2026-11-15T14:53:49.192760Z` |

Official PyPI metadata and downloads of both public files matched the exact
qualified hashes above. [PyPI 0.10.1](https://pypi.org/project/novel-creator/0.10.1/)
is available. The named production installation/hash checks both passed in
attempt 1: [Windows job 132850523611](https://github.com/bjarkig82/novel-creator/actions/runs/43726705586/job/132850523611)
and [Linux job 132850523612](https://github.com/bjarkig82/novel-creator/actions/runs/43726705586/job/132850523612).

Annotated tag `v0.10.1` is pushed and remotely verified. Tag object
`af80d66dd28613490511fe418bdd3460ae745739` peels to qualified source
`01fe9bf0ff033d690fda4343fbff1839842af2af`; its annotation identifies that source,
candidate and publication. The tag does not point to this later documentation
commit. No 0.10.1 GitHub release ZIP publication is recorded by this evidence.

## Limits

Release qualification is automated-only: `windows_host` and `linux_host` are
false. Native Codex/Claude Code discovery and reload, actual conversation or
voice/display delivery, specialist interaction, archive completeness, timing and
subjective writing quality remain unverified. Structural/file/install checks do
not establish those behaviors. This evidence contains no private writing or
real-novel update record; project maintenance is a separate authorized operation.
