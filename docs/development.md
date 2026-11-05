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
request), run the full suite and complete wheel verification from the configured
environment:

```bash
python -m unittest discover -q
python -m pip wheel . --no-deps --wheel-dir dist
python tests/verify_wheel.py dist/novel_creator-0.4.0-py3-none-any.whl
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

## Compatibility and evidence

Preserve legacy pinned resources, record identity, history, writer authority and
unrelated staged work. A package upgrade does not update a book. Notebook setup
is independent of legacy persistence; do not introduce transcript capture or
legacy runtime dependencies into native notebook writing.

Keep checks proportional to the change. Record failures and unsupported coverage
honestly; structural validity does not establish narrative quality. Read/save
latency targets were withdrawn by the owner; optimization is deferred and timings
are informational. No novice recruitment is required for this single-user project.

Detailed historical observations remain available in
[legacy functional qualification](../tests/evaluations/final-functional-qualification-20261028.md),
[host capture evidence](../tests/evaluations/host-capture.md),
[update qualification](../tests/evaluations/existing-book-update-qualification.md),
[update host evidence](../tests/evaluations/existing-book-update-host.md),
[retrospective qualification](../tests/evaluations/automatic-retrospectives-qualification.md)
and [notebook evidence](../tests/evaluations/agent-story-notebook.md).
Historical task numbers, blocked states and timing targets describe those runs;
use current functionality and evidence scope when reporting today's status.
