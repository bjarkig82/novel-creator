# Quickstart and Validation Guide

These commands and test modules describe the planned implementation. They are not available or passing merely because this plan exists.

## Prerequisites and creation

Use a disposable path outside every Git repository. Install a candidate implementation wheel in Python >=3.11 with Git >=2.39 and an existing intended Git identity. Actual behavior evaluation requires Codex with native file/Git tools.

Proposed creation command:

~~~bash
novel-creator notebook init "Notebook Trial" --path /tmp/notebook-trial --language en --json
~~~

Windows uses a new absolute path outside repositories. Verify every installed guidance link resolves and the shared resources remain separate from the Codex entry. Verify the independent repository and installed contents against [the setup contract](contracts/setup-and-host.md). No invented story facts, empty character sheets or transcript journal.

Open the folder in Codex and start brainstorming without invoking a special skill or requesting a save.

## Acceptance journeys

1. **Capture and authority (SC-001, SC-004)**: Explore a keeper and two motivations. Accept one trait, express only interest in another and leave a substantive question open. Verify saved states and no redundant approval. With no mode request, verify guided help; request freeform exploration and verify immediate adaptation without a questionnaire.
2. **Fresh session/brief (SC-002, SC-003)**: Open a new conversation with no old chat context. Introduce a new character: no recap. Ask for a keeper brief: only supported relevant facts/proposals/questions. Ask about an unknown topic: no invented memory.
3. **Revision/continuity (SC-005)**: Establish a fact linked to a plot note; propose a significant contradiction. Verify conflict surfaced before canon change. Clearly revise the fact; verify current notes, impact review and recoverable prior value. Distinguish character beliefs from truth.
4. **Interruption/failure (SC-006, SC-007)**: Leave after a meaningful turn without session closure; retrieve decisions in a fresh session. Deny a disposable write and verify failure disclosure. Allow file writes but fail Git checkpointing: verify saved-versus-history distinction and retained superseded prose.
5. **External/staged edits (SC-006)**: Stage an unrelated file before a note update; verify bytes and index entry remain intact. Stage a manual edit in a touched topic; ensure checkpointing does not consume it. Change a note between read and patch in a controlled host journey; verify reconciliation.
6. **No legacy dependency (SC-008)**: Complete brainstorming and briefs without a Python save/validation call. Confirm no installed runtime, exchange receipt, retrospective or update controller.
7. **Existing targets (SC-009)**: Test a disposable legacy novel, completed notebook, empty directory and unrelated occupied directory; setup refuses without mutation. Also test symlinked paths, nested repositories, concurrent creation and partial setup failure.
8. **Language/identity**: Repeat core journeys in Icelandic with Unicode names. Rename a character without breaking references. Open cross-topic links as ordinary file links and locate the referenced Item-ID without any custom-anchor support. Use two same-title characters and verify focused disambiguation.

## Planned deterministic checks

~~~bash
python -m unittest tests.unit.test_notebook_contract tests.integration.test_notebook_init tests.integration.test_notebook_package
python -m unittest discover
bash tests/speckit-smoke.sh
python -m pip wheel . --no-deps --wheel-dir dist
~~~

The new modules are planned additions. Extend existing wheel and package-install verifiers to cover wheel/sdist resources and outside-checkout initialization while retaining legacy expectations.

## Evidence and completion

Record source/package, OS, host, actual input route, tool permissions, outcomes and limitations in tests/evaluations/agent-story-notebook.md. Separate structural results, native-host judgments and literary-quality assessment. Linux native host and any unavailable environment stay unverified until actually exercised.

Plan phase ends with these reviewed design artifacts. Product completion requires implementation, acceptance journeys and recorded evidence. No release, implementation or migration is performed by planning.
