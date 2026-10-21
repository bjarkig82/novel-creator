# Initialize a novel

Accept an existing concept, a vague idea, or no concept. Offer a working title,
concept, genre/subgenres, audience, manuscript language, tone, style, perspective,
complexity, workflow preferences and human review preferences. Ask normally one
focused question at a time. Accept bundled answers without asking again. Every
answer may be skipped or left unknown; do not make a checklist mandatory for the
writer. A temporary title is fine. English is the language default; Icelandic
text and names must remain unchanged. Do not translate the original concept.

Prepare a UTF-8 brief JSON object. A minimal brief is `{}`. Supported keys are
title, original_concept, manuscript_language, creative_brief,
workflow_preferences, review_preferences and creative_directions. Title/concept
and creative or workflow values may be strings, null, or explicit preferences:
`{"state":"unknown"}` or
`{"state":"supplied","original_text":"exact answer","interpretation":null}`.
Creative brief keys are genre, subgenres, audience, tone, style, perspective,
complexity. Keep any interpretation separate from the supplied original text.
Workflow preferences are named preferences, such as suggestion frequency.
Review preferences contain routine_checkpoint: on_request (default),
session_close or every_exchange. These never waive saving, conflict holds,
user authority or manuscript protection. Creative directions are exact text
entries, never inferred canon. Unknown answers cannot contain invented text.

Use `init --path PATH --brief-file FILE --json` on an explicit independent target
outside the framework and other repositories. Require Python >=3.11,
jsonschema >=4.23,<5, jsonschema-rs >=0.59,<0.60, Git >=2.39 and a user-configured Git identity. Do not invent
an identity, overwrite unrelated content or change global configuration. On
partial initialization, preserve all local evidence and retry with the unchanged
brief. Stop if payload/files have changed; disclose the last confirmed checkpoint.

Existing recognized novels continue with their original identity. Do not recreate
them or apply a replacement brief implicitly. Read their current project first.
Title and later settings changes are full project revisions in a conversation
exchange, sourced to the current user message; original_concept remains the
immutable original input. Use records.revise_project to preserve unchanged fields.

The bootstrap artifact preserves the original supplied JSON and its digest,
with JSON Pointer provenance. It does not fabricate conversational messages or
authorize canon. Only clear user decisions can establish story facts later.
After confirmed initialization, offer optional guided brainstorming. Setup can
finish without starting brainstorming. Disclose any unfinished capability.

All conversational replies and subsequent changes follow save-before-display:
preserve the exact native user message, prepare one exact reply, save both and
all typed revisions in a single exchange, wait for success, then display the
saved reply unchanged. On failure disclose unsaved work and pause authority.
