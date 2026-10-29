# Quickstart and Validation Guide

Status: the single-user POC is delivered. Novice recruitment and manual testing
are not prerequisites; owner testing follows delivery. Current automated
capture/resumption, authority, continuity and paired language observations are
documented in [Phase 22 results](../../tests/evaluations/phase22-resumption-20261028.md).
Broader scale qualification still misses the Windows save target. Human literary
quality and host combinations outside the observed scope remain unmeasured.

The scoped actual-host capture gate has passed. `init`, `session list`,
`context`, `inspect`, `validate`, `exchange save` and explicit `recover` inspection/
retry are implemented. Settings and session transitions use typed exchange
revisions. Shared guidance/authority/continuity resources and English/Icelandic
resource selection are present; their full creative-host, human, language and
release evaluations remain incomplete. See [current usage](../../README.md) and
[record format](../../docs/record-format.md). The numbered scenarios below remain
acceptance procedures, not claims that every product/human evaluation has run.

## Prerequisites and installation verification

Use Python >=3.11, Git >=2.39 with a configured local author identity, and a
supported Codex host with filesystem/shell access to an independent novel folder.
Run the release checks on Linux and Windows before claiming each platform.
macOS support and verification are deferred from the current release.
The host owns authentication and voice transcription; the tool needs no model key.
Use disposable directories outside the framework repository for all examples.

For foundation development, run from the framework checkout. These structural
checks need no model credentials or interactive host:

```bash
python -m venv .venv
# Activate .venv with the current shell's standard activation command.
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m novel_creator --help
python -m unittest discover -v
```

Windows may use `py -3` to create the environment. Use the active environment's
`python` for subsequent commands. Pin dependency resolution in release evidence.
These commands verify the implemented foundation. Product journeys, human
evaluations and claimed-host support require their separate evidence.

Existing development-tool smoke check (already available):

```bash
bash tests/speckit-smoke.sh
```

Before attempting product initialization, follow the disposable installed-fixture
procedure in [host-capture.md](../../tests/evaluations/host-capture.md). The minimal
fixture uses production persistence without implementing the stories. The actual
host gate now has scoped real Desktop evidence; synthetic turns and subprocess
context readers alone do not establish product creative quality or release readiness.

## 1. Planned first vertical slice and host capability gate

The following product commands become available only after the actual-host gate
passes and their story tasks are implemented.

Prepare a UTF-8 `brief.json` in a disposable scratch directory using the project
schema: title can be temporary, concept and all creative preferences can be
explicitly unknown, manuscript language can be `en` or `is`.

```bash
python -m novel_creator init --path /absolute/path/to/new-novel --brief-file /absolute/path/to/brief.json --json
python /absolute/path/to/new-novel/.novel-creator/run.py context --novel /absolute/path/to/new-novel --json
```

Expected: independent Git root, stable identity, unknowns preserved, installed
bundle and a confirmed bootstrap commit; no inferred canon. Move or temporarily
make the framework checkout unavailable and repeat context/validation using the
novel-local launcher and its documented Python dependency environment. This must
not depend on the original framework path.

Open that novel in the claimed Codex host. Invoke `$novel-init` or
`$novel-brainstorm` as applicable, skip uncertain answers and accept the invitation
to explore. The actual host check must demonstrate:

1. A current user message and the exact prepared visible response are committed
   with their captures before response display and before the next exchange.
2. At least two further turns save automatically without repeated skill invocation.
3. Interrupt after save but before display; resume exposes the saved response
   without treating it as seen or accepted. Retry applies no duplicate decision.
4. Open a fresh chat, invoke `$novel-resume`, select the saved session and recover
   mode, focus, canon and open questions without retelling the story.
5. Inject a save failure through the test harness and confirm a visible failure,
   last confirmed checkpoint and pause of further authoritative changes.

Capture host version/model, user-visible messages, tool receipts, Git checkpoints
and interruption timing. This spike blocks dependent release claims if unsuccessful;
there is no assumed after-response hook. Do not use an actual full disk or delete
real story records to test errors; use temporary repositories/fault injection.

## 2. Record inspection and independent consumer

```bash
python /absolute/path/to/new-novel/.novel-creator/run.py session list --novel /absolute/path/to/new-novel --json
python /absolute/path/to/new-novel/.novel-creator/run.py inspect --novel /absolute/path/to/new-novel --kind assertion --json
python /absolute/path/to/new-novel/.novel-creator/run.py validate --novel /absolute/path/to/new-novel --json
```

Use an independently written fixture reader in the integration tests to fold
committed bundles according to [data-model.md](data-model.md) and
[storage.md](contracts/storage.md), without importing the production reducer.
Compare designated entities, relationships, event order, perspective/timing,
current/superseded facts and decision origins. No conversation prose parsing or
host access is allowed. Delete caches and repeat; authoritative results match.

## 3. Acceptance and continuity scenarios

Use paired English/Icelandic fixtures and actual host runs. Include:

- Explicit "Let's make Thomas the murderer" versus praise, "Maybe Thomas",
  silence, dialogue quotations, ambiguous references and compound selections.
- A secret learned after an event versus action requiring that knowledge earlier;
  recorded lies, unreliable narration and delayed reader revelation.
- Explicit revision/reversal of a sourced fact, with prior state and directly
  affected references inspectable, and no approved manuscript file changes.
- Mode switches, topic changes and reduced suggestions taking effect in the
  next response; session resumption preserving the previous mode.
- Unreadable relevant canon: disclose incomplete coverage, save proposals only
  when safe, hold affected canon until restoration, revalidate before resuming.

Agent judgments need recorded expected outcomes and review; a passing schema
validator does not establish semantic acceptance or narrative consistency.

## 4. Fault and overlap suite

Automated integration tests use temporary real repositories and explicit failure
points before file publication, after publication/before commit, after commit/
before conditional ref publication, after ref publication/before index cleanup or
receipt, and before visible output. Exercise Git identity/commit failure,
held locks, unrelated staged/unstaged work, unexpected external HEAD advancement,
same-ID identical/changed retries, a competing commit immediately before update-ref
(the rejected candidate must remain absent from authoritative history), private
index preservation, saved-with-cleanup-needed recovery, bootstrap input-artifact
provenance, all three routine checkpoint modes and no redundant canon approval,
malformed/unsupported envelopes, missing source
refs, damaged context, cross-novel IDs and outside-root/symlink writes. Assert
last confirmed authority, no duplicate decision, no unrelated content overwritten,
accurate incomplete/save-failure disclosure, and manuscript path protection.
Recover pending work through the documented `recover` interface. Never repair
history with an automatic force-push, reset or overwrite.

## 5. Release evidence matrix

| Target | Required evidence |
|---|---|
| SC-001 | Automated installed journeys initialize without a concept, preserve skipped preferences as unknown, offer optional brainstorming and reopen without invented details; no novice/manual prerequisite |
| SC-002 | In both languages, every supplied preference/concept retains meaning after reopen; skipped details remain unknown |
| SC-003 | Three sessions plus fresh interaction recover all 20 ideas, 10 decisions and 5 questions with correct state/source |
| SC-004 | At least 12 clear-acceptance and 12 non-acceptance examples spanning both languages and partial selections; all specified outcomes correct |
| SC-005 | Every designated significant conflict in all six categories interrupts in the next response; intentional techniques remain distinct |
| SC-006 | Five revisions preserve prior/current state, sources and every directly linked affected item; approved manuscript hashes unchanged |
| SC-007 | Mode/topic switches take effect in the next automated acceptance response, preserving preferences and prior ideas; subjective usefulness/control is left to the owner after POC delivery |
| SC-008 | Independent consumer reconstructs every designated entity, relationship, ordering, perspective and decision origin |
| SC-009 | All interruption/unavailable-context/save-failure/duplicate/overlap exercises preserve confirmed authority and disclose incomplete work; unreadable relevant canon prevents affected canon writes |

Check all Story 1–6 acceptance scenarios as well as these outcome counts. Organize
evidence under planned `tests/evaluations/`: fixture IDs, language, host/model/
version, exact inputs/outputs, checkpoints, expected/actual findings, reviewer
judgment and human approvals where relevant. Mark unavailable evidence unverified.

## 6. Performance and compatibility

Generate 100 sessions, 5,000 exchanges, 10,000 active assertions and 25 MiB total
JSON in a temporary repository. Record laptop CPU/RAM, OS/filesystem, Python/Git
versions, fixture seed and raw timings for 30 warm reads and saves when measuring
performance. All latency targets were withdrawn by the owner on 2026-10-28;
timings are informational, excluding model latency. Report cold-read separately.
Qualification requires correct, completed operations and honest failure disclosure,
without a timing pass/fail claim. If a cache is introduced, verify its removal/rebuild
and rejection after HEAD/schema changes. Unsupported record versions must fail
explicitly and leave canon unchanged. No automatic incompatible migrations.

## Planning completion versus release completion

This guide separates current foundation checks from future product verification.
A completed plan does not establish host
capture, language quality, performance, accessibility or novice outcomes. Record
their actual results during implementation and release review. Continue with
`$speckit-implement` for remaining story/evaluation work. The capture gate has
passed within its documented scope. Do not treat this guide as release evidence.
