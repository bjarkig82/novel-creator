<!--
Sync Impact Report
Version change: unratified scaffold -> 1.0.0 (initial adoption)
Modified principles: generic placeholders replaced by the eleven principles below.
Added principles:
  I. Simplicity and Pragmatism
  II. Agent and Platform Independence
  III. Human Creative Authority, AI Execution
  IV. Story Consistency and Traceability
  V. Guided Creative Collaboration
  VI. Structured, Portable, Version-Controlled Data
  VII. Genre and Language Independence
  VIII. Separation of Responsibilities
  IX. Quality Through Verification
  X. Mobile-First, Accessible User Experience
  XI. Incremental Delivery and Maintainability
Added sections: Scope and Architectural Boundaries; Development Workflow and Quality Gates;
  project-specific Governance.
Removed sections: none; unfilled scaffold examples replaced.
Dependent templates and commands: unchanged; they read the constitution at runtime.
Follow-up TODOs and deferred intents: none.
-->

# Novel Creator Constitution

## Core Principles

### I. Simplicity and Pragmatism

Design and implementation MUST follow KISS, DRY, and YAGNI: choose the simplest maintainable
solution that satisfies an established requirement, avoid unnecessary duplication, and defer
speculative functionality. New abstractions, dependencies, infrastructure, and orchestration MUST
have a documented concrete requirement and an explanation of why existing proven capabilities
are insufficient. Development MUST proceed incrementally and deliver usable functionality early.
This keeps maintenance costs proportional to demonstrated needs.

### II. Agent and Platform Independence

The framework MUST NOT require a single AI provider for its platform-independent workflows or
story data. Codex MUST be the initial supported platform; integration boundaries MUST permit
future support for Claude Code, GitHub Copilot, and other platforms without redefining core
workflows or making novel data inaccessible. Platform-specific skills, instructions, commands,
and subagents MUST remain separate from shared workflow definitions. Integrations MUST use native
platform capabilities where they satisfy requirements. A custom AI runtime MUST NOT be introduced
unless an established requirement cannot be met by existing platforms and that gap is documented.
Extensibility does not require implementing every adapter in the first release.

### III. Human Creative Authority, AI Execution

The software MUST preserve the human's role as creative director while enabling AI agents to
perform most planning, writing, analysis, and revision work. Workflows MUST respect explicit
creative decisions and minimize intervention within configured autonomy boundaries. They MUST
provide configurable review checkpoints and MUST require human authorization for significant
changes to already approved manuscript content. Each workflow that changes approved content MUST
define significance criteria and its authorization boundary before autonomous execution.

Clearly accepted brainstorming decisions MUST automatically become established canon, with their
acceptance recorded. Suggestions, silence, and unresolved alternatives MUST NOT be treated as
acceptance. Establishing canon MUST NOT bypass authorization for significant revisions to approved
manuscript text. When an accepted decision conflicts with an explicit creative direction or
protected approved content, the system MUST surface the conflict and request clarification before
making the conflicting change. These controls preserve creative authority without requiring
repeated approval of routine work already within the user's authorization.

### IV. Story Consistency and Traceability

Narrative consistency MUST be a core software capability. Data models and workflows MUST distinguish
established canon from proposals, alternatives, and unresolved ideas, and MUST detect and surface
significant contradictions as early as relevant information is available, including during
brainstorming. They MUST distinguish objective story facts from character knowledge, character
beliefs, and reader knowledge rather than collapsing these into one factual state.

Creative decisions and story changes MUST retain traceable origins, such as accepted conversation
decisions, source artifacts, or revisions. Canon changes MUST support impact analysis and version
history so affected story information and manuscript content can be reviewed. The representation
and review process MUST support intentional contradictions, unreliable narrators, and deliberate
ambiguity; these MUST be distinguishable from accidental continuity errors. The framework MUST
support these techniques without prescribing which techniques a novel uses.

### V. Guided Creative Collaboration

Guided brainstorming MUST be the default interaction model, and users MUST be able to request
freeform exploration. Agent guidance MUST support meaningful questions, challenges to assumptions,
and relevant creative improvements, while keeping suggestions proportional to the conversation
and allowing the user to redirect or limit them. Brainstorming MUST support multiple sessions
with persistent context. Workflows MUST automatically capture ideas, decisions, and unresolved
questions with their status and origin, without promoting unaccepted ideas to canon.

The framework MUST accommodate different writing processes and narrative structures. A workflow
or agent configuration MUST NOT impose one methodology as a universal requirement. These are
interaction capabilities of the software, not rules governing how every author must write.

### VI. Structured, Portable, Version-Controlled Data

Each novel MUST be an independent Git repository. Git MUST be the source of truth for story
information, manuscript content, and creative decisions. Persistent formats MUST be human-readable
and suitable for version control; Markdown, YAML, and JSON are preferred. Any departure MUST
justify how portability, reviewable changes, and access without a particular AI platform are
preserved. Structured information MUST have consistent machine-readable schemas and references
suitable for validation and visualization.

Each authoritative datum MUST have clear ownership. Derived representations and caches MUST be
identified as such and MUST NOT become competing sources of truth. Data models MUST support schema
evolution, with documented migrations for incompatible changes. Novel repositories and writing
workflows MUST remain usable without the web dashboard.

### VII. Genre and Language Independence

Core workflows and data contracts MUST NOT hardcode a genre, narrative structure, or storytelling
convention as universally applicable. Agent configurations MUST adapt expertise to the novel's
configured needs. Writing language MUST be configured per novel; English and Icelandic MUST be
supported, and additional languages MUST be possible through modular language-specific behavior.
Manuscript storage and analysis MUST NOT assume English text, English-only character sets, or
English-specific linguistic rules. Language-dependent validation and review MUST be evaluated
using examples in the languages they claim to support.

### VIII. Separation of Responsibilities

Novel-writing methodology, story data, agent integrations, and visualization MUST have distinct
responsibilities and explicit interfaces. Components MUST be loosely coupled so that changes in
one area do not require unrelated changes elsewhere. The initial web dashboard MUST provide
read-only access to story information and MUST NOT be a required dependency of writing workflows.
Dashboard indexes and other derived views MUST respect Git's authority over novel data.

The framework MUST support contextual prompt generation so users can initiate changes through
their preferred AI agent. Generating a prompt MUST NOT itself modify authoritative story data.
Any later proposal for dashboard editing MUST be reviewed against these boundaries and the
constitution's amendment rules before implementation.

### IX. Quality Through Verification

Important functionality MUST have automated tests appropriate to its risks and observable behavior.
Verification MUST cover structured story data and cross-references, workflow behavior, canon
transitions, continuity checks, and agent-adapter contracts. Critical end-to-end workflows MUST
have integration tests. Tests MUST protect important invariants and regressions rather than mirror
implementation details.

Manuscript-generation workflows MUST include defined editorial and continuity review stages before
generated content is treated as having passed review. Review criteria and outcomes MUST be explicit
and traceable; successful parsing or schema validation MUST NOT be reported as proof of factual
correctness, narrative consistency, or editorial quality. Verification MUST distinguish automated
checks, agent judgments, and human approvals so their evidence and limitations remain visible.
This governs the software's review capabilities without dictating a novel's artistic style.

### X. Mobile-First, Accessible User Experience

The dashboard MUST support phones, tablets, and desktops, with navigation and readable content
prioritized over decoration. Relationship graphs and other complex views MUST remain usable on
small screens and MUST provide accessible alternatives to visual-only information. Essential
information and actions MUST be available through keyboard operation and assistive technologies.

Dashboard features MUST define and verify relevant responsive-layout and accessibility acceptance
criteria. Performance-sensitive views MUST specify representative large-novel datasets and
measurable responsiveness targets during planning, and verify those targets before release.
Interface design MUST support the creative workflow without requiring duplicate data entry or
dashboard-only administrative maintenance.

### XI. Incremental Delivery and Maintainability

Development MUST deliver vertical slices with measurable user value, beginning with a minimal
end-to-end novel-writing workflow. The agent-based workflow MUST be validated through a working
slice before substantial dashboard investment; lightweight visualization experiments may support
that validation. Significant features MUST have explicit acceptance criteria before implementation.

Important architectural decisions and trade-offs MUST be documented. Project structure and
technology choices MUST favor conventional, widely understood approaches unless a concrete
requirement justifies an alternative. Installation and onboarding MUST have clear, verified
instructions, and each delivered slice MUST document the steps needed to use it.

## Scope and Architectural Boundaries

Novel Creator is an open-source, AI-powered framework inspired by BMad and SpecKit. It provides
structured multi-agent workflows for planning, writing, reviewing, and maintaining novels, plus
a mobile-first dashboard for visualizing story information. This constitution governs how the
software is designed, developed, tested, and evolved. It MUST NOT prescribe the plot, prose style,
genre, structure, or creative process of an individual novel.

The principles define product capabilities and architectural constraints; they do not authorize
implementing all capabilities in one release. Specifications and plans MUST identify the vertical
slice being delivered and any constitutional capabilities that remain future work. They MUST NOT
claim support that has not been implemented and verified.

Implementation languages, frontend frameworks, databases, and specific AI models MUST be chosen
in subsequent architecture and planning decisions against established requirements. This
constitution imposes no selection of those technologies. Novel data ownership, platform
independence, and operation without the dashboard MUST remain intact across those decisions.

## Development Workflow and Quality Gates

1. Specifications MUST define intended behavior, acceptance criteria, and relevant constitutional
   principles. Ambiguous creative authority or conflicting requirements MUST be clarified before
   dependent implementation proceeds.
2. Plans MUST document component responsibilities, interfaces, important trade-offs, and any new
   complexity. Changes to data schemas or architectural contracts MUST include compatibility and
   migration analysis proportional to their impact.
3. Implementation MUST proceed in usable vertical slices. Reviews MUST check the architecture and
   feature behavior against relevant principles and identify any proposed deviation explicitly.
4. Before a slice is declared complete, its acceptance criteria MUST be checked, relevant automated
   tests MUST pass, and applicable integration, language, accessibility, and performance evidence
   MUST be recorded. Unavailable verification MUST be reported as unverified, never as passing.
5. Breaking changes MUST include a documented migration plan, affected data or integrations,
   validation steps, and recovery guidance. User-facing installation, onboarding, and operational
   documentation MUST be updated when delivered behavior changes.

## Governance

This constitution takes precedence over implementation convenience, individual feature
specifications, plans, and local practices. Contributors and reviewers MUST assess architecture
and feature changes against the relevant principles before acceptance.

Every proposed deviation MUST document the affected principle, concrete need, alternatives, impact,
and intended duration or resolution. Justification alone MUST NOT silently waive a principle.
A change that contradicts a constitutional requirement MUST receive an explicit maintainer-approved
amendment before the conflicting implementation is accepted. Where principles conflict or
interpretation would make a consequential product or authority decision, the issue and trade-off
MUST be presented for clarification rather than resolved silently.

Amendments MUST document the rationale, changed principles, compatibility impact, and any required
migration plan. A project maintainer MUST explicitly approve the amendment. The constitution update
MUST include a Sync Impact Report and identify affected specifications, plans, or contracts that
require follow-up. Dependent templates and commands consume this constitution at runtime; they MUST
NOT be changed merely to duplicate its requirements.

The constitution MUST use semantic versioning: MAJOR for backward-incompatible principle removals
or redefinitions, MINOR for new principles or materially expanded guidance, and PATCH for
non-semantic clarifications and corrections. Significant architectural contracts MUST also be
versioned, with documented compatibility expectations and migration plans for breaking changes.
Ratification records initial adoption; the last-amended date MUST change when amendments are made.

**Version**: 1.0.0 | **Ratified**: 2026-10-21 | **Last Amended**: 2026-10-21
