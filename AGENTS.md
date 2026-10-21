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
