# Everyday writing with Novel Creator

[Start here](start-here.md) · [First-time setup](beginner-setup.md)

Use this guide once your novel folder and Python environment are ready. Most
steps below are **messages to send in Codex**, not terminal commands. You can
write in ordinary language; you do not need to repeat a skill name on every turn.
This page describes legacy novels. Native notebooks use their project instructions
and ordinary file/Git tools, without a Python interpreter during writing.

## Open the right project

Open your novel folder itself, such as **My Novel**, in Codex. A parent workspace
does not guarantee automatic discovery of a nested novel's instructions. Ask the
agent to read that folder's AGENTS.md and installed entry guide and load saved
context before answering creatively. Use the initialized folder; do not set it
up again. If you need manual environment help, use the
[reconnect instructions](beginner-setup.md#reconnect-after-closing-the-terminal).

The agent should retain the interpreter from successful initialization tool output.
In a fresh or moved workspace, it should inspect and verify actual environment
candidates as described in the installed entry guide before asking you. You need
not repeat a path already available to the agent. If no compatible environment
can be established, you can supply a known one with the optional message below.
Replace the placeholder with its exact path, keeping the quotes.

**Optional environment message:**

> Use the Python interpreter at "PASTE_YOUR_PYTHON_PATH_HERE" for this novel's
> `.novel-creator/run.py`.

The installed workflow reads the novel's saved context. It should explain any
unavailable records or required capabilities before continuing. On Linux the
conversation integration remains unverified; native Mac framework support is
deferred. See the [platform table](start-here.md#which-computer-can-i-use).

## Begin with as much or as little as you have

For a newly created novel, start conversational setup. You may already have done
this at the end of the setup guide; if so, continue that conversation.

**Message to send in Codex — starting without an idea:**

> Run `$novel-init`. I have no story idea yet. Ask me one question at a time.
> I may leave some answers undecided.

**Message to send in Codex — starting with an idea:**

> Run `$novel-init`. My starting idea is a lighthouse keeper who receives letters
> dated tomorrow. Help me explore it. The setting and ending are still undecided.

These are alternatives; send the one that fits you, or write your own. You can
use a temporary title, skip a question, or stop after setup. You do not have to
complete a questionnaire or settle every creative choice.

The working language defaults to English. You can ask to work in Icelandic or
revise preferences later. Changing a preference does not silently translate your
original concept or existing records.

**Message to send in Codex:**

> Please use Icelandic for our work on this novel. Keep existing names and
> original wording unchanged unless I ask for a change.

## Explore ideas in the way that suits you

When you are ready to brainstorm, use `$novel-brainstorm`.

**Message to send in Codex — guided exploration:**

> Run `$novel-brainstorm` in guided mode. Help me explore the keeper's motivation,
> one question at a time.

**Message to send in Codex — open exploration:**

> Switch to open brainstorming. Let me think aloud about the letters before
> offering suggestions.

You can change topics, ask for fewer suggestions, or leave something unresolved.
For example, send: "Let's leave the ending open and focus on the keeper's daily
life." Changing topics does not answer an earlier open question.

## Make your decisions clear

Ideas suggested by Codex remain proposals until you clearly accept them. Praise
such as "I like that" can be ambiguous if several ideas were suggested together.
Name the specific part you want to keep. Accepting one part does not accept all
the other details.

**Message to send in Codex:**

> Establish that the keeper's name is Mara. Leave the proposed island setting
> undecided. Do not establish the suggested family history.

You can also reject an idea or defer it: "Reject the idea that the letters are a
prank. Leave their actual origin undecided." An undecided idea is still available
to explore later.

## Change your mind without losing the earlier decision

Identify the existing fact and its replacement. Novel Creator records the revision
and retains the earlier version and its source for inspection.

**Message to send in Codex:**

> Revise the keeper's established name from Mara to Elin. Keep her role as the
> lighthouse keeper. Review recorded connections affected by that change.

If your request conflicts with another established decision, Codex should explain
the conflict and ask a focused question. Its review can only cover the connections
recorded in the project; it cannot guarantee that every implication was detected.
Changing a story fact does not authorize rewriting manuscript text.

## Ask what has been saved

**Message to send in Codex:**

> Run `$novel-inspect`. Summarize the established facts, unaccepted proposals,
> and open questions. Include the confirmed checkpoint and supporting record
> references. Tell me if any relevant information is unavailable.

The references connect the summary to saved records and revisions. You can ask
Codex to explain a reference or show an earlier version. Inspection reads existing
information; asking to inspect does not accept proposals or change story facts.

Every exchange in the installed conversation workflow is saved before its exact
prepared reply is displayed. Asking for a summary changes when you review the
work, rather than turning saving on. Look for confirmation of the saved checkpoint;
a failed or pending save is a reason to pause. If a reply was saved before an
interruption, resumption can offer its exact text without assuming you saw or
accepted it.

## Finish a session

**Message to send in Codex:**

> Close this session. Summarize the decisions, proposals, and open questions,
> and confirm the saved checkpoint. Do not start a new topic.

Wait for confirmation that the close and exchange were saved before closing
the application. If saving fails, keep the error and pending exchange details
and follow the [save-warning guidance](beginner-setup.md#a-save-or-initialization-warning-appears).

## Return later

Open the same novel folder in Codex. In a new chat, supply the same interpreter
path again, then send:

**Message to send in Codex:**

> Run `$novel-resume`. Show my saved sessions and restore the one I choose,
> including its focus, established decisions, and unanswered questions.

If there are several sessions, choose the one you want using the identifier Codex
shows; two sessions can have the same topic name. A session you explicitly closed
needs an explicit request to reopen it.

**Message to send in Codex — after selecting a closed session:**

> Reopen that closed session and continue from its saved focus.

You should not need to retell information already recorded. Do not initialize
the novel again to resume it. If context is missing or damaged, have Codex disclose
what is unavailable rather than invent a replacement.

## A short example

**Illustration only:** this fictional conversation shows the intended decisions,
not a transcript of a verified run. Actual saved replies also include the relevant
checkpoint and record references.

| Who | Message |
| --- | --- |
| Writer | "Suggest a name for the lighthouse keeper. Leave the setting open." |
| Codex | "One possibility is Mara. That remains a proposal; the setting is undecided." |
| Writer | "Establish Mara as the keeper's name. Keep the setting undecided." |
| Codex | "Mara is now the established name. The setting remains an open question." |
| Writer | "Revise her name from Mara to Elin. Keep her role unchanged." |
| Codex | "The current name is Elin. The earlier name remains in the revision history." |
| Writer | "Close this session and confirm the saved checkpoint." |
| Later, in the same novel | "Run `$novel-resume`. Show the saved sessions." |
| Writer, after choosing | "Reopen that closed session and remind me what is still undecided." |
| Codex | "The keeper's current name is Elin. The setting remains undecided." |

## Keep a separate backup

Saved history stays in the novel folder. It is not an automatic upload, cloud
backup, or a substitute for a copy stored elsewhere. After a confirmed save,
close the novel's active clients and use your normal backup tool to copy the
**whole novel folder**, including hidden `.git`, `.novel-creator`, and `.agents`
folders, to a separate backup location. A helper can confirm these folders are
included. Avoid copying in the middle of a save, update, or recovery.

Record the Python interpreter path and installed framework version separately
for your setup notes. A Python environment is tied to its installation location;
moving a novel to another computer requires a compatible environment there.
Copying the runtime folder is not a reliable way to install it on another machine.
Contributor permissions, if enabled separately, do not transfer just by copying
the novel. Installing a new package also does not update a novel's pinned framework.

For maintenance or recovery, use the [technical guide](getting-started.md).
Ordinary writing does not require contributor retrospectives, GitHub tools, or
publishing your novel anywhere.
