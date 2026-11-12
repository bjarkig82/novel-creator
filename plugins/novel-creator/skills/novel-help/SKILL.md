---
name: novel-help
description: Use when the writer wants help choosing a next step, asks how notebook commands work or what input they accept, or explicitly invokes the novel-help plugin skill in a format-1 story notebook.
---

# Help with notebook commands

First read and follow [project routing](../../references/notebook.md). Establish
the selected `novel_path`; all snapshot paths below are relative to
`<novel_path>/.novel-notebook/workflows/`, never this cached skill.

Read and follow the shared `help.md` snapshot (help workflow)
and `agents.md` snapshot (role and handoff rules).
 No input is required;
optional freeform input can be a command name, goal, topic or `commands`.
Explain actually installed entries and accepted input forms with copyable chat
examples. This pass is read-only: no automatic notes, files, staging, checkpoints,
task execution or native role changes. Example commands are not invocations.
Use actual native tools to read context and respect host permissions.
If the workflow or format-1 notebook is unavailable, explain the limitation and
preserve existing files; do not substitute legacy capture or convert the book.

Check actual enabled plugin inventory and read the relevant cached entry skills
plus selected book snapshots. Do not require book-local skill directories.
