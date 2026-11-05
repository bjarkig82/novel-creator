# Testing and completing a change

Choose validation that tests the behavior affected by your change. Keep a short
plan for larger work, implement a usable slice, check it and review the diff.
No feature-template or task-generation workflow is required. See
[development setup](development.md) and [current functionality](functionality.md).

## Automated checks

For normal work, select the smallest meaningful affected test modules or cases
and their direct dependencies. For example, a notebook contract change can use
this focused check from the configured environment at the repository root:

```bash
python -m unittest tests.unit.test_notebook_contract -q
```

Expand focused checks when failures or affected behavior warrant it, without
automatically escalating to the full suite. Follow the authoritative
[focused testing policy](../AGENTS.md#focused-testing-policy) for implementation,
review, commit and push work. Use disposable projects
outside the framework and other Git repositories. Preserve unrelated work and
never reset a real novel to manufacture a passing test. Add regression coverage
for meaningful behavior changes. Documentation changes usually need reference,
link and diff checks rather than new code tests.

For resource-inclusion changes, perform targeted artifact-content and isolated
install/package checks for affected resources in both wheel and source
distribution. The complete rebuilt-wheel verifier also covers broad legacy and
update journeys; it is not required for every routine packaging edit.

### Release-only full validation

Run the full suite and any required full coverage checks when preparing a new
package release before publication, or when the user explicitly requests them:

```bash
python -m unittest discover -q
```

Also run the complete wheel verifier as described in
[development](development.md#packaging). Preserve the candidate install,
source-distribution, cross-platform and other gates in the
[release workflow](../.github/workflows/package-release.yml). Routine focused
checks do not replace these release gates. Publication is a separate, explicitly
authorized operation.

## Behavior to preserve

- Setup: independent repositories, English/Icelandic text, unknown preferences,
  safe destinations, preserved inputs and actionable partial-failure guidance.
- Legacy storage: exact saved exchanges, source-backed typed records, stable
  identities, save-before-display, idempotent retry and explicit safe recovery.
- Authority: identifiable clear acceptance only, precise partial selection,
  retained revision history and no manuscript edits.
- Continuity: sourced significant-conflict holds, distinct author/character/reader
  knowledge, intentional ambiguity and honest incomplete-context reporting.
- Notebook: meaningful notes, stable topic/item references, targeted edits,
  derived summaries, requested briefs, preserved history and unrelated staging.
- Updates: read-only preview, reviewed release/checkpoint binding, verified
  framework ownership, content preservation and exact-operation recovery.
- Retrospectives: default off, valid opt-in, privacy, focused validated drafts,
  no duplicates, revocation and notices included in saved replies.

Use the linked workflows in [functionality](functionality.md) for detailed rules.
A change need not rerun every historical scenario when it cannot affect them.

## Legacy inspection and recovery

For an initialized legacy novel, replace the example path and use its configured
Python environment:

```text
python /path/to/novel/.novel-creator/run.py context --novel /path/to/novel --json
python /path/to/novel/.novel-creator/run.py session list --novel /path/to/novel --json
python /path/to/novel/.novel-creator/run.py inspect --novel /path/to/novel --kind assertion --json
python /path/to/novel/.novel-creator/run.py validate --novel /path/to/novel --json
python /path/to/novel/.novel-creator/run.py recover --novel /path/to/novel --exchange EXCHANGE_UUID --json
```

Quote paths containing spaces using your shell's syntax. Inspect the receipt and
confirmed checkpoint before an explicit unchanged retry:

```text
python /path/to/novel/.novel-creator/run.py recover --novel /path/to/novel --exchange EXCHANGE_UUID --retry --expected-head CONFIRMED_HEAD --json
```

For an unpublished first bootstrap, the expected head is `unborn`. Inspection
alone does not write. A changed payload, managed file, staged entry or checkpoint
can block recovery. Keep the original payload and evidence; never steal locks,
delete receipts or rewrite history to clear a failure. A published save with
cleanup pending is already saved and must not be replayed.

These commands belong to legacy projects. Native notebooks use ordinary file and
Git tools, disclose unsaved files versus pending checkpoints and preserve old
accepted content in history or a historical Revisions section.

## Actual host verification

Automated CLI, fixture and schema checks do not establish what Codex displayed,
what a writer accepted or literary consistency. When a change affects host
behavior, record the actual host, platform, input source, saved files, visible
result and any unavailable evidence. Native user input and explicitly authorized
delegated evaluation input are separate evidence sources. Never fabricate a
conversation or infer display from a successful save receipt.

The retained [capture evaluation](../tests/evaluations/host-capture.md) documents
legacy checks for automatic follow-ups, unchanged retry, interruption after save,
fresh-chat recovery, failed-save disclosure and exact retry. Its disposable
[fixture setup](../tests/fixtures/host-spike/setup.py) remains available. Preserve
evidence outside receipt discovery, under the fixture's local evidence folder.
Do not apply its legacy transcript protocol to notebook writing.

Current scoped evidence is linked in [development](development.md#compatibility-and-evidence).
Windows legacy host evidence does not prove Linux host behavior. Notebook
Desktop conversations remain unverified. English/Icelandic structural coverage
does not prove literary parity; voice belongs to the host and has separate limits.
Owner/manual assessment follows delivery; novice recruitment is not required.
Latency targets were withdrawn, so report measurements without obsolete gates.

## Completion report

State what changed, what relevant checks passed or failed and what remains
unverified. Name the exact checks run; focused results do not establish full-suite
or full-coverage success. Review the final diff for unrelated changes and broken
documentation links. Preserve historical evaluation records as evidence of their original runs;
old task numbers and closed gates do not create current implementation work.
Do not push, publish, deploy or change a real novel without user authorization.
