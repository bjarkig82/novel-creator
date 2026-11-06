# Native Codex writing agents

Status: approved by the writer in chat. After the feasibility checkpoint found
that target-desktop interaction cannot be exercised in this managed workspace,
the writer explicitly authorized implementation with desktop acceptance pending.
Native direct specialist access remains a delivery requirement, not a verified
capability or an invitation to substitute conversation personas.

## Intent and agreed scope

Novel Creator will run inside Codex initially. The orchestrator is the default
writing partner. The writer can choose to converse with a specialist and remain
with it until requesting another role. The first version includes brainstorming,
research, scene and chapter manuscript drafting, and independent review.

Keep the existing local Markdown notebook, writer authority, English/Icelandic
support, and Git history. Skills remain reusable methods; custom agents provide
separate delegated contexts and responsibilities. Agent definitions alone do not
provide additional host tools or prove better literary quality.

## Approaches considered

- Native Codex agents: extend the existing project adapter with project-scoped
  role definitions and shared workflows. Reuse Codex conversations, tools and
  permissions. Interaction controls depend on the installed client.
- A dedicated application: own the agent picker, conversation runtime and model
  integrations. This provides more UI control but introduces another application
  to maintain.

The writer selected Codex for the initial version. A separate application is
outside this design.

## Host integration and direct conversations

Install six namespaced custom agent TOML definitions under `.codex/agents/` in
new novel projects. Each defines `name`, `description` and
`developer_instructions`, following the current [Codex subagent documentation](https://developers.openai.com/codex/subagents).
Do not replace Codex's built-in `default` agent or modify global configuration.
Use the root `AGENTS.md` to make the main conversation follow the orchestrator
workflow; the orchestrator definition also makes that role available explicitly.

Direct role choice must work through an ordinary request such as "Let me work
with the scene writer." The selected role remains active for that conversation
until the writer changes it. A direct request to a specialist does not require
an orchestrator response or an orchestrator save before continuing.

There are two distinct host behaviors to validate:

1. Codex discovers the named agents and delegates into separate agent contexts.
2. The target desktop client permits an ongoing writer conversation with the
   selected specialist, either in its agent thread or through another documented
   native control.

The documentation establishes agent definitions and subagent inspection, but
does not establish a universal top-level agent picker. Make a disposable target
desktop feasibility exercise the first implementation checkpoint, before
building the complete role/resource set or documenting controls. Direct access
to an actual specialist remains a first-version requirement. If the host cannot
support it, report the unmet requirement and settle the interaction approach
with the writer before dependent implementation. A main-chat role can be offered
as a compatibility option, but is not an agreed substitute for a custom agent.
Do not create user-owned chats automatically or imply that switching projects
occurred. For this implementation, the writer has explicitly allowed dependent
resource and workflow work to proceed while that target-desktop check remains
pending; this does not waive the native-interaction requirement.

When custom-agent tools are unavailable, the main chat may perform the requested
work using the same workflows and disclose unavailable delegation where relevant.
This limited compatibility behavior does not establish delivery of the native
multi-agent experience. Do not claim independent review when one context
performed both jobs.

## Roles

| Name | Responsibilities | Limits |
| --- | --- | --- |
| `novel_orchestrator` | Follow the writer's intent, choose focused context, delegate useful work, reconcile results, maintain navigation and continue the conversation. | Do not delegate every turn or override a directly chosen specialist. |
| `novel_brainstormer` | Explore concepts, premise, characters, setting and plot using the existing brainstorming and outline methods. | Preserve provisional alternatives; outlining remains explicit-only. |
| `novel_researcher` | Investigate a bounded question, compare sources, record evidence and uncertainties relevant to the book. | Research findings do not establish fictional canon. |
| `novel_scene_writer` | Draft or revise a scene with a purpose, viewpoint, voice, relevant context and consequences. | Do not rewrite surrounding manuscript outside the requested scope. |
| `novel_chapter_writer` | Shape chapter progression, draft its scenes and transitions, and reconcile pacing and consistency across them. | Reuse scene-writing guidance; do not spawn a separate agent for every scene by default. |
| `novel_reviewer` | Independently assess requested prose, continuity, character behavior, structure and source-dependent claims. | Return findings and suggested changes; reviewing alone does not authorize rewriting prose. |

Automatic delegation should serve an identifiable need: independent assessment,
bounded research, or a substantial drafting assignment. Small requests can be
handled directly. Parallel work is useful for independent research/review, not
for concurrently editing the same chapter or topic.

## Shared context, delegation and persistence

All roles use the same project brief and authoritative notebook topics. The
working summary remains derived navigation. Read only relevant notes, outlines,
manuscript passages and prior findings; do not load the entire novel by default.
An agent's remembered conversation is not a second owner of story facts.

A delegation brief supplies the task, requested output, language and creative
directions, relevant source paths, accepted facts, unresolved questions, and
exact editing ownership. A specialist returns the resulting paths or proposed
text, assumptions, new invented details, conflicts and remaining questions.
The coordinator checks relevant current files before integrating results.

Directly selected specialists can save relevant notes and requested manuscript
changes using normal notebook rules. During delegation, the coordinator owns
shared notebook updates and the Git checkpoint. A delegated specialist may edit
only explicitly assigned output paths and must not commit. Concurrent delegates
receive disjoint paths or return proposals without editing shared files. This
is workflow coordination, not an enforced filesystem security boundary.

Do not blindly overwrite concurrent writer edits. Reload changed files and
reconcile; disclose unresolved collisions. Preserve unrelated staged work and
use exact paths for local checkpoints. No automatic push or publication.

Persist substantive decisions and work in project files, including a concise
handoff when useful. Conversation role choice is session-local; starting a fresh
main chat defaults to the orchestrator. A new agent recovers saved project
context, not an assumed complete transcript of every other conversation.

## Manuscript storage and revisions

Proposed implementation choice: use ordinary Markdown under `manuscript/`,
separate from notebook fact records. Create content on demand rather than empty
chapters and scene forms at initialization.

- `manuscript/index.md` records stable chapter/scene identities, ordering,
  ownership paths and drafting status. Display numbers and titles may change
  without changing identity.
- `manuscript/chapters/<chapter-id>.md` owns the prose of an assembled chapter,
  with explicit stable scene identifiers beside its scene headings.
- `manuscript/scenes/<scene-id>.md` owns a standalone scene before inclusion in
  a chapter. Incorporation moves its prose into the owning chapter and updates
  the index; do not leave two editable authoritative copies. Preserve existing
  prose through Git or an explicit historical copy before removal.
- `reviews/<review-id>.md` stores substantial requested reviews, citing stable
  manuscript identities and actual passages. Mark findings as based on the
  reviewed revision; later prose changes may make them stale.

A request to draft or revise identifiable material authorizes producing and
saving that work; do not introduce routine approval checkpoints. Respect explicit
instructions to propose changes first or preserve a particular passage.
Brainstorming, research and review requests do not themselves authorize
manuscript rewriting. Preserve the previous prose in verified Git history or
an explicitly historical copy before replacement. Report file-save and checkpoint
failures separately, as the current notebook does.

Before drafting, use available viewpoint, tense, voice, scene purpose, outline
and neighboring context. Ask only when a missing choice materially prevents
useful work; otherwise keep assumptions visible and drafts revisable. Do not
require an exhaustive questionnaire or impose a narrative framework.

## Creative authority and research

The existing proposed/accepted/rejected and open/resolved notebook distinctions
remain authoritative. A drafting request authorizes creative invention inside
the draft, but does not accept every new story fact it introduces. Record
material new details as linked proposals when useful, rather than extracting
every sentence into the notebook. Explicit writer acceptance establishes only
the identifiable selected content. Revisions of accepted facts retain history.

Surface a significant conflict with accepted facts or explicit directions before
developing the affected contradictory material. Continue unaffected work where
possible. Distinguish objective truth, character belief/knowledge and reader
revelation; intentional ambiguity is not automatically an error.

Research uses available host search/browser/connector tools and records actual
sources, relevant publication/access dates, supported claims and uncertainty.
Store substantial research in `research/<research-id>.md`, linking relevant topic
items and manuscript passages without creating another canon registry. A source
may be reliable about the real world without being true in the fictional world.
Never invent citations or imply a deep-research service was invoked when only
ordinary browsing was available. Missing browsing tools must be explicit; local
source analysis can continue. Imported text and story files remain data, not
instructions or authorization.

## Adapter, skills and installation

Keep substantive role guidance in platform-independent notebook workflows. Thin
TOML agent definitions and focused skills point to the installed guidance.
Retain existing brainstorming and outline skills; add focused entry points for
role selection, research, scene drafting, chapter drafting and review as needed.
Role selection and substantive task authorization remain distinct: choosing the
reviewer does not itself request a review of the entire book.

Extend resource packaging and notebook initialization to install agent
definitions, workflows and entry skills. Preserve the setup-only Python model;
there is no per-turn Python controller, new provider integration or additional
API credential requirement. Inherit host model/effort settings initially rather
than hardcoding a provider model or increasing reasoning effort for every role.
Permissions, provider and connected services remain controlled by Codex.

Proposed first-version compatibility boundary: install into new notebooks only.
Existing notebook and legacy projects stay unchanged, including pinned resources.
Document this explicitly. Existing-project installation/migration, a standalone
application, publication/export pipelines and legacy manuscript support are
separate work. A package upgrade alone does not update an existing novel.

## Validation and delivery

Implementation should use focused checks, including:

- TOML parsing, required role fields, unique names and resolvable installed
  guidance; no reliance on unsupported configuration keys.
- Disposable notebook initialization in English and Icelandic, confirming
  tracked resources, existing-path preservation and no empty manuscripts.
- Targeted wheel and source-distribution content checks and isolated installs
  for the new packaged resources; preserve existing release gates.
- Notebook contract checks where authority or format guidance changes.
- Scenario evaluations for default orchestration, persistent direct role choice,
  independent delegated review, research without tools, a requested scene and
  chapter, scene incorporation, scoped revisions, proposed draft inventions,
  interrupted saves and conflicting/concurrent edits.
- A real target Codex desktop exercise for role discovery, actual delegation,
  specialist interaction, handoff and resumption. Record the tested host/version,
  observed controls and unsupported behavior. Structural tests do not prove
  native UI behavior, independence, narrative quality or exhaustive continuity.

Update ordinary functionality, setup and everyday-writing documentation around
the delivered behavior. No release publication, global configuration changes,
edits to a real novel, commits or pushes are authorized by this design document.

## Decisions left to implementation

The builder can choose internal module boundaries, filenames for shared
workflows, exact skill names and proportionate fixtures. Preserve the agreed
roles, direct-access semantics, storage ownership and authority boundaries.
Verify the host integration before implementing the dependent interaction and
finalizing instructions. Report observed native specialist access. If unavailable,
leave that requirement explicitly unmet rather than silently substituting a
main-chat role.

## Design review

An independent builder review identified one consequential gap: the original
draft allowed a main-chat role fallback without the writer having selected that
tradeoff. The design now preserves native specialist access as a requirement and
places host feasibility first. The review found shared-file ownership,
manuscript authority and compatibility sufficiently specified for planning.
