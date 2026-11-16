# Session usability feedback: source resolution evidence

Reviewed 2026-11-16 against source commit `6862de0`, including implementation
`4bc0110`. All five concerns in GitHub issue #8 have source-level provisions.
This records their scope; it does not claim a reproduced or qualified native
writing session. These improvements remain unpublished and are absent from the
public 0.10.2 package.

| Concern | Owning implementation and evidence | Remaining limit |
| --- | --- | --- |
| Repeated requests for suggestions | [Notebook conversation](../notebook/workflows/conversation.md), [notebook brainstorming](../notebook/workflows/brainstorming.md) and [legacy brainstorming](../workflows/brainstorm.md) require provisional current-session adaptation, one useful question/invitation, immediate respect for fewer/no options and independent writer acceptance. | Conversational usefulness and subsequent host turns have not been observed. |
| Reliable optional debug capture | Both [notebook](../notebook/workflows/debugging.md) and [legacy](../workflows/debugging.md) guides provide the same UTF-8 file-based Python recipe and PowerShell invocation. CLI record help exposes operation/path rules and result checks. [Recipe integration tests](../tests/integration/test_debug_recipe.py) exercise Unicode, punctuation, multiline text, rejected operations/paths and failed-before/gap/later-context evidence. | The recorder cannot recover earlier bytes or enforce a host's truthful phase label. The host must check success before editing, disclose gaps and never relabel a later snapshot as the missing before image. Debugging remains local and opt-in. |
| Stale derived navigation | [Conversation save rules](../notebook/workflows/conversation.md) require refreshing every affected existing derived value from current owning items, excluding revisions and preserving unrelated rows/staging. [Grouped fixture tests](../tests/unit/test_notebook_grouped.py) check four-to-five accepted statements with one proposal and detect stale/history-inflated counts. | These are authored before/after snapshots and assertions, not execution of an automatic host save or proof that staging was preserved during one. |
| Readable accumulated notes | [Format guidance](../notebook/workflows/format.md) separates current material, possibilities, questions and revisions while retaining independent IDs, states, perspectives, origins, links and recoverable history. Grouped fixture tests check those properties and unchanged unrelated items. | Readability is a qualitative host evaluation. Organization does not authorize saving a chat-only profile draft or selecting alternatives. |
| Small-turn orchestration | Conversation guidance reuses valid loaded context, batches independent reads/compatible writes and avoids unnecessary delegation for small work, while retaining role ownership, fresh checks before writes and meaningful-turn persistence. The shared debug recipe avoids repeated ad hoc payload construction. | No latency claim or benchmark is supported. Native specialist selection and actual tool-call behavior remain unverified. |

The [readable-notebook evaluation scenarios](../tests/evaluations/readable-notebooks.md)
remain explicitly unexecuted. They include repeated-option adaptation, stale
navigation repair, preservation of staging and profile save boundaries. No real
novel was changed for this review.

For intentional source use, follow [project upgrade guidance](upgrading-projects.md)
and the [bounded notebook procedure](session-guidance-upgrade.md). New notebooks
and legacy novels receive source guidance at setup. Existing notebooks require
explicit preview/application and host rereading/reloading. Existing legacy
novels have no supported same-version source refresh; do not bypass that limit
or imply a package upgrade updates their pinned guidance. Filesystem checks do
not establish native skill discovery, voice behavior or writing quality. A future
release still requires its own authorization and complete release qualification.
