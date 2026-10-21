# Testing Novel Creator and finishing the current feature

This guide covers the current **Novel Initialization and Guided Brainstorming**
feature. Start with the host test below. Once it passes, Codex can implement the
remaining workflows in the planned order.

## 1. Where the project stands

The persistence foundation works: versioned JSON records, source validation,
current-message authorization, atomic local Git saves, unchanged retries and
structured errors. The latest automated run passed **52 tests** and the Bash
smoke checks. These tests establish storage behavior, not the quality of an AI
conversation or complete product readiness.

Initialization, full brainstorming, session management, production context and
inspection, continuity review, bilingual workflows and safe recovery are still
unfinished. Their CLI placeholders are not usable product features.

Our live experiment saved an initial prepared reply and two real typed follow-up
exchanges without repeating a skill invocation. An unchanged retry also returned
the original checkpoint. This is useful partial evidence. We have not completed
independent display verification, fresh-chat recovery, controlled interruption
or visible failed-save handling. The initial voice transcript paraphrased the
prepared reply, so **run the remaining experiment in text mode**; do not treat
spoken-output fidelity as verified.

The local Codex CLI we found was version 0.163.0. It could not start a model turn
in the cloud environment because its state directory was read-only. This is an
environment blocker, not proof that the adapter fails in your local desktop app.

Existing evidence: [partial live run](../tests/evaluations/host-capture-runs/20261021T133322Z/README.md).
The cloud fixture path `/workspace/host-capture-spike-5321347ef6` belongs to that
environment; it is not a path on your computer.

## 2. What you need to do personally

1. Run Codex on your computer with a writable local workspace and its normal
   sign-in. Use one specific host/version for the whole experiment.
2. Send three real test messages, observe the saves, deliberately stop one
   response, and open a genuinely new chat in the same test folder.
3. Keep the evidence described below and let Codex review it against the gate.
4. After the gate passes, have Codex implement the remaining feature slices.
5. Arrange the required human evaluations and review the results before release.

You do not need to manually implement the Python code. Codex can do the coding,
automated tests, documentation and evidence organization. Genuine user turns,
desktop interruption/observation and human evaluations need your participation.

## 3. Get the current code onto your computer

Use the latest `main` containing this guide and the foundation fixes. From your
local checkout on `main`, pull before testing:

```text
git pull --ff-only origin main
```

If Git reports local changes or divergent history, preserve your work and resolve
that condition before continuing. Do not reset or overwrite local changes.
Alternatively, use the accompanying `novel-creator-test-kit.zip` snapshot if
provided.

The snapshot is source code for testing, without repository history or a Python
environment. Extract it first. Its `novel-creator-test-kit` folder is the
framework folder in the following instructions. Preserve/apply the task changes
in your normal repository separately when integrating the work.

Requirements:

- Python 3.11 or newer, Git 2.39 or newer, and the Codex host you intend to support.
- A normal writable local home/state directory. Do not disable sandboxing or
  copy authentication secrets to work around the cloud limitation.
- A disposable test location **outside** the framework and every other Git
  repository. The setup script rejects existing target folders and nested repos.

Open a terminal in the framework folder. On macOS/Linux:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m unittest discover -v
```

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m unittest discover -v
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of
`python` for each command; no execution-policy change is needed.

The baseline is 52 passing tests at the time this guide was written. Keep the
actual output. Stop to investigate a failing baseline before calling the host
experiment successful. The optional developer smoke check is
`bash tests/speckit-smoke.sh`; it also requires Bash, `jq` and `rg`.

## 4. Create a fresh disposable fixture

From the same framework terminal, with the Python environment active:

macOS/Linux:

```bash
spike="$HOME/novel-creator-host-tests/spike-01"
python tests/fixtures/host-spike/setup.py --path "$spike"
python "$spike/.novel-creator/src/fixture-context.py"
python -c 'import sys; print(sys.executable)'
```

Windows PowerShell:

```powershell
$spike = Join-Path $HOME 'novel-creator-host-tests\spike-01'
python tests/fixtures/host-spike/setup.py --path $spike
python "$spike/.novel-creator/src/fixture-context.py"
python -c 'import sys; print(sys.executable)'
```

Do not create `spike-01` beforehand. If it exists, choose a new name such as
`spike-02`; do not erase an existing folder to make the command pass.

Setup should return `ok: true`, `data.saved: true` and a checkpoint. The context
helper should report the bootstrap checkpoint and `display_confirmed: false`.
That false value is expected: storage cannot know what you saw on screen.

Record the full Python executable path printed by the last command. The agent
needs that interpreter, or another interpreter with the same dependencies, when
running the fixture. In a new terminal, reactivate that environment before using
the `python` commands below.

Open **the new fixture folder** as a project/workspace in Codex. The installed
`AGENTS.md` contains the experimental protocol. Do not open the framework folder
and assume a new chat automatically points to the fixture.

Keep all extra test notes, screenshots and JSON evidence in a subfolder such as
`.novel-creator/local/evidence/`, or outside the fixture. Do not put unrelated
`.json` files directly in `.novel-creator/local/`: saves inspect that location for
transaction receipts.

## 5. Record the test environment

Create a note containing:

- Date/time and timezone; operating system and filesystem when known.
- Codex desktop version from its About screen, or `codex --version` for a CLI run.
- Model label and any revision/build identifier the host actually exposes.
- Python, Git and jsonschema versions; fixture path and starting checkpoint.
- The fixture's `.novel-creator/manifest.json` and its checksum information.

Useful commands in the activated environment:

```text
python --version
git --version
python -c "import importlib.metadata; print(importlib.metadata.version('jsonschema'))"
```

Never invent an unavailable version. Record the displayed label and explicitly
mark missing identifiers. Review unresolved required evidence before passing the
gate. Desktop and CLI results are separate; one does not establish the other.

## 6. Run the six host checks

Use typed messages. A screen recording with the tool receipts and final replies
visible is useful evidence of order. Save screenshots or copied visible text as
well. Hidden reasoning and private transcript databases are not test inputs.

### A. Save before display, then two automatic follow-ups

Start a new chat in the fixture folder. Replace the interpreter placeholder in
this prompt with the full Python executable path recorded above:

```text
Run the disposable host-capture fixture experiment in this folder. Read AGENTS.md
and use <FULL PYTHON EXECUTABLE PATH> for the installed fixture helpers.

Preserve each current user message exactly. Prepare one exact final response,
save the pair with fixture-prepare.py and the installed run.py exchange save,
and wait for a successful saved receipt before displaying that response.
Continue this automatically on later ordinary turns without another invocation.
Store extra test evidence under .novel-creator/local/evidence/. Do not create
canon, edit framework code, capture hidden reasoning, push, or add an unsaved
suffix. Disclose failures and pause rather than claiming a failed save succeeded.

Story idea: a lighthouse keeper receives letters from tomorrow.
```

After the reply, send two separate messages without mentioning saving or skills:

```text
The next letter is written in the keeper's own handwriting.
```

```text
What could make the keeper afraid to open it?
```

After **each** reply, inspect the last committed pair with:

```text
python "<FULL FIXTURE PATH>/.novel-creator/src/fixture-context.py"
```

Compare the stored user and assistant text with the visible messages, including
Unicode, newlines and any final suffix. The entire initial prompt is a user
message too; it must not be silently replaced by only its story-idea sentence.

**Pass:** all three exchanges are saved before their final replies, both later
turns save without reinvocation, and committed text matches what was displayed.
**Fail:** a missed save, text mismatch, unsaved addition or unproven ordering.
Do not assume a successful receipt alone proves display ordering.

### B. Retry an unchanged exchange

Keep the payload path returned by preparation for one successful exchange. Do
not prepare it again. Set `payload` to that exact existing file in your terminal.

macOS/Linux:

```bash
payload="/absolute/path/returned/by/preparation.payload"
git -C "$spike" rev-list --count HEAD
python "$spike/.novel-creator/run.py" exchange save --novel "$spike" --input "$payload" --json
git -C "$spike" rev-list --count HEAD
```

Windows PowerShell:

```powershell
$payload = 'C:\absolute\path\returned\by\preparation.payload'
git -C $spike rev-list --count HEAD
python "$spike/.novel-creator/run.py" exchange save --novel $spike --input $payload --json
git -C $spike rev-list --count HEAD
```

**Pass:** `already_saved: true`, the original exchange/checkpoint is returned,
and the commit count does not increase. Retain both receipts.

### C. Interrupt after save and before final display

Use this test-only prompt in the active fixture chat:

```text
For this interruption test only, prepare and save the exact response:
The keeper leaves the letter sealed.

After a successful save receipt, run a foreground wait of 45 seconds so I can
press Stop before the final response is displayed. If I do not stop you, display
only the prepared response when the wait ends. Do not treat a saved response as
proof that I saw it. Use the existing fixture protocol and preserve this user
message exactly.
```

Once the successful save receipt is visible and the waiting tool is running,
press Codex's **Stop** button. Then inspect committed context in a terminal.

**Pass:** the prepared response is committed, the final response was not shown,
and the checkpoint and timing are recorded. If the final response appears before
you stop it, record that attempt and repeat the case; it did not demonstrate the
required interruption window. The deliberate wait is test instrumentation.

### D. Recover in a genuinely new chat

Open a new chat in the **same fixture project**, with no old conversation history
attached. Do not paste the interrupted response or the old conversation into it.

```text
Read this fixture's AGENTS.md and committed fixture context using
<FULL PYTHON EXECUTABLE PATH>. Recover the last confirmed exchange from disk.
Report its checkpoint and offer its exact saved response without assuming it was
displayed or accepted. Continue the save-before-display protocol for this turn.
```

**Pass:** the new chat obtains the interrupted response and checkpoint from the
saved fixture, needs no retelling and does not infer visibility or acceptance.
Check its own new response was also saved. This fixture context reader is the
available tool; production `context`, `session` and `recover` commands are still
placeholders and must not be used as though implemented.

### E. Disclose a failed save and pause

Ensure no save is currently running. In the terminal, create an **empty test
lock**, only if the path is absent:

macOS/Linux:

```bash
mkdir "$spike/.novel-creator/local/write.lock"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Path "$spike/.novel-creator/local/write.lock" -ErrorAction Stop
```

If the lock already exists, stop and inspect it. Do not remove someone else's
lock. Record `git -C <FIXTURE PATH> rev-parse HEAD`, then send an ordinary story
message in the active fixture chat, such as:

```text
Perhaps the keeper recognizes the seal. What does that suggest?
```

**Pass:** save returns code 6, the agent visibly reports the failure, pending
exchange ID and last verifiable checkpoint, and pauses authoritative work.
The attempted story reply must not be presented as successfully saved. HEAD
must not advance. Preserve the failed payload and failure receipt.

The failure disclosure itself is expected to be visible even though the story
save failed; it must truthfully explain the unsaved attempt.

### F. Remove only your injected fault and retry

For the empty test lock **you created in E**, remove that directory only:

macOS/Linux:

```bash
rmdir "$spike/.novel-creator/local/write.lock"
```

Windows PowerShell:

```powershell
Remove-Item -LiteralPath "$spike/.novel-creator/local/write.lock"
```

Do not use recursive deletion, a force flag or Git reset. If it is not the same
empty test lock, stop and inspect rather than removing it.

Retry the **original failed payload**, using the command in B. It has its original
exchange ID and text. Do not replace it with a newly prepared response.

**Pass:** the original attempt saves once, then an identical retry returns the
same checkpoint without another commit. Offer the saved response without claiming
it was previously displayed. If `cleanup_required: true` appears, retain the
evidence and stop: production cleanup recovery is not implemented yet. Do not
delete receipts or rewrite history to force the test to pass.

## 7. Keep a small evidence report and review the gate

For every case, save its exact user input, prepared/final visible text, payload,
receipt/error, checkpoint before/after, actual result and screen/timing evidence.
Record human observations separately from automated readback checks.

| Check | Result to record |
|---|---|
| A: initial save and two automatic turns | Pass/fail/unverified; text and display-order evidence |
| B: unchanged committed retry | Original checkpoint, unchanged commit count |
| C: saved but undisplayed response | Save receipt, stop timing, absence of final display |
| D: fresh chat | Recovered text/checkpoint from disk, visibility not assumed |
| E: failure disclosure | Code 6, pending ID, checkpoint, unchanged HEAD, visible pause |
| F: retry after removing test fault | Original payload saved once; no replay or overwrite |

Keep the report under the framework's `tests/evaluations/host-capture-runs/` when
bringing local evidence back for review. Preserve the fixture until reviewed.
Do not share tokens or other authentication files with the report.

Give Codex this handoff:

```text
Review this real host-capture evidence against T012 and tests/evaluations/host-capture.md.
Distinguish observed results from assumptions and mark any missing case unverified.
If every required case and environment detail is supported by evidence, record a
passing T013 gate decision and complete the equivalent T012/T069/T089 obligations.
Otherwise keep the gate blocked and identify the specific missing check or adapter
change. Do not implement dependent stories or weaken FR-009 to make the gate pass.
```

The [task plan](../specs/001-novel-initialization-brainstorming/tasks.md) says:
**“No story phase starts before T013 passes.”** T013's current checked marker
means a blocked decision was recorded; it does not mean the experiment passed.
Repeating converge will not supply missing host evidence.

## 8. Finish implementation in these milestones

After a supported gate pass, use `$speckit-implement`. Work in slices so each
milestone has a usable result and its own tests and instructions.

| Order | Milestone | Original tasks | What must work |
|---|---|---|---|
| 1 | Initialize a novel | T014–T021 | Start with or without a concept; preserve unknowns, preferences and identity; independent installation |
| 2 | Guided/open brainstorming | T022–T028 | Useful guidance; next-response mode/topic changes; proportionate suggestions |
| 3 | Capture, sessions and recovery | T029–T037 | Automatic structured capture; resume without retelling; sourced inspection; safe failure recovery |
| 4 | Canon and revisions | T038–T045 | Clear acceptance, precise partial selection, retained history/impact and review checkpoints |
| 5 | Continuity Guardian | T046–T053 | Six conflict categories, knowledge/timing distinctions, intentional techniques and safe holds |
| 6 | Icelandic and portability | T054–T061 | Full English/Icelandic workflows; independent reconstruction and installed-bundle operation |
| 7 | Performance and release evidence | T062–T067 | Measured targets, platform results, complete journeys, documentation and constitution review |

Later convergence tasks refer back to these obligations. They do not multiply
the feature scope: reuse the same implementation and acceptance evidence, then
close the corresponding task references together. The foundation fixes through
T090 are already completed.

Suggested implementation handoff:

```text
$speckit-implement
Use the reviewed passing host gate and continue from the first incomplete original
story phase. Respect dependencies and reuse the convergence task references rather
than building duplicate alternatives. Write meaningful regression tests first,
verify the slice end to end, update onboarding and task markers, and obtain review.
Leave unavailable human/host/platform evidence explicitly unverified.
```

Run convergence after a completed slice or a substantial implementation pass.
An honest completion report must distinguish implemented code, passing automated
tests, real-host observations, agent judgments and human evaluations.

## 9. What is required before calling this feature finished

The specification's full acceptance criteria remain authoritative. In particular:

- **Novice usability:** five evaluators; at least four initialize within ten
  minutes without outside assistance, and at least four rate guidance/control
  at least 4/5. Have someone other than the implementer perform these exercises.
- **Resume:** three sessions plus a fresh interaction recover all 20 designated
  ideas, 10 decisions and 5 questions with correct state/source.
- **Authority:** at least 12 clear-acceptance and 12 non-acceptance examples,
  including partial selections and both languages; five deliberate canon
  revisions preserve prior/current states, origins and directly affected links.
- **Continuity:** every designated significant conflict across all six categories
  interrupts conflicting development in the next response; intentional techniques
  remain distinguishable from errors.
- **Language/portability:** supplied concepts/preferences survive reopening in both
  languages; an independent consumer reconstructs the designated structured story
  information without re-extracting it from conversation prose.
- **Failure protection:** interruption, unreadable context, failed saves, duplicate
  processing and overlapping edits preserve confirmed authority and disclose gaps.
  Approved manuscript text remains unchanged.
- **Performance:** 100 sessions, 5,000 exchanges, 10,000 active assertions and
  25 MiB JSON; 30 warm runs, p95 read at most 2 seconds and validate/local save
  at most 1 second, excluding model latency; report cold reads and hardware.
- **Platforms and release:** collect Linux/macOS/Windows evidence required by the
  plan; do not claim support for unverified combinations. All automated tests,
  quickstart journeys, release evidence and required reviews must pass.

You supply real user observations, the novice evaluators and any language review
you want from fluent readers. Codex can prepare fixtures, run measurements,
implement fixes and organize evidence. A code test cannot substitute for a human
rating or an unavailable real-host/platform run.

Completion means the current initialization/brainstorming feature satisfies
[spec.md](../specs/001-novel-initialization-brainstorming/spec.md), its
[plan](../specs/001-novel-initialization-brainstorming/plan.md) and release gates.
Chapter drafting, literary editing, publication, the dashboard and additional
host adapters are explicitly outside this feature. Finishing the larger Novel
Creator product requires separately specified and planned features for those
capabilities after this foundation is usable.

**Your immediate next action:** obtain this task's current code locally, create
the disposable fixture, and run A–F in your intended Codex host. Bring back that
evidence to resolve the gate; the remaining implementation can then proceed.
