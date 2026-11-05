# Notebook Brainstorming Implementation Plan

**Goal:** Guide an empty book toward an idea while respecting explicit topic and method choices.

**Architecture:** Shared Markdown conversation/method guidance; five thin notebook
Codex skills; explicit initializer resource list. Existing package-data globs
already cover these files. No runtime conversation engine or legacy changes.

**Spec:** [Approved design](../specs/2026-11-05-brainstorming-design.md).

**Constraints:** Preserve writer authority, en/is, stable notes, existing books,
legacy bundle isolation and explicit-only outline invocation. No version bump
or package publication. Coordinator handles independent reviews; implement
inline here without further delegation, as explicitly instructed.

## Tasks

- [x] Read notebook resources, initializer, packaging and tests. Record the reported
  empty-book character/topic-first failure; add real installation/link/commit and
  legacy-exclusion tests and observe missing-resource failures in en/is.
- [x] Add shared stage routing and concrete conversational methods, then thin
  book-idea/premise/character/plot/setting skills and explicit initialization.
- [x] Update onboarding, functionality, candidate notes and manual scenarios.
- [x] Run initializer/legacy/package checks, full suite, wheel verifier and link/
  diff review. Record structural results separately from unrun host/quality checks.

## Review focus

Empty and sparse books; explicit character-first requests; method-first starts;
known answers and topic switches; provisional choices and open questions. Manual
conversation scenarios cover these judgment cases; installation tests verify
resources, portable links, language-specific seeds and legacy exclusion.

## Review results

Independent requirement review identified a missing explicit default method
selection rule. Added contextual technique selection and adaptation while keeping
explicit method choice priority. Scoped re-review and overall independent review
reported no remaining actionable findings. Read-only simulated opening/method-first/
character-first reasoning checks were consistent; these are not native host runs.
After implementation and validation, the user authorized committing and pushing
this feature to main. Package publication remains outside the requested scope.

## Final validation

- New installation regression observed failing in en/is before implementation;
  built wheel and sdist regression observed failing for missing book-idea skill.
- Focused initializer, legacy, distribution and package-verifier checks: 22 passed.
- Rebuilt wheel verifier after method-selection fix: passed, 60 source files
  verified, both language notebooks and existing legacy/update journeys checked.
- Full `.venv/bin/python -m unittest discover -q`: 404 tests in 456.637 seconds,
  OK with 3 skips.
- Changed documentation relative links and `git diff --check`: passed.
- Native Desktop discovery/conversation quality remains unverified. See the
  evaluation ledger for the exact evidence boundaries.
