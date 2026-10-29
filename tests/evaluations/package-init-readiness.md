# Package initialization readiness

Date: 2026-10-29. **Remote candidate verified on Windows and Linux; full public-release scope remains incomplete.**
The maintainer authorized commit/push/workflow availability and candidate execution. Corrected source `1d6d6632c81ca8402ff60ca05a7ec832a0dea802` passed [candidate run 40882235905](https://github.com/bjarkig82/novel-creator/actions/runs/40882235905), attempt 1, artifact 12901057415. Windows: 208 tests passed; Linux: 208 total with three Windows-only skips. Both wheel identity/pinned save/reopen and clean dependency/install matrices passed. Separate source-archive rebuild/clean install and the corrected Windows guide command slice passed. [Candidate record](package-init-candidate.md).

35/48 tasks are complete: T033/T034/T035 have remote candidate evidence and T036 has verified publisher/environment setup. Actual Codex guide walkthroughs and full troubleshooting verification, final public name control/release metadata, complete public release documentation, publication and public named installs remain open. The maintainer now reports PyPI account bjarkig82; authenticated access and pending trusted publishing are verified; the name remains unreserved until first publication. The repository is now public by maintainer authorization. The pypi environment requires approval by bjarkig82, restricts deployments to main and disables administrator bypass; the matching pending PyPI publisher is registered and visibly verified. No publisher configuration, publication, real-novel edit or provider call occurred. Licensing remains intentionally unlicensed. Earlier sections/logs below retain their original local/pre-authorization scope.

## Implemented behavior

- `novel-creator init NAME` and optional full destination, separate title, en/is language, machine JSON or readable completion.
- Legacy path/brief interface and exact raw-brief provenance preserved, including JSON output without --json.
- Deterministic separate CLI request artifact; retries compare original choices/mode and preserve saved IDs/resources. Recognized novels ignore replacement settings; cleanup-required saves never claim ready.
- Printed interpreter preserves virtual-environment symlinks. Pinned launcher help discovers its sibling workflow directory. Dependency and Git-identity failures have actionable diagnostics.
- Canonical shipped writer guide and README/help/completion discovery, runtime handoff, inspection/resume, optional examples, and six troubleshooting categories.
- Verified package-guide fallback for historical novels, without modifying their original resources/history.
- Local manual candidate/publish workflow, immutable artifact identity/hash checks, scoped permissions and by-name public artifact comparison. This is prepared code, not a verified remote workflow.

## Executed evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Initial unchanged normal-access baseline | 22 tests passed; sandbox attempt separately failed temporary-file access | Implementation ledger and tool transcript |
| Windows broad regression | 191 total, 189 passed, 2 symlink-privilege skips; exit 0, 1116.246s. Began before later review/diagnostic corrections; not labeled a final-source full run. | [Full run](package-init-windows-tests.txt) |
| Final affected Windows suite | 43 tests passed; exit 0, 209.482s | [Focused run](package-init-final-focused-windows.txt) |
| Final fast contracts | 22 tests passed, including later source/provenance and release rejection guards; exit 0 | [Contracts](package-init-final-contracts.txt) |
| Supplementary Windows regressions | 3 provenance/missing-guide/concurrent-reservation cases passed, then 2 legacy raw-brief/recognized-replacement cases passed; these were run separately after addition | Tool transcript; corresponding test methods |
| Linux/WSL2 ext4 full source suite | 204 total, 201 passed, 3 Windows-only skips; exit 0, 32.145s. Later public empty-manifest guard separately verified in fast contracts. | [Linux run](package-init-linux-tests.txt) |
| Clean local-wheel dependency installations | Windows and Linux pass; declared dependencies fetched into fresh venvs, no inherited dependency sites; printed interpreter executes pinned validation. Default/Unicode, distinct title/is, explicit en/destination, spaces, and four invalid-input cases pass. | [Windows](package-init-clean-windows.txt), [Linux](package-init-clean-linux.json) |
| Installed wheel identity and pinned save/reopen | Final local wheel passes on Windows/Linux for unknown and Icelandic briefs plus name-only init/guide/version. Offline verifier borrows dependency sites and is explicitly separate from clean installs. Both final logs bind to wheel SHA-256 03d4701e30124af11cab53eb5f58d82a45e33fa672d491af9b0ac12e2ede1fdf. | [Windows wheel run](package-init-wheel-windows.txt), [Linux wheel run](package-init-wheel-linux.json) |
| Historical wheel continuation | Actual 2026-10-23 wheel creates novel; new package preserves all 34 recorded files and checkpoint, resolves labeled guide fallback; exit 0 | [Historical bundle](package-init-old-bundle.txt) |
| Build and metadata | Local wheel/sdist build succeeds; twine check passes without metadata warnings after README metadata added | [Build](package-init-build.txt), tool transcript |
| Source archive rebuild | Isolated sdist-to-wheel build succeeds; rebuilt verification wheel stays separate from original candidate bytes | [Rebuild](package-init-sdist-rebuild.txt) |
| Workflow structure/security tests | YAML parsed; only manual dispatch; every action pinned to a verified official commit; public job actions:read and publish-only id-token:write. Mocked wrong run/attempt/source/artifact/workflow/result/host binding, invalid evidence URLs, changed public metadata/download bytes and empty manifests rejected. | Final contracts, workflow file and tool transcript |

Linux source tests require editable resource mappings, separately from installed-package checks. The first noneditable source-test attempt had 11 missing-schema-layout failures; its [initial log](package-init-linux-initial.txt) is retained. The successful private snapshot installs editable mappings for source tests only. No system Python packages were changed. Base Ubuntu lacks ensurepip: the private caller's pip installs into clean --without-pip venvs using --python, without inheriting validator sites. The writer guide still explicitly requires normal pip/venv prerequisites.

Independent review found and prompted fixes for Linux interpreter symlink resolution, cross-platform resource line endings, public hash binding and cross-run artifact permissions. A second review confirmed the original fixes; additional local rejection tests exposed and closed missing attempt/artifact-ID/URL and empty-manifest validation gaps. Passing code/fixtures do not establish a genuine novice, literary or human approval result.

## Requirement assessment

| Scope | Local status | Remaining acceptance |
| --- | --- | --- |
| FR-002–FR-013; SC-002/003/004/006 | Command, settings, provenance, safety, diagnostics and legacy behavior implemented and covered by source/installed tests | No public-release claim implied |
| FR-001; SC-001 | Local package/build/clean installation available | Verify PyPI name control, choose confirmed release version, authorized remote candidate, publish, and both public named-install/hash checks |
| FR-014 | Both OS command/install matrices pass | Full literal writer-guide shell walkthrough still open; Ubuntu prerequisite limitation is disclosed |
| FR-015–FR-018; SC-005/007/008 | Guide, discovery, old-novel fallback, options/troubleshooting and structural command evidence available | Actual fresh Codex first-exchange/inspection/resume walkthrough on required host/platform combinations; complete guide-only walkthrough |
| Remote release workflow | Local YAML and integrity contracts pass | Push/availability/dispatch, remote candidate run/attempt/artifact ID, bound platform/host evidence, publisher/environment setup and production verification |

## Outstanding tasks

### Convergence verification — 2026-10-29

T041/T042 close the empty-destination and actual pip-selection gaps. These results supersede affected earlier local evidence; earlier logs retain their original scope. The updated local-only manifest records new artifacts from `dist/package-init-convergence`, previous hashes and current source hashes.

| Corrected-source check | Result | Evidence |
| --- | --- | --- |
| Windows affected contracts | 30 passed | [Contracts](package-init-convergence-contracts.txt) |
| Linux full suite and clean wheel | 208 total, 205 passed, three Windows-only skips; clean installation passes | [Linux](package-init-convergence-linux.txt) |
| Windows clean wheel | Default/options and five refusals pass, including no default-folder creation for empty destination | [Clean install](package-init-convergence-clean-windows.json) |
| Windows wheel resources and pinned save/reopen | Passed against corrected wheel | [Wheel](package-init-convergence-wheel-windows.json) |
| Corrected wheel/source build and metadata | Passed | [Build](package-init-convergence-build.txt) |
| Separate source archive rebuild | Passed without replacing original wheel | [Source rebuild](package-init-convergence-sdist.txt) |

Pip-selection contract tests cover normalized name/version, approved wheel/source filename/hash, missing hashes, duplicate products, unsupported reports and an alternate same-version platform wheel. The latter is rejected even when expected public files passed their metadata/download checks. This is fixture evidence; actual public installation remains pending. Public checks now emit `installed_product` with the selected filename and archive SHA-256 before reporting success.

At that local convergence checkpoint, 31 of 45 tasks were complete. The later authorized remote-candidate results above complete T033/T034/T035, with the current total at 34/48; full host and public release gates remain open.

T024/T025/T044/T047 retain full documentation/troubleshooting and actual-host validation. T031/T043/T046 await verified public name control/release metadata/documentation access. T037–T040/T045/T048 remain open for publishing, public named installs and final assessment; T036 setup is complete. T032/T033/T034/T035 now have successful remote candidate execution and platform evidence. Name lookup returned HTTP 404, which does not establish ownership. Licensing is intentionally unlicensed by explicit maintainer choice, not a pending question.

Historical local artifacts retain their original hashes. The current manifest now identifies the immutable GitHub candidate and its exact verified bytes. Version 0.1.0 remains provisional for public release because public name control is unverified; the maintainer now reports PyPI account bjarkig82. No package was published. Candidate commit/push/availability/dispatch authorization is settled; do not request it again for the completed action. Publisher setup, publication and actual host evidence remain distinct gates.
