# Explicit delegated input support

The user selected this route on 2026-10-23 and retained all native-input and
genuine-novice requirements. Implementation choices below are engineering calls.

Use the existing installed Python launcher, not a new model runtime. Add
`input capture` with explicit source, snapshot file, current thread and turn IDs.
Native input remains one complete text userMessage. Delegated evaluation input
is one complete codex_app create_thread/send_message_to_thread output using the
observed codex_delegation wrapper, with an explicitly expected source thread.
Require `--evaluation-only` for delegation. Reject missing, ambiguous, stale,
truncated, malformed or unexpected source events. Never silently change modes.

Return exact text and a normal input_artifact carrying source labels, selected
public event, thread/turn/item IDs and an integrity digest. Include that artifact
in each saved exchange so fresh interactions retain provenance. Local raw
capture belongs under local/evidence. Host IDs and labels are evidence only,
never story identity, human participation or independent proof of approval.
Scenario decisions in a disposable evaluation are simulated director inputs;
they cannot authorize changes in real novels. No schema/authority relaxation.

Alternatives considered: implicit fallback would hide provenance and is rejected;
documentation-only extraction would lack deterministic boundary validation;
an explicit parser plus existing input_artifacts retains portability and makes
the selected route reviewable without changing JSON schema fields. The existing
bootstrap-only semantic rule needs a narrow host-input exception: exactly one
artifact, rebuilt from its selected public event and matching the current user
message. Conversation provenance is never registered as a bootstrap creative
source in full or certified validation. Older bundles retain their old behavior;
no installed novel is silently upgraded.

Implementation sequence:
1. Add failing native/delegated parser and command tests, including exact Unicode,
   CRLF, trailing whitespace, current-turn selection, truncation and malformed data.
2. Implement installed capture command and provenance artifact; test committed
   artifact retention and installed resource independence.
3. Update adapter/workflow instructions, retain native/novice gates and old evidence.
4. Verify focused Windows/Linux checks, final wheel and appropriate regressions.
5. Resume the two authorized disposable host tasks with an observed delegated gate;
   independently compare input, committed response and native displayed response.
   Continue scenarios and fresh resumption only after this gate passes. Keep
   delegated results separate from native-host and human release criteria.
