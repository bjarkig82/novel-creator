# Upgrade an existing project

Installing Novel Creator updates the Python package. Project-local skills and
instructions require an explicit project update as well. Keep the configured
Python environment outside the novel and open the intended novel folder in Codex.
Do not initialize over an existing novel or convert formats to obtain a skill.

The 0.7.1 commands below are usable after publication. During candidate preparation,
use the candidate installation instead of claiming PyPI availability.

```text
python -m pip install --upgrade novel-creator==0.7.1
```

## Legacy novels

A legacy novel contains `.novel-creator/`. Ask the agent in that novel to preview
an update to 0.7.1 using `$novel-update` and its external controller. Review the
concrete target version, changed paths, blockers and HEAD, then request that exact
preview's application. Follow the [existing update procedure](../workflows/getting-started.md#updating-an-existing-book),
including client closure for initial 0.1.0/0.2.0 updates and exact-operation
recovery. Installing the new package alone does not replace pinned files.

The update installs legacy versions of `$novel-clarify`, `$novel-analyze` and
`$novel-help` with their linked workflows. It preserves story records, manuscripts,
custom instructions and unrelated staging in the updater's dedicated framework
commit. Clarification keeps exact-exchange saving and writer authority. Analysis
and help are explicit read-only passes, without session changes, input capture,
journal saves or automatic maintenance. A later request to save findings is
separate work under the ordinary saved workflow.

## Existing Markdown notebooks

A notebook contains `notebook/project.md` and `.novel-notebook/`. Use the installed
0.7.1 CLI from your configured environment to preview the selected notebook:

```text
novel-creator notebook update --path "/path/to/My Novel" --json
```

On Windows, use your notebook's actual path, such as `C:\Novels\My Novel`.
Review the changed paths and any blockers. Use the returned preview ID and HEAD:

```text
novel-creator notebook update --path "/path/to/My Novel" --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
```

This is an additive retrofit for Clarify, Analyze and Help, including required
linked guidance and instruction routing. It does not replace every older notebook
resource. It creates missing resources, accepts byte-identical resources and
refuses to overwrite differing customized resources. Existing `AGENTS.md` text is
preserved; a bounded routing block is added when needed. Story notes, manuscripts
and existing Git history are preserved. The command does not stage, commit or
push; review the framework changes and checkpoint them with ordinary scoped Git
tools. Preserve unrelated staged work.

A stale preview, changed HEAD, unsafe path or resource conflict stops application.
Resolve the reported conflict without blindly replacing custom content, then
request a fresh preview. An interrupted retrofit can leave partial resource
installation; preserve those files and rerun preview to finish the remaining
additions. Do not claim a partial installation is ready.

## Reload in Codex

After verified completion, have the agent reread the novel's instructions and
linked workflows. Reload or reopen that project in Codex so project skills can
be discovered, then search for `$novel-clarify`, `$novel-analyze` and `$novel-help`.
Open the novel itself, not just a parent folder. Check the actual `.agents/skills/`
files when diagnosing missing entries. Native Codex Desktop discovery remains a
separate host check; filesystem tests do not prove the menu reloaded.
