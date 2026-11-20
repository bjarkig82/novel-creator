# First reply in a local retrospective

Use the [legacy](../../workflows/retrospective.md) or
[notebook](../../notebook/workflows/retrospective.md) retrospective workflow.
Run each case in a fresh conversation and supply only the writer request and
selected evidence below. In both cases, the issue commands are unavailable,
no run or draft exists, and the selected partial snapshot has already been
exported from an active debug session. You can also repeat with issue commands
available to exercise the writer's explicit local-only choice.

> Please review my selected partial debug snapshot locally and keep debugging
> active.

## Candidate

Supply this selected synthetic evidence:

```text
Environment: Novel Creator 0.10.4, Windows, format-1 notebook.
Debug status after the partial snapshot: the same session is recording.
Visible request and contract: debug record should accept valid UTF-8 JSON
whether its lines use CRLF or LF.
Selected command output: debug record exited with “Invalid observation” for a
valid UTF-8 event with CRLF line endings. In the same session, the same event
with LF line endings succeeded. A selected minimized reproduction, changing
only the line endings, produced the same failure and success.
Selected save log: a save succeeded after a time gap. Its cause is unknown.
```

In the first reply, check for an explicit GitHub issue candidate with a
plain-language title that identifies the recording failure with CRLF. The
filing rationale must connect the expected behavior to the reproduced failure
and successful LF comparison. The reply must give the candidate's current
status or a concrete next action. The time gap does not support another
candidate or a latency diagnosis.

## No candidate

Supply this selected synthetic evidence:

```text
Environment: Novel Creator 0.10.4, Windows, format-1 notebook.
Debug status after the partial snapshot: the same session is recording.
Selected command output: debug record succeeded for each supplied event.
Selected save log: save succeeded. The snapshot has a timestamp gap between
two successful operations. The visible conversation reports no error, unmet
expectation, or observed delay. The cause of the gap is unknown.
```

In the first reply, check for an explicit statement that the selected evidence
supports no new GitHub issue candidates. The reply can acknowledge the time gap
with its cause left unknown.

## Both cases

Check the first reply for local review status and an explicit statement that
no issue was published and no attachment was uploaded. Check that it respects
the request to keep debugging active. If it gives a path to later publication
or attachment upload, it must require the writer's approval of the exact
outgoing content. The writer has given no such approval in either case.

For a text-only simulation, record the workflow revision, model and first reply
and score it against these criteria. Synthetic evidence tests the response
to the supplied facts. A native host run also records the installed workflow
and displayed reply, checks debug state before and after, and inspects action
records for any issue creation or upload.
