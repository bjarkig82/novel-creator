# Novel Creator

A home for developing an app that helps writers plan and create novels.

## Getting started

Start by asking your agent to set up a story, for example: “Use Novel Creator
to create a new English story notebook called My Novel at /path/to/My Novel.
I don't have a story idea yet.” Use your intended new folder. The agent can run
setup, read the generated project instructions and continue in the same
conversation. See [agent-led setup](workflows/start-here.md#ask-your-agent-to-set-up-a-story)
for prerequisites, safe destinations and host access limits.

This checkout prepares **0.5.0, a qualified but unpublished candidate**, adding
six writing roles with scene/chapter manuscripts, research and review guidance for new
notebooks. These additions are absent from the published 0.4.1 package. New
writing instructions apply to notebooks initialized from this updated source or,
after publication, 0.5.0. Agent-led setup handoff improvements and explicit legacy
realtime input capture are already available in published 0.4.1.

Installing a package does not rewrite existing project guidance. The new writing
resources passed automated Windows/Linux release qualification for the exact
candidate recorded in the [release evidence](tests/evaluations/release-0.5.0.md).
Native specialist interaction in Codex Desktop remains unverified. See the
[0.5.0 candidate notes](docs/releases/0.5.0.md) for changes and host requirements.

**New to the tools?** Start with the [beginner guide](https://github.com/bjarkig82/novel-creator/blob/main/workflows/start-here.md),
which explains setup, everyday writing, and the Windows, Linux, and Mac limits.
If someone has already prepared your novel, go straight to
[everyday writing](https://github.com/bjarkig82/novel-creator/blob/main/workflows/everyday-writing.md).

Install [Novel Creator 0.4.1 from PyPI](https://pypi.org/project/novel-creator/0.4.1/)
in your configured environment:

```text
python -m pip install novel-creator==0.4.1
```

**Usable only after 0.5.0 is published:**

```text
python -m pip install --upgrade novel-creator==0.5.0
```

Existing legacy novels need an [explicit supported update](workflows/getting-started.md#updating-an-existing-book)
to change pinned resources. Existing notebooks are not automatically updated or
migrated.

For new notebooks, use the setup route below. The
[legacy getting-started guide](https://github.com/bjarkig82/novel-creator/blob/v0.4.0/workflows/getting-started.md)
covers `novel-creator init 'My Novel'`, pinned saves and returning later for the
separate legacy format, including Python/Git prerequisites and an isolated environment.
Windows PowerShell and Linux Bash production installs are verified, together with
Windows Codex Desktop setup/save/inspection/resume. Linux Codex integration remains
unverified. The developer/older POC instructions below remain reference material.

See the [release history](docs/releases/README.md) for version changes and
compatibility. Candidate verification precedes publication.

## New story notebook (0.4.0)

The published 0.4.0 package adds a native Codex Markdown notebook for **new novels**.
Install it in a Python 3.11+
virtual environment, with Git 2.39+ and your Git identity configured. The
older 0.3.0 package does not contain this command. Your agent can execute
this direct CLI fallback using the configured environment and a new path outside
every existing Git repository:

```bash
novel-creator notebook init "My Novel" --path "/path/to/My Novel" --language en
```

Use `--language is` for Icelandic and optionally `--title` for the working title.
After successful setup, have the agent read the created folder's `AGENTS.md`
and linked guides, project notes and working summary before continuing there.
If the host cannot access the folder, select/open the initialized project in
Codex. Talk naturally about your story; ask for a
topic brief whenever useful. The notebook does not request an automatic recap.
Python is used for setup; the writing workflow uses Codex's native file and Git
tools. Existing novels use the separate legacy commands and are not converted.

In a newly created notebook, invoke `$novel-outline` to propose a book outline
from the notes, refine it in conversation, and save the chosen structure as a
linked topic. It supports English and Icelandic, preserves existing outline
edits and history, and keeps proposed facts and open questions distinct from
accepted structure. It creates no chapter or scene manuscript files and adds no
CLI command. Existing notebooks do not acquire the skill automatically.

Notebook brainstorming adapts to the book's stage and your chosen topic or method.
With no concept, it starts broadly and asks one question at a time. Optional
`$novel-book-idea`, `$novel-premise`, `$novel-character`, `$novel-plot` and
`$novel-setting` skills provide focused entry points; outlining remains explicit-only.
These additions ship only into new notebooks. See the
[0.4.0 release notes](docs/releases/0.4.0.md) for upgrade instructions,
compatibility and evidence limits.

Notebook conversations in Windows and Linux Codex Desktop remain unverified;
see the [notebook evidence ledger](tests/evaluations/agent-story-notebook.md) and
[release preparation](tests/evaluations/agent-story-notebook-release.md).

## Writing agents and manuscripts (0.5.0 source candidate)

New notebooks initialized from this source install six `.codex/agents/` roles.
The root conversation follows the orchestrator; you can request a specialist in
ordinary language, such as “Let me work with the scene writer.” Native role
selection and ongoing direct turns depend on the actual Codex client and remain
unverified in the target desktop. Ask the host to disclose unavailable capabilities.

The [writing-agent usage guide](docs/writing-agents-usage.md) covers role choices,
on-demand scenes and chapters, scoped revisions, research sources and review
findings, with optional skill entries. Open the initialized novel folder itself.
Existing notebooks and legacy novels stay unchanged; there is no new migration
or updater command. See [focused evidence](tests/evaluations/writing-agents.md)
and the [pending desktop checkpoint](tests/evaluations/writing-agents-host.md).

## Project status

**Existing-book updater (0.3.0 release target):** this checkout implements explicit published
release checks, reviewed previews, framework-only local update commits and exact
operation recovery. The published 0.1.0/0.2.0 packages do not contain it. Package
installation alone does not update a pinned book. See the
[update instructions](workflows/getting-started.md#updating-an-existing-book),
[shared workflow](workflows/update.md) and
[qualification ledger](tests/evaluations/existing-book-update-qualification.md).
Keep legacy clients closed through first application/recovery and use the
external controller. The actual Windows Codex host workflow has been exercised
with user-approved delegated evaluation input, including instruction/skill reload
and exact saved-response checks; see the [host evidence and scope](tests/evaluations/existing-book-update-host.md).
Direct native-user input and Linux Codex update behavior remain unverified.
On Windows, keep preview/apply/recovery in the same scoped filesystem-access
context so the configured runtime's detected platform markers remain consistent.
No release, push or publication is implied by the implementation or evaluation.

**Single-user POC:** the current delivery is the local Codex workflow for novel
setup, brainstorming, saved story records, canon decisions, continuity and
resumption. The owner is the initial user. Novice testing is out of scope;
manual/owner testing follows delivery and does not block it. Start with the
[POC quickstart](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/docs/poc-quickstart.md) and
[automated POC evidence](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/tests/evaluations/poc-readiness-20261023.md).

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
See the [final functional qualification](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/tests/evaluations/final-functional-qualification-20261028.md).
See the [host evaluation](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/tests/evaluations/host-capture.md).

## Development

Version 0.2.0 includes **optional contributor retrospectives**, disabled by
default for everyone. Newly initialized novels can explicitly opt in to review
completed tasks and prepare checked draft contributions through a separate
framework checkout. Existing novels retain their pinned bundle after a package
upgrade. See the [qualification scope and retained limitations](tests/evaluations/automatic-retrospectives-qualification.md),
the [contributor workflow](workflows/retrospective.md) and [0.2.0 release notes](docs/releases/0.2.0.md).
Windows Codex native behavior and a separately authorized normal-protocol real
draft have been verified in their recorded scopes. Linux Codex integration remains
unverified; local fake-transport tests do not establish real GitHub effects.

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
manuscript edits. See [record ownership and compatibility](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/docs/record-format.md).

The automated journeys verify storage and record behavior on Linux and Windows.
macOS support is deferred. Novice evaluations are out of scope for the initial
single user. Full English/Icelandic literary parity and broader release/durability
qualification remain separate from automated POC verification.
The earlier Linux reference passed the performance targets. The final-source
large Windows fixture misses its read target and times out on save attempt 27,
so save p95 is unavailable; see the
[measured configurations](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/tests/evaluations/performance.md). Voice
capture/transcription and spoken output belong to the host; exact
spoken-output fidelity is unverified.

For validation commands and current completion guidance, see
[Testing and completing a change](docs/testing-and-completion-guide.md).

Requires Python >=3.11 and Git >=2.39. From this checkout:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m novel_creator --help
python -m unittest discover -v
```

On Windows, activate `.venv\Scripts\Activate.ps1`. Tests use disposable
repositories and local test identities; no model credentials are required. The available persistence command is
`exchange save --novel PATH --input FILE --json`, using a complete exchange
envelope and a prepared independent repository. For a reproducible disposable
installation, follow the [host-spike fixture procedure](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/tests/evaluations/host-capture.md#reproducible-structural-fixture).

To check the distributable as well as the editable checkout, build and verify a
wheel from the configured dependency environment:

```bash
python -m pip wheel . --no-deps --wheel-dir dist
python tests/verify_wheel.py dist/novel_creator-0.5.0-py3-none-any.whl
```

Use the actual versioned filename produced by the build. The verifier installs
the wheel in a disposable environment, checks its source
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
[development setup and limitations](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/docs/development.md) and
the [validation guide](docs/testing-and-completion-guide.md).

## Project tooling

Use lightweight planning and focused implementation for this single-maintainer
project. Small changes need no separate plan document; larger changes can use a
short list of concrete steps. Repository [agent instructions](AGENTS.md) require
scoped subagent implementation and independent reviews when available.

The [functionality guide](docs/functionality.md) describes setup, legacy persistence,
canon and continuity, the Markdown notebook, updates, optional retrospectives and
current limits. See [development setup](docs/development.md) and
[testing guidance](docs/testing-and-completion-guide.md) for contributor commands.
Shared application workflows and installed Codex skills remain product resources.

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
See [measured performance and platform limits](https://github.com/bjarkig82/novel-creator/blob/v0.2.0/tests/evaluations/performance.md).
