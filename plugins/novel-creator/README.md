# Novel Creator plugin

Create independent story notebooks and use focused writing methods in Codex or
Claude Code. The 15 writing entries share creative workflows saved with the
selected book; the setup entry creates new format-1 notebooks for both hosts.
The permanent plugin name is `novel-creator` in `novel-creator-marketplace`.

Candidate version 0.9.0 is unpublished; 0.8.0 is the published release. It supports Windows and Linux with Python >=3.11 and Git >=2.39.
Runtime setup normally installs the exact manifest version from PyPI. Use
`--wheel PATH` for an unpublished local candidate or explicit local
validation; report the actual setup error if the pinned version is unavailable.
No provider keys, MCP server, per-turn Python runtime, or global settings are required.

Start with `setup`, using the enabled host's skill discovery. Writing examples:
Codex `$novel-creator:novel-character`; Claude Code
`/novel-creator:novel-character`. Ordinary conversation can continue after setup.
Project creation does not automatically switch the host to the new folder.
Native specialist controls depend on the host's actual available capabilities.

The [setup skill](skills/setup/SKILL.md) and [runtime reference](references/setup.md)
describe prerequisites and safe recovery. The [project routing reference](references/notebook.md)
explains explicit book selection and cached skill paths. Keep the plugin cache
separate from story folders. Existing legacy novels and adoption of standalone
notebooks are deferred; setup creates only a new destination.

Help and Analyze are read-only; Clarify saves clear answers one question at a
time; Outline requires explicit invocation. Other writing entries preserve
writer authority, existing prose and scoped history through book snapshots.

Character development returns one bounded numbered batch of proposed profile
prose. Drafts and revisions stay in chat until explicit approval to save current
or selected additions. Use `$novel-creator:novel-character-develop` in Codex or
`/novel-creator:novel-character-develop` in Claude Code. Existing plugin books
need the repository's `docs/character-development.md` manual snapshot update;
upgrading cached entries alone leaves their snapshots and instructions pinned.
