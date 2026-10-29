# Getting started with Novel Creator

Novel Creator helps you set up a novel, explore ideas, keep decisions and questions,
and return to saved conversations in Codex. You can start with no story idea.
Each novel is its own local Git repository. Initialization finishes before creative
setup begins; you choose when to start brainstorming.

**Release status:** the simple initializer is available in the development package.
Public package publication and name ownership have not yet been verified. Only use
the public install-by-name examples below after the project's release announcement
confirms the package name/version. Until then, install the maintainer's verified
wheel in the same environment instead. Do not install an unverified namesake.

## Before you begin

- Windows PowerShell or Linux Bash, with Python >=3.11 and pip/venv support.
- Git >=2.39 and your own Git identity already configured.
- Codex with access to the novel folder and its Python interpreter.
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

## Return later

Open the same novel folder in Codex and invoke `$novel-resume`. Supply the same
interpreter path again if the new chat does not have it. Do not initialize again
to resume. In a new terminal, set the variables again and reactivate the existing
environment, or use the interpreter's full path. To check the selected interpreter:

```text
python -c "import sys; print(sys.executable)"
```

The printed path should belong to your Novel Creator environment. Moving a novel
to another machine requires a compatible Python environment there; give Codex its
new interpreter path. No framework checkout or history rewrite is needed.

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
