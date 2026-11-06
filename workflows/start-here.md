# Start here: Novel Creator for writers

Novel Creator helps you develop a novel through conversations in Codex. You can
start with a detailed idea, a few loose thoughts, or no idea at all. It keeps a
local record of your ideas, decisions, and unanswered questions so you can return
to them later.

You make the creative decisions. Codex can suggest possibilities, ask questions,
and help you explore them. A suggestion becomes an established story fact only
when you clearly accept it. You can change your mind later and keep a record of
what changed.

## Ask your agent to set up a story

Ask in the conversation where you are already working, for example: “Use Novel
Creator to create a new English story notebook called My Novel at
/path/to/My Novel. I don't have a story idea yet.” Replace the example with your
intended new folder. A temporary working title is fine; you do not need a concept,
genre or outline before setup.

The agent should establish the destination, language and working title from your
request and context, asking only for missing choices. It should use your configured
compatible Python environment and the actual installed CLI, check success, then
read the new project's `AGENTS.md`, linked guides and relevant project notes before
continuing in the same conversation. It should switch its working directory to
the story folder when possible and do this before any creative reply. Setup does
not require a new chat or repeated
skill commands, and starting brainstorming is your choice. Outlining remains an
explicit request.

The published 0.4.1 package includes notebook setup and the improved generated
instructions and continuation messages described here. Existing projects keep
their installed instructions; installing a package does not update them.

Setup needs Python 3.11+, the installed package, Git 2.39+, your configured Git
identity and access to the intended destination. Keep the Python environment
outside the story. The agent must preserve existing books and unrelated files,
confirm it is targeting the intended new destination outside all Git repositories,
and never overwrite an existing notebook destination. It must not invent a Git
identity, change global configuration or request a model key. If setup is partial,
preserve the evidence and follow its recovery message rather than overwrite it.

The host may not be able to access a newly created folder or change project
context. The agent should report the actual limit; you may need to select/open
that initialized folder in the host. Setup does not install global instructions,
guarantee global skill discovery or switch host projects automatically. Do not
initialize again after successful setup.

For later cloud or desktop sessions, select the story folder itself as the host
project root. Opening a parent workspace does not guarantee that the agent will
discover a nested story's instructions before answering. Tell the agent which
existing story to continue if the destination is ambiguous.

For an existing legacy novel, continue with its pinned launcher and installed
entry guide; creating a notebook does not convert it. Legacy setup preserves any
pre-existing `AGENTS.md` byte for byte, so that file may not direct future sessions
to Novel Creator. The initializing agent must explicitly read
`.novel-creator/workflows/entry.md` and load committed context even then; automatic
discovery in a later host session is not guaranteed. Native-input capture and
save-before-display safeguards still apply; unavailable host capabilities must
be disclosed before creative continuation.

Legacy setup returns its Python interpreter and launcher paths to the agent in
the tool result, so you do not need to repeat them in chat. When that result is
unavailable in a fresh or moved workspace, the agent should inspect actual CLI
and virtual-environment candidates and verify dependencies and read-only pinned
context before asking you about an environment. A conventional folder name alone
does not prove an interpreter is compatible. Machine paths are not committed to
your story, and notebook conversations do not need this legacy runtime discovery.

## New story notebook

Novel Creator 0.4.0 offers a separate Markdown notebook for a new novel. The agent
can execute the direct CLI fallback below in the configured environment, using
a new folder outside existing Git repositories:

```text
novel-creator notebook init "My Novel" --path "/path/to/My Novel" --language en
```

Choose `is` for Icelandic and use `--title` if you want a different working title.
After setup, read the generated instructions and continue as described above.
Ask for a brief
on a topic when you want one; recaps are not automatic. Python is needed for
setup, while Codex uses its native tools for the notebook. Existing novels stay
on the separate legacy workflow described below; this command does not convert
them. The notebook's Windows and Linux Codex Desktop conversations are still
unverified. The notebook evidence ledger is available in the source repository.

In a new notebook, you can say “I want to write a book, but I don't know what
about.” Guided conversation starts with your interests, a feeling or a rough
image, one question at a time. You do not have to choose a genre or invent a
character first. If you already want a character, place or plot, say so and
start there. You can also choose a method first, such as “Let's try mind mapping,”
and change focus whenever you like. Suggestions stay tentative until you choose.

Optional focused skills are `$novel-book-idea`, `$novel-premise`,
`$novel-character`, `$novel-plot` and `$novel-setting`; ordinary conversation
chooses a useful focus and method without requiring these commands. `$novel-outline` remains
an explicitly requested later option. These additions belong to newly initialized
notebooks. Package installation does not add them to existing notebooks
or change legacy brainstorming. These notebook features are not available from
the older published legacy releases.

New notebooks initialized from the unpublished 0.5.0 source candidate also
install six writing roles and guidance for on-demand scenes, chapters, research
and review. Open the initialized novel folder itself, then check whether your
actual Codex client supports custom agents and ongoing direct specialist turns.
Those native interactions remain unverified in the target desktop. Ordinary
requests such as “Let me work with the scene writer” require that host support;
missing capabilities must be disclosed. For practical examples and limits, read
`docs/writing-agents-usage.md` in the updated Novel Creator source checkout; that
guide is not installed in legacy novels. No repeated skill command, per-turn
Python or full questionnaire is required. These additions are absent from
published 0.4.1, leave existing notebooks and legacy novels unchanged, and
introduce no migration or updater command.

The rest of this page describes the existing legacy workflow.

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
