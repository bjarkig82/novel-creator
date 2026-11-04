# Research: Agent-Maintained Story Notebook

## Native writing workflow

**Decision**: Agent instructions and native Markdown/Git editing; Python only scaffolds a novel once.

**Rationale**: The writer does not need a full archive. Current workflows/entry.md requires exact input capture, typed exchange preparation, save-before-display and optional retrospective handling. Removing those requirements makes a native notebook viable.

**Alternatives considered**: Shortening the existing instructions preserves runtime complexity. A custom save helper is deferred until a demonstrated reliability gap. Manual copying alone makes distribution and safe creation harder.

## Minimal structured Markdown

**Decision**: Versioned JSON metadata inside Markdown, readable item fields, stable references and concise decision origins.

**Rationale**: Constitution VI requires a consistent machine-readable structure. Standard-library JSON avoids new parsing dependencies, separate authoritative data files and per-turn schema validation. Notes remain readable without tools.

**Alternatives considered**: Unconstrained prose weakens references; a separate JSON graph duplicates truth; full exchange schemas recreate the current burden.

## Separate setup and resources

**Decision**: Add an explicit notebook init route. Keep shared guidance, languages and seeds in notebook/, mapped to novel_creator.notebook_resources, and only the thin Codex entry in adapters/codex/notebook/. Preserve all legacy routes.

**Rationale**: install.initialize always bootstraps/validates an exchange and invokes storage.save. bundle_files copies runtime sources, schemas, workflows and skills. Reusing them defeats simplification. AGENTS.production.md and even languages/is.md mandate the old exact-save protocol. Notebook language resources must be separate.

update_release.export_bundle derives payloads from bundle_files, so notebook activation must remain outside legacy bundle selection and update export. Mutable notebook content must never be installed as immutable checksummed framework data.

Implementation review established that both the legacy exporter and release verifier enumerate top-level Python modules. They now consistently exclude the setup-only notebook.py module, and the shared CLI omits its command in the pinned-launcher layout. The full installed package retains notebook setup. A real legacy-launcher regression verifies this separation; merely omitting Markdown resources was insufficient.

**Alternatives considered**: Changing the current default risks existing contracts. Placing shared methodology in the Codex adapter violates platform separation. A separate release package adds unnecessary maintenance; a resource-only package within the existing distribution supplies the required boundary. An explicit route is clearer than silently interpreting legacy manifests.

**Evidence**: Read-only setup review checked CLI parser/dispatch, install.initialize/bootstrap/bundle_files, package-data configuration, legacy update resource selection and initialization/wheel test anchors. It supports isolation; no code was changed by the review.

## Portable item navigation

**Decision**: Give each item a plain Item-ID field. Pair semantic topic/item keys with ordinary relative file links, without fragments.

**Rationale**: Files open in any ordinary Markdown reader; explicit item identifiers remain readable/searchable regardless of renderer-generated heading anchors. Development checks verify both file ownership and the exact target item.

**Alternatives considered**: Custom heading attributes are unsupported by some readers. HTML anchors may be filtered, and generated heading fragments vary with titles, Unicode and renderer. None is required for the initial notebook.

## Guided default

**Decision**: Preserve guided brainstorming as default, with freeform exploration and immediate redirection on request.

**Rationale**: This retains the constitutional interaction default without imposing a questionnaire or automatic recap. Verify both modes in actual host journeys.

## History and failures

**Decision**: Attempt scoped native Git checkpoints after meaningful changes. Retain superseded accepted prose in a topic's historical revision section until prior values are recoverable through Git. Distinguish save from checkpoint failure.

**Rationale**: This preserves meaningful revision history without transaction receipts. Native operations must preserve unrelated staged entries. A touched file with pre-existing staged user edits causes checkpoint deferral instead of consuming those edits.

**Alternatives considered**: A commit for every exchange creates churn; saving only on session close loses ordinary progress; atomic multi-file journals recreate an unnecessary runtime.

## Targeted context

**Decision**: Compact derived working summary plus links to authoritative topic files; read relevant notes and search locally. Display a recap only when requested.

**Rationale**: The writer may start a new topic at any session boundary. A mandatory recap or previous-topic closure obstructs that experience.

**Alternatives considered**: Whole-book loading wastes context. A transcript is unwanted. A search service or database has no demonstrated need.

## Verification

**Decision**: Deterministic setup/contract tests and separate actual-host English/Icelandic journeys.

**Rationale**: Schema shape cannot prove that praise was interpreted correctly or that a contradiction was detected. Existing test/evidence practice already distinguishes structural and semantic behavior.

**Alternatives considered**: Fake transcripts do not establish native behavior. New latency benchmarks are out of scope because the owner withdrew numeric targets.

## Disposition

No unresolved product clarification blocks planning. Exact instruction phrasing and internal helper names remain implementation choices. New-only scope excludes migration design and leaves current novels untouched.
