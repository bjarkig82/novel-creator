---
name: setup
description: Use when the writer wants to create a new independent Novel Creator story notebook through the enabled plugin.
---

# Set up a new story notebook

Use the [setup reference](../../references/setup.md) and the bundled
[bootstrap script](../../scripts/bootstrap.py). This plugin supports Windows and
Linux, Python >=3.11 and Git >=2.39. Find a compatible Python interpreter using
actual host tools; virtual-environment activation is not required. On Windows
try `py -3.11` or a compatible installed Python; on Linux try `python3.11` or
another verified `python3`. Verify versions rather than assuming command names.

Establish an absolute destination, working title and language (`en` or `is`)
from the writer's request and current context. Ask only for missing choices.
The parent must exist and the destination must be new: never initialize an
existing or occupied path, the framework repository, or a folder within another
Git repository. Check Git identity with read-only `git var GIT_AUTHOR_IDENT`
and `git var GIT_COMMITTER_IDENT` from the intended parent, without changing it.
If absent, explain the missing Git identity so the writer can configure it; do
not modify global, account or project Git configuration. Do not request API keys,
provider authentication or registration for this package.

Run the bundled script by the chosen interpreter, never relying on its
executable bit: `<python> <cached-plugin>/scripts/bootstrap.py --novel <PATH>`.
Without `--wheel`, bootstrap installs the exact plugin manifest version from PyPI.
Use `--wheel <candidate.whl>` for an unpublished local candidate or when
explicitly validating a local artifact. Do not infer publication from the plugin
being installed: if the pinned version is missing from the index, report that
actual failure and use a matching local wheel only when one is available for
the intended setup. Check the JSON result and use its returned
`data.runtime_python`, not an inferred interpreter, for exactly one initialization:

```text
<runtime_python> -m novel_creator notebook init <NAME> --path <PATH> --language en --host both --skill-source plugin --json
```

Replace `en` with `is` when selected. Add `--title <TITLE>` when the working
title differs from NAME. Pass title and paths as separate arguments using the
host's proper quoting; preserve spaces and non-ASCII characters. On failure,
preserve partial setup, explain the reported cause and recovery, and
never blindly delete or retry initialization over an existing directory. A
successful init is not repeated. Runtime setup may safely retry its own known
partial runtime as described by the bootstrap result.

After success, retain the returned novel_path and runtime_python in context.
Read the generated applicable instructions, workflow snapshots,
`notebook/project.md`, `notebook/working-summary.md` and relevant notes from that
novel_path before any creative reply. Continue in the same chat using native
file/Git tools and [project routing](../../references/notebook.md). A story idea
is optional. Do not claim automatic host project switching; if access is
unavailable explain that the writer must select/open the new book folder.
