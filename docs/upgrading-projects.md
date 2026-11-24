# Upgrade an existing project

Installing Novel Creator updates the Python package. Project-local skills and
instructions require an explicit project update as well. Keep the configured
Python environment outside the novel and open the intended novel folder in Codex.
Do not initialize over an existing novel or convert formats to obtain a skill.

<a id="timeline-recap-guidance-in-current-source"></a>

## Upgrade to 0.10.6

Install [0.10.6](releases/0.10.6.md), published on 2026-11-24, in a Python 3.11+
environment outside the book.
Use that interpreter for the commands below. Git 2.39+ is required.

```text
python -m pip install --upgrade novel-creator==0.10.6
```

**New projects.** For a legacy novel, run `python -m novel_creator init "My Novel"`
from a suitable parent directory. It includes the revised retrospective workflow.
For a new format-1 notebook, run
`python -m novel_creator notebook init "My Novel" --language en --host codex --skill-source project`.
Select the intended language (`en` or `is`), host (`codex`, `claude` or
`both`) and skill source (`project` or `plugin`). New notebooks also receive
the revised recap and delegated character-development guidance. Enable the
matching 0.10.6 plugin for plugin notebooks.

**Existing legacy novel.** Use the external 0.10.6 interpreter as `CONTROLLER`,
the book's verified interpreter as `RUNTIME` and its folder as `BOOK`. Review
the preview, resolve any blockers and apply with the reviewed ID and HEAD.
For an initial update from 0.1.0 or 0.2.0, close other book clients and add
`--confirm-quiescent` to the apply command after confirming they are closed.

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.10.6 --json
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.10.6 --expected-head REVIEWED_HEAD --json
```

The framework updater refreshes the pinned runtime and managed guidance in a
dedicated commit, preserving story content, custom instructions and unrelated
staging. Follow the [legacy update procedure](../workflows/getting-started.md#updating-an-existing-book).

**Existing format-1 notebook.** A package upgrade alone leaves local instructions
pinned. For a current 0.10.5 notebook, pause editing and follow these steps.

1. Preview issue setup and review the proposed paths, including the retrospective,
   conversation and help guides. Handle [customized workflows](#review-workflow-conflicts)
   before applying. For a stale preview, changed HEAD or redirected path, resolve
   the problem and preview again. Apply with the returned ID and HEAD.

   ```text
   python -m novel_creator retro issue setup --novel BOOK --json
   python -m novel_creator retro issue setup --novel BOOK --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
   ```

2. Complete the [character guidance refresh](character-development.md#refresh-an-existing-notebook-for-delegated-proposal-saves).
   Use the **same 0.10.6 interpreter** to create a disposable reference outside
   the novel with matching language, host and skill source. Compare the listed
   workflows, root Character development section, specialist role and project
   skill. Merge the remaining changes while preserving custom instructions.
   Plugin notebooks also need the matching 0.10.6 plugin installed and enabled.
   Neither step creates a story save or Git checkpoint. Review the diff and
   verify story content, history and unrelated staging are preserved.
3. Inspect the selected skill and role and follow their links in the actual
   book. Reopen the folder in Codex or Claude Code, reread its `AGENTS.md`
   and/or `CLAUDE.md`, and reload skills using host controls or a fresh chat.
   Use the same host reload after a legacy update.

The [topic-index checker](functionality.md#check-topic-index-counts-on-demand)
runs from the external runtime on new or existing format-1 notebooks without
the guidance refresh. Its report leaves book files and staging untouched.
The recap and delegated character guidance also apply to format-1 notebooks.
Use the [legacy writing workflows](../workflows/everyday-writing.md) in a legacy novel.

## Live debug snapshots and local retrospectives in 0.10.5

Install [0.10.5](releases/0.10.5.md), published on 2026-11-20, in a Python 3.11+
environment outside the book and use its interpreter for the rest of the update.
Git 2.39+ is required.

```text
python -m pip install --upgrade novel-creator==0.10.5
```

| Project | How to receive the retrospective update |
| --- | --- |
| New legacy novel | From a suitable parent directory, run `python -m novel_creator init "My Novel"`. The new novel receives the pinned runtime, updated legacy guides and retrospective skill. |
| Existing legacy novel | Use the external framework controller to preview and apply the update below. Keep the book's verified runtime interpreter. |
| New format-1 notebook | Run `python -m novel_creator notebook init "My Novel" --language en --host codex --skill-source project` from a suitable parent. Other supported settings are `--language is`, `--host claude` or `both`, and `--skill-source plugin` with the matching enabled plugin. |
| Existing format-1 notebook | Use the external 0.10.5 runtime to preview and apply issue setup below. It supports both languages, all three host selections and both skill sources. Also update and enable the matching plugin for plugin notebooks. |

**Existing legacy novel.** Use the external Python interpreter as `CONTROLLER`,
the book's verified interpreter as `RUNTIME` and its folder as `BOOK`. Review the
target version, paths, blockers and HEAD. Apply the returned preview ID and HEAD.
Follow any quiescence or recovery instructions in the
[legacy update procedure](../workflows/getting-started.md#updating-an-existing-book).

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.10.5 --json
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.10.5 --expected-head REVIEWED_HEAD --json
```

The update refreshes the managed workflows, skill and pinned runtime in a dedicated
framework commit. It preserves story records, manuscript files, custom instructions
and unrelated staging. The two project formats use their own update procedures.

**Existing notebook.** Review the resource paths first. For a current 0.10.4
notebook, issue setup refreshes `retrospective.md`, `conversation.md`,
`debugging.md` and `help.md`, the managed retrospective routing in the applicable
`AGENTS.md` or `CLAUDE.md`, and each installed project-local `novel-retro` skill.
It also refreshes the recognized session-guidance routing block if present.
Plugin notebooks use the enabled plugin's skill entries. For older projects
that still need earlier features or writing guidance, follow the relevant
historical sections below using their specified versions.

```text
python -m novel_creator retro issue setup --novel BOOK --json
python -m novel_creator retro issue setup --novel BOOK --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
```

The notebook update preserves story files, history, unrelated staging and custom
instructions outside the managed blocks. It makes no story save or Git checkpoint.
Customized managed resources, stale previews and unsafe paths require review before
a new preview. Current source builds offer a [workflow conflict preview](#review-workflow-conflicts).
Inspect the actual local skill or enabled plugin entry and its linked
workflows. Reopen the novel folder in the host, reread its applicable `AGENTS.md`
or `CLAUDE.md` and reload skills using the host's controls or a fresh chat. The
same inspection and reload applies to the legacy framework update. Native skill
reload and actual retrospective replies require observation in the host.

### Review workflow conflicts

In a read-only `retro issue setup --json` preview, `data.conflicts` lists the
customized managed workflows. Each entry gives the notebook-relative `path` and
the full shipped Markdown as `replacement`, rendered for the notebook's host
and skill source. The `data.changes` list shows other pending updates. Setup
refuses to apply any changes while a workflow conflict remains.

Save a copy of each customized guide and compare it with its `replacement`.
Decide which custom instructions to retain. To clear a conflict, put the shipped
replacement at the listed path, then take a fresh preview. Once the conflict
list is empty, review the changes and apply using that preview's ID and HEAD.
Keep retained instructions in separate project guidance where practical so
future upgrades can still recognize the shipped guide. If you restore edits to
a managed guide after setup, future previews will flag it again.

<a id="unreleased-brainstorming-continuity-guidance"></a>

## Story status in summaries and handoffs in 0.10.4

Install [0.10.4](releases/0.10.4.md), published on 2026-11-19, in a Python 3.11+
environment outside the book. Use its interpreter for the following commands.
Git 2.39+ is required. [Release evidence](../tests/evaluations/release-0.10.4.md)

```text
python -m pip install --upgrade novel-creator==0.10.4
```

For plugin notebooks, update and enable the matching 0.10.4 plugin in the
selected host. Installing Python or a plugin alone leaves each book's snapshots pinned.

| Project | How to receive the revised guidance |
| --- | --- |
| New legacy novel | From a suitable parent directory, run `python -m novel_creator init "My Novel"` to create an independent legacy novel. Its pinned workflows include `brainstorm.md` and `resume.md`. |
| Existing legacy novel | Use the external controller preview and apply below. Keep the book's verified runtime interpreter. The update creates a dedicated framework commit and preserves story records, custom instructions and unrelated staging. |
| New format-1 notebook | Run `python -m novel_creator notebook init "My Novel" --language en --host codex --skill-source project` from a suitable parent. Choose `en` or `is`, `codex`, `claude` or `both`, and `project` or `plugin` for your setup. The selected root instructions link to the revised shared `conversation.md`. |
| Existing format-1 notebook | From the external 0.10.4 environment use the issue-setup preview and apply below. This works for both languages and each host/skill source. Plugin notebooks use the enabled plugin's entries and need no project skill copies. |

**Existing legacy novel.** Set `CONTROLLER` to the
external interpreter, `RUNTIME` to the verified interpreter used by the book,
and `BOOK` to the project path. Review the target, changes, blockers and HEAD
before applying the exact preview. Follow any quiescence or recovery instructions
in the [legacy update procedure](../workflows/getting-started.md#updating-an-existing-book).

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.10.4 --json
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.10.4 --expected-head REVIEWED_HEAD --json
```

**Existing notebook.** Use the returned preview ID and HEAD, after reviewing its
resource paths. In an otherwise current 0.10.3 notebook, only
`.novel-notebook/workflows/conversation.md` changes. The update also offers
recognized missing issue-setup prerequisites on older notebooks. If you still
need the earlier session guidance, complete its [0.10.3 upgrade](#session-usability-guidance-in-0103)
in that version's environment first. The six-guide procedure belongs to that older
upgrade. Moving from a current 0.10.3 notebook to 0.10.4 needs only issue setup.

```text
python -m novel_creator retro issue setup --novel BOOK --json
python -m novel_creator retro issue setup --novel BOOK --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
```

Notebook setup makes no story save or Git checkpoint. Review the resulting diff.
Reconcile customized resources, stale previews or redirected paths, then preview
again. Inspect the actual skill files or enabled plugin entries and follow their
links to the selected workflows. Open the book folder in Codex or Claude Code,
reread its applicable `AGENTS.md` or `CLAUDE.md`, and reload the skills using
the host's controls or a fresh chat. Live voice behavior and native reload still
need observation in the host.

<a id="unpublished-session-usability-guidance"></a>

<a id="session-usability-guidance-in-0103-candidate"></a>

## Session usability guidance in 0.10.3

For this earlier upgrade, install `novel-creator==0.10.3` in an external environment.
Version 0.10.3 improves debug help/UTF-8 JSON recipes, suggestion adaptation,
readable individually addressable notes and retrospective publication handoffs.
Installing a package alone leaves book guidance pinned.

| Project case | Complete delivery sequence |
| --- | --- |
| New legacy novel | Install the selected package externally, then authorized normal legacy initialization. |
| Existing legacy novel, including 0.10.2 | External-controller framework update preview/apply targeting `--version 0.10.3`; inspect the preview and HEAD. No same-version bypass. |
| New format-1 notebook | Install the selected package and matching enabled plugin where selected, then normal notebook initialization. |
| Existing notebook, including 0.10.2 | Install externally and update/enable matching plugin where selected. Add side-character prerequisites only if missing. Run `retro issue setup` preview/apply **first**, then the exact six-guide preview/apply [procedure](session-guidance-upgrade.md). |

Issue setup refreshes retrospective/debugging/conversation/Help and actual skill
entry/routing; the six-guide step delivers brainstorming, format, role and character
guidance. Both steps are required for 0.10.2 notebooks. Notebook maintenance leaves
changes uncommitted and saves no story. Legacy framework application creates its
dedicated framework-only commit. Story/history, custom instructions and unrelated
staging stay protected; customized managed files, stale previews and unsafe paths
refuse. Inspect partial writes and take a new preview before resuming.

Inspect actual skills or enabled plugin entries, root routing and linked workflows
after applying. Have Codex reread/reload them in the novel folder, possibly in a
new chat. Plugin books must not get duplicate project skills. File checks do not
prove native discovery, voice behavior or conversational quality.

<a id="unreleased-side-character-profiles"></a>

## Side-character profiles in 0.10.2

The side-character feature ships in published `0.10.2` and was absent from 0.10.1.
First install the exact package in an isolated Python 3.11+ environment outside
novels. The [complete side-character installation procedure](side-characters.md#install-or-update-0102)
includes installation commands, the short feature-only maintenance script,
new-project behavior, preservation/save effects and actual host reload steps.
Installing Python or updating a plugin alone does not refresh existing books.

For an existing **legacy novel**, run the compatible
external controller (not the book's pinned runtime) and retain its verified
runtime interpreter. The ordinary stable-public-release gate remains in force;
select published 0.10.3. Historical qualification used a controlled offline fixture
transport separately from this public update route:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.10.3 --json
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.10.3 --expected-head REVIEWED_HEAD --json
```

Review the exact preview, version, changed paths, blockers and HEAD before apply.
The ordinary framework update adds the legacy skill/workflow/routing, preserves
structured sourced-capture semantics, custom instructions, story and unrelated
staging, and creates its dedicated framework commit. No format conversion occurs.

For an existing **default standalone Codex/project notebook** without an
integration marker, use the selected package's focused notebook updater:

```text
novel-creator notebook update --path BOOK --json
novel-creator notebook update --path BOOK --apply --preview PREVIEW_ID --expected-head REVIEWED_HEAD --json
```

It adds the side-character skill/workflow/root section, its absent supported
prerequisites and recognized public Help refresh. It does not replace custom
feature resources or make a commit. Review the concrete preview before applying.

For **Codex/Claude Code/both project or plugin notebook layouts**, follow the
[bounded feature-only procedure](side-characters.md#install-or-update-0102)
using `novel_creator.notebook_side_character.update`. It adds only this feature;
old Help/shared workflows/roles/root custom bytes remain. Matching plugin skill
delivery must be updated/enabled first, with no duplicate project skill copies.
The procedure preserves markers and refuses mixed/retained-legacy state,
missing prerequisites, unsafe paths, conflicting/custom feature resources and
stale previews. Preserve partial results and review a fresh preview to resume.

After each format's update, inspect actual skill files or enabled plugin entry,
root routing and linked workflow, then have the host reread/reload those resources
in the novel folder. Native discovery remains unverified until observed in that
host. Updates save no character profile; notebook drafts remain chat-only until
clear approval, while legacy discussion retains normal sourced capture.

## Session guidance in 0.10.1

Release 0.10.1 provides an explicit [version-pinned preview/apply manual procedure](https://github.com/bjarkig82/novel-creator/blob/v0.10.1/docs/session-guidance-upgrade.md)
for existing format-1 notebooks in all supported host/skill-source/language layouts.
For published 0.10.2 shared guidance, use its [version-pinned procedure](https://github.com/bjarkig82/novel-creator/blob/v0.10.2/docs/session-guidance-upgrade.md)
after its explicit issue-setup prerequisite. For the historical 0.10.3 guidance,
use its [0.10.3 procedure](session-guidance-upgrade.md). The 0.10.1 procedure below remains a
historical supported route for notebooks intentionally using that package.
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
installation outside the novel. Use the published 0.10.5 target below and
retain the verified runtime interpreter if it differs.

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --python RUNTIME --version 0.10.5 --json
```

Review the concrete target version, changed paths, blockers and HEAD. After
requesting that exact preview's application, use its returned preview ID and HEAD:

```text
CONTROLLER -I -B -m novel_creator update --novel BOOK --apply --preview PREVIEW_ID --version 0.10.5 --expected-head REVIEWED_HEAD --json
```

Follow the [existing update procedure](../workflows/getting-started.md#updating-an-existing-book),
including client closure for initial 0.1.0/0.2.0 updates, `--confirm-quiescent`
only after that confirmation, and external exact-operation recovery. Installing
the new package alone does not replace pinned files. See the
[release notes](releases/0.10.5.md) for compatibility and verification scope.

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

<a id="unreleased-session-issue-retrospectives"></a>

## Session issue retrospectives in 0.10.2

This feature ships in **published 0.10.2** and was absent from 0.10.1.
Package/plugin installation leaves pinned project snapshots unchanged. Install
`novel-creator==0.10.3`
in an isolated environment outside novels before resource setup; use the external
controller environment for an existing legacy novel. If a notebook lacks the
side-character prerequisite, reuse this selected 0.10.3 environment and matching
plugin for only the [side-character guide's existing-notebook feature preview/apply steps](side-characters.md#install-or-update-0102)
and short script. Skip that guide's historical 0.10.2 package/plugin installation
and new-project instructions; keep the selected 0.10.3 runtime throughout.

Existing **legacy novels** use the ordinary external-controller framework update
preview/application above, selecting published `--version 0.10.3`.
The ordinary updater requires a published stable target. Review/apply the
exact preview/HEAD; it delivers shared retrospective guidance and the legacy
`.agents/skills/novel-retro/SKILL.md`. Existing story/history/custom-instruction
protections and historical recovery fences remain. No conversion is required.
Installing source alone does not bypass public discovery for this route.

Existing **format-1 notebooks**, including standalone pre-integration-marker
books and Codex/Claude/both project/plugin layouts, use the selected installed
0.10.3 runtime:

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

New **legacy novels** initialized from the selected package bundle the
workflow and legacy adapter skill. New **notebooks** bundle the snapshot/project
skill or selected plugin routing. Plugin delivery keeps its notebook-only scope.
After each format's install/update, verify the actual skill file and links:
`.agents/skills/novel-retro/SKILL.md`, `.claude/skills/novel-retro/SKILL.md`, or
enabled plugin `novel-retro` plus the selected notebook snapshot. Reread/reload
root instructions and host skills before invoking them. Python imports/file
checks do not prove native Codex/Claude discovery. Checkpoint resource changes
only through the normal authorized workflow; package installation is insufficient.

Issue setup requires an independent format-1 notebook Git root, so legacy-only
books and Git worktree/redirected roots refuse. Mixed-marker notebooks retain
the actual legacy debug location, without moving or converting logs; this differs
from the side-character helper, which refuses mixed/retained-legacy state.
Setup does not enable debugging or automatic participation. Explicit session
debugging and optional active-session automatic retrospective each need their
own author opt-in; sharing/publication still needs exact current approval.

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

<a id="unpublished-retrospective-handoff-clarification"></a>

## Retrospective handoff clarification in 0.10.3

Version 0.10.3 makes publication next steps explicit in the first retrospective
response. It changes no sharing or publication authority. Follow the complete
four-format sequence above: existing notebooks need issue setup and the six-guide
refresh; existing legacy novels use the external updater targeting published
0.10.3. Reread/reload actual instructions and skills afterward.
