# Novel Creator

Novel Creator is a writing toolkit for planning, drafting, and revising a novel
with an AI assistant in Codex or Claude Code. Start with a complete premise, a
rough idea, or a blank page. You make the creative decisions.

Each new novel gets its own **story notebook**. It holds your ideas, decisions,
open questions, and manuscript drafts in readable Markdown files. Git keeps a
local history of saved changes. When you return to the folder, the assistant
can pick up from the saved notes.

## What you can do

| If you want to… | Try asking your assistant |
| --- | --- |
| Find a book idea | “I want to write a novel, but I don't have an idea yet. Ask me one question at a time.” |
| Develop a character, plot, or setting | “Help me explore why the lighthouse keeper would hide the first letter.” |
| Create a supporting character | “Propose a profile for the night ferry operator. She knows the lighthouse keeper from school.” |
| Turn notes into an outline | “Propose a chapter outline from my notes and flag decisions I still need to make.” |
| Draft or revise a scene | “Draft the scene where the first letter arrives. Keep the point of view with the lighthouse keeper.” |
| Check continuity | “Analyze chapter two against the outline and flag contradictions. Keep your findings in chat.” |
| Pick up where you left off | “Remind me what we decided about the letters and which questions are still open.” |

The notebook keeps confirmed story facts, suggestions, and unanswered questions
distinct. Say which ideas you want to make part of the story. The assistant
updates relevant notes as you work and drafts scenes or chapters when you ask.
Proposed character profiles stay in chat until you explicitly ask to save them.
[Character profile examples](https://github.com/bjarkig82/novel-creator/blob/main/docs/side-characters.md).

## Create your first notebook

### 1. Install Novel Creator and create a folder

For the setup below, you'll need access to Codex, **Python 3.11 or
newer**, and **Git 2.39 or newer** with your name and email configured. Git uses
that identity for the local history. [Set up your Git identity](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup#_your_identity).

Run the commands for your system to install Novel Creator 0.10.6 in a
separate Python environment and create a notebook called **My Novel**.
Use a new folder outside any existing Git repository. Its parent folder must
already exist.

**Windows PowerShell**

```powershell
py -3 -m venv "$env:USERPROFILE\.novel-creator-venv"
& "$env:USERPROFILE\.novel-creator-venv\Scripts\python.exe" -m pip install novel-creator==0.10.6
& "$env:USERPROFILE\.novel-creator-venv\Scripts\novel-creator.exe" notebook init "My Novel" --path "$env:USERPROFILE\My Novel" --language en
```

**Linux Bash**

```bash
python3 -m venv "$HOME/.novel-creator-venv"
"$HOME/.novel-creator-venv/bin/python" -m pip install novel-creator==0.10.6
"$HOME/.novel-creator-venv/bin/novel-creator" notebook init "My Novel" --path "$HOME/My Novel" --language en
```

Use `--language is` for Icelandic. Once the package is installed, you can also
ask Codex to create the notebook for you by giving it the title, language, and
full path to the new folder. [Agent-led setup](https://github.com/bjarkig82/novel-creator/blob/main/workflows/start-here.md#ask-your-agent-to-set-up-a-story).

For Claude Code or a plugin-based setup in Codex, follow the marketplace
installation instructions. Package and setup checks cover Windows and Linux.
Native skill discovery and specialist interactions depend on the host and remain
unverified. macOS support is deferred. [Marketplace setup](https://github.com/bjarkig82/novel-creator/blob/main/docs/plugin-marketplaces.md).

### 2. Open the novel folder and start writing

Open **My Novel** itself as the project folder in your assistant. Ask it to read
the project instructions and try one of the prompts above. In a standalone Codex
notebook, you can also type `$novel-help` in chat to see available writing tools
and get suggestions for a next step.

To resume on another day, reopen the same folder and tell the assistant what
you want to work on. You can open the Markdown files in a text editor to read
your notes and drafts. The notebook files and Git history live in that folder.
[More examples for drafting, revising, and reviewing](https://github.com/bjarkig82/novel-creator/blob/main/docs/writing-agents-usage.md).

## Already have a Novel Creator project?

Open the existing project folder to continue. Older projects created with
`novel-creator init` use the legacy workflow. [Legacy writing guide](https://github.com/bjarkig82/novel-creator/blob/main/workflows/everyday-writing.md).

To add newer tools to an existing notebook or legacy novel, follow the
project-specific upgrade steps after installing the package. Each project keeps
its own copy of its instructions. [Upgrade guide for version 0.10.6](https://github.com/bjarkig82/novel-creator/blob/main/docs/upgrading-projects.md#upgrade-to-0106).

<a id="unreleased-session-issue-retrospectives"></a>

## Review a writing session

You can ask the assistant to review a session for workflow problems. Findings
stay local unless you explicitly approve the exact GitHub issue and any
attachments to share. [Session review guide](https://github.com/bjarkig82/novel-creator/blob/main/workflows/retrospective.md).

## Releases

- [Novel Creator 0.10.6 on PyPI](https://pypi.org/project/novel-creator/0.10.6/)
- [0.10.6 release notes and compatibility](https://github.com/bjarkig82/novel-creator/blob/main/docs/releases/0.10.6.md)
- [Release history](https://github.com/bjarkig82/novel-creator/blob/main/docs/releases/README.md)

## Development

- [Application functionality](https://github.com/bjarkig82/novel-creator/blob/main/docs/functionality.md)
- [Development setup and packaging](https://github.com/bjarkig82/novel-creator/blob/main/docs/development.md)
- [Testing guide](https://github.com/bjarkig82/novel-creator/blob/main/docs/testing-and-completion-guide.md)
- [Legacy save recovery commands](https://github.com/bjarkig82/novel-creator/blob/main/workflows/getting-started.md#troubleshooting)
