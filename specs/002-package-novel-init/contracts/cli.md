# CLI Contract: Simple Initialization

Status: planned additive interface; examples require implementation. Existing [CLI contract](../../001-novel-initialization-brainstorming/contracts/cli.md) remains authoritative for legacy operations.

## Forms

```text
novel-creator --version
novel-creator --help
novel-creator init --help
novel-creator init NAME [--path DESTINATION] [--title TITLE] [--language en|is] [--json]
novel-creator init --path DESTINATION --brief-file FILE [--json]
```

No separator before optional flags. NAME required only for shorthand. --path is the full target (absolute or relative to cwd). Default target: cwd/NAME. --title defaults to NAME; language retains existing en default. Reject empty explicit title, whitespace-only/invalid/path-like NAME and unsupported language. Unicode/spaces remain unchanged. Names beginning with '-' may use the standard end-of-options separator after flags; exclude that special case from minimal examples.

Reject NAME plus --brief-file, title/language plus --brief-file, incomplete legacy path/brief pair, title/language without NAME, duplicate settings and unknown options before writes. Help/version perform no novel writes/network.

## Output

Shorthand default: readable resolved folder, saved/ready or recovery status, exact interpreter, pinned launcher, local guide and $novel-init next action. No story dump, mandatory color formatting or claim that brainstorming started. UTF-8 text.

Shorthand --json: exactly one JSON envelope on stdout, diagnostics on stderr. Existing shape plus output-only additions from [data model](../data-model.md). No prose mixed into JSON. Failures identify prerequisite/destination/access/partial-state category and safe next action without printing briefs.

Legacy: keep current JSON even without --json, raw brief provenance/defaults, root checks and retry semantics. Other commands unchanged.

| Exit | Meaning |
| --- | --- |
| 0 | Confirmed saved result or recognized novel; inspect cleanup_required/ready |
| 2 | Invalid arguments/names/language/brief/evidence |
| 3 | Existing content, changed retry/file, stale-state conflict |
| 4 | Unsupported runtime/schema or unavailable context |
| 5 | Filesystem/Git failure; retain current classification for absent Git/identity |
| 6 | Lock held |

Published save with index cleanup outstanding: exit 0, saved true, cleanup_required true, ready false, recovery instructions. No replay/rollback or ready message. Improve missing-prerequisite diagnostics without changing legacy code classification or configuring Git automatically.

## Safety and retry

Reuse bootstrap/install/storage, never a second initializer. Normalize shorthand request once and compare it plus brief on retry; retain original IDs/resources. Recognized novels preserve settings even when new flags differ; explain ignored replacement choices. Changed checksum/resources surface repair conflict.

Retain legacy allowance for otherwise empty unborn repositories and safe instruction/metadata files. Refuse unrelated occupied/nested/redirected roots; preserve AGENTS.md, history and unrelated work. No pushes, global changes, permission bypass, providers, auto-upgrades or manuscript writes. Subprocesses use argument arrays without shell interpolation; displayed commands quote paths for the shell.

For shorthand continuation of a pre-feature novel lacking a guide, return the verified installed-package guide path and label the fallback; do not install a guide into the old novel. Evaluate readiness against its original manifest. Prefer an existing verified pinned guide when available, and explain that package-guide instructions do not upgrade its installed workflows. Missing fallback resources produce an actionable diagnostic, never a fabricated path. Preserve legacy result fields/rendering.

## Runtime handoff

Completion prints sys.executable and the pinned run.py location. Writer supplies the interpreter path to the Codex novel project; workflows invoke that interpreter, not an assumed system Python. Opening Codex independently does not establish activation. Reopening/moving novels uses a documented compatible environment and updated local path guidance, without committing machine paths or mutating history.
