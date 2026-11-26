# Novel Creator 0.10.7 release evidence

Published on PyPI on **2026-11-26**. The remote annotated tag `v0.10.7` has object
`11a04020a70ede41e3d1a0e1e9066a2b7f826608` and points to qualified source
`fc495fe9e57227778e5d44de7c3c841a1340215f`.
[Tagged source](https://github.com/bjarkig82/novel-creator/tree/v0.10.7) ·
[Release notes](../../docs/releases/0.10.7.md)

## Qualification

Candidate run `45826342637`, attempt `1`, produced immutable artifact
`15120716170`. Full Linux and Windows qualification passed. The suites ran
663 tests on each platform, with five skips on Linux and none on Windows.
[Candidate run](https://github.com/bjarkig82/novel-creator/actions/runs/45826342637/attempts/1) ·
[Linux](https://github.com/bjarkig82/novel-creator/actions/runs/45826342637/job/139931517477) ·
[Windows](https://github.com/bjarkig82/novel-creator/actions/runs/45826342637/job/139931517533)

Supplemental offline checks used the qualified wheel and source archive and the
hash-verified public 0.10.6 wheel. Both candidate installations initialized new
English and Icelandic legacy novels and format-1 notebooks. Upgrades passed for
all 12 notebook layouts across both languages, three host selections and two
skill sources. The refreshed conversation and retrospective guides matched new
setup, and installed workflow and skill links resolved. The refresh preserved
writer files, custom root instructions, staging and HEAD. Stale previews,
customized guides and redirected paths were refused without writing. The legacy
update kept writer work and history, made one framework commit and supported a
subsequent synthetic save.

## Publication

The protected PyPI deployment and both named public installation checks passed
in run `45844463909`, attempt `1`. [Publish run](https://github.com/bjarkig82/novel-creator/actions/runs/45844463909/attempts/1) ·
[Publish job](https://github.com/bjarkig82/novel-creator/actions/runs/45844463909/job/139994421796) ·
[Public Linux](https://github.com/bjarkig82/novel-creator/actions/runs/45844463909/job/140000580133) ·
[Public Windows](https://github.com/bjarkig82/novel-creator/actions/runs/45844463909/job/140000580051)

Both public downloads were independently verified against the qualified
candidate by SHA-256 and size on 2026-11-26. [PyPI distributions](https://pypi.org/project/novel-creator/0.10.7/#files)

| Distribution | SHA-256 | Bytes | PyPI upload time (UTC) |
| --- | --- | ---: | --- |
| `novel_creator-0.10.7-py3-none-any.whl` | `4dc7245e6d73cffc6f1a07a3102d60f9d58d0fff5d66e28987f1142ffe3b265f` | 318994 | 2026-11-26T15:09:32.929939Z |
| `novel_creator-0.10.7.tar.gz` | `465a76aae7cab82570b725436f61d2f8c0161db3584d0a3230b9a4daa835ff92` | 278350 | 2026-11-26T15:09:34.450286Z |

Native skill discovery and reload, live voice and handoffs, host GitHub
connector publishing and Git permission handling in live writing sessions
remain unverified.
