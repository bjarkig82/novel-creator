# Marketplace setup for new notebooks

Version **0.8.0 is published, 2026-11-12**; see the
[release notes](releases/0.8.0.md). Full Windows/Linux automated qualification,
public package installation and normal published-index bootstrap passed.
An isolated Claude Code GitHub marketplace installation reported fifteen skills.
Native Codex/Claude Code conversations, GUI discovery and specialist interaction
remain unverified; CLI installation and file checks do not establish them.

The plugin creates new independent Markdown notebooks. Existing notebook
adoption, a legacy-format host port, macOS, MCP and public-directory submission
are deferred. Existing stories continue through their installed standalone
instructions and [supported update paths](upgrading-projects.md).

## Install the plugin

Install from the GitHub repository. In Codex CLI 0.163.0 the install command
is `plugin add`:

```text
codex plugin marketplace add https://github.com/bjarkig82/novel-creator.git
codex plugin add novel-creator@novel-creator-marketplace
```

In Claude Code:

```text
claude plugin marketplace add bjarkig82/novel-creator
claude plugin install novel-creator@novel-creator-marketplace
```

Repository availability and PyPI availability are separate: installing the
plugin does not prove the matching Python package has been published.

The permanent plugin name is `novel-creator` and the catalog is
`novel-creator-marketplace`. Enable the plugin in your actual host and inspect
its available skills. It contains `setup` and fourteen writing entries; the six
writing roles are installed in the book during setup, so the plugin inventory
itself can report zero agents. Expected writing invocation syntax is Codex
`$novel-creator:novel-help` and Claude Code `/novel-creator:novel-help`.
Native menu discovery and these invocations still need confirmation in the
target hosts. Ordinary conversation can continue after setup.

## Create a notebook

Ask the enabled plugin to create a new English or Icelandic notebook, providing
an absolute destination and a working title. An idea is optional. Setup requires
Python 3.11+, Git 2.39+ and your existing Git author/committer identity. It checks
that the destination is new, its parent exists and it is outside every existing
Git repository. It does not request a model key or alter global Git settings.

The agent runs the plugin's standard-library bootstrap using a compatible
Python. Without `--wheel`, it installs the exact plugin manifest version from
PyPI through the configured package index:

```text
python /absolute/path/to/plugin/scripts/bootstrap.py --novel "/path/to/My Novel"
```

For optional development validation, a local checkout or extracted marketplace
archive can be added by absolute path instead of the GitHub repository. Supply
the exact matching local wheel to validate that artifact explicitly:

```text
python /absolute/path/to/plugin/scripts/bootstrap.py --wheel /absolute/path/to/novel_creator-0.8.0-py3-none-any.whl --novel "/path/to/My Novel"
```

Here `/absolute/path/to/plugin` is the installed plugin directory, not the
catalog root. Choose the actual compatible Python command on your system.
Bootstrap returns JSON containing `data.runtime_python`, `version` and `reused`.
The agent uses that returned interpreter to run:

```text
RUNTIME_PYTHON -m novel_creator notebook init "My Novel" --path "/path/to/My Novel" --language en --host both --skill-source plugin --json
```

Use `--language is` for Icelandic and optional `--title` for another working
title. The direct CLI also accepts `--host codex`, `--host claude` and
`--skill-source project`; omitting both options preserves the original
Codex/project setup. Never initialize over an existing notebook to change hosts.

The runtime is an isolated virtual environment for the exact plugin version,
outside the plugin cache and the book. Windows uses
`%LOCALAPPDATA%/NovelCreator/runtimes/0.8.0`; Linux uses
`$XDG_CACHE_HOME/novel-creator/runtimes/0.8.0`, falling back to
`~/.cache/novel-creator/runtimes/0.8.0`. Reuse checks the installed version,
dependencies and installation source; a local wheel's SHA-256 binds its
provenance. A changed candidate wheel or switching from wheel to PyPI needs a
separate cache location. Proxy, CA and package-index transport settings are
preserved while pip destination overrides are excluded. See the
[runtime reference](../plugins/novel-creator/references/setup.md).

If the pinned version is missing from the index, report that actual failure;
use a matching local wheel only when it is available for the intended setup.
To install or upgrade the separate package in your configured environment:

```text
python -m pip install --upgrade novel-creator==0.8.0
```

If setup fails, preserve its partial files and follow the reported recovery
instructions. Known same-source runtime setup can retry its owned partial
environment. Do not blindly delete runtime/book directories, remove an active
lock or repeat successful initialization. The bootstrap creates a runtime;
notebook initialization is a separate step.

## Write in the selected book

Open the initialized book folder itself in the host. Read its applicable
`AGENTS.md`/`CLAUDE.md`, linked workflow snapshots, `notebook/project.md` and
`notebook/working-summary.md` before continuing. Setup cannot guarantee an
automatic host project switch or access to another folder.

The fourteen methods cover book ideas, premises, characters, plots, settings,
outlines, role selection, scenes, chapters, research, review, clarification,
analysis and help. The six roles are orchestrator, brainstormer, researcher,
scene writer, chapter writer and reviewer. Their native selection and ongoing
specialist turns depend on the host. Help and Analyze remain read-only; Clarify
offers concise suggestions plus custom answers, and only clear writer choices
become accepted facts. Outline stays explicit-only. No per-turn Python or MCP
server is needed; writing uses the host's native file and Git tools.

Plugin notebooks contain host-specific root instructions and role files but no
duplicate `.agents/skills` or `.claude/skills`. Their
`.novel-notebook/integration.json` records the layout version, host selection and
skill source. Cached plugin entries select the intended book explicitly and use
its pinned `.novel-notebook/workflows/`, never a book inferred from the cache path.

## Updates and removal

A plugin update changes cached entries. It does not update a book's saved
workflow snapshots, instructions, role files, prose or Git history. Installing
or upgrading the Python package also leaves books unchanged. Uninstalling the
plugin leaves book data and its independent runtime in place; plugin entries
then require re-enabling a compatible plugin before use.

The notebook updater supports the original standalone Codex/project layout and
focused Clarify/Analyze/Help resources. It refuses host/plugin integration
layouts before writing and is not a marketplace adoption or snapshot updater.
There is no supported in-place adoption or snapshot migration for plugin books
in 0.8.0. Preserve their pinned workflows. Existing legacy books use
their existing reviewed updater; see the [upgrade guide](upgrading-projects.md).

See [release notes](releases/0.8.0.md),
[development checks](development.md#plugin-artifacts-and-installation-checks) and
[qualification evidence](../tests/evaluations/release-0.8.0.md) for exact scope.
