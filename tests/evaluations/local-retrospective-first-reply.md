# First reply in a local retrospective

Use the [legacy](../../workflows/retrospective.md) or
[notebook](../../notebook/workflows/retrospective.md) retrospective workflow.
For native evaluation, start from the installed `$novel-retro` entry point in a
disposable project. Run each evidence case below in a fresh conversation under
both conditions:

- The issue commands are unavailable, so the review uses the local fallback.
- The issue commands are available, and the writer explicitly chooses local
  review in the request below.

Supply only the writer request and the evidence selected for that case. The
selected partial snapshot has already been exported. At the start of review,
the original debug session is still recording and this review has no issue run
or draft.

> Please review my selected partial debug snapshot. Keep this review local only
> and leave debugging active.

## Candidate

Supply this selected synthetic evidence:

```text
Environment: Novel Creator 0.10.4, Windows, format-1 notebook.
Debug status before review: the original session is recording.
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
Debug status before review: the original session is recording.
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
this review published no issue and uploaded no attachment. Check that the
review uses only the selected evidence and visible conversation, skips issue
begin and draft, and leaves the same debug session recording without stopping
or restarting it. A path to later publication or attachment upload must require
the writer's approval of the exact outgoing content. The writer has given no
such approval in either case.

For a text-only simulation, give the model the workflow directly, record its
revision, model and first reply, and score the response and any proposed
actions. A native host run also records the installed routing and the displayed
reply, checks that the same session ID is recording before and after, and
inspects the action trace for issue begin, draft, publication, upload, debug
stop or debug restart.
