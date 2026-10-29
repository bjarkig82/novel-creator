# Novel Creator

A home for developing an app that helps writers plan and create novels.

## Project status

**Single-user POC:** the current delivery is the local Codex workflow for novel
setup, brainstorming, saved story records, canon decisions, continuity and
resumption. The owner is the initial user. Novice testing is out of scope;
manual/owner testing follows delivery and does not block it. Start with the
[POC quickstart](docs/poc-quickstart.md) and
[automated POC evidence](tests/evaluations/poc-readiness-20261023.md).

The Python/Git exchange-persistence foundation is implemented, with versioned
JSON schemas, source/authorization validation, atomic local saves and a disposable
installed host-spike fixture. Saves preserve unrelated staged work and manuscript
files; the tool does not push automatically.

Initialization, settings revisions, installed context/inspection/session listing
and explicit pending/published recovery are implemented. Shared Codex workflows
cover guided/open brainstorming, capture, authority and continuity; their new
product-level creative judgments have scoped automated host evidence; subjective
quality remains for the owner's later use.
The actual Codex capture capability gate has **passed**
for the tested Windows Desktop native-tool/text-input combination with scoped
filesystem approval. Story tooling and shared workflows are delivered; their
subjective literary quality remains unmeasured. All latency targets were withdrawn
by the owner on 2026-10-28; optimization is deferred. Timings are informational.
See the [final functional qualification](tests/evaluations/final-functional-qualification-20261028.md).
See the [host evaluation](tests/evaluations/host-capture.md).

## Development

Create a UTF-8 brief JSON file. `{}` starts with no concept and unknown creative
preferences. A supplied brief can combine answers:

```json
{"title":"Bréf","original_concept":"A keeper receives letters from tomorrow.","manuscript_language":"is","creative_brief":{"genre":"Mystery","tone":null},"review_preferences":{"routine_checkpoint":"on_request"}}
```

From the configured Python environment, initialize an explicit novel path outside
the framework and every other Git repository:

```powershell
python -m novel_creator init --path C:\Novels\MyNovel --brief-file C:\Novels\brief.json --json
python C:\Novels\MyNovel\.novel-creator\run.py context --novel C:\Novels\MyNovel --json
python C:\Novels\MyNovel\.novel-creator\run.py session list --novel C:\Novels\MyNovel --json
python C:\Novels\MyNovel\.novel-creator\run.py validate --novel C:\Novels\MyNovel --json
```

Use your own paths. Git needs an existing author/committer identity; installation
does not invent one or alter global configuration. Unrelated occupied directories
are refused. Existing AGENTS.md is preserved. Interrupted initialization retains
its original brief/payload; retry with that unchanged brief and inspect any conflict.
Repeated setup on a recognized novel offers continuation without replacing it.

Open the new novel folder in Codex. Its installed `$novel-init`,
`$novel-brainstorm`, `$novel-resume` and `$novel-inspect` entries load pinned shared
workflows. Setup can finish before brainstorming. Start guided or request open
exploration, change topics or ask for fewer suggestions. The host prepares typed
session/capture revisions and saves every exact exchange before displaying it.
Session start, resume, mode changes and closure are records in that same transaction.
Python/jsonschema/jsonschema-rs remain required; no framework path, model key or dashboard is needed.

Resume lists stable session IDs, restores saved focus/mode and offers any saved
reply with display unconfirmed. Inspect source-backed records and history:

```powershell
python C:\Novels\MyNovel\.novel-creator\run.py inspect --novel C:\Novels\MyNovel --kind assertion --json
python C:\Novels\MyNovel\.novel-creator\run.py recover --novel C:\Novels\MyNovel --exchange EXCHANGE_UUID --json
python C:\Novels\MyNovel\.novel-creator\run.py recover --novel C:\Novels\MyNovel --exchange EXCHANGE_UUID --retry --expected-head CONFIRMED_HEAD --json
```

For a first unpublished bootstrap use `--expected-head unborn`. Inspection alone
does not write. Explicit retry preserves the payload/IDs and published saves are
cleaned without replay; stale checkpoints and changed managed files conflict.
Held locks are disclosed and never silently stolen. On a save failure, pause
authority and show the last confirmed checkpoint plus unsaved pending exchange.
Default sandbox hard-link denials can require scoped filesystem approval.

Clear acceptance establishes only selected facts. Ambiguity asks one focused
question. Correct/revise/reverse explicitly, retaining prior versions, sources and
direct impact for inspection. Contradictions cite sources and options; deferral
keeps the idea unresolved and holds affected canon. Unavailable context is
disclosed and revalidated after restoration. These changes never authorize
manuscript edits. See [record ownership and compatibility](docs/record-format.md).

The automated journeys verify storage and record behavior on Linux and Windows.
macOS support is deferred. Novice evaluations are out of scope for the initial
single user. Full English/Icelandic literary parity and broader release/durability
qualification remain separate from automated POC verification.
The earlier Linux reference passed the performance targets. The final-source
large Windows fixture misses its read target and times out on save attempt 27,
so save p95 is unavailable; see the
[measured configurations](tests/evaluations/performance.md). Voice
capture/transcription and spoken output belong to the host; exact
spoken-output fidelity is unverified.

For verified commands and the remaining delivery milestones, see
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

To check the distributable as well as the editable checkout, build and verify a
wheel from the configured dependency environment:

```bash
python -m pip wheel . --no-deps --wheel-dir dist
python tests/verify_wheel.py dist/novel_creator-0.1.0-py3-none-any.whl
```

The verifier installs the wheel in a disposable environment, checks its source
and resource bytes, and exercises initialization, recovery, saves and Unicode
readback outside the checkout. It reuses the calling environment's dependency
packages and pip without downloading runtime dependencies. JSON output uses
UTF-8 even when Python starts with a legacy terminal encoding.

Saving failures disclose the last verifiable checkpoint and pending exchange.
Published saves needing index cleanup remain saved, but further writes pause.
Use the recovery inspection command above, then explicitly retry against its
current checkpoint when safe. Pending retries use the unchanged receipt payload;
published cleanup synchronizes managed index entries without replaying decisions
or adding a commit. Changed payloads, managed files, staged entries or stale
checkpoints can block recovery; preserve that evidence and inspect the conflict.
Never reset history or delete receipts to clear a pause. See
[development setup and limitations](docs/development.md) and
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

### Optional validation cache

For repeated reads/saves, `NOVEL_CREATOR_VALIDATION_KEY_FILE` may point to an
existing private 32-byte cache key file at an absolute path outside the novel. The
CLI only reads this runtime configuration; it never creates or modifies the key.
With no key configured, full validation remains available.

The cache under `.novel-creator/local/cache/` contains authenticated validation
metadata bound to the exact Git snapshot, schemas and runtime. Records are read
from Git and their object hashes are checked. Cache files can be deleted safely;
the next read validates fully and rebuilds them. A changed snapshot/schema,
malformed proof or novel-supplied key cannot bypass validation or authorize canon.

The repeatable benchmark creates its own temporary external key and removes it
afterward. `--no-validation-cache` measures the full-validation configuration.
See [measured performance and platform limits](tests/evaluations/performance.md).
