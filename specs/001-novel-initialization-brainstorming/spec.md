# Feature Specification: Novel Initialization and Guided Brainstorming

**Feature Branch**: `main` (existing branch; no branch hook configured)

**Created**: 2026-10-21

**Status**: Draft — validated for planning

**Input**: User description: "Initialize an independent novel, brainstorm across sessions, automatically capture ideas and accepted canon, and guard continuity while preserving human creative authority and platform independence."

## Clarifications

### Session 2026-10-21

- Q: When should brainstorming conversations and captured story information be saved automatically? → A: Save every user message and agent response, including captured ideas and decisions, before continuing.
- Q: If relevant saved canon cannot be read, should the agent pause changes to canon until that information is restored? → A: Allow exploration; block affected canon changes until the relevant records are readable.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start a Novel from Any Starting Point (Priority: P1)

As a creative director with little or no writing experience, I can start conversationally with an existing concept, a vague idea, or no idea, and leave with a persistent novel workspace.

**Why this priority**: A usable starting point enables every subsequent workflow.

**Independent Test**: Initialize separate novels with and without a concept, then reopen them. Each provides a revisable creative brief without requiring brainstorming.

**Acceptance Scenarios**:

1. **Given** no concept, **When** the user initializes a novel and skips uncertain answers, **Then** a workspace is created with a temporary working title, explicit unknowns, no invented canon, and an offer to start guided brainstorming.
2. **Given** an existing concept, **When** the user supplies it and preferences, **Then** original information is preserved, interpretations are distinguishable, and only clearly accepted facts become canon.
3. **Given** conversational setup, **When** several preferences are supplied together, **Then** they are recorded without repetitive questions and remaining questions can be skipped.
4. **Given** an initialized novel, **When** its title or preferences change, **Then** its identity, sessions, and references remain intact.
5. **Given** existing work at the chosen location, **When** initialization is repeated, **Then** content is preserved and continuation or a separate novel is offered.

---

### User Story 2 - Develop Ideas through Creative Conversation (Priority: P1)

As a writer, I can explore any story topic with a novelist and coach who contributes ideas, adapts to my needs, and lets me direct the conversation.

**Why this priority**: Guided collaboration must deliver creative value without requiring a developed premise.

**Independent Test**: With a prepared brief, explore a premise, character, and setting, change modes, and redirect the conversation without requiring later writing features.

**Acceptance Scenarios**:

1. **Given** a new session, **When** brainstorming starts, **Then** guidance is the default, the agent offers a useful starting point even without a concept, and normally asks one focused question at a time.
2. **Given** guided brainstorming, **When** the user requests open-ended exploration and later guidance, **Then** the mode changes in the next response without losing context, ideas, or canon.
3. **Given** genre, complexity, and style preferences, **When** exploring possibilities, **Then** guidance contributes relevant conflicts, motivations, and alternatives and explains weaknesses constructively without imposing a narrative methodology.
4. **Given** character exploration, **When** the user redirects to worldbuilding or requests fewer suggestions, **Then** the next response follows that direction while preserving earlier work.

---

### User Story 3 - Resume without Retelling the Story (Priority: P1)

As a creative director, I can resume an existing session or start a focused one and rely on automatic records of discussions, ideas, decisions, and unresolved questions.

**Why this priority**: Persistence enables extensive brainstorming without manual administration.

**Independent Test**: Reopen a prepared novel with two saved sessions in a fresh interaction, resume one and create another, then compare recalled information with its sources.

**Acceptance Scenarios**:

1. **Given** an exchange containing character ideas, alternatives, and an unanswered question, **When** the agent responds, **Then** the user message, agent response, and captured items with status and origin are saved automatically before continuing, without a note-taking or save request.
2. **Given** multiple saved sessions, **When** one is resumed after ending the original interaction, **Then** its focus, relevant canon, decisions, and unresolved questions are available without asking the user to repeat recorded information.
3. **Given** a new topic-focused session, **When** the user asks how a character relates to an event or plot thread, **Then** recorded connections are explained with sources and new interpretations are labeled proposals.
4. **Given** an incorrect capture, **When** the user corrects it, **Then** the correction and its origin are retained without erasing decision history.

---

### User Story 4 - Establish and Revise Canon (Priority: P1)

As a creative director, I can accept ideas naturally, explore alternatives safely, and deliberately change established facts with a record of what changed and what it affects.

**Why this priority**: Reliable acceptance boundaries preserve human creative authority.

**Independent Test**: Use prepared proposals and canon to test clear acceptance, ambiguity, rejection, and explicit revision; inspect resulting facts and history.

**Acceptance Scenarios**:

1. **Given** a non-conflicting proposal, **When** the user says "That's brilliant! Let's make Thomas the murderer," **Then** that fact becomes canon automatically with its accepting statement and session recorded, without a second approval.
2. **Given** that proposal, **When** the user says "Maybe Thomas," praises it without selecting it, remains silent, or quotes a character's claim, **Then** no objective fact is established from that statement.
3. **Given** several alternatives, **When** one is explicitly accepted and another rejected, **Then** their states remain distinguishable and other alternatives remain unaccepted.
4. **Given** canon, **When** the user explicitly requests a revision with an unambiguous target and replacement, **Then** it is recorded without redundant approval, the prior fact remains in history, and directly affected information is identified for review.
5. **Given** apparent acceptance conflicting with explicit creative direction or protected approved content, **When** applying it would cross that boundary, **Then** the conflict is explained and clarification is required; this feature leaves approved manuscript text unchanged.

---

### User Story 5 - Catch Continuity Problems during Exploration (Priority: P1)

As a creative director, I receive significant contradiction warnings before the agent develops a conflicting idea further, while retaining freedom to create mysteries, deception, and ambiguity.

**Why this priority**: Early intervention avoids building the concept on accidental contradictions.

**Independent Test**: Use prepared conflicts involving motivation, chronology, knowledge, plot dependencies, world rules, and relationships, alongside intentional deception and unresolved alternatives.

**Acceptance Scenarios**:

1. **Given** canon that a character learns a secret after an event, **When** a new idea requires knowingly acting on it earlier, **Then** the next response interrupts conflicting development, identifies the established knowledge and timing, explains consequences, and offers resolutions.
2. **Given** an active contradiction, **When** the user rejects or revises the idea, deliberately changes canon, or explicitly defers it, **Then** that disposition is recorded; a deferred conflict remains visible and cannot silently become settled canon.
3. **Given** a recorded lie, unreliable viewpoint, or hidden truth, **When** character or reader knowledge differs from author truth, **Then** the difference alone is not treated as an objective continuity error.
4. **Given** uncertainty about whether a significant conflict is intentional, **When** development depends on resolving it, **Then** the agent explains the uncertainty and asks a focused question without changing canon.
5. **Given** a recorded story connection, **When** the agent notices a foreshadowing or motivation opportunity, **Then** it offers a sourced, non-blocking proposal without changing canon.

---

### User Story 6 - Retain Language and Platform Independence (Priority: P2)

As a creative director, I can develop an English or Icelandic novel and retain understandable, connected story information independently of its original agent or a dashboard.

**Why this priority**: Language support and portability protect the work. P2 sequences delivery after the core loop; both remain required for release.

**Independent Test**: Use equivalent English and Icelandic examples and reconstruct their story information from saved records without the originating agent.

**Acceptance Scenarios**:

1. **Given** either supported language, **When** initializing, brainstorming, accepting a fact, and checking continuity, **Then** the workflow supports that language and preserves names, spelling, and meaning.
2. **Given** a saved novel opened without its originating platform, **When** a person inspects authoritative records, **Then** settings, sessions, canon, proposals, sources, and history are understandable.
3. **Given** connected story records, **When** an independent consumer reads them, **Then** characters, locations, events, plot threads, relationships, and knowledge states are distinguishable using documented references without interpreting conversation prose or reorganizing authoritative information.

### Edge Cases

- Empty answers, uncertainty, mixed languages, duplicate names, and title changes must not lose information or conflate entities. Ambiguous references require clarification before canon changes.
- Interrupted setup and sessions must distinguish saved from unsaved work and resume from the last confirmed saved state. Saving failures must be reported and further authoritative changes paused until saving succeeds.
- Reprocessing an accepted exchange must not duplicate decisions or canon changes. Conflicting overlapping edits must be surfaced before overwriting either version.
- Partial acceptance of a compound proposal applies only to clearly selected elements; unclear targets remain unaccepted pending clarification.
- Hypothetical scenes, mutually exclusive alternatives, character beliefs, unknown timing, and withheld revelations must not be merged into objective truth.
- Canon revisions must identify directly affected recorded information without silently rewriting unrelated facts. Unrecorded dependencies cannot be guaranteed detectable.
- Missing, damaged, or unsupported records must be identified as unavailable; the agent must not claim a complete continuity check when relevant context is unreadable. Exploration may continue as proposals, but affected canon changes must remain paused until the relevant records are readable.
- Summaries of long sessions must retain source references and cannot override authoritative facts or hide unresolved contradictions.

## Requirements *(mandatory)*

### Functional Requirements

#### Initialization and guidance

- **FR-001**: The system MUST provide a simple initialization entry point and conversational setup accepting an existing concept, a vague idea, or no concept. Users MUST be able to skip questions or indicate uncertainty without blocking creation (Story 1).
- **FR-002**: Setup MUST offer working title, initial concept, genre and subgenres, audience, manuscript language, tone, style, narrative perspective, complexity, workflow preferences, and human review preferences. Supplied answers MUST be preserved without repetitive questioning, unknowns distinguished, and later changes supported (Story 1).
- **FR-003**: Each novel MUST have an independent Git repository as its authoritative home. Initialization MUST preserve existing content, distinguish identity from title, and finish by offering optional guided brainstorming (Stories 1, 6).
- **FR-004**: New sessions MUST default to guided brainstorming; natural-language requests MUST switch to open-ended exploration or back, or redirect topics, effective in the next response (Story 2).
- **FR-005**: Guidance MUST normally ask one focused question per turn, explain techniques accessibly, contribute creative possibilities, challenge weak ideas constructively, and adapt to genre, complexity, and preferences without requiring a particular narrative methodology (Story 2).
- **FR-006**: Users MUST be able to explore characters, plot, themes, settings, worldbuilding, relationships, or other story topics and reduce suggestions without losing recorded work (Story 2).
- **FR-007**: Interaction MUST support natural language and accept host-provided voice transcriptions where available without requiring visual forms. Audio capture, transcription, and synthesis remain host responsibilities (Stories 1, 2).

#### Sessions, capture, and creative authority

- **FR-008**: Users MUST be able to identify, list, start, resume, and close multiple topic-focused sessions per novel. Fresh interactions MUST recover relevant saved canon, decisions, ideas, and unresolved questions (Story 3).
- **FR-009**: After every exchange, the system MUST automatically save the user message, agent response, and captured story information before continuing, without requiring a save request or session closure. Captures MUST include relevant ideas, character information, plot developments, world details, relationships, events, alternatives, questions, and creative decisions with source references. Saving failures MUST follow FR-014 (Story 3).
- **FR-010**: Captured items MUST distinguish proposed, accepted, rejected, and unresolved states. Conversations, extracted ideas, acceptance decisions, and current canon MUST remain distinguishable; lack of acceptance MUST NOT imply canon (Stories 3, 4).
- **FR-011**: Clear user acceptance of an identifiable idea MUST establish the corresponding canon automatically and record its accepting statement and session without another approval, subject to FR-013 and FR-017. Praise alone, silence, speculation, quoted dialogue, and ambiguous references MUST NOT establish objective facts (Story 4).
- **FR-012**: Users MUST be able to correct captures and explicitly revise or reverse facts. The system MUST retain prior and current states, the revision's origin, and references to directly affected recorded elements needing review. Superseded facts MUST NOT appear as current (Stories 3, 4).
- **FR-013**: Review preferences MUST govern routine autonomy while preserving human authority. Routine checkpoints MUST support on request (default), session closure, or every exchange. Checkpoints MUST summarize captured proposals, decisions and open questions and pause agent-initiated exploration until user direction, without delaying saving or requiring repeated approval of clearly accepted facts. Conflicts with explicit creative direction MUST require clarification before the conflicting change. This feature MUST NOT edit approved manuscript text; a canon change MUST NOT authorize later manuscript revisions (Story 4).
- **FR-014**: The system MUST disclose saving failures and the last confirmed saved state, support interruption recovery, prevent duplicate decision application, and surface conflicting overlapping edits rather than silently overwrite them (Story 3; Edge Cases).

#### Continuity and connections

- **FR-015**: The Continuity Guardian MUST evaluate new ideas against relevant available canon and knowledge during brainstorming. Significant contradictions make a recorded event or rule impossible, invalidate an accepted plot dependency, require unavailable character knowledge, or directly conflict with explicit established motivations, relationships, or backstory (Story 5).
- **FR-016**: On detecting a significant contradiction, the next response MUST interrupt further development of the conflicting idea, identify established information and sources, explain likely consequences, and offer resolutions. Uncertainty and missing information MUST be disclosed instead of asserted as proven contradictions. If relevant saved canon is unreadable, exploration MAY continue as proposals, but affected canon changes MUST remain paused until the relevant records are readable (Story 5).
- **FR-017**: Users MUST be able to reject or revise the idea, deliberately revise canon, explain an intentional technique, or defer the conflict. Conflicting development MUST remain paused until the user's direction permits it. Deferred ideas MAY remain unresolved alternatives but MUST NOT silently establish canon. An unambiguous explicit canon revision already authorizes that revision without redundant approval, except at the FR-013 boundary (Stories 4, 5).
- **FR-018**: Checks MUST distinguish author truth, character knowledge and beliefs, and reader revelations at relevant story points, accounting for recorded deception, unreliable narration, mystery, and intentional ambiguity (Stories 5, 6).
- **FR-019**: Recorded connections MUST be explainable with their sources. Creative opportunities MAY be suggested but MUST remain proposals, be non-blocking, and respect requests to reduce suggestions (Stories 2, 3, 5).

#### Story knowledge, language, and portability

- **FR-020**: Story information MUST represent characters and characteristics, relationships, locations, events, timelines, plot threads, established facts, ideas, decisions, and questions with distinguishable identities and references that survive title or name changes (Stories 1, 6).
- **FR-021**: Fact and knowledge assertions MUST retain subject, meaning, perspective, holder or reader audience, relevant story point or interval when known, status, and source. Unknown timing and withheld information MUST remain distinguishable from established absence or falsehood (Stories 5, 6).
- **FR-022**: Authoritative records MUST be human-readable, version-controllable, and interpretable without the originating platform. Ownership, reference meanings, and record version MUST be documented; derived summaries and future views MUST be identifiable and MUST NOT become competing authorities (Story 6).
- **FR-023**: Saved information MUST allow independent consumers to reconstruct entities, relationships, event ordering, knowledge distinctions, and decision history without extracting them again from conversations. Future incompatible changes MUST have documented migration and recovery guidance (Story 6).
- **FR-024**: Manuscript language MUST be configurable per novel with English and Icelandic supported. Setup, guidance, capture, acceptance, and continuity MUST be evaluated in both languages, preserving their characters and avoiding English-only story assumptions (Story 6).
- **FR-025**: Codex MUST be the initial supported host. Shared methodology, story records, and workflow definitions MUST remain independent of replaceable host integration. Additional hosts are deferred, and novels MUST remain usable without a dashboard (Story 6).
- **FR-026**: Onboarding MUST explain initialization, brainstorming, resumption, inspecting knowledge, resolving contradictions, and revising canon. Verification MUST distinguish automated structural checks, agent judgments, and human approval; valid record structure alone MUST NOT be reported as narrative consistency (Stories 1–6).

### Key Entities *(include if feature involves data)*

- **Novel Project**: Stable identity, revisable title, creative brief, manuscript language, workflow and review preferences; owns its sessions and story information independently of other novels.
- **Brainstorming Session**: Identity, topic, interaction mode, conversation history, continuation context, and references to captured items and decisions.
- **Idea**: A possibility about story elements, with status, alternatives, source, and accepting or rejecting decisions. Acceptance may establish several related facts while preserving original wording.
- **Story Element**: Identifiable character, location, event, or plot thread with characteristics and sourced connections. Events support known, partial, or unknown timeline ordering; plot threads may depend on facts and events.
- **Relationship**: A sourced connection between identified elements, its meaning, status, and applicable time when known; may be proposed rather than canonical.
- **Fact or Knowledge Assertion**: A claim distinguished as author truth, a particular character's knowledge or belief, or a reader revelation, with timing and source. Beliefs may be false; revelation order may differ from event order.
- **Creative Decision and Revision**: User-directed acceptance, rejection, or change; preserves source, affected items, previous and resulting state, and references needing impact review.
- **Unresolved Question**: An open issue, linked context, alternatives, and eventual resolution. Unanswered questions never imply facts.
- **Continuity Finding**: A conflict or uncertainty with sources, consequences, affected elements, resolutions, user disposition, and intentional narrative explanations; distinguishable from non-blocking creative opportunities.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 4 of 5 novice evaluators can initialize from no concept, skip uncertain preferences, and reach the brainstorming invitation within 10 minutes without outside assistance (Story 1).
- **SC-002**: In both languages, all supplied preferences and original concept statements in acceptance examples survive reopening unchanged in meaning, and no skipped detail is invented as canon (Stories 1, 6).
- **SC-003**: Across three sessions and a fresh interaction, all 20 designated ideas, 10 explicit decisions, and 5 unresolved questions are recoverable with correct state and source without manual note-taking (Story 3).
- **SC-004**: Across at least 12 clear-acceptance and 12 non-acceptance examples covering partial selections and both languages, every unambiguous, non-conflicting acceptance establishes intended facts without repeated approval; no ambiguous, rejected, or hypothetical item becomes canon (Story 4).
- **SC-005**: Every designated significant conflict in a review set covering the six contradiction categories interrupts conflicting development in the next response with evidence and resolutions. All designated intentional mysteries, lies, and unreliable viewpoints remain distinguishable from accidental contradictions (Story 5).
- **SC-006**: For five deliberate canon revisions, current and previous facts, decision origins, and all directly linked affected elements remain inspectable; no approved manuscript text changes (Story 4).
- **SC-007**: Mode switches and topic redirections take effect in the next response in every acceptance example. At least 4 of 5 novice evaluators rate guidance at least 4 out of 5 for usefulness and creative control (Story 2).
- **SC-008**: Without the original agent or dashboard, an independent reader or consumer can recover every designated entity, relationship, event ordering, knowledge perspective, and decision origin in a representative saved novel without restructuring records or interpreting conversation prose (Story 6).
- **SC-009**: Interruption, unavailable-context, failed-save, duplicate-processing, and overlapping-edit exercises each preserve the last confirmed authoritative state and disclose incomplete work; none reports unsaved work or incomplete continuity review as successfully completed. In the unavailable-context exercise, proposals may be explored, but no affected canon change is applied until the relevant records are readable (Story 3; Edge Cases).

## Assumptions

- One human creative director manages each novel in this release. Collaboration, role permissions, and concurrent coauthor workflows are deferred; accidental overlapping changes still require protection.
- New sessions start guided unless the user requests open-ended exploration at entry. Resumed sessions retain their mode.
- English is the initial default when no preference is supplied; Icelandic remains required for release. Temporary titles and explicit unknowns allow setup without creative commitments.
- Supplied concepts are source material, not blanket approval of inferred facts. Only clear commitments establish canon; unclear acceptance targets or intentional contradictions require focused clarification.
- Review preferences govern this brainstorming slice. Future drafting preferences may be recorded without claiming those workflows exist.
- Continuity operates on available recorded information and involves agent judgment, not a guarantee of catching every literary inconsistency. Evaluation must include definite conflicts and intentional narrative techniques.

### Scope Boundaries and Dependencies

- **Included**: Initialization, guided and open-ended brainstorming, multiple persistent sessions, automatic capture, explicit acceptance, canon revision history, significant continuity interruptions, basic connection explanations, English and Icelandic, and portable story knowledge. Stories 1–5 form the core loop; Story 6 is required before release.
- **Excluded**: Chapter drafting, scene generation, literary editing, manuscript publication, dashboard implementation, graphical visualization, autonomous multi-chapter writing, advanced orchestration, and additional host integrations. Approved manuscript boundaries preserve future compatibility without adding text editing.
- **Governance**: Constitution 1.0.0 governs this feature, particularly principles I–IX and XI. Principle X's dashboard-specific delivery criteria remain future work; conversational and host-supported voice interaction apply here.
- **Operational dependencies**: A supported conversational agent host and access to each novel's version-controlled workspace. Voice depends on host capabilities; delivered onboarding must disclose installation requirements and unavailable capabilities.
- **Planning questions**: Determine dedicated-agent versus reusable-skill/workflow responsibilities, define portable record contracts and compatibility rules, and choose the simplest host integration. This specification selects no implementation technologies, custom execution engine, or sophisticated graph engine. Added complexity requires demonstrated need under the constitution.
- **Future consumers**: Architecture, outlining, drafting, editing, and read-only dashboard features will consume these identities, sources, canon, knowledge states, and preferences. This release depends on none of their implementations and does not authorize dashboard editing.
