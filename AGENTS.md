# Development

This is a small, single-maintainer project. Keep the process proportionate to the change.

- Read the relevant code, tests and documentation before editing. Preserve unrelated work.
- For a small change, explain the intended result briefly and implement it directly.
  For larger changes, keep a short plan with concrete steps and update it as needed.
  No templates, numbered feature directories or separate specification workflow are required.
- Make focused changes; preserve existing novel data, compatibility and writer authority.
- Run checks relevant to the change. Add regression tests for meaningful behavior changes;
  documentation-only changes usually need link/reference checks and a diff review.
- Review the diff, update ordinary documentation when behavior changes, and report what
  changed, what was checked and any remaining limits. Do not imply unobserved host behavior
  or subjective writing quality was verified by structural tests.
- Follow the user's authorization for commits and pushes. Publishing, deployment and
  changes to a real novel require their own authorization.

See [functionality](docs/functionality.md), [development setup](docs/development.md)
and [testing guidance](docs/testing-and-completion-guide.md). Application workflows
and installed Codex skills are product resources; preserve them when changing tooling.

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
