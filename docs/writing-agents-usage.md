# Writing with notebook agents

This guide covers the writing roles introduced in **published 0.5.0**, focused
memory guidance in **published 0.6.0**, and clarification, analysis and help
introduced in **published 0.7.0**. The latest published package is
[0.7.1](releases/0.7.1.md), published 2026-11-10; it supplies explicit project
updates for focused methods. The [0.7.2 unpublished candidate](releases/0.7.2.md)
adds clarification suggestions and custom input. The earlier 0.4.1 package does
not include these writing roles or manuscript workflows. Package installation
leaves existing notebooks and legacy novels unchanged; follow the
[project upgrade steps](upgrading-projects.md) to update installed guidance.
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

## Help choosing a next step (0.7.0)

New notebooks initialized **with published 0.7.0** include `$novel-help`.
It is an optional chat skill, not a terminal command. This skill is not in 0.6.0
and is not added to existing notebooks by installing the package or reading this
guide.

> $novel-help

No input is required. Help offers a few next steps suited to the saved story's
stage without starting them or imposing an order. You can begin with no story
idea. “What should I do next?” works too. To narrow the explanation, add a command
name, goal or topic; use `commands` for the compact full list of installed entries:

> $novel-help novel-clarify

> $novel-help commands

For a named command, help explains its purpose, whether extra input is needed,
useful optional details, save effects and one copyable example. A target can be
a character's ordinary name or description, an outline, a scene/chapter title,
or an optional known stable ID or file path. `$novel-clarify` does **not** require
a character ID. For example, `$novel-clarify Elin's motivation` is enough when
Elin is identifiable. With no supplied target, it can use a clear current focus;
otherwise it asks one scope question. `$novel-analyze` accepts similar targets
but returns a read-only report; `$novel-review` saves substantial findings.

Help checks what is actually installed in your notebook instead of assuming a
newer command exists. It changes no files, notes, summaries or history and does
not switch agents or execute the examples. A later explicit writing request uses
the relevant workflow; “Help me revise this scene” remains a revision request.
See the shared [help workflow](../notebook/workflows/help.md) for the catalog and
detailed guidance.

## Clarify and analyze (0.7.0)

The published [0.7.1 patch](releases/0.7.1.md) extends these methods to existing
projects through explicit updates; see [upgrading projects](upgrading-projects.md).
Legacy novels receive format-specific skills through their supported updater.
Older notebooks receive an additive retrofit. The original 0.7.0 limitations
below describe that release, not the availability after a successful 0.7.1 update.

New notebooks initialized **with published 0.7.0** include two
additional methods. They are not part of published 0.6.0, and installing a package
or reading this guide does not add them to an existing notebook. No notebook
migration or new CLI command is introduced. Use ordinary language or the optional
skill entries:

> $novel-clarify Elin's motivation for hiding the letter. Ask me up to three
> questions, one at a time.

The clarification pass reads relevant notes, chooses the most consequential gap
and asks one question at a time, with up to five questions by default. You can
answer freely, select an offered alternative, leave something unknown, skip or
stop. Clear answers update the owning notes with their existing stable identities
and history. Choosing an outline order does not accept every suggested plot fact.
Clarification does not rewrite scene or chapter prose.

In the [0.7.2 unpublished candidate](releases/0.7.2.md), notebook and legacy clarification questions
normally include 2–4 short labeled suggestions plus **Custom — type your own
answer**. Reply with a label or just type your answer; you can adapt a suggestion,
say you are unsure, or ask for fewer/no suggestions. For example, a question about
why Elin hides the letter might offer “A: To protect someone” and “B: To protect
herself”, while you can answer “Neither—she wants time to verify it.” Only your
selected or custom proposition is established. Existing project-local guidance
is not silently refreshed by a package upgrade. Existing legacy novels need their
reviewed framework update; existing notebooks need a previewed update. The 0.7.2
notebook updater recognizes original published 0.7.0/0.7.1 clarification files,
replaces those unchanged copies, and refuses customized resources. See
[upgrading projects](upgrading-projects.md) for package installation, preview/apply
and reloading instructions and skills in Codex.

> Ask me clarifying questions about the midpoint of the outline. Keep the
> sender's identity unresolved.

> $novel-analyze chapter two against the outline and Elin's character notes.
> Focus on what she knows when she opens the letter.

Analysis is read-only. It returns findings in the conversation with scope,
reviewed revision, actual passages/locations, severity, story consequences and
suggested remedies. It compares selected material with relevant accepted notes
and directions, distinguishes character belief from objective fact and reader
knowledge, and respects intentional mystery. Unavailable context and unexamined
future payoffs stay explicit; the report does not claim exhaustive continuity.
Optional pacing/style advice is separated from substantiated conflicts.

> Analyze the arrival scene for causality and pacing without changing any files.

No notes, review files, summaries or checkpoints are written during analysis,
even though ordinary notebook conversation maintains notes automatically.
`$novel-review` retains its existing behavior of saving substantial requested
reviews. You can separately request “Save that analysis as a review” or a scoped
revision afterward. Neither a finding nor an offered remedy changes accepted
facts or authorizes a manuscript edit by itself. Actual independent analysis
still needs a separate native context; a context assessing its own draft is
self-review. See [clarification](../notebook/workflows/clarify.md) and
[analysis](../notebook/workflows/analyze.md) for detailed rules.

## Focused memory and conversational responsiveness (0.6.0)

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

This guidance ships in [published 0.6.0](releases/0.6.0.md) for
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
