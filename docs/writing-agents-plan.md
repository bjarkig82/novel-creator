# Native Codex writing agents implementation plan

Design: [approved writing-agent design](writing-agents-design.md).

Use scoped implementers and independent requirement/quality reviews, following
the repository's development instructions. Do not commit, push, publish, change
global configuration or modify a real novel. Work on the current task branch;
the only initial change is this chat's untracked approved design.

## Constraints

- Keep Python setup-only, notebook format 1, English/Icelandic, writer authority
  and existing legacy/pinned projects intact.
- Six native project agents; orchestrator by default, ongoing direct specialist
  access on request. A same-chat persona is not an accepted substitute.
- First inspect target-host capabilities in a disposable project. The writer
  subsequently authorized implementation with desktop acceptance pending because
  this managed workspace cannot access that UI; do not claim runtime verification.
- No unconditional fan-out, hardcoded provider models or permission overrides.
- Shared notebook updates and checkpoints belong to the delegation coordinator;
  direct specialists may save requested work. No concurrent writes to shared files.
- Manuscript, research and reviews are created only when requested/useful, with
  stable identities and one owner of prose; draft inventions remain proposals.
- Focused tests plus targeted wheel/sdist contents and isolated-install checks.
  Do not run the complete suite or complete release verifier for routine work.

## Tasks

### 1. Native host feasibility

- [x] Inspect available Codex version, documented custom-agent schema and actual
  client/protocol capabilities without touching global configuration.
- [ ] Use a disposable project and minimal agent definition to check native
  discovery, a real separate agent context, repeated direct specialist turns,
  and a return to orchestration wherever tools permit.
- [x] Record exact observed evidence and limits in
  `tests/evaluations/writing-agents-host.md`; distinguish protocol inspection,
  actual agent execution and desktop interaction.
- [x] Independently review the proof against the native-interaction requirement.
  If it cannot be exercised here, report the specific missing capability. The
  writer has authorized dependent implementation with desktop acceptance pending.

### 2. Role and manuscript workflows

Files: `notebook/workflows/{agents,manuscript,research,review}.md`,
`notebook/workflows/conversation.md`, `adapters/codex/notebook/AGENTS.md`,
`adapters/codex/notebook/agents/*.toml`, and focused notebook skills.

- [x] Add six thin namespaced TOML roles and platform-independent workflows for
  routing, scoped handoffs, direct conversations, persistence and role limits.
- [x] Add scene/chapter authoring, incorporation and revision guidance using
  `manuscript/index.md`, standalone scene files and owning chapter files.
- [x] Add sourced research and independent review guidance; preserve fact states,
  unknown context, writer edits, requested language and save-failure disclosure.
- [x] Add focused skills for specialist selection, research, scene/chapter writing
  and review. Keep existing outline invocation explicit-only.
- [x] Review requirements and quality independently before integration.

### 3. Initialization, packaging and structural regression checks

Files: `src/novel_creator/notebook.py`, `pyproject.toml`,
`tests/integration/test_notebook_init.py`, `tests/verify_wheel.py`,
focused new agent-resource tests and existing isolated-package tests.

- [x] Add failing initialization/resource tests for six distinct parseable roles,
  resolvable installed guidance/skill links, preserved source bytes, tracked files,
  both languages and no empty manuscripts; run to confirm meaningful failure.
- [x] Extend resource installation and wheel/sdist inclusion without changing
  existing-project refusal or legacy export behavior.
- [x] Run affected initialization, notebook contract and CLI cases; build both
  artifacts and verify their new resources through isolated installs.
- [x] Independently review specification compliance and code quality.

### 4. Scenario evidence, documentation and overall review

Files: focused evaluation scenarios/evidence, `README.md`,
`docs/functionality.md`, `workflows/everyday-writing.md`, and setup guidance.

- [x] Exercise focused disposable workflow scenarios covering separate-context
  review, unavailable browsing, scene/chapter drafting, incorporation, revisions,
  proposed inventions, seeded interrupted-transfer recovery and concurrent edits.
  Record actual observations and untested save/checkpoint errors. Native default
  routing and persistent specialist interaction remain pending under Task 1.
- [x] Document actual Codex controls, new-notebook-only delivery and limits;
  update old notes-only claims where the delivered workflow changes them.
- [x] Run focused link/whitespace and final affected checks; obtain an independent
  overall review, resolve findings and report exact test/evidence scope.

## Review focus and progress

Review native direct access separately from agent-definition validity; standalone
scene incorporation must retain recoverable prose and update ownership; delegated
agents must not race shared notes/checkpoints; unavailable browsing must not yield
invented sources; draft inventions and revisions must preserve writer authority.
Each corresponding task above carries its validation, including observed host
scenarios where structural tests cannot establish behavior.

Host evidence, resource implementation, packaging and workflow application checks
are recorded. Independent requirement and quality reviews passed each slice.
Final overall review identified one packaged-guide reference issue; the bounded
fix passed independent scoped re-review, with no open findings. The writer
explicitly authorized implementation with target-desktop acceptance pending;
that Task 1 native-interaction exercise is still outstanding.
