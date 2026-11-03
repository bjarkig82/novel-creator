# Feature Specification: Package Installation and Simple Novel Initialization

**Feature Branch**: No feature branch created; specification prepared on `main`.

**Created**: 2026-10-29

**Status**: Draft

**Input**: User description: "I would like to create a simpler way to initialize a novel project using the novel creator. Perhaps something similar to what SpecKit and BMad, install a package and run a script that will set things up for you (e.g. 'NovelCreator init <novel name> -- <some optional flags>')"

## Clarifications

### Session 2026-10-29

- Q: How should writers obtain Novel Creator when this feature is delivered? → A: Install a published package by name using a standard package tool.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install and Start a Novel (Priority: P1)

As a writer, I want to install Novel Creator as a package and initialize a named novel with one command, so I can start without a framework checkout, developer setup, or a manually prepared configuration file.

**Why this priority**: Removes the setup work between obtaining Novel Creator and opening an independent novel.

**Independent Test**: Follow the installation instructions without the framework checkout, initialize using only a name, then open the resulting folder in Codex and invoke its installed setup workflow.

**Acceptance Scenarios**:

1. **Given** a supported environment with documented prerequisites and no framework checkout, **When** the writer follows instructions to install the publicly published package by name using a standard package tool, **Then** the initialization command and help are available without editing source files, building a local package, or configuring a framework source path.
2. **Given** an installed package and writable parent outside existing repositories, **When** the writer initializes with only a novel name, **Then** a child folder with that name contains an independent Git-backed novel, its required local resources, and Codex workflow entries; no brief file or creative questionnaire is required.
3. **Given** successful initialization, **When** the writer reads completion output, **Then** it identifies the created folder and explains how to open it in Codex and start conversational setup; initialization ends without starting brainstorming or calling a provider.
4. **Given** the initialized novel and documented runtime prerequisites, **When** the framework checkout is unavailable, **Then** installed setup, inspection, brainstorming, and resume workflows remain usable from the novel folder.
5. **Given** a missing prerequisite or unavailable package source, **When** installation or initialization is attempted, **Then** instructions or diagnostics identify the failed step and corrective action, without claiming a ready novel.

---

### User Story 2 - Supply Optional Setup Choices (Priority: P2)

As a writer, I want to supply a destination, working title, or manuscript language, so I can choose common settings without a separate brief and leave other creative choices for later.

**Why this priority**: Optional choices accommodate normal writing environments while keeping the default command short.

**Independent Test**: Initialize disposable novels with default settings and explicit destination, title, and language choices; compare saved projects with supplied values.

**Acceptance Scenarios**:

1. **Given** a valid novel name and explicit destination, **When** initialization succeeds, **Then** the novel is created at that destination and output identifies its resolved location.
2. **Given** a name without a separate title, **When** initialization succeeds, **Then** the name becomes the initial working title without establishing story facts.
3. **Given** a working title distinct from the folder name and Icelandic manuscript language, **When** initialization succeeds, **Then** title and language are saved exactly, including Icelandic characters, and folder location follows the destination choice.
4. **Given** omitted creative settings, **When** initialization completes, **Then** the existing English language default applies, other unspecified creative choices remain unknown, and later conversational setup accepts skipped answers.
5. **Given** help or an unsupported option or language value, **When** the command runs, **Then** it lists supported usage or explains the invalid value, respectively, without creating or changing a novel.

---

### User Story 3 - Preserve Existing Work and Recover Safely (Priority: P1)

As a writer, I want initialization to recognize existing work and explain failures, so trying or repeating the simpler command cannot replace my novel or unrelated files.

**Why this priority**: Convenience must retain existing initialization and creative-authority safeguards.

**Independent Test**: Exercise recognized novels, occupied folders, nested repositories, missing Git identity, and interrupted initialization in disposable locations; compare existing files and history before and after.

**Acceptance Scenarios**:

1. **Given** an existing recognized novel, **When** initialization is repeated there, **Then** it preserves identity, records, history, settings, and installed resources, reports the existing novel, and gives continuation instructions without applying replacement setup choices.
2. **Given** unrelated content or a destination inside or containing an unrelated repository, **When** initialization is attempted, **Then** it refuses, explains how to choose a safe destination, and leaves existing content and history unchanged.
3. **Given** interrupted initialization, **When** the writer follows recovery instructions with the original choices, **Then** it completes the same initialization once or reports a conflict; changed choices or conflicting files never silently replace original work.
4. **Given** missing Git identity or insufficient filesystem access, **When** initialization is attempted, **Then** it explains the problem without inventing identity, changing global settings, bypassing permissions, or claiming completion.
5. **Given** a caller using the existing explicit-path and brief-file interface, **When** it initializes a novel, **Then** existing behavior remains supported, including original-input provenance and recovery protections.

---

### User Story 4 - Follow a Complete Getting-Started Guide (Priority: P1)

As a writer new to Novel Creator, I want an easy-to-find guide that takes me from prerequisites to my first saved conversation and returning later, so I know what to do after installing and can recognize when each step has worked.

**Why this priority**: A shorter initialization command needs equally clear guidance through the first useful writing interaction.

**Independent Test**: Starting from the README, follow the guide in each supported environment using an installed package and disposable novel. Confirm setup, one saved conversation, inspection, and resumption using only the guide and its linked references.

**Acceptance Scenarios**:

1. **Given** a writer arriving at the README, **When** they follow its getting-started link, **Then** they reach a writer-facing guide with prerequisites, supported environments, installation and verification, a minimal initialization example, and expected results, without needing developer instructions.
2. **Given** a newly initialized novel, **When** the writer follows the guide, **Then** they can open the correct folder in Codex, invoke conversational setup, use an example request with no story idea, and identify confirmation that their first exchange was saved.
3. **Given** a saved first session, **When** the writer follows the next-steps instructions, **Then** they can inspect saved state and return to that novel with its resume workflow without reinitializing it.
4. **Given** a writer choosing a different destination, working title, or Icelandic manuscript language, **When** they consult the optional-settings reference, **Then** examples explain the choices, defaults, and shell-appropriate quoting without making those choices mandatory for the minimal path.
5. **Given** command-not-found, missing prerequisite or Git identity, unsafe destination, permission failure, or interrupted initialization, **When** the writer follows the troubleshooting entry, **Then** they can identify the relevant diagnostic and a safe corrective or recovery action that preserves existing work.

### Edge Cases

- Names and paths containing spaces or Icelandic characters retain supplied text; platform-invalid names fail with actionable guidance before project creation.
- Names implying parent traversal or multiple path components are rejected; explicit destination selection controls location instead.
- An existing empty destination is accepted when it meets normal independence and access checks.
- Filesystem aliases are checked by resolved location and cannot bypass repository or overwrite protections.
- A destination conflicting with a file, unwritable parent, missing dependency, or failed initial save produces a failure diagnostic identifying partial work needing recovery.
- Help and invalid or contradictory arguments leave the filesystem unchanged. Combining the new shorthand with the legacy brief-file form is rejected with guidance to choose one form.
- Reinstalling the package never silently upgrades installed resources or changes story data in existing novels.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Delivery MUST include a publicly published, versioned package that writers can install by name using a standard package tool, without cloning the framework, editing source, building a local package, or using a development-only installation. A local build or downloadable release file alone MUST NOT satisfy this delivery requirement. Instructions MUST state the package name, installation command, prerequisites, supported environments, and how to verify command availability. (Story 1.1, 1.5)
- **FR-002**: Initialization MUST accept a novel name as its only required setup input and create a ready novel without a user-authored brief or configuration file. (Story 1.2)
- **FR-003**: The default destination MUST be a child folder named after the novel under the current directory. Writers MUST be able to select an explicit destination instead; every destination MUST satisfy existing independence and safety rules. (Story 1.2, 2.1, 3.2)
- **FR-004**: Initialization MUST create an independent novel Git repository with local resources and Codex entries for setup, brainstorming, inspection, and resumption. Subsequent use MUST NOT require the framework checkout. (Story 1.2, 1.4)
- **FR-005**: Working title and manuscript language MUST be optional command inputs. The name MUST supply the working title when no separate title is given. Omitted language MUST retain the existing English default; English and Icelandic MUST be supported. (Story 2.2-2.4)
- **FR-006**: Supplied names, titles, and language choices MUST be preserved without translation or invented creative interpretation, with traceable input origins and no fabricated conversation. A working title MUST NOT establish story canon; other unspecified creative choices MUST remain unknown. (Story 2.2-2.4)
- **FR-007**: Initialization MUST finish without creative questions, story generation, brainstorming, model credentials, or AI provider calls. Conversational setup MUST remain a separate next action. (Story 1.2-1.3)
- **FR-008**: Help MUST explain the name-only form, destination/title/language choices, defaults, prerequisites, and examples for supported shells. Invalid names, values, unknown options, and conflicting forms MUST produce actionable diagnostics before novel writes. (Story 2.5; edge cases)
- **FR-009**: Success MUST be reported only after initial project save is confirmed and required resources are present. Output MUST identify the resolved location and concrete instructions to open the novel in Codex and invoke setup. (Story 1.2-1.3)
- **FR-010**: Repeated initialization MUST preserve a recognized novel's identity, settings, history, records, and resources and provide continuation guidance. It MUST NOT apply replacement settings or silently upgrade the novel. (Story 3.1; edge cases)
- **FR-011**: Initialization MUST retain protections against occupied unrelated destinations, nested repositories, alias bypasses, and writes outside the selected destination. It MUST NOT overwrite unrelated instructions or files, alter global configuration, invent Git identity, or push remotely. (Story 3.2, 3.4; edge cases)
- **FR-012**: Missing prerequisites, access failures, and partial initialization MUST have distinct failure outcomes, corrective guidance, and disclosure of partial state. Recovery MUST retain original inputs and identity, disclose conflicts, and avoid duplicate initialization or destructive cleanup. (Story 1.5, 3.3-3.4)
- **FR-013**: The existing explicit-path and brief-file interface MUST remain supported. The simpler form MUST preserve the same independent-project, provenance, save, and recovery guarantees. (Story 3.5)
- **FR-014**: Installation and initialization instructions MUST cover Windows PowerShell and Linux Bash and identify unsupported environments. Examples MUST be verified using an installed package outside the framework checkout. (Story 1.1-1.4)
- **FR-015**: A writer-facing getting-started guide MUST be directly linked from the README and referenced by command help and successful initialization output. It MUST present one clearly marked minimal path from prerequisites and installation through initialization, opening the novel in Codex, conversational setup, and a first saved exchange, with expected results at each stage. (Story 4.1-4.2)
- For FR-010/FR-015 compatibility, continuation of an older novel without a pinned guide MUST reference the verified installed-package guide with a clear fallback label, without changing the novel's files, manifest or history. Readiness MUST use that novel's existing resource manifest; a newer guide MUST NOT become an implicit upgrade prerequisite. Verification MUST include a pre-feature novel lacking the guide and unchanged before/after state.
- **FR-016**: The guide MUST include copyable, shell-appropriate examples for Windows PowerShell and Linux Bash, explain where to run commands and which values to replace, and show how to begin without a story idea. Optional destination, title, and English/Icelandic choices MUST be documented separately from the minimal path, with defaults and quoting examples. (Story 4.1-4.2, 4.4)
- **FR-017**: Getting-started documentation MUST explain how to recognize saved state, inspect the novel, and resume later without reinitializing. It MUST distinguish local initialization from the Codex conversation and explain which creative choices can remain unknown. (Story 4.2-4.3)
- **FR-018**: The guide MUST include troubleshooting for unavailable commands, missing prerequisites and Git identity, unsafe destinations, insufficient permissions, and interrupted initialization, linking to existing safe recovery instructions where appropriate. It MUST explain current support limits and reconcile existing quickstarts so writers are not directed to conflicting or obsolete setup steps. (Story 4.5)

### Key Entities *(include if feature involves data)*

- **Installable Release**: A publicly published, versioned package installable by name using a standard package tool, containing resources for independent novels and declaring prerequisites and supported environments.
- **Initialization Request**: Supplied name, destination selection, optional title/language, and their recorded origins; original choices remain identifiable during recovery.
- **Novel Project**: An independent repository with stable identity, settings, local workflows, and history. Folder name and working title may differ.
- **Initialization Outcome**: A confirmed ready project, recognized existing project, or failed/partial attempt, with location and continuation or recovery guidance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On both supported environments, installation of the publicly published package by name followed by one name-only initialization command produces a novel that can enter conversational setup without a framework checkout, local package build, manually authored configuration, or extra setup questions. Every case in this two-environment matrix succeeds; local-artifact checks alone do not establish completion.
- **SC-002**: Default, explicit-destination, separate-title, English, Icelandic, and spaces/Unicode acceptance cases preserve 100% of supplied settings and leave every unspecified creative choice unresolved, apart from documented working-title and language defaults.
- **SC-003**: Across existing-novel, unrelated-content, nested-repository, alias, and invalid-argument cases, 100% of pre-existing files and history remain unchanged and every unsafe attempt reports an actionable outcome.
- **SC-004**: Every interruption/retry acceptance case either produces exactly one saved novel with original identity and choices or reports a recoverable conflict; zero cases report readiness with missing required resources or an unconfirmed save.
- **SC-005**: In an automated walkthrough on each supported environment, completion instructions lead to invoking the installed setup workflow without an undocumented step. The owner can use those instructions afterward; human usability approval is recorded separately when available.
- **SC-006**: Every existing explicit-path/brief-file compatibility case retains its prior initialization, provenance, refusal, and recovery outcomes.
- **SC-007**: On both supported environments, every step of the documented minimal journey from installation through a first saved exchange, inspection, and resumption succeeds using only the guide and its linked references, with zero undocumented prerequisites or commands. Each step's stated result matches observed behavior; automated command evidence and agent-operated host evidence are labeled separately from human usability approval.
- **SC-008**: The README, command help, and initialization completion output each provide a working route to the guide. Every documented optional-setting example and each of the six troubleshooting categories in Story 4.5 is checked against the delivered behavior, with no conflicting setup instructions in the linked quickstarts.

## Assumptions

- This simplifies obtaining and starting the current single-user product. Drafting, dashboards, additional AI hosts, synchronization, project upgrades, and migrations remain outside scope.
- The illustrative `NovelCreator init <novel name>` expresses the desired command shape. Exact executable spelling, option spelling, public package service, distribution tooling, and any argument separator are planning decisions. Public package publication and installation by name are required delivery outcomes; the specific service remains unselected. The required user experience is package installation followed by one name-only initialization command.
- Windows PowerShell and Linux Bash retain existing platform scope; macOS remains deferred. Runtime prerequisites and Git identity may need prior configuration; initialization explains these rather than silently provisioning the machine.
- Obtaining the package and dependencies may require network access. After installation, initialization requires neither network nor provider account. Codex remains the initial creative-workflow host.
- Existing initialization, record contracts, installed-resource behavior, and recovery are dependencies to reuse. Existing novels retain pinned resources; there is no automatic upgrade.
- The novel name provides a provisional title when no separate title is supplied. Other creative choices can wait for existing conversational setup.
- Automated installation and workflow acceptance provide delivery evidence. This feature does not reintroduce retired latency targets or mandatory novice/manual evaluation gates. Subjective ease of use remains a separate owner assessment.
- Getting-started documentation is a required feature deliverable. It describes verified delivered commands when implemented; the specification does not claim that the proposed simplified commands already exist. Existing developer and POC documentation may remain as clearly labeled references, with the writer-facing starting route made unambiguous.


## Owner-approved release scope amendment — 2026-10-29

The owner explicitly selected: "Amend to Windows Codex + Linux CLI" after learning that no Linux Codex host is connected and the WSL Codex launcher is unavailable. This supersedes the Linux Codex-host portion of US1/AC4, US4/AC2–AC3, SC-001, SC-005 and SC-007 and corresponding references in the plan/tasks. Windows Codex Desktop must complete actual setup, exact first-save/display, inspection and resume. Windows PowerShell and Linux Bash must both pass installation, initialization, settings/provenance, guide/discovery, safety/troubleshooting and public named-install/hash checks. Linux Codex integration remains explicitly unverified and is not a release gate for 0.1.0. No command, provenance, recovery or creative-authority safeguard is waived; fixtures do not become host or human evidence. Public package delivery remains required.
