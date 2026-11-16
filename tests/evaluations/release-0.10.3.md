# 0.10.3 release evidence

Status on 2026-11-16: **verified published on PyPI; full Linux and full Windows
qualification, exact public archive hashes, both named public installation
checks and the annotated qualified-source tag verified**.
The [release notes](../../docs/releases/0.10.3.md) compare with 0.10.2 and explain
complete new/existing legacy/notebook delivery.

The [machine-readable record](release-0.10.3-candidate.json) preserves actual
candidate/publication runs and jobs, immutable manifest, installed reports,
public-download identities, public installation reports, remote tag annotation
and superseded candidate. It identifies the immutable qualified source rather
than this later documentation commit.

## Qualified source and exact distributions

- Qualified source: `e137235d0dad085584a9e5ee6522abb98313a9ee`.
- [Candidate run 43963885221, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43963885221/attempts/1): successful.
- Immutable artifact `14275223544`, `candidate-43963885221-1`.
- Downloaded artifact ZIP: 567625 bytes, SHA-256 `890ff11fde4a46ef5c2478533238809316e6a11dc71b4fdab20308e7b42ee964`.
- Source-bound Windows `auto` selected **full**, baseline `8df4ca09e58f71d800211a4dad794dd6c1f0c610`. The exact changed-path reason is retained in the manifest in the machine-readable record.
- The strict immutable-candidate remote verifier passed after all required platform gates.

| Distribution | Qualified and actual public-download SHA-256 | Bytes | PyPI upload time (UTC) |
| --- | --- | --- | --- |
| `novel_creator-0.10.3-py3-none-any.whl` | `c29f36dad95f8289a9a2b19d0d0fe3246d8a6c2c2d2860bd736c2b981c6629f9` | 306355 | 2026-11-16T23:11:40.436122Z |
| `novel_creator-0.10.3.tar.gz` | `0b413ceef5934d5087f54eac483fb481e05bd5148ea95011a04ab42c49ac7c66` | 271888 | 2026-11-16T23:11:42.927177Z |

The exact qualified archives were published; public metadata and actual public
downloads matched the immutable manifest. This evidence update does not rebuild
or replace published artifacts. No 0.10.3 GitHub release ZIP assets are claimed.

## Full platform qualification

| Platform | Full suite | Other required gates |
| --- | --- | --- |
| [Linux job 133638340483](https://github.com/bjarkig82/novel-creator/actions/runs/43963885221/job/133638340483) | 618 tests, 728.486 seconds, OK (5 skipped) | All passed, including literal Bash guide |
| [Windows job 133638340637](https://github.com/bjarkig82/novel-creator/actions/runs/43963885221/job/133638340637) | 618 tests, 3338.241 seconds, OK (0 skipped) | All passed; Bash-only step not applicable |

Both platforms passed the existing release gates, including manifest/skill
checks, plugin runtime installation, previous-public compatibility, complete
wheel verification and clean candidate/package installations. Previous-public
reports contain twelve source/artifact journeys per platform across installed
wheel and source distributions. Old 0.10.2 projects are initialized from its hash-pinned public wheel; candidate
controllers run under both installed candidate wheel and source distributions.
These actual public 0.10.2 updates include all four
new/existing format cases, all twelve notebook host/source/language layouts,
issue setup followed by the exact six-guide procedure, actual skills/routing and
links, preservation of story/history/custom instructions/unrelated staging, and
customized/stale/unsafe refusals. Offline disposable legacy fixture transport
exercises the explicit updater without bypassing production public-version guards.

These are automated structural/install checks. They do not establish native
Codex/Claude discovery/reload, plugin enablement, conversational usefulness,
voice behavior or subjective literary quality. No real novel or global runtime
was changed for qualification.

## Publication, index propagation and public installs

[Publication run 43976970316, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/attempts/1)
used the exact qualified source/artifact. The normal protected `pypi` environment
review was approved under the user's publication instruction; protections and
workflow gates remained unchanged.
[Publisher job 133683333239](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/job/133683333239)
succeeded **once**. Initial public checks
[Linux 133683857683](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/job/133683857683) and
[Windows 133683857896](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/job/133683857896)
failed because their index listings still ended at 0.10.2.

A failed-jobs-only retry in
[attempt 2](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/attempts/2)
passed both named public installation checks:
[Linux 133684726881](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/job/133684726881) and
[Windows 133684726533](https://github.com/bjarkig82/novel-creator/actions/runs/43976970316/job/133684726533).
Both report `validated: true`, exact `novel-creator==0.10.3` installation and
public wheel/source hashes matching the candidate. The attempt-2 publisher entry
`133684728909` carries forward the earlier success; it is not a second upload.

## Annotated source tag

The remote annotated [v0.10.3 tag](https://github.com/bjarkig82/novel-creator/tree/v0.10.3)
is verified as tag object `3efa8b550531b5bd9640ef0ce45cee8b01184592`, peeled to
`e137235d0dad085584a9e5ee6522abb98313a9ee`, with tagger time
`2026-11-16T23:16:25Z`. The complete actual annotation is retained in the
machine-readable record. This is annotation/target verification, not a claim of
a cryptographic signature (GitHub reports unsigned). The tag remains at the
qualified source, not this later documentation commit.

## Superseded unpublished candidate

Candidate 1, source `deca45d9fbb5f31bfb5d52cf0bc7c953872da682`,
[run 43959609586, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43959609586/attempts/1),
artifact `14274205264`, was neither qualified nor published. Linux ran 618 tests
in 716.023 seconds with 2 errors and 5 skips; Windows was cancelled. Both errors
came from an installed side-character package test fixture labeling a 0.10.3
artifact as 0.10.2. The production wheel-identity guard correctly rejected it.

The scoped source fix derives listing/preview/application/report version from
the installed candidate distribution. Production validation stayed unchanged.
The affected method reproduced two artifact-case errors in 99.453 seconds,
then passed both wheel/source cases in 158.653 seconds; the adjacent export test
passed in 0.376 seconds. Independent reviews approved the fix and a fresh source
candidate reran every release gate. No candidate-1 gate was carried over.
