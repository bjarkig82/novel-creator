# Data Model: Novel Initialization and Guided Brainstorming

Status: Phase 1 design; executable JSON Schemas are implementation work.
The [storage contract](contracts/storage.md) defines serialization and authority.

## Common record rules

All structured records have `id` (UUID), `kind`, `revision` (positive integer),
`previous_revision` (null at creation, otherwise exact prior revision),
`source_refs` (typed message or bootstrap-artifact references, defined below), and
`created_exchange_id`. Subsequent versions retain their identity, increase revision
by one and record a sourced decision/reason. Exchange order resolves revision
application; wall-clock time does not. IDs never derive from names or titles.
All text is UTF-8; user text is preserved rather than translated or ASCII-folded.
References contain stable IDs and, where historical meaning matters, revisions.

Structured records own extracted meaning; message records own exact statements.
Derived context cannot change either. A source reference is evidence of origin,
not proof of human approval. Approval is a separate Creative Decision judged by
the agent and checked structurally. All required fields must be present; unknown
values are explicit null/unknown values, never invented defaults or empty facts.

### Source reference types

A message source has `type: message`, `exchange_id`, `message_id` and an optional
Unicode code-point range. A bootstrap source has `type: bootstrap_artifact`,
`exchange_id`, `artifact_id` and a JSON Pointer to a preserved brief field.
Bootstrap envelopes contain `input_artifacts`: stable artifact IDs, original
UTF-8 input text, parsed JSON value and a SHA-256 digest of the original bytes.
References resolve within the committed envelope; a pointer must identify an
existing field. Preserve the original input rather than relying on its external
file path. Omitted/default settings have an explicit system-default origin and
empty source_refs, never fabricated user sources. Bootstrap artifacts establish
provenance of supplied settings/concepts only; they cannot authorize canon.
Creative Decisions still require an actual user message and accepting span.

## Exchange envelope

Fields: `schema_version` ("1.0"), `novel_id`, `exchange_id`, `sequence` (integer
starting at 1), `previous_exchange_id` (null for bootstrap), `previous_digest`
(null for bootstrap), `session_id` (nullable for initialization/project operations),
`expected_git_head` (commit ID; null for an unborn bootstrap repository), `recorded_at` (UTC timestamp), `messages`,
`record_versions`, `continuity_review`, and `payload_digest`.

Messages have stable `message_id`, role (`user` or `assistant`) and exact `text`.
An ordinary conversational exchange has one current user message and one prepared
assistant response. Initialization and installation metadata exchanges may have
no conversation and must be labeled `operation: bootstrap`; they cannot fabricate
user authorization. `operation` is `bootstrap` or `conversation` or `maintenance`.
Maintenance is limited to explicit recovery/migration and cannot introduce canon.

`continuity_review` contains `coverage` (complete/incomplete/not_applicable),
`reviewed_record_refs`, `unavailable_refs`, `canon_hold_refs` (IDs or wildcard),
`finding_ids`, and an agent assessment summary. Complete means the declared scope
was available, not that every possible literary inconsistency was detected.

Digest: SHA-256 of canonical JSON (UTF-8, sorted object keys, compact separators,
no NaN/Infinity, excluding `payload_digest`); arrays retain order. Hashes detect
accidental changes; they are not signatures or evidence of acceptance.

## Novel Project

Fields: stable identity, title, `original_concept`, structured `creative_brief`,
`manuscript_language` (BCP-47 code; en default, is supported), workflow/review
preferences and explicit creative direction entries with sources.
Brief keys cover genre/subgenres, audience, tone, style, perspective and complexity.
Unknown entries have `state: unknown`; supplied entries preserve original text
and distinguish interpretation. Preferences can request checkpoints but cannot
waive explicit acceptance, conflict holds or manuscript protection. Bootstrap
metadata provides novel ID and bundle/schema versions; the project record owns
creative settings, avoiding duplicate title/preference authority.

`review_preferences.routine_checkpoint` is `on_request` (default), `session_close`
or `every_exchange`. `on_request` adds a summary checkpoint only when requested;
`session_close` also summarizes when a session closes; `every_exchange` summarizes
after every exchange. A checkpoint lists captured proposals, established decisions
and open questions in the saved response and pauses agent-initiated new exploration
until user direction. It does not delay automatic saving or require confirmation
of already accepted facts. A new explicit user direction satisfies the pause;
closing a session needs no extra acknowledgment. Mandatory conflict/ambiguity
questions apply in all modes, independent of these routine checkpoints.

## Brainstorming Session

Fields: identity, topic, `mode` (guided/open), `state` (open/closed),
`started_exchange_id`, `last_exchange_id`, `related_record_ids`,
`unresolved_question_ids` and a derived-context reference if available.
New sessions default guided; resume preserves mode. Closed sessions may reopen
on explicit user request. A mode change affects the prepared response in the
same exchange. Session membership of messages comes from the owning exchange;
there is no second authoritative transcript file.

## Idea

Fields: statement, `status` (proposed/accepted/rejected/unresolved/superseded),
`related_element_ids`, `alternative_group_id` (nullable), `selected_parts`,
`decision_ids`, `resulting_assertion_ids`.
An alternative group distinguishes mutually exclusive proposals without assuming
rejection of every unselected option. Partial acceptance selects precise parts;
remaining parts stay proposed or unresolved. Rejected/superseded ideas can be
reconsidered through a new sourced revision, never by erasing history.

## Story Element

Fields: `element_type` (character/location/event/plot_thread), display name,
aliases, `status` (proposed/accepted/rejected/unresolved/superseded),
`assertion_ids`, `relationship_ids`, `dependency_refs`.
Duplicate display names are valid. Characteristics/backstory are assertions,
not independently writable prose attributes. Events include `time_ref`;
plot threads list recorded dependencies. Arbitrary genres require no extra types.

## Relationship

Fields: `from_element_id`, `to_element_id`, meaning, assertion perspective,
`time_ref`, `status`, decision/source refs. Directionality is explicit;
reciprocal relations are not silently inferred. A proposed relationship is not
canon just because both endpoints are accepted.

## Fact or Knowledge Assertion

Fields: subject element ID, predicate (human-readable meaning), value (text,
scalar or referenced element), `perspective` (author_truth/character_knowledge/
character_belief/reader_revelation), `holder_id` (required for character
perspectives), `reader_audience` (required for reader revelations), `time_ref`,
`truth_state` (affirmed/denied/unknown), `status`, acceptance decision refs and
`supersedes` (nullable prior assertion ref).

`time_ref` distinguishes event chronology and narrative/revelation order. Each
axis has `precision` (known/partial/unknown), optional event anchor, interval
bounds and explicit before/after references. Unknown bounds are null. Absence of
a knowledge assertion never means the character lacks knowledge. Conflicting
accepted author truths require a finding/resolution or an explicitly recorded
intentional ambiguity; character beliefs may differ from author truth.

## Creative Decision and Revision

Fields: `action` (accept/reject/correct/revise/reverse/resolve/defer),
`user_message_ref`, exact accepting/revising span, `target_refs`, `selected_parts`,
`prior_refs`, `result_refs`, `reason`, `affected_refs`, `review_required_refs`.
All canon transitions require a user decision with an identifiable target.
Correction retains the erroneous version and explanation. Revision records
replacement and supersession in the same exchange; reversal identifies which
prior state is restored through a new version. Directly recorded dependencies
populate impact review; unknown dependencies are disclosed, not guessed.

## Unresolved Question

Fields: question text, related refs, alternative IDs, `state` (open/resolved),
resolution decision and sources. A resolved question can reopen via a sourced
revision; its unanswered form never creates a fact.

## Continuity Finding

Fields: `category` (motivation/chronology/knowledge/plot_dependency/world_rule/
relationship), `assessment` (conflict/uncertainty/opportunity), `severity`
(significant/advisory), `source_refs`, `affected_refs`, explanation, consequences,
resolution options, `disposition` (open/rejected_idea/revised_idea/revised_canon/
intentional/deferred/resolved), decision refs and optional narrative explanation.
Opportunities are non-blocking proposals. Open significant conflicts hold
conflicting development. Deferred conflicts remain unresolved and hold canon
promotion; an intentional explanation preserves perspective/timing distinctions.
Missing context is uncertainty, not an invented proven contradiction.

## Transition and validation invariants

- Create records only at revision 1; updates name the exact predecessor. Reject
  dangling references, duplicate revisions and cross-novel links.
- Proposed/unresolved → accepted requires a sourced, unambiguous user decision
  and no blocking continuity/direction hold. Praise/quotes/silence cannot qualify.
- Accepted → superseded with a replacement requires explicit revise/reverse
  authorization. Never leave replaced assertions simultaneously current by mistake.
- Partial selections change only selected propositions; do not accept a compound
  proposal wholesale. Current state excludes rejected and superseded assertions.
- Every canon-affecting creation or revision, including a relationship or element,
  obeys the same authorization and unavailable-context rules as an assertion.
- If relevant canon is unreadable, persist proposals and an incomplete review
  only when the ledger can safely accept them. Unknown impact scope holds all
  canon changes. Restore and revalidate before lifting the hold.
- Never write manuscript content, even when an affected-ref points to it.
- Idempotency uses exchange ID and digest, not text similarity. Identical retry
  returns the original checkpoint; different payload under the same ID conflicts.
- Validate the entire proposed transition and accessible reference scope before
  saving. Structural validity does not prove semantic accuracy or literary quality.

## Schema evolution

Each envelope declares schema version; installed bundle manifest declares readable
versions. Unsupported versions produce unavailable-context reports and mutation
holds, not best-effort data coercion. Compatible additions must preserve documented
consumer behavior. Incompatible migrations require explicit user initiation,
a pre-migration Git checkpoint, migration map, validation of IDs/references/history,
and recovery instructions. No incompatible migration is implemented in this slice;
unknown versions fail safely. Derived caches include schema/head digest and may
always be deleted and rebuilt.
