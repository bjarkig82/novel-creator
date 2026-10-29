# Research: Simple Package Initialization

Date: 2026-10-29. Decisions are planned behavior. No package was published/installed during planning.

## Distribution and install route

**Decision**: PyPI and the existing Python console entry point. Canonical route: `python -m pip install novel-creator` in a user-owned venv outside novels. Keep executable novel-creator; select the next unused release version during release preparation.

**Rationale**: pyproject.toml already declares this package/command and dependencies. PyPA documents package-name installs and isolated environments. Reuse avoids a new language, runtime or packaging layer.

**Alternatives considered**: npm wrapper duplicates packaging; local wheel alone fails FR-001. pipx isolates console apps, but system Python cannot see its dependencies for the pinned novel run.py; supporting that end-to-end needs extra routing/discovery. pip/venv preserves the existing runtime model with explicit interpreter guidance. pipx is not claimed as a supported end-to-end route for this slice.

**Release preconditions**: Verify PyPI name ownership/availability before advertising live installability. Read-only web attempts at project/JSON URLs returned cache misses, which establish neither availability nor ownership. If unavailable, obtain and record a maintainer-approved distribution-name substitution throughout metadata/docs/evidence; console name can stay. Verify unused version, publisher configuration, metadata and licensing. No local license file was found: do not invent a license or claim legal/open-source release readiness. These are execution gates, not unresolved architecture choices.

Sources: [PyPA pip/venv guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), [pipx model](https://pipx.pypa.io/stable/). Local evidence: pyproject.toml, install.py, installed adapter and wheel verifier.

## Publishing

**Decision**: Build wheel/sdist, verify both and clean installs, then publish the exact artifacts via GitHub Actions Trusted Publishing in a protected/manual job. Current remote is bjarkig82/novel-creator; verify account access before publisher setup. Restrict OIDC permissions to the publish job.

**Rationale**: Official guidance describes short-lived OIDC publishing. No .github workflow currently exists; this design does not imply configured accounts or permissions. Optional staging-index checks cannot replace production named-install evidence.

**Alternatives considered**: Manual token uploads add secret handling; publish-on-push exceeds release intent; release attachments alone fail the accepted package-by-name route. Local builds cannot prove production name identity or dependency acquisition.

Sources: [PyPI publishing](https://docs.pypi.org/publishing/publishing-to-pypi/), [PyPA Actions flow](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/), [publisher configuration](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).

## CLI and provenance

**Decision**: Add positional NAME with --path, --title, --language; no separator before options. Preserve legacy path/brief interface and original brief bytes. Shorthand creates a deterministic effective brief plus a second bootstrap artifact for parsed setup choices.

**Rationale**: initialize(target, original_text) validates before writes; project_from_brief rejects unfamiliar keys. Existing bootstrap artifact schema supports multiple entries. The second artifact preserves NAME when title differs; project field sources still point at the ordinary brief. Preserve parsed values, not purported shell keystrokes; omit language from effective brief when not supplied.

**Alternatives considered**: Mandatory brief files defeat the feature. Effective title alone loses name/option provenance; arbitrary keys break creative brief contracts; fabricated messages violate authority. Retry must compare NAME even when an explicit identical title hides a change, exclude presentation flags, and reuse original pending identities.

Read-only agent research and local inspection: cli.py parser/main; install.py bootstrap/initialize/_reserve_setup; records.py preference/project_from_brief; validation.py artifact checks; contract/integration tests. Preserve legacy empty-unborn-repository and metadata-file allowances rather than silently tightening them.

## Pinned runtime and guide

**Decision**: Keep run.py; expose exact sys.executable as output-only runtime guidance. Canonical guide: workflows/getting-started.md, packaged through existing resources and installed under .novel-creator/workflows/. README links to source, help to installed-package copy, completion to novel-local copy.

**Rationale**: run.py selects pinned novel modules but needs dependencies in the invoking interpreter. A new Codex process may not inherit activation. Provide an explicit interpreter handoff and verify it in a separate host session; do not commit machine paths. Old novels keep pinned resources after package upgrades.

**Alternatives considered**: Central dispatcher adds public surface; committed absolute interpreter paths break portability; global installs affect unrelated environments; duplicated guides drift; documentation hosting is unnecessary. A moved novel needs a compatible local environment/interpreter, not altered history.

## Verification

**Decision**: Existing suites plus shorthand/provenance/recovery cases, clean dependency installs, guide execution and post-publication checks; label host and human evidence separately.

**Rationale**: tests/verify_wheel.py reuses dependency sites and disables network. It proves installed source/resource integrity, not clean dependency resolution or public availability. Feature-001 final qualification withdraws timing goals and novice/manual prerequisites; retain that policy.

**Alternatives considered**: New latency thresholds or mandatory novice panels expand scope. Structural conversations do not establish native capture or human approval.

All technical design unknowns are resolved. Name control, licensing/publisher setup, exact release version, and platform execution remain explicit release prerequisites requiring current evidence at execution time.

## Analysis remediation — 2026-10-29

**Decision**: Older recognized novels without a pinned guide receive a verified, labeled installed-package guide fallback without novel mutations; readiness uses their own manifest. Baseline recovery tests are introduced/executed in US3, and optional-setting recovery cases are introduced in US2 before its flag implementation, then verified afterward.

**Rationale**: Guide discovery cannot require silent upgrades, and a baseline safety gate must not depend on unimplemented optional syntax. Existing legacy output stays unchanged.

**Decision**: Separate manual candidate/publish workflow modes. Store one built wheel/sdist plus manifest under immutable repository/run/attempt/artifact identity. Final platform/guide/host evidence binds to that candidate. Publish downloads it, validates identity/hashes/evidence, and uploads without rebuilding; sdist-rebuilt verification wheels remain separate.

**Rationale**: An explicit artifact handoff makes the tested-bytes requirement executable and rejects missing/expired/mismatched candidates. Candidate creation needs finished story code/docs and local checks; final candidate-bound host evidence follows creation, avoiding a circular prerequisite.

**Alternatives considered**: Copying a guide into older novels breaks preservation; skipping optional tests to pass baseline masks dependencies; rebuilding at publication breaks artifact identity. No runtime or release actions were performed by this remediation.
