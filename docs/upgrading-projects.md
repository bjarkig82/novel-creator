# Upgrade an existing project

Installing Novel Creator updates the Python package. Project-local skills and
instructions require an explicit project update as well. Keep the configured
Python environment outside the novel and open the intended novel folder in Codex.
Do not initialize over an existing novel or convert formats to obtain a skill.

[0.7.1](releases/0.7.1.md) is the latest published package. The
[0.7.2 candidate](releases/0.7.2.md) adds suggested clarification answers and
custom input in both formats. The version-pinned 0.7.2 commands below are usable
only after publication; during qualification use the candidate installation.

```text
python -m pip install --upgrade novel-creator==0.7.2
```

New legacy novels and new notebooks initialized with 0.7.2 receive the guidance
during setup. Existing projects follow the format-specific procedure below;
package installation alone does not refresh their pinned resources.

## Legacy novels

A legacy novel contains `.novel-creator/`. Ask the agent in that novel to preview
an update to 0.7.2 using `$novel-update` and its external controller. The controller
is the absolute path to the compatible Python installation outside the novel;
retain the verified runtime interpreter if it differs. After publication:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.7.2 --json
```

Review the concrete target version, changed paths, blockers and HEAD. After
requesting that exact preview's application, use its returned preview ID and HEAD:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.7.2 --expected-head REVIEWED_HEAD --json
```

Follow the [existing update procedure](../workflows/getting-started.md#updating-an-existing-book),
including client closure for initial 0.1.0/0.2.0 updates, `--confirm-quiescent`
only after that confirmation, and external exact-operation recovery. Installing
the new package alone does not replace pinned files.

The update installs legacy versions of `$novel-clarify`, `$novel-analyze` and
`$novel-help` with linked workflows. In 0.7.2, Clarify offers labeled suggestions
and custom answers while keeping exact-exchange saving and writer authority.
Story records, manuscripts, custom instructions and unrelated staging are
preserved in the updater's dedicated framework commit. Analysis and help remain
read-only passes, without session changes, input capture, journal saves or
automatic maintenance. A request to save findings remains separate work.

## Existing Markdown notebooks

A notebook contains `notebook/project.md` and `.novel-notebook/`. Use the 0.7.2
CLI from your configured environment to preview the selected notebook:

```text
novel-creator notebook update --path "/path/to/My Novel" --json
```

On Windows, use your notebook's actual path, such as `C:\Novels\My Novel`.
Review the changed paths and any blockers. Use the returned preview ID and HEAD:

```text
novel-creator notebook update --path "/path/to/My Novel" --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
```

The update adds missing Clarify, Analyze and Help resources, linked prerequisites
and instruction routing. Version 0.7.2 also replaces only the original published
0.7.0/0.7.1 clarify skill and workflow when their normalized hashes establish
ownership. LF/CRLF differences alone do not make those files customized. Current
identical resources are accepted. Other differing resources, including customized
clarify files, block replacement; the update does not replace every historical
notebook resource.

Existing `AGENTS.md` text is preserved; a bounded routing block is added when
needed. Story notes, manuscripts and existing Git history are preserved. The
command does not stage, commit or push; review the framework changes and
checkpoint exact changed paths with ordinary Git tools. Preserve unrelated staging.

A stale preview, changed HEAD, unsafe path or resource conflict stops application.
Resolve the reported conflict without blindly replacing custom content, then
request a fresh preview. An interruption can leave completed additions or
replacements; preserve them and rerun preview to finish remaining changes.
Inspect any partially written conflicting file rather than removing ownership
checks. Do not claim a partial installation is ready.

## Reload in Codex

After verified completion, inspect the actual `.agents/skills/novel-clarify/SKILL.md`
and its linked workflow for the suggested-answer and custom-input guidance. Have
the agent reread the novel's instructions and linked workflows. Reload or reopen
that project in Codex so project skills can be discovered, then search for
`$novel-clarify`, `$novel-analyze` and `$novel-help`. Open the novel itself,
not just a parent folder. Native Codex Desktop discovery remains a separate host
check; filesystem tests do not prove the menu reloaded.
