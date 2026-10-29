# Functional POC — ready to use (2026-10-28)

## Owner-approved delivery scope

The owner withdrew all time-related performance targets on 2026-10-28 and
requested a working single-user POC before further optimization. Neither read
nor save latency blocks this delivery. Timings remain informational; historical
misses retain their original results and are not retroactively called passes.
The benchmark now reports `target_seconds: null` and `passes: null` for both
operations; its exit status requires all requested operations to complete.
Errors, incomplete samples and operational timeouts remain failures. The timeout
is a test execution bound, not a responsiveness promise.

The POC covers initialization, guided/open brainstorming, automatic sourced
capture, acceptance/revision, continuity, inspection, resumption and recovery,
in English and Icelandic. Native and delegated evidence stay distinct. Every
authority, persistence, integrity, path/index, lock, manuscript and recovery
safeguard remains active. No runtime optimization or storage change is included.
Novice/manual testing remains excluded as a delivery prerequisite by Phase 21;
owner use and subjective literary assessment follow delivery.

## Functional coverage

| Story / criteria | Evidence |
|---|---|
| 1: setup, unknowns, preserved preferences; SC-001/002 | Fresh Windows/Linux installed-wheel initialization/reopen checks and existing initialization journeys |
| 2: guidance, mode/topic changes; SC-007 | T168/T171 actual delegated replies plus current structural guidance/session tests |
| 3: automatic capture, correction, fresh resumption; SC-003/009 | T168 complete three-session matrix, sourced correction and fresh chats; current persistence/recovery tests |
| 4: acceptance, non-acceptance, revisions/checkpoints; SC-004/006 | T169 paired acceptance/non-acceptance matrix, five revisions per language, protected-direction and checkpoint cases; current authority tests |
| 5: continuity, dispositions, holds and perspectives; SC-005/009 | T170 six categories, intentional viewpoints and all dispositions; current fault/hold tests |
| 6: language and independent consumption; SC-002/008 | T171 paired language-pitfall observations; current independent-consumer, language and pinned-bundle tests |

The source-specific six-story/SC mapping and its native/human/subjective limits
are retained in [the Phase 22 assessment](phase22-release-assessment-20261028.md).
These existing agent observations were not replayed in this closeout; they
remain valid for their unchanged runtime/resources and explicitly limited scope.

The active functional delivery scope is complete. T172/T174 are closed as
withdrawn optimization requirements; T173/T175 are complete under this scope.
Earlier unchecked native/human/latency entries remain historical and are not
active POC prerequisites. No original failed performance target is called passed.

## Final verification

| Check | Result | Evidence |
|---|---|---|
| Windows full suite | 176 passed, 2 real-symlink privilege skips; 178 total, exit 0 | [Corrected external-temp run](windows-final-functional-corrected-20261028.txt) |
| Linux/WSL full suite | 175 passed, 3 Windows-only junction skips; 178 total, exit 0 | [Full log](linux-final-functional-tests-20261028.txt) |
| Windows offline wheel | Source identity and two installed init/save/reopen cases pass; exit 0 | [Report](windows-final-wheel-external-20261028.json) |
| Linux offline wheel | Same source identity and installed cases pass; exit 0 | [Report](linux-final-wheel-20261028.json) |
| Spec Kit Bash smoke | Pass, exit 0 | [Corrected cached-jq run](linux-final-speckit-smoke-corrected-20261028.txt) |

The two Windows real-symlink tests skip because privilege 1314 is unavailable;
those real-symlink cases pass on Linux. Linux skips the three Windows-specific
junction regressions, which pass on Windows.

Both full-suite invocations include the new benchmark-policy regressions: slow
successful reads/saves have informational timings and no latency verdict; save
timeouts and operation errors still fail. The retained wheel reports each verify
26 source/resource files and a 27-file installed bundle, with product modules
loaded from the isolated installed environment. No new benchmark run or
optimization is required to qualify this unchanged product runtime.

The first Windows suite and wheel attempt placed temporary novel fixtures under
the framework checkout. Initialization correctly refused nested novel roots;
the suite was stopped and restarted with external system-temp fixtures. The
original outputs remain visible. The first Linux smoke attempt lacked jq on
PATH; the corrected invocation uses the already cached executable on that
process's PATH, without installing tools or changing global configuration.
The initial policy-test sandbox failure and both deliberate red regressions
are also retained separately. None is relabeled a successful final run.

## Distribution and limitations

Use [the POC quickstart](../../docs/poc-quickstart.md). The retained offline wheel
is [novel_creator-0.1.0-py3-none-any.whl](../../dist/phase22-20261023/novel_creator-0.1.0-py3-none-any.whl),
SHA-256 `003c938689ca6121488884fe3d0a2e53bd9a04a06688cc7d3c3abed798898514`.
Only the development benchmark policy, its regression tests and delivery
documents change; product/runtime/resource bytes remain matched to this wheel.
No rebuild is needed for a documentation and benchmark-policy change.

No universal host/model/filesystem, physical power-loss durability, subjective
literary quality or human approval is claimed. macOS, additional host adapters,
dashboard and manuscript drafting/editing remain deferred. Normal scoped Windows
filesystem access is needed when sandbox restrictions deny hard-link publication.
No real novel, global configuration, provider, framework commit, push or external
publication is changed by this qualification.
