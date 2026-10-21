# Novel Creator

A home for developing an app that helps writers plan and create novels.

## Project status

Repository initialized. The application framework and implementation have not been selected yet.

## Development

Application setup and run instructions will be added when the app is scaffolded.

## Project tooling

The existing `.specify/` and `.agents/` directories contain specification templates and agent workflows for planning and implementing features.

### Spec Kit locally and in the cloud

Use the same Codex skills in either environment: `$speckit-specify`,
`$speckit-plan`, `$speckit-tasks`, and `$speckit-implement`. The workflows include
commands for both Bash and PowerShell; select the one matching your session.

| Environment | Scripts | Requirements |
| --- | --- | --- |
| Codex cloud, Linux, macOS, WSL, Git Bash | `.specify/scripts/bash/*.sh` | Bash and standard Unix tools; Git for repository operations |
| Local Windows PowerShell | `.specify/scripts/powershell/*.ps1` | PowerShell and Git |

`jq` is recommended for Bash JSON handling, and Python 3 enables advanced
preset/extension template resolution. Neither PowerShell nor the Specify CLI is
needed to run the checked-in Bash scripts.

For example, resolve a template without creating a feature:

```bash
bash .specify/scripts/bash/resolve-template.sh spec-template --json
```

```powershell
.specify/scripts/powershell/resolve-template.ps1 spec-template -Json
```

Run commands from the repository root. Start with `$speckit-specify` to create a
feature before running planning or task commands. Both script variants share the
same templates and `.specify/feature.json` pointer. That pointer is ignored by Git;
in a fresh checkout, select an existing feature using `SPECIFY_FEATURE_DIRECTORY`
(a repository-relative path works across machines):

```bash
export SPECIFY_FEATURE_DIRECTORY=specs/001-your-feature
bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only
```

```powershell
$env:SPECIFY_FEATURE_DIRECTORY = 'specs/001-your-feature'
.specify/scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
```

The scripts are based on Spec Kit **1.0.5**, with Codex skill invocation names in
diagnostics. Initialization metadata still records the original PowerShell
setup. When updating Spec Kit, retain both script sets and the shell-specific
workflow instructions; regenerating with only `--script sh` or `--script ps`
can replace those instructions.

Validate the Bash scripts in an isolated temporary checkout with
`bash tests/speckit-smoke.sh` (requires `jq` and `rg` for assertions).
