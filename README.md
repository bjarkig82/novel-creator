# Novel Creator

A home for developing an app that helps writers plan and create novels.

## Project status

The Python/Git exchange-persistence foundation is implemented, with versioned
JSON schemas, source/authorization validation, atomic local saves and a disposable
installed host-spike fixture. Saves preserve unrelated staged work and manuscript
files; the tool does not push automatically.

Novel initialization, brainstorming, session management, production context and
inspection, and safe recovery are not implemented. Their CLI entries return an
explicit unavailable error. Actual Codex capture remains **unverified** and blocks
dependent story implementation; no host, bilingual workflow or feature release
is claimed supported. See the [host evaluation](tests/evaluations/host-capture.md).

## Development

For the manual host test and the remaining delivery milestones, see
[Testing and completing the current feature](docs/testing-and-completion-guide.md).

Requires Python >=3.11 and Git >=2.39. From this checkout:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m novel_creator --help
python -m unittest discover -v
bash tests/speckit-smoke.sh
```

On Windows, activate `.venv\Scripts\Activate.ps1`. Bash smoke checks require
Bash, `jq` and `rg`. Tests use disposable repositories and local test identities;
no model credentials are required. The available persistence command is
`exchange save --novel PATH --input FILE --json`, using a complete exchange
envelope and a prepared independent repository. For a reproducible disposable
installation, follow the [host-spike fixture procedure](tests/evaluations/host-capture.md#reproducible-structural-fixture).

Saving failures disclose the last verifiable checkpoint and pending exchange.
Published saves needing index cleanup remain saved, but further writes pause;
`recover` is not yet implemented. Preserve evidence and do not reset history to
clear a pause. See [development setup and limitations](docs/development.md) and
the [validation guide](specs/001-novel-initialization-brainstorming/quickstart.md).

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
