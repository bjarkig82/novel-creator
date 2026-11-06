# Development

This is a small, single-maintainer project. Keep the process proportionate to the change.

- Read the relevant code, tests and documentation before editing. Preserve unrelated work.
- For a small change, explain the intended result briefly and implement it directly.
  For larger changes, keep a short plan with concrete steps and update it as needed.
  No templates, numbered feature directories or separate specification workflow are required.
- Make focused changes; preserve existing novel data, compatibility and writer authority.
- Follow the focused testing policy below. Add regression tests for meaningful
  behavior changes; documentation-only changes need reference/link checks and a diff review.
- Review the diff, update ordinary documentation when behavior changes, and report what
  changed, what was checked and any remaining limits. Do not imply unobserved host behavior
  or subjective writing quality was verified by structural tests.
- Follow the user's authorization for commits and pushes. Publishing, deployment and
  changes to a real novel require their own authorization.

See [functionality](docs/functionality.md), [development setup](docs/development.md)
and [testing guidance](docs/testing-and-completion-guide.md). Application workflows
and installed Codex skills are product resources; preserve them when changing tooling.

## Focused testing policy

For normal implementation, review, commit and push work, choose the smallest
meaningful set of affected test modules or cases, including direct dependencies.
Expand focused checks when failures or affected behavior warrant it; this does
not automatically require the full suite. Do not rerun exhaustive historical
recovery scenarios or the complete release wheel verifier for every task.
Documentation-only changes normally need reference/link validation and diff
whitespace review, without running code tests.

Run the full suite and any required full coverage checks only when preparing a
new package release before publication, or when the user explicitly requests
them. Every release requires full Linux qualification. Windows uses the source-bound
`auto` policy (compatibility for routine changes, full for sensitive changes or
uncertain history); `full` explicitly requests full Windows coverage. Compatibility
coverage must never be described as full qualification. See the
[Windows release policy](docs/testing-and-completion-guide.md#windows-release-selection).
Preserve all existing release workflow gates; focused routine checks do
not replace release validation or authorize publication.

When resource inclusion changes, keep targeted artifact-content and isolated
install/package checks for the affected resources, including wheel and source
distribution contents. These checks are distinct from the complete rebuilt-wheel
release verifier, which also exercises broad legacy and update journeys.

Report the exact checks run, their results and remaining limits. Focused passing
results do not establish full-suite or full-coverage success.

## PyPI releases

When asked to publish a new version of `novel-creator` to PyPI, prepare its
release documentation before publication as part of the release work:

- Create or update `docs/releases/<version>.md` and add it to the
  [release history](docs/releases/README.md), newest version first. Link the
  release history from the README when updating its installation/version guidance.
- State the exact package version and whether it is an unpublished candidate or
  a verified published release. Add the publication date only after verifying
  publication; do not describe a planned release as available on PyPI.
- Compare with the previous published version, using the relevant source changes
  and release evidence. Explain user-visible additions, fixes, changed behavior,
  compatibility or breaking changes, and known limitations in plain language.
  Omit empty categories and distinguish verified behavior from pending work.
- Include a version-pinned install/upgrade command and any required migration or
  follow-up steps. Explain effects on existing novels, including when installing
  the package leaves their pinned resources unchanged. For candidates, label the
  command as usable only after publication.
- Keep the notes, package version, installation guidance and release artifacts
  consistent. Follow the existing candidate checks and publication workflow;
  release notes do not replace validation or authorize publication.
- After authorized publication, verify availability, update the notes' status and
  date, and report the version, main changes and release-note location to the user.

## Implementation and review

Use subagent-driven development for implementation work in this repository.
When available, follow the `superpowers:subagent-driven-development` skill.
The coordinator keeps the lightweight plan, sequences work and reports progress.
Give implementation slices to scoped implementers with self-contained context and
expected validation. After each slice, obtain independent requirement-compliance
and code-quality review, resolve findings and finish with an independent overall
review. Do not run writers concurrently on shared files. Continue routine work
without repeated permission requests. If subagents are unavailable, say so and
perform the same implementation, validation and review steps inline. Explicit
user instructions override these defaults.
