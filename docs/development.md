# Development

## Story implementation after the host gate

The current tool implements init, context, session list, inspect, validate and
explicit recover inspection/retry. Settings and session transitions are typed
conversation exchange revisions. The independent installer pins source/schemas,
shared workflows, language resources and Codex entries; it preserves existing
instructions/content and original bootstrap provenance. Use the README commands.

New deterministic checks cover settings/identity, guided/open session changes,
focused context, sourced revisions, partial selection, supersession, direct impact,
routine checkpoint triggers, significant/deferred conflict holds and unknown time.
Shared authority/continuity workflows own the host judgments and response order.
No model API or custom conversational runtime was added. The independent reader
does not import the production reducer. Full-scale performance is not measured.

See [release evidence](../tests/evaluations/release-readiness.md) for remaining
host/human/language/platform gates. Checklist markers were inspected read-only
(16/16 requirements checked). No .specify/extensions.yml hooks are registered.

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
manual host test is required for this change. Dependent story implementation may
begin. Product workflows, release readiness, voice, other hosts and unattended
default-sandbox operation remain unverified.

The earlier assessments and procedures below are retained as historical records.
Their BLOCKED/pending statements are superseded by this decision; their test
counts describe their respective runs.

## Historical assessments and procedures

## Native message-boundary remediation — T116

The Desktop adapter now obtains the current public userMessage from native
read_thread using CODEX_THREAD_ID, serializes that selected item as JSON and
uses fixture-prepare.py --user-message-file. The helper takes the single native
text string without adding/removing any characters. It rejects wrong roles,
multiple text segments and non-text sources rather than inventing a join rule.
Native IDs remain ignored local preparation evidence, outside story identity.

This addresses the observed retyping boundary: the test chats materialized user
text with PowerShell here-strings, whose closing-marker newline is excluded from
the value. The storage helper itself already preserves input bytes. Do not
assume every user message ends in LF or automatically append/strip one. The
adapter preserves whatever the native current-message source actually supplies.

A new installed-fixture regression reproduced the missing input mode before
implementation, then passed exact LF, multiple trailing blank lines, leading
spaces, Icelandic text, CRLF and no-final-newline saves, plus invalid-source
rejections. This is structural evidence, not a fresh actual-host turn. The
official [App Server item contract](https://learn.chatgpt.com/docs/app-server#items)
documents userMessage content as user inputs; it does not establish an automatic
delimiter-stripping convention, so none is assumed here.

T116/T103 stay open until a focused real Desktop turn verifies native-source to
prepared-payload to committed-message parity under the revised adapter. Retain
spike-02 and its successful B/C/D/E/F evidence unchanged. No Stop-test repetition
is needed for this input-only change. Native read_thread/current identity/full
text availability is an explicit adapter prerequisite; no private transcript
scraping or model runtime is a fallback. Scoped filesystem approval remains
required where the sandbox denies hard-link publication.

## Actual host gate status — 2026-10-21

The new user-driven spike-02 run exercised automatic follow-ups, successful
save-before-interruption, genuine fresh-chat recovery, visible lock failure and
unchanged retry without duplication. See [the actual Desktop report](../tests/evaluations/host-capture-runs/20261021T161928Z-spike-02/README.md).

T013 remains **BLOCKED** and T103 unchecked: native public user-message readback
contains one terminal LF absent from each of eight stored user messages. Determine
whether this is capture loss or a host envelope convention using authoritative
evidence; preserve intentional line breaks and do not normalize away the issue.
Native adapter planning must also account for sandbox os.link permission denial:
scoped normal-access retries succeeded, unattended default-sandbox saves did not.
The user has completed the requested hands-on checks; no repeat of the Stop
exercise is currently needed. No story gate or exact-text requirement is waived.

## Windows foundation remediation — 2026-10-21

T102 changes the managed-index flush to use a writable descriptor. Windows
rejects fsync on the previous read-only descriptor with errno 9, leaving a
published save marked cleanup_required and blocking continuation. Regressions
cover clean existing/unborn bootstrap, continuation, receipts, identical retries
and installed-fixture saves. This change does not implement recover or repair
previously interrupted fixtures. Preserve the earlier Desktop fixture and its
evidence; use a new disposable fixture for the next host experiment.

T111 canonicalizes temporary repository roots in test helpers, retaining the
production traversal/symlink restrictions. The installed-fixture test compares
exact UTF-8 bytes decoded to text, preserving CRLF and trailing newlines.
Real symlink rejection is a separate test: Windows error 1314 is reported as
skipped/unverified; other errors still fail. Traversal/payload tests always run.

Use a writable canonical temporary directory outside all Git repositories for
the foundation suite. For example, in a normal local PowerShell terminal:

```powershell
$novelTestTemp = Join-Path $HOME 'novel-creator-test-temp'
New-Item -ItemType Directory -Force -Path $novelTestTemp | Out-Null
$env:TEMP = (Resolve-Path -LiteralPath $novelTestTemp).Path
$env:TMP = $env:TEMP
$env:PYTHONUTF8 = '1'
.\.venv\Scripts\python.exe -B -m unittest discover -v
```

These environment variables affect this terminal and its child processes only.
Tests allocate disposable child directories and local Git identities. A sandbox
denying file creation or hard links is an environment failure, not a passing
storage exercise; do not weaken production publication checks to accommodate it.
See [current Windows evidence](../tests/evaluations/platform-results.md) for
actual commands, outcomes, skipped coverage and remaining support limitations.
Filesystem power-loss durability and actual Codex host capture remain unverified.

Windows Desktop preflight on 2026-10-21 also remains **BLOCKED**: the independent
fixture bootstrap returned `cleanup_required: true`; no host conversation cases
were started or gate obligations closed. Preserve its history and receipts.
See [the run report](../tests/evaluations/host-capture-runs/20261021T154100Z/README.md)
for environment, checkpoint, baseline logs and missing evidence.

Requires Python 3.11 or newer and external Git 2.39 or newer. Use a local
virtual environment; no model credentials, server or AI runtime are needed.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m novel_creator --help
python -m unittest discover -v
bash tests/speckit-smoke.sh
```

On Windows activate `.venv\Scripts\Activate.ps1`. The test extra uses Python's
standard unittest runner. `requirements-lock.txt` records exact runtime resolution;
packaging declares the compatible range. Tests use temporary Git repositories,
local disposable identities, and automatic fixture cleanup. They never configure
a global identity. Interrupted fixtures may be removed only after confirming
they are disposable test directories.

Structural tests do not establish literary consistency or native-host support.
Each claimed Codex host/model/version needs separate actual capture evidence in
`tests/evaluations/host-capture.md`. No host is yet verified; story implementation
must wait for the foundation gate.

## Foundation status and hard gate

Foundation packaging, complete shared schemas, structural transition validation,
atomic exchange-save and an independent disposable host-spike fixture are
implemented. `init`, session operations, production context/inspection/validation
and `recover` are command placeholders returning an explicit unavailable error.
The fixture's context helper is test-only. Pending retries use the exact original
`exchange save` payload. Published cleanup failures return saved/cleanup_required;
further writes remain paused because safe cleanup recovery is later T034 work.
Never manually reset history to clear this pause.

New decisions must cite the current conversation's actual user message;
historical messages may remain provenance but cannot authorize a new change.
Malformed committed envelopes and recovery receipts return structured
unavailable-context errors with the affected path, rather than tracebacks.
Journal failures retain the last validated prefix and its historical Git
checkpoint when verifiable; a null `git_head` means no matching valid historical
snapshot could be confirmed. An unsafe journal never permits further saves.
Stale-write conflicts include `error.expected_git_head` and
`error.actual_git_head`, alongside the last confirmed checkpoint and pending ID.
Held writer locks also report the attempted exchange ID and an independently
verified committed checkpoint when available. Inspection reads a captured Git
snapshot without taking over the lock; unborn or unreadable history does not
produce an invented checkpoint. The existing lock and pending files are retained.

Before dependent implementation, the actual host still needs real automatic
subsequent turns, fresh-chat recovery and controlled save/display interruption
evidence. Reading thread summaries or running subprocess fixtures does not
establish those behaviors. Foundation remediation does not pass this gate.

**T013 decision: BLOCKED. T012 actual Codex host evidence is unverified.** See
[host-capture evaluation](../tests/evaluations/host-capture.md). No available host
control can create genuine subsequent turns, a fresh chat or display interruption
here. T014+ remains unimplemented. A subprocess fixture or prompt compliance
cannot waive that gate. Return to actual-host evaluation/adapter planning before
continuing; no supported-host claim, manuscript feature or release is implied.

## Measured performance remediation — 2026-10-21

The 100-exchange cProfile baseline spent 4.112s in validation, including 2.517s
in repeated prefix folds/deepcopies and 1.535s in schema checks. Incremental
validation reduced this to 1.570s, with 1.482s then spent in schema checks.
The same generated population with compiled schema checks took 0.090s under
cProfile. These are profiling samples, not representative p95 measurements.

The pinned jsonschema-rs 0.59 dependency is justified by this measured gap
against the existing plan targets. It compiles the same Draft 2020-12 resources
offline, uses the reference UUID/date format checks and is parity-tested against
jsonschema on valid and mutated records. jsonschema remains the reference/error
reporting backend. No model runtime, network schema retrieval, persisted cache
or second story authority was added. Installed environments must now install
both locked validation dependencies. See pyproject.toml and requirements-lock.txt.

Committed reads use one binary-length-checked Git cat-file batch plus incremental
source/version/hold indexes. Failed additions do not mutate those indexes. Managed
file protection computes Git blob hashes over exact file bytes (SHA-1/SHA-256 as
indicated by the committed object ID) and reads index entries once; it still checks
every protected file before candidate creation and again before publication.
The Git transaction, private index, expected-parent publication and post-publication
cleanup boundaries remain the same. These changes need full fault-suite verification.

The local jq 1.8.2 binary lives under ignored .tools/jq-1.8.2/; official-release
SHA-256 verified as a6fc67fedaf9128a3309a1e2ebb8b986aeccf70122ee46d2cb4849e423f0c627.
Use its directory on this shell PATH to run tests/speckit-smoke.sh. The initial
real smoke run failed because MSYS converted JSON --arg path values for native jq.
JSON constructor calls now suppress that conversion only for the jq process; file
read arguments retain normal conversion. The unmodified smoke assertions now pass.
All Bash scripts remain LF.

Further profiling found Python file opens dominated the working-file guard:
11.157s of a 14.909s save on a 1,000-exchange fixture under cProfile. The final
guard batches `git hash-object --no-filters --stdin-paths` rather than opening
each file in Python, while retaining every-byte and stage/mode/path checks. A
new real-Git regression checks same-size, same-timestamp tampering for both
SHA-1 and SHA-256 repositories. The measured publication boundary is unchanged.

Actual Linux verification uses Ubuntu 24.04.4 LTS, WSL2 kernel
6.6.87.2-microsoft-standard-WSL2, Python 3.12.3, Git 2.43.0 and ext4. An isolated
user-cache source copy and local virtual environment avoid system package changes.
The initial full run exposed four failures: two installed CRLF resources appeared
modified under LF attributes, and two host-fixture setups inherited executable
text-file modes from the Windows source mount. A failing CRLF installation
regression preceded normalizing framework text resources; original brief/message
text bypasses that normalization. Fixture-only copied files are now mode 0644.
The final Linux run passed 105 tests in 20.871s with no skips or failures.
Linux Bash smoke also passed using verified jq 1.8.2; the smoke uses grep when
ripgrep is unavailable. This verifies structural tooling/storage/CLI behavior,
not a Codex host model or macOS filesystem.

### Cache follow-up after the linear implementation

The uncached 30-run reference read passed on Linux but save p95 was 2.011s,
above 1s; Windows also missed its targets. This measured remaining cost justifies
the optional validation proof cache in validation_cache.py (T063), not a story
state cache. Its explicit external runtime key authenticates proofs, because a
key shipped with untrusted novel data could authenticate its own false claims.
The application reads that key and only writes ignored novel-local metadata.
The benchmark/test harness creates private temporary keys outside novel roots.
Default operation without configured key still fully validates every snapshot.

Proofs bind HEAD, journal entries and actual blob hashes, schema/code/runtime
fingerprints and a private-key HMAC. Deletion/rebuild, malformed/forged proofs,
tracked proofs, actual installed-schema changes, damaged Git object bytes,
novel-supplied keys and current canon authorization all have real-Git regressions.
Every new exchange still undergoes complete validation. An early local-key
prototype is retained only as experimental evidence; the delivered cache rejects
novel-provided trust keys and requires explicit outside-novel runtime configuration.

The final Ubuntu/WSL2 ext4 run passed 112 tests in 18.885s and all 30 warm
measurements completed: read p95 0.826192151s, validation/local-save p95
0.982377050s. These targets pass on that documented reference configuration.
Windows performance and macOS support are separate claims.
