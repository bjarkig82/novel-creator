# Quickstart Validation Guide: Automatic Retrospectives

This guide describes future acceptance execution after implementation. Retro commands and the listed focused tests are implemented; actual qualification outcomes are recorded separately. The guide itself performs no tests, GitHub probes, pushes or publication. Fake-transport results do not establish real GitHub behavior or native-host compliance.

## Prerequisites

Use Python >=3.11 with current project dependencies and Git >=2.39, disposable novel roots outside all Git repositories, and a separate disposable framework checkout. Optional real publication requires existing gh authentication and explicitly authorized upstream write access. Do not use real story content or credentials in fixtures. Use synthetic English and Icelandic material with distinctive private markers.

Commands below are PowerShell, run from the framework root. `$pythonExe` is the absolute compatible interpreter chosen for this environment. On Linux use the same argv with the configured interpreter and Bash quoting. All novel paths must be absolute. Resolve the package version and wheel filename from the candidate build; do not assume an older release contains this feature.

## Local automated verification after implementation

Focused test entry points:

```powershell
& $pythonExe -m unittest tests.contract.test_retro_cli tests.contract.test_retro_authorization tests.contract.test_retro_publication
& $pythonExe -m unittest tests.integration.test_retro_journey tests.integration.test_retro_recovery tests.integration.test_retro_privacy
& $pythonExe -m unittest tests.integration.test_portable_install tests.integration.test_path_redirection
```

Expected: deterministic tests use fake gh/GitHub transport, capture outbound requests, and never call the production repository. Temporary Git repositories exercise real local branches/indexes. Include at least these cases:

| Scenario | Expected evidence | Requirements |
| --- | --- | --- |
| Absent/disabled participation, with and without nominal access | Zero review and network/checkout probes; writing succeeds | FR-001, SC-001 |
| Enable, status, disable, copied novel/settings, partial grant writes | Only explicit bound grant enables; copies/partial state stay disabled; no stored tokens | FR-002–FR-003, FR-015 |
| Invalid/missing/overlapping checkout, missing gh, denied/revoked access | Disabled/blocked outcome; no mutation or credential setup | FR-003, FR-015 |
| Completed multi-turn task and explicit session close versus ordinary reply | Exactly one eligible claim for each completed task; routine turns yield none | FR-004–FR-005 |
| No finding, speculative feature, truncated or missing evidence | No PR; honest local outcome | FR-006–FR-008, SC-003 |
| One supported defect with two additional suggestions | One focused validated draft contribution only | FR-007, FR-010–FR-011, SC-002 |
| Dirty configured index/worktree and subsequent failure | Byte/index/history preservation; edits confined to allocated worktree | FR-009, FR-016, SC-006 |
| Failed/missing check, modified tree/body after approval, moved upstream | Publication blocked until affected validation is repeated | FR-010 |
| Existing equivalent open/merged fix, duplicate signal, concurrent novels | No duplicate review/PR; stable receipts; repository lock serializes operations | FR-005, FR-012, SC-004 |
| Interrupted push/create, timeout after server success, inconclusive queries | Intent retained; remote SHA/PR reconciled; no blind second create | FR-012, SC-004 |
| Disable during preparation, validation, or between push and create | Next operation stops; in-flight results recorded; no cleanup mutation | FR-015 |
| Private transcript/story/path/credential markers in evidence or candidate diff | Zero markers in outbound requests, Git objects and PR material; unsafe generalization skipped | FR-013, SC-005 |
| Failed/pending/cleanup-required writing save, redirected local paths, held locks | No retro begins; no lock stealing or story recovery bypass | FR-014–FR-016 |
| Unknown state version or lost machine grant | Fail closed; preserve receipts/worktrees; no silent migration | FR-002, FR-012, FR-015 |
| Same-run restart, disabled recovery, terminal claim release, abandoned/dead owner | Disabled resume/release returns re-enablement-required with zero framework/GitHub access; explicit enablement alone starts no work; directly requested same-binding recovery can reconcile and release, preserving all work and unresolved publication | FR-001, FR-009, FR-012, FR-015–FR-016 |

Add notice protocol tests at reservation-file creation, each notice reference update, story save and acknowledgement. Verify exact exchange/message/payload/text digests and UTF-8 spans, concurrent reservation conflicts, published-save/local-cleanup pauses, pending-save retention and confirmed-unsaved release. Recovery after save succeeds but acknowledgement fails must consume the existing reservation without inserting the notice again; local handling remains available after disablement. Assert fetch/base recording precedes worktree creation and its exact base SHA is used.

Repeat interruption cases at each local intent write, network call and result-write boundary. Include independent, unrelated PRs, closed PRs, unexpected head collisions, GitHub response with wrong draft/base/head, and failing optional host PR attachment. Assert no merge/deploy/credential/fork requests are emitted. A publisher scanner passing alone does not establish semantic privacy.

## Packaged and pinned installation

Build a candidate locally, then verify its exact wheel outside the checkout:

```powershell
& $pythonExe -m pip wheel . --no-deps --wheel-dir dist
& $pythonExe tests/verify_wheel.py $candidateWheel
& $pythonExe -m unittest tests.integration.test_install tests.integration.test_portable_install
```

`$candidateWheel` is the absolute newly built wheel path. Extend the verifier for the new retro modules, schemas, workflow, language resources and adapter bytes. In an independent novel, invoke its launcher with isolated Python and no framework PYTHONPATH and verify retro imports resolve to novel-local modules. No framework checkout is needed for normal writing; a configured checkout is required only for participation.

Compare an existing pre-feature novel's manifest, tracked files, HEAD and staged state before/after newer package installation and continuation. Expect no retro injection, opt-in or bundle rewrite. A fresh novel must contain pinned retro resources and default disabled state (FR-017, SC-007).

## Installed control smoke scenario

After implementation, from a new disposable novel:

```powershell
& $pythonExe "$novelRoot/.novel-creator/run.py" retro status --novel $novelRoot --json
& $pythonExe "$novelRoot/.novel-creator/run.py" retro disable --novel $novelRoot --json
```

Expect disabled state and no network calls. Enablement is intentionally not part of a generic smoke command: it authorizes real future external work. In fake-transport integration, exercise the explicit enable argv defined in [the CLI contract](contracts/retro-cli.md) and assert no production URL is contacted.

## Native host acceptance

Open a newly installed synthetic novel in Codex. Use its normal native public input and save-before-display workflow. In disabled mode, complete a task and verify zero retrospective activity. Under an explicitly authorized fake-transport contributor setup, exercise a multi-turn task, routine replies, session closure, no-action review, selected defect, and an interrupted run. Compare final displayed text byte-for-byte against the saved response, including whitespace. Confirm no retrospective suffix or story/canon changes, and verify a brief PR/problem notice appears automatically in the next normally saved reply without a status request. Inject failed saves and interrupted notice bookkeeping; verify pending notices survive and confirmed saved inclusion is not repeated. No-action outcomes remain queryable through status. Repeat English/Icelandic operational cases.

Record interpreter, installed bundle hashes, host input route, confirmed exchanges/checkpoints, task identities, receipt states, and synthetic transport requests. Native completion recognition and semantic privacy require review of actual host behavior; unit tests are insufficient.

## Optional real publication qualification

Only under separate explicit execution authorization for a controlled upstream test contribution: use a new synthetic novel, configured clean framework checkout and existing GitHub identity. Follow the opt-in and protocol contracts, produce one harmless evidenced correction, and verify a draft PR's actual target/base/head/commit and sanitized content. Record its URL and outcome locally; attach it to the host when supported. Do not merge, deploy, auto-close or delete remote branches. If access or approval is unavailable, report this qualification as unverified, not passed.

## Completion record

Map evidence to SC-001–SC-008 and FR-001–FR-018. Keep automated local tests, fake remote integration, real GitHub publication, native Codex behavior, semantic privacy review and human merge approval distinct. No timings are release gates. No feature is complete merely because these planning files exist.

## Convergence verification

Use `tests.integration.test_retro_comparison` for public unmarked/paraphrased/open/merged/closed-unmerged judgments, upstream-present fixes, stale snapshots, irrelevant markers and bounded summaries. Follow `comparison_required` with the snapshot-bound `retro compare` contract before proceeding; synthetic fixture helpers explicitly attest only their disposable public scope.

Use `test_retro_release_edges`, `test_retro_receipt_edges`, `test_retro_recovery` and `tests.contract.test_retro_transport` for terminal-save/owner-unlink/lock-cleanup interruption, re-enablement ordering, actual process death, immutable notice inclusion, idempotent publication notice, known URL before failed metadata lookup and in-flight revocation. `test_retro_diagnostics` verifies Unicode failed/interrupted/unavailable output, exact tree/log digests, retained attempts, ignored files and public-payload exclusion.

The pre-convergence fingerprint is retained at `tests/evaluations/automatic-retrospectives-source-before-convergence.json`. Current hashes and actual final results are recorded separately; historical reports remain evidence for their original bytes. T049/T055 remain open until authorized native/live qualification occurs. The local wheel is unpublished and must not be uploaded as the released 0.1.0 package.
