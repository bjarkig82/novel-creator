# Feature Specification: Agent-Maintained Story Notebook

**Feature Branch**: Not created; specification-only change

**Created**: 2026-11-04

**Status**: Draft for review

**Input**: The writer wants to chat naturally with an agent about characters, storylines, plots and other novel topics while the agent automatically maintains useful summaries and story files. A full conversation archive is unnecessary. Sessions may begin with entirely new topics. Recaps are requested by the writer and limited to the requested topic; there is no automatic whole-book or session recap.

## Clarifications

### Session 2026-11-04

- Q: Should the first version support converting existing novels, or start with new novels only? → A: Start with new novels only. Existing-novel migration is deferred.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Brainstorm with automatic notes (Priority: P1)

As a writer, I want to explore a character or plot through ordinary conversation and have useful material saved without managing files or invoking a save command.

**Why this priority**: Conversation with durable, useful notes is the core product value.

**Independent Test**: Discuss a new character, consider two possible motivations, accept one characteristic and leave a question unanswered. Inspect the resulting notebook without requiring a transcript.

**Acceptance Scenarios**:

1. **Given** a novel with no character notes, **When** the writer explores a new character, **Then** the agent creates a relevant profile automatically as useful material emerges, without demanding a completed questionnaire.
2. **Given** two proposed motivations, **When** the writer explicitly chooses one, **Then** the selected motivation is recorded as accepted and the other remains an unselected possibility unless explicitly rejected.
3. **Given** an unanswered question, **When** the writer changes topic, **Then** the question remains open rather than acquiring an inferred answer.
4. **Given** meaningful new material in a reply, **When** the agent finishes that turn, **Then** relevant notes are updated without a separate save request or formal session closure.
5. **Given** a conversational turn that adds no meaningful story material, **When** the agent responds, **Then** it need not create a record or change a file merely to document that turn.

### User Story 2 - Start anywhere and request a focused brief (Priority: P1)

As a writer, I want to start a fresh session on any topic, or ask for a brief on a particular topic before exploring it.

**Why this priority**: Persistent context must help the conversation without making every session begin with a review of the book.

**Independent Test**: In a fresh agent session with access only to saved notebook files, request a brief about an existing antagonist, then begin discussing a previously unmentioned character.

**Acceptance Scenarios**:

1. **Given** saved notes from several topics, **When** the writer opens a session and introduces a new character, **Then** the agent engages with that character without an unsolicited recap or a requirement to finish the previous topic.
2. **Given** accepted facts, proposals and questions about the antagonist, **When** the writer asks for a brief about the antagonist, **Then** the agent concisely presents the relevant material, distinguishing those states and excluding unrelated topics.
3. **Given** no saved material about a requested topic, **When** the writer requests a brief, **Then** the agent states that no notes were found rather than inventing prior discussion.
4. **Given** a request for a broader recap, **When** the writer explicitly asks for one, **Then** the agent can summarize the requested broader scope.
5. **Given** two characters with the same display name, **When** a brief request cannot be resolved from context, **Then** the agent asks one focused question before choosing a character.

### User Story 3 - Revise decisions while retaining continuity (Priority: P2)

As a writer, I want my changes of mind reflected in the notes while the agent helps me notice consequences for established story material.

**Why this priority**: A notebook becomes misleading if old facts remain current or tentative ideas silently become canon.

**Independent Test**: Change an accepted character relationship with a known connection to a plot note, and inspect both the updated fact and the identified consequence.

**Acceptance Scenarios**:

1. **Given** an accepted fact, **When** the writer clearly replaces it, **Then** the current note reflects the replacement, its earlier value remains recoverable through history, and no redundant approval is requested.
2. **Given** a proposal that contradicts relevant accepted material, **When** it is explored, **Then** the agent surfaces the conflict and obtains direction before replacing affected canon.
3. **Given** an intentional lie or character misconception, **When** the agent maintains notes, **Then** it distinguishes that perspective from objective story facts.
4. **Given** a note correction, **When** the agent applies it, **Then** unrelated notes and manuscript content remain intact.

### User Story 4 - Continue after an interrupted session (Priority: P2)

As a writer, I want to return without remembering to close the previous session and without losing material the agent reported as saved.

**Why this priority**: Automatic notes must be useful during ordinary starts, stops and interruptions.

**Independent Test**: Complete turns with meaningful decisions, close the conversation without a closing command, and verify those decisions are available to a fresh session.

**Acceptance Scenarios**:

1. **Given** completed turns containing decisions and open questions, **When** the writer leaves without closing the session, **Then** saved topic notes and a concise working summary remain sufficient to continue.
2. **Given** a failed note update, **When** the agent responds, **Then** it discloses what remains unsaved and does not claim persistence or silently discard existing content.
3. **Given** a note edited externally since the agent read it, **When** an update would overwrite that edit, **Then** the agent preserves it and reconciles the change or asks for clarification.

### Edge Cases

- Brief praise, speculation, quoted dialogue and silence do not establish an accepted decision.
- A topic change does not reject previous proposals or resolve previous questions.
- A character rename updates relevant references without creating a second character accidentally.
- Related topics can share references without maintaining conflicting authoritative copies of a fact.
- Missing or unreadable notes are disclosed as unavailable; they are not interpreted as an empty story.
- A writer's direct file edits remain valid input; unclear or contradictory edits require reconciliation.
- Notes use the novel's configured writing language, including Unicode names and prose.
- Interruptions during the current turn may leave its latest material unsaved; the system does not promise exact transcript recovery.
- An existing novel using the legacy record system remains unchanged. Attempting notebook setup in an existing novel is refused with an explanation that migration is unsupported in this delivery.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The workflow MUST support natural conversation about characters, relationships, plots, storylines, setting, themes and other writer-selected topics without a fixed questionnaire or mandatory narrative structure. Guided brainstorming MUST be the default; the writer MUST be able to request freeform exploration or redirect the topic immediately.
- **FR-002**: The agent MUST automatically create and maintain human-readable story notes and concise working summaries as meaningful material develops. The writer MUST NOT need to issue routine save or file-management commands.
- **FR-003**: Meaningful material MUST include new substantive proposals, explicit decisions, revisions and unresolved story questions. Notes MUST capture these by completion of the relevant turn, subject to a disclosed save failure.
- **FR-004**: The notebook MUST distinguish accepted facts, tentative proposals, unselected alternatives, rejected ideas when relevant, and unresolved questions. Summary compression MUST NOT change these states.
- **FR-005**: A clear writer decision MUST update the relevant accepted material without repeated approval. Ambiguous creative direction MUST receive a focused clarification rather than an invented commitment.
- **FR-006**: The agent MUST maintain only the files needed for the developing novel. A new novel MUST NOT require prefilled character sheets, plot templates or empty files for every possible topic.
- **FR-007**: Starting or resuming a session MUST NOT trigger an unsolicited recap. The writer MUST be able to begin an unrelated or entirely new topic immediately.
- **FR-008**: On request, the agent MUST provide a concise brief limited to the requested topic or scope, using relevant saved notes and disclosing missing context.
- **FR-009**: The agent MUST retrieve relevant saved context before relying on prior decisions or assessing continuity. It MUST NOT require the writer to paste earlier conversations.
- **FR-010**: The agent MUST surface significant contradictions with available accepted material before making a conflicting canon change. Intentional ambiguity, character beliefs and reader revelation MUST remain distinct from objective story facts.
- **FR-011**: Revisions MUST retain recoverable history and a concise origin or decision explanation sufficient to understand why a current accepted fact changed. Exact messages, exact source spans and complete conversation archives MUST NOT be prerequisites for routine notebook operation.
- **FR-012**: Notes and summaries MUST have clear ownership: topic notes hold current story information; working summaries provide orientation and references rather than a competing canon.
- **FR-013**: Notes MUST remain readable and editable outside the agent platform. Story data MUST remain in an independent, version-controlled novel repository.
- **FR-014**: Routine creative conversation MUST NOT depend on per-exchange archival validation, a custom agent scheduler, contributor retrospectives, or framework update operations.
- **FR-015**: The agent MUST preserve existing content when updating notes, disclose failed saves, and avoid overwriting intervening edits without reconciliation. It MUST NOT claim that displayed content is saved until the update succeeds.
- **FR-016**: Automatic persistence MUST NOT require a formal session-close action. A full transcript and exact reply replay are explicitly unnecessary.
- **FR-017**: Notebook maintenance MUST NOT modify manuscript content or authorize external publication. Manuscript drafting and revision behavior are outside this feature's scope.
- **FR-018**: The initial workflow MUST support the existing Codex integration while keeping story content portable and shared creative instructions independent of the platform. Shared conversation, format, language and template resources MUST remain separate from the thin platform-specific entry adapter.
- **FR-019**: Notes and requested briefs MUST follow the configured novel language. English and Icelandic behavior MUST be evaluated in their claimed scopes.
- **FR-020**: The first delivery MUST support new novels only. Setup MUST refuse to overwrite or convert an existing novel, preserve its files, and explain that migration is not supported. Existing-novel migration and its design are deferred to a separate feature.

### Key Entities

- **Novel brief**: The writer's concept, creative preferences, language and explicit directions; unknown preferences remain unknown.
- **Topic note**: Current material about a character, plot thread, relationship, place or other meaningful topic, with distinguishable acceptance states and references to related notes.
- **Creative decision**: A concise record of the writer's acceptance or revision, its target and relevant rationale or context; it does not require a full transcript.
- **Open question**: An unresolved issue linked to its relevant topics; a topic change does not resolve it.
- **Working summary**: A concise orientation to recent exploration, decisions and open threads, referencing topic notes and maintained without requiring session closure.
- **Requested brief**: A derived conversational summary of the writer-selected scope; it does not become a second authoritative story record.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a scripted brainstorming journey containing a new character, a plot proposal, an explicit acceptance and an unanswered question, all meaningful items appear in appropriate saved notes with the correct states and no manual save request.
- **SC-002**: A fresh session can accurately brief each saved test topic using the notebook alone, without the previous conversation archive. Every assertion of an established fact in these briefs is supported by an accepted note.
- **SC-003**: In fresh-session journeys starting with a new topic, the agent produces no unsolicited recap and imposes no previous-topic completion step.
- **SC-004**: In acceptance journeys covering praise, speculation, alternatives and explicit decisions, no unaccepted idea is promoted to canon and every unambiguous decision is recorded without redundant approval.
- **SC-005**: In revision and continuity journeys, the replaced fact is no longer presented as current, its earlier state is recoverable, and the known relevant contradiction is surfaced without modifying a manuscript.
- **SC-006**: In persistence-failure and external-edit journeys, existing material is preserved and no failed update is reported as saved.
- **SC-007**: The writer can leave after a completed meaningful turn and later recover its saved decisions and questions without a session-close command.
- **SC-008**: The core brainstorming, note-maintenance and requested-brief journey succeeds without a complete transcript archive, contributor workflow or framework-update operation.
- **SC-009**: In a setup journey targeting an existing novel, setup refuses conversion, explains the limitation, and leaves existing files unchanged.

## Assumptions

- The initial user is the existing single writer using Codex; novice onboarding, multi-user collaboration and a dashboard are separate work.
- The writer's final preference supersedes the earlier suggestion of an automatic start-of-session recap: recaps are on request only.
- Guided brainstorming remains the default, and open/freeform exploration is available on request. Neither mode forces a questionnaire, recap or mandatory topic order.
- Directly maintained Markdown notes with Git history are the proposed starting approach, not an already implemented capability. A save helper must justify itself through an observed reliability need.
- There are no new latency targets. Verification focuses on usefulness, correct state, preservation and continuity behavior.
- This delivery applies only to newly created novels. Existing novels retain their current workflow and records; migration is deferred to a separate feature.

## Scope and Alternatives

The first delivery is a usable path for a new novel from conversation to maintained notes to a focused brief in a fresh session. It includes lightweight setup and necessary instructions, but excludes existing-novel migration, manuscript generation, automatic contribution retrospectives, dashboard work, exact transcript capture and automatic framework maintenance.

Three approaches were considered during discussion:

1. Retain the existing typed exchange system and shorten its instructions. This preserves archival guarantees but retains the complexity that motivated the change.
2. Make readable story notes primary and let the agent edit them using native capabilities and version history. This is the recommended direction reflected in this draft; it meets the writer's stated needs while giving up exact exchange replay.
3. Use the same notebook plus a small persistence helper. This remains available if evidence shows that native file operations cannot meet preservation requirements; it is not required upfront.

## Constitutional Alignment and Planning Constraints

Principles I, II, III, IV, V, VI, VII, IX and XI apply: simplicity, native agent capabilities, writer authority, continuity, automatic capture, portable versioned data, language support and verified incremental delivery.

Readable notes do not waive Principle VI's requirement for consistent machine-readable structure and references. Planning MUST define the smallest sufficient note contract and its compatibility rules; it MUST NOT assume that eliminating the exchange schemas eliminates all data contracts. If the proposed design would contradict this requirement, an explicit constitutional amendment must precede acceptance of that implementation.

Principle IV's traceability is satisfied in intent by concise decision origins, linked notes and recoverable revisions rather than exact conversation spans. Planning must explain how impact review works with those references and disclose that agent review cannot guarantee detection of all narrative contradictions.

Prior feature specifications remain historical contracts for existing bundles. Planning MUST identify which routine-writing requirements this feature replaces for new novels and which legacy capabilities remain separate. Existing novels remain on their installed workflow; transition design belongs to a future migration feature. This draft does not amend the constitution or change current installed behavior.
