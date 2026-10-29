# Release preflight

Date: 2026-10-29. Candidate package name: novel-creator. Local version begins at 0.1.0; implementation version is provisional until public name/version checks and release authorization.

- Local pyproject.toml declares novel-creator and the existing console entry. This does not establish ownership on PyPI.
- No LICENSE file found. The maintainer explicitly chose “keep it unlicensed for now” during implementation. Preserve that choice: no license file/expression or open-source-license claim is added. Licensing selection is resolved as intentionally unlicensed, not an outstanding question.
- PyPI name control, maintainer account access and trusted-publisher configuration are not verified. No account/name reservation or publication performed.
- No .github workflow existed at baseline. Local workflow preparation is authorized; pushing/dispatching/configuring external environments remains a separate release action.
- Local implementation can proceed. T031 and external candidate/publication gates stay open until their prerequisites are actually met.

Read-only normal-access PyPI lookup returned HTTP 404 for `https://pypi.org/pypi/novel-creator/json`. Sandbox lookup failed DNS first. A 404 does not prove ownership or reserve a name. Public name control/version and trusted publisher access remain unverified; no external changes occurred.

Build-only tools were installed into this repository's existing .venv after confirming the build frontend/backend were absent. No system Python settings were changed. Official action repository HEAD commits were resolved read-only on 2026-10-29 and pinned in the local workflow; it has not been pushed or dispatched.

## Authorized candidate preparation — 2026-10-29

The maintainer explicitly authorized committing the prepared changes, pushing `codex/package-novel-init`, making the workflow available and running candidate mode. Publishing and publisher/account configuration remain separate gates. The maintainer has no PyPI account; name control and trusted publishing remain unavailable. Refreshed package and provisional 0.1.0 version lookups both returned HTTP 404, establishing no ownership.

The connected GitHub account has admin/push access to `bjarkig82/novel-creator`. The repository is private. Read-only workflow/run inventories both contained zero entries, and the workflow file was absent from the default branch. Candidate dispatch therefore needs workflow availability on the default branch plus the feature source on its named branch. Repository visibility is unchanged. Public release documentation URLs cannot be claimed accessible while the repository is private; resolve that release prerequisite before publication.

The authorized branch push and manual workflow installation have now occurred. The workflow-only default-branch commit is `9bb9bf5196ada1d326bcd2c437a9f921ecf92699`. First candidate `40881175659` was superseded after the literal guide found an undocumented Windows `py` launcher dependency. Corrected source `1d6d6632c81ca8402ff60ca05a7ec832a0dea802` is in replacement run `40882235905`, attempt 1, artifact `12901057415`. These are private development candidates, not public releases. PyPI account/name control, publisher configuration, release documentation access and explicit publication authorization remain unresolved. Licensing stays intentionally unlicensed.
