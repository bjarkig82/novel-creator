# Develop a character profile

This feature is **unpublished source work**, not part of published 0.6.0. A
package containing these resources installs them into new format-1 notebooks;
installing or upgrading a package does not change existing notebooks. Existing
notebooks can use the explicit manual procedure below. Legacy novels are outside
this workflow. No CLI command, provider, schema or additional writing role is added.

In an equipped notebook, ask naturally or use the optional skill:

> Fill the gaps in Elin's character profile, focusing on her relationship with
> her brother. Preserve what we already know.

> $novel-character-develop Develop Elin's profile where it most needs depth.

Without a focus, the agent chooses useful gaps from the owning notes and briefly
explains its choice. Expect a summary of at most about 100 words, then 2–3
connected additions of actual profile prose totaling roughly 200–400 words,
less when appropriate. Ask for a smaller batch at any time. After one batch the
agent waits; it does not continue generating automatically. Ordinary exploratory
character work and `$novel-character` still use question-led brainstorming;
“Just ask questions; no suggestions yet” remains a valid preference.

The additions are proposals in chat, not saved notes or accepted canon. Discuss,
revise or discard them: “Make addition 2 less hostile,” “I like 1,” and “Let's
choose 2” do **not** authorize saving. Numbers stay stable through revisions.
“Save addition 2” saves only its current text; “Save the current draft” saves the
current additions. Explicit saving accepts the selected facts unless you ask to
save them as proposals. You can also say “Save only the first paragraph of 2 as
proposed; discard the rest.” Clear instructions need no repeated approval.

Accepted facts remain intact unless you explicitly request a revision. Conflicts
need direction; character beliefs and reader knowledge remain distinct from story
truth. Approved saves preserve owning notes, stable IDs, provenance, history and
unresolved questions. They do not authorize manuscript edits. Unselected additions
remain chat-only even after a save, cancellation or topic change. Before saving,
there are no notes, summary changes, draft/handoff files or Git checkpoints for
this mode. Unsaved drafts have no guaranteed recovery after interruption or in
another chat. File saves and pending/failed checkpoints must be reported separately.

English and Icelandic project languages are supported, for example:

> Dýpkaðu persónulýsingu Elínar, sérstaklega sambandið við bróður hennar.

The [shared workflow](../notebook/workflows/character-development.md) defines the
full behavior; the [evaluation ledger](../tests/evaluations/character-development.md)
separates structural checks from unverified native conversation and literary quality.

## Manually install into an existing format-1 notebook

Use a trusted source checkout or package artifact containing this feature, in an
isolated Python environment (Python 3.11+). For a source checkout, install that
reviewed checkout with `python -m pip install /absolute/path/to/novel-creator`.
There is no released version number to request for this feature. The capability
probe below uses `importlib.resources`, so a published 0.6.0 installation lacking
the resources stops before notebook changes. It prints the selected package
resource locations; check they belong to the intended installation.

Open the actual notebook folder and inspect `git status` and its `AGENTS.md` first.
Read the supplied [root Character development section](../adapters/codex/notebook/AGENTS.md#character-development).
Reconcile custom instructions that explicitly conflict with its chat-only
exception intentionally, retaining the writer's original guidance. Do not blindly
refresh `AGENTS.md` or any older workflows, reinitialize the notebook or change
global configuration. If prerequisites below are absent, stop and reconcile that
notebook separately rather than copying a blanket resource bundle.

With notebook editing paused, run this one-off Python snippet from the notebook
root using the environment containing the feature. Paste it into Python or save
it outside the notebook and run it there; it is a manual maintenance example,
not an updater command. It checks format 1, configured language, shared guidance,
links and all existing destinations before writing. Divergent resources or an
existing differing feature section stop the procedure with original bytes intact;
compare and reconcile them manually, then rerun. Identical installation is harmless.

```python
from importlib.resources import files
from pathlib import Path
import json
import re

root = Path.cwd().resolve()  # Must be the intended notebook root.
shared = files('novel_creator.notebook_resources')
codex = files('novel_creator.codex').joinpath('notebook')
copies = {
    '.novel-notebook/workflows/character-development.md':
        shared.joinpath('workflows/character-development.md').read_bytes(),
    '.agents/skills/novel-character-develop/SKILL.md':
        codex.joinpath('skills/novel-character-develop/SKILL.md').read_bytes(),
}
supplied = codex.joinpath('AGENTS.md').read_text(encoding='utf-8')
section_match = re.search(r'^## Character development\n.*?(?=^## |\Z)',
                          supplied, re.M | re.S)
assert section_match, 'Package lacks the root feature section; stop.'
section = section_match.group().rstrip() + '\n'
print('Package resources:', shared, codex)

project = (root / 'notebook/project.md').read_text(encoding='utf-8')
envelope = re.match(r'\A(```|~~~)json\n(.*?)\n\1\n', project, re.S)
assert envelope, 'Missing format metadata; stop.'
meta = json.loads(envelope[2])
assert isinstance(meta, dict) and type(meta.get('version')) is int, 'Invalid metadata; stop.'
assert (meta.get('format'), meta.get('version'), meta.get('kind')) == (
    'novel-notebook', 1, 'project'), 'Requires a format-1 notebook; stop.'
language = meta.get('language')
assert language in ('en', 'is'), 'Unsupported configured language; stop.'
for relative in ('notebook/working-summary.md',
                 '.novel-notebook/workflows/conversation.md',
                 '.novel-notebook/workflows/format.md',
                 '.novel-notebook/workflows/agents.md',
                 '.novel-notebook/workflows/brainstorming.md',
                 f'.novel-notebook/languages/{language}.md'):
    assert (root / relative).is_file(), f'Missing prerequisite: {relative}; stop.'

agents_path = root / 'AGENTS.md'
original = agents_path.read_bytes()
text = original.decode('utf-8').replace('\r\n', '\n')  # Compare text; preserve original bytes.
existing = re.search(r'^## Character development\n.*?(?=^## |\Z)',
                     text, re.M | re.S)
assert not existing or existing.group().rstrip() == section.rstrip(), (
    'Divergent root feature section; preserve and reconcile before retrying.')
merged = original if existing else original + (
    ('\n' if original.endswith(b'\n') else '\n\n') + section).encode('utf-8')
planned = {**copies, 'AGENTS.md': merged}
for relative, raw in planned.items():
    path = root / relative
    assert not any(p.is_symlink() for p in (path, *path.parents)), (
        f'Symlink destination: {relative}; stop.')
    if relative != 'AGENTS.md' and path.exists():
        assert path.read_bytes() == raw, f'Divergent {relative}; preserve and reconcile.'
    for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', raw.decode('utf-8')):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
            continue
        target = (path.parent / link).resolve()
        assert target.is_relative_to(root) and (
            target.relative_to(root).as_posix() in planned or target.is_file()), (
                f'Unresolved local link in {relative}: {link}; stop.')

for relative, raw in copies.items():
    path = root / relative
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
if merged != original:
    assert agents_path.read_bytes() == original, 'AGENTS.md changed; stop and reconcile.'
    agents_path.write_bytes(merged)
for relative, raw in planned.items():
    assert (root / relative).read_bytes() == raw, f'Verification failed: {relative}'
print('Verified two feature resources and merged root section; Git staging/history untouched.')
```

Review the resulting diff: only the two new resources and the root feature
section should change. All story bytes, existing index entries and custom root
guidance must remain intact. The snippet leaves Git staging and history alone;
it is not a cross-file transaction. On write failure, inspect the actual files,
preserve partial work and rerun only after reconciliation. For an optional local
checkpoint, follow the notebook's native focused Git guidance for these three
paths, preserving unrelated staged writer edits; do not use a blanket `git add`
or automatically push.

Have the host read the updated root instructions, skill and workflow before
writing. Installed bytes do not prove native skill discovery or that an active
chat has reloaded guidance. Use the host's actual supported project/reload
controls if available; there is no universal reload command. A new chat may be
needed, and chat-only drafts will not thereby become recoverable.
