# Feature Specification: Update Novel Creator in Existing Books

**Feature Branch**: `main` (feature directory and branch are independent; no branch was created)

**Created**: 2026-11-03

**Status**: Draft

**Input**: User description: "I would like to be able to update novel-creator in the repo I'm working on if there is an update published after I started working on my book." Subsequent decisions: check only when asked; use published stable releases with latest or explicit version selection; provide one guided workflow with preview and explicit application. Use the current 0.2.0 product baseline, cover older 0.1.0 books, and preserve retrospective settings, authorization and recovery evidence.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Check and preview an available update (Priority: P1)

As a writer working in an existing book repository, I want to explicitly check for a newer published release and understand what it would change before deciding to update.

**Why this priority**: A writer needs to distinguish the version installed in their book from the separately installed package, and make an informed choice without changing their writing environment.

**Independent Test**: Present a recognized existing book and controlled release listings; request a check and preview. Verify that the writer receives the installed version, selected release, proposed framework changes and compatibility or blockers, while the book's files and history remain unchanged.

**Acceptance Scenarios**:

1. **Given** a book pinned to an older release and a newer published stable release, **When** the writer requests an update check without choosing a version, **Then** the latest stable release is selected for preview, its identity and proposed framework changes are shown, and no update is applied.
2. **Given** several published releases, **When** the writer selects a particular newer stable version, **Then** the preview describes that exact release rather than substituting a different version.
3. **Given** a book already using the selected release, **When** checked, **Then** the writer receives an already-current result and the book remains unchanged.
4. **Given** release information cannot be retrieved or the selected release is unavailable, **When** checked, **Then** the limitation and next action are disclosed without claiming the book is current or changing it.
5. **Given** a normal start, resume, save or package installation, **When** the writer has not requested an update check, **Then** no automatic release check or book update occurs.
6. **Given** a requested downgrade, prerelease or source-checkout version, **When** selected, **Then** the unsupported selection is explained and no update is applied.

---

### User Story 2 - Apply a reviewed update without losing book work (Priority: P1)

As a writer, I want to explicitly apply the release I reviewed through one guided workflow, retaining all my book work and custom instructions.

**Why this priority**: This delivers the core value: adopting framework improvements without starting a new book or manually replacing framework files.

**Independent Test**: Use a compatible older book containing saved conversations, story records, manuscript content, custom instructions and unrelated staged and unstaged changes. Apply a reviewed newer release and compare the preserved material and history before and after.

**Acceptance Scenarios**:

1. **Given** a compatible book with an unchanged reviewed checkpoint, **When** the writer explicitly applies the selected release, **Then** its framework resources and installation identity are updated together, and completion names the verified installed release and a dedicated, reviewable update commit.
2. **Given** manuscript content, exact saved conversations, canon, proposals, unresolved decisions, settings, session state and revision history, **When** an update succeeds, **Then** their stored content, identities, references and prior history are preserved without reinterpretation, acceptance or new creative decisions.
3. **Given** custom instructions and unrelated staged and unstaged work, **When** an update succeeds, **Then** custom content and existing staging choices are preserved and unrelated work is excluded from the update commit.
4. **Given** the release listing changes after preview, **When** the writer applies the reviewed release, **Then** the workflow uses that exact release or refuses with an explanation; it never silently switches targets.
5. **Given** the book changes after preview, **When** application is attempted, **Then** the stale review is rejected and a fresh preview is required before mutation.
6. **Given** an updated book already at the selected release, **When** the same update is requested again, **Then** it reports the existing state without creating another update commit.

---

### User Story 3 - Understand blockers and recover interrupted updates (Priority: P1)

As a writer, I want conflicts and interruptions to leave my work intact and provide a clear recovery path without pretending the update completed.

**Why this priority**: Updating the runtime and writing instructions is unsafe if failures leave an undisclosed mixture of releases or overwrite work that changed during recovery.

**Independent Test**: Exercise conflicts and inject interruptions before changes, during resource replacement, after commit publication and before cleanup. Inspect and explicitly recover each interrupted operation, checking preserved book material and truthful state reporting.

**Acceptance Scenarios**:

1. **Given** a modified or missing framework-owned file, an unsafe path or a user-owned file occupying a new framework path, **When** preview or pre-application checks run, **Then** affected paths and corrective guidance are reported and application is blocked without overwriting them.
2. **Given** damaged installation evidence, invalid saved records or a release requiring an incompatible story-data migration, **When** evaluated, **Then** the update is refused before installation changes, with the reason and next action disclosed.
3. **Given** an unresolved writing save, cleanup requirement, active writer, retrospective operation or another update, **When** application is attempted, **Then** it does not interfere with that operation; the writer is told what must finish or be recovered first.
4. **Given** an interruption after update changes begin, **When** state is inspected, **Then** inspection is read-only and identifies the intended release, last confirmed checkpoint, incomplete or already-published work and explicit recovery action. Normal writing cannot proceed using an incomplete mixed installation.
5. **Given** unchanged recovery evidence and a confirmed current checkpoint, **When** the writer explicitly retries recovery, **Then** the same selected update completes without replaying story decisions, rewriting history or producing duplicate update commits.
6. **Given** files, checkpoint or recovery evidence changed after interruption, **When** recovery is attempted, **Then** it stops with a conflict and preserves that evidence rather than replacing intervening work or taking over a held lock.
7. **Given** an update commit is published but cleanup or verification remains incomplete, **When** the result is reported, **Then** the published state and remaining work are distinguished; the workflow does not claim ready-to-write completion prematurely.
8. **Given** the updater stops after creating the legacy writer-lock directory but before the durable confirmed ownership checkpoint exists, **When** status or recovery is requested, **Then** it reports unproven ownership, preserves the directory and journal, and refuses automatic takeover, even if an owner file already contains the intended token. No launcher, framework file, index or branch may have changed before that ownership checkpoint.

---

### User Story 4 - Continue an older book with its existing controls (Priority: P2)

As a writer using a book created before update support, I want a documented way to adopt newer framework behavior and continue writing with my existing preferences and permissions.

**Why this priority**: The feature must serve existing books, including 0.2.0 installations with optional contributor retrospectives, rather than only books created by the new updater release.

**Independent Test**: Start from independent books created by 0.1.0 and 0.2.0. Use a controlled newer release to update each, then inspect context, restore the existing session and save a new exchange. Repeat the 0.2.0 cases with disabled, enabled, revoked and interrupted retrospective state.

**Acceptance Scenarios**:

1. **Given** a recognized 0.1.0 or 0.2.0 book lacking updater instructions, **When** the writer follows the documented bootstrap and guided update workflow, **Then** they can update without recreating the book, cloning the framework or manually replacing its resources.
2. **Given** a successfully updated book, **When** the writer follows any required instruction-reload guidance, inspects context, resumes a saved session and saves a new exchange, **Then** the updated book-local framework performs those operations using the preserved book identity, history and session settings.
3. **Given** a book with retrospectives disabled, absent or revoked, **When** updated, **Then** the updater does not enable participation, restore revoked permission or initiate contribution work or publication.
4. **Given** a 0.2.0 book with enabled retrospective participation, **When** updated, **Then** its novel-specific authorization, revocation generation, configured checkout binding and existing access checks are preserved without broadening permission.
5. **Given** interrupted retrospective work or pending notices, **When** an update is evaluated, **Then** their evidence is retained; incompatible outstanding work blocks application until resolved. The updater neither resumes nor publishes contributions, consumes notices nor treats saved inclusion as proof of display.
6. **Given** English or Icelandic book settings and Unicode content or paths, **When** updated and resumed, **Then** content and language settings remain intact and operational guidance respects the existing interaction-language behavior.
7. **Given** a 0.1.0 or 0.2.0 book, **When** its first update is requested, **Then** the workflow requires the writer to close all other book runtimes and confirm that they will remain closed until update or external-controller recovery completes. Existing held locks still block application. Restarted clients must enter through the guarded launcher; direct calls through previously imported legacy modules are outside this bootstrap's supported use.

### Edge Cases

- A newer release appearing between preview and application must not change the selected target.
- Missing or contradictory version, ownership or integrity evidence must not be guessed or repaired implicitly.
- Custom instructions and shared repository rules may coexist with framework defaults; uncertain ownership must not authorize overwriting custom content.
- Files removed by the target release may be removed only when verified as unchanged framework-owned resources; new path collisions must block application.
- Network, download, prerequisite or package-preparation failures must not alter the book installation or history.
- An external operation changing the book while application is underway must not be overwritten; report the conflict and retain recovery evidence.
- A repeated apply or recovery request must not create duplicate update commits or replay story saves.
- An absent retrospective configuration in an older book is not authorization to create an enabled configuration.
- Active contributions, revoked participation, pending notices and uncertain publication outcomes retain their existing authorization and recovery boundaries.
- Checking releases must not upload story content, transcripts, credentials or private book paths.
- Interrupted installation must remain distinguishable from verified completion even if the target version label has already changed.
- A prepared update journal alone does not prove ownership of an empty writer-lock directory. Unproven ownership blocks automatic recovery and cannot authorize deletion or takeover.
- Legacy bootstrap requires closed clients throughout update and interruption recovery. A writer confirmation is an explicit supported-use precondition, not proof that arbitrary legacy processes were discovered or stopped.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Writers MUST be able to explicitly check an existing recognized book for published stable releases. Normal start, resume, save and package installation MUST NOT implicitly check for releases or update pinned book resources. (Story 1.1, 1.5)
- **FR-002**: The workflow MUST default to previewing the latest published stable release, support selection of an exact newer published stable version and report an already-current selection as a no-op. Downgrades, prereleases and source-checkout updates MUST be refused in this first version. (Story 1.1-1.3, 1.6)
- **FR-003**: Preview MUST identify the book's installed release, selected target, proposed framework additions, replacements and removals, compatibility, blockers and next action. Preview MUST leave book files and history unchanged. Failed release discovery MUST NOT be reported as already current. (Story 1.1-1.4)
- **FR-004**: Application MUST require explicit writer initiation and MUST bind to the exact reviewed release and book checkpoint. Changed targets or stale book state MUST require a fresh review rather than silent substitution. (Story 2.1, 2.4-2.5)
- **FR-005**: Updates MUST be limited to identified framework-owned runtime, launcher, schemas, workflows, language resources, integration skills and installation metadata, plus necessary framework rules in shared instruction or repository-rule files. Ownership MUST be verified before replacement or removal; custom content MUST be preserved. Uncertain ownership, local framework edits, missing resources, unsafe paths and new path collisions MUST block conflicting application. (Story 2.3; Story 3.1; ownership and removal edge cases)
- **FR-006**: Manuscript bytes, saved exchange bytes, novel and record identities, references, revisions, creative settings, session state and prior Git history MUST be preserved. Maintenance MUST NOT create canon, reinterpret acceptance, revise creative content or treat update evidence as story authority. (Story 2.2; Story 4.2)
- **FR-007**: Unrelated staged and unstaged changes and their staging choices MUST be preserved. A successful update MUST produce one dedicated reviewable Git commit containing only update-related changes; the workflow MUST NOT reset, amend or push history. Repeated application or recovery MUST NOT duplicate that commit. (Story 2.1, 2.3, 2.6; Story 3.5)
- **FR-008**: The workflow MUST validate recognized book identity, installation integrity, runtime prerequisites and the selected release's compatibility with existing saved records before modifying the installation. Invalid records and incompatible migrations MUST cause refusal without automatic data conversion. Failed release preparation MUST leave the book unchanged. (Story 3.2; preparation edge case)
- **FR-009**: Application MUST exclude concurrent writing, retrospective and update mutations within the supported runtime lifecycle, and MUST refuse unresolved saves, cleanup requirements and incompatible outstanding operations. For initial 0.1.0/0.2.0 bootstrap, the writer MUST close other book runtimes and explicitly confirm they remain closed through application and interruption recovery; restarted clients MUST use the guarded launcher. Confirmation MUST NOT bypass held locks or be presented as process-discovery evidence. Already-imported legacy modules cannot be retroactively guarded and are outside this supported bootstrap lifecycle. The updater MUST preserve held locks and report a finish-or-recover action without silently taking ownership. (Story 3.3, 3.6; Story 4.5, 4.7)
- **FR-010**: An interrupted update MUST retain enough local evidence to identify its original release and checkpoint, changed resources and publication state. Read-only inspection MUST distinguish pending changes, published updates, remaining cleanup and conflicts and MUST provide an explicit next action. Normal writing MUST not use an incomplete mixed installation. (Story 3.4, 3.7)
- **FR-011**: Explicit recovery MUST validate the current checkpoint and original update evidence before continuing the same update. It MUST preserve intervening work, refuse changed or unproven ownership evidence, avoid duplicate commits and never replay story decisions or silently select another release. If interrupted lock acquisition leaves ownership unproven, recovery MUST preserve the lock and journal and report the blocker rather than infer ownership from a prepared journal, token intent, directory age or presumed process death. (Story 3.5-3.6, 3.8)
- **FR-012**: Completion MUST require verification of the installed target and the usability of its book-local framework. The result MUST distinguish verified completion from a published update still requiring cleanup or verification, identify the confirmed checkpoint and provide any instruction-reload guidance. (Story 2.1; Story 3.7; Story 4.2)
- **FR-013**: Recognized books created by 0.1.0 and 0.2.0 MUST have a documented bootstrap path that does not require an already-installed update skill, book recreation, a framework clone or manual replacement of framework files. Installing a newer package alone MUST continue to leave pinned books unchanged. (Story 1.5; Story 4.1)
- **FR-014**: The updater MUST preserve retrospective participation, explicit novel-specific authorization, revocation state, checkout bindings, access-check obligations, existing run/recovery evidence and pending notices. It MUST NOT enable absent or disabled participation, restore revoked permissions, broaden valid permissions, start or resume a retrospective, publish a contribution or consume a notice. Incompatible outstanding work MUST block application until resolved. (Story 4.3-4.5)
- **FR-015**: Update discovery and preparation MUST NOT transmit private story content, conversations, credentials or private book paths to release services. Update authorization MUST NOT authorize contribution publication or changes to credentials, access permissions or global Git configuration. (Privacy edge case; Story 4.3-4.5)
- **FR-016**: The feature MUST provide usable writer-facing check, preview, apply, conflict and recovery guidance through the initial Codex integration and standalone command workflow. Guidance MUST preserve English/Icelandic settings, Unicode content and existing save-before-display boundaries; update results MUST NOT be appended as unsaved creative replies. (Stories 1-4; Story 4.6)
- **FR-017**: Acceptance MUST cover Windows and Linux installation/command workflows, both historical book origins and 0.2.0 retrospective states. Platform command evidence MUST be distinguished from native Codex integration qualification; unavailable verification MUST remain explicitly unverified. (Story 4 independent test and scenarios)

### Key Entities *(include if feature involves data)*

- **Book installation**: The novel identity, pinned framework release, framework-owned resources and evidence distinguishing those resources from writer-owned content.
- **Published release**: An identifiable stable distribution of Novel Creator and its compatibility with an existing book; not an unpublished checkout or an assumed future version number.
- **Update preview**: A review of one book checkpoint against one exact selected release, including proposed changes, compatibility and blockers; grants no creative or contribution authority.
- **Update operation**: The writer-initiated application of the reviewed release, its confirmed checkpoint, publication outcome and verification status.
- **Recovery evidence**: Local information sufficient to inspect and explicitly continue the same interrupted update without overwriting intervening changes or duplicating publication.
- **Existing retrospective state**: Participation, authorization and revocation, checkout binding, unfinished work and notices governed by feature 003; preserved rather than reauthorized by maintenance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All check-only, already-current, unsupported-selection and failed-discovery acceptance cases leave book files and history unchanged and accurately distinguish available, current and unknown status.
- **SC-002**: Every successful-update acceptance case installs exactly the reviewed release and produces exactly one reviewable update commit, including repeated application and recovery requests.
- **SC-003**: Across successful and interrupted updates, all seeded manuscript content, saved exchanges, record identities, references, settings, prior history and unrelated staged/unstaged changes retain their required before-update values and staging choices.
- **SC-004**: Every tested unsafe-path, ownership conflict (including interruption before durable fence ownership), incompatible-record, stale-checkpoint, held-lock and unresolved-operation case blocks conflicting application without overwriting protected work. The interrupted-ownership case leaves the launcher, framework files, index and HEAD at their pre-application values and never auto-removes the ambiguous lock.
- **SC-005**: Each tested interruption before replacement, during replacement, after update publication and before cleanup has an accurate read-only status and explicit recovery outcome: exact-operation continuation when ownership/evidence is verified, or a preserved-evidence blocker when it is unproven. Within the supported lifecycle in FR-009, no case permits normal writing on an incomplete mixed installation or creates duplicate update commits. Legacy-client tests MUST separately show guarded fresh launches and the unsupported already-imported-client case; confirmation alone is not successful exclusion evidence.
- **SC-006**: Books originating from both 0.1.0 and 0.2.0 can follow the documented update path to a controlled compatible newer release, inspect preserved context, resume an existing session and save a valid new exchange.
- **SC-007**: Disabled, absent and revoked retrospective acceptance cases yield zero new authorization or contribution actions. Enabled and interrupted cases preserve existing permissions, bindings, run evidence and notices without broadening authority or consuming pending notices.
- **SC-008**: All seeded private story passages, transcripts, credentials and private book paths are absent from outgoing release-service requests.
- **SC-009**: Windows and Linux command acceptance cases and English/Icelandic preservation cases record explicit outcomes, with native-host qualification reported separately and no unsupported platform success claims.

## Assumptions

- The current source baseline is Novel Creator 0.2.0. Compatibility fixtures include books created by 0.1.0 and 0.2.0; controlled newer release fixtures establish upgrade behavior without reserving or claiming a real future release number.
- Published stable package releases are the only update source in this slice. Release discovery requires network access; lack of access is a disclosed limitation, not evidence of no update.
- A single guided workflow supports explicit check, preview and application, through Codex or standalone commands. Installing updater-capable tooling is the bootstrap for older books; it does not update a book by itself.
- Existing single-user, independent-repository and configured runtime prerequisites remain applicable. Shared update behavior and portable book data remain independent of an AI provider and require no dashboard or model credentials.
- Initial legacy bootstrap requires closed book sessions until external update/recovery completes, followed by instruction/runtime reload through the guarded launcher. This lifecycle condition is disclosed before application; it does not promise to stop or retrofit arbitrary in-memory legacy code.
- This feature extends the explicit existing-bundle update boundary deferred by features 002 and 003. Their prohibitions on implicit upgrades and implicit retrospective opt-in remain in force; their historical scope statements are not rewritten.
- Constitution principles I, II, III, IV, VI, VII, VIII, IX and XI govern simplicity, integration separation, creative authority, provenance, portability, language preservation, verification and usable documentation. No constitutional deviation is proposed. Dashboard-specific work remains outside this slice.
- Exact commands, public interfaces, package preparation, ownership metadata and transaction/recovery architecture belong to subsequent Spec Kit planning, not this specification.
- Downgrades, prereleases, source-checkout updates, incompatible story-data migrations, automatic checks, package publication and contribution publication are outside this feature's update authorization. No timing targets or novice-testing gates are introduced.
- Windows and Linux installation/command verification is required. Existing Linux Codex integration limitations remain unverified until independently qualified; this specification grants no release-readiness claim.
