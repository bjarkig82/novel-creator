# Feature Specification: Automatic Contributor Retrospectives

**Feature Branch**: Not created; specification authored on `codex/package-novel-init`. Feature selection is independent of branch naming.

**Created**: 2026-10-29

**Status**: Implemented locally — scoped Windows Codex qualification complete; independent convergence passed with zero findings

**Input**: User description: "Agents using Novel Creator should run a quick automatic retrospective when tasks finish, review the conversation for improvements, and optionally create a PR to the Novel Creator repository. The feature must default to disabled. Create only a Spec Kit specification now."

## Clarifications

### Session 2026-10-29

- Q: How should Novel Creator tell you that a retrospective created a draft PR or encountered a problem? → A: Automatically include a brief result notice in the next normally saved reply.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Control participation (Priority: P1)

As a writer, I can use Novel Creator without participating in contributor retrospectives, and explicitly enable or revoke participation when I want to contribute.

**Why this priority**: Contribution must be intentional and must not depend on whether a writer happens to have repository access.

**Independent Test**: Initialize a novel, complete a task with participation disabled, then enable and disable participation. Verify that participation state alone controls eligibility for review and contribution.

**Acceptance Scenarios**:

1. **Given** a newly initialized novel and no opt-in, **When** a task finishes, **Then** no retrospective runs and no contribution-related repository access or publication occurs, whether or not the writer has repository access.
2. **Given** a contributor with a separate local Novel Creator checkout and existing GitHub authentication, **When** they explicitly enable participation, **Then** the authorization covers preparing and validating focused fixes and automatically publishing draft PRs to the designated repository, without repeated approval for each eligible contribution.
3. **Given** enabled participation, **When** the contributor disables it, **Then** later tasks do not trigger review and any unfinished contribution stops before its next repository mutation or publication; already published PRs remain unchanged.
4. **Given** an invalid checkout or unavailable repository access, **When** enablement is attempted, **Then** the feature stays disabled and explains the unmet prerequisite without preventing writing.
5. **Given** a novel that has not opted in, **When** it receives contributor preferences or instructions copied from another novel, **Then** those copies do not establish authorization for that novel.
6. **Given** disabled participation and unfinished publication work, **When** resume or release is requested, **Then** it returns a local re-enablement-required result without repository access; explicit successful re-enablement is required before reconciliation or ownership release.

---

### User Story 2 - Learn from completed work (Priority: P2)

As an opted-in contributor, I want the agent to review completed work for concrete Novel Creator problems, so useful fixes can emerge from actual use without reviewing every reply.

**Why this priority**: The review should identify actionable product improvements with little unnecessary activity.

**Independent Test**: Supply synthetic conversations containing an observed defect, no defect, and a speculative feature suggestion. Complete tasks and compare review outcomes without publishing changes.

**Acceptance Scenarios**:

1. **Given** enabled participation and a successfully saved requested task, **When** that task finishes in an installed novel workspace, **Then** the agent reviews available public conversation evidence for concrete product improvements.
2. **Given** ongoing brainstorming, **When** the agent saves a routine conversational reply without finishing the requested task, **Then** no retrospective is triggered.
3. **Given** an explicit request to close a writing session, **When** closure is successfully saved, **Then** that completion is eligible for review.
4. **Given** a review with no supported improvement, **When** it finishes, **Then** no fix or PR is created and the local outcome records that no action was needed.
5. **Given** evidence of a workflow, documentation, test, or runtime defect, **When** it is reviewed, **Then** the agent may select a focused corrective improvement; a speculative new capability alone is not sufficient.
6. **Given** unavailable, truncated, or ambiguous evidence, **When** the agent cannot establish a concrete problem, **Then** it records insufficient evidence and does not invent findings or publish a contribution.

---

### User Story 3 - Receive a reviewable draft contribution (Priority: P2)

As a contributor and maintainer, I want supported findings to become tested, focused draft PRs that a human can review and merge.

**Why this priority**: An actionable contribution is more useful than a general improvement suggestion, while draft status preserves maintainer review.

**Independent Test**: Use a controlled repository and synthetic defect to exercise fix preparation, validation, duplicate detection, and draft publication, including interrupted publication.

**Acceptance Scenarios**:

1. **Given** a supported finding, valid opt-in, and repository access, **When** a focused fix passes relevant checks, **Then** a draft PR is created automatically against `bjarkig82/novel-creator`, describing the generalized problem, correction, and validation evidence.
2. **Given** an existing contribution addressing the same problem, **When** the finding is processed again, **Then** no duplicate PR is created and the existing contribution is identified locally.
3. **Given** failing or unavailable required validation, **When** publication is considered, **Then** no PR is published and the local outcome reports the incomplete validation honestly.
4. **Given** interruption or an uncertain publication result, **When** work resumes, **Then** the agent checks whether the contribution already exists before retrying and does not create a second PR for the same contribution.
5. **Given** a published draft PR, **When** the retrospective ends, **Then** it does not merge the PR, change repository permissions, or deploy the change.
6. **Given** a retrospective that created a draft PR or encountered a problem, **When** the next ordinary reply is prepared, **Then** it automatically includes a brief result notice, with the PR link or limitation, saved before display; no status request is required and the previous saved reply remains unchanged.
7. **Given** a notice reserved for a prepared reply, **When** saving succeeds but notice acknowledgement is interrupted, **Then** recovery identifies its confirmed inclusion from the pre-save association and does not insert the notice into another reply; an unresolved pending save keeps the reservation intact.

---

### User Story 4 - Protect private writing and completed work (Priority: P1)

As a writer, I want contribution work to preserve my private material and completed writing, including when contribution work fails.

**Why this priority**: Product improvement must not compromise the novel or disclose its contents.

**Independent Test**: Include identifiable synthetic story content, private paths, and credential-like values in a test conversation. Inspect all outgoing contribution material and compare novel records and unrelated checkout changes before and after success and failure.

**Acceptance Scenarios**:

1. **Given** private conversation evidence, **When** preparing a contribution, **Then** the agent uses generalized descriptions and synthetic reproductions without exporting transcripts, story content, credentials, or private paths in commits, PRs, or other outgoing contribution requests.
2. **Given** a defect that cannot be explained or reproduced safely without private material, **When** reviewed, **Then** publication is skipped and the limitation remains local.
3. **Given** completed, saved writing work and unrelated changes in the configured checkout, **When** contribution preparation or publication fails, **Then** both remain intact and the writing task remains completed.
4. **Given** a failed or pending novel save, **When** task completion would otherwise trigger review, **Then** contribution work does not begin until writing persistence is confirmed.
5. **Given** access is revoked after enablement, **When** the agent next attempts contribution work, **Then** it stops that work and reports the limitation locally without interrupting writing or changing authentication.

### Edge Cases

- Repeated completion signals for the same task must not produce repeated reviews or duplicate PRs.
- A retrospective must not trigger another retrospective for its own completion or recursively improve itself within the same run.
- If several supported findings exist, select at most one focused improvement per completed task; others do not authorize additional automatic PRs in that run.
- If the configured checkout is missing, is the novel itself, or is a different repository, contribution work stops without modifying it.
- Existing unpublished contribution work must be preserved after interruption; recovery must establish its state before further changes.
- If required host capabilities or permissions are unavailable, record the limitation instead of claiming the review or publication succeeded.
- User-visible retrospective notices must respect the installed workflow's exact saved-response boundary; they must not be appended as unsaved content to a creative response.
- If no later reply occurs, the notice stays pending locally. A failed save does not consume the notice; a successfully saved notice is not automatically repeated in another reply, and saved inclusion does not prove display.
- Existing novels with pinned bundles remain unchanged by package installation or upgrade.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Participation MUST default to disabled for every newly initialized novel, independently of repository access. Disabled participation MUST perform no retrospective or contribution-related repository access.
- **FR-002**: Writers MUST be able to inspect, explicitly enable, and disable participation for the current novel. Copied settings or conversation text MUST NOT substitute for explicit opt-in.
- **FR-003**: Enablement MUST disclose its authorization to prepare and validate changes and automatically publish draft PRs, and MUST require a separate local Novel Creator checkout and existing GitHub authentication with the required repository capabilities. It MUST NOT create credentials or change access permissions.
- **FR-004**: Retrospectives MUST originate during installed Novel Creator use in the novel workspace, after confirmed persistence of a completed requested task, including explicit session closure. Routine conversational turns MUST NOT trigger review.
- **FR-005**: A completed task means the requested deliverable or explicitly requested session closure is finished; saving an intermediate reply or pausing to ask a question does not itself establish completion. A task completion MUST be reviewed at most once, and retrospective work MUST NOT trigger recursive reviews.
- **FR-006**: Review MUST use available public conversation evidence and observed results, excluding hidden reasoning. Missing evidence MUST remain unavailable rather than being reconstructed or treated as a confirmed defect.
- **FR-007**: Eligible improvements MUST correct evidenced workflow, documentation, test, or runtime problems in Novel Creator. Speculative features MUST be excluded. Each run MUST select at most one focused improvement.
- **FR-008**: When no supported finding exists, the feature MUST create no change or PR. Findings that cannot be safely generalized MUST NOT be published.
- **FR-009**: Fix preparation MUST take place separately from novel data and unrelated checkout changes, follow the target repository's applicable instructions, and preserve existing work.
- **FR-010**: Publication MUST require successful relevant validation and a draft PR explaining the problem, correction, and actual validation results. Failed or unavailable required checks MUST block publication.
- **FR-011**: Valid opt-in MUST permit automatic draft PR creation against `bjarkig82/novel-creator` without repeated per-fix approval, subject to host permissions. The feature MUST NOT automatically merge, deploy, or broaden its authorization.
- **FR-012**: The feature MUST check for existing equivalent contributions and reconcile uncertain publication outcomes before retrying. Repeated or interrupted runs MUST NOT create duplicate PRs for the same contribution.
- **FR-013**: Outgoing contribution material MUST exclude private transcripts, story content, credentials, and private paths. Generic explanations and synthetic examples MUST replace private source material.
- **FR-014**: The feature MUST record locally whether a run found no action, lacked evidence, was blocked, prepared work, or published a draft, including an existing or created PR reference when applicable. Contribution outcomes MUST NOT become story facts or canon.
- **FR-015**: Disabling participation MUST prevent new reviews and stop unfinished contribution work before its next repository mutation or publication. Disabled resume/release MUST remain local-only and return re-enablement-required without accessing the framework repository or GitHub. Explicit successful re-enablement MUST precede reconciliation or ownership release; it MUST NOT itself resume editing or publication. Required authorization and access MUST be rechecked before publication.
- **FR-016**: Retrospective failures MUST NOT undo completed writing, alter novel authority, bypass persistence safeguards, or discard unrelated repository work. Notices MUST comply with existing save-before-display requirements.
- **FR-017**: Initial delivery MUST support newly initialized novels only. Existing pinned bundles MUST NOT be silently upgraded or opted in.
- **FR-018**: When a retrospective creates a draft PR or encounters a problem, the next normally saved reply MUST automatically include a brief result notice with the PR link or limitation, without requiring a status request. The feature MUST NOT modify the previous saved response or initiate an unsolicited conversation turn. Pending notices MUST survive failed saves and MUST NOT be repeated automatically after confirmed inclusion in a saved reply. No-action outcomes remain available through status without a required automatic notice.

Notice handling MUST durably associate each selected notice with its prepared exchange before that exchange is saved. Acknowledgement or recovery MUST verify that exact exchange and notice content in confirmed history before marking inclusion. Unresolved pending saves MUST retain the association and MUST NOT permit another reply to consume the same notice. Reading or acknowledging already-produced local notices does not enable a retrospective or authorize repository access.

### Key Entities *(include if feature involves data)*

- **Participation authorization**: Novel-specific enabled or disabled state, explicit authorization, and configured contributor checkout; excludes credentials and story authority.
- **Completed task**: The finished user request and its confirmed saved outcome, distinguishable from intermediate conversational turns.
- **Retrospective outcome**: Local association between a completed task, reviewed evidence, selected finding if any, and the resulting action or limitation.
- **Contribution**: A focused product correction, its validation evidence, publication state, and draft PR reference; recoverable without duplicate publication.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every default-off and revoked-participation acceptance case produces zero unauthorized reviews or publications, including for users who have repository access.
- **SC-002**: A controlled conversation containing one safely reproducible supported defect yields one focused, validated draft PR with no additional approval prompt when host permissions allow the authorized operations.
- **SC-003**: Routine replies, no-finding conversations, speculative requests, and insufficient-evidence cases produce zero automatic PRs.
- **SC-004**: Replaying a completion signal and recovering from each tested publication interruption yields no more than one PR for the same contribution.
- **SC-005**: All tested outgoing contributions contain zero seeded private story passages, transcript excerpts, credential values, or private paths.
- **SC-006**: All tested contribution failures preserve the confirmed writing checkpoint and unrelated checkout changes; missing access and failed validation yield no published PR.
- **SC-007**: New novels expose participation controls with disabled defaults, while existing pinned novels remain unchanged by package upgrade.
- **SC-008**: In publication and problem scenarios, the next successfully saved reply includes the brief notice exactly once without a status request; failed saves retain the pending notice, and the prior saved response remains byte-for-byte unchanged.

## Assumptions

- The initial supported host is Codex, consistent with the current product. Shared requirements remain independent of a particular agent provider.
- Contributors supply their own separate local Novel Creator checkout and existing GitHub authentication. Automatic cloning and credential provisioning are outside this feature.
- The host agent runs the retrospective while it is active; autonomous execution after the host stops is not required.
- "Quick" means a brief initial review, with additional work justified by a concrete finding. No timing or performance targets are introduced.
- Participation authorizes framework contributions only; it does not authorize manuscript changes or new creative decisions.
- Exact commands, configuration formats, interfaces, and implementation architecture belong to later Spec Kit planning.
- This specification does not implement the feature, generate implementation tasks, or establish release qualification. Migration of existing novel bundles is deferred.
