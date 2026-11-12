# Character development: scenarios and evidence

November 12, 2026. Unpublished source work for format-1 notebooks, absent from
published 0.6.0. This ledger distinguishes resource delivery from agent behavior,
native host discovery and literary quality. No real novel is an evaluation target.
See the [usage/manual-install guide](../../docs/character-development.md) and
[behavioral workflow](../../notebook/workflows/character-development.md).

## Conversation rubric

Use disposable English and Icelandic notebooks with accepted character facts,
proposals, linked facts, open questions and writer history. Capture actual turns,
complete owning notes, file hashes, Git status and index before/after each turn.
Read the whole response and resulting items; phrase matching alone cannot judge
acceptance, useful prose, continuity or instruction following. Mark each scenario
with its host/runtime, observed result and limitations when actually run.

| Scenario and writer turns | Expected observations |
| --- | --- |
| `$novel-character-develop` with a named character and relationship focus; separately “Fill the gaps in Elin's profile.” | Both routes select this mode. Read current project directions, configured language, owners and relevant unresolved findings. Focused request stays focused; no-focus request chooses useful gaps and explains why. |
| First response with sufficient context | Summary at most about 100 words; 2–3 connected numbered additions of actual profile prose, roughly 200–400 words total or less when appropriate, with contribution explanations separate. No required summary approval, generic questionnaire or automatic second batch. |
| “Help me explore a character,” or `$novel-character`; “No suggestions yet, just questions.” | Ordinary guided brainstorming baseline remains available. A character topic alone does not trigger profile additions; no-suggestion preference is honored. |
| “I like this”; “Maybe”; “Choose 2”; “Make 2 gentler.” | No notebook writes, summary updates, handoff/draft artifacts or checkpoints. Revisions retain addition numbers and make the current replacement clear; choosing/praise alone is not save approval. |
| Revise 2, then “Save addition 2”; separately “Save only its first paragraph as proposed.” | Save only current selected prose with correct accepted/proposed status, not contribution explanations or earlier wording. No second approval for clear instructions; clarify only genuinely unclear modify-and-save requests. Unselected material stays chat-only. |
| “Discard this”; “Cancel”; then change topic | No draft material leaks into automatic notes or later checkpoints. Cancellation ends this mode. No promised recovery in another chat. |
| Save selected additions, request another batch, then repeat development | Read accepted current notes; deepen remaining gaps without duplicating accepted content. One new requested batch, then wait. Stable IDs for changed items; new items have appropriate identities and provenance. |
| “Change her established birthplace and save it”; separately an unrequested addition contradicts that birthplace | Explicit revision can change the fact with ownership/history preserved. Unrequested contradiction is surfaced and needs direction; no silent canon rewrite or manuscript edit. |
| Missing owner despite summary link, two characters sharing a name, or unreadable project directions | Disclose unavailable context; ambiguity gets one focused question. Missing/omitted context is not evidence of absence. No invented prior conversation or legacy conversion. |
| Character lies to her brother; reader learns truth later; linked fact lives in another topic | Keep objective truth, character knowledge/belief and reader revelation distinct. Reference the existing owner without duplicating or rewriting it without authority. Preserve open questions. |
| Writer changes/stages owning notes after drafting, before approval | Reload current files and Git state. Preserve unrelated edits/index entries; clarify affected conflicts instead of overwriting the writer or silently changing the approved draft. |
| Approved save suffers write denial, partial multi-file write or checkpoint failure | Report what actually persisted and what remains pending separately. Inspect before retrying; no false success, duplicate additions, automatic push or loss of staged writer edits. |
| English and Icelandic; explicit alternate conversation/output language | Saved prose/headings use project language with stable format fields/IDs. Honor explicit output requests without changing configured language. A human assesses idiom and literary usefulness separately. |

These are required checks, not recorded passes. Native conversations for the
full rubric and human literary assessment remain unrun.

## Automated delivery and manual-install evidence

The focused `tests.integration.test_character_development_install` module executes
the actual Python snippet from the guide using installed package resource bytes.
Its disposable older-format notebooks retain custom `AGENTS.md` instructions,
story notes, a navigation edit, and both staged and unstaged writer changes.
Five tests passed: English/Icelandic installation with backtick/tilde metadata
fences plus identical retry, divergent
workflow/skill/root-section refusal before writes, and missing shared guidance,
configured-language resource or unsupported format refusal, plus CRLF root-section
divergence refusal and identical CRLF reinstallation without changing original
bytes. Both CRLF regressions failed against the previous snippet before its
section-detection text was normalized, then passed after the fix. Assertions compare
all non-Git file bytes, exact resource bytes, the complete Git index entries and
HEAD for successful installation; divergence also preserves the index. Only two
new resources and the appended root section change on success.

The coordinator separately reported six focused package/CLI tests passing,
including wheel and source-distribution inventories of 28 resources and isolated
English/Icelandic notebook initialization. It also reported 28 focused Task 1
initializer/verifier tests passing. Those are structural resource-delivery checks,
not evidence of conversation quality or native skill discovery. This task does
not rerun full release qualification or the full suite.

## Controlled agent-runtime exercise

The coordinator ran a three-turn exercise in a disposable English notebook,
supplying the installed guidance explicitly to an available collaboration agent
runtime. A natural request to fill gaps in Alex the lighthouse keeper's profile
produced a 51-word summary and three connected focused additions (233 words of
proposed prose by simple whitespace counting), with contribution explanations
and clear unsaved status. Praise plus a request to quieten addition 2 returned
only the revised #2, clearly replacing its earlier wording. After each of those
turns all 36 non-Git file hashes and the complete Git index remained unchanged.

“Save only revised addition 2” then changed only `notebook/topics/keeper.md`,
adding accepted `keeper#shared-habit` with the exact revised prose and approval
Origin. Prior content remained intact, the earlier hope stayed proposed and
`letters#sender` stayed open. Additions 1/3 were absent; the summary and index
were unchanged. The format fixture checker passed for five notebook documents.
The actor disclosed a pending checkpoint under its delegate no-commit rule.
The session's transcript and snapshots are under
`/tmp/character-development-work/`; they are disposable evidence, not shipped
artifacts. This is limited explicit-load agent-runtime evidence for these three
turns, not native Codex CLI/Desktop discovery, direct writer UI interaction,
the full rubric, general failure recovery or independent literary assessment.

## Native host feasibility and remaining limits

On November 12 a real native feasibility probe was attempted in the managed
Linux environment with inherited configuration and permissions:

```text
codex exec --ephemeral --skip-git-repo-check --cd /tmp/character-development-work --json 'Reply HOST_READY only. Do not call tools or modify files.'
```

It exited 1 before model invocation. After a PATH alias startup warning, stderr
reported `failed to initialize in-process app-server client: Read-only file system
(os error 30)`. No `HOST_READY` response or feature conversation ran through that
CLI. No authentication files were read, provider/global configuration changed,
user-owned chat accessed or real novel touched. Raw disposable logs are in
`/tmp/character-development-work/host-probe.stdout` and `host-probe.stderr` for
this session; they are not shipped artifacts.

Native CLI and target Windows/Linux Desktop discovery, guidance reload,
conversation persistence, all unrun rubric scenarios and human literary quality
remain unverified. Package installation and a controlled explicit-load harness
cannot establish those outcomes or English/Icelandic literary parity.
