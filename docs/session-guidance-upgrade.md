# Update session guidance in an existing notebook

This procedure delivers **published 0.10.3 guidance (2026-11-16)**.
Version 0.10.2 lacks these improvements; its [version-pinned guide](https://github.com/bjarkig82/novel-creator/blob/v0.10.2/docs/session-guidance-upgrade.md)
and [release evidence](../tests/evaluations/release-0.10.2.md) remain historical.
Use an isolated Python 3.11+ environment outside novels. Install the exact
published package:

```text
python -m pip install --upgrade novel-creator==0.10.3
```

Use that same environment for every step. Update/enable the matching 0.10.3 plugin
first where used; do not copy project skills into plugin books. Installation
alone leaves existing notebook snapshots unchanged, including 0.10.2 notebooks.

Before this six-guide refresh, install missing feature prerequisites explicitly:

1. If `side-character.md` is absent, run the supported [side-character feature-only
   preview/application](side-characters.md#install-or-update-0102), using the
   already-selected 0.10.3 environment and matching plugin. Follow only that guide's
   existing-notebook feature preview/apply steps and short script; skip its
   historical 0.10.2 package/plugin installation and new-project instructions.
   Truly old public 0.10.0 notebooks lack this prerequisite; the revised
   brainstorming/format links require it.
   This adds the feature workflow, actual project skill (or plugin routing) and
   bounded root section; it saves no profile. Preserve customized feature resources.
2. Run `retro issue setup` preview/application as described in
   [project upgrades](upgrading-projects.md#session-issue-retrospectives-in-0102),
   using this same reviewed environment. It installs/refreshes the retrospective,
   conversation/debugging/Help resources and actual entry/routing. Public 0.10.2
   shared bytes are recognized exactly; customized bytes still refuse. Setup does
   not activate debugging or a retrospective.
3. Run the exact preview/application snippet below, review its diff, then reread
   and reload the selected host instructions, actual skills and linked workflows.

New 0.10.3 notebooks receive the guidance at initialization. New legacy novels
receive the legacy 0.10.3 workflows at setup. Existing legacy novels use only the
normal external-controller updater selecting a newer stable published version.
Existing 0.10.2 legacy books select published `--version 0.10.3` in
the external-controller preview/application. Same-version source updates remain
unsupported; do not bypass the public version gate.

This bounded manual procedure refreshes six shared guides from exact supported
public snapshots or identical current resources and appends the existing bounded
session routing when absent. It adds no role, schema, runtime note validator or
host capability. Customized resources and unsupported markers fail safely; never
delete integration markers, reinitialize or convert a book to bypass refusal.

Pause notebook editing and inspect its Git status and selected `AGENTS.md` and/or
`CLAUDE.md`. Save the following **exact** snippet as `session-guidance-upgrade.py`
outside the notebook. With the notebook itself as the working directory, run
`python /absolute/path/session-guidance-upgrade.py preview`. Preview writes
nothing. Review the returned `changes`, package/resource location, `preview_id`
and `reviewed_head`, then run
`python /absolute/path/session-guidance-upgrade.py apply PREVIEW_ID REVIEWED_HEAD`.
Do not change the snippet between preview and apply. All inspected file hashes,
resource identities, selected host/language, index bytes and HEAD bind the review;
a changed input requires a fresh preview. A customized existing routing section,
unsafe path, unsupported format or unexpected public resource stops before writes.

```python
from importlib.resources import files
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
from novel_creator import __version__
from novel_creator.notebook import _host_text

# Frozen LF-normalized rendered resources from the public 0.10.0 wheel:
# novel_creator-0.10.0-py3-none-any.whl
# SHA256 097e9d093424a04fdf0d50fcfbc47c3ed7fd0e6d4d081167b3a78cda497ce4d6
PUBLIC_0100 = {
    "codex/project": {
        "agents.md": "90d4e085e1cafe85fd0911997c9baad6a35413c782804f4b4c8605c6a7364749",
        "character-development.md": "1c75c5b40a43ca73726904adc43020b5b31237d5cdc57740d432e2021c22313e",
        "conversation.md": "3c8447d48d1a0355193fa9288fa21107889adfc31cb1db99cc92e33820ca8066",
        "debugging.md": "082637983c394396bd0448b314c1892dabce7ccdb3f3a3af140ad377ace1cad2",
        "brainstorming.md": "bd22bd415261ee25dd27f8b298a7ece1e047bf22c9f9fae9db67bb27f543a5e4",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "codex/plugin": {
        "agents.md": "0fd3ceb3e611ab58be6ee77de378e97745ed56ee0054f5ac9791daaa67deba94",
        "character-development.md": "265d3dd87cebe06fb1791638c37a7aa8dbf204c371a807eefd1a0ccb181d9a67",
        "conversation.md": "8cf503cc7af3df2e4408c0a163a0e04c06824d9b73a2e31e4be31b9361358656",
        "debugging.md": "082637983c394396bd0448b314c1892dabce7ccdb3f3a3af140ad377ace1cad2",
        "brainstorming.md": "9de9b586fa6cd14b0851281e29c3f166ca7c5a3eb3bb4301b7ed3334f65d0bd2",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "claude/project": {
        "agents.md": "ba77d42938f8d7a3a8b3b2455639e173bc04afffb86c1533e79b9642e8725b59",
        "character-development.md": "c0721ca8b5c7525bd977e5f1bda62530b042e412baf98ec035948b21b4cb38c7",
        "conversation.md": "8966d22d44c6b7344f37b9871c16147980e0fa47c5ddb2385ecd8102d71422f2",
        "debugging.md": "f75990d434e77809839a951dc30d2fa6d3ac16e56f6b016888f00c2d5f8a3009",
        "brainstorming.md": "940254889612fcf2ba1c3d93a742f6f7555a1f6b76be731c341ce89b6c0929ea",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "claude/plugin": {
        "agents.md": "d20980ac2346fd4429bcf15f471a691266c9427304cc42e7760439b936ca290d",
        "character-development.md": "e3a916ee44b511d3aa92b5834b64ca3bc473f10c72380518d5b19c7ce6bac29b",
        "conversation.md": "f04a1c0fd300c63f2dec7777aee4a6d9b78a027705c69ec2aec7438848eae234",
        "debugging.md": "f75990d434e77809839a951dc30d2fa6d3ac16e56f6b016888f00c2d5f8a3009",
        "brainstorming.md": "80abd3a305e4381538a28984fa42ea7608b62ec57f523ff305ad668320bae785",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "both/project": {
        "agents.md": "a4395ca9c2821b578cdd5f5ade07f8389cdaecc857907df95a85becbadb41230",
        "character-development.md": "8f65cdeec8e490fd60ae7ba4a4924ac457644a54d4b362082e55215ef64e47e6",
        "conversation.md": "bd9d9a4293575544f080ebe49ee84024dc12a0ac00aabfa7141bdb41209e07b1",
        "debugging.md": "082637983c394396bd0448b314c1892dabce7ccdb3f3a3af140ad377ace1cad2",
        "brainstorming.md": "9ec8792dd8e4ac4352bdb7f11bf3f1fe09a29d509c9f2e1e9309d799c7aaebea",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "both/plugin": {
        "agents.md": "565373cccece9f2ec9558732b2e50ac33a0837c4a908073cc6093f52974a9599",
        "character-development.md": "315b5ca0931c41daacf568c89104405ec5405ddd2551c3b1464724c158090b5b",
        "conversation.md": "48e6dfcf686c377d9282241619b55a4dc47145977a5774cdf8cb4596fa6ed8bb",
        "debugging.md": "082637983c394396bd0448b314c1892dabce7ccdb3f3a3af140ad377ace1cad2",
        "brainstorming.md": "59f38eeb5e029010fcb8b1e8bf79a6e20736cbd8b26efb6b5b74974ead121b96",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    }
}

# Exact released 0.10.2 resources from immutable source commit
# 6259a15a73b7de93b7a0388feb90c451c6cf36b6 (resources match qualified
# source 9deeaa1cbbca6ad7c172b90687b698f5ae63b4f4). Offline fixtures
# preserve raw bytes; only LF/CRLF normalization is accepted.
PUBLIC_0102 = {
    "codex/project": {
        "conversation.md": "9be000952e7caf5edd9690ead66aadbe8ebc354cfeab63f7afed6fd7988090ac",
        "character-development.md": "594d3dcd788afa2b2b2dbe07667ce90f260739f6c1a1aeb6c2e9d1348b408eed",
        "debugging.md": "23b8ada16221ce4f08532529a79dcf6c705c436767e17855d5507f080db87388",
        "agents.md": "90d4e085e1cafe85fd0911997c9baad6a35413c782804f4b4c8605c6a7364749",
        "brainstorming.md": "166dd78e8b7ba638af3d83145ca397c71883c3bdcb2fbe61116138bc969e7e17",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "codex/plugin": {
        "conversation.md": "5b1bf354f929bc0adf72f3f893d11f1e0a77e81b485344d25dbdbc7182173236",
        "character-development.md": "442d18d79117da7da3765a4c6a18d9683043a4ba34771c24dca295ebf4fbde4a",
        "debugging.md": "23b8ada16221ce4f08532529a79dcf6c705c436767e17855d5507f080db87388",
        "agents.md": "0fd3ceb3e611ab58be6ee77de378e97745ed56ee0054f5ac9791daaa67deba94",
        "brainstorming.md": "1e96c37e86240ec22823d1dd51751be748c0080f4c2dbf21ffa8de8f267d3757",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "claude/project": {
        "conversation.md": "ffc4f995460960dcc393de8c33b63b6202c0acb264db23ffc843babdf69b840c",
        "character-development.md": "03214c14bfac35748836497ebaab530af168fad6da7132c120fbe42f7c3f40a7",
        "debugging.md": "150d8aa8c008b2a9b0dfa8962a7fca0410c9f8cdca06c81ab8e1463f77cd3859",
        "agents.md": "ba77d42938f8d7a3a8b3b2455639e173bc04afffb86c1533e79b9642e8725b59",
        "brainstorming.md": "756069a2f7bea7313bd2a28c3c4a408d9552fbb2f0257b8390428382b24c8d2c",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "claude/plugin": {
        "conversation.md": "1b0f27b5a133e65571b9d487d48611fc38fe0cef68e9d2440b1ff0d79eec6def",
        "character-development.md": "53ec3163592c34772da956a6f68df52c38e42c84f047822fbc1bdde164faf38e",
        "debugging.md": "150d8aa8c008b2a9b0dfa8962a7fca0410c9f8cdca06c81ab8e1463f77cd3859",
        "agents.md": "d20980ac2346fd4429bcf15f471a691266c9427304cc42e7760439b936ca290d",
        "brainstorming.md": "7b6cd0220e710301be5c6975a027a16581b0e0bacd5f1c9e93323b61cbce1191",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "both/project": {
        "conversation.md": "dfe01a61e53b9ec8a960714baea28719fc8eaa94a1491eafd10fe1f619c361cd",
        "character-development.md": "45b17499fed2f408fe0aedbd81d0482b4a4e41fb27dac3d014b1dd4dd104a630",
        "debugging.md": "23b8ada16221ce4f08532529a79dcf6c705c436767e17855d5507f080db87388",
        "agents.md": "a4395ca9c2821b578cdd5f5ade07f8389cdaecc857907df95a85becbadb41230",
        "brainstorming.md": "9eab890481471beaab251333b477b582a442ab470d778d11b0b63611059288ae",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    },
    "both/plugin": {
        "conversation.md": "99c6a23d2439bef32a6a59289c4d9cd392ee9667acca725fd6918357d624d2a2",
        "character-development.md": "9f1986534b825843811fabda0a606226dfa6428ad29c8c5d589f0f360aa37b15",
        "debugging.md": "23b8ada16221ce4f08532529a79dcf6c705c436767e17855d5507f080db87388",
        "agents.md": "565373cccece9f2ec9558732b2e50ac33a0837c4a908073cc6093f52974a9599",
        "brainstorming.md": "12de86cd6d367e417aafcdccb13b513db6b6ba7c1223b9c36aadbc1599a7d773",
        "format.md": "71f21b9e4daededf4385cfce2a987d83b0901b137d6d1ee09e60ea9f4740903b"
    }
}

def require(condition, message):
    if not condition:
        raise SystemExit(message + '; stop and reconcile without overwriting custom work.')

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def normalized(raw):
    return raw.decode('utf-8').replace('\r\n', '\n')

root = Path.cwd().absolute()  # Must be the intended notebook root.
inputs, identities = {}, {}

def regular(relative, required=True):
    path = root / relative
    require(path.resolve() == path and not any(
        p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction())
        for p in (path, *path.parents)), 'Redirected path: ' + relative)
    require(all(not p.exists() or p.is_dir() for p in path.parents),
            'Invalid parent: ' + relative)
    if path.exists():
        state = path.stat()
        require(path.is_file() and state.st_nlink == 1 and state.st_mode & 0o444,
                'Unsafe or unreadable file: ' + relative)
        identities[relative] = (state.st_dev, state.st_ino)
        raw = path.read_bytes()
    else:
        require(not required, 'Missing prerequisite: ' + relative)
        raw = None
    inputs[relative] = raw
    return raw

require(root.is_dir() and (root / '.git').is_dir(), 'Requires an independent Git notebook')
require(not (root / '.novel-creator').exists(), 'Legacy or mixed-format book is unsupported')
regular('.git/HEAD')
regular('.git/index')
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.fsmonitor=false', '-C', str(root),
                                    *args], env=env).decode().strip()

require(Path(git('rev-parse', '--show-toplevel')).resolve() == root and
        Path(git('rev-parse', '--absolute-git-dir')).resolve() == root / '.git',
        'Requires the selected local Git root')
head = git('rev-parse', '--verify', 'HEAD')
marker = regular('.novel-notebook/integration.json', False)
host, source = 'codex', 'project'
if marker is not None:
    integration = json.loads(marker)
    require(isinstance(integration, dict) and set(integration) ==
            {'version', 'host', 'skill_source'} and type(integration['version']) is int
            and integration['version'] == 1, 'Invalid integration marker')
    host, source = integration['host'], integration['skill_source']
require(host in ('codex', 'claude', 'both') and source in ('project', 'plugin'),
        'Unsupported host or skill source')
project = normalized(regular('notebook/project.md'))
envelope = re.match(r'\A(```|~~~)json\n(.*?)\n\1(?:\n|\Z)', project, re.S)
require(envelope is not None, 'Missing notebook metadata')
meta = json.loads(envelope[2])
require(isinstance(meta, dict) and type(meta.get('version')) is int and
        (meta.get('format'), meta.get('version'), meta.get('kind'), meta.get('id')) ==
        ('novel-notebook', 1, 'project', 'project'), 'Requires a format-1 notebook')
language = meta.get('language')
require(language in ('en', 'is'), 'Unsupported project language')
regular('notebook/working-summary.md')
regular('.novel-notebook/languages/' + language + '.md')
regular('.novel-notebook/workflows/side-character.md')
regular('.novel-notebook/workflows/retrospective.md')
shared = files('novel_creator.notebook_resources').joinpath('workflows')
planned, links = {}, {}
for name, approved in PUBLIC_0100[host + '/' + source].items():
    relative = '.novel-notebook/workflows/' + name
    original = regular(relative)
    desired = _host_text(shared.joinpath(name).read_text(encoding='utf-8'),
                         host, source).encode('utf-8')
    probes = {'conversation.md': 'An approved but unwritten change remains',
              'character-development.md': 'until its actual write to the owning',
              'debugging.md': 'recorded_sequences',
              'brainstorming.md': 'repeated',
              'format.md': 'coherent'}
    require(name not in probes or probes[name] in normalized(desired),
            'Selected package lacks revised session guidance: ' + name)
    require(normalized(original) == normalized(desired) or
            digest(normalized(original).encode('utf-8')) in
            (approved, PUBLIC_0102[host + '/' + source][name]),
            'Customized workflow: ' + relative)
    planned[relative] = original if normalized(original) == normalized(desired) else desired
    links[relative] = normalized(desired)

start = '<!-- novel-creator:session-guidance:start -->'
end = '<!-- novel-creator:session-guidance:end -->'
section = ("## Session guidance\n\n" + start + """
Follow the revised [conversation and save rules](.novel-notebook/workflows/conversation.md),
[character-development boundary](.novel-notebook/workflows/character-development.md)
and [role ownership](.novel-notebook/workflows/agents.md). These shared rules
clarify older general save wording: writer approval, verified file saves and
verified local Git checkpoints are distinct. Approved but unwritten work remains
unsaved; saved files can have a pending checkpoint. Keep character-development
drafts in chat until explicit save authority, including during a pending save.
Use the host's approved scoped access route when available for an authorized
checkpoint, preserving unrelated staging; otherwise disclose the limitation.
For a requested retrospective or active-session opt-in at explicit closure,
follow the [retrospective workflow](.novel-notebook/workflows/retrospective.md).
Stop known current debugging before review and keep it off. Exact outgoing
issue/attachment approval is required before sharing; no story save or commit.
""" + end + '\n').encode('utf-8')
for selected in (('codex', 'claude') if host == 'both' else (host,)):
    relative = 'AGENTS.md' if selected == 'codex' else 'CLAUDE.md'
    original = regular(relative)
    text = normalized(original)
    if start in text or end in text:
        require(text.count(start) == text.count(end) == 1 and
                normalized(section) in text, 'Customized session routing: ' + relative)
        planned[relative] = original
    else:
        planned[relative] = original + (b'\n' if original.endswith(b'\n') else b'\n\n') + section
    links[relative] = normalized(section)  # Existing custom root links are unrelated.

for relative, text in links.items():
    for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
            continue
        target = (root / relative).parent.joinpath(link).absolute()
        require(target.resolve().is_relative_to(root), 'Workflow link leaves notebook')
        # Resolve lexical .. for links, then inspect the destination and parents.
        linked = target.resolve().relative_to(root).as_posix()
        regular(linked)
changes = [name for name, raw in planned.items() if raw != inputs[name]]
for name in changes:
    require((root / name).stat().st_mode & 0o222, 'Unwritable destination: ' + name)
binding = dict(root=str(root), version=__version__, head=head, host=host, source=source,
               language=language, identities=identities,
               inputs={n: None if raw is None else digest(raw) for n, raw in inputs.items()},
               outputs={n: digest(raw) for n, raw in planned.items()})
preview = digest(json.dumps(binding, sort_keys=True, separators=(',', ':')).encode())
require(len(sys.argv) == 2 and sys.argv[1] == 'preview' or
        len(sys.argv) == 4 and sys.argv[1] == 'apply',
        'Usage: script.py preview OR script.py apply PREVIEW_ID REVIEWED_HEAD')
if sys.argv[1] == 'apply':
    require(sys.argv[2:] == [preview, head], 'Stale preview or changed HEAD')
    # Recheck every input before writing any file. Editing must remain paused.
    before = dict(inputs)
    before_ids = dict(identities)
    for name, raw in before.items():
        require(regular(name, raw is not None) == raw and
                identities.get(name) == before_ids.get(name), 'Changed input: ' + name)
    require(git('rev-parse', '--verify', 'HEAD') == head, 'Changed HEAD')
    for name in changes:
        require(regular(name) == before[name] and identities[name] == before_ids[name]
                and git('rev-parse', '--verify', 'HEAD') == head, 'Changed during apply: ' + name)
        (root / name).write_bytes(planned[name])
        require(regular(name) == planned[name], 'Write verification failed: ' + name)
print(json.dumps(dict(package_version=__version__, resources=str(shared), changes=changes,
                     preview_id=preview, reviewed_head=head, applied=sys.argv[1] == 'apply')))

```

Review the diff: only those six workflows (conversation, character-development,
debugging, agents, brainstorming and format) and appended selected root routing
sections may change. Story files, summaries, existing custom root bytes, project
skills, roles, history and unrelated staging stay intact. No commit or push is
made. A repeated preview/apply with current identical resources is harmless.
This is manual maintenance, not a cross-file transaction or a concurrent editor
lock: on interruption or write failure, inspect actual files and preserve partial
work, then reconcile and take a fresh preview. Do not claim partial delivery ready.

Have the host reread the selected root instructions and shared workflows. Inspect
actual project skill files and their workflow links, or actual enabled plugin
entries. Use the host's supported reload/reopen controls, possibly a new chat;
there is no universal reload command. Filesystem checks do not establish native
skill discovery, reload, observed voice behavior or subjective writing quality.
Unsaved chat drafts have no guaranteed recovery in a new chat. For an optional
local checkpoint, use the existing exact-path Git guidance and preserve unrelated
staged writer edits.
