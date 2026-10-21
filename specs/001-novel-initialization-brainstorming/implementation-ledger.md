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

## Integration for local Desktop testing — 2026-10-21

User explicitly requested committing and pushing these changes to main.
Fetched origin/main; it matches the current base 12fa90b. Fresh pre-push
verification: all 52 automated tests pass, Bash smoke checks pass and
git diff --check is clean. Guide links and recorded JSON evidence validate.
The guide now directs local users to pull main before testing. Include the
foundation fixes, regression tests, convergence tasks, manual Desktop guide and
partial live host evidence. Actual-host gate remains BLOCKED; no product-story
completion or supported-host claim is introduced by integration.
