# 0.10.2 release evidence

Status on 2026-11-16: **verified published on PyPI; full Linux and full Windows
qualification, exact public archive hashes, both named public installation
checks and the annotated source tag verified**.
The [release notes](../../docs/releases/0.10.2.md) describe changes from 0.10.1
and the explicit project upgrade paths.

The [machine-readable record](release-0.10.2-candidate.json) preserves candidate,
platform, publication and superseded-attempt identities. It refers to the
immutable qualified source, not this later documentation commit.

## Immutable qualified source and distributions

- Qualified source: `9deeaa1cbbca6ad7c172b90687b698f5ae63b4f4`.
- [Candidate run 43783843943, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43783843943/attempts/1): successful.
- Artifact: `14189193059`, `candidate-43783843943-1`.
- Downloaded artifact ZIP: 549405 bytes, SHA-256
  `1ddab6c2498c6c2621dcba1a54e026cb4c1922f6bb219bd9ff87b11bed1b78df`.
- Windows policy: `auto` selected `full`, baseline
  `8df4ca09e58f71d800211a4dad794dd6c1f0c610`. The full source-bound changed-path
  reason is retained in the manifest in the machine-readable record.

| Distribution | Qualified and public SHA-256 | Bytes |
| --- | --- | --- |
| `novel_creator-0.10.2-py3-none-any.whl` | `24117c4c17c7a56a981edbf1852440bbca94f668ea4f4fdf9aef4b940a000659` | 297549 |
| `novel_creator-0.10.2.tar.gz` | `78c9c16b6864b6ebc76157d0984cc9f4957cf013c84830614a2b136e95008956` | 262804 |

The manifest binds exact run, attempt, source and distribution hashes. The
strict immutable-candidate remote verifier passed after both required platforms
completed. Direct archive inspection matched 112 wheel product files and 142
tracked source-distribution files to exact qualified Git bytes, with no
unexpected/private/untracked payload. Downloaded candidate and actual public
archive hashes match. This later documentation does not rebuild or replace them.

## Full platform qualification

| Platform | Full suite | Other required gates |
| --- | --- | --- |
| [Linux job 133027033185](https://github.com/bjarkig82/novel-creator/actions/runs/43783843943/job/133027033185) | 601 tests in 524.424 seconds, OK (5 skipped) | All passed, including literal Bash guide |
| [Windows job 133027033095](https://github.com/bjarkig82/novel-creator/actions/runs/43783843943/job/133027033095) | 601 tests in 3980.668 seconds, OK (0 skipped) | All passed; Bash-only step not applicable |

Both platforms passed manifest verification, project skill upgrades, plugin
runtime installation, previous-public compatibility, full unit suite, complete
wheel bytes and legacy journeys, clean wheel installation and clean installation
from the candidate source distribution. Windows ran full qualification. Counts
and timings are actual successful candidate-job results, not local focused runs.

Retained installed-candidate reports validate the exact candidate wheel hash,
English/Icelandic new notebooks with 39 verified resources each, and explicit
previous-public 0.7.1 notebook/legacy updates. Plugin-runtime reports validate
isolated runtime creation/reuse and both English/Icelandic dual-host plugin
notebooks, with no duplicate local skills. Each platform's previous-public
report validates all ten source/artifact dispatches and exact candidate hashes.

Compatibility retains historical journeys and adds actual public 0.10.1 delivery
under installed wheel and source-distribution runtimes: all twelve
host/source/language feature-only side-character and issue-retro setups, both
default-layout notebook updates, new legacy/notebook setup and explicit offline
trusted-artifact legacy updates. Checks cover actual skills, linked workflows,
root routing, current/no-op, stale/custom/unsafe refusals and preservation of
story, custom directions, history, integration and unrelated raw staging.
All qualification books are disposable synthetic projects; their offline legacy
transport does not bypass the ordinary public stable-release discovery gate.

## Superseded candidates and repairs

All four earlier candidates were superseded and **not published**. Partial
successful gates were never transferred to the final candidate.

| Candidate | Source and run | Observed result and correction |
| --- | --- | --- |
| 1 | `17f66649a7bc61aabc2fb3ae34c6195f9bf8e679`, [43766631897/1](https://github.com/bjarkig82/novel-creator/actions/runs/43766631897/attempts/1), artifact `14182815632` | Failed stale exact inventory in previous-public compatibility. Completed failure before cancellation request. Exact verifier inventory repaired and actual public 0.10.1 artifact coverage added. |
| 2 | `379b8040ae5135da93191f1badb17b44a6f6e4e6`, [43769789773/1](https://github.com/bjarkig82/novel-creator/actions/runs/43769789773/attempts/1), artifact `14183464108` | Linux compatibility passed; full suite 599 tests/483.686s failed (3 failures, 5 errors, 5 skips). Remaining run cancelled. Fixture-local Git identity, stale 35-versus-39 inventory and HTTPS-as-local assumptions repaired. |
| 3 | `6b545beeb3e9f96ba52395bc38b345bedcedac54`, [43772275559/1](https://github.com/bjarkig82/novel-creator/actions/runs/43772275559/attempts/1), artifact `14185051279` | Linux full 599 tests passed in 685.298s (5 skips); wheel/legacy gate passed. Clean-wheel gate failed old-0.7.1 expected changed-path inventory missing side-character/retrospective resources; remaining Windows cancelled. Two verifier/test files repaired with exact bytes/root/link/raw-index checks. |
| 4 | `d7297f077ede3cc8148026bdaa26f224c49cda45`, [43774843761/1](https://github.com/bjarkig82/novel-creator/actions/runs/43774843761/attempts/1), artifact `14185936333` | Linux all gates passed (601 tests/440.579s/5 skips). Windows full 601 tests passed in 4100.798s/no skips; compatibility, wheel/legacy and clean wheel passed. Whole-job 90-minute guard cancelled final clean-sdist step after about 53 seconds. GitHub annotation confirms maximum `1h30m0s`; incomplete final gate prevented qualification. |

The intervening `379b804` source contains **two production/runtime-resource fixes**
from independent review, distinct from verifier/fixture repairs: strict
same-repository issue or PR references work for duplicate equivalence while
actual creation/reconciliation/attachment targets remain issue-only; ordinary
notebook retrospective turns no longer run copied legacy notice/exchange
protocols. Genuine historical legacy recovery stays explicit/external. Scoped
red/green checks passed 34 affected tests without skips, with additional notebook
and approved legacy-filesystem follow-up.

The `6b545be` repairs were test-fixture changes (including fixture-only LF
restoration), plus plugin README writing-entry count 15 to 17; runtime and
production guards stayed intact. Scoped checks passed 52 tests with one existing
local symlink skip and three installed-artifact tests without skips. The
`d7297f0` verifier repair passed 25 focused tests and exact candidate-3 wheel and
sdist complete clean installs, with independent scoped/overall reviews.

Final qualified source `9deeaa1` changes one workflow configuration file only:
bounded candidate-check job timeout 90 to 120 minutes plus explanatory comments.
All gate commands, conditions, matrix and source-bound Windows selection remain
unchanged. Three focused contract tests passed in 20.998 seconds after an
approved scoped Git/MSYS retry, with independent task and overall review clean.
The final candidate then passed both complete platform runs above.

## Publication and public installation checks

[Publish run 43792811241, attempt 1](https://github.com/bjarkig82/novel-creator/actions/runs/43792811241/attempts/1),
[publish job 133054863954](https://github.com/bjarkig82/novel-creator/actions/runs/43792811241/job/133054863954),
successfully published the exact qualified candidate. The normal configured
required-reviewer PyPI environment approval was used; protection/gates remained
in place. Publication was not rerun to retry downstream public-install checks.

| Public PyPI file | Size | Actual upload time (UTC) |
| --- | --- | --- |
| Wheel | 297549 bytes | `2026-11-16T02:33:21.458180Z` |
| Source archive | 262804 bytes | `2026-11-16T02:33:22.784968Z` |

[Official PyPI metadata](https://pypi.org/pypi/novel-creator/0.10.2/json) and actual
downloads of both public files match the exact qualified hashes above.
[PyPI 0.10.2](https://pypi.org/project/novel-creator/0.10.2/) is available.

Named public-install verification **passed on both platforms after index
propagation retries**. Attempt 1 Linux job
`133055095629` and Windows job `133055095615` failed because the package index
had not yet listed 0.10.2. Only failed downstream checks were retried. Attempt 2
Linux `133055465641` again reported index propagation; Windows
[133055465937](https://github.com/bjarkig82/novel-creator/actions/runs/43792811241/job/133055465937)
passed on its actual attempt-2 execution (02:34:38–02:36:26 UTC, install step
02:34:49–02:36:23). Only the remaining failed Linux check reran in attempt 3:
[Linux job 133056643513](https://github.com/bjarkig82/novel-creator/actions/runs/43792811241/job/133056643513)
passed (02:38:22–02:38:50 UTC, install step 02:38:27–02:38:46). Both reports
validate the named `novel-creator==0.10.2` install, selected wheel hash and both
public archive hashes against the immutable qualified candidate.

The publish workflow completed successfully at latest attempt 3. GitHub carries
the already-successful Windows execution forward under attempt-3 alias job
`133056644782`, with the same execution timestamps. Windows did **not** actually
rerun in attempt 3. The publisher itself ran only once, in attempt 1; reruns
repeated failed public checks only.

## Annotated source tag

Annotated `v0.10.2` is pushed, with its annotation and peeled commit remotely
verified. Tag object `2fe0f8bdbcfde192e46598d6179548192d4727ee` peels to immutable
qualified source `9deeaa1cbbca6ad7c172b90687b698f5ae63b4f4`. The tagger timestamp
is `2026-11-16T02:40:39Z`; the annotation identifies version, qualified source,
candidate and publication. It points to qualified source, never this later
documentation commit.
No 0.10.2 GitHub release ZIP assets are claimed by this evidence.

## Limits

Release qualification is automated-only: `windows_host` and `linux_host` are
false. Native Codex/Claude Code discovery/reload, actual conversations or
voice/display delivery, specialist interaction, capture completeness, semantic
privacy, attachment-byte integrity, timing and subjective writing quality remain
unverified by structural/file/install checks. No private writing or real-novel
update is recorded here. Project resource maintenance remains an explicit
authorized operation, separate from Python/plugin installation and publication.
