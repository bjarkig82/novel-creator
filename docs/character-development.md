# Develop a character profile

This feature is an **unpublished 0.9.0 candidate**, compared with published 0.8.0. A
package containing these resources installs them into new format-1 notebooks;
installing or upgrading a package does not change existing notebooks. Existing
notebooks can use the explicit manual procedure below. Legacy novels are outside
this workflow. No CLI command, provider, schema or additional writing role is added.

In an equipped notebook, ask naturally or use the optional skill:

> Fill the gaps in Elin's character profile, focusing on her relationship with
> her brother. Preserve what we already know.

> $novel-character-develop Develop Elin's profile where it most needs depth.

Standalone Claude Code uses `/novel-character-develop`. With the enabled plugin,
use `$novel-creator:novel-character-develop` in Codex or
`/novel-creator:novel-character-develop` in Claude Code. Ordinary language works
with every equipped layout.

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
After publication, install `novel-creator==0.9.0`; until then use the reviewed candidate. The capability
probe below uses `importlib.resources`, so a published 0.8.0 installation lacking
the resources stops before notebook changes. It prints the selected package
resource locations; check they belong to the intended installation.

For default standalone Codex/project notebooks, prefer the reviewed
[preview/apply updater](upgrading-projects.md#existing-markdown-notebooks) from
0.9.0. This manual alternative also supports Codex, Claude Code and both hosts,
with project or plugin skills, in English and Icelandic. A valid integration
marker selects nondefault routing; absent markers mean Codex/project. Malformed,
unsupported or unreadable markers stop before writes. Never remove a marker,
adopt a plugin, reinitialize or convert a book to bypass a refusal.

For plugin notebooks, upgrade and enable the 0.9.0 plugin in the actual host first;
this procedure updates the book's workflow snapshot and root approval sections,
without installing duplicate local skills. Project layouts get the matching
`.agents/skills/` and/or `.claude/skills/` entries. The existing Help catalog is
retained; discover this addition from its root section and actual installed entry.

Open the actual notebook folder and inspect `git status` and its selected
`AGENTS.md` and/or `CLAUDE.md` first.
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
from novel_creator.notebook import _host_text, _instructions

root = Path.cwd().resolve()  # Must be the intended notebook root.

def regular(relative, required=False):
    path = root / relative
    assert path.resolve() == path, f'Redirected path: {relative}; stop.'
    assert not any(p.is_symlink() for p in (path, *path.parents)), (
        f'Symlink path: {relative}; stop.')
    for parent in path.parents:
        assert not parent.exists() or parent.is_dir(), f'Invalid parent: {relative}; stop.'
    if path.exists():
        assert path.is_file() and path.stat().st_nlink == 1, f'Unsafe file: {relative}; stop.'
        assert path.stat().st_mode & 0o444, f'Unreadable file: {relative}; stop.'
    else:
        assert not required, f'Missing prerequisite: {relative}; stop.'
    return path

def normalized(raw):
    return raw.decode('utf-8').replace('\r\n', '\n')

marker = regular('.novel-notebook/integration.json')
host, source = 'codex', 'project'
if marker.exists():
    integration = json.loads(marker.read_bytes())
    assert isinstance(integration, dict) and set(integration) == {
        'version', 'host', 'skill_source'}, 'Invalid integration marker; stop.'
    assert type(integration['version']) is int and integration['version'] == 1, (
        'Unsupported integration marker; stop.')
    host, source = integration['host'], integration['skill_source']
    assert host in ('codex', 'claude', 'both') and source in ('project', 'plugin'), (
        'Unsupported integration marker; stop.')
hosts = ('codex', 'claude') if host == 'both' else (host,)
project = normalized(regular('notebook/project.md', True).read_bytes())
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
    normalized(regular(relative, True).read_bytes())

shared = files('novel_creator.notebook_resources')
codex = files('novel_creator.codex').joinpath('notebook')
print('Package resources:', shared, codex, 'layout:', host, source)
workflow = shared.joinpath('workflows/character-development.md').read_text(encoding='utf-8')
copies = {'.novel-notebook/workflows/character-development.md':
          _host_text(workflow, host, source).encode('utf-8')}
sections = {}
for selected in hosts:
    name = 'AGENTS.md' if selected == 'codex' else 'CLAUDE.md'
    supplied = _instructions(codex, selected, source).decode('utf-8')
    match = re.search(r'^## Character development\n.*?(?=^## |\Z)', supplied, re.M | re.S)
    assert match, 'Package lacks the root feature section; stop.'
    sections[name] = match.group().rstrip() + '\n'
    if source == 'project':
        directory = '.agents' if selected == 'codex' else '.claude'
        skill = codex.joinpath('skills/novel-character-develop/SKILL.md').read_text(encoding='utf-8')
        copies[f'{directory}/skills/novel-character-develop/SKILL.md'] = (
            _host_text(skill, selected, source).encode('utf-8'))

# Preflight every destination before any writes. Retain existing identical bytes.
planned, originals, link_text = {}, {}, {}
for relative, desired in copies.items():
    path = regular(relative)
    original = path.read_bytes() if path.exists() else None
    assert original is None or normalized(original) == normalized(desired), (
        f'Divergent {relative}; preserve and reconcile.')
    originals[relative] = original
    planned[relative] = desired if original is None else original
    link_text[relative] = normalized(desired)
for relative, section in sections.items():
    path = regular(relative, True)
    original = path.read_bytes()
    existing = re.findall(r'^## Character development\n.*?(?=^## |\Z)',
                          normalized(original), re.M | re.S)
    assert len(existing) <= 1 and (not existing or existing[0].rstrip() == section.rstrip()), (
        f'Divergent root feature section in {relative}; preserve and reconcile.')
    originals[relative] = original
    planned[relative] = original if existing else original + (
        ('\n' if original.endswith(b'\n') else '\n\n') + section).encode('utf-8')
    link_text[relative] = section  # Unrelated custom root links are not feature links.
for relative, raw in planned.items():
    if raw == originals[relative]:
        continue
    path = root / relative
    owner = path if path.exists() else next(p for p in path.parents if p.exists())
    assert owner.stat().st_mode & 0o222, f'Unwritable destination: {relative}; stop.'
for relative, text in link_text.items():
    path = root / relative
    for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
            continue
        target = (path.parent / link).resolve()
        assert target.is_relative_to(root) and (
            target.relative_to(root).as_posix() in planned or target.is_file()), (
                f'Unresolved local link in {relative}: {link}; stop.')

for relative, raw in planned.items():
    path = regular(relative)
    original = originals[relative]
    assert (path.read_bytes() if path.exists() else None) == original, (
        f'Changed during maintenance: {relative}; stop and reconcile.')
    if original is None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    elif raw != original:
        path.write_bytes(raw)
for relative, raw in planned.items():
    assert regular(relative, True).read_bytes() == raw, f'Verification failed: {relative}'
print('Verified rendered feature resources and root sections; Git staging/history untouched.')
```

Review the resulting diff: only the feature workflow, selected project skill entries (if applicable) and
appended root feature section(s) should change. All story bytes, existing index entries and custom root
guidance must remain intact. The snippet leaves Git staging and history alone;
it is not a cross-file transaction. On write failure, inspect the actual files,
preserve partial work and rerun only after reconciliation. For an optional local
checkpoint, follow the notebook's native focused Git guidance for the exact changed
paths, preserving unrelated staged writer edits; do not use a blanket `git add`
or automatically push.

Have the host read the updated root instructions, skill and workflow before
writing. Installed bytes do not prove native skill discovery or that an active
chat has reloaded guidance. Use the host's actual supported project/reload
controls if available; there is no universal reload command. A new chat may be
needed, and chat-only drafts will not thereby become recoverable.
