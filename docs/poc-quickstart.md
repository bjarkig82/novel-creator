# Start the single-user POC

This POC runs in Codex against an independent local Git repository per novel.
It supports conversational setup, guided/open brainstorming, saved questions
and proposals, explicit canon decisions, continuity review, inspection and
resumption. English and Icelandic text are supported. No manual test or novice
evaluation is required before starting; the owner will try it after delivery.

## Start from this configured checkout on Windows

Run PowerShell in the Novel Creator checkout. The existing .venv contains the
configured dependencies. Choose an unused novel folder outside this checkout
and every other Git repository. The example leaves creative preferences unknown.

```powershell
$novelPython = (Resolve-Path .venv/Scripts/python.exe).Path
$novelPath = Join-Path $env:USERPROFILE 'Documents/Novels/MyNovel'
$briefPath = Join-Path ([IO.Path]::GetTempPath()) ('novel-brief-' + [guid]::NewGuid() + '.json')
[IO.File]::WriteAllText($briefPath, '{}', [Text.UTF8Encoding]::new($false))
& $novelPython -m novel_creator init --path $novelPath --brief-file $briefPath --json
& $novelPython "$novelPath/.novel-creator/run.py" context --novel $novelPath --json
```

Git must already have your author/committer identity configured. Initialization
reports a missing identity and refuses occupied unrelated or nested repositories;
it does not change global Git settings. Change the example novel path as needed.
Keep the original brief unchanged if an interrupted initialization needs retry.

Open that novel folder as a project in Codex. Use `$novel-init` for conversational
setup, `$novel-brainstorm` for exploration, `$novel-resume` to return to a saved
session, or `$novel-inspect` to inspect saved records. A starting request can be:

> I have no concept yet. Help me begin with one question at a time.

Unknown creative choices can stay unknown. Request Icelandic, free exploration,
a different topic, fewer suggestions or a checkpoint when helpful. Clear story
acceptance establishes only the selected fact; a proposal remains unaccepted.
The installed workflow saves each exact exchange before displaying its reply.

## Independent distribution

The latest verified wheel is
[novel_creator-0.1.0-py3-none-any.whl](../dist/phase22-20261023/novel_creator-0.1.0-py3-none-any.whl).
It includes the [save-before-display commentary clarification](../tests/evaluations/display-boundary-20261023.md),
verified against freshly installed workflows. The original
[POC evidence report](../tests/evaluations/poc-readiness-20261023.md) retains its
source-specific baseline and known limits.
On a different machine create a Python >=3.11 environment, install that wheel
with its jsonschema/jsonschema-rs dependencies and use Git >=2.39. Run the same
init command with that environment's Python. Initialized novels contain a pinned
launcher, product modules and workflows; they need the Python dependencies but
do not need the original framework checkout or a model API key.

## Return later or inspect a save

```powershell
& $novelPython "$novelPath/.novel-creator/run.py" session list --novel $novelPath --json
& $novelPython "$novelPath/.novel-creator/run.py" inspect --novel $novelPath --kind assertion --json
& $novelPython "$novelPath/.novel-creator/run.py" validate --novel $novelPath --json
```

Use `$novel-resume` in the novel's Codex project to recover its focus, mode,
canon, proposals and open questions. A saved reply's display is unconfirmed until
the host observation establishes it; that never implies story acceptance.

If saving fails, preserve the pending exchange and last confirmed checkpoint.
Use the [documented recovery commands](../README.md#development) to inspect it
before an unchanged retry. Scoped filesystem approval may be needed when the
Windows sandbox denies hard links. Never delete receipts or bypass a held lock.

The POC's automated evidence and known large-history performance/semantic limits
are documented separately. Older novels keep their installed bundle; this build
does not silently upgrade them. Start a new workspace for the updated POC rather
than replacing an existing novel's files.

The [2026-10-28 qualification assessment](../tests/evaluations/phase22-release-assessment-20261028.md)
adds completed automated scenario matrices and the current full-scale timings.
The owner withdrew all latency targets on 2026-10-28. Read/save timings are
informational and optimization is deferred until after functional delivery.
No manual test is required to use the POC. See the
[final functional qualification](../tests/evaluations/final-functional-qualification-20261028.md).
