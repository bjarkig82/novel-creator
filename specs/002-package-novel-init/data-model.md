# Data Model: Package Initialization

Reuse schema v1 and existing bootstrap, manifest and transaction formats. No database or story-schema migration. Legacy briefs/artifacts remain unchanged.

## Installable release

Fields: distribution_name (candidate novel-creator; verify control before release), release_version (next unused), requires_python (>=3.11), dependencies (existing validator constraints), console_entry (novel-creator), wheel/sdist names and SHA-256 hashes, source revision, supported OS/interpreter evidence, production index URL, verification status.

Candidate identity additionally records repository, candidate workflow run ID/run attempt, immutable artifact ID, source commit and manifest hashes. Verification evidence references this identity. Publishing run ID is separate; publish consumes the stored candidate wheel/sdist without rebuilding and validates identity/hashes before upload. Rebuilt-sdist test output is not a release artifact substitution.

One release creates many independent pinned novel bundles. Synchronize distribution version, package __version__ and newly generated manifest bundle_version from one release version source. Schema version is independent. Never rewrite old novel manifests during a package upgrade.

Lifecycle: designed → built → candidate verified → publication authorized → published → public-install verified. Publication alone does not complete the feature. Existing public versions/files are not overwritten. Current name/version/publisher ownership checks are release gates.

## Initialization request

Fields: mode (shorthand/legacy), name (shorthand), resolved_destination, title_argument (optional exact text), language_argument (optional en/is), effective_brief, presentation (human/json; excluded from authoritative setup identity).

Validate NAME as a nonempty, non-whitespace single filesystem component, not . or .., without slash/backslash, NUL, control characters or platform-invalid spelling. Preserve Unicode/spaces without translation. --path is the complete destination, not a parent to append NAME to. Existing root/reparse/repository guards remain; no alias canonicalization that bypasses safety. Reject invalid options before writes.

Effective brief: title is explicit title or NAME; include manuscript_language only when explicitly supplied. Omit other creative values, retaining existing unknowns/defaults. Deterministic UTF-8 serialization uses fixed sorted keys/separators and no locale-dependent bytes.

Provenance: preserve ordinary first brief input artifact and project JSON-pointer sources. Append a second bootstrap input_artifact whose parsed_value is identified by request_type: cli_init_v1 and records name, resolved_destination, title_argument and language_argument (absent arguments are null). original_text is deterministic JSON; digest is SHA-256 of its UTF-8 bytes. The first brief is derived from those parsed choices; neither artifact fabricates conversation or accepts canon. Do not record full process argv, environment, executable path or purported original shell quoting. Destination may reveal a local folder; it is explicit initialization input, not a machine runtime configuration.

Retry identity: immutable setup state retains the entire original bootstrap including request artifact. Compare canonical request and brief, excluding newly generated IDs/timestamps; reuse the saved bundle. NAME changes conflict even if explicit title is unchanged. Argument order and equivalent resolved destination spellings do not change identity. Explicit en differs from omitted language in provenance. Legacy partial state without request artifact is retried through unchanged legacy brief input, never inferred into shorthand mode.

## Novel project and installed bundle

Existing identity/revisions and unknown/supplied/default preference states remain. NAME as provisional title is supplied input; request artifact preserves title/name distinction. Existing language defaults and immutable original_concept remain. No new project fields or creative claims.

Manifest retains schema_version, bundle_version, managed_paths and checksums; guide is one more managed resource. Recognized projects verify existing history/resources and return continuation without replacing settings. Interpreter paths are never added to committed metadata.

Lifecycle: uninitialized → reserved partial setup → initial save published → ready, or saved/cleanup_required awaiting explicit recovery. Conflict/failure preserves evidence and never implies readiness. Existing lock, expected-head, private-index and receipt protections own concurrency/transaction safety.

## Initialization outcome

Retain envelope ok/operation/novel_id/warnings/checkpoint/data. data.saved and data.cleanup_required retain their meanings. Shorthand adds data.novel_path, data.runtime_python, data.launcher_path, data.getting_started_path and data.ready. runtime_python is the current absolute sys.executable, advisory output only. Paths are validated before rendering next actions.

ready requires a confirmed bootstrap, verified required resources, and no cleanup requirement. An existing-novel result may be ready but never implies new flags were applied. Saved-but-cleanup-required remains exit 0 with ready false and explicit recovery guidance. Preserve legacy fields/rendering/exit codes; no change to persisted story output contracts.

For recognized older novels, required resources are those in their original manifest. getting_started_path points to a verified pinned guide when present, otherwise the verified current package guide with an explicit fallback label. Never create a missing novel-local guide or alter its manifest/history to satisfy discovery. Validate fallback existence; report an actionable documentation problem if unavailable, not a nonexistent path. Keep legacy machine output unchanged.
