# Novel Creator 0.7.0 release evidence

**Status: verified published release, 2026-11-10.**
Full Linux and Windows automated qualification, the local full suite, independent
verification of the downloaded immutable wheel and the remote release verifier
passed. Both actual public archive hashes match the candidate, both public CI
installation checks passed and fresh PyPI metadata confirms 0.7.0 as latest.
An additional independent clean named-package check passed on retry after initial
index propagation; no upload or CI check was repeated.
The [release notes](../../docs/releases/0.7.0.md) describe the additions and
compatibility. The [machine-readable candidate record](release-0.7.0-candidate.json)
retains selected evidence without raw logs, signed URLs or private paths.

## Immutable candidate

- Repository: `bjarkig82/novel-creator`.
- Source committed and pushed to main: `e69d5a7288165950240be94f96a9fbf19a5b5b4e`.
- [Candidate run 42812449865, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/42812449865/attempts/1): completed successfully.
- Candidate artifact: `13763505786`, named `candidate-42812449865-1`.
- Artifact ZIP SHA-256: `754e234e05005b68a622ffe2ad2748f415b543274d266b2e99c56a49e49cbf11`.

| Distribution | SHA-256 |
| --- | --- |
| `novel_creator-0.7.0-py3-none-any.whl` | `e7dba537ba4abf6e1b9c832f816dd71886ed9fcd1510aa89ca8e29c4cac8e27f` |
| `novel_creator-0.7.0.tar.gz` | `3754f43b3a9e9da4eab95ad52ee422d2684153478e583f3c029191ed9efe85c3` |

The downloaded artifact ZIP digest and manifest source/run/attempt identities and
distribution hashes were verified. The manifest selects `windows_suite: full`
under the unchanged [source-bound policy](../../docs/testing-and-completion-guide.md#windows-release-selection),
with baseline `8df4ca09e58f71d800211a4dad794dd6c1f0c610`. Compatibility coverage is
not substituted for full Windows qualification, and the baseline is unchanged.

## Qualification results

| Platform | Full suite | Other required candidate checks |
| --- | --- | --- |
| [Linux job 129817180985](https://github.com/bjarkig82/novel-creator/actions/runs/42812449865/job/129817180985) | Passed; 439 tests in 465.855 seconds, 3 skipped; job completed 2026-11-10T12:12:07Z. | Candidate manifest, strict wheel bytes and legacy journeys, clean wheel installation, clean source archive installation and literal Bash getting-started guide passed. |
| [Windows job 129817181087](https://github.com/bjarkig82/novel-creator/actions/runs/42812449865/job/129817181087) | Passed; 439 tests in 3213.596 seconds, 0 skipped; job completed 2026-11-10T13:00:46Z. | Candidate manifest, full suite, strict wheel bytes and legacy journeys, clean wheel installation and clean source archive installation passed. |

An independent check of the downloaded candidate wheel passed: all 83 compared
packaged source files matched the selected source bytes. Disposable legacy
English/Icelandic cases passed initialization, pinned save/reopen, full/current/
working views, focused complete-record retrieval, lexical query misses and
installed/pinned memory-module origin checks. Old 0.1.0/0.2.0 update journeys
passed with writer work and history preserved. English/Icelandic notebooks each
verified 32 installed resources and their links. This independent verifier reused
the calling environment's dependency package directories and checked product
module origins; it is not a clean dependency-isolation result. The platform clean
installation checks above are separate evidence.

Separately, the local `.venv/bin/python -m unittest discover -q` run passed:
439 tests in 789.458 seconds, 3 skipped, exit code 0. This result is distinct from
the Linux CI full-suite timing above and does not replace platform qualification.
The normal remote release verifier passed against the exact manifest, artifact,
source, completed candidate run/attempt and actual required platform jobs. The
candidate was qualified for publication under the unchanged gates, with native host
flags false. These documentation additions do not rebuild or replace the immutable
candidate artifact.

## Manually guided workflow exercises

These disposable exercises manually loaded the workflows; they did not establish
native custom-skill discovery, native invocation or independent literary quality.
No private novel contents are included here.

- Clarification asked one question and saved its selected answer only in the
  owning note. Previous prose/history, unrelated proposals and open-question
  states, and unrelated staged work were preserved.
- Analysis identified a seeded objective contradiction while retaining intentional
  character belief and mystery. All 136 inspected files, including Git metadata,
  remained byte-identical.
- Help explained named-command inputs with ambiguous duplicate names and optional
  IDs, offered next steps for an empty Icelandic notebook, and inspected a partial
  13-skill inventory without claiming absent entries were installed. The three
  exercises preserved all 135, 123 and 126 inspected files respectively, including
  Git metadata. Examples were not executed and no notes/checkpoints were created.

## Verified publication and public installation

[Publication run 42820797937, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/42820797937/attempts/1)
was dispatched once at `2026-11-10T13:01:47Z` from source
`e69d5a7288165950240be94f96a9fbf19a5b5b4e`, bound to the exact candidate
run/attempt, artifact, source and distribution hashes above. Before dispatch,
the PyPI 0.7.0 JSON endpoint returned HTTP 404.

The initial normal approval POST for protected environment `pypi` (`25700067917`)
returned HTTP 403, `Resource not accessible by integration`, despite GitHub reporting
current-user eligibility. GitHub's approval-history API subsequently recorded
`bjarkig82` approving `pypi`; the interface used was not observed. The earlier wait
is resolved. No protection, workflow or qualification gate was bypassed or changed.

The publication run completed successfully on attempt 1. Publish job `129845531571`
started at `2026-11-10T13:05:03Z` and succeeded at `2026-11-10T13:05:28Z`.
PyPI reports the wheel upload at `2026-11-10T13:05:23.389784Z` and source archive
upload at `2026-11-10T13:05:24.708259Z`. Both actual public archives were downloaded
and their hashes matched the immutable candidate manifest. Fresh project metadata
confirmed [Novel Creator 0.7.0](https://pypi.org/project/novel-creator/0.7.0/) as
the latest published release.

The [Linux public check job 129847357181](https://github.com/bjarkig82/novel-creator/actions/runs/42820797937/job/129847357181)
passed, completing at `2026-11-10T13:05:49Z`. The
[Windows public check job 129847357767](https://github.com/bjarkig82/novel-creator/actions/runs/42820797937/job/129847357767)
passed, completing at `2026-11-10T13:06:31Z`. Both ran successfully on attempt 1;
there was no publication rerun, upload retry or public CI retry.

An additional independent clean named-package installation initially failed when
its simple index listed versions only through 0.6.0. Unrefreshed project-level
metadata also initially returned 0.6.0 while version-specific 0.7.0 metadata and
files were already available. Fresh project metadata confirmed latest 0.7.0 and
the fresh default simple index listed it before only that independent check was
retried. The retry of `novel-creator==0.7.0` passed with no inherited dependency
sites. It selected the matching public wheel, verified both public archive hashes,
checked full/current/working views and installed/pinned memory-module origins,
and verified all 32 resources and links in English/Icelandic notebooks.

This named installation selected the wheel; no independent public source-archive
installation is claimed. Candidate source-archive and CI installation checks
passed separately. The independent first failure and retry do not imply an upload
or CI failure. Documentation/evidence updates do not rebuild or replace the
qualified artifact.

## Scope and remaining limits

Native Windows/Linux Codex Desktop skill discovery, delegation and ongoing direct
specialist controls remain unverified; native host flags remain false. Automated
CLI/package checks and guided scenarios do not establish actual desktop writing
behavior, English/Icelandic literary parity, writing quality, exhaustive continuity
or measured voice responsiveness. macOS support remains deferred. Existing
notebooks and pinned legacy novels remain unchanged by package installation.
