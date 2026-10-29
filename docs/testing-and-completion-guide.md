# Testing Novel Creator and finishing the current feature

## Current implemented commands

**Current target: single-user POC (owner decision, 2026-10-23).** Novice testers
are out of scope and manual testing follows delivery. Use the
[POC quickstart](poc-quickstart.md) and
[POC verification report](../tests/evaluations/poc-readiness-20261023.md).
The broader historical release gates described below are not prerequisites for
trying this POC. Unknown literary quality and unmeasured host behavior remain
unknown; no human observations are inferred from automated tests.

Initialization, settings revisions, context, session list, inspection, structural
validation and explicit recovery are now implemented. Installed Codex entries
load shared guidance, resumption, authority and continuity workflows. Use the
[current README](../README.md) for runnable setup and recovery examples.

The host capture gate has passed; no repeat of its Stop-button exercise is needed.
The current authorized delegated evaluation now covers the capture/resumption,
authority, continuity and paired language-pitfall matrices. Structural checks,
agent meaning judgments and human observations remain distinct. See the
[2026-10-28 continuation](../tests/evaluations/phase22-resumption-20261028.md).
The new ordinary-layout Windows measurement completes all 30 reads and saves:
read p95 is 1.028736700s and save p95 is 3.067419500s. The owner withdrew all
latency targets on 2026-10-28; these timings are informational. Historical target
misses remain unchanged. The current benchmark exits successfully only when all
requested operations complete, with no latency pass/fail verdict.
Representative independent-consumer coverage is automated. Earlier Linux
performance remains source/configuration specific. Native-input coverage outside
the observed host scope and subjective literary quality are unmeasured; novice
recruitment and manual ratings are excluded from this POC's prerequisites.
Current platform scope is Linux and Windows; macOS support and verification
are deferred.
[Release evidence](../tests/evaluations/release-readiness.md) separates completed
structural journeys from those remaining gates. Older procedures below are
historical fixture procedures, not the current product entry point.

## Current product recovery

For a novel created with `init`, inspect a saved or pending exchange through its
installed launcher. Use the configured Python environment and actual novel path:

```powershell
python C:\Novels\MyNovel\.novel-creator\run.py recover --novel C:\Novels\MyNovel --exchange EXCHANGE_UUID --json
```

Inspection is read-only. `data.saved` identifies whether the exchange is committed;
`data.state` distinguishes `pending`, `published` and `cleanup_needed`.
`saved_response_display: unconfirmed` does not establish that a reply was seen or
accepted. A held lock must be inspected; recovery never steals it.

Only after inspecting the report, request an explicit unchanged retry with its
current `checkpoint.git_head`:

```powershell
python C:\Novels\MyNovel\.novel-creator\run.py recover --novel C:\Novels\MyNovel --exchange EXCHANGE_UUID --retry --expected-head CONFIRMED_HEAD --json
```

Use `--expected-head unborn` only when no first commit exists. Pending recovery
reuses the original receipt payload and IDs. Published cleanup preserves the
saved commit, updates managed index entries and does not replay decisions. If
HEAD, the pending payload, managed files or staged entries conflict, preserve
them and inspect the error instead of retrying with replacement content. Further
writes pause until recovery succeeds. Do not reset history or delete receipts to
force progress. Older spike installations remain pinned; do not copy current
source over an old fixture or assume its test helpers are product commands.

## Current decision: PASS — focused spike-03 confirmation

The actual Desktop capture gate is passed for the tested Windows Desktop
native-tool, single typed-text input and scoped filesystem approval combination.
Native source, prepared payload and committed user text match exactly, including
the ending LF; the displayed reply matches the saved assistant text, and the
save event precedes display. [Actual run and scope](../tests/evaluations/host-capture-runs/20261021T171237Z-spike-03/README.md).

Spike-02 supplies the retained automatic-turn, interruption, fresh-chat,
failure-disclosure and unchanged-retry evidence. Spike-03 resolves its manual
here-string input loss using the original native userMessage text. Capture
source JSON belongs under `.novel-creator/local/evidence/`, outside root receipt
discovery. No old exchange or payload ID was rewritten.

T012/T069/T089/T103/T116 are complete; T013's current decision is PASS. No further
manual capture-gate test is required for this change. Story tooling is implemented;
its product-level creative judgments and release readiness remain unverified,
along with voice, other hosts and unattended default-sandbox operation.

The earlier assessments and procedures below are retained as historical records.
Their BLOCKED/pending statements are superseded by this decision; their test
counts describe their respective runs.

## Historical assessments and procedures

This guide covers the current **Novel Initialization and Guided Brainstorming**
feature. Start with the host test below. Once it passes, Codex can implement the
remaining workflows in the planned order.

The user has now completed the spike-02 hands-on A-F exercises. A remaining
exact-user-text discrepancy led to the revised native-input adapter. For its
focused follow-up, use a new fixture containing that adapter and send one typed
test message. Let Codex compare the current native userMessage, prepared JSON,
committed user text and final response with no trimming or newline conversion.
The adapter's AGENTS.md describes the native read_thread prerequisite and
--user-message-file preparation mode. Do not repeat the prior Stop-button test
unless a later change invalidates that evidence. Preserve existing fixtures.

## 1. Where the project stands

The persistence foundation works: versioned JSON records, source validation,
current-message authorization, atomic local Git saves, unchanged retries and
structured errors. An earlier Linux run passed **52 tests** and the Bash
smoke checks; see the [current Windows foundation report](../tests/evaluations/platform-results.md)
for local results and unavailable coverage. These tests establish storage behavior, not the quality of an AI
conversation or complete product readiness.

At this early assessment, initialization, session management, production reads
and safe recovery were placeholders. They are now implemented as described in
the current product sections above; full creative-host and bilingual evaluation
remains incomplete.

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

Open a terminal in the framework folder. On Linux (Bash):

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

The original baseline was 52 passing tests; new regressions can change the count.
Keep the actual output and distinguish skipped coverage from passes. For Windows
temporary-path setup, see [development instructions](development.md#windows-foundation-remediation--2026-10-21).
Stop to investigate a failing baseline before calling the host
experiment successful. The optional developer smoke check is
`bash tests/speckit-smoke.sh`; it also requires Bash, `jq` and `rg`.

## 4. Create a fresh disposable fixture

From the same framework terminal, with the Python environment active:

Linux (Bash):

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
- Python, Git, jsonschema and jsonschema-rs versions; fixture path and starting checkpoint.
- The fixture's `.novel-creator/manifest.json` and its checksum information.

Useful commands in the activated environment:

```text
python --version
git --version
python -c "import importlib.metadata; print(importlib.metadata.version('jsonschema')); print(importlib.metadata.version('jsonschema-rs'))"
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

Linux (Bash):

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
Check its own new response was also saved. Use this historical fixture's pinned
context helper for that experiment. Current product installations provide
`context`, `session list` and `recover`; their commands and recovery boundaries
are described above. Do not assume an older fixture includes the current runtime.

### E. Disclose a failed save and pause

Ensure no save is currently running. In the terminal, create an **empty test
lock**, only if the path is absent:

Linux (Bash):

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

Linux (Bash):

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
it was previously displayed. If `cleanup_required: true` appears, the exchange
is already saved. Preserve its receipt and checkpoint. A current product
installation supports explicit managed-index recovery as described above; an
older pinned spike may lack that command and should be preserved for inspection.
Do not delete receipts, replace the fixture runtime or rewrite history to force
the test to pass.

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
records the current PASS decision described above; the earlier blocked decision
is historical. Repeating converge will not supply missing product-host evidence.

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

- **Initialization/guidance:** automated installed journeys preserve unknown
  preferences and reopen without invented creative details; mode/topic changes
  take effect in the next response. Novice recruitment and manual ratings are
  excluded by the owner's current POC scope; owner assessment follows delivery.
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
- **Platforms and release:** collect Linux/Windows evidence required by the
  plan; do not claim support for unverified combinations. All automated tests,
  quickstart journeys, release evidence and required reviews must pass.

Codex can execute the authorized automated scenarios, run measurements,
implement fixes and organize evidence. Optional owner or fluent-reader review
after delivery remains separate; it is not required to start using the POC.
A code test cannot substitute for a human rating or an unavailable host/platform
observation, and no such result is inferred from delegated inputs.

Completion means the current initialization/brainstorming feature satisfies
[spec.md](../specs/001-novel-initialization-brainstorming/spec.md), its
[plan](../specs/001-novel-initialization-brainstorming/plan.md) and release gates.
Chapter drafting, literary editing, publication, the dashboard and additional
host adapters are explicitly outside this feature. Finishing the larger Novel
Creator product requires separately specified and planned features for those
capabilities after this foundation is usable.

**Current next actions:** continue from the latest incomplete tasks using
`$speckit-implement` and resolve Windows save performance before broader release
qualification. No novice/manual recruitment is requested. The earlier A–F capture
experiment already passed in its documented scope; repeat it only if a later
change invalidates that evidence.
