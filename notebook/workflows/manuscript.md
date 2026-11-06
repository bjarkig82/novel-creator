# Scene and chapter manuscripts

Follow [roles and ownership](agents.md), [conversation and saves](conversation.md)
and the [format-1 fact rules](format.md). Manuscripts are ordinary Markdown,
separate from notebook fact records. Create content only when useful and requested;
do not initialize empty scenes, chapters or manuscript forms.

## Scope and creative authority

A request to draft or revise identifiable material authorizes producing and
saving that work without routine approval checkpoints. Respect “propose first,”
protected passages, scope and other explicit directions. Choosing a writing role
alone does not authorize a whole book. Brainstorming, research and review alone
do not authorize manuscript rewriting. If the target cannot be identified, ask
one focused question while continuing useful independent work.

Read the project brief, relevant accepted facts, open questions, outlines and
neighboring passages. Use available scene purpose, viewpoint, tense, voice,
chronology and consequences. Ask only when a missing choice materially blocks
useful work; otherwise make bounded assumptions visible and keep drafts revisable.
Do not require a full questionnaire, impose a narrative framework or invoke the
outline skill automatically. Use configured English or Icelandic for saved
headings and prose, preserving names, Unicode and stable IDs. Honor an explicit
output-language request without changing project settings.

Drafting permits invention in the draft; it does not accept each new fact as
canon. Record material new details as linked proposed notebook items when useful,
rather than extracting every sentence. Clear acceptance establishes only the
identifiable selected content. A saved or approved draft does not silently resolve
every open question or promote all its inventions. Preserve proposed/accepted/
rejected and open/resolved distinctions. Research truth is not automatically
fictional truth.

Surface a significant conflict with accepted canon or explicit directions before
developing the affected contradictory material; explain the conflict and seek
direction, continuing unaffected work where possible. A clear authorized correction
can revise accepted material with history. Distinguish objective truth, character
belief/knowledge, reader revelation and their timing. Intentional ambiguity or
unreliable narration is not automatically a continuity error. Do not claim
exhaustive consistency or literary quality from file checks.

## Stable identity and one prose owner

Create `manuscript/index.md` on the first manuscript save. Use a readable Markdown
table recording each stable chapter/scene ID, type, display order/title, owning
relative file link, parent chapter if any, and drafting status. Status describes
work such as draft or revised, not canon acceptance. Use unique stable IDs such as
`chapter-harbour` and `scene-arrival`, matching `[a-z][a-z0-9-]*`; reuse existing
IDs when renaming, reordering or revising. Check existing IDs before adding one.

- `manuscript/scenes/<scene-id>.md` owns a standalone scene's prose before
  incorporation. Include its visible stable scene ID beside its heading.
- `manuscript/chapters/<chapter-id>.md` owns an assembled chapter, with its visible
  stable chapter ID and each scene ID beside the corresponding scene heading.
- For a scene inside a chapter, the index points to the chapter as its prose
  owner and records its parent chapter. Find its visible ID within that file;
  links need no custom anchors. Do not keep a separately editable scene copy.
- Keep historical copies explicitly historical, outside editable scene/chapter
  ownership, for example under `manuscript/history/`. A retired scene path may
  contain only a short non-authoritative pointer to its chapter and stable ID.

Use relative Markdown file links and verify their targets. Topic references pair
their semantic `topic-id#item-id` with a file link under the format contract.
The manuscript index owns prose navigation, not a second registry of story facts.

## Write or revise

For a scene, establish its requested purpose, viewpoint and immediate context;
develop action, change and consequences at the requested scale. Preserve the
writer's voice and constraints. For a chapter, use that same scene guidance while
shaping progression, scene order, transitions and pacing across the chapter.
Reuse existing owned scenes and IDs rather than silently redrafting duplicates.
Do not spawn an agent per scene by default.

Read the current owning file and Git differences immediately before replacement.
Preserve unaffected passages and direct writer edits. A revision to an incorporated
scene edits its owning chapter in the assigned scope. Reload and reconcile changes
made since the initial read; never overwrite a concurrent edit blindly. Unresolved
collisions require disclosure and focused clarification.

Before replacing or removing prose, verify that its exact current contents are
recoverable. A commit of an older version is insufficient for uncommitted writer
prose. Check that verified Git history contains the current content, or save and
read back an explicitly historical copy of that content before replacement. Cover
every affected file, including the destination chapter. If preservation fails,
do not perform the destructive replacement; retain the proposed revision and
explain what remains pending. Preserve history before editing, not only after a
checkpoint failure. History is not current canon or another editable owner.

Save the requested prose, then update ownership/status and any useful linked
proposals, then derived navigation. Confirm saved contents and index links before
reporting completion. A delegate returns shared-note/index changes as proposals
for its coordinator. The coordinator applies transfers involving the shared index
and checkpoints delegated work.

## Incorporate a standalone scene

Treat incorporation as a move of prose ownership, not a copy-and-forget operation.
Read the standalone scene, destination chapter and index, including current writer
edits. Confirm the requested destination/order and preserve exact current source,
destination and index in verified history or historical copies before replacement.
Do not silently remove prose already present in the destination.

1. Serialize the transfer: pause edits to both prose paths. Record a pending
   transfer in the index with scene ID, current owner, intended destination and
   recoverable history locations. The source remains the sole owner until the
   destination has been saved and verified. Any inserted destination copy is
   explicitly pending and must not be edited as another authoritative scene.
2. Insert the scene once into the chapter under the same stable scene ID; make
   only authorized integration changes. Save and read back the chapter, checking
   preserved destination passages and complete source prose or requested revisions.
3. Update the index to name the verified chapter as the sole scene owner, parent
   and order. Mark the source retired/non-authoritative while cleanup is pending.
   Verify this ownership update before removing the standalone prose.
4. Replace the standalone path with a non-authoritative pointer or remove it only
   after recoverable history has been verified. Check links and final ownership,
   clear the pending transfer and resume edits only to the chapter's owned prose.

Multi-file saves are not atomic. On any interruption or failure, report the paths
actually saved and leave the pending transfer explicit. Inspect actual source,
chapter, index and history before retrying; never blindly repeat an insertion.
If the chapter is incomplete, retain or recover the source as sole owner. If the
chapter is complete and the index has switched ownership, finish retiring the
source without duplicating its scene. Reconcile new writer edits before either
choice. If ownership cannot be established safely, pause edits to the affected
scene, preserve both versions as historical/pending material and ask for direction.
Do not report successful incorporation until there is one verified prose owner.

## Save failures and checkpoints

Use the shared scoped Git rules: preserve unrelated staged entries and defer a
checkpoint if a touched path contains pre-existing staged writer work. Never
broadly stage, reset, stash, remove locks, bypass hooks or push automatically.
Verify status/history after an attempted local checkpoint.

A file-save failure means affected work remains unsaved; preserve recoverable
originals and report partial saves and index mismatches. A checkpoint failure
means saved files may exist without a new commit; report that separately and
retain historical copies needed for replaced prose. Retry only after inspecting
the latest state. Do not promise exact current-turn recovery or claim unsaved
draft text is persisted canon.
