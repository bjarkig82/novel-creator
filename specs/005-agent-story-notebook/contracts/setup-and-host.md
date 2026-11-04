# Setup and Codex Host Contract

## Proposed setup interface

novel-creator notebook init NAME [--path PATH] [--title TITLE] [--language en|is] [--json]

NAME supplies a provisional folder name/title. Path selects a new destination; default is NAME under the current directory. Existing legacy init behavior remains unchanged. Invalid or repeated/conflicting arguments produce an input error.

Success reports notebook format/version, created location, language and next action to open the folder in Codex. It makes no creative decisions.

## Destination and failure rules

Require a nonexistent destination outside other Git repositories, no symlinked path components, a writable existing parent, compatible Git and an existing usable author/committer identity. Never change global Git configuration or invent identity.

Refuse every existing destination, including an empty folder, a legacy novel or a completed notebook, without writes. This narrow first-version boundary avoids migration/adoption ambiguity.

Validate inputs/prerequisites, create the destination exclusively, write the explicit resource set, initialize an independent Git repository and commit initial files. Concurrent creators cannot overwrite the winner. On failure after creation, preserve partial files and report the state and inspection/new-path next step. Retry against an occupied target refuses; no automatic deletion or custom recovery ledger is added.

## Installed contents

- Root AGENTS.md supplied by the thin Codex adapter, linking platform-independent conversation and format guidance.
- .novel-notebook/workflows/ and the selected dedicated language resource.
- notebook/project.md and notebook/working-summary.md.
- Minimal Git ignore/attributes text.

No launcher, Python sources, exchange schemas/receipts, legacy manifest, contributor or update resources are installed. Mutable notes are writer content, not immutable installation checksums. Future notebook updates and migration are separate features.

## Native host behavior

Codex reads root project instructions normally. No per-turn skill invocation is needed. Guided brainstorming is the default; freeform exploration is available on request, and redirection takes effect immediately. Neither mode forces a questionnaire or recap. Conversation can begin on any topic. The agent reads the brief/relevant notes, distinguishes decisions from proposals, and maintains useful files by meaningful turn completion when tools permit.

A requested brief uses relevant authoritative notes; summary is navigation only. Ambiguous identity receives one focused question. Missing notes receive honest absence. Recaps are never automatic.

No exact-input capture, saved-response replay, per-turn Python validation or custom scheduling. Save failures and incomplete history are disclosed. Manuscripts remain untouched and no push or publication is authorized.

## Packaging and legacy compatibility

Map the shared notebook/ tree to the resource-only package novel_creator.notebook_resources, including its package marker and explicit workflow/language/template package-data patterns. Add explicit coverage for the separate Codex notebook entry. Do not mix shared content into the Codex adapter or legacy resource packages. Keep legacy workflow/skill resource selection unchanged; notebook activation must not enter update_release.export_bundle.

All shared workflows, both language resources, seeds and the adapter entry must exist before setup is exercised for successful creation. Setup copies the explicit selected resources; package tests verify that each installed guidance link resolves.

Use a separate initializer, not legacy initialize/bootstrap/save. Reuse only helpers independent of legacy manifests and exchange state. Installed wheel and sdist checks exercise notebook creation outside the checkout; legacy installation and update-preservation tests remain regression requirements.
