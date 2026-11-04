# Repository tooling

Spec Kit workflows are in `.agents/skills/speckit-*/SKILL.md`. Use the script
variant for the session's shell:

- Bash (cloud, Linux, macOS, WSL, or Git Bash): run
  `bash .specify/scripts/bash/<name>.sh` with Bash flags such as `--json`.
- PowerShell (local Windows): run
  `.specify/scripts/powershell/<name>.ps1` with PowerShell flags such as `-Json`.

Run scripts from the repository root. Both variants use the same templates and
feature state. Do not invoke `.ps1` files directly from Bash. Bash sessions do
not require PowerShell or the Specify CLI for the checked-in scripts.
Quote arguments using the current shell's syntax; Bash single-quote escape
examples in the workflows do not apply to PowerShell.

The `script: "ps"` entries in Spec Kit's initialization metadata record how the
project was originally generated; select scripts using the current shell.
When refreshing Spec Kit, preserve both script directories and the shell choices
in the agent workflows. Keep Bash scripts on LF line endings.

## Development workflow

Use subagent-driven development by default for implementation work. When
available, follow the `superpowers:subagent-driven-development` skill; the
workflow below also applies when that skill is not installed.

- The coordinator owns the plan, task sequencing, and progress reporting.
- Give each implementation task to a fresh, scoped implementer subagent with
  self-contained context, requirements, constraints, and expected validation.
- After each task, use independent reviewers to check spec compliance and code
  quality, and resolve findings before moving on. Finish with an independent overall review.
- Do not run writers in parallel when they touch shared files.
- Continue through routine implementation and review without permission
  questions. Explicit user preferences override these defaults.
- If subagents are unavailable, state that limitation and execute the workflow
  inline, including validation and review.
