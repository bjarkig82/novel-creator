# Quickstart and Validation: Existing-book Updates

**Status**: Proposed validation guide. Update commands, test modules and the update verifier below are planned deliverables, not implemented or run by this planning phase. Use disposable books only for acceptance. No command here authorizes publishing a package, pushing a commit or updating a real manuscript repository.

## Prerequisites

- Windows PowerShell or Linux Bash, Python >=3.11, Git >=2.39, pip and the project's configured dependency/test environment.
- A built updater-capable wheel and a compatible controlled newer target wheel advertising update protocol 1. Do not infer availability from the current 0.2.0 version label.
- Verified historical 0.1.0 and 0.2.0 distribution wheels with recorded SHA-256 identities. Supply the release artifacts explicitly; a rebuilt tag is diagnostic source evidence, not identical published-wheel evidence.
- Synthetic English/Icelandic content and paths, Git test identity and no real credentials or manuscript content. Tests inject a fake release transport and block outbound network. Production CLI exposes no fake-server flag.
- Actual Codex host evaluation uses a separate disposable book and a restarted host session. The user selected/approved delegated evaluation input on 2026-11-04; preserve that provenance, keep direct native-user input unverified and do not infer Linux Codex integration from Linux CLI verification.

## 1. Contract and integration checks

From the repository root, using its configured interpreter:

```text
python -m unittest tests.contract.test_update_cli tests.contract.test_update_release tests.contract.test_update_protocol -v
python -m unittest tests.integration.test_update_preview tests.integration.test_update_apply tests.integration.test_update_recovery tests.integration.test_update_legacy tests.integration.test_update_retro_preservation -v
python -m unittest tests.integration.test_storage tests.integration.test_recovery tests.integration.test_install tests.integration.test_portable_install -v
python -m unittest discover -v
```

The new names above define proposed test entrypoints for subsequent tasks. Fixtures must include exact historical origins, mode/bytes/index snapshots and seeded private values, not mocks of the production reducer alone. Run relevant retrospective controls, notice and preparation/recovery regressions as part of discovery. Re-run only when changed code or failures justify it; no performance gate is added.

Expected outcomes: contract assertions pass, no real release/GitHub calls, no global settings changes, and no unreported unavailable checks. Check package inventory includes new Python modules, operational schema, update metadata, workflow and Codex skill through the existing wheel verifier.

## 2. Installed package journey

The standalone `tests/verify_update.py` accepts `--source-wheel PATH` (repeatable), `--target-wheel PATH` and `--json`. It installs artifacts into disposable environments and supplies fake release responses internally; it is not a production source-checkout update route. Run `verify_wheel.py` against the distribution built from the current checkout version. A controlled newer target fixture can carry a different version and is qualified separately by `verify_update.py`; neither is a published release claim.

Windows example after implementation, with explicit verified artifact paths:

```powershell
$source010 = Read-Host 'Absolute path to verified 0.1.0 wheel'
$source020 = Read-Host 'Absolute path to verified 0.2.0 wheel'
$targetWheel = Read-Host 'Absolute path to controlled updater-capable target wheel'
$distributionWheel = Read-Host 'Absolute path to distribution built from this checkout version'
python tests/verify_update.py --source-wheel "$source010" --source-wheel "$source020" --target-wheel "$targetWheel" --json
python tests/verify_wheel.py "$distributionWheel"
```

Linux equivalent:

```bash
read -r -p 'Absolute path to verified 0.1.0 wheel: ' source010
read -r -p 'Absolute path to verified 0.2.0 wheel: ' source020
read -r -p 'Absolute path to controlled updater-capable target wheel: ' target_wheel
read -r -p 'Absolute path to distribution built from this checkout version: ' distribution_wheel
python tests/verify_update.py --source-wheel "$source010" --source-wheel "$source020" --target-wheel "$target_wheel" --json
python tests/verify_wheel.py "$distribution_wheel"
```

The verifier creates independent source books with isolated interpreters. For each origin it prepares exact source exchanges, a session, Unicode manuscript files, custom instructions, unrelated tracked/untracked work and partial index staging. It runs the public controller contract through a local test transport, then verifies the installed launcher with an interpreter that cannot import product modules from the framework checkout.

Expected: preview leaves book bytes/HEAD/index/retro state unchanged; apply creates one framework-only commit with the reviewed parent and release; candidate differs only in approved paths. Context, inspect, session listing/resume and validation retain original data. A new synthetic exchange saves successfully after completion. Repeated apply/recovery creates no second update commit. Preserve all original exchange/manuscript bytes and unrelated staged content.

## 3. Operational command flow

These commands describe the implemented writer workflow once an updater-capable package is available. `PATH`, `VERSION`, `UUID` and `HEAD` stand for exact values returned by a successful preview; do not guess them or paste sample IDs.

```text
novel-creator update --novel PATH --json
novel-creator update --novel PATH --version VERSION --json
novel-creator update --novel PATH --apply --preview UUID --version VERSION --expected-head HEAD --confirm-quiescent --json
novel-creator update status --novel PATH --json
novel-creator update recover --novel PATH --operation UUID --json
novel-creator update recover --novel PATH --operation UUID --retry --expected-head HEAD --json
```

Close other book runtimes before confirming legacy quiescence and keep them closed throughout application and external recovery. Restart only through the guarded launcher. That flag never clears a held lock or proves process discovery. Retain the separately installed controller/interpreter for recovery. Status and recovery inspection are read-only and offline. Apply/retry require explicit reviewed state. Reload Codex instructions after `ready: true`; do not resume writing on `cleanup_required` or mixed state. Detailed fields and errors are in [the CLI contract](contracts/update-cli.md).

## 4. Failure and preservation matrix

| Scenario | Required observation |
| --- | --- |
| New latest release, explicit older stable target, incompatible latest, already current | Exact selected target or explicit blocker; no silent fallback; no book writes during preview. |
| Offline/HTTP error, yanked/prerelease/local version, source-only release, wrong hash/identity, hostile archive path, unsupported protocol/dependencies | Truthful unavailable/unsupported/error state, no install or global dependency changes. |
| Custom AGENTS, changed shared rules, staged affected shared file, modified/missing exclusive resource, new-file collision or removal | Custom content retained; conflicting apply refused; unchanged verified removals handled correctly in worktree and index. |
| Changed HEAD, branch, worktree, index, grant or notice after preview | Conflict requiring fresh preview; no stale overwrite. |
| Concurrent writer/retro operation, pending save/cleanup, run/notice reservation, uncertain publication or held fence | Nonblocking refusal; no lock theft, contributor reconciliation or external network probe. |
| Disabled/absent/revoked/mismatched grant and valid enabled grant with clean terminal state | Byte-identical grants, bindings, run and notice evidence; zero enable/disable/publication/notice-consumption calls. Disabled cases never access external checkout storage. |
| Crash around journal/fence creation, launcher swap, each file replacement/removal, ref publication, index sync, verification, completion or fence release | Accurate local status; fresh launches pause; exact-candidate recovery for proven ownership or the explicit unproven-ownership blocker before installation changes; no duplicate commit or story replay. |
| Changed recovery bytes, stale expected HEAD, ambiguous owner/PID reuse, missing local artifact | Preserve evidence and refuse; no blind download, forced rollback or lock deletion. |
| Hard stop after lock-directory creation, before ownership-file publication/flush or the confirmed journal checkpoint | `ownership_unproven`, exit 6, unchanged launcher/framework/index/HEAD, preserved lock/journal and no automatic takeover based on prepared intent, an unacknowledged owner file or presumed process death. |
| Different controller and `--python` interpreters | Selected absolute interpreter reaches preparation/probes, is returned as `runtime_python` and remains bound on apply/recovery; changed prerequisites block rather than selecting another interpreter. |
| Configured interpreter already has the target product version installed, with deliberately different product bytes | Private-venv pip still installs the verified local wheel; product import origins and all module/resource bytes match that private copy before/after probes, while inherited package bytes remain unchanged. Wrong-origin/changed-resource injection blocks preview/application. |
| US1 status before any update transaction is implemented | Synthetic journals and real disposable refs cover no operation, pending, published cleanup, conflict/unproven ownership and complete observations through the public CLI, with no writes or network. US3 later reuses that same inspector for real recovery. |
| Outgoing requests with seeded private values; credential-bearing pip/Git environment | Fixed public release requests only, zero seeded private data or credential propagation, no inherited alternate index/auth behavior. |
| English/Icelandic, Unicode paths, Windows/Linux | Preserve all settings/bytes; separately record CLI and native-host outcomes. |

For hard interruption use actual subprocess termination after an acknowledged durable fault point. An exception caught in-process does not establish crash durability. Capture initial/final HEAD, tree diff, semantic index entries, resource hashes, state/grant/notice hashes, operation/candidate IDs and exact observed exit/state. Keep private diagnostics outside distributable evidence.

## 5. Revisit FUP-001 and report qualification

Read [the tracked compatibility follow-up](follow-ups.md). Its test-only historical-client investigation is a foundational gate before maintenance/transaction implementation, followed by requalification of the implemented behavior. Exercise actual 0.1.0/0.2.0 fresh launcher attempts and separately already-imported legacy clients. Verify the lock bridge during live apply and the persistent writer/launcher fence after a hard interruption. Do not claim an old in-memory retrospective client understands a new durable marker. Supported bootstrap requires closing those clients through application and recovery; failure to demonstrate that supported boundary blocks dependent implementation or interrupted-update qualification.

Record results under a new `tests/evaluations/` update qualification artifact with wheel hashes, platform/interpreter versions, individual matrix outcomes and limitations. Native Codex must demonstrate explicit preview/application, preserved custom instructions and reloading the installed update workflow. Do not initiate a retrospective/publication as part of this check.

Functional acceptance covers SC-001-SC-009. Timings are informational only; novice testing and release publication are outside this workflow. Documentary plan completion, passing CLI tests, native-host acceptance and published-release readiness are separate claims.
