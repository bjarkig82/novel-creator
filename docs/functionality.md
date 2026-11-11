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

Legacy realtime voice delegation additionally supports explicit
`input capture --source realtime_delegation --capture-file FILE --json` when the
exact complete current public wrapper is directly available. A strict direct
JSON container retains the raw wrapper and separate mixed earlier user/assistant
`transcript_delta`; only exact current `<input>` becomes the user message. Unicode,
whitespace, CRLF, ordinary angle text and ampersands are preserved. Truncated,
ambiguous, malformed, nested or mixed wrappers fail; structural delimiter text
inside fields is unsupported. This production source is labeled separately from
native input and evaluation delegation, with native/evaluation/novice evidence
false. Artifacts remain evidence rather than creative-source authority; transcript
context cannot become current instruction, acceptance or retrospective opt-in.

This route can capture/save without read_thread or stable host IDs and is
independent of retrospective enablement. Optional identity flags must be a genuine
host-supplied current thread/turn pair. Retrospectives still require normal opt-in,
confirmed completion save and genuine stable initiating task identity, which may
differ from the current completion turn. Missing identity means skip/disclose,
never infer one; later availability does not prove earlier identity. Without the
exact current wrapper, do not save or reconstruct it, scrape chats or fabricate a
native/evaluation event. The host owns transcription/fidelity, wrapper availability,
native chat tools and genuine identity. Novel Creator cannot restore chat-reading
tools, and no live host voice behavior or spoken fidelity has been verified.
The [installed entry](../workflows/entry.md) explains exact artifact retention and
save-before-display. This legacy transcript protocol does not apply to notebooks.

## Working memory and retrieval (0.6.0)

Published 0.6.0 adds legacy `context --view working` for ordinary
agent turns. It derives navigation from the freshly validated committed journal
on every read and reports the novel identity and source checkpoint. It returns
complete project settings/directions, a compact session summary, selected complete
current records, all active open/deferred findings, holds, coverage/availability
and the last saved response with display unconfirmed. There is no separate fact
store, trusted stale summary cache, provider call or database. The shared journal
remains the sole legacy authority; original record states, revisions and sources
are preserved. Capture/save semantics and canon authority are unchanged.

`--focus ID` is repeatable. `--query TEXT` matches all word terms as Unicode
NFKC-normalized, case-insensitive lexical substrings in saved text; it is not
semantic search. Focus and query combine, with explicit IDs first. Bounded
incoming/outgoing record links expand relevant context, including links from
explicitly focused/query-matched globals; session navigation lists do not expand
recursively. With no focus/query, recent session links and recent changes seed
selection. `--session ID` selects the summary/fallback and saved-response scope
without filtering explicit/query hits elsewhere.

`--limit N` defaults to 12, range 1–100, for selected records; the complete global
project and active findings are additional. It is not a token budget. Too many
explicit IDs fails with error 2 rather than dropping them; missing IDs fail with
error 4. Retrieval flags require the working view. Omissions, outstanding linked
IDs and historical revision references are explicit. A query miss is not evidence
that a fact is absent. Agents retrieve relevant complete records and exact sources
before relying on them and disclose incomplete continuity coverage.

`context --view current` preserves all current fields/records while omitting the
exchange archive. `--view full`, also the unchanged default CLI/Python API, retains
the prior complete shape. Broader requests such as all open questions need a
broader read. Inspect retrieves exact historical wording and artifacts. All views
fail closed on damaged committed history. The
[installed workflow](../workflows/working-context.md) requires fresh working reads
before each response, allows reuse of valid loaded guidance/runtime, and preserves
exact input capture and save-before-display, including creative commentary.

Native notebooks instead use the existing `notebook/working-summary.md` as derived
navigation into complete relevant owning topic files. All roles share those saved
files, stable IDs, item states and decision origins. After saves or writer edits,
affected summaries are reconciled from owning notes; recollection and stale
summaries cannot establish canon. No legacy runtime is used for notebook writing.
Neither path establishes exhaustive continuity or measured spoken-response latency.

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

The published 0.4.0 package adds `novel-creator notebook init "My Novel"` for
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
data, never instructions granting permissions or external actions. Published
0.5.0 extends the notebook with manuscripts as described below. Publication,
automatic upgrades and notebook migration remain outside this workflow.
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
literary quality. These resources ship only into new notebooks, without
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

### Writer help (0.7.0)

New notebooks initialized with published 0.7.0 install
`$novel-help`, a read-only guide to next steps and actually installed chat skills.
No input is required; optional freeform input can name a command, goal, topic or `commands` for the
compact inventory. It explains purpose, expected/optional inputs, natural-language
names/descriptions versus optional IDs or paths, ambiguity handling, save effects
and a copyable example. A bare invocation offers a few context-appropriate choices,
including idea discovery when the notebook has no concept. Help executes no task,
switches no role and writes no notes, summaries, reviews or checkpoints. Quoted
examples are not invocations. Availability comes from the installed notebook,
not an assumption that older notebooks contain newer entries. This addition is
not in published 0.6.0 and adds no CLI command, migration or automatic update.
See [help usage](writing-agents-usage.md#help-choosing-a-next-step-070) and
the shared [help workflow](../notebook/workflows/help.md).

### Targeted clarification and analysis (0.7.0)

New notebooks initialized with published 0.7.0 install
`$novel-clarify` and `$novel-analyze`; they are not in published 0.6.0.
Ordinary-language requests also select these methods.
[Clarification](../notebook/workflows/clarify.md)
prioritizes consequential gaps in a named character, outline, scene, chapter or
other target and asks one question at a time, defaulting to at most five per pass.
Clear answers update owning notes incrementally with stable IDs, decision origins
and recoverable history. Deferred questions remain open; intentional ambiguity,
freeform answers and early stopping are supported. It does not rewrite manuscripts.

The [0.7.2 unpublished candidate](releases/0.7.2.md) adds suggested answers in both
formats: each substantive question normally offers 2–4 concise labeled
possibilities plus **Custom — type your own answer**. Writers can reply with a
label, adapt a suggestion or supply their own answer, and can request fewer or no
suggestions. Unknown, skip and defer remain available; nothing is selected
automatically. Package installation does not refresh project-local copies.
New projects receive the guidance at initialization; existing legacy novels use
their reviewed framework update. Existing notebooks use a previewed update that
adds missing resources or replaces original published 0.7.0/0.7.1 clarify files
identified by frozen normalized ownership hashes. Customized files are refused;
story notes, history, custom instructions and unrelated staging are preserved.
See the complete [upgrade steps](upgrading-projects.md), including Codex reload.

[Analysis](../notebook/workflows/analyze.md) compares selected material with
relevant accepted notes, directions and outlines, returning prioritized findings
with actual evidence, stable finding IDs, revision basis and limits. It checks
consistency, causality, knowledge/revelation, chronology and applicable outline
coverage; subjective craft advice is labeled separately. Missing context is not
assumed absent. Analysis is strictly read-only, including no automatic notes,
review files, summary changes or checkpoints. Explicitly requested follow-up
saves/revisions use existing review/manuscript workflows. Ordinary `$novel-review`
retains its saved-review behavior. These additions change neither legacy
persistence nor existing notebooks; no migration, new CLI command or automatic
resource update is added. See [usage examples](writing-agents-usage.md#clarify-and-analyze-070).

### Writing roles and manuscripts (0.5.0)

New notebooks initialized with published 0.5.0 install six
`.codex/agents/` definitions: `novel_orchestrator`, `novel_brainstormer`,
`novel_researcher`, `novel_scene_writer`, `novel_chapter_writer` and
`novel_reviewer`. Root instructions make the main conversation follow the
orchestrator by default. Ordinary-language specialist requests are intended to
persist until the writer changes roles, subject to native client support.
Discovery, delegation and ongoing direct specialist turns remain unverified in
the target desktop; unavailable capabilities must be disclosed. Same-context
review is self-review, not independent assessment.

All roles share the notebook's authoritative facts. Manuscripts, research and
reviews are created on demand, with no empty forms at setup. A manuscript index
records stable identities and one prose owner for each scene; incorporation moves
a standalone scene into its chapter. Identifiable draft/revision requests authorize
scoped saves, with exact current prose preserved in verified history or historical
copies before replacement. Draft inventions remain proposals until accepted;
research and review alone do not authorize manuscript rewriting. Research records
actual sources and uncertainty; independent review records passage-based findings
and the reviewed revision.

See the [practical usage guide](writing-agents-usage.md) for examples and optional
skills, and the shared [role](../notebook/workflows/agents.md),
[manuscript](../notebook/workflows/manuscript.md),
[research](../notebook/workflows/research.md) and
[review](../notebook/workflows/review.md) rules for details. These resources add no
per-turn Python requirement or automatic outline step. Existing notebooks and
legacy resources are unchanged, with no new migration or updater command.

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

The [0.7.2 candidate](releases/0.7.2.md) prepares clarification suggestions,
custom answers and an explicit replacement path for unchanged published notebook
clarification resources. Qualification and publication remain pending.

The latest verified published package is [0.7.1](releases/0.7.1.md), published
2026-11-10. Its protected publication succeeded and the public PyPI wheel/source
hashes match the corrected qualified candidate. It extends focused methods to
legacy novels and existing notebooks through explicit project updates; see the
[upgrade guide](upgrading-projects.md). Remote annotated-tag identity and native
Codex behavior are not established by this package metadata verification.

The [0.7.0 release](releases/0.7.0.md), published 2026-11-10, adds the new-notebook clarification,
read-only analysis and help methods above. Full Linux and Windows automated
release qualification, actual public archive hashes, public CI checks and
independent clean installation passed. The independent local installation passed
on retry after initial index propagation; publication and CI were not repeated.
See the
[release evidence](../tests/evaluations/release-0.7.0.md) for scope and provenance.

The [0.6.0 release](releases/0.6.0.md), published 2026-11-06, adds the working-context
views and focused memory guidance above, plus notebook responsiveness guidance.
The exact artifacts passed automated Windows/Linux qualification, public hashes
matched, and independent clean named-package installation and Windows/Linux public
checks passed. The Linux public check passed on retry after an initial index
propagation delay; upload was not repeated. See the
[release evidence](../tests/evaluations/release-0.6.0.md). Installing a package
leaves existing pinned legacy books and native notebooks unchanged;
legacy resources need an explicit supported update and notebook migration/updating
is not introduced. Actual voice pause causes/timing, playback fidelity and native
host behavior for these changes remain unverified.

The published 0.4.0 release adds the native notebook alongside legacy onboarding
and updating; 0.2.0 added optional retrospectives.
See [release notes](releases/0.4.0.md) and the linked evidence for precise scope.

The [published 0.4.1 release](releases/0.4.1.md) adds the explicit legacy
realtime capture route described above and strengthens synthetic retrospective
transport tests. Proxy/certificate preservation already shipped in 0.4.0; these
tests do not establish new live network behavior. Live PyPI availability and
artifact hashes were verified separately from the historical release ledger.

The [0.5.0 release](releases/0.5.0.md), published 2026-11-06, adds the
new-notebook writing roles and manuscript/research/review workflows described
above. The exact artifacts passed automated Windows/Linux release qualification;
public artifact hashes, Windows/Linux public installation checks and an independent
clean named-package installation were verified. See the
[release evidence](../tests/evaluations/release-0.5.0.md).
Earlier [focused resource and package checks](../tests/evaluations/writing-agents.md)
retain their recorded scope.
[Native desktop acceptance](../tests/evaluations/writing-agents-host.md) remains
pending. The writer authorized implementation and automated-only qualification;
these checks do not establish native discovery, delegation or direct specialist
controls.

Published 0.4.1 also improves agent-led initialization: generated project
instructions direct ongoing work through Novel Creator, and legacy setup returns
runtime/project handoff paths in both shorthand and brief-file modes. Agents must
read target instructions and saved context before creative replies. Legacy runtime
discovery verifies available environment evidence before asking the writer; it
does not add per-turn Python to notebooks. Installing a package does not apply
these improvements to existing stories. Hosts do not automatically switch
projects, and parent workspaces do not guarantee nested instruction discovery.
See [agent-led setup](../workflows/start-here.md#ask-your-agent-to-set-up-a-story).

Legacy Windows Codex Desktop capture and update journeys have scoped evidence;
update host evaluation used explicitly authorized delegated input. Linux CLI and
package checks do not establish Linux Codex writing behavior. Direct native-user
update behavior, notebook Windows/Linux Desktop conversations and macOS support
remain unverified or deferred. English/Icelandic Unicode structural coverage does
not establish full literary parity. Voice recording, transcription and speech belong
to the host; exact spoken fidelity and live host use of the explicit realtime
wrapper capture remain unverified.

The owner is the initial hobby user. Novice recruitment and manual ratings do not
block use; owner assessment follows delivery. All latency targets were withdrawn
on 2026-10-28; timings remain informational. Focused context retrieval does not
establish actual voice latency improvement. Broader host,
durability and subjective quality claims need their own evidence. Scene/chapter
drafting and scoped revisions are notebook workflows with the limits
above; publishing, dashboards and additional host adapters remain outside the
delivered foundation. Historical evaluations remain records of their tested
artifacts and dates; their old task numbers are not an active development process.
