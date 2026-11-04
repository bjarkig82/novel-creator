# Agent story notebook evidence

This ledger distinguishes setup and packaging checks from actual writing behavior.
The notebook is a development candidate for new novels; existing novels remain on
the legacy route.

Evaluation context: November 4, 2026; Linux managed development checkout, Python
3.12, uncommitted candidate based on package version 0.3.0. No release or
publication is implied. Package checks install generated wheel/source artifacts
into disposable environments; they do not use the editable product as the
installed implementation. Windows structural execution remains unverified here.

## Structural evidence

On Linux, targeted notebook setup and CLI tests, legacy initialization tests, and
notebook contract fixture checks passed. A candidate wheel was built and the
expanded wheel verifier passed, including notebook resource byte comparisons and installed setup.
An offline integration test built and installed both wheel and source distribution
into isolated disposable environments outside the checkout. Both installed
artifacts created English and Icelandic notebooks with Unicode and spaces in paths;
the checks covered guidance references, an initial Git commit, and absence of a
legacy Python runtime in the notebook. These are structural checks, not evidence
of conversational behavior.

Before the convergence localization fix, earlier full-suite attempts overlapped dependency installation or final export-inventory
source corrections and were superseded. After all production changes were fixed and
the environment stayed stable, `python -m unittest discover` passed: 398 tests run,
three skipped. The final focused notebook checks also passed (25 tests), and the
rebuilt candidate wheel passed the expanded verifier, including legacy export checks.
Spec Kit Bash smoke checks passed. Independent task reviews and the final overall
review identified no remaining material concern after their corrections.

Spec Kit Bash smoke checks passed. The clean package verifier's candidate versus
historical-public-release policy has focused regression coverage, including full
console version strings; candidate failures cannot silently skip notebook checks.

## Acceptance coverage

| Outcome | Structural evidence | Native host evidence |
| --- | --- | --- |
| SC-001: automatic meaningful notes | Valid capture/state examples and invalid fixture mutations | Unverified automatic maintenance |
| SC-002: focused fresh-session brief | Linked authoritative topic and summary fixtures | Unverified brief and recall |
| SC-003: no unsolicited recap | Workflow explicitly specifies requested recaps only | Unverified session-opening behavior |
| SC-004: accepted versus tentative | States, question types and origins checked in bilingual fixtures | Unverified interpretation of writer commitments |
| SC-005: revisions and continuity | Linked impact, beliefs and historical-value fixtures | Unverified conflict detection and revision behavior |
| SC-006: preservation and honest failures | Setup refusal, staged-work preservation, competing creation and partial failure tests pass | Writing-time external edits, failed writes and checkpoint handling unverified |
| SC-007: no formal session closure | Notes/summary representation supports persistent context | Unverified interruption and resumption |
| SC-008: writing without legacy runtime | Installed notebook has no Python runtime, exchange archive or legacy resources | Actual conversation without legacy calls unverified |
| SC-009: refuse existing novels | Existing targets remain unchanged in setup tests | No native host judgment needed for deterministic setup |

These structural results do not establish the unverified semantic outcomes.

## Convergence localization and qualification

T027 is complete: initial project and working-summary documents now use only the
configured English or Icelandic prose/headings, while retaining stable metadata
and author-supplied Unicode titles. New setup and installed wheel/source-distribution
checks failed against the former bilingual seeds and passed after localization.
Focused verification passed (27 tests), and independent task and overall reviews
found no material issues.

After all localization edits, the fresh full suite passed: 399 tests run, three
skipped. The rebuilt wheel passed source-byte and installed-notebook verification
in both languages, including legacy export checks. These results remain Linux
structural evidence, not native Desktop conversation evidence.

T028 remains blocked: this Linux execution environment exposes no Windows host,
native Codex Desktop, SSH or Codex thread-control tools. Windows structural checks
and actual Desktop journeys were not performed. Earlier native-host tasks remain
unchecked; no fixture or package test is counted as a substitute.

## Native host and literary evidence

**Unverified:** Windows and Linux Codex Desktop conversations, including native
input, automatic note maintenance, fresh-session recall, revision, preservation of
external edits, write failures, and English/Icelandic behavior. The environment
used for these checks did not provide native Codex Desktop or thread tools. The
acceptance journeys in the feature quickstart still need actual host evaluation.
Subjective literary quality has not been assessed.
