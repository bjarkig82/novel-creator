# Start here: Novel Creator for writers

Novel Creator helps you develop a novel through conversations in Codex. You can
start with a detailed idea, a few loose thoughts, or no idea at all. It keeps a
local record of your ideas, decisions, and unanswered questions so you can return
to them later.

You make the creative decisions. Codex can suggest possibilities, ask questions,
and help you explore them. A suggestion becomes an established story fact only
when you clearly accept it. You can change your mind later and keep a record of
what changed.

## Choose your starting point

- **Someone has already set things up for you:** open your novel folder in Codex
  and go straight to [Everyday writing](everyday-writing.md). Ask your helper for
  the novel folder and its Python interpreter path before you begin.
- **You are setting up your own computer:** follow [First-time setup](beginner-setup.md).
  It separates Windows and Linux instructions and explains the current Mac limits.
- **You already have a saved novel:** use the
  [returning-later instructions](everyday-writing.md#return-later).
- **You need detailed commands, updates, or recovery:** use the existing
  [technical getting-started guide](getting-started.md).

## What you will use

There are three parts to the setup:

1. **Codex** is the application where you talk about your story.
2. **Novel Creator** gives Codex instructions and tools for organizing and saving
   that work. It is installed using Python, a program that runs those tools.
3. **Your novel folder** holds that novel's saved records and local history.
   Each novel has its own folder. Git, a history tool, records the saved changes.

Once setup is complete, most of your work happens by typing ordinary messages in
Codex. You do not need to edit Python code, write JSON files, download the
framework source, or create a GitHub account to use the writing workflow.

This release focuses on setup, planning, brainstorming, story decisions, and
returning to saved conversations. Saving those records does not write chapters
or edit your manuscript. A finished manuscript is separate work.

## Which computer can I use?

These are Novel Creator's recorded testing limits; an application being available
on a platform does not mean this framework's whole writing workflow was tested there.

| Computer | What has been tested | What this means for you |
| --- | --- | --- |
| Windows | Package installation and the local Codex Desktop setup, save, inspect, and resume workflow | This is the tested conversational route. Start with the Windows setup instructions. |
| Linux | Package installation and terminal commands | The Codex conversation workflow remains unverified. Setup explains where to stop if required capabilities are missing. |
| Mac | Framework support is deferred | Read the Mac section for limits and alternatives. This guide does not offer a supported native Mac setup. |

## What gets saved, and where?

The installed writing workflow saves each conversation exchange before showing
its prepared reply. It also records the related story decisions and questions.
Look for a confirmed saved checkpoint. A save warning means you need to resolve
the problem before treating pending work as saved.

Those saves and Git history are **local to your computer**. Novel Creator does
not automatically upload or back up your novel. Local history helps you inspect
earlier work, but it cannot protect against losing the computer or its drive.
See [keeping a backup](everyday-writing.md#keep-a-separate-backup).

Installation needs internet access to download the software. Creating the local
novel folder can then work offline. Conversations still depend on your Codex
account, access, and connectivity. Novel Creator itself does not require a
separate model API key; see [OpenAI's application documentation](https://learn.chatgpt.com/docs/app)
for current account and application setup information.

## A few useful words

| Word | Plain-language meaning |
| --- | --- |
| Terminal | A window where you type computer commands. On Windows, use PowerShell; on Linux, use Bash. |
| Path | The address of a file or folder on your computer. Quotes keep an address containing spaces together. |
| Python interpreter | The particular Python program used to run Novel Creator. Keep the exact path printed during setup. |
| Environment or runtime | A separate folder containing Python and Novel Creator's dependencies. Keep it outside your novel. |
| Skill | A named set of instructions Codex can follow, such as `$novel-resume`. Type it in a Codex message. |
| Session | A saved conversation with a topic and a mode, such as guided brainstorming. |
| Proposal | An idea you have not yet accepted as a story fact. |
| Canon | The story facts you have clearly established. |
| Checkpoint | An identified saved state that the tools can confirm and inspect. |

Next: [set up your computer](beginner-setup.md) or
[start working on your story](everyday-writing.md).
