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
