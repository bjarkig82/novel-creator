# Notebook Outline Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver an installed, explicitly invoked outline skill for new story notebooks.

**Architecture:** A thin notebook-specific Codex skill loads shared creative guidance. Notebook initialization copies the adapter and shared workflow; packaging and installed-resource verification cover both. Existing legacy skills stay separate.

**Tech Stack:** Markdown skills, Python setup, setuptools, unittest.

**Spec:** docs/superpowers/specs/2026-11-05-outline-skill-design.md (approved by the writer).

## Global Constraints

- Outline-only; no chapter/scene manuscript files or new CLI command.
- Preserve existing facts, states, stable identities, writer edits, and local history.
- Support English and Icelandic; do not convert or silently update existing notebooks.
- No external publication, push, or legacy behavior changes as part of the outline workflow. Repository delivery follows the user’s later authorization to push directly to main.

## Review Focus

- Sparse notes must not become invented accepted facts.
- Structure selection must not silently accept new story facts.
- Existing outlines and direct writer edits must survive revision.
- Installed skill references must resolve in both languages and built wheels.
- Legacy initialization/export must not install the notebook-only skill.

## Task 1: Deliver the outline skill end to end

**Files:** Create notebook/workflows/outline.md and adapters/codex/notebook/skills/novel-outline/SKILL.md; modify src/novel_creator/notebook.py, adapters/codex/notebook/AGENTS.md, pyproject.toml, tests/verify_wheel.py, relevant notebook tests, and README.md.

**Interfaces:** initialize(target, *, title=None, language='en') remains unchanged. New notebooks receive .agents/skills/novel-outline/SKILL.md referencing .novel-notebook/workflows/outline.md. Shared workflow uses format-1 topic records and existing native save/history rules.

- [x] Record baseline application scenarios before authoring the skill; verify installation expectations fail before implementation.
- [x] Implement the thin skill and shared outline workflow, with proposal/refinement/selection saving, linked topic ownership, incomplete-information handling, revision preservation, and both language resources.
- [x] Install and package the resources for new notebooks only; extend wheel verification and meaningful initialization/legacy regression coverage.
- [x] Document invocation and scope; run focused tests and actual wheel verification where environment supports it.
- [x] Run representative application scenarios with the skill and record evidence boundaries without claiming native-host qualification.
- [x] Commit scoped changes and report validation, limitations, and self-review findings.

## Review and completion

- [x] Independent spec and quality review; resolve material findings and verify fixes.
- [x] Independent overall review; no material findings.
- [x] Final delivery authorized: the writer explicitly requested pushing now while the broader recovery suite continues, with any findings addressed afterward.

## Execution ruling

The user approved implementation after selecting the skill and outline-only scope. Repository AGENTS.md selects delegated implementation by default. Proceed without another execution-method permission question.

## Results

The outline implementation and documentation migration received independent scoped reviews and an independent combined review, with no material findings. Focused initialization, legacy-boundary, wheel/source-distribution installs and built-wheel verification passed in English and Icelandic. Simulated-writer applications preserved proposal states, open questions, writer edits, history and unrelated staging. Native Desktop skill discovery remains unverified. See tests/evaluations/outline-skill.md.

The user also requested removal of Spec Kit and the existing top-level specs, preservation of normal functionality documentation, explicit subagent-driven development instructions, and committing/pushing the completed changes directly to main. These scope additions are included in the implementation.

The broader full-suite run was still advancing through recovery checks at delivery; it is not claimed as passed. The writer explicitly chose to proceed with the reviewed changes and completed focused/package/application checks rather than wait for that run.
