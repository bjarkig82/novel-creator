# 0.9.0 release evidence

Status on 2026-11-12: **verified published on PyPI; public checks and annotated
source tag verified**. Full Linux and full Windows qualification, both public CI
installation checks and an independent clean public installation passed. GitHub
release and plugin/marketplace ZIP completion remain pending.

The [release notes](../../docs/releases/0.9.0.md) describe the change from 0.8.0.
The [machine-readable candidate record](release-0.9.0-candidate.json) preserves
observed source, artifact, platform, publication and tag identities. Those
identities refer to the qualified source below, never a later documentation
commit. The [feature evaluation](character-development.md) retains its scoped
implementation and agent observations; these do not replace release qualification.

## Immutable qualified candidate

- Source on main: `73973ea1a15dadf38a2123511e420b35fcb3c9fd`.
- [Candidate run 43307264896, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43307264896/attempts/1): completed successfully.
- Artifact: `13982904277`, `candidate-43307264896-1`.
- Downloaded artifact ZIP SHA-256: `574903451c2ac1962bb70fddddfc4599c8b9169f6acb106c3f2189f4283f2fd0`, matched GitHub artifact metadata.
- Windows policy: `full`, reason “Manual full qualification requested”, baseline `8df4ca09e58f71d800211a4dad794dd6c1f0c610`.

| Qualified distribution | SHA-256 |
| --- | --- |
| `novel_creator-0.9.0-py3-none-any.whl` | `59050772544faa3056fa173f06c7c410e5f07e352fdad38d41bf88185e86667f` |
| `novel_creator-0.9.0.tar.gz` | `1e2bf80c94db2fc464c3b90814fd9cf13ab82747cd39a52978ffcf385d9b5fe4` |

The manifest and downloaded payload agree on source, run, attempt and hashes.
The source-bound remote release verifier passed after both platforms finished.
Independent payload inspection matched all 98 wheel product files and all 126
tracked source-distribution files to the exact qualified Git source. The 16-entry
plugin archives matched that source distribution and reproduced byte-for-byte.
Published distributions and release ZIPs retain the exact qualified source bytes;
later repository documentation corrections do not rebuild or replace them.

| Reproduced plugin archive (not yet published as a GitHub asset) | SHA-256 |
| --- | --- |
| `novel-creator-plugin-0.9.0.zip` | `7ff5fbd64408ec25343b5c2ada8e7a9a8605277f2d9b7b2bb2020906a6dca15b` |
| `novel-creator-marketplace-0.9.0.zip` | `838f9c5bb8904c6262f4e40052139668a95419f00ba86434d70ad5a1a9f9a245` |

## Full platform qualification

| Platform | Full unit suite | Remaining candidate gates |
| --- | --- | --- |
| [Linux](https://github.com/bjarkig82/novel-creator/actions/runs/43307264896/job/131493930641) | 534 tests in 615.468 seconds, OK (4 skipped) | Passed, including literal Bash guide |
| [Windows](https://github.com/bjarkig82/novel-creator/actions/runs/43307264896/job/131493930523) | 534 tests in 3655.775 seconds, OK (0 skipped) | Passed; Bash-only guide step skipped |

Both platforms passed manifest verification, project skill-upgrade checks, plugin
runtime installation, previous published notebook compatibility, complete wheel
byte/legacy journey verification, clean wheel installation and clean installation
from the candidate source archive. Windows ran full qualification, not the reduced
compatibility suite. Counts and times above come from the candidate job logs.

The previous-release gate uses frozen public 0.7.2/0.8.0 artifacts. It exercises
supported standalone updates and the documented manual Character development
procedure in public 0.8.0 notebooks for Codex/Claude/both × project/plugin ×
English/Icelandic under installed wheel and source-distribution runtimes. Checks
cover rendered bytes, project skills and linked workflows, conflicts, identical
retry, story/custom directions, index, HEAD and unrelated staging preservation.
Legacy journeys retain their existing methods; Character development is
notebook-only. All writing projects are disposable synthetic fixtures.

Qualification history: the first candidate, run `43305390887` attempt 1 at source
`9464795c17a9edaa443d859c3ad8953e7d48feb3`, artifact `13983916263`, was cancelled
and must never be published. The local full Linux preflight exposed stale positive
plugin-bootstrap fixtures still pinned to 0.8.0: 534 tests, 9 failures, 2 errors
and 4 skips. A version-aware fixture repair preserved guards and intentional bad
versions; 39 focused tests passed. The fresh candidate above then passed both
full platforms. The first candidate's wheel/sdist identities are superseded;
matching ZIP hashes alone do not make its cancelled package publishable.

## Publication and annotated source tag

[Publish run 43318747681, attempt 2](https://github.com/bjarkig82/novel-creator/actions/runs/43318747681/attempts/2)
completed successfully at the same qualified source, using the exact candidate
run, attempt, artifact and distribution hashes above. The publish workflow was
dispatched and its `head_sha` verified before advancing main with release evidence.
The protected `pypi` approval gate was preserved and the owner approved in GitHub.

| Public PyPI archive | Size | Upload time (UTC) |
| --- | --- | --- |
| Wheel | 248522 bytes | `2026-11-12T22:20:02.527254Z` |
| Source archive | 221732 bytes | `2026-11-12T22:20:04.068074Z` |

Both public archive downloads and metadata hashes match the qualified manifest.
[PyPI 0.9.0](https://pypi.org/project/novel-creator/0.9.0/) is available. Windows
public installation passed in attempt 1. The initial Linux public check failed
because 0.9.0 was not yet visible in the PyPI simple index immediately after
upload. Only the failed Linux public check was retried after propagation, and
passed in attempt 2. The successful publish and Windows results retained their
original timestamps in the rerun; publication was not repeated.

The independent clean named public install also passed on retry after initial
index propagation. Its preserved report records `novel-creator 0.9.0`, the exact
installed wheel hash, both public distribution hashes, valid disposable project
and prior-project update probes, and `dependency_inheritance: false`. The full
report and its SHA-256 are embedded in the candidate record. These are package
installation checks, not native host conversations.

Annotated tag `v0.9.0` is pushed and remotely verified, with tag object
`ac473d4de57f689f6600180b8e73acd84e8507d1` peeling to
`73973ea1a15dadf38a2123511e420b35fcb3c9fd`. The annotation identifies the
qualified source and candidate. The tag points to the immutable published source,
not a later documentation or asset-workflow commit.

## Pending GitHub asset completion

The [0.9.0 selection](../../.github/release-assets-0.9.0.json) and separate
[0.9.0 workflow](../../.github/workflows/github-release-assets-0.9.0.yml) pin the
actual candidate, successful publish attempt, source, annotated tag object and
reproduced ZIP hashes above. They use the existing unchanged publisher and normal
Actions contents-write/actions-read permissions, with no dispatch inputs. The
old 0.8.0 selection and workflow remain unchanged.

A read-only publisher rehearsal passed against the real candidate, successful
publish attempt, annotated tag and public PyPI bytes, preparing all four exact
assets and verifying reproduced ZIP hashes. It reported that the GitHub release
was absent; `--publish` was omitted. GitHub release creation/upload and remote
four-asset byte/hash/size verification remain pending. The expected ZIP hashes above establish candidate reproduction,
not remote availability. The publisher preserves all existing source-bound gates,
requires both public checks, verifies the annotated tag and public PyPI bytes,
and refuses to overwrite mismatched existing release assets. It never repeats
PyPI publication or moves a tag.

## Limits

Qualification is **automated-only**: `windows_host` and `linux_host` remain false.
Native Codex/Claude conversations, active-chat reload, Desktop/GUI discovery,
specialist invocation and English/Icelandic literary quality remain unverified.
The retained explicit-load agent exercise has its own narrower scope in the
feature evaluation; structural checks do not establish the full conversation
rubric. Unsaved chat drafts have no guaranteed recovery.

Existing notebooks require explicit updates; package/plugin installation alone
does not refresh book snapshots. Original Codex/project notebooks have preview/
apply; other supported layouts and the default-layout alternative use the bounded
manual procedure. Existing notebook marketplace adoption, whole plugin-book
snapshot migration, legacy host port, macOS, MCP and public-directory submission
remain deferred. No real novel or global installation was used for these probes.
