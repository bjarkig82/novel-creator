# Implementation Plan: Package Installation and Simple Novel Initialization

**Branch**: `main` (actual Git branch; no branch hook configured) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: `specs/002-package-novel-init/spec.md`. Spec Kit reports feature identifier `002-package-novel-init`; it is not an existing Git branch.

## Summary

Extend the existing Python package and console command with `novel-creator init NAME [--path DEST] [--title TITLE] [--language en|is]`, readable completion and unchanged legacy brief-file support. Publish a verified versioned package to PyPI. Candidate distribution name is the existing `novel-creator`, subject to verifying owner control before release. Ship a complete getting-started guide with the existing workflow resources and link it from README, help and completion.

Canonical installation uses standard pip in a user-owned virtual environment outside novel repositories. Reuse existing pinned novel launchers and show the exact runtime interpreter in completion so Codex need not inherit shell activation. No npm wrapper, custom runtime or new dispatcher. See [research](research.md).

## Technical Context

**Language/Version**: Existing Python >=3.11; Git >=2.39. Verify documented interpreter/OS combinations rather than promising all future Python versions.

**Primary Dependencies**: argparse, importlib.resources, setuptools>=77; existing jsonschema>=4.23,<5 and jsonschema-rs>=0.59,<0.60. Release-only tools: build and twine. No new runtime dependencies.

**Storage**: Independent Git novels, schema-v1 bootstrap artifacts, checksum manifests and ignored immutable setup state. No story-schema migration.

**Testing**: Existing unittest contracts/integration suite, installed distribution/resource verification, sdist rebuild, clean dependency installation, public-index checks on Windows/Linux, and labeled Codex first-exchange/inspection/resume walkthrough.

**Target Platform**: Windows PowerShell and Linux Bash; label WSL evidence separately. macOS/additional hosts deferred.

**Project Type**: Local CLI with packaged Codex workflows and Markdown documentation.

**Performance Goals**: No latency thresholds; withdrawn targets remain retired. Errors/timeouts remain failures.

**Constraints**: No provider/network during initialization, global settings changes, manuscript edits, repository nesting or silent upgrades. No source-checkout dependency. Package acquisition/publication requires network. Preserve root/index/history/reparse/lock/CAS/recovery guards.

**Scale/Scope**: One writer per independent novel; four stories, FR-001–018, SC-001–008. This phase writes design artifacts only; no implementation, tasks, publication or account changes.

## Constitution Check

Pre-research gate: PASS. Post-design gate: PASS with the same boundaries. No waiver/amendment proposed.

| Principles | Design evidence |
| --- | --- |
| I, XI: simplicity/incremental delivery | Extend current CLI/package; pip/venv and shipped Markdown; locally verified candidate precedes public release. |
| II, VIII: platform boundaries | Shared workflows and Codex adapter remain separate; no custom AI runtime/dashboard. |
| III–V: authority/provenance/guidance | Settings only, unknown creative choices remain unknown, no invented messages/canon; later conversation retains save-before-display. |
| VI: portable authority | Independent Git projects, pinned resources, existing-schema request artifact; old novels unchanged. |
| VII: language | Exact Unicode and en/is cases; no translation. |
| IX: evidence | Local artifacts, clean dependencies, public installs, host operation and human approval remain distinct. |
| X: accessibility | Text, descriptive links, copyable shell-labeled commands; no screenshot-only essential steps. Dashboard outside scope. |

PyPI name control, truthful metadata/licensing and publisher configuration are release prerequisites, not design exceptions. Missing evidence prevents release completion, not local planning. No license file was found: do not select a license without maintainer direction or imply licensing readiness.

## Project Structure

### Documentation (this feature)

```text
specs/002-package-novel-init/
  spec.md
  plan.md
  research.md
  data-model.md
  quickstart.md
  contracts/cli.md
  contracts/distribution-and-docs.md
  checklists/requirements.md
```

`tasks.md` belongs to the later `$speckit-tasks` phase.

### Source Code (repository root)

```text
pyproject.toml
src/novel_creator/{cli,install,records}.py
workflows/getting-started.md                 # proposed canonical writer guide
workflows/{initialize,entry}.md
adapters/codex/AGENTS.production.md
adapters/codex/skills/novel-init/SKILL.md
README.md
docs/{poc-quickstart,development}.md
tests/contract/{test_cli,test_initialize}.py
tests/integration/{test_install,test_initialize_journey,test_portable_install}.py
tests/verify_wheel.py
.github/workflows/package-release.yml        # proposed protected release workflow
```

**Structure Decision**: Keep one Python project. Put the guide in workflows/ because those resources already ship in the package and are pinned into novels; no documentation service or duplicated canonical guide.

## Component Design and Compatibility

1. Parse two exclusive forms before writes: shorthand NAME with optional path/title/language, or legacy explicit path/brief file. Add --version from the release version source. Preserve legacy JSON even without --json; shorthand defaults to readable text and supports the existing JSON envelope.
2. Deterministically normalize effective brief and append a separate bootstrap request input artifact for name/resolved target/explicit settings. Keep ordinary project source references pointing at brief fields. Existing schema supports multiple bootstrap artifacts; no new novel_project fields.
3. Reuse initialize/bootstrap/storage. Retry compares canonical setup choices plus brief bytes and reuses immutable saved bundle IDs/resources. Never regenerate pending identity or delete receipts. Recognized novels continue without applying replacement flags. Retain legacy acceptance of otherwise empty unborn repositories and safe instruction/metadata files.
4. Keep pinned run.py loading novel-local code. Shorthand output exposes resolved root, sys.executable, launcher and guide locations; these are advisory output, not committed machine paths. For older novels lacking a pinned guide, link to the verified installed-package guide with a fallback label, preserve all novel resources, and evaluate readiness against their original manifest. Guide explicitly passes that interpreter to Codex. Verify in a newly opened Codex project, not just an activated terminal.
5. Ship one canonical writer guide covering installation through first saved conversation, inspection/resume, optional settings and six troubleshooting categories. Reconcile existing quickstarts and update installed environment guidance. Initial setup still needs no story idea/provider credentials.
6. Use separate manual candidate/publish workflow modes. Candidate mode builds wheel/sdist once from an immutable source commit and stores them plus a manifest in an immutable artifact identified by repository, run ID/attempt and artifact ID. Candidate platform/guide/host checks consume those bytes and record that identity. Publish mode downloads the selected artifact, verifies manifest identity and hashes, and uploads without rebuilding through protected PyPI Trusted Publishing. Missing/mismatched/expired artifacts or evidence fail closed; source/rebuild changes require a new candidate. A rebuilt-sdist wheel is verification output only. Pin action revisions during implementation. No publishing on ordinary push/PR events. Repository workflow availability, dispatch and publication are separately authorized execution steps; this planning invocation performs none.

## Verification and Delivery Gates

| Gate | Evidence and mapping |
| --- | --- |
| Arguments/settings | Default and optional choices, en/is, spaces/Unicode, invalid/mixed forms; SC-002, FR-002–008. |
| Safety/compatibility | Existing tests plus repeated novels, changed name with same title, fault/retry, aliases, identity/access, concurrent reservations, cleanup-required; SC-003/004/006. |
| Packaging | Wheel/sdist metadata, rebuilt sdist, source/resource hashes outside checkout; local candidate evidence only. |
| Runtime/dependencies | Clean Windows/Linux environments without inherited packages/PYTHONPATH; exact interpreter used in separate Codex host; SC-001/005/007. |
| Documentation | Three discovery paths, executable examples, confirmed first exchange + inspection/resume, six failure categories; SC-007/008. |
| Public delivery | Install exact named release from PyPI without local artifacts/cache; compare hashes/version and repeat novel entry on both platforms; required for SC-001. |

Existing wheel verifier inherits dependency packages; retain that useful source/bundle check and add independent clean/public evidence. New bundle changes require affected suites/resource checks again. Use disposable novels, label command fixtures vs actual host operation vs subjective approval; record skips/unavailable checks honestly. No novice/manual or latency gate is introduced.

## Complexity Tracking

No constitutional violations. No new service, runtime manager, story schema, package ecosystem or provider integration is planned.


## Owner-approved verification scope — 2026-10-29

Per the explicit owner amendment in spec.md, use an actual Windows Codex Desktop setup/first-save/inspection/resume walkthrough plus Windows PowerShell and Linux Bash package/CLI/guide/troubleshooting/public-install checks. Linux Codex integration is unverified; do not claim a Linux host pass. The release verifier requires windows_guide, linux_guide, windows_host and linux_cli true, with linux_host explicitly false. All evidence remains bound to the immutable candidate. No additional provider integration, custom runtime or migration is introduced.
