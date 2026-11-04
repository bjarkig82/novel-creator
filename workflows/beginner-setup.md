# First-time setup

[Start here](start-here.md) · [Everyday writing](everyday-writing.md)

This guide takes you from installing the tools to opening your first novel in
Codex. If someone has already prepared your novel folder and Python environment,
skip to [Everyday writing](everyday-writing.md).

Choose your computer: [Windows](#windows) · [Linux](#linux) · [Mac](#mac).
You only need the instructions for your computer.

## Before you start

- You need Python **3.11 or newer**, Git **2.39 or newer**, and access to Codex.
  Python 3.13 is the version used in the release's automated installation checks.
- You need internet access to download the software and whatever access your
  Codex account requires for conversations. The framework needs no separate model API key.
- Use a computer where you can install software and create folders. On a managed
  work computer, you may need help from your administrator.

The commands below install the published **Novel Creator 0.3.0**, verified against
[PyPI's package metadata](https://pypi.org/pypi/novel-creator/json) on **2026-11-04**.
These beginner pages are newer than the published package and will ship in a
future release; an existing installed novel may not contain them. Keep this guide
open while following along.

Commands labeled **Terminal commands** go in PowerShell or Bash. Text labeled
**Message to send in Codex** goes in the Codex conversation. Do not type the
surrounding Markdown marks or a terminal's prompt such as `PS C:\>` or `$`.
Run commands one line at a time, pressing Enter after each line. If a command
reports an error, stop at that step and use [Troubleshooting](#troubleshooting).

We will call the example novel **My Novel**. It is a working title you can change
later. Its folder and the separate `NovelCreatorRuntime` folder must be outside
any existing Git repository, including a downloaded framework checkout.

## Windows

### 1. Install the tools and open PowerShell

Use the official [Python for Windows downloads](https://www.python.org/downloads/windows/)
and [Windows installation instructions](https://docs.python.org/3/using/windows.html).
Python 3.13 is a suitable choice; use a normal installation with pip and virtual
environment support, rather than an embeddable package. If the installer offers
**Add python.exe to PATH**, select it so the terminal can find Python.

Install [Git for Windows](https://git-scm.com/install/windows). Ensure its installer
allows Git to be used from the command line. Install and sign in to Codex using
[OpenAI's Windows application instructions](https://learn.chatgpt.com/docs/app/windows).
Choose the Codex experience when the application offers multiple experiences.

Open the Start menu, search for **PowerShell**, and open it. You do not need an
administrator window. If it was already open during installation, close it and
open a new window so it can find the installed tools.

**Terminal commands — PowerShell:**

```powershell
Set-Location $env:USERPROFILE
python --version
git --version
```

**Expected:** Python reports 3.11 or newer and Git reports 2.39 or newer.
For example, `Python 3.13.x` is suitable. If `python` fails but `py --version`
reports a suitable version, use `py` instead of `python` when creating the
environment in step 3. Later commands use the environment's exact executable.

### 2. Check the name attached to your saved history

Git records an author name and email address with each save. You do not need a
GitHub account. First check whether your identity is already configured.

**Terminal commands — PowerShell:**

```powershell
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

**Expected:** both commands show your intended name and email, followed by numbers
representing the time. If they are correct, leave them as they are and continue.

If Git reports a missing identity, replace **both** example values below with
the name and email you want attached to your history, then run the commands.
These settings apply to all Git projects for your computer account; ask your
helper before changing an existing identity on a shared setup. You choose these
values yourself. Novel Creator does not configure them for you.

**Terminal commands — PowerShell, only if identity is missing:**

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

**Expected:** both checks now show the identity you chose. See
[Git's identity instructions](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
if you need more detail.

### 3. Install Novel Creator in its own environment

The runtime folder keeps Novel Creator's dependencies together. It is separate
from the folder holding your story. Create it once and reuse it for later sessions
and other novels. If `NovelCreatorRuntime` already exists in your user folder,
do not recreate it; use [Reconnect after closing the terminal](#reconnect-after-closing-the-terminal)
or ask whoever prepared it to confirm the setup.

**Terminal commands — PowerShell:**

```powershell
$runtime = Join-Path $env:USERPROFILE 'NovelCreatorRuntime'
python -m venv $runtime
$novelPython = Join-Path $runtime 'Scripts/python.exe'
& $novelPython -m pip install novel-creator==0.3.0
$novelCommand = Join-Path $runtime 'Scripts/novel-creator.exe'
& $novelCommand --version
```

**Expected:** installation completes without an error and the final command reports
0.3.0. Download and installation messages are normal. The `&` tells PowerShell to
run the executable whose path is stored in the variable. No activation script
or execution-policy change is needed.

### 4. Create your novel

The following creates a `Novels` parent folder in your user folder, then creates
`My Novel` inside it. The parent folder may already exist. The new novel destination
must be unused or empty, and outside all other Git repositories. Do not put the
novel inside `NovelCreatorRuntime`.

**Terminal commands — PowerShell:**

```powershell
$novels = Join-Path $env:USERPROFILE 'Novels'
New-Item -ItemType Directory -Path $novels -Force | Out-Null
Set-Location $novels
& $novelCommand init 'My Novel'
```

**Expected:** a ready message identifies the created novel folder and the Python
interpreter used for it. Copy the full interpreter path into a note for later,
along with the novel folder path. It will normally end in
`NovelCreatorRuntime\Scripts\python.exe`.

English is the default; other creative choices can stay unknown. A ready folder
does not mean you have already started a creative conversation. If you see
**saved; recovery required** or another warning, stop and follow the
[save-warning guidance](#a-save-or-initialization-warning-appears).

### 5. Open the novel in Codex

In Codex, open or add the folder printed by initialization as a project. Select
**My Novel itself**, rather than `Novels`, the runtime folder, or the framework's
source folder. The expected folder contains an `AGENTS.md` file and a hidden
`.novel-creator` folder; you do not need to edit them.

Start a chat in that project. Replace `PASTE_YOUR_PYTHON_PATH_HERE` with the full
interpreter path you saved in step 4, keeping the quotes around it.

**Message to send in Codex:**

> Use the Python interpreter at "PASTE_YOUR_PYTHON_PATH_HERE" for this novel's
> `.novel-creator/run.py`. Run `$novel-init`. I have no story idea yet.
> Guide me with one question at a time.

**Expected:** Codex reads the installed workflow and begins conversational setup.
You can skip questions. Its story replies follow the installed save-before-display
workflow. If it reports missing capture tools, a failed save, or a permission
problem, use [Troubleshooting](#troubleshooting) before continuing.

The Python path matters even if Codex was opened from a desktop icon: it does not
automatically inherit your terminal's settings.

Next: [Everyday writing](everyday-writing.md).

## Linux

Package installation and terminal commands have Linux test coverage. **Novel
Creator's Codex conversation, save, and resume integration remains unverified on
Linux.** You can prepare and inspect a novel using the steps below, but completing
installation does not establish that the conversation workflow will work.

### 1. Install prerequisites and open a Bash terminal

Open your distribution's Terminal application and use Bash for these commands.
Use its software manager to install Python 3.11 or newer with pip and `venv`
support, plus Git 2.39 or newer. See the official
[Python Linux notes](https://docs.python.org/3/using/unix.html) and
[Git Linux instructions](https://git-scm.com/install/linux).
On Ubuntu or Debian, the usual prerequisite packages are installed as follows;
other distributions use different package managers.

**Terminal commands — Bash, Ubuntu/Debian only:**

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

**Expected:** the package manager finishes successfully. It may ask for your
computer password. Older distribution releases may provide versions below the
minimum, so check before continuing.

**Terminal commands — Bash:**

```bash
cd "$HOME"
python3 --version
git --version
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

**Expected:** compatible versions and your intended Git author and committer
identity. If the identity is missing, replace both values below with your chosen
name and email. These settings affect all Git projects for your computer account;
leave an existing correct identity alone.

**Terminal commands — Bash, only if identity is missing:**

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

**Expected:** both checks show the identity you chose.

### 2. Install the framework and create your novel

Use a fresh `NovelCreatorRuntime` folder outside all Git repositories. If it
already exists, [reconnect](#reconnect-after-closing-the-terminal) rather than
recreating it. Keep the novel outside that environment and all other repositories.

**Terminal commands — Bash:**

```bash
runtime="$HOME/NovelCreatorRuntime"
python3 -m venv "$runtime"
"$runtime/bin/python" -m pip install novel-creator==0.3.0
"$runtime/bin/novel-creator" --version
mkdir -p "$HOME/Novels"
cd "$HOME/Novels"
"$runtime/bin/novel-creator" init 'My Novel'
```

**Expected:** version 0.3.0 and a ready message identifying the new novel folder
and its interpreter. Keep both paths. As on Windows, `My Novel` must be an unused
or empty destination. A warning is a reason to stop rather than assume readiness.

### 3. Check the local records

**Terminal commands — Bash:**

```bash
cd "$HOME/Novels/My Novel"
"$runtime/bin/python" .novel-creator/run.py context --novel . --json
"$runtime/bin/python" .novel-creator/run.py session list --novel . --json
```

**Expected:** successful results with a saved checkpoint and project settings.
The tools print structured text called JSON. There may be no sessions yet;
that is normal before the first conversation. These checks only read information.

### 4. Understand the Codex boundary before writing

Use [OpenAI's current application instructions](https://learn.chatgpt.com/docs/app)
to set up a local Codex host for your Linux computer. Open
`$HOME/Novels/My Novel` as its project and use the first Codex message from the
Windows section, substituting the Linux interpreter path printed during your setup.

This is an **unverified conversation route**. The installed adapter requires a
native tool named `read_thread` to capture your actual message exactly. If the host
cannot provide it, stop before creative work. Do not ask it to reconstruct messages
or bypass capture to make saving appear successful. A working Codex terminal
application alone does not prove that this capability is available.

Use the [tested Windows route](#windows) if you need the recorded end-to-end
workflow. See [Everyday writing](everyday-writing.md) for how sessions are intended
to work once the host requirements are met.

## Mac

Native Mac support for Novel Creator is deferred. Codex being available on Mac
does not establish framework compatibility. In particular, current framework
update/recovery ownership checks rely on Windows APIs or Linux `/proc` files;
there is no native macOS implementation of those checks.

This guide therefore does not give native Mac installation commands. For the
tested conversational route, use a Windows computer you can access, or ask a
helper to prepare a Windows environment that meets the prerequisites. Run both
Codex and the novel's Python tools there. A Linux environment is another option
for the tested local terminal operations, with the conversation limits described
above. Virtual or remote environments have not been separately qualified here.

You can read [Everyday writing](everyday-writing.md) on any computer to understand
the workflow, even if you are not yet able to run it locally.

## Reconnect after closing the terminal

Closing the terminal loses variables such as `$novelPython`; it does not remove
the installed software or your novel. For a default installation, reopen the
appropriate terminal and run the following. If a helper used other locations,
use the paths they gave you instead.

**Terminal commands — PowerShell:**

```powershell
$runtime = Join-Path $env:USERPROFILE 'NovelCreatorRuntime'
$novelPython = Join-Path $runtime 'Scripts/python.exe'
$novelCommand = Join-Path $runtime 'Scripts/novel-creator.exe'
& $novelPython -c "import sys; print(sys.executable)"
Set-Location (Join-Path $env:USERPROFILE 'Novels/My Novel')
```

**Terminal commands — Bash:**

```bash
runtime="$HOME/NovelCreatorRuntime"
"$runtime/bin/python" -c 'import sys; print(sys.executable)'
cd "$HOME/Novels/My Novel"
```

**Expected:** the interpreter path belongs to `NovelCreatorRuntime` and the
terminal is now in your novel folder. Copy the printed interpreter path into a
new Codex chat when needed, then use `$novel-resume`. Do not run initialization
again just to return to a saved novel.

## Troubleshooting

### A command is not found

If `python` or `git` is not recognized, reopen the terminal after installing it
and repeat the version checks. On Windows, try the `py` alternative described
in step 1. If needed, have a helper check the installation and PATH setting.

For Novel Creator, use the explicit executable paths shown above. A short
`novel-creator` command is not expected to work without environment activation.
If `$novelPython` is empty or `$runtime` is unset, use the reconnect section.
Do not reinstall into random Python environments to fix a missing short command.

### Git asks who you are

Return to your platform's identity step and configure your chosen name and
email only if missing. The framework does not invent an identity. If versions
or dependencies are missing, fix that step before retrying initialization.

### The folder is refused, or Codex cannot see the novel

Check the exact folder path. New novels must be outside every existing Git
repository; an occupied unrelated folder will be refused. Choose another unused
destination instead of deleting its contents. If `My Novel` is already a recognized
novel, open it and resume; repeating initialization preserves its existing setup.

In Codex, select the created `My Novel` folder itself. Opening the parent folder,
runtime, or framework source does not select your novel. Keep hidden framework
files in place.

### Codex does not recognize the skills

Confirm you opened the novel project and supplied its Python interpreter path.
Reopen the project or start a new chat so Codex can rediscover its installed
skills. You can send this explicit request:

**Message to send in Codex:**

> Read this novel's `.agents/skills/novel-init/SKILL.md` and follow its installed
> workflow using the Python interpreter path I supplied. If a required file or
> capture tool is unavailable, explain what is missing before making changes.

**Expected:** Codex loads the actual installed instructions, or identifies a
specific missing capability. Do not download replacement instructions into an
existing novel or substitute the latest source for its pinned version.

### A save or initialization warning appears

Keep the exact error message, novel folder path, last confirmed checkpoint, and
any pending exchange ID. A permission prompt can require access to a specific
folder or interpreter; review that scope rather than disabling protections.
Missing capture tools cannot be repaired by granting filesystem access.

Pause creative changes if saving is pending or failed. Ask Codex or a helper to
inspect the state using the [technical recovery instructions](getting-started.md#troubleshooting)
before an explicit retry. An interrupted initialization must retain its original
command choices and files. A published save needing cleanup must not be replayed.
Do not delete receipts or locks, reset Git history, or recreate the novel to clear
a warning.

### You want a newer framework version

Your novel keeps the framework version installed in it. Installing a newer Python
package alone does not update an existing novel. See
[Updating an existing book](getting-started.md#updating-an-existing-book) for the
separate preview-and-approval workflow and its release requirements. You do not
need to enable contributor retrospectives or install GitHub tools to write.

Next: [Everyday writing](everyday-writing.md).
