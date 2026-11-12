# Marketplace 0.8.0 candidate evidence

Current release status: **0.8.0 published 2026-11-12**. See the
[canonical release evidence](release-0.8.0.md) for qualified/published artifact
identities, full Linux/Windows CI results, public installations and verified tag.
The local builds, hashes and pending gates below are historical observations;
they are not the released artifact identities.

Historical preflight status on 2026-11-12: **unpublished candidate**. PyPI 0.7.2 is the verified latest
release; a final PyPI recheck also found 0.8.0 absent. The work branch was fast-forwarded
from `03a55cc` to source baseline `19d87e8`; published tag `v0.7.2` peels to
`ecf9bff`. Candidate implementation is a local uncommitted change, with no push,
publication, account changes or real-novel mutation.

The [release notes](../../docs/releases/0.8.0.md) and
[marketplace guide](../../docs/plugin-marketplaces.md) describe supported scope.
This ledger distinguishes automated/CLI observations from live host behavior.
Machine-local operation logs remain under `.cache/marketplace-implementation/`
in the qualification workspace; they are not public release artifacts.

## Focused source and artifact checks

Host integration passed 47 focused tests and independent requirement/code
review. Plugin implementation passed independent review after fixing Windows
lock close-before-unlink handling and pip transport configuration precedence,
including empty configuration/environment values. The latest focused plugin
run recorded in `plugin-report.md` was:

```text
.venv/bin/python -m unittest tests.unit.test_plugin_bootstrap tests.contract.test_plugin_bundle -q
```

Result: **39 tests passed** (32 bootstrap and 7 bundle tests) on Linux. Bootstrap
unit fixtures cover Windows cache/interpreter selection and reparse/lock logic;
these are not native Windows execution. Bundle tests inspect actual allowlisted
plugin/marketplace ZIP membership, source/wheel inputs, all fifteen skill entries
and links, manifest/catalog version synchronization, and source-based rebuilds.
The builder and `--check` passed in that run. An instruction-guided scenario
evaluation also covered cache-to-book routing, Help inventory, read-only Analyze
and setup handoff; it is not an authenticated host conversation.

## Final Linux and artifact checks

The coordinator ran the full Linux suite after implementation:

```text
.venv/bin/python -m unittest discover -q
```

Result: exit 0, **509 tests in 859.766 seconds, OK (3 skipped)**, recorded in
`full-linux.log`. Independent whole-change requirement and code-quality review
both passed with no findings. This is Linux evidence; remaining release gates
are listed below.

The clean-copy final wheel/source build succeeded (`final-build.log`). A real
independent source-distribution installation passed isolated dependency checks
and English/Icelandic dual-host/plugin notebook initialization (`sdist-final.json`).
The complete rebuilt-wheel verifier also succeeded:

```text
.venv/bin/python tests/verify_wheel.py dist/novel_creator-0.8.0-py3-none-any.whl
```

Result: exit 0, JSON `ok: true`, 89 verified source files, three legacy setup
cases, two notebook cases and two historical legacy update cases
(`wheel-verifier.log`). Product module origins were checked; this verifier
explicitly reused dependency directories from the calling environment. The
separate runtime/source-install checks establish their own isolated dependency
results. None of these checks supplies semantic host or human-quality evidence.

Final locally built artifact identities from `artifact-hashes.json`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `novel_creator-0.8.0-py3-none-any.whl` | 242314 | `7f6602edd121e8bdcd2e2e3a3c73a554eac48cbc337c4acc7e9333f3b1145e6a` |
| `novel_creator-0.8.0.tar.gz` | 216597 | `d5c44bed63ea3a67d951d85c197dbde7d856fde80c38973d6be223330a376c41` |
| `novel-creator-plugin-0.8.0.zip` | 21321 | `eb8f48751bfb4a16069766e60e2bf8c9696fc888459df81bb9030fd7fee19af1` |
| `novel-creator-marketplace-0.8.0.zip` | 22922 | `b66721b671dfb930b1d95b594163da7d4bcbef560ed050e4252fe828b3abd6be` |

These are candidate hashes, not published PyPI verification.

## Actual host CLI checks

Claude Code **2.1.322** was installed only in `.tools/claude-validation/` for
validation. With task-local `CLAUDE_CONFIG_DIR`, both commands succeeded with
empty errors/warnings:

```text
env CLAUDE_CONFIG_DIR="$PWD/.cache/marketplace-implementation/claude-config" .tools/claude-validation/node_modules/.bin/claude plugin validate plugins/novel-creator --strict --json
env CLAUDE_CONFIG_DIR="$PWD/.cache/marketplace-implementation/claude-config" .tools/claude-validation/node_modules/.bin/claude plugin validate . --strict --json
```

Isolated `plugin marketplace add` and `plugin install` succeeded for the local
catalog. `claude-installed.json` reports enabled 0.8.0; `claude-details.txt`
reports **15 skills, 0 agents**, with no MCP server. Roles are project-local
setup outputs, not plugin agent entries. A later isolated reinstall into
`claude-final` confirms enabled 0.8.0 and cached bootstrap bytes equal the current
source (SHA-256 `fd31018ccafbb9b1bc39c3c773733e758bb9b1c7d2e0b771b93e963174ef53d5`).

Codex CLI **0.163.0** returned the available candidate using transient catalog
configuration, without changing the user's default configuration:

```text
codex -c 'marketplaces.novel-creator-marketplace.source_type="local"' -c 'marketplaces.novel-creator-marketplace.source="/workspace/novel-creator"' plugin list --marketplace novel-creator-marketplace --available --json
```

`codex-discovery.json` reports plugin ID
`novel-creator@novel-creator-marketplace`, version 0.8.0, available and not
installed. Codex app-server plugin reading failed because its default home was
read-only despite task-local SQLite/log overrides (`codex-read.stderr.log`).
Catalog discovery is the observed Codex result; native installation, GUI
inventory and conversations are not established.

## Installed runtime and previous-version checks

The maintained opt-in verifiers were both rerun successfully against the final
wheel. The runtime verifier used the actual refreshed Claude plugin cache:

```text
.venv/bin/python tests/verify_plugin_install.py --wheel dist/novel_creator-0.8.0-py3-none-any.whl --plugin .cache/marketplace-implementation/claude-final/plugins/cache/novel-creator-marketplace/novel-creator/0.8.0 --report .cache/marketplace-implementation/runtime-final.json
.venv/bin/python tests/verify_marketplace_previous.py --wheel dist/novel_creator-0.8.0-py3-none-any.whl --previous-wheel .cache/marketplace-implementation/novel_creator-0.7.2-py3-none-any.whl --report .cache/marketplace-implementation/previous-072-final.json
```

Both exited 0 with JSON `ok: true`, binding the final candidate wheel SHA-256
`7f6602edd121e8bdcd2e2e3a3c73a554eac48cbc337c4acc7e9333f3b1145e6a`.
`runtime-final.json` records:

- Created and reused an isolated 0.8.0 runtime with isolated dependency checks.
- Created English and Icelandic dual-host/plugin notebooks at Unicode paths.
- Verified two root instruction files, twelve role definitions, no duplicate
  local skills, resolved links and clean initialized Git state in each book.
- Confirmed notebook update refuses this layout without changing files or Git
  state.

`previous-072-final.json` records verification of the public 0.7.2 wheel against
frozen SHA-256 `8ee343c10bfcc8129d860a8502c669856deaa92f62b5059f915a4027fc11c9f5`,
installation of that actual old product and English/Icelandic standalone setup.
Candidate 0.8.0 preview/application preserved story files, custom instruction
prefixes, HEAD and exact unrelated staging; subsequent preview was current.
No integration marker was silently added.

The maintained helpers are
[verify_plugin_install.py](../verify_plugin_install.py) and
[verify_marketplace_previous.py](../verify_marketplace_previous.py). Each accepts
`--wheel`, `--plugin` and `--report`; the latter also accepts `--previous-wheel`
for a local file with the same frozen identity. They derive defaults from their
own repository location and use disposable runtimes/books and process-local Git
identities. Syntax and argument-help checks also passed; see
[development commands](../../docs/development.md#plugin-artifacts-and-installation-checks).
Earlier prototype reports (`runtime-initial.json`, `previous-072.json`) remain
historical observations; the final reports above supersede them for these
candidate artifacts.

## Native Claude lifecycle probe

`qualify_claude_lifecycle.py` and `claude-lifecycle.json` record an actual isolated
Claude Code 2.1.322 marketplace ZIP install, a **synthetic metadata-only** update
from 0.8.0 to 0.8.1 through marketplace/plugin update commands, and uninstall.
Complete synthetic notebook file and Git snapshots stayed identical after
update and removal. All host settings were isolated. This establishes scoped
data preservation for those operations; it does not qualify a real 0.8.1
release, runtime compatibility after an upgrade or authenticated conversation.

## Remaining qualification

- CI, the literal Bash guide journey and remaining source-bound release workflow
  gates are pending. The completed local Linux checks do not establish full
  release qualification.
- Native Windows execution and full Windows release qualification remain
  pending. CLI/resource changes require full coverage under the
  [source-bound policy](../../docs/testing-and-completion-guide.md#windows-release-selection).
- Authenticated Codex/Claude Code conversations, GUI skill discovery, native
  specialist controls, actual language/literary quality and voice behavior remain
  unverified. No model keys or new account approvals were requested.
- Marketplace adoption for existing books, legacy host port, macOS, MCP and
  public-directory submission are deferred. Publication, public install/hash
  verification and release tag creation are not authorized or performed here.
