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

## PyPI account created — 2026-10-29

The maintainer reports creating PyPI account `bjarkig82`. This supersedes the earlier missing-account state. Authenticated access, name control and trusted publishing are not yet verified. A refreshed package lookup returned HTTP 404; the GitHub environment inventory is empty. Neither service was changed by these read-only checks.

Prepared pending GitHub publisher configuration: PyPI project `novel-creator`; repository owner `bjarkig82`; repository name `novel-creator`; workflow filename `package-release.yml`; environment `pypi`. This matches the verified candidate workflow. PyPI's official instructions permit a pending publisher for a new project but explicitly state that it does not reserve the project name: https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/ . Configuration is pending the explicit setup authorization required by T036. Publication remains a separate gate after host/guide/documentation prerequisites. Do not request or record API secrets.

## Authorized publisher/environment setup — 2026-10-29

The maintainer explicitly authorized the prepared pending publisher and GitHub environment configuration, then authorized making this repository public. The initial required-reviewer setup returned HTTP 422 because the private repository's billing plan did not support that protection; GitHub had still created an empty pypi environment. It was immediately restricted to main. After the authorized public visibility change, required-reviewer configuration succeeded.

Verified GitHub state: repository bjarkig82/novel-creator is public; environment pypi allows only branch main, requires reviewer bjarkig82 (user 6746233), and has can_admins_bypass false. Self-review remains allowed so the sole maintainer can approve a manually dispatched release. No secret was created or stored. PyPI visibly shows the signed-in bjarkig82 account but requires password confirmation to open Publishing. The maintainer was asked to complete that authentication directly; registration is not yet confirmed. Publication remains unauthorized by this setup approval, and candidate/guide/host/release gates remain in force.

The maintainer completed PyPI authentication directly. The exact prepared pending publisher was submitted and visibly confirmed by PyPI: "Registered a new pending publisher to create the project 'novel-creator'." The Pending publishers table shows GitHub repository bjarkig82/novel-creator, workflow package-release.yml and environment pypi. T036 is complete. A pending publisher does not reserve the name or establish a published project; public name control remains unconfirmed until the first authorized release. No password, API token or credential was handled or stored by the assistant. No publication was performed.
