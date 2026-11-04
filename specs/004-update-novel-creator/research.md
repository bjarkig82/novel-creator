# Research: Existing-book Updates

**Date**: 2026-11-03 | **Baseline**: source 0.2.0; book origins 0.1.0 and 0.2.0

Research is source inspection and design analysis, not executed update qualification. The Spec Kit planning workflow requested two read-only research agents: one for storage/legacy ownership, one for retrospective exclusion. No product changes or provider calls were made.

## 1. Explicit package-to-book maintenance

**Decision**: Run the controller from separately installed updater-capable tooling. Check/preview does not write inside the book. Prepare the selected release in an external private cache. Recover using that controller even if the book launcher is unavailable.

**Rationale**: `install.bundle_files()` copies an independent runtime, resources and skills. Package installation deliberately does not refresh that copy. Using the pinned launcher as the only updater would strand older books and partially replaced runtimes.

**Alternatives considered**: implicit `init` refresh violates existing continuation guarantees; manual resource copying loses ownership and recovery checks; a source checkout violates the chosen release-only workflow.

## 2. Release selection and package preparation

**Decision**: Use the public PyPI JSON API for the fixed project `novel-creator`. Use `packaging.version.Version` and `SpecifierSet` for ordering and prerequisite checks; add `packaging>=24` as a direct dependency rather than importing pip's private vendored copy. Reject prerelease, development, local and yanked releases. Default to the highest stable version; disclose incompatibility without silently choosing an older version. Users may explicitly choose a different supported newer release.

Select a compatible wheel, bind filename/size/SHA-256 and normalized version, require HTTPS public PyPI/file-host URLs and validate redirects. A source-only release is an explicit unsupported-artifact blocker for this first updater. Do not run source build hooks. Verify wheel metadata, archive paths, duplicate names, symlinks, distribution identity and downloaded digest before use. Include byte-count bounds and network timeouts as hang/resource protection, not product timing targets.

Create a private venv with access to the configured interpreter's existing dependency packages, but always install the verified target product wheel into that private venv using isolated pip with `--ignore-installed --no-index --no-deps --no-compile` and its absolute local filename. `--ignore-installed` prevents a same-version inherited distribution from satisfying the request and avoids an uninstall of the inherited installation. Run pip using the private venv's interpreter, not the controller or original interpreter. Existing dependency distributions may be reused; the `novel_creator` product package may not be inherited. Check target requirements against the original book interpreter before apply. Missing/incompatible dependencies produce prerequisite guidance; the updater does not install into that interpreter or change global packages. Pin the updater controller separately from the selected target. Store the original interpreter path in the preview and revalidate it on apply/recovery.

Before running export/probes, verify the resolved `novel_creator` package origin is inside the private venv's site-packages, verify the installed product modules and packaged resources against the selected wheel's canonical byte inventory, and reject unexpected product files or product modules resolved outside that root. After export/probes, check every loaded `novel_creator` module origin as well as the resulting inventory. A version string or pip success exit alone is insufficient. Strip inherited Python path injection and run children with isolated-mode Python; do not import product code from the controller/source checkout as a fallback.

Acceptance includes a configured interpreter with a non-editable same-version product distribution whose bytes differ from the verified wheel. Preparation must create a private installed copy, export/probe the verified bytes, and leave the inherited package unchanged. Inject wrong-origin and modified-resource cases to ensure preparation blocks before a book update.

Use `-I -B` for target child processes and disable pip configuration loading with a per-process `PIP_CONFIG_FILE=os.devnull` in addition to isolated pip and the sanitized environment. The explicit `--no-compile` avoids creating extra product bytecode files during installation, so module/resource inventory comparison does not silently exempt unverified product files. Do not write configuration files or mutate inherited packages to achieve isolation.

The public preview option `--python` selects that interpreter explicitly, defaulting to the controller interpreter; return the selected absolute path for later book commands. Execute release preparation outside the book with a restricted environment: strip inherited pip alternate-index/auth settings, credential-bearing Git settings and Python path injection; use isolated pip and fixed public endpoints. Never interpolate tokens, private paths or book content into URLs. A changed runtime/dependency fingerprint invalidates the preview.

Target releases must advertise update protocol 1 and export a versioned bundle inventory through the isolated target process. Older releases without that protocol are recognized source-book origins, not assumed compatible targets. Validate exported paths and content against the wheel and fixed managed allowlist; do not trust arbitrary target output paths. Use controlled updater-capable future fixtures in tests without reserving a release number.

**Rationale**: PyPI exposes release files, Python constraints, yanked state and archive digests. Pip supports wheel-only installation and offline local installs. A public release is trusted product code; an archive hash detects mismatch and is not an independent publisher signature.

**Alternatives considered**: pip defaults can select alternate indexes/build source; executing a framework checkout breaks the source boundary; changing global dependencies creates unrelated effects. A handwritten version comparator is unnecessary risk.

**Primary references**: [PyPI JSON API](https://docs.pypi.org/api/json/), [pip install](https://pip.pypa.io/en/stable/cli/pip_install/), [pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/), [Python version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/). These describe packaging behavior; they do not prove any Novel Creator release currently supports updating.

## 3. Legacy ownership and shared files

**Decision**: Verify the committed manifest and book identity, then compare exclusive framework paths to their committed installation hashes and published source-release inventory. Treat `AGENTS.md`, `.gitignore` and `.gitattributes` as shared files, not wholly framework-owned merely because legacy `managed_paths` lists them.

Replace `AGENTS.md` only when its full content is the verified old generated default and index/worktree are unchanged; otherwise preserve custom content entirely and deliver discovery through the installed update skill. Append only missing required ignore/attribute lines, preserving original bytes, line endings and unrelated rules. If a shared file must change but has staged changes, refuse that affected path instead of absorbing its staged content into the update commit. Unrelated shared files that need no changes remain untouched.

Add separate installation-format/ownership metadata while preserving story schema `1.0` and novel identity. New continuation checks validate exclusive resources, not whole shared-file snapshots. Local framework edits, missing exclusive files, ownership uncertainty, symlinks/reparse points and new path collisions block application. Do not offer forced overwrite or automatic merge.

**Rationale**: Legacy initialization stores whole-file checksums for user-supplied shared files. A checksum proves installed bytes, not ownership. Existing `initialize()` validates all legacy checksum entries and must be adapted alongside new manifest handling.

**Alternatives considered**: treating all managed paths as replaceable destroys custom instructions; automatic text merging creates unreviewed instruction precedence; skipping integrity checks loses the update boundary.

## 4. Separate Git transaction

**Decision**: Use `root_path`, safe path validation, `atomic_json`, committed/index entry reads and the existing private-index/`commit-tree`/conditional `update-ref` pattern. Do not call `storage.save()` or invent a maintenance exchange. Keep updater journals below `local/update/`, because old saves interpret top-level `local/*.json` as exchange receipts.

Implement replacement-aware worktree/index guards; `check_managed()` is specifically for new exchange paths. Extend/factor `sync_index()` to handle removals through zero-mode entries while preserving exchange behavior. Construct the exact candidate commit before replacement; persist old/new blobs, expected branch/HEAD, affected index entries and candidate ID before mutation. Publish only after rechecking target bytes and checkpoints. Merge only affected index entries into the then-current index under its real lock.

**Rationale**: This preserves unrelated staging and makes the candidate Git object the recovery authority after uncertain publication. Repeated calls inspect actual branch/candidate identity rather than trusting a journal flag.

**Alternatives considered**: `git add -A`, stash/reset, normal unrestricted commit and replacing the entire index can capture or lose unrelated work. A story exchange would create false creative authority.

## 5. Maintenance exclusion and legacy crash limitation

**Decision**: Introduce a common new-runtime maintenance guard and a persistent updater-owned legacy `local/write.lock` fence. Acquire a new updater OS mutex, then the legacy fences nonblockingly; stop on contention. For 0.2.0, acquire local retrospective `state.lock.guard`, `authorization.lock.guard` and sorted per-run `.lock.guard` while state coordination is held. Access a bound external framework inspection guard only when an existing valid enabled grant permits it; otherwise perform no external checkout inspection. Never claim/release contribution ownership or call GitHub.

Before package replacement, durably install a standalone maintenance launcher that imports no book product modules. It refuses normal commands with the external recovery instruction. Preserve it until target verification and index cleanup finish; restore the final target launcher last. Legacy source bootstrap requires the writer to close other book sessions and explicitly confirm quiescence. Existing locks still reject active work; confirmation is not permission to steal a lock.

**Limitation**: Already-loaded 0.2.0 code does not understand new durable markers; its OS guards release after updater process death. A launcher gate cannot retrofit guards into arbitrary in-memory legacy clients. The supported legacy bootstrap requires quiescence and restart, and qualification must test this distinction. This is recorded for revisit in [FUP-001](follow-ups.md). Do not claim unconditional crash exclusion of preloaded legacy clients.

FR-009 now states that supported lifecycle explicitly: other book clients remain closed through application and external recovery, then restart through the guarded launcher. SC-005 requires separate observations for supported fresh launches and unsupported preloaded clients. The FUP-001 investigation is a foundational gate before maintenance/transaction implementation, not a late qualification-only check.

Lock-acquisition interruptions use fail-closed ownership: create the directory exclusively and durably publish matching ownership metadata before any launcher/resource/index/ref changes. A prepared token is not a claim to an empty or unproven directory. Stops before durable ownership yield an `ownership_unproven` blocker; preserve evidence, perform no automatic takeover and leave installed files unchanged. This avoids introducing platform-specific atomic-directory-publication machinery while retaining the explicit conflict behavior permitted by FR-011.

Guard future CLI dispatch before importing mutable book services and before retrospective failure journaling; also guard direct save/recovery, continuation and retrospective mutation entrypoints. Read-only status remains local; `notices_pending(language)` is not read-only and must not be used as an updater probe. Unknown/unresolved operational state blocks apply. All nonterminal contribution runs, uncertain publication and pending notice reservations block; unreserved queued notices and terminal evidence may remain if their schema is compatible and no cleanup is required.

**Alternatives considered**: the story writer lock alone misses retrospective mutations; a new marker alone misses legacy clients; new-runtime guards inside retrospective error handling could create notices while claiming to block maintenance.

Implementation uses a shared lease for ordinary mutations and an exclusive lease for maintenance. A single exclusive mutex for all ordinary calls would prevent revocation during an in-flight contribution, violating the existing authorization boundary. Windows uses nonblocking shared/exclusive [LockFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex); Linux uses shared/exclusive `flock`. Existing legacy bookkeeping locks are still bridged separately. The lease file owns no story or authorization data.

## 6. Verification without story changes

**Decision**: Before mutation, validate committed history and existing retrospective JSON against target readers/schemas in a read-only isolated process; do not call enable/disable/resume/release/notice methods. After installation, verify target inventory, imports, context/session/validation reads and candidate identity. Do not create a real exchange as an updater smoke test. Post-update new-save acceptance uses disposable fixtures only.

**Rationale**: Read operations can establish installed usability without mutating canon, notice inclusion or authorization. English/Icelandic and Unicode preservation are separately observable from native-host behavior.

**Alternatives considered**: a production smoke save changes book history; retrospective status helpers with rendering/reconciliation can mutate preserved evidence; wheel tests alone cannot qualify the native host.

All planning unknowns have design decisions above. FUP-001 remains an explicit implementation/qualification risk with a supported bootstrap constraint, not an unexplained architecture placeholder.
