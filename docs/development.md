# Development

**Current delivery policy (owner, 2026-10-28):** all read/save latency targets
are withdrawn. Optimize after functional delivery. Keep every data/authority/
transaction safeguard and report timings without a pass/fail target. Older timing
misses below are historical, not outstanding delivery prerequisites. See
[final functional qualification](../tests/evaluations/final-functional-qualification-20261028.md).

**Single-user POC scope (2026-10-23):** novice testers are out of scope and the
owner will test after delivery. Automated POC verification and starting commands
are in [poc-quickstart.md](poc-quickstart.md) and the
[POC evidence report](../tests/evaluations/poc-readiness-20261023.md). Historical
human/native-host and broad release requirements below do not require manual
testing before this POC can be used. Source labels and all safety/integrity
checks remain unchanged; unknown semantic quality is not called verified.

The user subsequently authorized a separately labeled delegated evaluation route.
The installed `input capture` command requires explicit source selection and
current thread/turn binding; delegation additionally requires an expected parent
and `--evaluation-only`. Include its returned input_artifact in the saved exchange
so source provenance survives reopening. See [the implementation plan](delegated-input-plan.md)
and workflows/entry.md. This adds automated evaluation support without completing
native-input, genuine-novice or human-rating requirements. Earlier unavailable
native-input observations remain valid for their original route and source.

Cross-task automation does not currently supply the native userMessage required
by the Codex adapter. The [2026-10-23 delegated-input probes](../tests/evaluations/product-host-runs/20261023T095949Z/README.md)
found delegation tool output for both task creation and follow-up messages in
English and Icelandic. Those tasks stopped without initializing novels or saving
invented conversations. This limits the automated evaluation route; it does not
revoke the scoped direct typed-input capture result below.

Windows junctions and other reparse points are rejected in managed paths and
the novel's `.git` directory. Keep novel data and Git metadata in ordinary local
directories. See the [junction boundary correction and verification](../tests/evaluations/windows-junction-boundary-20261023.md)
for the tested scope and remaining release gates.

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
does not import the production reducer. Full-scale measurements exist: the earlier
Linux reference passed both targets with the optional authenticated cache;
latest recorded Windows and Linux save p95 remain above one second. See
[performance evidence](../tests/evaluations/performance.md) for configurations
and raw results. Current platform scope is Linux and Windows; macOS is deferred.

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
manual capture-gate test is required for this change. Story tooling is implemented;
its product-level creative judgments and release readiness remain unverified,
along with voice, other hosts and unattended default-sandbox operation.

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
`tests/evaluations/host-capture.md`. The recorded Windows Desktop capture gate
passes within its stated native-tool/text-input/scoped-approval combination;
broader product-host creative and bilingual outcomes remain unverified.

## Delivered commands and recovery boundaries

Foundation packaging, complete shared schemas, structural transition validation,
atomic exchange-save and an independent disposable host-spike fixture are
implemented. `init`, `session list`, `context`, `inspect`, `validate` and `recover`
are delivered commands; session start/mode/close and settings changes are typed
revisions saved through `exchange save`. Fixture helpers remain test-only.

Use the installed launcher in the configured Python environment. Replace the
paths, UUID and checkpoint with the actual recovery inspection values:

```powershell
python C:\Novels\MyNovel\.novel-creator\run.py recover --novel C:\Novels\MyNovel --exchange EXCHANGE_UUID --json
python C:\Novels\MyNovel\.novel-creator\run.py recover --novel C:\Novels\MyNovel --exchange EXCHANGE_UUID --retry --expected-head CONFIRMED_HEAD --json
```

Inspection is read-only and reports `pending`, `published` or `cleanup_needed`,
the confirmed checkpoint, saved status and any held writer lock. Explicit retry
requires the current Git HEAD from inspection; use `unborn` only before the first
commit. A pending retry uses its unchanged receipt payload and original exchange
ID; it cannot replace a changed file or reconcile a stale parent automatically.
Published cleanup retains the saved commit and synchronizes only managed index
entries without replaying decisions or changing unrelated staged work.

Published cleanup failures return saved/cleanup_required and pause further writes
until safe recovery succeeds. Changed managed files, staged entries, receipt
payloads or branch advancement can block cleanup; preserve the evidence and
inspect the conflict. Held writer locks are disclosed and never silently removed.
Never reset history, delete receipts or overwrite conflicting work to clear a pause.

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

### Historical foundation gate decision

The initial foundation assessment recorded T013 as BLOCKED because real automatic
subsequent turns, fresh-chat recovery and controlled save/display interruption
were unavailable. The later scoped PASS described above supersedes that decision;
the [host-capture evaluation](../tests/evaluations/host-capture.md) retains both
sets of evidence. Story tooling has since been implemented. Subprocess fixtures
alone still cannot establish product-host creative quality or release readiness.

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

Large Windows saves partition the final guard's complete byte reads across at
most four Git processes after every metadata/index/path check succeeds.
Inputs below 1,024 managed files and non-Windows runtime policy keep one reader.
Large Windows initial guards use two byte readers; final guards use four. Every chunk retains explicit root binding and complete byte hashing;
all processes/counts must succeed and all workers must finish before publication
or error cleanup. The history, authority, private-index, candidate, conditional
publication and recovery checks remain mandatory. See the
[parallel-hash verification](../tests/evaluations/windows-parallel-hash-20261022.md).

The earlier 2026-10-21 Ubuntu/WSL2 ext4 run passed 112 tests in 18.885s and all 30 warm
measurements completed: read p95 0.826192151s, validation/local-save p95
0.982377050s. Those targets passed on that historical reference configuration.
The four-history-reader source passes all 150 Linux tests. Its Linux performance
has not been remeasured; the earlier overlap source recorded ext4 save p95
1.072006791s. Windows save performance remains an open gate. See the
[latest verification](../tests/evaluations/windows-four-history-readers-20261022.md)
and [source-pinned measurements](../tests/evaluations/performance.md).
macOS support remains deferred.


Large public Windows reads (>=1,024 exchanges) fetch captured immutable blob
OIDs in at most four contiguous requests using the existing Git wrapper. Every
worker joins before parsing or returning. Successful outputs form one original-order
binary stream. Any worker/submission exception or nonzero child exit triggers one
full original serial request before parsing, preserving partial stdout, earlier
damaged-history errors and verified-prefix checkpoints. Small public reads and
non-Windows runtime stay serial. Large Windows saves now select two history readers alongside two first-guard
byte readers; small/non-Windows work remains serial. All history/blob/schema/digest/authority/hold,
path/symlink/mode/live-index, both complete root-bound byte guards, private
candidate, fresh branch/CAS, receipt and recovery safeguards remain. The
previous parallel final-byte guard is unchanged.

Both full suites cover 150 tests. See [current source and measurements](../tests/evaluations/windows-four-history-readers-20261022.md).


## Balanced Windows save readers

Large Windows saves use two history readers and two first-guard full-byte
readers while the original operations overlap. The final full-byte guard and
public history reads retain up to four readers. Each existing 1,024-item
threshold independently keeps small inputs serial; non-Windows defaults remain
one. All metadata/index/path/symlink/mode checks precede each guard's hashing.
All actual blob/digest/schema/authority/hold checks, both complete root-bound
byte guards, private candidate verification, original first-guard error/await
position, worker/lock lifetime, fresh branch/CAS, receipts and recovery remain.
History outputs keep ordered single-stream framing and one full serial fallback
on worker/submission/nonzero exit failure. No check is skipped or moved.

Windows full suite: 143 tests in 567.082s, 141 passed,
2 explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 143
pass in 58.745s, zero skips, exit 0. The same five source/test/harness/
helper fingerprints match before and after both suites and the benchmark.

Ordinary-layout Windows PowerShell with the optional authenticated cache:
first read 2.288559600s; read p95 2.289081100s; validation/local-save p95
9.240644400s. All 30 reads and 30 saves succeed without operation errors or timeouts.
Read misses the unchanged 2s target; save misses the unchanged 1s target.
Benchmark exit 1 records that unmet threshold. No explicit packing/maintenance
is requested. Linux performance has not been remeasured for this source;
its earlier reference results remain historical evidence.

[Current verification](../tests/evaluations/windows-balanced-save-20261022.md).


## Native Windows bundle metadata

Windows ordinary canonical bundle leaves use fresh GetFileAttributesW queries.
Only NORMAL alone or nonzero combinations of ARCHIVE/READONLY/HIDDEN/SYSTEM
classify regular files directly. Invalid, unknown, special, directory, reparse,
unavailable and exceptional results use the original lstat. Parents, other
managed paths, small bootstrap/write paths and non-Windows behavior retain
original checks. Only the API callable is cached; filesystem metadata is fresh.
Both complete live-index/path/type/byte guards, metadata-before-hash ordering,
root binding, full historical blob/digest/schema/authority/hold validation,
private candidate verification, worker joins under the lock, original error
ordering, fresh branch/CAS, receipts and recovery remain. No check is skipped.

Windows: 150 tests in 453.334s, 148 passed,
2 explicit real-symlink privilege skips, exit 0.
Linux/WSL: all 150 tests pass in 48.573s, zero skips,
exit 0. Six source/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Ordinary Windows PowerShell fixture: first read 1.998505000s; read p95
1.320975200s (PASS, target 2s); validation/local-save p95
3.292486500s (UNMET, target 1s). All 30 reads and 30 saves succeed without operation
errors or timeouts. Benchmark exit 1 records unmet performance thresholds.
No explicit Git packing or maintenance was requested. Linux performance was
not remeasured for this source; previous Linux timings remain historical.

[Latest source verification](../tests/evaluations/windows-native-bundle-mode-production-20261022.md).


## Four Windows save-history readers

Large Windows saves now use up to four history readers instead of two.
The existing 1,024-item threshold keeps small histories serial; non-Windows
keeps one reader. The initial full-byte guard retains two readers and the final
full-byte guard four. All history is read and hashed; JSON and ephemeral indexes
are rebuilt. Ordered framing, captured OIDs, original serial fallback, all child
joins, damaged-prefix/error precedence and lock lifetime remain. Fresh native
bundle metadata with conservative lstat fallback, parent checks, both complete
byte/live-index/path/type guards, candidate/tree/digest/parent verification,
authority/hold checks, fresh branch/CAS, receipts and recovery remain unchanged.
No check is skipped and no target is lowered.

Windows: 150 tests in 439.660s, 148 passed,
2 explicit real-symlink privilege skips, exit 0.
Linux/WSL: all 150 tests pass in 50.762s, zero skips,
exit 0. Six source/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Ordinary Windows PowerShell fixture: first read 1.984177600s; read p95
1.183358100s (PASS, target 2s); validation/local-save p95
2.856806500s (UNMET, target 1s). All 30 reads and 30 saves succeed without operation
errors or timeouts. Benchmark exit 1 records unmet performance thresholds.
No explicit Git packing or maintenance was requested. Linux performance was
not remeasured for this source; previous Linux timings remain historical.

[Latest source verification](../tests/evaluations/windows-four-history-readers-20261022.md).
