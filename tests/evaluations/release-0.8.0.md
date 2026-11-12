# 0.8.0 release evidence

Status on 2026-11-12: **published on PyPI; public checks and annotated tag
verified**. Full Linux and full Windows qualification, both public CI installation
checks, independent public installation and published-index plugin bootstrap
passed. The GitHub release and all four asset hashes are verified.

The [release notes](../../docs/releases/0.8.0.md) describe the published release.
This is the canonical release qualification ledger; the accompanying
[candidate record](release-0.8.0-candidate.json) preserves immutable identities,
both platforms' reports and workflow results. The earlier
[marketplace ledger](marketplace-0.8.0.md) records implementation/preflight
observations against earlier local builds. Its local artifact hashes, source
status and pending Linux/Windows gates are historical; the qualified candidate
and platform results below supersede them for release decisions.

## Immutable candidate

- Source on main: `9491664acccec5c9cb1f9c2ce6315883328aaeeb`.
- [Candidate run 43218783499, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43218783499/attempts/1): completed successfully.
- Artifact: `13945000853`, `candidate-43218783499-1`.
- Artifact ZIP SHA-256: `1f39564e754fba811536fc1913a28ed14d2c8c64e49ea03fedb18ff2377f4b66`, matched GitHub artifact metadata.

| Qualified distribution | SHA-256 |
| --- | --- |
| `novel_creator-0.8.0-py3-none-any.whl` | `390c6e208fe71a803783cd2cf979bada3e20988518a0032572fcf9a1b8711c5b` |
| `novel_creator-0.8.0.tar.gz` | `ad5b9fb1ad534c9e1268793743fd26f3f57679426f023920b468ec855d37f210` |

The downloaded artifact ZIP and both distribution hashes were checked locally.
The manifest identifies this source, run, attempt and package version. The
remote release verifier passed against the completed candidate and exact
artifact, source, hashes and required platform jobs. Windows selection is
`full`, reason “Manual full qualification requested”, with source-policy
baseline `8df4ca09e58f71d800211a4dad794dd6c1f0c610`.

Plugin assets reproduced from the qualified source distribution were also hashed:

| Reproducible plugin asset | SHA-256 |
| --- | --- |
| `novel-creator-plugin-0.8.0.zip` | `08ef3d9d33d06cf1696be1199ba4e28f634d4359114f427896a7a22cc8708d01` |
| `novel-creator-marketplace-0.8.0.zip` | `36ba44febb12bbcf06fe92a7c85e3805b45fd234239f43c521f4ffe2d0e33cac` |

The distributions above match published PyPI hashes. All four files are attached
to the verified GitHub release with matching SHA-256 digests and sizes.

## Linux and Windows qualification

| Platform | Full suite | Early project-upgrade guards | Package gates |
| --- | --- | --- | --- |
| [Linux](https://github.com/bjarkig82/novel-creator/actions/runs/43218783499/job/131184997980) | 509 tests in 612.714 seconds, OK (3 skipped) | 21 tests in 3.504 seconds, OK | Passed, including literal Bash guide |
| [Windows](https://github.com/bjarkig82/novel-creator/actions/runs/43218783499/job/131184997971) | 509 tests in 3660.762 seconds, OK | 21 tests in 38.593 seconds, OK | Passed; Bash-only guide step skipped |

Counts and times come from the actual candidate job logs. Both jobs passed
manifest verification, project skill-upgrade checks, plugin runtime installation,
previous published notebook compatibility, wheel byte/legacy journey verification,
clean wheel installation and clean installation from the candidate source archive.
Windows ran the full suite; the separate reduced compatibility-suite step was
skipped because full qualification was selected.

The candidate installation reports bind their results to wheel SHA-256
`390c6e208fe71a803783cd2cf979bada3e20988518a0032572fcf9a1b8711c5b`
and report no dependency inheritance. They cover new legacy and English/Icelandic
notebook setup, settings preservation, notebook guidance/resources, explicit
notebook retrofit, context/memory views and five invalid-input cases. Previous
0.7.1 upgrades exercise notebook resource refresh/preservation and disposable
legacy CLI update/save/recovery journeys; the legacy target matches 96 installed
product files. These are installed-controller probes, with native host evidence
explicitly false.

Both platforms' plugin runtime reports record isolated dependency checks,
runtime creation/reuse and English/Icelandic plugin notebooks for both hosts:
two instruction files, twelve project-local role definitions, zero duplicate
local skills, resolved links and clean initialized Git state. The updater refuses
that plugin layout without mutation. The `native_agents` report field counts
written role definitions; it does not establish host discovery or specialist use.

Both platforms also tested actual published 0.7.2 notebook upgrades, using frozen
wheel SHA-256
`8ee343c10bfcc8129d860a8502c669856deaa92f62b5059f915a4027fc11c9f5`.
English/Icelandic updates preserved story files, custom instructions, history and
unrelated staging. Focused updates stayed compatible and did not silently adopt
plugin integration. Complete report contents and their SHA-256 values are
preserved in the candidate record.

## Observed marketplace CLI behavior

An isolated Claude Code **2.1.322** configuration successfully added
`bjarkig82/novel-creator` from GitHub over HTTPS and installed
`novel-creator@novel-creator-marketplace`. CLI details reported version 0.8.0,
**15 skills, 0 agents, 0 hooks, 0 MCP servers and 0 LSP servers**. This is actual
CLI marketplace installation and inventory evidence. The project-local roles
created by notebook setup are separate from plugin agent entries.

The earlier marketplace ledger records strict local Claude plugin/catalog
validation, local installation, disposable lifecycle preservation and Codex CLI
**0.163.0** discovery with transient catalog configuration. Codex reported 0.8.0
available and not installed. Its app-server read failed because the default home
was read-only despite local database/log overrides. These historical CLI checks
do not establish native Codex installation or GUI inventory. The synthetic
metadata-only Claude update to 0.8.1 in that ledger is a lifecycle probe, not a
qualified release or runtime-upgrade result.

Normal bootstrap from the actual GitHub-installed Claude plugin passed through
the published PyPI index without `--wheel`. It created and reused the isolated
0.8.0 runtime and initialized English/Icelandic dual-host plugin notebooks. This
is separate post-publication evidence from candidate local-wheel runtime checks.

## Publication and source tag

[Publish run 43230160921](https://github.com/bjarkig82/novel-creator/actions/runs/43230160921)
completed successfully using the exact candidate run, attempt, artifact, source
and hashes above. PyPI reports wheel upload at `2026-11-12T14:24:14.994391Z`
and source archive upload at `2026-11-12T14:24:16.742941Z`. Public metadata and
both downloaded archive hashes match the qualified manifest. The package is
available at [PyPI 0.8.0](https://pypi.org/project/novel-creator/0.8.0/).

The [Windows public check](https://github.com/bjarkig82/novel-creator/actions/runs/43230160921/job/131268431822)
passed in publication attempt 1. The initial Linux public check failed because
0.8.0 was not yet visible in the PyPI simple index immediately after upload.
Only that failed public job was rerun; the
[Linux public check](https://github.com/bjarkig82/novel-creator/actions/runs/43230160921/job/131268427664)
passed in attempt 2, without repeating publication. Actual downloaded CI reports
were verified against their report archive hashes. Both record named production
installation, exact installed wheel identity, matching public wheel/source hashes,
valid project probes and no dependency inheritance. A separate independent public
installation also passed those checks, including prior-project update probes.
The candidate record preserves the complete reports and their SHA-256 values.

The annotated remote tag `v0.8.0` was verified with tag object
`8484e06ea3c9bc55e80fe21ec226b826097bb064`, peeled commit
`9491664acccec5c9cb1f9c2ce6315883328aaeeb`. It points to the immutable
qualified/published source, including after later documentation/evidence commits.
The [GitHub release](https://github.com/bjarkig82/novel-creator/releases/tag/v0.8.0)
was published at `2026-11-12T15:12:05Z` with both qualified distributions and both
reproducible plugin ZIPs. All four remote asset digests match the tables above;
sizes are 242293 bytes (wheel), 215931 bytes (source archive), 21565 bytes
(plugin ZIP) and 23166 bytes (marketplace ZIP). The
[asset completion run 43245148047](https://github.com/bjarkig82/novel-creator/actions/runs/43245148047)
passed, including downloading and hashing remote asset bytes. It reused the
qualified candidate and published package; it did not repeat PyPI publication.
The release tag still peels to the qualified source, rather than the later
asset-workflow or documentation commits.

Historical publication state: the run initially waited for the protected `pypi`
environment; an approval API call returned HTTP 403, “Resource not accessible by
integration”. The protection was not changed. That earlier pending state is
superseded by the successful publication and public verification above.

## Limits

All project probes use disposable synthetic writing. Authenticated Codex/Claude
conversations, GUI skill discovery, native specialist controls/invocation,
language/literary quality and voice behavior remain unverified. Linux/Windows
package qualification is automated evidence; `windows_host` and `linux_host`
remain false in the publication input. No real novel content is included.

Existing notebook plugin adoption, a legacy host port, macOS, MCP and
public-directory submission remain deferred. Existing-format standalone updates
and preservation checks do not establish those deferred capabilities.
