# Quickstart Validation: Package Initialization

Status: planned validation procedure. The shorthand, --version, shipped guide and public release are not implemented/verified by this planning run. Execute after implementation against an explicitly identified candidate/release. This is the maintainer validation guide; the writer-facing deliverable is workflows/getting-started.md described by [documentation contract](contracts/distribution-and-docs.md).

## Prerequisites and evidence

Python >=3.11 with venv/pip, Git >=2.39, configured test Git identity, Windows PowerShell and Linux Bash runners, and Codex for actual host checks. Use disposable novel paths outside every repository. Record exact source revision/version, artifact hashes, OS/shell/interpreters/Git and skips. Do not alter global identity or execution policy for testing. Real user identity configuration is a documented user action; test identities are scoped to test processes.

For public verification, first confirm maintainer control of distribution name, version and publisher; publication is a separate authorized release step. Do not execute install examples against an unverified namesake package. Replace the candidate distribution name consistently if a maintainer-approved rename is needed. No model credentials required.

## 1. Candidate source and packaging checks

The commands below are preliminary local checks. For release acceptance, make the workflow available in the repository and dispatch its manual `candidate` mode only under explicit execution authorization. Record repository, candidate run ID/run attempt, source commit, immutable artifact ID, distribution/version, wheel/sdist filenames and SHA-256 hashes in the release manifest. Download that stored artifact for final wheel/platform/guide/host validation. Evidence must bind to this identity; local builds and sdist-rebuilt test wheels never replace the stored release bytes. Final guide/host checks run after the candidate exists; they do not block producing the candidate from finished story code/docs and preliminary local checks.

Later manual `publish` mode selects this same candidate identity, downloads and verifies it plus the evidence, and uploads without a build step. Missing/expired/mismatched artifacts or evidence fail closed. A new source/build requires a new candidate and affected verification; publication records its own run separately. No workflow dispatch or publication is performed by following this document as a planning artifact.

From the framework root, with its existing development environment active:

```text
python -m unittest discover -v
python -m build
python -m twine check dist/*
```

Use a clean release output directory or explicitly select only the wheel/sdist of the intended version for metadata checks. Install build/twine in the build environment as build-only dependencies if absent. Existing development tests are separate from candidate/public installs.

Verify the exact candidate wheel using the existing verifier; set wheelPath to its actual absolute filename:

```powershell
python tests/verify_wheel.py $wheelPath
```

```bash
python tests/verify_wheel.py "$wheelPath"
```

Expect exit 0 and installed module/resource identity checks. The verifier inherits dependencies and is not clean-install evidence. In another clean environment, install the candidate wheel with normal dependency resolution, rebuild/install the sdist, and repeat steps 3–6. Record installed dependency versions/source; product imports must come from the installed wheel, never checkout/PYTHONPATH. Check guide bytes and new-novel bundle checksums.

## 2. Production named installation

Run only after a verified release is public. Set releaseVersion to the exact released version recorded in release evidence (a quoted version string, not an assumed latest). Create the environment outside novels and framework. Paths below are illustrative reusable test locations; choose unused ones and do not overwrite existing environments.

Windows PowerShell:

```powershell
$runtimeRoot = Join-Path $env:USERPROFILE 'NovelCreatorValidationRuntime'
python -m venv $runtimeRoot
$runtimePython = Join-Path $runtimeRoot 'Scripts/python.exe'
& $runtimePython -m pip install --no-cache-dir --index-url https://pypi.org/simple "novel-creator==$releaseVersion"
& $runtimePython -m pip check
$novelCommand = Join-Path $runtimeRoot 'Scripts/novel-creator.exe'
& $novelCommand --version
& $novelCommand init --help
```

Linux Bash:

```bash
runtimeRoot="$HOME/NovelCreatorValidationRuntime"
python3 -m venv "$runtimeRoot"
runtimePython="$runtimeRoot/bin/python"
"$runtimePython" -m pip install --no-cache-dir --index-url https://pypi.org/simple "novel-creator==$releaseVersion"
"$runtimePython" -m pip check
novelCommand="$runtimeRoot/bin/novel-creator"
"$novelCommand" --version
"$novelCommand" init --help
```

Expect the selected public version, resolved declared dependencies and working help. Clear inherited PYTHONPATH and package-index overrides for the controlled check; do not log secret environment variables. Record public artifact hashes and compare with the verified release. These explicit-interpreter examples avoid relying on PowerShell script activation policy. Separately execute the writer guide's documented activation/name-only command path.

## 3. Initialize and inspect outside checkout

Change to an unused writable parent outside repositories; set novelParent to that absolute path. Environment directory must not be inside the novel target.

PowerShell:

```powershell
Set-Location -LiteralPath $novelParent
& $novelCommand init 'My Novel'
$novelPath = Join-Path $novelParent 'My Novel'
& $runtimePython "$novelPath/.novel-creator/run.py" validate --novel $novelPath --json
& $runtimePython "$novelPath/.novel-creator/run.py" context --novel $novelPath --json
```

Bash:

```bash
cd "$novelParent"
"$novelCommand" init 'My Novel'
novelPath="$novelParent/My Novel"
"$runtimePython" "$novelPath/.novel-creator/run.py" validate --novel "$novelPath" --json
"$runtimePython" "$novelPath/.novel-creator/run.py" context --novel "$novelPath" --json
```

Expect independent Git root, confirmed checkpoint, ready result, correct interpreter/root/guide paths, title My Novel, default en and unknown remaining creative choices. No provider/network used by init. Copy/inspect the installed guide and required skills; framework source must be unavailable to the child operation.

## 4. Settings, provenance and refusal matrix

Using new disposable targets, run optional choices in both shells (with their command variable syntax from above):

```text
novel-creator init 'Bref' --title 'Bréf frá morgundeginum' --language is --path ABSOLUTE_UNUSED_TARGET --json
```

Replace ABSOLUTE_UNUSED_TARGET and quote it for the shell. Expect exact title/language, separate NAME request evidence, ordinary brief sources and no fabricated conversation/canon. Repeat for explicit en, omitted values, spaces/Unicode and explicit destinations.

Exercise invalid language/options, path-like/empty names, mixed shorthand/brief, occupied targets, nested repos, aliases, missing Git/identity, permission denial and concurrent initialization with existing test harnesses. Snapshot existing bytes/history first; refusals preserve them. Repeat recognized initialization with different flags: same identity/history/settings/resources and continuation only. Legacy path/brief cases remain unchanged.

Inject interruption through the existing disposable fault-enabled test harness, then retry unchanged. Verify original request/bundle IDs and exactly one bootstrap. Change NAME while keeping explicit title: conflict. Alter brief/files: conflict. Published cleanup-required state: saved true, ready false, exit 0, explicit inspection/recovery; no rollback or duplicate save. Use the existing recover CLI and confirmed expected-head contract rather than deleting evidence.

## 5. First-use documentation and actual Codex handoff

Also exercise shorthand continuation of a pre-feature novel whose original manifest lacks a guide. Confirm the output labels and resolves the installed-package guide fallback, readiness uses the original manifest, and every novel file/manifest/history entry remains unchanged. Prefer a verified pinned guide where one exists; a missing fallback must give a documentation diagnostic, not a nonexistent path. Legacy JSON output remains unchanged. The package guide must explain that reading it does not upgrade the older novel's workflows.

Start from README, then independently from help and completion; all routes must reach the canonical guide. Follow it without undocumented steps. Check optional-setting examples, expected outcomes and all six troubleshooting entries. Verify PyPI README links are usable absolute release links.

Open the new novel folder in a fresh Codex project, supply the printed runtime interpreter path, and invoke $novel-init. Use the guide's no-story-idea sample. Confirm the exact current input and response are saved before display; inspect saved state, close/reopen, and invoke $novel-resume. Context/mode/unknown choices must persist; no reinitialization. Capture actual host evidence separately from command fixtures and human usability approval. Windows host evidence does not establish Linux host evidence; record unavailable combinations honestly.

## 6. Completion assessment

Map results to SC-001–008 and FR-001–018 using [plan gates](plan.md). Local candidate, clean dependency, public install and actual host evidence are separate entries. Required unexecuted checks remain unverified. No latency target, novice/manual gate, or subjective literary-quality result is inferred. Public named installation must succeed before the feature is marked complete.


## Scope amendment — 2026-10-29

The owner approved actual Windows Codex Desktop verification plus Linux Bash/package/CLI evidence for this release. The Linux Codex-host portion of section 5 is explicitly unverified and not a 0.1.0 release gate. All other command, troubleshooting, exact-input/save, public delivery and immutable-artifact checks remain required.
