# Character development

Use this workflow in a format-1 story notebook for `$novel-character-develop` or
an ordinary request to fill gaps, enrich or deepen a character profile, optionally
with a focus such as relationships or motivation. Ordinary question-led character
exploration remains under [brainstorming](brainstorming.md); a character topic or
`$novel-character` alone does not select this mode. Follow [conversation](conversation.md),
[format](format.md) and [role guidance](agents.md), with the save boundary
below taking precedence over their automatic persistence rules in this mode.
If the workflow or supported notebook context is unavailable, explain the
limitation and preserve files; do not convert a legacy novel.

## Read before proposing

Read `notebook/project.md`, its explicit directions and configured English or
Icelandic language resource. Use `notebook/working-summary.md` only to find the
relevant owning character notes, stable topic/item identities and linked facts.
Read those owners and relevant unresolved findings before developing the profile.
Separate accepted facts, proposals and unresolved questions. Missing, unreadable
or omitted context is unavailable, never evidence that a detail does not exist.
Disclose material limits without inventing past discussions. Ask one focused
question only when character identity is ambiguous or necessary context is
missing; otherwise proceed with the substantive draft.

Preserve accepted facts and explicit creative directions. Add missing details or
deepen existing ones without replacing accepted facts unless the writer
explicitly requests their revision. Surface significant contradictions with the
established information and its consequences; obtain direction before applying
a conflicting canon change. Unrelated exploration may continue. Distinguish
objective story facts, what the character believes or knows, and what the reader
knows, including timing, lies and intentional ambiguity.

## Offer one connected batch

Begin with a compact summary of the character's relevant current profile, at
most about 100 words, keeping accepted facts, proposals and unknowns distinct.
Then offer 2–3 connected additions totaling roughly 200–400 words of actual
proposed profile prose. Use less when context is sparse; never pad. Honor requests
for a smaller batch or shorter text immediately. If a focus was supplied, stay
within it. Otherwise choose useful gaps from the available profile and briefly
explain why those details would help.

Number each addition consistently. For each, give the actual proposed text the
writer could put in the profile, followed by a brief explanation of its
contribution. Keep that explanation separate from the profile prose. Suggestions
about what could be written are not a substitute for the actual text. Make the
additions work together without assuming that any will be accepted. There is no
separate approval gate for the summary before offering the prose.

Keep the entire draft, discussion and every revision in the active conversation
until the applicable save boundary is met. Ordinarily, state that the proposals
remain unsaved until the writer clearly approves saving them. For an explicitly
delegated save, follow the instructions below after preparing the batch. After
this one batch, stop. Another batch requires a request.

## Revise and select in chat

Support modifying, selectively saving, discarding or cancelling the batch. Keep
addition numbers stable across revisions and partial saves; never reuse a number
for a different suggestion in this batch. Show only changed additions when
appropriate, identifying them by number and explicitly indicating that the new
text replaces that addition's earlier version. Keep the current wording of every
addition unambiguous when unchanged additions are omitted.

Praise, tentative acceptance, discussion, choosing an addition or requesting a
modification alone is not save authority. “Save the current draft” or “Save
addition 2” clearly approves the indicated current text; do not ask again. If the
writer asks to modify and save together, save the resulting text only when both
the requested change and content to save are clear. Ask one focused clarification
if that resulting content or selection is unclear, keeping it in chat meanwhile.
Discarded or cancelled suggestions remain unsaved. Cancellation ends this mode;
unselected draft material never becomes an automatic note when the topic changes.

## Explicit delegation for existing profiles

The writer may expressly authorize a specific assigned specialist to select and
save proposed additions to an existing profile before seeing the draft. The
writer's instruction must make clear who has the final decision to save, which
existing profile and scope of additions are assigned, and that the additions
are to be saved as proposals. A clear instruction to each assigned specialist
to draft, review, approve and save their own proposed additions qualifies. A
request to delegate drafting or review, a role selection, a coordinator's
assignment or general encouragement to proceed does not grant this authority.

The coordinator resolves any ambiguity about the authority, saver, profile or
scope with the writer before dispatching write-enabled work. Resolve the named
profile to its existing owning file before granting write ownership. Pass its
exact project-relative path and stable identity, the scope and proposal-only
status, any protected content, and the writer's express instruction in the
conversational handoff. The designated
saver owns only that output. Give parallel specialists disjoint paths. If the
designated specialist cannot save, report the limitation and obtain the writer's
direction before passing the save to someone else.

After reviewing the draft for fit with current facts and the assigned scope, the
authorized specialist can save the additions they select without a second
writer approval. Store only selected profile prose as items with `State: proposed`
and concise Origin reflecting the delegated instruction. Preserve accepted
facts, other items, history and open questions. Canon promotion, revision of
existing facts, other files, working summaries and Git checkpoints require their
own authority under the applicable rules. No delegated specialist commits.
Report the verified owning-file write and the exact text saved to the coordinator,
together with any conflicts or remaining unsaved text.

- “Have the specialist draft and review additions for Elin.” Return the numbered
  batch in chat for the writer's exact save selection.
- “Assign Elin to one specialist and Ari to another. Each can draft, review,
  approve and save additions to their assigned existing profile as proposals.”
  Resolve each owner and hand off only its path. Each specialist saves their own
  reviewed selection as proposed.
- “Have the specialists handle Elin and Ari and do what makes sense.” Clarify
  with the writer before dispatching any write-enabled handoff.

## Chat-only boundary and authorized saving

Without explicit delegation, make no notebook file writes for this mode until
the writer clearly approves saving the current draft or specific current
additions. In delegated work, the only exception is the bounded proposal write
described above after the designated specialist has reviewed and selected the
additions. This boundary overrides automatic notes, meaningful-turn saves,
summaries, handoff or draft files and Git checkpoints in all roles and languages. Do not save proposals elsewhere as
a workaround. Read-only context and Git inspection are allowed. Do not promise
cross-chat or interruption recovery for chat-only drafts. Other workflows retain
their normal save rules outside this mode; leaving it does not authorize saving
its unsaved draft.

Before either authorized save, read current owning files and Git state, reconcile
writer edits since the draft was prepared and preserve unrelated content. If new
facts or edits conflict with the approved text, surface the conflict and clarify
the affected change rather than overwrite the writer or silently alter the
approved draft. Save only the approved current profile prose to its appropriate
owner. Leave the contribution explanations in chat.
A writer's clear approval of the exact text accepts the selected profile
propositions unless the writer explicitly asks to save them as proposed.
Delegated approval authorizes saving the selected items as proposals only.
Split propositions as needed when only part of an addition is approved.
Unselected suggestions stay chat-only.

Approval, a saved file and committed history are separate states. Keep the
approved current draft available in chat until its actual write to the owning
file is verified. If writing is interrupted, denied or only partly succeeds,
identify the approved text that remains unsaved; do not claim it is persisted or
move it into a handoff/draft file to compensate. Verify current files before a
retry and save only the still-authorized selection. A verified file save with a
failed Git checkpoint is saved with history pending, not an unsaved draft.
In voice continuations or specialist handoffs, retain these exact distinctions
and the chat-only boundary; approval does not establish speech delivery or
cross-chat draft recovery.

Preserve format metadata and field labels, stable topic identity, ownership,
provenance, history and unresolved questions unless actually resolved. A changed
existing item retains its Item-ID; new facts receive their own items as
appropriate. Record concise approval/revision context in Origin and preserve
superseded accepted values under the format/history rules. Check linked facts
without duplicating their owners. Saving a character addition does not authorize
manuscript edits or rewrites of other characters; clarify separately if a linked
canon change needs that authority. For a writer-approved exact-text save,
update derived navigation only as needed, excluding unsaved draft material.

Follow the shared scoped save/checkpoint rules after approved writes, including
delegate ownership, preservation of staged writer edits and no automatic push.
Report file-save failures, incomplete writes and pending Git checkpoints
separately. Do not claim persistence or canon changes that failed. Do not ask
again for an already unambiguous save unless a new unresolved conflict needs
direction.

Use the project language for saved profile prose and headings, retaining stable
format fields and identifiers. Honor an explicit conversation or assigned-output
language request under the existing language rules without silently changing the
project language.
