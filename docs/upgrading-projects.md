# Upgrade an existing project

Installing Novel Creator updates the Python package. Project-local skills and
instructions require an explicit project update as well. Keep the configured
Python environment outside the novel and open the intended novel folder in Codex.
Do not initialize over an existing novel or convert formats to obtain a skill.

[0.10.1](releases/0.10.1.md), published 2026-11-15, is the latest verified
published package. It clarifies local report coverage and notebook session,
save/checkpoint and handoff guidance, with a read-only local notebook review.
Install the exact published version in your configured environment:

```text
python -m pip install --upgrade novel-creator==0.10.1
```

New projects receive the resources appropriate to their format at setup.
Existing projects need the format-specific updates below; package installation
alone does not refresh their pinned resources.

## Session guidance in 0.10.1

Release 0.10.1 provides an explicit [preview/apply manual procedure](session-guidance-upgrade.md)
for existing format-1 notebooks in all supported host/skill-source/language layouts.
It refreshes only four provenance-verified shared workflows and appends bounded
root routing, preserving project skills, roles and custom instructions. Package
installation alone leaves notebook snapshots unchanged; follow that procedure
and host reread/reload guidance after installing the reviewed package. First
install missing debugging prerequisites with `novel-creator debug setup --novel PATH --json`
if needed; this setup does not replace differing existing debugging guidance.
Save the exact linked snippet outside the notebook, pause editing and run it
with the notebook itself as the working directory:

```text
python /absolute/path/session-guidance-upgrade.py preview
python /absolute/path/session-guidance-upgrade.py apply PREVIEW_ID REVIEWED_HEAD
```

Review the package/resource location, changed paths and returned preview ID/HEAD
before applying. Customized workflows/routing, stale inputs and unsafe paths
refuse; the procedure makes no Git commit. Review partial writes on interruption
and take a fresh preview after reconciliation. It supports English/Icelandic,
Codex/Claude Code/both and project/plugin layouts; update/enable the matching
plugin first where used. Reread selected root instructions and linked workflows,
inspect skills/links and use the host's supported reload/reopen controls, possibly
a new chat. File checks do not prove native reload, voice delivery or specialist
behavior. Unsaved chat drafts have no guaranteed recovery.

Legacy novels use their separate framework update below; the notebook procedure
refuses retained legacy or mixed-format state. A manually migrated mixed-format
book needs separate adapter review. The older focused `notebook update` command
below does not refresh all session guidance or adopt marketplace routing.

## 0.9.0 character development

With the installed package, explicitly update the selected notebook.
Package installation alone leaves its resources unchanged.

For an original standalone Codex/project notebook (no integration marker), use
the preview/apply commands under [Existing Markdown notebooks](#existing-markdown-notebooks)
with the CLI's focused method updater (introduced in 0.9.0). It additionally
installs Character development, its workflow and absent prerequisites,
appends a separately protected approval section, and
refreshes only the provenance-verified public Help catalog. Customized Help and
differing feature resources block before application; LF/CRLF alone is harmless.

For Codex, Claude Code or both with a valid nondefault integration marker,
use the [manual character-development procedure](character-development.md#manually-install-into-an-existing-format-1-notebook).
An explicit manual alternative is also available for the default layout. It
preflights all selected root files, installs rendered project skills or uses
the enabled upgraded plugin without duplicates, and adds only the feature
workflow and bounded root approval sections. It preserves the older Help catalog;
consult the root routing and actual enabled entry to discover the new method.
Do not use the unsupported updater or remove a marker for these layouts.
Neither route adopts plugins, replaces broad instructions or changes story bytes,
existing history or unrelated staging. Review actual changed paths after completion.

After updating, have the active host reread the selected `AGENTS.md`/`CLAUDE.md`,
entry and workflow. Use actual host reload/reopen controls if available, possibly
a new chat. For plugin books update/enable the matching plugin first. Verify
`$novel-character-develop` (standalone Codex), `/novel-character-develop`
(standalone Claude Code), `$novel-creator:novel-character-develop` (Codex plugin)
or `/novel-creator:novel-character-develop` (Claude Code plugin) as applicable.
Installed files do not prove native discovery or reload; chat-only drafts have
no guaranteed recovery. Legacy novels receive no new profile-development method.

## Marketplace integration (0.8.0)

New notebooks can opt into the
[marketplace plugin](plugin-marketplaces.md). New and existing legacy novels
remain standalone. Existing notebooks keep their installed host routing and
project-local resources; original Codex/project notebooks retain the focused
Clarify/Analyze/Help and Character development update procedure below with the
installed CLI. This focused command is separate from the session-guidance refresh.

This updater refuses notebooks with a nondefault host/plugin integration marker
at `.novel-notebook/integration.json` before writing. It is not an adoption tool;
do not add/remove the marker or reinitialize an existing book to bypass it.
Marketplace adoption remains deferred. The bounded manual Character development
update above supports existing plugin books; it does not migrate their whole snapshot.

Plugin updates replace cached entries; book workflows, role definitions and
instructions remain pinned. Python installation alone still does not update a
book. Plugin uninstall leaves book data/history and its independent runtime in
place. After a plugin update, reload it in the actual host, open the book folder
itself and reread its applicable `AGENTS.md`/`CLAUDE.md` and linked workflows.
Native discovery needs its own host check. For standalone projects, continue
the complete package → project preview/apply → Codex reload sequence below.

## Legacy novels

A legacy novel contains `.novel-creator/`. Ask the agent in that novel to preview
an update to the selected published version using `$novel-update` and its external
controller. The controller is the absolute path to the compatible Python
installation outside the novel;
retain the verified runtime interpreter if it differs:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.10.1 --json
```

Review the concrete target version, changed paths, blockers and HEAD. After
requesting that exact preview's application, use its returned preview ID and HEAD:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.10.1 --expected-head REVIEWED_HEAD --json
```

Follow the [existing update procedure](../workflows/getting-started.md#updating-an-existing-book),
including client closure for initial 0.1.0/0.2.0 updates, `--confirm-quiescent`
only after that confirmation, and external exact-operation recovery. Installing
the new package alone does not replace pinned files. See the
[release notes](releases/0.10.1.md) for compatibility and verification scope.

The update installs legacy versions of `$novel-clarify`, `$novel-analyze` and
`$novel-help` with linked workflows. In 0.7.2, Clarify offers labeled suggestions
and custom answers while keeping exact-exchange saving and writer authority.
Story records, manuscripts, custom instructions and unrelated staging are
preserved in the updater's dedicated framework commit. The selected current
framework also delivers its shared report builder and legacy debugging workflow;
it does not add notebook character-draft semantics or convert the format.
Analysis and help remain read-only passes, without session changes, input capture, journal saves or
automatic maintenance. A request to save findings remains separate work.

## Existing Markdown notebooks

A notebook contains `notebook/project.md` and `.novel-notebook/`. This older
focused method/prerequisite updater supports the original Codex/project layout;
for revised 0.10.1 session guidance use the separate procedure above. Use the
installed CLI from your configured environment to preview the selected notebook:

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
notebook resource. Version 0.9.0 additionally installs Character development and
its approval section and refreshes provenance-verified public Help, as described
[above](#090-character-development).

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
`$novel-clarify`, `$novel-analyze`, `$novel-help` and, for updated notebooks,
`$novel-character-develop`. Open the novel itself,
not just a parent folder. Native Codex Desktop discovery remains a separate host
check; filesystem tests do not prove the menu reloaded.

## Unreleased session issue retrospectives

This feature is current-source work, **not included in published 0.10.1**.
Package/plugin installation leaves pinned project snapshots unchanged. Once a
future package containing the feature is qualified, install that exact version
in the intended isolated controller environment first.

Existing **legacy novels** use the ordinary external-controller framework update
preview/application above, selecting that future newer version. Review/apply the
exact preview/HEAD; it delivers shared retrospective guidance and the legacy
`.agents/skills/novel-retro/SKILL.md`. Existing story/history/custom-instruction
protections and historical recovery fences remain. No conversion is required.
Do not apply an invented future version to a real novel from this checkout.

Existing **format-1 notebooks**, including standalone pre-integration-marker
books and Codex/Claude/both project/plugin layouts, use current source or an
isolated qualified artifact containing this command:

```text
novel-creator retro issue setup --novel PATH --json
novel-creator retro issue setup --novel PATH --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
```

Preview binds all inspected input bytes/identities, rendered output and HEAD.
Apply installs the retrospective snapshot and project skill (or plugin routing),
refreshes only recognized shipped debugging/help/conversation guidance, preserves
arbitrary root custom bytes and establishes the notebook local ignore rule.
Conflicting custom resources, stale previews, hardlinks and redirected paths
refuse safely. Partial application preserves completed files: inspect, take a
fresh preview and explicitly apply the remainder. Story, index and history are
preserved; no log conversion, debug relocation, novel save or commit occurs.
Legacy-only books use the normal framework updater, not notebook setup.

New **legacy novels** initialized from the future qualified package bundle the
workflow and legacy adapter skill. New **notebooks** bundle the snapshot/project
skill or selected plugin routing. Plugin delivery keeps its notebook-only scope.
After each format's install/update, verify the actual skill file and links:
`.agents/skills/novel-retro/SKILL.md`, `.claude/skills/novel-retro/SKILL.md`, or
enabled plugin `novel-retro` plus the selected notebook snapshot. Reread/reload
root instructions and host skills before invoking them. Python imports/file
checks do not prove native Codex/Claude discovery. Checkpoint resource changes
only through the normal authorized workflow; package installation is insufficient.

Historical recovery uses `retro enable --novel PATH --checkout RECORDED_CHECKOUT
--recovery-only --json`, then explicitly requested old-run resume/release only.
It requires an authentic prior matching grant, creates no new grant and never
authorizes issue publication or new PR work.

The older focused notebook updater and `debug setup` may add an absent passive
retrospective snapshot to keep current guide links complete. This alone installs
no novel-retro skill, opts into nothing and grants no publication/upload authority.
The issue setup also supplies absent trusted writing-guide prerequisites for
older format-1 books, preserving existing custom prerequisite guides. Use its
explicit preview/application to install the complete issue entry and routing.
