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
