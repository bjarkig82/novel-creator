# Getting started with Novel Creator

For step-by-step explanations of the tools and your first writing session, use
the [beginner guide](start-here.md). If your setup is already prepared, go straight
to [everyday writing](everyday-writing.md). This page retains the detailed commands
and advanced maintenance instructions.

Novel Creator helps you set up a novel, explore ideas, keep decisions and questions,
and return to saved conversations in Codex. You can start with no story idea.
Each novel is its own local Git repository. Initialization finishes before creative
setup begins; you choose when to start brainstorming.

**Current published release:** `novel-creator` 0.5.0 is available on
[PyPI](https://pypi.org/project/novel-creator/0.5.0/). This checkout prepares the
unpublished 0.6.0 candidate with fresh working context and targeted retrieval.
This guide describes the
legacy format retained from 0.3.0; use the [beginner guide](start-here.md) for
new Markdown notebooks. During prepublication verification of a future release,
install only the maintainer's identified candidate wheel in the same environment.

## Before you begin

- Windows PowerShell or Linux Bash, with Python >=3.11 and pip/venv support.
- Git >=2.39 and your own Git identity already configured.
- Windows Codex Desktop with access to the novel folder and its Python interpreter
  for the conversational walkthrough. Linux Bash installation and CLI behavior
  are verified separately; Linux Codex integration is unverified in this release.
- Internet access to obtain the package and dependencies. Creating a novel then
  works offline and needs no model API key or framework source checkout.

Check `git --version`, `git var GIT_AUTHOR_IDENT` and
`git var GIT_COMMITTER_IDENT`. If an identity is missing, configure your intended
identity yourself before initialization. Novel Creator never invents one or changes
global Git settings. Codex access/account requirements belong to your Codex setup.
macOS, additional AI hosts, drafting and dashboards are outside this release.

## Install once

The environment below is outside every novel. Reuse it when you return; do not
create it inside a novel or inside another Git repository. The product manages
its own dependencies there, without changing system Python.

### Windows PowerShell

Run in PowerShell. Check `python --version` reports Python >=3.11. If your
installation uses a different command, substitute its full `python.exe` path
for `python` below. Choose an unused environment location if this one already exists.

```powershell
$runtime = Join-Path $env:USERPROFILE 'NovelCreatorRuntime'
python -m venv $runtime
$novelPython = Join-Path $runtime 'Scripts/python.exe'
& $novelPython -m pip install novel-creator
$novelCommand = Join-Path $runtime 'Scripts/novel-creator.exe'
& $novelCommand --version
& $novelCommand init --help
```

Expected: the installed version and help for `init NAME`, optional settings, and
this guide. For the short command in this terminal, activate the environment:

```powershell
& "$runtime/Scripts/Activate.ps1"
```

If script execution is restricted, keep using `& $novelCommand` instead of
`novel-creator`, and `& $novelPython` instead of `python`. No execution-policy
change is required. These variables only live in this terminal.

### Linux Bash

Run in Bash. Your distribution may supply pip/venv separately; install them using
its normal Python setup instructions if missing. Choose an unused environment path.

```bash
runtime="$HOME/NovelCreatorRuntime"
python3 -m venv "$runtime"
"$runtime/bin/python" -m pip install novel-creator
source "$runtime/bin/activate"
novel-creator --version
novel-creator init --help
```

Expected: the installed version and help. Activation applies to this shell only.
An explicit interpreter such as `"$runtime/bin/python"` also works without activation.

## Create your first novel

Choose a writable parent folder **outside the framework and all other Git
repositories**. For example, create and enter a `Novels` folder under Documents.
Run the following from that parent, after activating the environment:

```text
novel-creator init 'My Novel'
```

PowerShell without activation uses `& $novelCommand init 'My Novel'`.
Expected: a ready message identifying the independent `My Novel` folder, the
exact Python interpreter, the pinned launcher and the getting-started guide.
`My Novel` is a provisional working title; language defaults to English and
other creative choices stay unknown. No story questionnaire or brief file is needed.

If the result says **saved; recovery required**, initialization is not ready for
further writes. Follow the recovery instructions below. Repeating init for a known
novel preserves its settings and installed workflows; it does not apply new options.

## Open the novel in Codex

Open the **created novel folder**, not its parent or the framework checkout, as
your Codex project. Copy the exact **Python interpreter** path printed by init
into your first request so Codex uses that environment for the pinned launcher.
Opening Codex from a desktop icon does not inherit your activated terminal.

Send this in Codex, replacing the path with your printed path:

> Use the Python interpreter at PATH for this novel's `.novel-creator/run.py`.
> Run `$novel-init`. I have no story idea yet. Guide me with one question at a time.

You can skip creative questions, keep unknown choices unknown, provide a concept
you already have, or choose Icelandic later. Setup does not require brainstorming.
Suggestions become canon only through your clear acceptance. Each conversational
exchange is saved before its exact reply is displayed. A confirmed saved checkpoint
is the confirmation to look for; an unsaved/pending warning is not a successful save.

## Inspect what was saved

In a terminal in the novel folder, use the same environment's Python:

```powershell
& $novelPython .novel-creator/run.py context --novel . --json
& $novelPython .novel-creator/run.py session list --novel . --json
& $novelPython .novel-creator/run.py inspect --novel . --kind novel_project --json
```

```bash
"$runtime/bin/python" .novel-creator/run.py context --novel . --json
"$runtime/bin/python" .novel-creator/run.py session list --novel . --json
"$runtime/bin/python" .novel-creator/run.py inspect --novel . --kind novel_project --json
```

Expected: a confirmed checkpoint, saved project settings and any sessions. No
sessions is normal before the first conversational session. Inspection is read-only;
it does not establish story facts. Codex can also use `$novel-inspect`.

For a new or explicitly updated 0.6.0 legacy bundle, ordinary agent turns instead
start with `context --view working`, then retrieve relevant complete records and
sources on demand. See [working context](working-context.md) for `--focus`,
`--query`, `--limit`, omissions and freshness. `--view current` omits archived
exchanges; full remains the compatible default above. These options require the
new pinned runtime: package installation alone does not change an existing book.
Use the explicit supported update below after 0.6.0 is published; do not copy
source workflows over an older runtime. Existing Markdown notebooks remain
unchanged and use native topic files rather than these commands.

## Return later

Open the same novel folder in Codex and ask to resume; `$novel-resume` is an
explicit entry point. The agent should retain the initialization tool result's
interpreter and follow the installed entry guide's read-only discovery when it
is unavailable, before asking you for an environment. Supply a known compatible
interpreter only if needed. Do not initialize again
to resume. In a new terminal, set the variables again and reactivate the existing
environment, or use the interpreter's full path. To check the selected interpreter:

```text
python -c "import sys; print(sys.executable)"
```

The printed path should belong to your Novel Creator environment. Moving a novel
to another machine requires a compatible Python environment there; the agent
must verify it, and may need your help finding it. No framework checkout or history
rewrite is needed.

## Optional settings

The name is one folder component. `--path` selects the **complete destination**,
not a parent folder. `--title` can differ from the folder name. Options follow
the name directly; no extra `--` separator is needed.

```powershell
novel-creator init 'Bref' --path "$env:USERPROFILE/Documents/Novels/Bref" --title 'Bréf frá morgundeginum' --language is
```

```bash
novel-creator init 'Bref' --path "$HOME/Novels/Bref" --title 'Bréf frá morgundeginum' --language is
```

Replace example paths with unused independent targets. Quotes preserve spaces and
Icelandic characters. `--language en` explicitly selects English; omitted language
defaults to English. Add `--json` for one machine-readable result instead of prose.
Use `init --help` for supported options. Legacy `init --path PATH --brief-file FILE
--json` remains available; do not combine a brief file with a name/title/language.

## Troubleshooting

- **Command not found:** use the environment's full executable path or reactivate
  it. Confirm `--version` and the selected `sys.executable`. Do not reinstall into
  arbitrary system Python environments to fix a PATH mismatch.
- **Missing prerequisite:** check Python/Git versions and pip/venv availability.
  If package download/dependency resolution fails, initialization has not completed;
  check the release's verified name/version and your connection. A missing validator
  dependency means the selected interpreter is wrong or its installation needs repair.
- **Git identity missing:** configure your intended author/committer identity before
  retrying. The application does not choose or change identity for you.
- **Unsafe destination:** choose a fresh or empty folder outside all repositories.
  Unrelated occupied folders, nested repositories and redirected paths are refused.
  Existing novels are continued, not replaced; new flags never silently update them.
- **Permissions failure:** inspect the named folder/access problem and use a location
  you can write. A host sandbox may require narrowly scoped filesystem approval.
  Do not disable protections, steal locks or erase saved evidence to make it work.
- **Interrupted initialization:** keep the original command choices and all partial
  files. Retry the same initialization; changed choices/files cause a conflict instead
  of replacement. For a reported pending exchange, use read-only recovery inspection
  with its printed exchange ID and the exact interpreter, then follow explicit retry
  guidance against the confirmed head. Never delete receipts or reset history.

From the novel folder, replace EXCHANGE_ID and CONFIRMED_HEAD with the actual
diagnostic values (for an unpublished initial bootstrap, the expected head is `unborn`):

```text
python .novel-creator/run.py recover --novel . --exchange EXCHANGE_ID --json
python .novel-creator/run.py recover --novel . --exchange EXCHANGE_ID --retry --expected-head CONFIRMED_HEAD --json
```

Use the explicit environment interpreter instead of `python` if it is not activated.
A saved exchange needing cleanup stays saved; do not replay it. Missing or mismatched
evidence means preserve the project and investigate before further writes.

An older novel may lack this guide. The installed command then labels a package-guide
fallback; reading it changes nothing in that novel. Continue using the older novel's
pinned workflows. Installing/upgrading the package never upgrades an existing novel.

## Updating an existing book

The 0.3.0 controller implements explicit preview, application and recovery.
Published 0.1.0/0.2.0 book launchers do not provide these commands. Install the
updater-capable 0.3.0 package only after its release is available; during candidate
verification use the identified candidate archive. Package installation alone
never changes the pinned framework in an existing book.

Install the external controller in a separate Python
environment outside the book and retain its absolute interpreter path as the
external controller. No framework checkout, GitHub contribution access or model
key is required. Use the intended book runtime explicitly if it differs:

```powershell
& 'C:\path\to\controller\python.exe' -I -B -m novel_creator update --novel 'C:\Novels\MyNovel' --python 'C:\path\to\runtime\python.exe' --json
& 'C:\path\to\controller\python.exe' -I -B -m novel_creator update status --novel 'C:\Novels\MyNovel' --json
```

Check only when requested. The check selects a published stable release and
verifies its archive, runtime prerequisites and compatibility. It writes private
preparation/preview data outside the book, then reports the exact version, hashes,
reviewed HEAD, runtime interpreter and proposed paths. A same-version result is
`already_current`; unavailable release information is an error, not proof that
the book is current. Releases without update protocol 1 cannot be update targets.

A preview does not authorize changing the book. Review its target, paths and
blockers. After requesting that exact update, use the returned preview ID,
version and reviewed HEAD. The configured runtime is bound into the preview:

```powershell
& 'C:\path\to\controller\python.exe' -I -B -m novel_creator update --novel 'C:\Novels\MyNovel' --apply --preview PREVIEW_ID --version VERSION --expected-head REVIEWED_HEAD --confirm-quiescent --json
```

For initial 0.1.0/0.2.0 updates, close every other book client and keep them closed
through application and any external recovery. Add `--confirm-quiescent` only
after confirming that lifecycle. It does not discover/stop processes or bypass
locks: already-loaded legacy code cannot be retroactively fenced (FUP-001).
Restart through the guarded launcher after success. Updates of guarded format-2
books do not require that legacy confirmation flag.

If interrupted, preserve the operation ID, files and locks. Keep legacy clients
closed and inspect using the external controller. A failure can occur after the
update commit was published:

```powershell
& 'C:\path\to\controller\python.exe' -I -B -m novel_creator update recover --novel 'C:\Novels\MyNovel' --operation OPERATION_ID --json
& 'C:\path\to\controller\python.exe' -I -B -m novel_creator update recover --novel 'C:\Novels\MyNovel' --operation OPERATION_ID --retry --expected-head OBSERVED_HEAD --json
```

Run retry only after reviewing an eligible inspection and explicitly requesting
it. Use the exact currently observed HEAD, not a guessed or stale value. Status
and recovery inspection are local/read-only and never remove locks. Unproven
ownership or changed evidence blocks retry. Recovery uses the exact local
artifact and candidate; there is no implicit download, rollback or second commit.

Only `ready: true` with no cleanup means completion. Reload book instructions and
skill discovery, then read committed context before writing. Manuscript, saved
records, custom instructions, settings, unrelated staging and retrospective
grants/notices retain their meaning. The update is not a creative exchange and
does not start a retrospective. Missing runtime prerequisites require explicit
environment repair; no global package installation happens during an update.

In Bash, the same commands use the quoted executable path directly instead of
PowerShell's `&`. The shared [update workflow](update.md) contains the complete
writer/host protocol. See the development qualification ledger for actual CLI,
historical-wheel and platform results; native Codex acceptance is separate and
must not be inferred from scripted tests.

## Optional contributor retrospectives

New novels include an optional retrospective workflow, disabled by default for
everyone. It can review completed requests and prepare a focused, checked draft
PR for Novel Creator. Normal writing needs no GitHub CLI or framework checkout.
Existing novels keep their pinned bundle when you upgrade the package.

Contributors need a separate local Novel Creator checkout, the GitHub CLI (`gh`)
and existing authenticated upstream push access. Do not use your novel directory
as the framework checkout. In the following PowerShell example, replace the paths
and use the exact Python interpreter reported by initialization:

```powershell
& 'C:\path\to\python.exe' .novel-creator/run.py retro status --novel 'C:\Novels\MyNovel' --json
& 'C:\path\to\python.exe' .novel-creator/run.py retro enable --novel 'C:\Novels\MyNovel' --checkout 'C:\source\novel-creator' --authorize-draft-prs --json
& 'C:\path\to\python.exe' .novel-creator/run.py retro disable --novel 'C:\Novels\MyNovel' --json
```

Enable is explicit authorization for local framework fixes, checks, branch pushes
and automatic **draft** PRs to bjarkig82/novel-creator. It never authorizes merging,
deploying, manuscript changes, credentials or package publication. Disable prevents
subsequent contribution operations and retains prior work. Grants belong to this
novel, location, machine and account; copying/moving settings does not enable a
new location. Missing authentication/access leaves participation off.

PR or problem notices appear briefly in the next normally saved reply, without a
status request. No-action outcomes remain local unless requested. If there is no
next reply, the notice remains pending. Writing saves and exact responses retain
their existing recovery rules; a retrospective result is never an unsaved suffix.

Use `retro status --run UUID`, then `retro resume --run UUID` with the same `--novel`
and `--json` to inspect/reconcile existing work. Disabled recovery requires explicit
re-enablement first; it makes no repository requests while disabled. Enabling alone
does not resume work. `retro release --run UUID --confirm-abandon` is inspected
abandonment, preserving files/PRs and blocked by live locks or uncertain publication.
Never delete receipts, worktrees or locks to force recovery. Read the installed
`retrospective.md` for the complete protocol and limitations. Local state cannot
prove human intent against malicious code running as the same OS user.
