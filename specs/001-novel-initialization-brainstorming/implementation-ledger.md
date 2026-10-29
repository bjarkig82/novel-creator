# Implementation ledger

Baseline: latest main pulled before execution; clean work branch. No pushes or merges.
Repository workflow and constitution read; requirements checklist 16/16 checked.
Prerequisite script passed with explicit SPECIFY_FEATURE_DIRECTORY selector.
Using executing-plans and TDD. Foundation gate blocks T014 onward.

Preflight: schemas are the shared contract for reducer, storage and installed
fixture; storage owns confirmed Git checkpoints. No story feature may bypass
shared validation. No existing product source or Python tests.

T001–T004: packaging, CLI skeleton, disposable fixtures, locked dependencies and
prerequisites added. CLI contract observed RED (missing CLI), then GREEN:
`PYTHONPATH=src python -m unittest discover -v` (2 tests). Help works. No story
capabilities claimed. Resource packaging will be verified with schema installation.

Ruling: use this durable Markdown ledger rather than skill-specific shell helper
scripts — the cloud skill exposes text but not its script filesystem; equivalent
commands and observed results are retained here — cost if wrong: manual ledger
maintenance instead of automatic task bookkeeping.

T005–T007: schema/digest/source/authorization tests added and observed failing
against absent implementations; now all 13 tests pass via
`.venv/bin/python -m unittest discover -v`. Full typed schema includes all nine
record kinds, perspective/time fields, provenance and routine checkpoint enums.
Canonical schema resources map directly into the installed package (no duplicate
schema copies). Strict JSON rejects duplicate keys/nonfinite literals/invalid
UTF-8. Fold is detached and validates exact predecessor and same-bundle refs.
Actual user-message spans are mandatory for canon transitions; bootstrap artifacts
cannot authorize them. No semantic acceptance claims.

Environment note: system/user site-packages is read-only; dependency installation
was rerun successfully in repository-local ignored .venv, with existing compatible
system packages available. No credentials or global configuration changed.

T008–T010: private-index/CAS persistence and exchange-save dispatch implemented.
Disposable real-Git tests observed RED, then GREEN. Full suite now 28 tests.
Coverage: unborn bootstrap, immutable same-ID retries, competing commit just
before publication, unrelated staged work, manuscript hashes, filesystem/ref/
receipt windows, cleanup pause, path traversal/symlinks, malformed input and
structured checkpoints. Competing candidate remains absent from branch history.
An additional candidate-input race test failed, then passed after rechecking
all candidate file hashes immediately before publication. No reset/amend/push.

Ruling: cleanup recovery remains the later T034 command; foundation reports saved
with cleanup_required and blocks unrelated writes instead of implementing that
story early — blocked saves retain safe evidence — cost if wrong: users must
wait for T034 before automated cleanup recovery is available.

T011: disposable installed fixture and experimental save-before-emit adapter
implemented. Fixture test observed RED, then GREEN. Independent launcher/schema
loading, exact Icelandic text/trailing newlines and display-unknown context pass.
Fixture helpers remain under managed src paths; no production allowlist expansion.

Foundation hardening: strict overflowing numeric JSON and cross-type duplicate
UUID regressions observed RED→GREEN. Valid structural examples cover all
non-decision record types (decision covered by sourced-canon test), all routine
checkpoint enum values and reader-perspective requirements. Full suite: 33 pass.
Wheel build succeeds with both canonical schema resources packaged.

T012: actual host evaluation unavailable/unverified. No native interactive host
turn/fresh-chat/display control exposed; coordinator independently confirmed.
No actual host/model/version evidence fabricated. Structural fixture results are
separate and explicitly cannot pass this gate.

T013: BLOCKED decision recorded in host-capture.md and docs/development.md.
T014+ untouched. T013 completion marker means the stop decision was recorded,
not that the host gate passed. No dependent story work may begin.

Ruling: fixture-only scripts remain separate from production context/install
commands — minimal spike must precede stories — cost if wrong: extra small test
helpers retired or adapted after the actual host gate passes.

Final independent foundation review: four Important findings reproduced with
focused regression tests before fixes. One focused fix pass completed:
- Fixed writer-lock release errors overriding published success; storage and CLI
  retain saved checkpoint, warning and cleanup-required recovery evidence.
- Fixed lost receipt inference; retry compares committed managed entries with the
  real index. Both pre-cleanup and post-cleanup receipt loss are tested.
- Fixed discarded target revisions; exact current target/result authorizes its
  version. Explicit prior proposal acceptance permits only unchanged proposition
  content (status/provenance/revision metadata excluded); changed content fails.
- Fixed wrong-kind typed ID collections; same-bundle forward resolution retained.
Each reproduced fault was observed RED→GREEN. Legitimate unchanged-prior
acceptance was separately observed RED→GREEN after refining the revision rule.
Full final suite `.venv/bin/python -m unittest discover -v`: 41 tests pass.
Missing Git identity test preserves HEAD and pending evidence. Standalone rebuilt
wheel installed into a separate temporary virtual environment and schema validation
passed outside the checkout. Spec Kit Bash smoke checks and git diff --check pass.

Final: minor (deferred): stale-write diagnostics do not yet return separate
expected/actual heads; conditional publication still rejects moved branches.
Final: minor (deferred): committed history enumeration uses padded filenames;
sequence widths beyond six digits need numeric sorting (planned scale is 5,000).

No hooks file exists; pre/post extension hooks skipped. No commits, merges,
pushes, global Git changes or manuscript edits performed. Work stops at the
unverified actual-host gate; all later story/release criteria remain unverified.

## Convergence implementation pass — 2026-10-21

Executing the existing spec/plan/tasks inline with systematic debugging and TDD.
Requirements checklist: 16/16 checked. No extension hooks file. Existing managed
cloud checkout is on work with the previously appended tasks.md preserved.
Python development ignores are present. Installed editable package in ignored
.venv using existing compatible dependencies; baseline: 41 tests pass.

Preflight interfaces: T068 changes source authorization consumed by every canon
transition; T074/T075 share committed-history error handling and ToolError; T084
extends conflict diagnostics without changing publication semantics. These are
foundation remediations and must preserve production fixture/storage contracts.
Story tasks T070–T082 retain their original prerequisites. T083 permits immediate
foundation onboarding; future product instructions remain gated.

Ruling: retain this managed cloud checkout on work and the existing durable
implementation ledger instead of creating another checkout or using unavailable
cloud-skill shell helpers — preserves the user's convergence changes and exact
feature context — cost if wrong: changes require review in this working tree.

T068: complete. The new current-user-message regression failed because historical
authorization was accepted, then passed after binding decision.user_message_ref
to the current exchange. Historical source_refs and unchanged prior-proposition
acceptance remain valid. .venv/bin/python -m unittest discover -v: 42 tests pass.

T074: complete. Non-object committed JSON and malformed local receipt regressions
observed failure (uncaught AttributeError, wrong exit code or unreported scope),
then GREEN. Committed input requires an object; recovery receipts require the
transaction metadata shape before use, including retry and unrelated-save paths.
Errors name the unavailable path, preserve payload/index/HEAD and use code 4.
No generic AttributeError catch hides programming errors. Full suite: 45 pass.

T075: complete. Valid-prefix/damaged-successor and CLI regressions observed RED,
then GREEN for malformed and unsupported successors. read_history attaches the
validated prefix checkpoint and unavailable path; save preserves this error
checkpoint instead of overwriting it with null. A historical commit is named
only if its entire journal tree matches the validated prefix. External prefix
rewrites with no matching valid snapshot report git_head null rather than
labeling a damaged commit confirmed. Full suite: 48 tests pass.

T084: complete. Stale-parent diagnostics (including unborn HEAD) and the real
competing-commit publication race failed their expected/actual-head assertions,
then passed with optional error.expected_git_head/error.actual_git_head fields.
The captured expected parent and observed actual head are reported without
changing CAS publication, pending evidence or unrelated index protection.
Full suite: 50 tests pass.

T083: complete for the delivered foundation. README, development notes and
quickstart now identify executable setup/tests/exchange.save, command placeholders,
cleanup pauses and unverified native-host status. Product journeys remain planned;
T067 remains unchecked for their eventual verified delivery. CLI help, all 50
tests, Bash smoke checks and git diff --check passed.

T012/T069 reassessment: still BLOCKED/unverified. Tool discovery found shell and
thread-summary/status readers but no callable genuine conversation creation/turn
injection or display-interruption/timing control. No actual-host evidence was
collected. Existing evaluation and development docs record this limitation.
T013 is a recorded stop decision, not a passed gate. T070–T082 and original
story/release tasks remain unchecked; no production stories were implemented.

Independent review requested for current source/tests/docs and foundation task
changes. No commits, pushes, merges or actual novel/manuscript edits performed.

Final independent review: no actionable defects. Reviewer checked authority,
malformed-data handling, historical checkpoint safety, idempotency/publication,
stale-head diagnostics and docs, and independently ran all 50 tests successfully.
README Windows activation typo corrected; regression acceptance span points to
the actual acceptance phrase (focused test passed). No new deferred findings.
Cloud review/verification skill packages became unavailable during execution;
review used a fresh read-only agent and actual command evidence directly.

Post-execution hooks: skipped, .specify/extensions.yml does not exist.
Completed convergence tasks: T068, T074, T075, T083, T084. Gate-dependent tasks
remain unchecked. Implementation is partial, not feature/release completion.

## Second convergence implementation pass — T090

Requirements checklist remains 16/16 checked. No pre-implementation hooks.
Using the same current feature artifacts, managed work checkout, ignored .venv
and production contracts; 50-test baseline verified by the preceding converge.
Preflight: writer_lock fails before _save's error-context handler; safe diagnostic
reads may capture an immutable committed tree without owning a writer lock.
No story dependency or actual-host gate is waived.

T090 RED: both new real-Git storage and JSON CLI tests failed all saved/unborn/
unreadable cases because pending_exchange_id was null. The known saved checkpoint
was also missing in the saved case. GREEN: writer_lock accepts the attempted ID
and reads a single captured committed HEAD on contention, retaining valid prefix
checkpoint/unavailable refs on read failure without taking over the lock.
Regressions verify owner/local files, receipts, journal, index and HEAD preservation.
Unborn/damaged genesis contexts retain a null checkpoint. Focused 2/2 pass.
Development docs explain the behavior. Full-suite and independent review pending.

T090 independent review found one Important regression: a committed unrelated
non-UTF-8 filename raised UnicodeDecodeError during best-effort lock inspection.
Fix pass: added POSIX byte-filename storage/CLI cases; both reproduced the
traceback RED. Treating UnicodeError as unavailable inspection preserved the
structured code-6 error and pending ID without inventing a checkpoint. The full
52-test suite then passed, including those cases and installed-fixture checks.
Bash smoke and git diff --check also passed. No other review findings.

T090: complete and marked [X]. T012/T069/T089 remain unverified; T013 remains
a blocked gate decision. Original stories and carry-forward tasks remain
unchecked. Post-implementation hooks skipped: no .specify/extensions.yml.
No commits, pushes, merges, lock takeovers or manuscript edits performed.

## Windows convergence implementation — T102/T111, 2026-10-21

Requirements checklist: 16 checked, zero unchecked; read-only and unchanged.
PowerShell prerequisite check selected this feature. Existing user evaluation
edits/evidence were preserved. Python ignore patterns already cover this setup;
no additional tooling ignore files are needed. No extension hooks are registered.

T102 RED: the new real-Git clean-save/continuation/retry regression failed for
both existing and unborn repositories because cleanup_required was true.
The sandbox initially denied os.link, so meaningful red/green verification used
normal filesystem access with disposable canonical temp repositories outside
the framework. Root cause: sync_index fsync used a read-only descriptor, which
Windows rejects with errno 9. Opening it r+b preserves locking/atomic replacement
and allows the required flush. The regression then passed. CLI/installed tests
now explicitly require cleanup_required false on ordinary successful saves.

T111: canonicalize helper/installed-fixture temp roots without weakening
production path validation. Split real symlink coverage from traversal/payload
tests; Windows privilege error 1314 is explicitly skipped, other errors fail.
Installed-fixture testing exposed a separate expectation bug: read_text folded
CRLF while production correctly saved exact bytes. Compare decoded UTF-8 bytes
instead. The first full run loaded the old expectation and recorded one failure
plus one skip; that log is retained rather than presented as passing.

Final complete suite against corrected source: 54 tests in 187.144s, 53 passed,
one explicit symlink-privilege skip, zero failures/errors, exit 0. All previously
failing Windows index/checkpoint cases pass. Bash syntax and diff whitespace
checks pass. Full Bash smoke unavailable because jq is missing. Current Windows
environment, commands, both full-run logs and limitations are linked in
tests/evaluations/platform-results.md. Linux/macOS were not rerun; physical
power-loss durability, actual host behavior and literary quality remain unverified.

T102/T111 complete. T103/T012/T069/T089 remain unchecked; T013 remains BLOCKED.
The actual-host experiment requires genuine user turns and observed display
interruption/fresh-chat recovery, absent from this implementation session.
Per the plan's blocking capability spike, dependent story tasks remain open;
no simulated conversations, custom runtime or relaxed requirement substitutes
for the gate. Retained host-test fixture, history and receipts were not modified.
No commit, push, merge, manuscript edit or global Git configuration change.
Post-execution hooks skipped: .specify/extensions.yml does not exist.

## Integration for local Desktop testing — 2026-10-21

User explicitly requested committing and pushing these changes to main.
Fetched origin/main; it matches the current base 12fa90b. Fresh pre-push
verification: all 52 automated tests pass, Bash smoke checks pass and
git diff --check is clean. Guide links and recorded JSON evidence validate.
The guide now directs local users to pull main before testing. Include the
foundation fixes, regression tests, convergence tasks, manual Desktop guide and
partial live host evidence. Actual-host gate remains BLOCKED; no product-story
completion or supported-host claim is introduced by integration.


## Actual Desktop gate review — spike-02, 2026-10-21

The user completed real follow-up, interruption, fresh-chat recovery and visible
failure/retry checks. The coordinator created the new independent fixture,
verified pinned checksums and committed history, performed unchanged B/F CLI
retries, and created/removed only its verified empty injected lock. The final
checkpoint is sequence 9, aefc319663a948fcce1ec06d4f1097e084f864fc.

B/C/D/E/F evidence is supported. Seven displayed final assistant messages match
committed replies exactly; one successful saved response was interrupted before
final display. Scoped normal-access retries were necessary after initial and
fresh-chat sandbox os.link denials. No default-sandbox unattended claim is made.

All eight native public user-message readbacks contain a terminal LF omitted
from the corresponding committed user text. It is not established whether this
is capture loss or a host envelope convention. No silent normalization, record
rewrite or requirement waiver is permitted. T012/T069/T089/T103 remain unchecked
and T013 remains BLOCKED pending narrow adapter boundary investigation. The
requested human exercises are complete; no repeat of the Stop case is presently
needed. Public message/receipt/status evidence and unnormalized comparisons are
exported under tests/evaluations/host-capture-runs/20261021T161928Z-spike-02/.
No hidden reasoning, private transcript scrape, model API, manuscript edit,
commit, push or history reset was introduced.


## T116 native-input remediation — 2026-10-21

Converge appended Phase 13 T112-T123, preserving all prior task bytes and spec/plan.
The user then authorized tackling the newline issue. The exact-text gate remains
respected; this is adapter/foundation work, not a dependent story implementation.

Identified the input materialization boundary: native user text has an ending
LF absent from manually reconstructed PowerShell here-strings. Direct probe
confirms the closing-marker newline is excluded; existing storage reads exact
bytes. Do not infer a universal delimiter or blindly append/strip whitespace.
The native userMessage text is now the explicit Desktop capture boundary.

RED: installed-fixture regression failed all four valid text cases because
--user-message-file did not exist. GREEN: added a mutually exclusive native JSON
input mode preserving its one text string, with wrong-role/multi-input rejection.
Updated the host adapter to obtain current native userMessage via read_thread
and CODEX_THREAD_ID and serialize it directly, stopping on missing/ambiguous
source. No private transcript reads, model API, app modification or schema change.

Full suite: 55 tests in 121.279s, 54 passed, one explicit symlink-privilege skip,
exit 0. New cases cover LF/CRLF, multiple ending blank lines, leading spaces,
Icelandic text and absent final newline, plus invalid native source rejection.
Full log and native-boundary rationale are under tests/evaluations/. Fresh
spike-03 contains pinned revised instructions/helper; clean bootstrap, 13 verified
checksums, no cleanup needed. Spike-02 and all prior evidence are unchanged.

T116/T103/T012 remain unchecked and T013 BLOCKED pending one focused real typed
Desktop message with unnormalized native-source/payload/commit/final comparison.
The existing human Stop, fresh-chat and failure/retry evidence need not be
repeated for this input-only change. No release or supported-host pass is claimed.
Post-execution hooks skipped: .specify/extensions.yml does not exist.


## T116/T103 final actual-host gate — PASS, 2026-10-21

Spike-03 native userMessage equals the programmatically serialized source,
prepared payload and committed user text, with terminal LF preserved. Exact
displayed assistant final is Native capture is ready.; successful save event
precedes display. Checkpoint sequence 2, exchange
1e9054a1-f963-4a15-9b8e-35e0d32fe837, commit
bc7318a0d534b8e21600cedc669d67661e8daf34. All 13 checksums verify; Git status
is clean and cleanup_required false. Evidence exported under
tests/evaluations/host-capture-runs/20261021T171237Z-spike-03/.

The initial root-local source placement collided with receipt discovery; moving
source JSON under local/evidence resolved it with payload unchanged. A sandbox
hard-link denial then required scoped normal filesystem retry, which succeeded.
Adapter instructions now explicitly require the evidence subdirectory, and the
installed regression exercises that path. Original spike-02 history and native
LF mismatches remain untouched. Its B/C/D/E/F evidence continues to establish
retry, interruption, fresh-chat recovery and visible failed-save handling.

T012/T069/T089/T103/T116 marked complete; T013 latest decision PASS. Scope is
Windows Desktop OpenAI.Codex 26.1016.6573.0, visible GPT-6.1 Sol Medium selector,
available native tools, single typed text and scoped filesystem approval. Model
revision, voice, other hosts, unattended default sandbox, physical power-loss
durability and full story/release behavior remain unverified. No further human
Stop-button test required. Dependent story work can begin; none marked complete.

Final full suite after evidence-path regression: 55 tests in 216.277s, 54 passed,
one explicit Windows real-symlink privilege skip, zero failures/errors, exit 0.
Log: tests/evaluations/windows-native-evidence-path-tests.txt. Exported JSON
parses; all recorded parity checks true. Git diff whitespace check passes.
Post-execution hooks skipped: .specify/extensions.yml absent. No framework commit
or push, remote change or old-fixture rewrite performed.


## Story implementation continuation after T103 — 2026-10-21

User explicitly requested another speckit-implement run. PowerShell prerequisites
selected this feature; requirements checklist read-only scan was 16/16 complete.
No extension configuration exists before or after implementation. Existing local
changes and historical fixtures/evidence retained; no framework commit or push.

Delivered init/standalone pinned bundle, UTF-8 original bootstrap artifact and
JSON Pointer provenance, unknown/default distinction, BCP-47 language tags,
revisable settings with stable identity and immutable original concept. Existing
instructions are preserved, occupied/nested targets rejected, prerequisites/
identity checked before setup, and partial setup retries its saved original plan.
Recognized novels continue without overwriting; cleanup-needed remains disclosed.
Resources are included in setuptools packaging, not fetched from the framework
by the installed reader. Explicit setup paths include AGENTS.md only during setup.

Added new_exchange, project/session revision and checkpoint summary helpers;
installed context/session-list/inspect/validate, focused record selection, sources,
history, current canon and direct impact. Session mode/topic changes preserve
prior versions; closed sessions require explicit reopen through the helper.
Read views are derived, carry a checkpoint and never claim a literary verdict.
Recovery distinguishes pending/published/cleanup-needed; explicit expected-HEAD
retry preserves payload/IDs, never replays a published save, refuses changed
managed files/index entries and preserves unrelated staged work. Held locks
remain untouched. No stale-lock theft or implicit ref reset was added.

Authored shared initialize/brainstorm/resume/authority/continuity/entry resources,
four thin Codex skills and English/Icelandic language guidance. Strengthened
partial selection, supersession, open/deferred finding holds, sourced finding
dispositions and unknown timing. Added sourced five-revision/manuscript-protection
and damaged/restored-journal journeys. Paired authored 12+12 acceptance, five
revision and six-category conflict expectations remain semantically unverified.
Independent test reader reconstructs connected records from committed JSON/Git
without importing production reduction or re-extracting conversation prose.

RED/GREEN: new initialization/session/recovery APIs initially failed as missing;
focused-context, partial acceptance, finding holds/unsourced resolution, unknown
time and repeated-init cleanup disclosures reproduced behavioral failures before
correction. An intermediate 76-test full run retained a test-fixture statement
argument collision; it was corrected and its journey separately passed. A later
87-test full run passed with one skip. Final current-source suite: **90 tests in
304.636s, 89 passed, one explicit Windows symlink-privilege skip, no errors or
failures, exit 0**. Full log tests/evaluations/windows-story-final-tests.txt.
Normal filesystem access and the canonical external temp root were used because
the sandbox denies publication hard links. The installed isolation test uses -I
and verifies every product module path lies under the independent novel.
Wheel build succeeded and packaged workflow/language/skill/schema resources were
inspected. Git diff whitespace check passes. No speculative performance cache.

Task closures are recorded in tasks.md, including T014–T020, T022–T026,
T029–T030, T033–T035, T037, T039, T042, T045, T047, T049–T050, T053,
T056–T057, T061, T067 and recovery equivalents T078/T093/T106/T119.
Broader convergence tasks are intentionally not closed from partial structural
evidence. Actual product-host capture/extraction/guidance/authority/continuity,
five-novice outcomes, semantic bilingual parity, complete consumer/version cases,
representative performance and platform/durability release evidence remain open.
This is implementation progress, not full story/feature/release completion.
Post-execution hooks skipped: .specify/extensions.yml absent.

## Phase 14 implementation continuation — 2026-10-21

Checklist gate: requirements.md 16/16, read-only. No extension hooks registered.
Existing working changes retained; no commit, push or external product mutation.

T124: observed twelve negative unit subcases fail before the fix. Normal-access
real-Git execution also reproduced a metadata-only hold bypass. The sandbox
could not publish os.link, so that environment error is excluded from correctness
evidence. Prior active conflict scope is now protected until a sourced current-user
terminal disposition permits resolution. All three bypasses, proposal-only delayed
bypass, legitimate dispositions and save/retry preservation are covered.

T054/T058/T131: independent-reader tests first failed for dangling record/message
references and wrong creation origin, then passed after independent checks were
added. The representative fixture covers all nine kinds, all entity types, timing
precision/perspectives/truth states, renaming/duplicate names, current/superseded
history, sourced decisions and cache deletion. The isolated installed interpreter
now saves and exercises context/list/validate/inspect. Seven focused tests passed
in 34.800s. These task markers are complete within their structural scope.

T132 is partial: repeatable generator/measurement tooling now exists. The full
100-session/5,000-exchange/10,000-active-assertion fixture is 26,215,716 bytes.
Its first context-read subprocess hit a 30-second deadline, so full validation
and all warm p95 values remain unverified. The tool records explicit timeouts
and exits nonzero for unmet targets. See tests/evaluations/performance.md and
raw result files. No production performance optimization/cache is claimed.

T125-T130 retain missing real novice/product-host/bilingual judgments. T133
retains missing Linux/macOS, full quickstart and release evidence; the actual
Bash smoke attempt failed because jq is unavailable (the initial sandbox
MSYS startup failure was retried with normal access). No human observations,
creative judgments or cross-platform passes were fabricated.

Final Phase 14 automated result: 98 tests in 305.484s; 97 passed and one
explicit Windows symlink-privilege skip, exit 0. Log:
../../tests/evaluations/windows-convergence-final-tests.txt. Latest continuity/
benchmark fixture focused rerun: six passed. Whitespace check passed; spec/plan
unchanged. No before/after implementation hooks exist. Full feature/release
completion remains unclaimed for the missing gates above.

## Performance and platform continuation — 2026-10-21

Completed T062/T063/T081/T096/T109/T122/T132 against the documented Linux
reference configuration. The complete 100-session/5,000-exchange/10,000-assertion
fixture contains 26,215,716 JSON bytes. Thirty warm samples give read p95
0.826192151s and validation/local-save p95 0.982377050s; first read 1.615959638s.
This requires the opt-in authenticated proof cache with an explicitly configured
private key outside the novel. Default operation still performs full validation.
Windows cached read p95 is 1.745070200s; save p95 is 6.771292200s and remains
above the one-second target. No platform-wide latency guarantee is claimed.

Profiling justified incremental validation, compiled offline schema checks,
batched Git object reads/hashes and removal of redundant path processing.
Proofs contain no canonical story data, bind source/runtime/schema identity,
require independently configured trust and verify actual Git blob hashes.
New exchanges retain complete authority/continuity/transition validation.
Deletion, forgery, tracked metadata, schema staleness, corrupt object bytes,
novel-supplied keys and same-size/same-timestamp tampering have regressions.
The CLI only reads external key configuration and writes novel-local files.

Final Linux/Ubuntu 24.04.4/WSL2/ext4 suite: 112 tests in 21.138s, all passed,
zero skips. Installation tests exposed and verified fixes for CRLF framework
resources and executable fixture modes without changing original user bytes.
Full Bash smoke passes on Linux and Windows Git Bash with SHA-256-verified jq
1.8.2. Windows JSON constructors preserve POSIX paths under MSYS. See current
tests/evaluations/performance.md, platform-results.md and release-readiness.md.

T125-T130/T133 remain open for actual product-host creative/bilingual cases,
five genuine novice observations, macOS and complete release evidence.
Participant worksheets are prepared; no observations or semantic results were
fabricated. Earlier timeout, missing-jq and untested-Linux notes above are
historical. No commit, push, provider call or production change was made.

## Final performance continuation verification — 2026-10-21

Windows full suite: **112 tests in 268.801s, 111 passed, one explicit real-symlink
privilege skip, zero failures/errors; exit 0**. [Full log](../../tests/evaluations/windows-performance-final-tests.txt).
Linux full suite: **112 tests in 21.138s, all passed, zero skips; exit 0**.
[Full log](../../tests/evaluations/linux-trusted-cache-final-tests.txt). Full Bash smoke passes on both.
Reference performance tasks T062/T063/T081/T096/T109/T122/T132 are complete
within the opt-in Linux cache configuration recorded in performance.md.
Windows save latency remains above target. T125-T130/T133 and their original
host/human/bilingual/macOS/release obligations remain open. No release approval
is inferred. Final whitespace checks passed; Bash scripts retain LF; spec and
plan are unchanged. No extension hooks are registered (.specify/extensions.yml
is absent). No commit, push or external provider operation was performed.

## Platform scope decision — 2026-10-21

The user deferred macOS support for now. macOS is outside the current release
scope and is not a release blocker; no macOS support or verification is claimed.
This supersedes earlier macOS gate references in this document. Linux and Windows
remain in scope. Actual host/bilingual evaluations, five novice observations,
Windows save performance and the remaining release checks are still required.

## Independent guidance continuation — 2026-10-21

User confirmed no novice observations are available and requested continued
independent work. Added tests/integration/test_guidance_journey.py, exercising
four prepared exchanges through the installed CLI: exact Unicode/newline
messages, guided/open/guided mode changes, topic redirection, fewer-suggestion
preference retention, prior proposals and current-message source/checkpoint
consistency. Authored replies are structural fixtures, not product-host judgments.
T027 and broader human/host obligations remain open; no checklist markers changed.

Fresh full suites: Linux/WSL2 **113 passed in 39.578s, zero skips**; Windows
**112 passed, one explicit symlink-privilege skip in 295.635s**, zero failures or
errors, both exit 0. Git Bash smoke passes; Bash scripts retain LF and whitespace
checks pass. Full logs and commands are linked from tests/evaluations/release-readiness.md.
Initial sandbox hard-link denial was rerun with normal filesystem access; it is
not a product failure. No extension hooks are registered.

Aligned current quickstart, performance and release-guide instructions with
deferred macOS support. Production code, dependencies, schemas and acceptance
thresholds are unchanged in this pass. No commit, push, provider call or release
approval occurred. Actual host/bilingual evaluations, novice observations, Windows
save performance and overall release verification remain incomplete.

## Bilingual push and Windows save continuation — 2026-10-21

Under explicit user authorization, bilingual pitfall fixtures, their contracts
and evidence were committed/pushed to main as bd9f475. The full remote SHA was
verified as bd9f47515a6bab614298e57b96da52f733b61cff. Subsequent performance work
is local and has not been committed/pushed.

Profiled the current full-scale Windows save, discarded Git transport variants
without consistent benefit, then removed repeated immutable-tree lookups and
shared-directory stat calls within each individual managed guard pass. Every
leaf and full file hash is still checked on both passes; directory checks are
fresh for each pass. Live-index guards, private candidate index, parent/delta/
digest checks, compare-and-swap ref publication and flush/cleanup semantics remain.

Five alternating baseline/optimized saves reduce median time from 3.705116s to
3.173141s (14.36%). The prescribed fresh-process 30-read/30-save run completes
without operation errors/timeouts: cold read 3.070803300s, warm read p95
1.597038600s (PASS), save p95 3.845654300s (UNMET; unchanged target 1s, exit 1).
The older Windows p95 of 6.771s remains historical evidence; its larger timing
difference cannot all be attributed to this optimization. No new Linux timing
claim is made.

New regressions test SHA-1/SHA-256 same-size/same-timestamp tampering after
candidate preparation and a shared-directory symlink replacement between guard
passes. The final Linux/WSL2 suite passes 118 tests with zero skips. Final Windows
verification and all raw logs are recorded in tests/evaluations/windows-save-optimization.md.
T133 and real host/human/bilingual/novice release gates remain open. No schema,
dependency, transaction authority, checklist marker or performance target changed.

Final Windows full suite: 118 tests in 303.150s, 116 passed and two explicit
real-symlink privilege skips, zero failures/errors, exit 0. Both skipped cases
pass on Linux (118/118 in 51.548s). Whitespace checks pass. No extension hooks
are registered. Windows save p95 remains above target; no task/release gate is
waived. Performance changes remain local/uncommitted; only bd9f475 was pushed.

## Implementation gate review — 2026-10-21

Re-entered through speckit-implement using the PowerShell prerequisite script.
The active feature is this directory; requirements.md passes 16/16 and remains
unchanged. No extension hooks are registered. The user confirmed that no new
evaluation results are available. T125–T130 and T133 retain their host, novice,
bilingual and release evidence requirements; no task markers were closed.

Reviewed the existing uncommitted storage optimization and its race/tampering
regressions. Immutable tree reuse does not replace fresh index or byte-hash
checks, and the directory-check set is recreated for each guard pass. The
recorded Windows profile and discarded transport experiment do not justify
another production change in this pass. The existing 30-run benchmark still
records read p95 1.597038600s and save p95 3.845654300s; these were inspected,
not remeasured. The one-second save target remains unmet.

Fresh focused verification: `.venv/Scripts/python.exe -B -m unittest
tests.integration.test_storage -v` ran 28 tests in 68.510s with 26 passed,
two explicit Windows symlink-privilege skips, and exit 0. UTF-8 and disabled
bytecode were configured; TEMP/TMP used this chat's canonical visualization
directory outside Git repositories. See
[normal-access log](../../tests/evaluations/windows-implementation-storage-review-normal-access.txt).
The initial sandbox run was denied at `os.link` (WinError 5), before save
behavior could be exercised; its failures are environment evidence, not a
product result. See
[sandbox log](../../tests/evaluations/windows-implementation-storage-review.txt).

This pass adds verification evidence only. No production source, dependency,
schema, acceptance target, checklist marker, commit, push or provider operation
changed. Full feature completion and release readiness remain unclaimed.

## Phase 15 documentation implementation — 2026-10-21

The PowerShell prerequisites select this feature. The requirements checklist
passes 16/16 and remains read-only; no extension hooks are registered. Existing
source/performance work is preserved. T134–T139 require actual product-host,
bilingual and novice observations, which the user has confirmed are unavailable.
T140 retains the measured Windows save gap; no production code or benchmark
configuration was changed and no new timing result is asserted. T142 remains
dependent on those outstanding evaluations/performance results.

T141 complete: corrected README.md, docs/development.md and
docs/testing-and-completion-guide.md to describe implemented commands, read-only
recovery inspection, explicit unchanged-payload retry, expected-head/unborn,
published managed-index cleanup without replay, conflicting payload/files/index
or stale HEAD, and safe write pauses. Historical fixture procedures are identified
separately from current installed commands. Current Linux/Windows scope, deferred
macOS, the scoped capture-gate PASS, Linux reference performance and the unmet
Windows save target are consistent. No host or human outcome is invented.

Fresh verification: `.venv/Scripts/python.exe -B -m unittest
tests.integration.test_recovery tests.integration.test_portable_install -v`
passes six tests in 17.383s with no skips/errors (exit 0). See
[focused log](../../tests/evaluations/windows-recovery-docs-tests.txt).
An additional disposable installed-novel command check exercises `recover --help`,
pending inspection, missing/stale expected-head rejection, unchanged bootstrap
retry with `unborn`, published cleanup and repeated retry with no new commit,
and changed pending-file rejection/preservation. Every check passes (exit 0):
[installed CLI log](../../tests/evaluations/windows-recovery-docs-cli-smoke.txt).
The throwaway verification script is in this chat's external visualization
directory, not a product module or permanent regression test. Verification used
UTF-8, disabled bytecode, canonical external temporary repositories and normal
filesystem access for the production hard-link operation.

Only T141 is newly marked complete. The ignore configuration covers the current
Python setup; no new technology-specific ignores are required. Spec/plan hashes
are unchanged. No full-suite, Linux rerun, performance remeasurement, release
approval, source/dependency/schema change, commit, push or provider call occurred.

## Windows performance continuation — 2026-10-22

The user explicitly authorized Windows save performance work and deferred novice
evaluations because participants are unavailable. Ruling: proceed with T149
independently of the human evaluation tasks; keep T143/T144 and all original
human criteria unverified and unchecked. This changes execution order, not
release requirements. Existing uncommitted work is preserved.

The initial full-scale profile hit the Windows sandbox hard-link denial
(`WinError 5`); it is retained as environment evidence in
tests/evaluations/windows-save-profile-20261022.txt. The same disposable profiling
command was rerun with normal filesystem access. No transaction safeguards,
thresholds, dependencies, provider calls or shared Git state were changed.

Discarded `cat-file --buffer`: eight paired bulk reads per variant produced
medians of 0.582097s unbuffered and 0.597421s buffered, with identical bytes;
whole-save samples also showed no benefit. No transport change was retained.

Implemented `_verify_candidate` using a full tree delta comparison and a single
batched commit/blob read in place of four separate candidate inspection calls.
Commit hash, exact parents, allowed path/mode/OID delta, exact bundle and payload
digest are checked before publication. Both full working-byte/path/live-index
guards, private index, CAS, source/authority/hold validation, receipts/fsync and
recovery remain. New real-Git tests cover both Git object formats and tampered
trees, parents, bundles and batch output. The initial focused test failed on the
missing verifier, then passed after implementation. An independent read-only
review found no concrete safety or correctness issues.

Ruling: retain the verifier for its measured component benefit (0.227261500s to
0.110481450s, 51.4%) and preserved checks. Cost if wrong: additional parser
complexity without a demonstrated whole-save gain. The matched whole-save
medians are 3.115621350s before and 3.147080250s after, so no end-to-end
improvement is claimed.

Fresh verification: Windows full suite 120 total in 377.170s, 118 passed and two
explicit real-symlink privilege skips, zero failures/errors, exit 0. Linux/WSL2
full suite 120 passed in 56.558s, zero skips, exit 0; both real-symlink cases
execute there. No new Linux timing or host-support claim is made.

The full Windows benchmark completes 30 reads and 30 saves without operation
errors/timeouts: cold read 3.587267600s, read p95 3.252935300s and save p95
5.907091200s. Both unchanged thresholds are unmet, with expected exit 1. The
cause of the difference from the earlier 2026-10-21 p95 is not established.
Raw results, commands, hardware, source hashes and limits are linked from
tests/evaluations/windows-candidate-optimization-20261022.md. T149 remains open.

Novice tasks T143/T144 remain deferred/unverified and unchecked. No requirement,
spec/plan, schema, dependency, threshold, machine security setting or manuscript
was changed. Existing unrelated dirty work is preserved. No commit, push,
provider call or release approval occurred. No extension hooks are registered.

## Full-history and file-check continuation — 2026-10-22

The user explicitly requested continued T149 work on full-history reads and file
checks without weaker safeguards. Novice evaluations remain deferred/unverified.
The prerequisite script selects the same feature. Existing dirty work is preserved.

Disposable experiments reject object-ID request sorting and command-local Git
fscache because neither improves timings. A 1 MiB Windows pipe reduces bulk-read
median by about 9%, but Ruling: do not retain custom Windows IPC for this modest
component benefit — added handle/thread complexity is not justified; cost if
wrong: leaving about 0.054s of observed bulk-read savings unrealized.

Relative guard paths reduce diagnostic median 0.451939650s to 0.404683500s while
retaining every path/index/byte check. This small representation change is
implemented. New invariant tests cover Unicode/spaced paths, decoy cwd/Git env,
same-size/mtime changes and staged changes in both Git object formats.

Packing disposable Git objects reduces bulk-read median to 0.276538050s in a
sequential diagnostic. No automatic or real-novel maintenance is introduced.
The benchmark's explicit --pack-fixture configuration verifies unchanged HEAD/
tree and records maintenance time outside operation timers; defaults remain.
The initial read-only review found no actionable issues; follow-up review found
the root-binding defect described below before retention. Full regression and
matched/fresh-process measurements follow before any completion claim.

Follow-up review identified a P1 in the uncommitted relative-path prototype:
Git setup can change cwd to an ancestor core.worktree after initial root
validation. Combined with duplicated index prefixes, this masked actual-root
same-stat tampering. A real-Git test demonstrated the failure for SHA-1 and
SHA-256. The bulk hash call now explicitly binds trusted GIT_WORK_TREE to the
validated root. The adversarial test and root/cwd/index tests pass after the fix.
No actual user novel was modified. Earlier 121-test/prototype timing logs are
retained as intermediate evidence, not final verification of this source.

The staged-change fixture now uses a known blob OID and update-index directly;
git add may skip same-size/mtime edits and did not deterministically establish
the fixture's intended staged mutation. No assertion or runtime guard was relaxed.

Final frozen Windows verification: 122 tests in 326.671s, 120 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 122 in 60.080s,
zero skips; both final focused guard fixtures also pass after the deterministic
index-fixture correction. Input fingerprints and final logs are linked from
tests/evaluations/windows-history-guard-optimization-20261022.md. The earlier
Windows fixture failure remains preserved as intermediate evidence.

Final matched diagnostic: file-guard median 0.762300100s -> 0.532218250s;
whole-save median 4.314992800s -> 3.646429000s. Four samples per variant are
diagnostic, not p95 compliance. Packing an identical disposable snapshot lowers
read median 2.263453150s -> 1.534817100s but does not improve its save median
(3.777716700s -> 3.868343500s).

Canonical complete-fixture measurements, 30 fresh-process reads and saves each,
opt-in external-key cache, zero operation errors/timeouts:
ordinary first read 2.354371000s, read p95 1.715363500s, save p95 3.398351400s;
explicitly packed first read 1.913063100s, read p95 1.020150600s, save p95
2.739170400s. Packing takes 4.742777600s separately, outside operation timers.
These sequential layout runs do not isolate a packing-only save gain. Both
benchmarks exit 1 for the unchanged 1s save gate; reads pass 2s. T149 remains
unchecked. Source/test/benchmark fingerprints remain unchanged throughout the
final suite and measurements. Raw data, environment, logs and source hashes:
tests/evaluations/windows-history-guard-optimization-20261022.md.

T143/T144 remain deferred/unverified. No actual novel was packed or edited; no
threshold, schema, dependency, machine setting, spec/plan or requirement changed.
All byte/path/index, validation/authority/hold, private-index/CAS, receipt/fsync
and recovery safeguards remain. Existing dirty work is preserved; no commit,
push, provider activity or release approval occurred. No extension hooks exist.

## Further T149 diagnostics and snapshot reuse — 2026-10-22

The active goal remains completing remaining tasks; novice evaluations remain
explicitly deferred/unverified. Fresh directory-enumeration metadata shows only
a small noisy gain, and queued Git batch commands show nearly unchanged bulk
read time. Neither is retained. An isolated pinned pygit2/libgit2 SHA-1 prototype
is slower for bulk objects, full-file guards and saves; no native dependency or
backend is retained. See tests/evaluations/windows-native-git-investigation-20261022.md
and its raw logs. These are diagnostic samples, not replacement p95 measurements.

The next narrow change removes one duplicate immutable committed-tree read from
save. Public read_snapshot captures the tree then delegates to a private reader;
save captures the tree once under its writer lock and passes it to both the full
history reader and first file guard. Every blob still gets fetched and checked;
both guards still independently read live index/working bytes. Nothing is cached
across operations, and explicit trusted worktree binding remains intact.

A real-Git SHA-1/SHA-256 test proves an explicit old checkpoint still reads its
own history after HEAD advances. It passes before the change, then all five
focused snapshot/root/index/same-stat/bootstrap/retry regressions pass afterward
(68.004s). The read-only follow-up review finds no actionable issues. Current storage SHA-256:
57ba0d7f4dbb3c3ac68a70a74559236c36dadfad07713550f7970369f739a59b.

Final frozen verification: Windows 123 tests in 405.898s, 121 passed/two explicit
symlink-privilege skips, exit 0; Linux all 123 passed in 68.212s, zero skips,
exit 0. The matched trace shows 25 -> 24 Git calls and three -> two tree reads,
while all four live-index, four hash-object and two cat-file calls remain.
Whole-save medians 5.859287100s -> 4.449307250s are diagnostic only; the omitted
tree query's median 0.070551150s cannot explain the entire observed difference.

Full-scale 30-read/30-save runs complete without operation errors/timeouts.
Ordinary: first read 4.719507600s, read p95 3.545458500s, save p95 6.626094600s.
Packed: first read 4.780076500s, read p95 2.277303600s, save p95 4.562267800s;
maintenance takes 6.001285800s outside timers. Both runs exit 1: both targets
unmet. Higher p95 versus earlier runs has no established cause, and those
historical comparisons cannot isolate source effects. All frozen inputs remain
unchanged throughout verification/measurement. Evidence and raw results:
tests/evaluations/windows-snapshot-reuse-20261022.md.

T149 stays unchecked. T143/T144 remain deferred/unverified; remaining host,
semantic and final-release obligations are not substituted with structural
tests. No safeguard, target, spec/plan, dependency file, schema, actual novel,
machine security setting or manuscript was changed. No provider call, commit or
push occurred; existing dirty work is preserved. No extension hooks exist.

## T149 first-guard overlap — 2026-10-22

The next full-scale diagnostic overlaps complete committed-history validation
with the complete first managed-file guard. Same captured immutable tree,
writer lock, required first-guard result before receipts/candidates, and unchanged
second fresh guard before publication. Initial four-sample prototype medians:
3.263001450s serial -> 2.803969000s overlap; diagnostic only, not p95.

This changes a permitted external-race timing: editing managed bytes after the
background guard finishes during validation may leave pending work before the
second guard rejects it. Coordinated SHA-1/SHA-256 tests assert no publication,
unchanged user index/HEAD, preserved external bytes and truthful pending recovery.
A second case gives unreadable history precedence over simultaneous guard
failure and preserves the last valid checkpoint without pending files or a lock
leak. The serial baseline cannot exercise the coordination; the new cases fail
their wait conditions there, then all five focused cases pass after implementation
in 23.715s. Read-only review finds no actionable issues and explicitly retains
the changed pending-race semantics. Executor shutdown precedes lock release;
absent-HEAD bootstrap and existing-path retry behavior stay serial.

A separate installed-Git launcher/direct-binary diagnostic shows reduced startup
and save medians; no product selector or machine PATH change is introduced.
Git Bash normally selects the direct binary on this host, so an additional
native Windows Git Bash packed fixture will be measured separately. The harness
now records the selected executable. Full suites, matched final-source saves and
three sequential 30-run configurations complete against frozen source/tests.
Candidate storage SHA-256:
16de2fab76922e9252924eada706c7a8d5071875c68e155279192edd749b5828.
Evidence: tests/evaluations/windows-guard-overlap-20261022.md. T149 stays open;
novice evaluations remain deferred/unverified, and no safeguard/target is waived.

Final frozen suites: Windows 125 tests in 318.673s, 123 passed/two explicit
real-symlink privilege skips, exit 0; Linux all 125 passed in 36.951s, zero skips,
exit 0. Final Windows paired save medians 3.014429850s serial -> 2.673034800s
overlapping (11.3% lower), diagnostic only; complete live-index/hash/object
commands remain in the trace. Source/test/benchmark fingerprints match after
both suites, the matched diagnostic and all three Windows configurations.

Each configuration completes the full validated fixture and 30 reads/saves with
zero operation errors/timeouts. Ordinary PowerShell first/read/save p95:
2.672013800s/2.014926100s/2.733241800s, both targets unmet. Packed PowerShell:
1.977750300s/1.045105700s/2.209314500s, read passes/save misses; packing takes
4.524228100s separately. Packed native Windows Git Bash:
2.225943200s/0.942910200s/1.719383700s, read passes/save misses; packing takes
2.971372300s separately. All exit 1 for unmet thresholds; ordinary read is not
rounded into a pass. The Git Bash configuration does not replace default-shell
performance or establish a new full installation/host gate.

The current Linux reference uses identical runtime/schema bytes staged on ext4,
with canonical ext4 fixtures and temporary trusted key. All 30 reads/saves
succeed, first read 2.171033683s/read p95 1.153318426s/save p95 1.072006791s:
read passes/save misses, exit 1. The older Linux pass remains historical, not
claimed for this current-source run. A same-fixture eight-save-per-variant Linux
comparison lowers median 0.948380694s -> 0.788780154s (16.8%), but does not
establish p95 compliance or explain the tail. Both Linux source manifests confirm
unchanged current source. Raw data, loaded resource locations and reproduction:
tests/evaluations/windows-guard-overlap-20261022.md.

T149 stays unchecked and no current-source configuration passes both targets.
All remaining host, semantic, human and final-release obligations remain open;
novice evaluations remain explicitly deferred/unverified. No actual novel,
dependency, schema, persistent machine setting, spec/plan, checklist or manuscript
is changed. No provider call, commit or push occurs; unrelated dirty work is
preserved. No extension hooks are configured.


## T149 canonical path allocations — 2026-10-22

Retained the reviewed canonical-bundle parsing fast path and avoided discarded
Path objects in guards. The public signature/return and other path validation
remain. Both complete filesystem/index/root-bound byte guards, full history,
authority/hold, candidate verification, CAS and recovery remain unchanged.
A behavior regression matrix passes on the prior source and the candidate.
The four-sample-per-variant full-fixture diagnostic lowers guard/save medians
by 20.8%/18.9%; these are limited diagnostic results, not p95 compliance.
GC suppression and benchmark graph-release policy are not retained.

Final retained-source tests: Windows 126 tests in 373.021s, 124 passed and
two explicit Windows symlink-privilege skips, exit 0; Linux all 126 pass in
82.276s, zero skips, exit 0. The Windows and Linux manifests record the source
fingerprints; Windows before/after hashes match across tests and measurements.

Final-source Windows Git Bash, explicitly packed disposable fixture: first read
3.200534500s, read p95 1.587495700s, validation/local-save p95 3.645534700s.
All 30 reads and 30 saves succeed without timeouts or operation errors. Read
passes its 2s target; save misses its 1s target. Exit 1 records the unmet threshold.
Packing takes 5.748657100s outside operation timers and is fixture preparation,
not product behavior. This configuration does not establish ordinary-layout
performance. Linux performance has not been rerun for this path-allocation source;
previous overlap-source measurements remain historical and source-pinned.

Source, commands, raw samples, baseline bytes, original sandbox cleanup failure
and review boundaries are preserved in
tests/evaluations/windows-allocation-investigation-20261022.md.
T149 stays unchecked; novice evaluations remain deferred/unverified. Other
human/host/language/release requirements remain open. No real novel, dependency,
schema, machine setting, provider, spec/plan or checklist is changed.

## T149 current-source critical-path investigation — 2026-10-22

The preceding continuation retained the path optimization, new regression
matrix, frozen-source full suites and 30-run result. This investigation
preserves that verified source (storage
69ff00ee3e3a864a458f8c26074e241932911f58c654551afb1b22285eba3035) and all
save checks. New diagnostics use the complete 5,000-exchange/10,000-assertion/
26,215,716-byte fixture, structurally validated before timing.

Combined JSON decoding is slightly slower (parser median .196569300s individual
vs .201880000s combined) and raises peak Python allocations by ~10.4 MB; it is
not retained. Lightweight ordered stage events avoid adding overlapping thread
durations: full-history read .901-.927s overlaps almost all of the first guard,
while the final complete guard consumes .549-.660s serially. Each traced save
still executes 24 Git commands and both complete full-byte guard hashes.
Receipt writes and new-exchange validation are small; no durability change is
justified. Untraced controls near 2.2s are diagnostics, not a replacement p95.

The content-hash pipeline design is rejected to retain the final guard's existing
all-metadata-before-content boundary. Parallel metadata preserves that boundary
but two/four-worker full-guard medians .446331050/.563382300s versus serial
.466594300s do not justify added concurrency. Neither candidate is retained.
All diagnostic process handles completed with exit 0. Scripts, raw data, exact
source and review reasoning are recorded in
tests/evaluations/windows-save-critical-path-20261022.md.

No runtime/test/harness/schema/spec/plan/checklist, machine setting, real novel,
provider, dependency, manuscript or saved release claim changes. The previously
verified full suites remain applicable; no repetitive broad rerun is performed.
T149's current packed Windows p95 1.587495700s read / 3.645534700s save still
passes read and misses save. It stays unchecked; novice evaluations remain
deferred/unverified and other missing human/host/language evidence remains open.


## T149 combined branch/OID queries — 2026-10-22

Retained a reviewed private helper that combines only the initial and
postpublication branch/OID pairs. The ordinary save uses 22 Git processes rather
than 24, with the same four hash-object/four ls-files/two cat-file calls.
All full-history, path/root/mode/live-index/byte-hash, candidate/private-index,
authority/hold, CAS, fsync and recovery safeguards remain. The fresh pre-CAS
branch check is unchanged; no atomic reference snapshot is claimed.

A real-Git same-OID branch-switch regression passes on the baseline.
Compatibility/fallback tests are red before the helper and green afterward;
all three new tests pass in 24.872s, including SHA-1/SHA-256 and malformed result
fallback. Independent diff review found no actionable safety defect. Eight
matched full-fixture saves (four/variant) lower median 2.762793500s to 2.336735950s
(15.4%), not p95 compliance. The difference between independent p95 series is
not attributed to this change.

Final-source Windows suite: 129 tests in 457.064s, 127 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 129 pass in
85.357s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 4.237690400s; read p95 5.106631200s; validation/local-save p95
3.612526000s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records unmet thresholds. No explicit Git packing/maintenance is requested.
This is the default fixture layout; prior packed/native-Git results describe
their own source and configuration, not this source. Linux performance has not
been remeasured for this source; historical Linux/earlier Windows data is kept.

Exact source, primary Git documentation, executed scripts, raw samples and
manifest evidence are recorded in tests/evaluations/windows-ref-query-20261022.md.
T149 remains unchecked. Novice evaluations stay deferred/unverified; remaining
host/human/language/release observations are not invented or waived. No spec,
plan, checklist, dependency, schema, machine setting or actual novel is changed.


### T149 history reconstruction and parallel hash candidates — 2026-10-22

External diagnostics against unchanged storage SHA-256 47c6eac0122d1076a91f21caeb253bf6721678f4e626fc0630ab069557e55304
reject a certified-history index rewrite: about 10ms absolute reconstruction
saving, excluding Git/JSON/full-save work. Four-worker final-guard hashing is a
promising candidate: four balanced complete saves per variant on the full
validated packed Windows/Git Bash fixture lower median 3.245158150s to
2.469268600s (23.9%); two workers measure 3.005366000s. All 12 saves succeed.
These are small diagnostic medians, not p95 compliance. All metadata precedes
hashing; every managed byte, root binding, result count and process status is
checked before OID comparison/publication. SHA-1/SHA-256 isolated candidate
checks pass; the initial insufficient-fixture runner failure is preserved.

No production change is retained from these experiments. Adoption still needs
production publication/error-path regressions, measured small-fixture/platform
policy and final-source full suites/30-run benchmarks. Exact scripts, samples,
source/evidence hashes and limitations are recorded in
tests/evaluations/windows-history-hash-candidates-20261022.md. Previous verified
129-test suites and ordinary-layout read/save p95 5.106631200s/3.612526000s
remain current. T149 stays unchecked; novice evaluations stay deferred/unverified.


### T149 parallel-hash production implementation — verification in progress

The measured candidate is now implemented in storage.py, SHA-256
6ec58b45314b7a99877220452367f6b89b532bed2fe3b3c842f0272a9aba1f5a.
Only final guards on Windows with >=1024 managed files use up to four complete
root-bound Git byte readers; initial guards, smaller saves and non-Windows
runtime remain serial. Every metadata/path/index check precedes hashing; all
process/count results precede OID comparisons, and workers join before lock
release. Worker-start failures become structured code-5 errors. Candidate,
CAS, full history, authority/holds and recovery safeguards are unchanged.

Five focused production regressions pass (54.214s). Linux full suite: all 133
pass in 75.471s, zero skips; source fingerprints remain unchanged. Read-only
review and follow-up report no actionable findings. The initial full Windows
run has one installation encoding error and two explicit symlink skips because
the runner omitted documented PYTHONUTF8=1. Isolated reproduction fails without
it and passes with it; all logs are preserved. The complete Windows suite and
30-run benchmark are being rerun with the corrected documented environment.
No new p95 compliance or completed Windows verification is claimed yet.

Evidence and limitations: tests/evaluations/windows-parallel-hash-20261022.md.
T149 remains unchecked; novice evaluations stay deferred/unverified.


### T149 retained parallel final-guard hashes — 2026-10-22

Final-source Windows suite: 133 tests in 571.309s, 131 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 133 pass in
75.471s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 5.184642400s; read p95 5.110137800s; validation/local-save p95
6.566394800s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records threshold status. No explicit Git packing/maintenance is requested.
This is the default fixture layout; earlier packed/native-Git results describe
their own source and configuration. Linux performance has not been remeasured
for this source; historical Linux/earlier Windows data is retained.

Large Windows final guards use up to four complete root-bound byte readers only
after all metadata/index/path checks succeed, at >=1024 managed files. First
guards, small saves and non-Windows runtime keep serial hashing. All worker
statuses/counts precede OID comparison; every worker joins before lock release.
Worker-start failures now return structured code-5 errors. Candidate/CAS,
authority/hold and recovery safeguards remain unchanged. Four new production
regressions and the existing ancestor-worktree/index-prefix regression cover
SHA-1/SHA-256 tampering, resource failures, error precedence, index/HEAD
preservation, pending receipts and successful unchanged retry. Independent review
found no actionable issues. Exact source, threshold samples, raw full-scale
measurements and manifests: tests/evaluations/windows-parallel-hash-20261022.md.
T149 stays unchecked. Novice evaluations remain deferred/unverified; other
host/human/language/release evidence is not invented or waived.


Matched final-source ordinary-layout Windows/PowerShell evidence subsequently
completes all eight saves: four per variant, balanced ABBA/ABBA, median
6.313554450s before versus 5.400350250s after (14.5% lower).
This supports retaining the full-byte optimization, not p95 compliance. Git
invocations are 22/25; full hashing remains, with bounded parallel readers.
The full-history batch remains substantial (1.994884450s median
invocation wall time). Detailed counter checks, limitations and raw traces are
recorded in tests/evaluations/windows-parallel-hash-20261022.md. T149 remains
unchecked; novice evaluations remain deferred/unverified.


### T149 partitioned history-read prototype — not retained

Source remains verified 6ec58b45... unchanged. External immutable-OID partitioning
reduces median full-history snapshot read 3.853349350s to 1.474333450s
(four samples/configuration), but complete-save ABBA/ABBA medians are
5.399026300s serial versus 5.505927300s with four requests.
No complete-save benefit is established. Review requires preserving earlier
malformed-history errors before later worker exceptions and preserving binary
framing across chunk boundaries. Production retains the original history reader.
Correction, fault regressions and further measurements remain necessary before
adoption; no fresh p95 claim is made. Raw samples, executed scripts, SHA-256
manifest and limitations: tests/evaluations/windows-parallel-history-candidate-20261022.md.
T149 remains unchecked; novice evaluations stay deferred/unverified.


### T149 corrected public history reader — full verification pending

The working source 9b909213... now uses up to four immutable-OID requests for
large public Windows reads (>=1024 exchanges). Ordered single-stream framing
and one complete serial fallback on any worker/submission/nonzero-exit failure
preserve error and prefix semantics. Saves keep serial history reads; all file
and publication safeguards remain intact. Five focused methods pass in 31.152s,
including SHA-1/SHA-256 boundary and failure regressions. Full suites and fresh
30-run p95 remain pending because C: repeatedly reached zero free bytes. Earlier
133-test and p95 results apply only to source 6ec58b45..., not this change.
Corrected small-sample diagnostics show a public-read gain but no save benefit;
they do not establish compliance. Source snapshots, scripts, results and hashes:
tests/evaluations/windows-history-partition-pending-20261022.md.
T149 stays unchecked. Novice evaluations remain deferred/unverified.


### T149 public history reads — full verification after disk cleanup

Windows: 138 tests in 704.102s, 136 passed and two explicit real-symlink
privilege skips, exit 0. Linux/WSL2: all 138 pass in 229.403s, zero skips,
exit 0. All five runtime/test/harness/helper fingerprints match before and after
both suites and the benchmark.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 2.486383800s; read p95 1.787683800s; validation/local-save p95
9.219870400s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read passes its 2s target; save misses its 1s target. Exit 1
records the unmet save threshold. No explicit Git packing/maintenance is requested.
Linux performance has not been remeasured for this source; earlier reference
results remain historical evidence.

Large public Windows reads (>=1,024 exchanges) fetch captured immutable blob
OIDs in at most four contiguous requests using the existing Git wrapper. Every
worker joins before parsing or returning. Successful outputs form one original-order
binary stream. Any worker/submission exception or nonzero child exit triggers one
full original serial request before parsing, preserving partial stdout, earlier
damaged-history errors and verified-prefix checkpoints. Small public reads and
non-Windows runtime stay serial. Save history remains serial: measured parallel
save variants provided no gain. All history/blob/schema/digest/authority/hold,
path/symlink/mode/live-index, both complete root-bound byte guards, private
candidate, fresh branch/CAS, receipt and recovery safeguards remain. The
previous parallel final-byte guard is unchanged.

Matched final-source read medians 5.125521150s serial / 2.825309150s four
workers (44.88% lower; four samples/policy) are diagnostic, not p95.
Source, complete logs, raw measurements, hardware and stage events:
tests/evaluations/windows-history-read-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified and other release gates remain open.


### T149 balanced save-reader experiment — integration tests required

Production remains verified 9b909213... unchanged. An external current-source
ABBA/ABBA fresh-worker diagnostic changes only history/first-guard workers1/1
to 2/2, retaining final four and every safeguard. All eight saves succeed with 25/27 Git
calls. Four-sample medians 5.669104200s/4.856166300s (14.34% lower),
with substantial variability, support further integration tests, not p95 or
release compliance. Independent review requires combined worker/fallback,
error-prefix, lock/join, redirection/tampering, retry and platform-policy
regressions before adoption. Source, samples and hashes:
tests/evaluations/windows-balanced-save-readers-20261022.md. T149 remains
unchecked; novice evaluations remain deferred/unverified.


### T149 balanced-reader integration — full verification pending

Storage 9bbcb0ac... selects bounded two/two Windows save-history/first-guard readers,
keeping four public/final readers and existing small-input/non-Windows serial policy.
All checks, original first-guard await/error/prefix order and worker/lock/candidate/
CAS/recovery stages remain. Five new combined regressions and existing framing/
final-guard cases pass: 8 methods in 85.046s, exit 0. Review found no actionable issue.
Fresh full 143-test suites are running; fresh 30-run ordinary Windows measurement
remains required. Preceding 138-test/p95 evidence belongs to 9b909213... only.
Tests, exact source, red/green results and pending manifest:
tests/evaluations/windows-balanced-save-pending-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified.


### T149 balanced save readers — full verification

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

Matched final-source medians: 3.509755100s control / 3.061612450s two/two,
four balanced samples per policy. This is diagnostic, not p95 compliance.
Source, full results, hardware, paired samples and stage traces:
tests/evaluations/windows-balanced-save-20261022.md. T149 remains unchecked;
novice evaluations remain deferred/unverified.


### T149 fresh native bundle-mode experiment — not adopted

Verified production 9bbcb0ac... remains unchanged. A strict-bundle-only fresh
GetFileAttributesW type query retains lstat for parents, non-bundles, special/
unknown/error attributes, with no metadata cache or skipped byte/index checks.
Review required NORMAL alone; a failing assertion and corrected 16-accepted/
21-fallback table are recorded. Eight complete fresh-worker saves all succeed
with 27 Git calls, counted native queries and six complete byte-hash partitions.
Four-sample medians 4.413188450s/3.816763250s (13.51% lower) are variable
diagnostics, not p95 compliance. Production-path compatibility/failure/tampering
regressions and fresh complete verification remain necessary before adoption.
Exact source, raw samples, review boundary and hashes:
tests/evaluations/windows-native-bundle-mode-20261022.md. T149 stays unchecked;
novice evaluations remain deferred/unverified.


### T149 native Windows bundle metadata: verification pending (2026-10-22)

T149, 2026-10-22. Fresh per-leaf GetFileAttributesW queries classify only ordinary
canonical bundle files. Normal attributes must stand alone; unusual, invalid,
missing or unavailable results fall back to the original lstat. Parents and all
non-bundle checks retain lstat. Full byte hashes, both complete guards, live index,
root binding, candidate verification, conditional publication and recovery remain.
Only the API callable is cached; file metadata is queried anew for every check.

Seven new tests cover API/fallback/type boundaries, Unicode and actual native
extended Windows paths, SHA-1/SHA-256 same-stat tampering, live-index changes,
pending receipts, exact retries and bootstrap/public-read boundaries. Initial
red: 7 tests, 125 missing-feature errors, 4.469s. Final focused verification:
9 tests, 25.960s, all pass, exit 0. Read-only review found no actionable production
issue. The full 150-test Windows/Linux suites and ordinary-layout 30-run Windows
benchmark are pending for this source. Prior 143-test evidence applies to the
balanced-reader source only. No performance gate or release approval is claimed.
Novice evaluations remain deferred and unverified.

Evidence: `tests/evaluations/windows-native-bundle-mode-production-pending-20261022.md`.


### T149 native Windows bundle metadata — full verification

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

See `tests/evaluations/windows-native-bundle-mode-production-20261022.md`. T149 remains unchecked; novice evaluations remain deferred/unverified.


### T149 full-history component profile and four-reader policy (verification pending)

2026-10-22: full-scale save profile attributes about 0.79-0.80s of 1.03-1.08s
history work to Git cat-file reads, 0.14-0.19s to JSON decoding, about 0.015s
to blob hash constructors and about 0.019s to certified index reconstruction.
Per-call tracing has overhead; threaded durations overlap. Eight matched fresh
complete saves on the verified native-metadata source, ABBA/ABBA with two/four
history readers, produce medians 2.544967200s/2.258775650s (11.25% lower).
All byte guards, native leaf queries, six hash partitions, and publication checks
remain. This is diagnostic evidence, not p95 or a portable speedup.

Runtime changes only the bounded large-Windows save-history policy from two to
four. Existing 1024 threshold, serial non-Windows/small histories, two initial
byte readers and four final byte readers remain. Regression policy and fallback
checks now exercise four children and preserve earlier damaged history, guard
error precedence, complete joins under the lock, exact retry and original state.
Default-policy red run fails 2 != 4 before the runtime edit. Focused/full suites
and a fresh required 30-run benchmark must verify this source. T149 remains open;
novice evaluations remain deferred/unverified.

Evidence: tests/evaluations/windows-history-components-20261022.jsonl and
tests/evaluations/windows-native-history-workers-20261022.txt.


### T149 four Windows save-history readers — full verification

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

See `tests/evaluations/windows-four-history-readers-20261022.md`. T149 remains unchecked; novice evaluations remain deferred/unverified.

### T150 independent distribution and UTF-8 continuation — 2026-10-22

The independent built-wheel check exposed legacy-encoding JSON output in the
installed CLI. The CLI now selects UTF-8 for stdout/stderr. A regression first
failed all four ASCII/Windows-1252 success/error cases; all 11 focused CLI and
portable-install tests pass after correction. The wheel verifier checks exact
source/resources, isolated module origins, console initialization, pinned novel
saves/reopens, recovery inspection and isolated legacy-stream Unicode errors on
Linux and Windows, reusing existing dependency packages without system changes.
Both Bash smoke checks pass using existing local jq binaries. Full-suite and
artifact details are recorded in tests/evaluations/independent-release-verification-20261022.md.

This is partial T150/FR-024 verification. T143–T150 remain unchecked: genuine
novice and product-host semantic evidence and the Windows save target are still
missing. No benchmark was rerun, target or safeguard lowered, checklist changed,
commit, push, provider call or publication performed. Existing dirty performance
work was preserved.

### T159 Windows junction boundary correction — 2026-10-23

Observed Windows directory junctions passed the existing lstat-mode-only boundary checks. A shared lstat helper now classifies reparse attributes as redirected paths; managed paths reject them with code 2 and redirected .git directories with code 3. The ordinary native-bundle fast path retains conservative fallback. No transaction, authority, full-byte guard, CAS, cache, receipt or recovery safeguard is removed.

The normal-access red run records six failures across three methods. Four final regression methods include actual story/.git junctions and junction insertion after candidate construction, with unchanged published history and retained pending payload. Read-only independent review found no actionable issue. Windows full suite: 155 tests in 503.662s, 153 pass and two explicit symlink-privilege skips. Linux/WSL full suite: 155 tests in 69.759s, 152 pass and three Windows-only junction skips; Linux real symlink tests pass. Both exits are 0. The offline updated wheel passes the independent verifier on both platforms, comparing 25 source/resource files and exercising pinned installation, Unicode output, save/reopen and recovery. Storage/regression hashes match their pre-suite fingerprints.

Evidence: tests/evaluations/windows-junction-boundary-20261023.md and its linked raw logs/manifest. Development guidance and current release/platform pointers are updated. Requirements checklist remains 16/16; no extension hooks are configured. T151-T158 remain incomplete: genuine novice and product-host semantic evaluations and the unmet Windows save-performance gate are not supplied by these structural checks. No performance benchmark, provider call, dependency change, commit, push or publication occurred. Prior uncommitted work is retained.

### T157 performance continuation and prepared host evaluation — 2026-10-23

The unchanged junction-corrected source completes a new full Windows packed/direct-Git benchmark: first read 1.667932500s; 30-read p95 0.824995800s (passes <=2s); 30-save p95 1.971346700s (unmet <=1s). All operations succeed with no timeouts/cleanup warnings; benchmark exit 1 records the missed target. Explicit disposable packing takes 5.228656900s separately. This process-local direct-Git configuration does not substitute for ordinary PowerShell/default-layout compliance.

A four-save stage profile identifies initial metadata/byte guards as the dominant remaining packed cost, alongside full history and Git transaction work. An ABBA/ABBA fresh-worker metadata GIL-policy comparison checks the same 10,000+ fresh native leaf queries and all six root-bound full-file hash partitions per save: ordinary medians 1.928849400s existing / 2.025946900s hold-GIL (5.03% slower); packed medians 1.837499050s / 1.634014500s (11.07% faster). The layout-dependent result is rejected; no production code or dependency changes are retained. These four-sample medians are diagnostic, not p95. Current CPU/RAM/NTFS details and exact source/raw evidence are in tests/evaluations/windows-performance-continuation-20261023.md. Existing T159 full-suite/wheel evidence remains applicable because production/test source is unchanged; no redundant full-suite rerun was performed.

A concrete, unexecuted plan for prepared English/Icelandic host cases, capture revalidation and fresh-task resumption is in tests/evaluations/product-host-run-plan-20261023.md. The app requires explicit user instructions to create and drive separate Codex tasks; no evaluation task was created or messaged. The plan preserves unavailable voice/native metadata limits and separates automated-host/agent judgments from genuine novice observations and human ratings. T151-T158 remain unchecked. No target, safeguard, checklist, real novel, machine setting, provider operation, commit, push or publication changed.

### T160 authorized delegated-input probes — 2026-10-23

The user explicitly approved creation and driving of the prepared four-task host evaluation plan. Two initial local projectless tasks were created with the default configured model: Novel host evaluation English (01a16833-e1cf-79d2-bee0-80a6ca973e3c) and Novel host evaluation Icelandic (01a16833-fa8e-7ec1-9c69-53dc7eaec197). Each received one follow-up capture probe. Native read_thread observations expose functionCallOutput codex_delegation for both create_thread and send_message_to_thread, with zero current userMessage items in all four probes. The delegated strings match their driver submissions exactly, but are not relabeled native user input. Both tasks correctly stopped without initializing a novel or saving a conversation. The two fresh-resumption tasks were gated and not created; no semantic, novice, human or bilingual outcome was collected. Direct typed-input spike evidence remains scoped and is not revoked or broadened.

Public observations, original task reports, authorization, exact driver inputs, workspace inventories and a reproducible independent boundary verifier are retained under tests/evaluations/product-host-runs/20261023T095949Z/. Reasoning items are excluded. The verifier checks snapshot consistency, not independent native-host provenance; that limitation is explicit. Unavailable model/package metadata is not invented. The existing unavailable-native-input rule is clarified in workflows/entry.md and the Codex fragment; development, current capture/release/platform and individual semantic-result documents point to the observed route limit. The plan status now records approval and the actual partial execution, rather than asking for permission again.

Fourteen installation/portable-install/initialization checks pass on Windows in 54.724s and Linux/WSL in 4.466s, zero skips/failures/errors, both exits 0. The updated offline wheel passes independent verification on both platforms, comparing 25 source/resource files plus isolated pinned installation, Unicode output, save/reopen and recovery. Wheel SHA-256: db8f9aa8def1b9338d337bbcc9fd65d46a718f05646233c90ee657d041fa035b. Runtime Python/schema code remains unchanged; the existing 155-test full-suite evidence is retained and full suites/performance were not redundantly rerun for text-only clarification. Independent read-only review found no actionable issue in the boundary evidence or clarification.

T151-T158 remain open. Actual supported native current-turn input is required to proceed with these host conversations; task-to-task messages cannot satisfy that adapter boundary. The existing tasks remain available for direct user interaction. No real novel, source/authority safeguard, dependency, machine setting, checklist, provider API, external message to a person, commit, push or publication was changed. The authorized task executions used normal Codex account execution. There are no extension hooks configured.

### T161 Git blob identity repair - 2026-10-23

Real SHA-1/SHA-256 loose-object corruption exposed two raw-identity gaps: candidate verification accepted a replacement blob with equivalent parsed JSON, and uncertified history reads accepted and could certify it while certified reads correctly rejected it. Canonical exchange payload validation cannot substitute for validating the raw Git blob ID. Candidate verification now checks that identity before parsing; history validation performs its existing raw hash check under every cache policy. No extra Git processes, filesystem reads, dependencies or authority sources were added.

The candidate regression failed four subcases before its fix. The history regression failed six uncertified-policy subcases before its fix; certified-policy cases already rejected corruption. Twelve focused tests pass on Windows (43.235s) and Linux (3.707s), including failure checkpoint/HEAD/index/proof preservation, retained pending work, restoration, and exactly-once retry. Independent read-only review found no actionable defects. A separate corrupt-tree diagnostic was already rejected by Git ls-tree on the tested versions and did not warrant another change.

The candidate-only intermediate full suites passed 157 tests: Windows 462.427s with two real-symlink privilege skips; Linux 47.344s with three Windows-only skips. Final history-fix source is separately pinned in tests/evaluations/git-blob-integrity-20261023.md. Final Linux passes 158 tests in 753.914s with three Windows-only skips; final Windows passes 158 tests in 32783.725s with two explicit real-symlink privilege skips. Both final suite exits are zero. The unusually long Windows elapsed interval is not product-performance evidence. The same offline wheel passes independent Windows/Linux source/resource comparison (25 files), isolated pinned installation, save/reopen, recovery and Unicode checks; SHA-256 a8be8f63cd77ef958e0e4307a686eae1f78c4360017a869ad6237efda22488e6. Earlier performance values are now explicitly historical; no final-source product benchmark or threshold compliance is claimed.

T151-T158 remain open. The separately prepared tests/evaluations/product-host-route-decision-20261023.md records the pending supported-input decision without changing the adapter contract or existing native/novice acceptance requirements. Existing dirty work was preserved; no commit, push, publication, real novel, machine setting or provider operation was performed.

### T162 explicit delegated evaluation support - 2026-10-23

The user selected explicitly labeled delegated input and retained native-input and novice requirements, authorizing continued independent work. The installed input capture command requires an explicit source, one current public turn, matching thread/turn IDs and one unambiguous input event. Delegation additionally requires the expected parent, supported codex_app create_thread/send_message_to_thread wrapper and evaluation-only opt-in. It preserves exact text and fails closed on missing, stale, truncated, malformed, ambiguous or mixed input. It never substitutes a preview, intended driver text or older human message. Delimiter collisions are explicitly unsupported.

The first installed test exposed the bootstrap-only input_artifacts rule. The narrowly added conversation exception validates exactly one host_input artifact by rebuilding selected public-event provenance and binding its exact text to the current message. It is not registered as a bootstrap creative source on full or certified paths; artifact IDs still participate in collision checks. No-artifact conversations and bootstrap artifacts retain their semantics; JSON schema fields are unchanged. A source artifact is evidence rather than independent host authentication, story identity or creative authority. Older installed bundles are not silently upgraded. Plan, adapter, workflow, data-model and CLI contracts record these boundaries.

Red evidence covers the absent module, three missing turn/truncation rejections and the original conversation-artifact rejection. Final 31-test authority/cache/installed-input regressions pass Windows 115.295s and Linux 59.933s. Full final suites pass 165 tests: Windows 1143.908s with two real-symlink privilege skips; Linux 97.115s with three Windows-only skips, both exits zero. Two independent read-only reviews found no actionable defect. The final offline wheel verifies on both platforms against all 26 source/resource files plus isolated pinned install, save/reopen, recovery and Unicode; SHA-256 d0bc73c599e9c84449202556a394a0d3ab9a6c2b5790c9241c63159d422289a0. Source-pinned manifest and reproducible verifier: tests/evaluations/delegated-input-support-manifest-20261023.json and verify-delegated-support-20261023.py.

The two existing authorized English/Icelandic tasks resumed. A metadata-only read setting in the driver caused the first Icelandic attempt to stop honestly; corrected public-output capture succeeded. Both actual delegated gates pass independent observed-input, committed-provenance, exact saved/displayed reply, save-before-display, installed-bundle and fresh CLI context/artifact checks. They do not satisfy native-input or human/novice criteria. Prepared guidance cases continue under tests/evaluations/product-host-runs/20261023T202447Z/ with actual public events and committed bundles retained, agent semantic judgments separate from persistence verification and human ratings. T163 and T151-T158 remain open. No real novel, manuscript, dependency, global setting, provider API, commit, push or publication changed; no extension hooks are configured.

The final-source ordinary Windows benchmark was then run with both host tasks
idle. Thirty reads complete with p95 3.453516100s, missing the two-second target.
Twenty-six saves complete; attempt 27 exceeds the unchanged 30-second worker
deadline and remaining attempts do not run. Save p95 is unavailable, not inferred
from partial samples. No benchmark worker remains after exit 1. Raw samples,
environment and source identity are recorded in
tests/evaluations/windows-delegated-provenance-performance-20261023.md. T157
remains open; differing historical configurations do not establish a causal
regression or current compliance.

### T163 additional delegated host evidence - 2026-10-23

All four previously authorized tasks have now run: the initial English/Icelandic
tasks plus two actual fresh resumption tasks. Two delegated capture gates and
32 subsequent case observations pass independent exact input, committed
provenance, saved/displayed response, Git checkpoint and save-before-display
checks. The cases include proposal setup and an unscored storm/shipwreck pilot
whose missing prerequisite is retained rather than scored as a parity result.
Selected agent judgments cover G01-G08, G11/G12, A01, seeded A11 partial selection,
quoted dialogue and intentional mistaken-belief resolution. Native input,
human participation or ratings are never inferred from these delegated events.

Fresh tasks read only committed installed context, without story answers or
earlier task transcripts. All 42 English and 35 Icelandic current records are
recovered; stable session IDs and guided mode survive. Each fresh summary is
saved before exact display, and no creative record changes. One session per
novel does not establish the required three-session capture matrix. The English
evidence file reserializes four timestamps through PowerShell, dropping trailing
fractional zeros. The initial strict failure is preserved; the verifier checks
equivalent instants for those fields and requires every other value to match.
The Icelandic context matches the independent baseline exactly. Raw evidence is
not rewritten to obtain a pass.

Capture differences remain visible: English separately records some preference
questions that Icelandic retains only in saved messages. English and Icelandic
classify the sender finding differently (uncertainty/conflict); both interrupt
development and later retain a sourced intentional resolution without changing
the actual sender. The Icelandic fresh visible summary names session/checkpoint
without enumerating record revisions, so full derived-summary citation compliance
is not claimed. No complete semantic matrix, fluent human review, interrupted-
before-display observation, voice result, unchanged-manuscript-content test or
exhaustive extraction parity is inferred from this subset.

Evidence, committed envelopes, observed public events without reasoning, scoped
agent judgments, baselines and reproducible verifiers are retained under
tests/evaluations/product-host-runs/20261023T202447Z/. verify_complete.py requires
every submitted case/language pair and fingerprints the result. Runtime and
packaged resource source remains the final T162 wheel; source-specific 165-test
suites and both independent wheel checks still apply. T163 is complete only for
additional delegated evidence; T151-T158 retain all native/human/performance and
release requirements. No framework commit, push or publication was performed.

### T164-T167 single-user POC delivery - 2026-10-23

The owner explicitly removed novice testers from scope and requested a working
POC without manual testing; personal testing follows delivery. Spec SC-001 and
SC-007 now use automated criteria, and plan/tasks/onboarding distinguish POC
readiness from broader release/scale qualification. Historical unchecked human
worksheets remain as unexecuted evidence, not a request for participants or a
POC prerequisite. All creative-authority, input-source, exact persistence,
hash/path/lock/publication and manuscript-protection boundaries are retained.

Two observed workflow gaps were addressed without runtime/schema changes:
brainstorming audits each new open question, including preference/evaluation
prompts, and resumption visibly cites supporting record IDs/revisions plus a
checkpoint. Initialization and brainstorming reference the explicitly selected
entry input source. Existing installed novels retain their pinned bundles.
The earlier Icelandic omitted-question case fails the new baseline check; its
messages and failed evidence remain intact rather than being retroactively fixed.

The two already authorized fresh evaluation tasks each create a new disposable
POC novel. Eight actual delegated observations pass independent observed-input,
committed provenance, exact response save/display and ordering checks. Both new
question types have source-backed records/session links; unanswered preference
questions survive the topic switch. Summaries preserve proposed status, cite
correct question/idea revisions and checkpoint, and pause without new exploration.
Current installed source/resource bytes and manifest checksums are verified.
Agent semantic judgments are recorded separately; no human/native outcome is
inferred. Read-only independent review found no actionable issue.

Fourteen affected installed/integration checks pass Windows 287.003s and Linux
15.825s with no failures, errors or skips. All runtime Python hashes match the
prior 165-test full-suite source; that evidence is retained without calling it
a freshly rerun full suite. The new offline wheel independently verifies on
both platforms against 26 source/resource files plus isolated install, pinned
save/reopen/recovery and Unicode. SHA-256:
8e3ec2e7c895bd16359a916a8f614b56830ea53f80e7396e367dfdb73a4f1a64.

A ten-session/100-exchange/200-assertion/1,048,668-byte synthetic small-history
run completes all 30 reads and saves without errors or timeouts. Cold read is
0.715602800s; read p95 0.579379300s; save p95 1.983323900s still misses 1s.
There is no remaining benchmark worker. This does not replace the larger
fixture's recorded read miss/save timeout or qualify full-scale performance.
No machine setting, dependency or safeguard was changed. Functional POC
readiness and these limits are reconciled in tests/evaluations/poc-readiness-
20261023.md and its reproducible source/artifact manifest. The current wheel
and docs/poc-quickstart.md are ready for owner use. No real novel, manual test,
framework commit, push, publication or provider API operation was performed.


### T168 automated capture/resumption and display boundary - 2026-10-23

T168 is complete for its explicitly labeled delegated automated scope. Three
sessions preserve all twenty designated proposition groups, ten director
selections and five open questions per language. Actual fresh chats recover
exact independent 86/90-record baselines without story answers or earlier
transcripts, save sourced summaries and change no creative records. Correction
history, unresolved alternatives and every capture kind are retained. Twelve
current observations pass exact public input, committed source labels, final
response, save ordering, current bundle and separately reviewed commentary.

Original paired CAPTURE3 runs disclosed creative conclusions in commentary
before save, despite matching final replies. Their failures remain untouched.
workflows/entry.md now explicitly covers progress commentary and exact whitespace;
paired freshly installed regressions pass the original scenario. No runtime,
schema, dependency, authority, storage or existing-novel bundle change occurred.
The first Icelandic fresh attempt stopped on reported public-tool unavailability;
supported discovery on a new actual turn succeeded, with both attempts retained.

Twenty-two affected checks pass on Windows/Linux; the current offline wheel
independently verifies against 26 files on both. SHA-256 is
003c938689ca6121488884fe3d0a2e53bd9a04a06688cc7d3c3abed798898514.
See tests/evaluations/display-boundary-20261023.md and phase22-runs/20261023T231406Z/
for raw evidence and reproducible verifiers. No human/native result or arbitrary
semantic guarantee is inferred. Only T168 is checked; T169-T173 remain open.


### T169 interrupted public-host verification - 2026-10-27

Public app coordination stopped returning usable observations: wait_threads
reported a 3600s tool-call timeout, and subsequent read_thread requests remained
unresolved. Those read-only orchestration waits were terminated. T169 remains
unverified; no unknown-outcome scenario was resent and T170-T173 were not advanced.

Read-only Git inspection confirms English AUTH_PARTIAL at sequence 8. Icelandic
HEAD remains the independently recorded fresh-resumption checkpoint at sequence 7;
its AUTH_PARTIAL receipt is pending and uncommitted. The child's mojibake/unknown-
checkpoint report is preserved, but current files match the driver exactly and
sequence 7 is the known authorized fresh resumption. No repair/retry or source-
authenticity claim is inferred without supported public observations.

Current installed-source fingerprints and wheel hash still match the verified
artifact. T168 re-verifies at its immutable observed checkpoints, and all seven
current verifier tests pass. Only T168 is checked. Full evidence, stopped-call
limitations and exact continuation details: tests/evaluations/phase22-status-
20261027.md. No commit/push/provider/global-setting or real-novel action occurred.

## Phase 22 continuation — 2026-10-28

Completed T169–T171 with actual authorized English/Icelandic delegated observations, exact public source/save/display checks, unchanged pending recovery and separate app-continuation verification. Retained all earlier work/failures. Added evidence collection for distinct original-input and completed-display turns, protected by nine passing regressions on each of Windows/Linux. Product runtime/resources, wheel and dependencies are unchanged. Full-scale ordinary Windows qualification completes 30 reads/30 saves without errors/timeouts; read p95 1.028736700s passes and save p95 3.067419500s misses <=1s. Focused stage diagnostics retain every guard and justify no additional runtime change. T172 and dependent T173 remain unchecked; T173's provisional assessment maps all stories/SCs, onboarding, source/platform identity and explicit unknowns. Corrected stale novice/manual requirements in current guides to match the owner's Phase 21 scope. Evidence: tests/evaluations/phase22-resumption-20261028.md and phase22-release-assessment-20261028.md.

### T172 safe-save investigation — 2026-10-28

Recorded profiling motivates reduced-concurrency and history-first scheduling
experiments, executed without production edits. Twenty fresh-worker complete
saves on fully validated ordinary-layout 100-session/5,000-exchange/10,000-
assertion/26,215,716-byte fixtures all succeed, retaining both complete guards
and counted object/byte reads. Current-policy/reduced-history/reduced-first-hash
medians are 3.052792150/4.330007750/3.224343650s; a separate overlap/history-first
comparison measures 3.087430600/3.309358300s. All alternatives are rejected.
No runtime, resource, dependency or benchmark edit is retained. Source hashes
and independent 30-run p95 arithmetic reverify; the unchanged save target is
still missed. T172 and dependent T173 stay open, with the existing provisional
release assessment preserved. Original sandbox temporary-key denial is recorded
separately from successful scoped normal-access runs. Full evidence and verifier:
tests/evaluations/windows-phase22-save-investigation-20261028.md.

### T172 tree-construction diagnosis — 2026-10-28

Investigated the next distinct measured bottleneck, private-candidate
`write-tree`, without repeating earlier reader/schedule/guard experiments.
Eight full-scale ordinary-layout fresh-worker saves compare a command-local
fscache option in ABBA/ABBA order, all successful with both complete guards and
counted object/hash reads. No improvement is demonstrated; activation tracing
then proves this command does not enable that cache, with `status` as a working
positive control. Traced medians are diagnostic and not causal regression or
p95 evidence. Tree-update work accounts for 0.219981000/0.267330000s median;
the trace does not isolate its individual object lookup/write costs. Four
SHA-1/SHA-256 cases preserve missing-object rejection. No runtime, resource,
dependency or benchmark edit is retained. Reproducible verification confirms
source identity, sample arithmetic and traces. T172/T173 stay open; unchanged
30-run save p95 still misses <=1s. Evidence and next constraints:
tests/evaluations/windows-phase22-write-tree-20261028.md.

### T172 autonomous component/prototype continuation — 2026-10-28

Four full guarded saves and eight identical private-index tree replays separate
fresh/existing object writes while retaining referenced-object checks. Independent
native type/access, verified tree-byte hash/compression and scratch-fsync probes
are recorded without adding/subtracting them into fictitious native phase costs.
Fresh/existing native update medians overlap at 0.322688500/0.339142500s. A load
sample records 100% CPU and about 2.8 GiB free physical memory; no machine setting
or unrelated process changes. Another distinct lexical parent-prefix prototype
completes eight full-scale fresh-worker saves, preserving full guard/hash/history
and fresh leaf counts, with current/prototype medians 7.865432450/12.297503250s.
It demonstrates no gain and is not retained; no causal slowdown is claimed under
the variable conditions. All diagnostics/verifiers exit 0 and source identities
match. No production, resource, dependency or harness edit invalidates platform/
wheel evidence. T172/T173 stay open and the previous 30-run result remains the
qualification result. Evidence: windows-phase22-tree-components-20261028.md and
windows-phase22-parent-prefix-20261028.md under tests/evaluations/.

### T172 isolated native build and direct timers — 2026-10-28

Pinned Git for Windows v2.53.0.windows.3 to commit
f8165afd89b0c190677a093f20894f5fce12f97a and built unmodified/instrumented
MSVC controls in ignored .tools/t172-git-native-20261028/. Portable CMake is
publisher-checksum verified; zlib is isolated/static. Existing compiler/SDK,
installed Git, global settings and product dependencies are unchanged. Preserved
the failed first configure and successful corrected/instrumented build logs.

Eight format/variant cases match Unicode tree OIDs and reject missing objects.
Sixteen full-scale guarded fresh-worker saves pass with exact original guard/hash
counts. Four owner-thread native profiles directly time lookup, buffer assembly,
object writing, compression and flushes with inclusive/exclusive accounting and
errno/return-value preservation. Source/build/compiler/load limitations remain
explicit. The initial quiet gate passes but all native profile windows exceed
the CPU criterion; a stricter follow-up refuses new measurement at preflight.
Independent verification confirms source/binary hashes, arithmetic, nesting and
the explicit non-measurement. No production change or new qualification p95;
T172 and dependent T173 remain open. Full evidence and replay tools:
tests/evaluations/windows-phase22-native-profile-20261028.md.


## Phase 23 T174 stderr-pipe investigation — 2026-10-28

A source-free prototype redirects only discarded checked-Git stderr, preserving
unchecked diagnostics, stdout/stdin, sanitized errors and all save safeguards.
Actual Git correctness checks pass in SHA-1/SHA-256. Component ABBA batches reduce
reader threads from 16 to zero and median eight-command time from 0.602102700 to
0.538249500s, but the eight full-scale fresh-worker saves have effectively equal
current/prototype medians 6.261266500/6.255118250s under high variable CPU load.
All successful saves retain exact guard/hash/object counts. Original sandbox
WinError 5 and the corrected diagnostic reader-thread assumption are preserved.
No prototype/runtime/resource/dependency/benchmark change is retained. Independent
verification exits 0; qualification stays at read p95 1.028736700s and save p95
3.067419500s, with save <=1s unmet. T174/T175 and T172/T173 remain unchecked.
Existing source-specific wheel/platform/story evidence is unchanged; no fresh
broad suite or host evaluation is claimed. Full sources, samples and verifier:
tests/evaluations/windows-phase23-stderr-pipe-20261028.md.


### Final functional qualification — complete, 2026-10-28

The owner withdrew all read/save latency targets and deferred optimization.
T172/T174 are explicitly retired requirements, not measured target passes;
T173/T175 are complete for the current single-user functional scope. Earlier
unchecked tasks retain historical native/human/scope evidence and do not reopen
retired timing or novice/manual prerequisites. No active POC delivery work remains.

Fresh corrected suites: Windows 178 total, 176 passed and two explicit real-
symlink privilege skips; Linux/WSL 178 total, 175 passed and three Windows-junction
skips. Both exit 0. The four policy regressions verify informational slow reads/
saves while keeping errors/timeouts failing. The same offline wheel independently
passes Windows/Linux source/resource identity and installed initialization/save/
reopen checks. Spec Kit Bash smoke passes with the existing cached jq. Initial
sandbox/temp-location/tool-PATH failures remain visible, separately from passing
final runs. No product runtime/resource/dependency or safeguard changes, new
performance qualification claim, provider call, real-novel edit, commit or push.

Current report: tests/evaluations/final-functional-qualification-20261028.md.
Source and evidence manifest: tests/evaluations/final-functional-manifest-20261028.json.
Start here: docs/poc-quickstart.md. All six stories and SC-001-SC-009 retain
source-specific structural and labeled delegated coverage; subjective literary
quality, broader native-host combinations and physical power-loss durability
remain unmeasured. macOS, additional hosts, dashboard and drafting remain deferred.
