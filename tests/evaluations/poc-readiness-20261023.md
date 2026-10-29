# Single-user POC - ready for owner use

The owner explicitly excludes novice testers and will personally test after
receiving a working POC. Manual/native-host sessions and human ratings are not
delivery prerequisites. This scope supersedes older novice/manual release gates
for this POC; it does not invent successful human observations.

Current scope: initialization/settings, guided/open brainstorming, source-backed
capture, canon decisions/revisions, continuity findings/holds, inspection,
resumption and recovery in independent Git novels using the Codex adapter.
Native input and explicitly authorized delegated evaluation input remain labeled
separately. All authority, exact-input, save-before-display, transaction, hashing,
path, lock and manuscript-protection safeguards remain active.

The observed missing preference-question records and incomplete visible summary
revision citations prompted a narrow workflow update. Questions now receive an
explicit pre-save capture audit, including preference prompts; resumption
requires record IDs/revisions alongside the checkpoint in the visible summary.
Runtime/schema/storage code is unchanged. Current verification follows below;
historical source-specific evidence is never presented as a fresh full-suite run.

## Distribution and automated checks

Current wheel: [novel_creator-0.1.0-py3-none-any.whl](../../dist/poc-20261023/novel_creator-0.1.0-py3-none-any.whl).
SHA-256: 8e3ec2e7c895bd16359a916a8f614b56830ea53f80e7396e367dfdb73a4f1a64.
Both Windows/Linux independent wheel verifiers pass, comparing 26 source/resource
files and exercising isolated product origins, initialization, pinned saves,
reopening, recovery and Unicode. No dependency was downloaded or changed.

Fourteen affected installed/integration tests pass on each platform: Windows
287.003s, Linux/WSL 15.825s, no skips/failures/errors. These cover install,
portable modules, no-concept/combined settings initialization, guidance session
transitions, the three-session 20-idea/10-decision/5-question structural journey
and installed native/delegated capture. Raw outputs are windows-poc-workflows-
20261023.txt and linux-poc-workflows-20261023.txt; wheel reports use the matching
windows/linux-poc-wheel-20261023.json names.

All runtime Python source hashes still match the prior 165-test full-suite
manifest. That runtime evidence is retained: Windows 163 pass/two symlink-privilege
skips; Linux 162 pass/three Windows-only skips. It is not a newly run full suite
for the POC workflow changes. The affected checks and wheel verifiers above are
fresh. Read-only independent review found no actionable scope/workflow/onboarding
issue; it did not self-award the still-running live regressions.

Eight current installed-host observations pass exact public input, committed
source labels, saved/displayed response, checkpoint and save-before-display
checks across both languages. Both updated installed bundles match current
source/resources. QUESTION and PROPOSAL save source-backed question records and
retain earlier unanswered questions. RESUME includes the idea, both questions,
correct record revisions and checkpoint citations, and pauses without new
exploration. See [the actual run](poc-runs/20261023T223255Z/README.md) and its
separate scoped agent judgments. The old Icelandic missing-question case is
retained with an explicit failing baseline assertion; it is not rewritten.

No real novel, novice session or manual user test is created as part of
verification. Manual testing is for the owner's later use, not a missing POC gate.

## Measured responsiveness and known limits

A fully validated synthetic small-history fixture has ten sessions, 100 exchanges,
200 active assertions and 1,048,668 JSON bytes. All 30 reads and 30 saves complete
without errors or timeouts. First read: 0.715602800s; warm read p95: 0.579379300s;
warm save p95: 1.983323900s. The two-second read target passes for this fixture;
the one-second save target is still unmet. There is no latency waiver or claim
that the larger release-scale target now passes.

Windows 11 build 26300, Python 3.13.13, Git 2.53.0.windows.3 and eight logical CPUs
are recorded in windows-poc-small-30-20261023.json. The standard harness uses its
temporary private validation-cache key, no explicit Git packing, bounded workers
and the unchanged storage safeguards. Host/model latency is excluded. All test
jobs and delegated tasks were idle during measurement. Progress and raw samples
are retained; no benchmark worker remains after completion.

The larger 5,000-exchange/10,000-assertion Windows fixture remains unqualified:
read p95 3.453516100s and a timeout on save attempt 27, with no valid save p95.
The smaller run is POC responsiveness evidence, not a substitute for that scale
qualification. No storage optimization, machine setting, dependency or safeguard
was changed to obtain it.

Use single typed-text inputs through the supported Codex route. Delegated input
remains evaluation-only. Subjective coaching quality, complete literary parity,
arbitrary extraction completeness, voice fidelity and unsupported filesystems
are not guaranteed. macOS and broader host adapters remain outside this build.
The delivered slice covers setup/story planning and records; chapter drafting,
editing and dashboard delivery remain future slices in the feature scope.

## Readiness conclusion

The local single-user POC is ready to use with the
[starting instructions](../../docs/poc-quickstart.md). Its working loop is
initialize/settings -> brainstorm -> source-backed save -> inspect/resume,
with canon/revision/continuity and failure-recovery safeguards. The verified
wheel is linked above. verify-poc-20261023.py reconciles all eight current host
observations, both 14-test runs, both wheel checks, unchanged full-suite runtime
hashes and completed small-fixture samples into poc-manifest-20261023.json.

This is functional POC readiness with the listed limits, not full release-scale
or subjective literary qualification. No human test, novice rating or native-user
outcome is inferred from automated/delegated checks, and none is requested as a
prerequisite to deliver this POC.

## Functional coverage of the POC

| Capability | Automated evidence | Scope of the conclusion |
| --- | --- | --- |
| No-concept setup and settings | Current initialization journey, pinned installation and wheel checks | Unknowns and supplied bilingual values survive reopening; optional brainstorming is exposed. |
| Guided/open collaboration | Installed guidance journey and earlier labeled G01-G08/G11/G12 observations | Mode/topic/preferences persist; selected actual replies were assessed by agents. Usefulness is for later owner use. |
| Capture and resumption | Three-session structural 20/10/5 journey, prior actual fresh tasks, current question/summary regressions | Record recovery is verified; subjective completeness across arbitrary conversations is not guaranteed. |
| Canon and revisions | Authority unit tests and real-Git canon journey, selected earlier A01/A11/quoted-dialogue observations | Explicit decisions, partial selection, revision history, source guards and manuscript boundaries remain enforced. |
| Continuity and failure recovery | Continuity/recovery/fault/overlap checks, selected earlier sourced intentional-resolution observations | Holds and failure preservation are checked; literary conflict detection remains agent judgment. |
| Independent bilingual data | Current two-platform wheel, Unicode and consumer/source checks | Product modules run from pinned novels; full English/Icelandic literary parity and macOS are not claimed. |

Earlier actual-host observations are retained under
product-host-runs/20261023T202447Z/ with their original source/version limits.
No completed structural journey is relabeled a real human trial or a complete
automatic semantic evaluation. Core creative-authority and transaction safeguards
remain delivery requirements; the scope change concerns manual/novice qualification.
