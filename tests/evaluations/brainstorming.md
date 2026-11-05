# Stage-aware brainstorming: scenarios and evidence

November 5, 2026. New format-1 notebook resources in the unpublished candidate.
These scenarios are a manual/application evaluation rubric, not a claim that
native Desktop conversations or literary quality have passed.

## Baseline

The writer reported trying an empty book and receiving a request to choose a
character/topic before there was a genre or book concept. Existing shared
conversation guidance said guided brainstorming was the default but supplied no
empty-book routing or concrete discovery method. Language examples began with
an already-existing keeper and letters. This user report is the behavioral
baseline; no fabricated baseline transcripts or rationalizations are supplied.

Before resource implementation, the new initialization test failed in both en/is
because the shared brainstorming workflow was absent. The installed wheel and
source-distribution test failed because the book-idea skill was absent. An
initial invocation with system Python could not import the editable package;
validation used the existing project virtual environment thereafter.

## Manual conversation checks (not yet run in a native host)

Use disposable newly initialized notebooks, preserving actual outputs and notes
when running. Check language, next-question fit and saved states by reading the
whole exchange; word matching alone does not establish success.

| Context and writer turns | Expected behavior to inspect |
| --- | --- |
| Empty en notebook: “I want to write a novel but have no idea.” Then “I like quiet, eerie places.” | One broad invitation, then a question about that interest; no mandatory genre, character or topic menu. No inferred accepted premise. |
| Empty is notebook: “Mig langar að skrifa bók en veit ekki um hvað.” Then “Einmanaleiki og hafið heilla mig.” | Icelandic discovery question followed by that answer's mood/theme; no keeper/letters material imported from examples. |
| No method request; fragments “a lighthouse, broken clocks, an old friendship.” Then “I'm stuck.” | Automatically choose associations/clustering or another suitable technique, adapting to the later stuck response with an optional contrast/freewriting invitation. No compulsory method menu. |
| Only a working title or genre: “Help me brainstorm.” | Treat context as sparse; use what is known without repeating it or requiring a checklist. |
| Empty notebook: “Let's try mind mapping.” Then “I don't know the topic yet.” | Retain mind mapping; invite a word/image/feeling or offer optional seeds, then branch from the chosen seed. Do not demand premise or silently switch methods. |
| Empty notebook: “I want to develop a character first.” | Start with a person who interests the writer; no prior book-idea requirement. Explicit skill invocation has the same focus priority. |
| Existing premise and accepted preferences: “What could happen after she refuses?” | Explore plot what-if/cause/consequence without repeating genre/preferences or automatically invoking outline. |
| Character: “She wants independence but can't leave her brother.” | Explore a motivation/contradiction/relationship with one focused next question, not a full biography questionnaire. |
| Setting: “An island is cut off each winter.” | Explore associations, constraints and lived effects; examples remain proposed rather than established world rules. |
| “Maybe that works.” Then “Let's talk about the harbour instead.” | Preserve tentative proposal and open question; change focus without inferring acceptance or resolving the old question. |
| “No suggestions for now, just questions.” Later “Actually, give me a few possibilities.” | Adapt naturally; explicit choices persist only while relevant. Do not restart onboarding. |
| “Use Snowflake to develop this seed.” | Optional sentence-to-paragraph expansion; no imposed act structure, ending or manuscript. Empty-book default never demands Snowflake. |
| Missing/unreadable topic note with an established summary link | Disclose missing context instead of treating the book as empty or inventing saved facts. |
| Explicit `$novel-outline` after exploration | Use existing outline workflow, preserving proposed details and open questions. Ordinary brainstorming does not invoke it automatically. |

## Automated evidence and limits

Installation tests exercise real filesystem/Git initialization in both languages,
resource tracking and relative links. Distribution tests install built wheel and
source archives offline outside the checkout. Legacy initialization/export checks
exclude notebook-only skills and workflows. These verify delivery boundaries,
not whether the model asks a compelling question or interprets acceptance well.

Native Codex skill discovery, Windows/Linux Desktop conversation behavior,
manual scenario outcomes and human assessment of usefulness remain unverified.
No internet, model-provider key or external service was added to notebook runtime.

The focused initializer, legacy-boundary and built wheel/source-distribution run
passed: 17 tests. The second run included package-verifier contracts and passed all 22 tests. The
rebuilt wheel verifier passed source-byte inventory, isolated installed module
origins, English/Icelandic notebook resource/link checks, and existing legacy
and update journeys. This is structural application evidence, not a conversation
or native skill-discovery result. Documentation relative links and diff whitespace
checks passed. The complete `.venv/bin/python -m unittest discover -q` run passed: 404 tests
in 456.637 seconds, three skips, no failures.

Independent requirement review identified that focus selection was automatic but
method selection needed an explicit default. Guidance now selects and adapts
techniques from context and replies, while retaining explicit method choices.
Re-review and independent overall review reported no remaining actionable
findings. Read-only simulated opening, method-first and character-first reasoning
checks were consistent with the contract; they did not execute native host turns
or exercise note persistence and are not reported as manual host passes.
