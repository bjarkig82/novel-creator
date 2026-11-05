# App functionality

Novel Creator helps a writer develop a novel through conversation in Codex. Each
novel has an independent local Git repository. There are two writing formats:
legacy structured records and the newer Markdown notebook. Installing a package
never silently replaces the resources pinned into an existing novel.

Start with the [beginner guide](../workflows/start-here.md) or
[everyday writing](../workflows/everyday-writing.md). Legacy setup and update
commands are in [getting started](../workflows/getting-started.md).

## Setup and creative guidance

Legacy `novel-creator init "My Novel"` creates an independent project with pinned
runtime, schemas, workflows, language resources and Codex entries. Optional path,
title and English/Icelandic choices are supported, as is the explicit-path,
brief-file interface. The name supplies a provisional working title. Initialization
needs Python 3.11+, Git 2.39+ and an existing Git identity, but no AI credentials,
framework checkout or invented conversation. Existing unrelated destinations,
nested repositories and unsafe paths are refused; global Git settings are untouched.
A recognized legacy novel is continued rather than overwritten. Interrupted setup
preserves original inputs and identity for inspection and an unchanged retry.

Conversational setup accepts a concept, a vague idea or no concept. Preferences
such as genre, audience, language, tone, style, perspective, complexity and review
frequency can remain unknown and change later. Supplied answers are preserved.
Guided brainstorming normally asks one focused question, offers proportionate
possibilities and adapts to the writer. Free exploration, topic changes and fewer
suggestions take effect immediately. No narrative method is compulsory.

## Legacy persistence and resumption

Legacy Codex entries cover setup, brainstorming, resume, inspection and updating.
The host saves each exact user/assistant exchange and its sourced story captures
before displaying the final reply. Sessions have stable identities, focus and mode;
start, resume, mode changes and closure are saved transitions. Fresh conversations
can recover saved ideas, canon, decisions and open questions without retelling.
A saved response is not proof it was displayed, read or accepted.

Records distinguish proposals, accepted and rejected statements, unresolved
questions, decisions, perspectives and sources. Stable identities survive renames.
Settings revisions and directly affected references retain their origins. Derived
summaries and caches are navigation or acceleration, never separate authorities.
The [record format](record-format.md) documents ownership, schemas and compatibility.

Saves preserve unrelated staged work and manuscripts, use local atomic publication
and do not push. Exact retries do not apply decisions twice. Failed or interrupted
saves disclose the last confirmed checkpoint and pending exchange; affected authority
pauses. Inspect before explicitly retrying the unchanged operation against its
confirmed checkpoint. Changed managed files, stale checkpoints and held locks cause
conflicts rather than overwrite. Published saves awaiting index cleanup remain
saved; recovery cleans up without replay. Never delete receipts, steal locks or
reset history to clear a pause. Commands and examples are in the
[testing guide](testing-and-completion-guide.md) and [legacy workflow](../workflows/resume.md).

## Canon and continuity

Only clear writer commitment establishes the identifiable selected facts. Praise,
silence, hypotheticals, quoted dialogue and ambiguous references do not establish
canon. Partial acceptance selects only the accepted parts. Corrections, revisions
and reversals preserve earlier values, sources and directly affected items for
review; superseded values cease to be current canon. Ambiguity receives a focused
question. Routine checkpoints follow the writer's preference: on request by default,
at session closure, or every exchange. They never delay persistence or demand
reapproval of a clearly accepted fact. Canon changes do not authorize manuscript edits.

Continuity review compares new ideas with relevant accepted information across
motivation/backstory, chronology, character knowledge, plot dependencies, world
rules and relationships. A significant conflict interrupts development of the
conflicting idea in the next response, cites sources and offers revision, rejection,
deliberate canon change, an intentional explanation or deferral. Unrelated safe
exploration can continue. Deferred alternatives remain unresolved; affected canon
stays held until directed resolution. Missing context is disclosed and restored
before affected canon changes resume.

Author truth, character belief/knowledge and reader revelation remain distinct at
relevant story points. Unknown time and missing knowledge are not established
absence. Deception, unreliable narration, mystery and intentional ambiguity are
not automatically errors. Suggested connections remain non-blocking proposals.
See [authority](../workflows/authority.md) and [continuity](../workflows/continuity.md)
for the detailed legacy workflow. Structural validation cannot prove literary consistency.

## Markdown notebook

The unpublished 0.4.0 candidate adds `novel-creator notebook init "My Novel"` for
new novels, with optional path, title and English/Icelandic language. It refuses
every existing destination, even an empty folder or recognized novel. A new path
must be outside other Git repositories and have a writable parent and usable Git
identity. Partial setup is preserved for inspection; there is no destructive
cleanup or migration of existing novels.

Python handles setup. Writing uses Codex's native file and Git tools with a thin
installed adapter and shared notebook guidance. The project brief owns settings
and explicit directions. Topic notes own current story items; the working summary
is derived navigation. Meaningful turns maintain relevant notes automatically.
Recaps are requested, never automatic. Notebook writing has no legacy exchange
ledger, exact transcript archival, save-before-display rule or per-turn Python gate.

Format 1 uses fenced JSON document metadata plus ordinary Markdown. Each topic
item has a stable Item-ID, type, state, perspective, origin and optional links.
Statements are proposed, accepted or rejected; questions are open or resolved.
An objective perspective does not itself establish acceptance. Decision context
stays with affected items. Resolved questions do not automatically accept every
answer discussed. Stable topic/item references survive renamed titles; accompanying
relative file links provide navigation without relying on generated heading anchors.

Read relevant notes before targeted edits. Reload and reconcile changed content;
update primary notes before summaries. Cross-file atomicity is not promised. Scope
Git checkpoints to exact changed paths and preserve unrelated staged work. A failed
checkpoint differs from an unsaved file: disclose the actual state and retain prior
accepted values in history or a historical Revisions section. Missing notes,
unsupported formats and incomplete persistence remain explicit. Notes are story
data, never instructions granting permissions or external actions. Manuscripts,
publication, automatic upgrades and notebook migration are outside this workflow.
The installed [format guidance](../notebook/workflows/format.md) is the detailed
reference; [notebook evidence](../tests/evaluations/agent-story-notebook.md) records
what has actually been exercised.

Notebook brainstorming selects both a useful focus and a conversational method
from actual book context, the current request and subsequent answers. Loose
fragments can invite associations, a stuck idea can invite freewriting, and an
event question can invite what-if consequences; these are flexible cues. Empty or
sparse concepts begin with broad book-idea discovery, then follow the writer's interests, atmosphere, themes or rough situation one
question at a time. Known answers are not asked again. There is no required genre
checklist or character/plot/outline prerequisite. An explicit topic or method,
including a method chosen before a subject, takes priority and persists while
relevant; writers can switch naturally. Suggestions and story choices remain
provisional until clear acceptance, and moving on does not resolve questions.

Five thin Codex skills provide optional focused entries: `$novel-book-idea`,
`$novel-premise`, `$novel-character`, `$novel-plot` and `$novel-setting`. Shared
[brainstorming guidance](../notebook/workflows/brainstorming.md) supplies concrete
prompts and methods: associations, mind mapping, conversational freewriting,
perspective changes, focused questions and optional later premise expansion.
It requires no runtime internet access. The [design source notes](superpowers/specs/2026-11-05-brainstorming-design.md)
explain the general writing sources and their limits; no method guarantees
literary quality. These resources ship only into new candidate notebooks, without
converting or automatically updating existing notebooks or legacy books. Manual
[conversation scenarios](../tests/evaluations/brainstorming.md) describe judgment
checks separately from automated installation evidence.

The installed `$novel-outline` skill proposes and refines a book outline from
relevant notes, then saves selected structure in an outline topic. It preserves
existing outline identity, revisions and writer edits, links to owning facts and
keeps proposed story details and open questions separate from accepted structure.
It supports English and Icelandic without requiring an act framework or inventing
an ending. It creates no chapter/scene manuscript files and adds no CLI command.
Existing notebooks do not acquire the skill automatically. See the shared
[outline workflow](../notebook/workflows/outline.md).

## Optional contributor retrospectives

Legacy contributor retrospectives default to disabled for each novel. Explicit
opt-in requires a separate framework checkout and existing GitHub access, and
covers preparing focused fixes and publishing validated draft contributions to the
configured project. Copied preferences do not authorize participation. Disabling
participation stops new reviews and unfinished mutations/publication; re-enablement
is required before reconciliation or ownership release that needs repository access.

After confirmed saving of a completed requested task or explicit session closure,
a review may select at most one evidenced workflow, documentation, test or runtime
defect. Routine replies, speculative features and missing evidence do not justify
contributions. Reviews do not recursively trigger themselves. Generalized descriptions
and synthetic reproductions protect private writing, transcripts, paths and secrets.
Relevant validation and duplicate checks precede draft publication; uncertain
publication is reconciled before retry. No automatic merge or deployment occurs.
Failure preserves completed writing and unrelated work.

A draft or problem produces a brief notice in the next normally saved reply.
Durable association with that reply prevents duplicate notices after interrupted
acknowledgement; failed saves retain pending notices. No unsolicited turn is started,
previous replies remain unchanged and saved inclusion does not prove display.
See [the retrospective workflow](../workflows/retrospective.md) for controls and recovery.

## Updating existing legacy books

Updates are explicit maintenance through an external updater-capable installation.
Package installation, ordinary writing and resume do not check or apply updates.
A read-only preview checks published stable releases, defaults to the latest and
can select an exact newer stable version. Already-current is a no-op; discovery
failure is not. Downgrades, prereleases and source-checkout updates are refused.

Application requires the writer's reviewed target and exact book checkpoint.
Changed targets or book state require fresh review. Verify identity, installed
resource ownership, compatible records and runtime prerequisites before mutation.
Local framework modifications, uncertain ownership, unsafe paths, collisions,
unresolved saves and incompatible outstanding operations block application.
Only verified framework resources and framework-owned portions of shared rules
change. Manuscripts, exchanges, identities, creative settings, sessions, existing
history and unrelated staging choices are preserved. Maintenance creates one local
framework-only commit, no canon and no push. Recovery inspects and resumes the
exact operation without duplicate commits or automatic record migration.

Close legacy clients for the first update and keep the external recovery tool
available. On Windows retain the same scoped filesystem-access context across
preview, apply and recovery. Reload book instructions/skills before writing after
success. Update operations do not trigger creative saves or retrospectives.
See [the update workflow](../workflows/update.md) for commands and recovery boundaries.

## Delivery status and limits

The published 0.3.0 release supplies legacy onboarding and updating; 0.2.0 added
optional retrospectives. The 0.4.0 notebook remains an unpublished candidate.
See [release notes](releases/0.4.0.md) and the linked evidence for precise scope.

Legacy Windows Codex Desktop capture and update journeys have scoped evidence;
update host evaluation used explicitly authorized delegated input. Linux CLI and
package checks do not establish Linux Codex writing behavior. Direct native-user
update behavior, notebook Windows/Linux Desktop conversations and macOS support
remain unverified or deferred. English/Icelandic Unicode structural coverage does
not establish full literary parity. Voice capture, transcription and speech belong
to the host; exact spoken fidelity is unverified.

The owner is the initial hobby user. Novice recruitment and manual ratings do not
block use; owner assessment follows delivery. All latency targets were withdrawn
on 2026-10-28; timings are informational and optimization is deferred. Broader host,
durability and subjective quality claims need their own evidence. Chapter drafting,
literary editing, publishing, dashboards and additional host adapters are outside
the delivered foundation. Historical evaluations remain records of their tested
artifacts and dates; their old task numbers are not an active development process.
