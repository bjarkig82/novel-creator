# Novel Creator 0.10.6 release evidence

Published on PyPI on **2026-11-24**. The remote annotated tag `v0.10.6` has object
`d18826762cbd641592fb1b8655e8305f810baa15` and points to qualified source
`0d0cdad4432c6c52297ef21d15295ef652984305`.
[Tagged source](https://github.com/bjarkig82/novel-creator/tree/v0.10.6) · [Release notes](../../docs/releases/0.10.6.md)

## Qualification

Candidate run `45396960150`, attempt `1`, produced immutable artifact
`14921896174`. Full Linux and Windows qualification passed. The full suites
ran 647 tests on each platform, with five skips on Linux and none on Windows.
Both platforms verified upgrades from earlier public versions, wheel and source
installs, and pinned legacy workflows. Linux also passed the Bash guide check.
[Candidate run](https://github.com/bjarkig82/novel-creator/actions/runs/45396960150/attempts/1) ·
[Linux](https://github.com/bjarkig82/novel-creator/actions/runs/45396960150/job/138455361131) ·
[Windows](https://github.com/bjarkig82/novel-creator/actions/runs/45396960150/job/138455361114)

Supplemental checks upgraded from the hash-verified published 0.10.5 wheel
using each installed candidate artifact. All 12 notebook layouts preserved
story files, writer instructions, staging and HEAD. The legacy upgrades retained
writer work and history and each completed a subsequent save. The read-only
index check preserved both notebook and Git bytes.

## Publication

GitHub's protected PyPI deployment approved the verified candidate. It
uploaded the two archives once. Both public install jobs initially received
HTTP 404 from PyPI before the new version appeared in the index. The retry
ran only the failed install jobs. The publisher and both named public
installation checks passed in run
`45412854596`.
[Publish run](https://github.com/bjarkig82/novel-creator/actions/runs/45412854596) ·
[Public Linux](https://github.com/bjarkig82/novel-creator/actions/runs/45412854596/job/138518639947) ·
[Public Windows](https://github.com/bjarkig82/novel-creator/actions/runs/45412854596/job/138518639540)

Both public archives were downloaded and matched the qualified candidate
SHA-256 hashes and published sizes. [PyPI distributions](https://pypi.org/project/novel-creator/0.10.6/#files)

| Distribution | SHA-256 | Bytes | PyPI upload time (UTC) |
| --- | --- | ---: | --- |
| `novel_creator-0.10.6-py3-none-any.whl` | `ab7fc7b1ed06a39c760614a92b0718b329ea923d3bed312ed5499dbca6934ecb` | 316349 | 2026-11-24T14:29:32.123658Z |
| `novel_creator-0.10.6.tar.gz` | `3ff29c0c8196dd5963426737e33ea602c66665364270229b5bc55b2d8d3d114f` | 275655 | 2026-11-24T14:29:33.394198Z |

These checks verify automated behavior and installed bytes. Native Codex
Desktop skill discovery, delegate behavior, live voice and connector publishing
remain separate host observations.
