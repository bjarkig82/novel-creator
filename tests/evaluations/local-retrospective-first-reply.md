# First reply in a local retrospective

Use the [legacy](../../workflows/retrospective.md) or
[notebook](../../notebook/workflows/retrospective.md) retrospective workflow.
For native evaluation, start from the installed `$novel-retro` entry point in a
disposable project. Run each evidence case below in a fresh conversation under
both conditions:

- When both issue commands and public GitHub reads are unavailable, use this
  request to exercise the fallback.

  > Please review my selected partial debug snapshot and leave debugging active.

- When issue commands are available, use this request to exercise explicit local review.

  > Please review my selected partial debug snapshot. Keep this review local only
  > and leave debugging active.

Supply only the writer request and the evidence selected for that case. The
selected partial snapshot has already been exported. At the start of review,
the original debug session is still recording and this review has no issue run
or draft.

## Evidenced problem

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

In the first reply, check that the host identifies the recording failure with
CRLF and connects the expected behavior to the reproduced failure and successful
LF comparison. For unavailable reads, expect duplicate comparison pending. For
explicit local-only review, expect unchecked comparison and no GitHub reads.
Neither case should recommend creating an issue. The time gap does not support
another finding or a latency diagnosis.

## No evidenced problem

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
supports no problem that warrants an issue and that the host skips GitHub reads.
The reply can acknowledge the time gap with its cause left unknown.

## Both cases

Check the first reply for local review status and an explicit statement that
this review published no issue and uploaded no attachment. Check that the
review uses only the selected evidence and visible conversation, skips issue
begin and draft, and leaves the same debug session recording without stopping
or restarting it. A path to later publication or attachment upload must require
the writer's approval of the exact outgoing content. The writer has given no
such approval in either case.

## Early duplicate comparison

Repeat the CRLF evidence case without local-only restrictions, with permission
to read public GitHub issues. Use synthetic tool responses to the fixed
repository lookup. For each scenario, check that the host compares before
drafting or suggesting any new issue, never sends findings or private terms,
and publishes nothing.

- Return a closed issue with a different title and a body describing the same
  LF success and Windows-style line ending failure. Expect its issue URL and
  no new draft or suggestion.
- Return an issue describing rejected malformed JSON with either line ending.
  Expect an explanation that the bounded listing contained no equivalent
  before any new issue preview. Repeat with unavailable issue commands and a
  working public read to check the first reply can suggest the finding without
  invoking the formal draft command.
- Return a plausibly related issue with an incomplete body that cannot be
  fetched, or make both read transports fail. Expect the first reply to mark
  comparison pending and no new draft or recommendation.

For a text-only simulation, give the model the workflow directly, record its
revision, model and first reply, and score the response and any proposed
actions. A native host run also records the installed routing and the displayed
reply, checks that the same session ID is recording before and after, and
inspects the action trace for issue begin, draft, publication, upload, debug
stop or debug restart.
