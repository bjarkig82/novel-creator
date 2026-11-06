# Writing with notebook agents

This guide covers the writing roles introduced in **published 0.5.0** and the
focused memory/responsiveness guidance in the **unpublished 0.6.0 candidate**.
The earlier 0.4.1 package does not include these writing roles or manuscript
workflows. Package installation leaves existing notebooks and legacy novels
unchanged; there is no migration or new updater command for these additions.
For setup, see [start here](../workflows/start-here.md#ask-your-agent-to-set-up-a-story).
The [everyday-writing guide](../workflows/everyday-writing.md) covers legacy novels.

## Open your novel and check host support

Open the initialized novel folder itself in Codex and have it read `AGENTS.md`
and relevant saved context. Do not initialize again to continue. A parent
workspace does not guarantee discovery of a nested novel's instructions.
Python is needed for setup; writing uses Codex's native file and Git tools.

New notebooks install six project definitions under `.codex/agents/` and root
instructions that make the main conversation follow the orchestrator. Check that
your actual Codex client supports custom-agent discovery, delegation and ongoing
direct writer turns with a specialist. These interactions remain **unverified in
the target desktop**; no universal agent picker or switching command is established.
See the [host checkpoint](../tests/evaluations/writing-agents-host.md).

If a capability is unavailable, the agent should say which one. The current chat
can still perform requested work using the shared workflows, with that limit
clear. A same-chat role does not establish a native specialist, and a context
reviewing its own draft provides self-review rather than independent review.
Roles inherit host tools and permissions; they add no browsing service, provider
credential or global configuration.

## Choose a focus and give it a task

The orchestrator is the default writing partner. It handles small requests and
coordinates bounded research, substantial drafting or independent assessment when
useful. You can request a specialist naturally:

> Let me work with the scene writer. Draft the arrival at the closed harbour gate
> from Elin's viewpoint, using our accepted notes. Keep the ending unresolved.

With native support, the selected specialist should remain your conversation
partner until you change roles; no orchestrator save is required between direct
turns. A fresh main chat defaults to orchestration and recovers saved files,
not an assumed transcript of all earlier conversations.

| Installed role | Useful request |
| --- | --- |
| `novel_orchestrator` | “Return to orchestration and help me choose the next task.” |
| `novel_brainstormer` | “Explore three reasons Elin might refuse the letter. Keep them provisional.” |
| `novel_researcher` | “Research how this harbour's tide would affect a small boat in winter.” |
| `novel_scene_writer` | “Revise only the gate scene to make Elin's hesitation visible through action.” |
| `novel_chapter_writer` | “Draft the first chapter from the selected outline, preserving the existing arrival scene.” |
| `novel_reviewer` | “Independently review the first chapter for chronology and character knowledge. Return findings without editing it.” |

Choosing a role selects a focus, not a whole-book assignment. “Let me work with
the reviewer” alone does not request a review or revision of the entire novel.
Use an identifiable target and desired work; the agent should ask only for choices
that materially block progress, without a forced questionnaire. Outlining remains
an explicit request.

Optional entry skills are `$novel-agent`, `$novel-research`, `$novel-scene`,
`$novel-chapter` and `$novel-review`. They supply methods and do not themselves
prove a native agent switch. Ordinary conversation needs no repeated skill or
Python command. Saved work follows the project's English or Icelandic language;
you can request another output language without silently changing project settings.

## Focused memory and conversational responsiveness (0.6.0 candidate)

The [conversation guidance](../notebook/workflows/conversation.md#conversational-responsiveness)
now asks for a useful reaction, idea or next question when enough context is
available, instead of a generic bookkeeping promise before a long tool gap. It
also encourages reuse of valid focused context and fewer tool round trips while
preserving context checks, writer authority, saves by turn completion and scoped
Git checkpoints. An early response does not mean notes have already been saved;
save and checkpoint failures must still be reported.

Start with the project brief and derived `notebook/working-summary.md`, then read
complete relevant items in their owning topic notes, following stable IDs and
links. Check relevant unresolved findings and project directions. Keep accepted
facts, live proposals, open questions and original decision context distinct.
Search or follow links for missing detail and exact history; an omitted item or
search miss does not prove absence. Reconcile affected summaries after saves or
writer edits. All roles use these same saved files as authority; agent memory
and summaries never become a separate canon.

This guidance is part of [0.6.0's unpublished candidate](releases/0.6.0.md) for
new notebooks created with that version. Existing notebooks are not automatically
updated; neither a package upgrade nor reading this source guide changes their
installed instructions. No notebook migration/updater is added. Legacy books
need an explicit supported update for their new working-context workflow, whose
exact input capture and save-before-display behavior is preserved. Actual
Codex voice latency and playback remain unverified; no measured improvement or
cause of a voice pause has been established.

## Shared notes and manuscript ownership

All roles use the same project brief and authoritative notebook topics. The
working summary is navigation. Saved files own facts; agent memory is not a second
canon. Drafting permits creative invention, but a saved or approved draft does not
automatically accept all its new details. Material inventions can be linked
proposals; only clear acceptance establishes the selected story facts. Questions
remain open until resolved.

Content is created on demand. Setup creates no empty manuscript, research or
review forms.

| Path in your novel | Purpose |
| --- | --- |
| `manuscript/index.md` | Stable chapter/scene IDs, order, owning file links and drafting status. |
| `manuscript/scenes/<scene-id>.md` | A standalone scene's prose before incorporation. |
| `manuscript/chapters/<chapter-id>.md` | An assembled chapter and its scenes, with stable IDs beside headings. |
| `research/<research-id>.md` | Substantial research, consulted sources, uncertainty and story implications. |
| `reviews/<review-id>.md` | Substantial requested findings tied to particular prose and its reviewed revision. |

Each scene has one editable prose owner. For example:

> Incorporate the standalone arrival scene into the first chapter after the
> harbour description. Keep its prose and stable identity, and update the index.

The workflow moves ownership to the chapter and retires the standalone prose;
it must not leave two editable authoritative copies. History preserves the prior
contents. If interrupted, the agent should report saved paths and pending transfer
state, inspect actual files and recover before repeating an insertion.

## Revise within scope and preserve history

> Revise only Elin's final exchange in the arrival scene. Preserve the opening
> and all other scenes. Save the revision, keeping the current prose recoverable.

An identifiable draft or revision request authorizes producing and saving that
work without routine approval checkpoints. “Propose first” and protected passages
remain binding. Before replacement, exact current prose must be recoverable in
verified Git history or a verified historical copy, including uncommitted writer
edits. The agent should reload changed files and reconcile concurrent edits.
Brainstorming, research and review alone do not authorize manuscript rewriting.

During delegation, specialists edit only assigned paths and never commit; the
coordinator owns shared notes, index integration and the checkpoint. Directly
selected specialists can save requested work under the normal scoped rules.
File-save failures, partial updates and failed Git checkpoints must be reported
separately. Local history is not a separate backup, push or publication.

## Research and independent findings

> Research likely winter sailing constraints for this setting. Cite sources you
> actually consult, distinguish uncertainty, and leave fictional choices proposed.

Research uses available host tools and local sources. Saved findings identify
actual consulted sources, relevant dates and supported claims. If browsing or a
source is unavailable, the agent should disclose it and label unverified background
knowledge. It must not invent citations or imply an unavailable research service.
Real-world evidence does not automatically become fictional canon.

An independent reviewer needs an actual separate native context and relevant
prose/notes. Findings should cite a stable scene/chapter ID, owning file and actual
passage, explain the consequence, and suggest a remedy or focused question.
Reviews record the revision assessed and can become stale after edits. Requesting
findings does not authorize applying suggested rewrites or changing accepted facts.

Detailed rules: [roles and handoffs](../notebook/workflows/agents.md),
[manuscripts and recovery](../notebook/workflows/manuscript.md),
[research](../notebook/workflows/research.md) and
[review](../notebook/workflows/review.md). The
[focused evidence](../tests/evaluations/writing-agents.md) records installation,
packaging and evaluation scope. Focused checks do not establish native desktop
acceptance, complete release qualification or literary quality.
