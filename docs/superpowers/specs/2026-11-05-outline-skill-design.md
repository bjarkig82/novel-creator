# Notebook outline skill

## Intent and scope

Help a writer turn brainstorming in a new-format story notebook into a proposed book outline, refine it in conversation, and save the chosen outline. Creating chapter or scene manuscript files is deferred.

## Approaches

The writer selected a conversational skill over a command plus skill. A skill can use the existing notes and native Codex tools without adding a Python runtime command. A command would add an entry point and maintenance without supplying the creative judgment needed here.

## Proposed behavior

- Offer an explicitly invoked Codex outline skill for new-format notebooks. Keep creative guidance in shared notebook resources and the host skill as a thin adapter.
- Read the project preferences, existing outline if any, and relevant topic notes. Disclose missing information; ask a focused question when it materially affects the outline.
- Suggest a structure suited to the story rather than imposing a fixed narrative framework. Parts, chapters, and scene beats may be described within the outline when useful; these are planning entries, not separate manuscript files.
- Explain the suggested progression and each section's purpose. Reuse established facts and mark new ideas, unresolved questions, and alternatives as tentative.
- Discuss revisions and save the selected outline as a topic using the current notebook metadata, stable item identities, states, and relative links. Link existing owning notes instead of duplicating their facts. Update working-summary navigation when useful.
- Preserve revisions and writer edits using existing notebook saving and local history rules. Never overwrite an existing outline blindly or treat selection of a structure as acceptance of every proposed story fact.

## Constraints and non-goals

No manuscript generation, chapter or scene file scaffolding, external publication, automatic conversion of legacy novels, or new CLI command. English and Icelandic notebook behavior must remain supported. Existing notebooks do not silently acquire new installed resources.

## Implementation decisions left to the builder

Choose the skill name and resource layout consistently with repository packaging. Include the skill in new notebook setup and distribution checks without changing legacy skill behavior. Validate installed resources and representative outline journeys, including revisions, insufficient notes, and preservation of unrelated content. Native host creative quality must not be claimed from static checks alone.

## Approval

The writer approved this design and implementation on 2026-11-05. They subsequently requested lightweight standard planning and execution without Spec Kit.
