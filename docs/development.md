# Development

This is a single-maintainer Python project. Use a short plan when useful, make a
focused change, run relevant checks and review the diff. Small fixes need no
separate planning document. Repository instructions are in [AGENTS.md](../AGENTS.md).
The [functionality guide](functionality.md) describes current behavior and limits;
writer onboarding starts at [start here](../workflows/start-here.md).

## Local setup

Use Python 3.11+ and Git 2.39+. From the checkout on Linux Bash:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m novel_creator --help
python -m unittest tests.unit.test_notebook_contract -q
```

The test command is a concrete focused example. Select the modules or individual
cases affected by your change and their direct dependencies, following the
[focused testing policy](../AGENTS.md#focused-testing-policy). Expand focused
checks if failures or affected behavior warrant it. Documentation-only changes
normally need reference/link and diff whitespace checks.

On Windows PowerShell, create the environment with `py -3 -m venv .venv` and
activate `.venv\Scripts\Activate.ps1`. If activation is blocked, invoke
`.venv\Scripts\python.exe` directly; no execution-policy change is required.
Use shell-appropriate quoting and disposable novel destinations outside this
checkout and every other Git repository. Initialization requires an existing
Git author/committer identity and does not set one globally.

Tests use temporary repositories and local test identities; they need no model
credentials. Host conversations require the actual Codex capabilities documented
by the installed adapter. Do not copy credentials or disable sandboxing to make
a test work. On Windows, if temporary-directory access is blocked, select an
ordinary writable temporary location for the test process and retain the failure
and environment details. Some real-host saves may require scoped filesystem access.

### Retrospective network settings

Optional legacy retrospective Git and GitHub CLI subprocesses preserve the host's
existing `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` and `NO_PROXY` settings, including
their lowercase forms. They also preserve `SSL_CERT_FILE`, `SSL_CERT_DIR`,
`REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE`, `GIT_SSL_CAINFO` and `GIT_SSL_CAPATH` for
custom certificate authorities. These settings supplement existing authentication;
they do not configure credentials or grant network access.

The subprocess environment remains an explicit allowlist. Caller environment
overrides for the repository, GitHub host, Git configuration and TLS verification
disabling are excluded. Global/system Git configuration stays disabled and prompts
stay off. A proxy or certificate failure still stops the contribution operation;
inspect it without exposing proxy credentials, tokens or private writing.

Synthetic child-process regression checks require no GitHub requests:

```bash
python -m unittest tests.contract.test_retro_transport tests.contract.test_retro_github -q
```

## Packaging

For resource-inclusion changes, build the affected artifacts and perform targeted
content and isolated install checks for the changed resources in both wheel and
source distribution. Select checks that exercise the affected packaging behavior.
The complete wheel verifier below also runs broad legacy and update journeys;
it is a release gate, not a routine check for each task, review, commit or push.

For new package release preparation before publication (or an explicit user
request), run the full Linux suite and complete wheel verification from the configured
environment. Windows runs full or compatibility coverage according to the
[source-bound release policy](testing-and-completion-guide.md#windows-release-selection);
use candidate input `windows_suite: full` to request full Windows coverage.
Compatibility coverage does not establish full Windows qualification.
The local full-suite/build commands are:

```bash
python -m unittest discover -q
python -m pip wheel . --no-deps --wheel-dir dist
python tests/verify_wheel.py dist/novel_creator-0.8.0-py3-none-any.whl
```

Use the actual versioned filename produced by the build. The wheel verifier
installs outside the checkout and checks resource bytes and independent project
behavior. The release workflow also checks source distributions and production
installation. Preserve all release workflow gates and any required full coverage
checks. Local builds do not establish publication or actual Codex behavior.
See [testing guidance](testing-and-completion-guide.md) and
[the release workflow](../.github/workflows/package-release.yml).
For every requested PyPI release, prepare versioned notes and update the
[release history](releases/README.md) following the
[release documentation requirements](../AGENTS.md#pypi-releases).

### Plugin artifacts and installation checks

Version 0.8.0 is an unpublished candidate; 0.7.2 remains the latest verified PyPI
release. Generate plugin manifests/catalogs and deterministic archives from the
package version, then check for drift without writes:

```text
python scripts/build_plugins.py
python scripts/build_plugins.py --check
```

The default outputs are `dist/novel-creator-plugin-0.8.0.zip` (plugin root) and
`dist/novel-creator-marketplace-0.8.0.zip` (both catalogs and the plugin tree).
Use `--output DIR` for a disposable destination. Both archives exclude runtime
caches, credentials and bytecode. `tests.contract.test_plugin_bundle` checks
manifest/version consistency, all fifteen skills and relative links, actual ZIP
membership, wheel resources and source-distribution inputs; it also rebuilds the
plugin from the extracted source distribution. Focused checks are:

```text
python -m unittest tests.unit.test_plugin_bootstrap tests.contract.test_plugin_bundle tests.integration.test_notebook_hosts tests.integration.test_notebook_update -q
```

The following opt-in helpers perform real installations into temporary runtimes
and books, outside the checkout. They can download dependencies; the previous
release helper also downloads the frozen hash-verified public 0.7.2 wheel unless
`--previous-wheel PATH` supplies it locally. They are not unittest discovery
modules. They need Python 3.11+, Git 2.39+ and Windows/Linux; they set disposable
Git identities only in subprocess environments and do not modify global settings.

```text
python tests/verify_plugin_install.py --wheel dist/novel_creator-0.8.0-py3-none-any.whl --report /tmp/plugin-install.json
python tests/verify_marketplace_previous.py --wheel dist/novel_creator-0.8.0-py3-none-any.whl --report /tmp/marketplace-previous.json
```

On Windows choose a writable report path such as `$env:TEMP\plugin-install.json`.
Both helpers accept `--plugin PATH`; point it at the actual installed cache to
qualify cached bytes rather than the default source plugin. The first verifies
runtime creation/reuse, English/Icelandic dual-host plugin notebooks, links,
clean Git state and updater refusal without mutation. The second creates real
0.7.2 standalone notebooks, applies the installed candidate's supported update,
and checks custom instructions, story files, HEAD and unrelated staging with no
implicit marketplace adoption. These checks do not prove GUI skill discovery,
native conversations or writing quality.

Use the [marketplace guide](plugin-marketplaces.md) for host installation and
candidate wheel bootstrap. In release preparation, preserve the full Linux
suite, complete rebuilt-wheel verifier and all existing workflow gates. CLI and
resource changes select full Windows qualification under the
[Windows release policy](testing-and-completion-guide.md#windows-release-selection).
See the [candidate evidence ledger](../tests/evaluations/marketplace-0.8.0.md).

### Completing GitHub release assets

The manually dispatched [GitHub assets workflow](../.github/workflows/github-release-assets.yml)
completes the already published 0.8.0 release using the normal Actions token.
Its [reviewed selection](../.github/release-assets-0.8.0.json) deliberately pins
candidate run 43218783499, attempt 1, artifact 13945000853, the qualified source,
successful publish run 43230160921 attempt 2, annotated tag object and ZIP hashes.
These are version-specific recovery pins; dispatch has no inputs. It does not
publish to PyPI or replace the existing package release gates.

The helper runs the qualified source's `verify-remote` against the downloaded
candidate, requires successful Windows/Linux public-install checks at the same
source, verifies the remote annotated tag and both public PyPI archives, and
rebuilds the two deterministic plugin ZIPs from the verified candidate sdist.
The workflow's current checkout supplies only the helper and reviewed selection;
it supplies no release payload. An existing public release is reused only after
its exact four-asset inventory and downloaded bytes match. Missing or different
assets fail without replacement; tags are never created, moved or deleted.

For a local read-only rehearsal, use a separate checkout at the selected source,
the downloaded candidate directory, a fresh output directory and a GitHub token
with read access:

```text
python scripts/github_release_assets.py --selection .github/release-assets-0.8.0.json --source QUALIFIED_CHECKOUT --candidate CANDIDATE_DIR --output FRESH_OUTPUT_DIR
python -m unittest tests.contract.test_github_release_assets -q
```

Only `--publish` permits creation of the GitHub release and upload of its four
assets. The helper never overwrites an existing release asset. A partial or
mismatched release requires investigation; rerunning cannot silently repair it.
These checks remain automated evidence, with the native host limits stated in
the generated release notes.

## Compatibility and evidence

Preserve legacy pinned resources, record identity, history, writer authority and
unrelated staged work. A package upgrade does not update a book. Notebook setup
is independent of legacy persistence; do not introduce transcript capture or
legacy runtime dependencies into native notebook writing.

Keep checks proportional to the change. Record failures and unsupported coverage
honestly; structural validity does not establish narrative quality. Read/save
latency targets were withdrawn by the owner; timings remain informational. The
published 0.6.0 release adds focused context retrieval, not a measured voice speed claim.
Use fresh `context --view working` and targeted complete records for legacy turns;
the unchanged default full view remains available for compatibility. Installed
wheel/clean-package probes exercise these views in the real pinned runtime and
check inclusion of `memory.py`. See the
[working-context guide](../workflows/working-context.md) and
[release notes](releases/0.6.0.md). No novice recruitment is required for this
single-user project.

Detailed historical observations remain available in
[legacy functional qualification](../tests/evaluations/final-functional-qualification-20261028.md),
[host capture evidence](../tests/evaluations/host-capture.md),
[update qualification](../tests/evaluations/existing-book-update-qualification.md),
[update host evidence](../tests/evaluations/existing-book-update-host.md),
[retrospective qualification](../tests/evaluations/automatic-retrospectives-qualification.md)
and [notebook evidence](../tests/evaluations/agent-story-notebook.md).
Historical task numbers, blocked states and timing targets describe those runs;
use current functionality and evidence scope when reporting today's status.
