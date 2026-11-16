# Create a complete side-character profile

This feature ships in **0.10.2, published 2026-11-16**, and was absent from
0.10.1. See the [release notes](releases/0.10.2.md) and
[qualification evidence](../tests/evaluations/release-0.10.2.md) for verified scope
and native-host limits. Installing a Python package or plugin alone does
not refresh resources pinned into an existing novel. Use only a book equipped
with the matching workflow and routing; do not reinitialize or convert a book
to obtain it. Project upgrade instructions are maintained separately in the
[upgrade guide](upgrading-projects.md).

Ask naturally, or use the optional chat skill:

> Create a complete supporting-character profile for the harbour's radio
> technician. She knows Elin from school. Keep her outside the central conspiracy.

> $novel-side-character Create a minor character who runs the night ferry.

Plugin Codex uses `$novel-creator:novel-side-character`; standalone Claude Code
uses `/novel-side-character` and its plugin uses
`/novel-creator:novel-side-character`, when equipped. These are chat inputs, not
terminal commands. No new writing role, provider or data schema is added.

The agent first reads project directions, relevant accepted facts, character
owners, unresolved findings and language guidance. It asks up to three missing
basics **one at a time**: role, connection to the cast, and fixed traits or limits.
It skips known answers. Say “skip”, “you decide” or request a shorter profile to
move directly to useful prose. A necessary identity or conflict clarification
can still be asked, without turning the flow into an extended interview.

Expect one connected practical profile of roughly **400–700 words**, shorter
when requested or appropriate, covering identity, appearance, voice, personality,
motivation, relevant history, relationships and continuity cues. These are actual
proposed paragraphs, not a checklist. A side character needs no compulsory arc,
major plot function, diagnosis or solution to an intentional mystery. Existing
facts remain protected; objective truth, character beliefs and reader knowledge
remain distinct, with timing and uncertainty intact.

This complete-profile mode takes precedence over generic enrichment for an
explicit side/supporting/minor profile request. A character topic alone or
`$novel-character` still starts ordinary exploration. “Deepen Elin's motivation”
retains the separate [character-development](character-development.md) mode.

Discuss, revise or cancel the profile. “I like it”, selecting a trait, or “Make
her less formal” alone does not save/accept the generated profile. **“Save this
profile” accepts and saves the current complete profile with no second approval.**
“Save only the voice paragraph” selects a narrower current part. You can explicitly
ask to retain a selected part as proposed. Saving includes only profile content,
not the assistant's explanatory rationale, and authorizes no manuscript or
other-character changes. The agent rereads owners before applying and asks for
direction if current facts or intervening edits conflict. Existing identity,
history, provenance, linked owners and unrelated staging remain protected.
After saving or cancelling, the mode stops; no next character starts automatically.

The two formats have different persistence rules:

| Format | Before approval | On clear save approval |
| --- | --- | --- |
| Format-1 Markdown notebook | Entire intake, profile and revisions stay in chat. No notes, summaries, draft/handoff files or checkpoints in any role. Unsaved drafts have no guaranteed recovery in another chat or after interruption. | Save approved profile prose to the appropriate owning character/topic notes, preserving Item-IDs, Origin and history; then follow scoped checkpoint rules. |
| Legacy structured novel | Normal exact-current-input, sourced exchange capture and save-before-display continue every turn. Generated details are captured as proposed; clear writer answers keep normal authority. Cancellation does not erase historical captures. | Accept/save the current approved profile through existing character elements, assertions, relationships and current-user decisions; no duplicate authoritative profile document. Later retrieval uses normal source-backed context. |

File saves and Git checkpoints are reported separately. Approval alone does not
prove writing. Partial/failed saves need current-file inspection and a retry of
only still-authorized missing work, without duplicate records. A successful file
save with a pending checkpoint remains saved with history pending.

English and Icelandic project languages are supported. For example:

> Búðu til heila persónulýsingu fyrir aukapersónu sem sér um næturferjuna.
> Hún þekkir Elínu úr skóla. Haltu henni utan aðalráðgátunnar.

Saved prose and headings use the configured project language with stable field
labels and IDs. An explicit conversation/output-language request follows existing
language rules without silently changing the project's language.

The [notebook workflow](../notebook/workflows/side-character.md) and
[legacy workflow](../workflows/side-character.md) define the full safeguards.
The [synthetic host rubric](../tests/fixtures/side-character/scenarios.md) is
explicitly unexecuted: resource contracts and storage tests do not verify native
skill discovery, conversational compliance, idiom or literary quality.

<a id="install-or-update-the-unpublished-candidate"></a>

## Install or update 0.10.2

Create an isolated Python 3.11+ environment outside all novels, then install
the published version. Git 2.39+ and an existing local Git identity are required
for project initialization:

```text
python -m venv /outside/books/side-character-env
/outside/books/side-character-env/bin/python -m pip install --upgrade novel-creator==0.10.2
```

On Windows use that environment's `Scripts/python.exe`. For explicit local
artifact evaluation, a reviewed matching `.whl` or `.tar.gz` can replace the
package argument. Use the selected environment's interpreter and console command
throughout the steps below. Package installation leaves existing books pinned.

- **New legacy novel:** ordinary authorized legacy initialization from the
  package installs `.agents/skills/novel-side-character/SKILL.md`, its legacy
  workflow and routing. Existing structured save/capture rules remain.
- **Existing legacy novel:** use the external controller's
  ordinary framework update preview/application, selecting version `0.10.2`, as described
  in [project upgrades](upgrading-projects.md#side-character-profiles-in-0102).
  Review the concrete changed paths, blockers and HEAD; apply only that preview.
  The public discovery gate requires a published stable target; select 0.10.2.
  Offline fixture transport used during qualification is separate from this
  public update route and does not establish a real-novel update.
  The update changes managed resources in a framework commit while preserving story,
  custom instructions and unrelated staging. It does not convert the book.
- **New format-1 notebook:** ordinary authorized notebook initialization installs
  the workflow, selected root section and project skill for the chosen host.
  Plugin layouts use the enabled matching plugin skill and keep no duplicate
  local skill. Update/enable the matching 0.10.2 plugin in the actual host first;
  package installation does not update a plugin cache.
- **Existing default Codex/project notebook without an integration marker:**
  run `novel-creator notebook update --path BOOK --json`, review its changes,
  then run `novel-creator notebook update --path BOOK --apply --preview PREVIEW_ID
  --expected-head REVIEWED_HEAD --json`. This focused updater also supplies its
  absent prerequisites and refreshes only recognized public Help snapshots.
  Customized managed resources stop safely.
- **Other supported format-1 notebooks:** use the bounded procedure below.
  It supports English/Icelandic and Codex/Claude Code/both with project/plugin
  skills. The default layout can also use it for feature-only additions.
  Do not remove/change integration markers or reinitialize to bypass a refusal.

Pause editing and review the selected roots (`AGENTS.md` and/or `CLAUDE.md`),
Git status and any custom writer policy. Save this short script **outside the
notebook** as `side-character-upgrade.py`:

```python
import json
import sys
from novel_creator.cli import ToolError
from novel_creator.notebook_side_character import update

try:
    if len(sys.argv) == 3 and sys.argv[2] == 'preview':
        result = update(sys.argv[1])
    elif len(sys.argv) == 5 and sys.argv[2] == 'apply':
        result = update(sys.argv[1], apply=True, preview_id=sys.argv[3],
                        expected_head=sys.argv[4])
    else:
        raise SystemExit('Usage: script BOOK preview | script BOOK apply PREVIEW_ID REVIEWED_HEAD')
except ToolError as error:
    print(json.dumps(error.result(), ensure_ascii=False, indent=2))
    raise SystemExit(error.code)
print(json.dumps(result, ensure_ascii=False, indent=2))
```

Use the selected isolated interpreter; preview writes no files or directories:

```text
python -B /outside/books/side-character-upgrade.py BOOK preview
python -B /outside/books/side-character-upgrade.py BOOK apply PREVIEW_ID REVIEWED_HEAD
```

Review `changes`, `host`, `skill_source`, `language`, `preview_id` and
`reviewed_head` before application. The helper binds the installed package and
rendered resources, all inspected bytes/absence/identities, destination parents,
exact Git index and HEAD. It adds only the side-character workflow, applicable
project skill and protected root section. Existing root bytes, Help, roles,
shared workflows, story/history and staging stay intact. The appended section
explicitly overrides older generic enrichment/automatic-save routing for this
mode and tells Help to inspect the actual feature entry even with an older catalog.
The conservative preflight refuses feature-specific side/supporting/minor-character
labels (including plural/hyphen forms and Icelandic `aukapersón*`) anywhere outside
the protected section, irrespective of word order or line breaks. Reconcile that
text manually even when it is harmless; the helper does not interpret writer
policy. Human review remains necessary for arbitrary wording. Custom unrelated
generic root instructions are preserved. No commit is made by this helper.

Missing prerequisites, mixed/retained-legacy formats, unsupported markers,
custom/duplicate feature resources, redirected paths, hardlinks and stale
reviews refuse. Partial failures disclose completed `written_paths` and an
`attempted_path` that may be incomplete: inspect those files, preserve completed
work, then take/apply a fresh preview for remaining additions. An incomplete or
customized file must be reconciled explicitly rather than blindly overwritten.

For every route, review actual changed resources and links before continuing.
Have the active host reread the selected root, actual installed/enabled
`novel-side-character` skill and selected-book workflow; use its supported
reload/reopen controls, possibly a new chat in the novel folder itself. Codex
uses `$novel-side-character` or `$novel-creator:novel-side-character`; Claude Code
uses `/novel-side-character` or `/novel-creator:novel-side-character`. File/import
checks do not establish native discovery. Installation/update performs no
profile save; notebook intake/drafts remain chat-only until explicit save
authority. No Python requirement is added to ordinary notebook writing.
