# Data Model: Story Notebook Format 1

## Ownership

The novel owns an independent Git repository. Initial story files are notebook/project.md and notebook/working-summary.md. Topic files under notebook/topics/ appear only when meaningful material exists.

Project brief owns settings and explicit creative directions. Each current topic item has one owner; other notes reference it. Working summary is derived navigation, never competing canon. Git history and historical revision entries preserve superseded information.

## Project brief

Metadata: format = novel-notebook, version = 1, kind = project, stable id, language = en or is initially. Title is the supplied provisional title.

Prose: Concept, Creative preferences, Explicit directions. Unknown information stays unknown; setup does not invent a genre or story structure. Display prose uses the configured language; contract field labels stay stable. Guided brainstorming is the default when no interaction mode is requested; the writer can request freeform exploration without changing story facts.

## Topic note

Metadata: format, version, kind = topic, stable id, category. Categories such as character, plot, setting, relationship and general describe content without imposing a taxonomy.

Topic title/filename can change without changing identity. Two topics can share a display title, never an identifier. File moves require updating navigation links.

Each meaningful item has:

- Stable Item-ID unique within its topic, written as a plain field below a descriptive heading.
- Type: statement or question.
- State: proposed, accepted or rejected for statements; open or resolved for questions.
- Perspective: objective, character:<topic-id>, reader, or explicitly unknown when the holder is unavailable.
- Origin: concise decision/proposal context; no exact quotation or transcript required.
- Links: optional stable references paired with relative Markdown navigation.
- Prose describing the material, including uncertainty, timing or intentional ambiguity where relevant.

An objective perspective describes the proposition's domain, not its acceptance: a proposed objective fact remains a proposal.

## Decisions and state transitions

Clear writer commitments change proposed statements to accepted; clear rejections change them to rejected. Partial acceptance splits independently meaningful parts. Praise, silence, topic changes, hypotheticals and quoted dialogue cause no acceptance transition.

Accepted statements can be revised or rejected on direction. Reversal establishes a new revision rather than rewinding Git. Questions resolve only on clear resolution, with results described or linked; reopening requires direction. Resolved questions do not automatically make all discussed answers accepted.

Significant unresolved conflicts block the affected canon change while unrelated exploration may continue. Intentional ambiguity is recorded as such, not flattened into an accidental contradiction.

## Revision history

Decisions remain with affected items, not in an exchange ledger. A revision identifies the item, old accepted content, new content and rationale/context. The Item-ID remains stable.

Before replacing accepted content, ensure its previous value is recoverable in Git or preserve that value in the topic's historical Revisions section during the same edit. A failed checkpoint retains that prose. Once history is verified, an entry can reference the historical version rather than repeating all old prose. Historical entries are never current canon.

## Working summary

Metadata: format, version, kind = summary, stable id. Prose gives recent focus and pointers to decisions/open threads. Detailed facts remain in their owning topics.

Update when navigation changes meaningfully, not on empty turns. The summary is maintained automatically but never automatically displayed at session start. Requested briefs are generated from relevant topic notes.

## Validation and privacy

Topic IDs and Item-ID values use short ASCII slugs; names, titles and prose support Unicode. Renames preserve IDs. A semantic reference such as keeper#motivation identifies the item independently of rendering. Its accompanying relative Markdown link opens the owning file without a fragment; the visible Item-ID locates the item by reading/search. No custom heading anchors or renderer-generated fragments are required. References resolve within the notebook.

Development fixtures check required metadata, version, unique topic IDs and Item-ID fields, allowed states/types/perspectives, origins, file links and exact semantic-reference targets. This is not a runtime gate on every reply.

No machine-specific interpreter paths, credentials, hidden reasoning, host thread IDs or exact-message digests are stored. Unsupported versions are disclosed rather than automatically rewritten.
