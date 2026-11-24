"""Execute the exact documented procedure on disposable public/synthetic books."""
import json
import os
from pathlib import Path
import re

try:
    from tests.verify_plugin_install import require, run, snapshot
except ModuleNotFoundError:
    from verify_plugin_install import require, run, snapshot

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ('conversation.md', 'character-development.md', 'debugging.md', 'agents.md',
          'brainstorming.md', 'format.md')


def procedure():
    doc = (ROOT / 'docs/session-guidance-upgrade.md').read_text(encoding='utf-8')
    snippets = re.findall(r'```python\n(.*?)\n```', doc, re.S)
    require(len(snippets) == 1, 'Exercise the exact documented procedure')
    return snippets[0]


def check_links(book):
    for directory in ('.agents/skills', '.claude/skills', '.codex/agents', '.claude/agents'):
        for path in (book / directory).rglob('*'):
            if not path.is_file():
                continue
            for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text(encoding='utf-8')):
                if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                    require((path.parent / link).resolve().is_relative_to(book) and
                            (path.parent / link).is_file(), 'Unresolved skill/role link: ' + str(path))


def prepare_retro(python, book, expected, env, *, host, source, expected_changes=None):
    """Actual CLI prerequisite with writer state present before the first preview."""
    try:
        from tests.feature_upgrade_checks import check_features, feature_paths
    except ModuleNotFoundError:
        from feature_upgrade_checks import check_features, feature_paths
    roots = ('AGENTS.md', 'CLAUDE.md') if host == 'both' else (
        'AGENTS.md' if host == 'codex' else 'CLAUDE.md',)
    root_bytes = {}
    for name in roots:
        path = book / name
        path.write_bytes(path.read_bytes() + b'\n## Before prerequisite\nPreserve exact writer directions.\n')
        root_bytes[name] = path.read_bytes()
    (book / 'notebook/prerequisite-writer.md').write_bytes(b'Accepted before prerequisite.\n')
    staged = book / 'prerequisite-staging.txt'
    staged.write_bytes(b'Staged before prerequisite\n')
    run(['git', '-C', book, 'add', '--', staged.name], env=env, cwd=book.parent)
    staged.write_bytes(b'Unstaged before prerequisite\n')
    before = snapshot(book)
    index = (book / '.git/index').read_bytes()
    head = run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=book.parent)
    command = [python, '-I', '-B', '-m', 'novel_creator', 'retro', 'issue', 'setup', '--novel', book]

    def preview():
        return json.loads(run([*command, '--json'], env=env, cwd=book.parent))['data']

    review = preview()
    conversation = '.novel-notebook/workflows/conversation.md'
    if expected_changes is not None:
        require(sorted(review['changes']) == sorted(expected_changes),
                'Unexpected issue-setup preview paths: ' + str(review['changes']))
    require(snapshot(book) == before, 'Retro prerequisite preview wrote files')
    path = book / roots[0]
    raw = path.read_bytes()
    path.write_bytes(raw + b'Late writer edit.\n')
    changed = snapshot(book)
    run([*command, '--apply', '--preview', review['preview_id'], '--expected-head',
         review['reviewed_head'], '--json'], env=env, cwd=book.parent, expected_exit=3)
    require(snapshot(book) == changed, 'Stale prerequisite mutated files')
    path.write_bytes(raw)
    custom_resource = (conversation if expected_changes == {conversation}
                       else '.novel-notebook/workflows/retrospective.md')
    path = book / custom_resource
    raw = path.read_bytes()
    path.write_bytes(raw + b'Custom retrospective.\n')
    changed = snapshot(book)
    conflict = preview()
    require(conflict['conflicts'] == [{'path': custom_resource, 'replacement':
            (expected / custom_resource).read_text(encoding='utf-8')}]
            and custom_resource not in conflict['changes'] and not conflict['ready']
            and not conflict['already_current'], 'Customized workflow conflict preview mismatch')
    require(snapshot(book) == changed, 'Custom prerequisite preview mutated files')
    run([*command, '--apply', '--preview', conflict['preview_id'], '--expected-head',
         conflict['reviewed_head'], '--json'], env=env, cwd=book.parent, expected_exit=3)
    require(snapshot(book) == changed, 'Custom prerequisite apply mutated files')
    path.write_bytes(raw)
    outside = book.parent / (book.name + '-retro-hardlink.md')
    outside.write_bytes(raw)
    path.unlink()
    os.link(outside, path)
    changed = snapshot(book)
    try:
        run([*command, '--json'], env=env, cwd=book.parent, expected_exit=3)
        require(snapshot(book) == changed and outside.read_bytes() == raw,
                'Unsafe prerequisite path changed files')
    finally:
        path.unlink()
        path.write_bytes(raw)
    review = preview()
    applied = json.loads(run([*command, '--apply', '--preview', review['preview_id'],
        '--expected-head', review['reviewed_head'], '--json'], env=env, cwd=book.parent))['data']
    require(applied['applied'], 'Prerequisite application failed')
    after = snapshot(book)
    allowed = set(roots) | feature_paths(host, source, 'retrospective') | {
        '.novel-notebook/workflows/' + name + '.md' for name in ('help', 'conversation', 'debugging')}
    changed = {n for n in before.keys() | after.keys() if before.get(n) != after.get(n)}
    if expected_changes is not None:
        require(changed == expected_changes, 'Unexpected issue-setup changes: ' + str(sorted(changed)))
    require(changed <= allowed,
            'Prerequisite changed writer files')
    pattern = rb'<!-- novel-creator:issue-retro:start -->.*?<!-- novel-creator:issue-retro:end -->'
    for name in roots:
        original = root_bytes[name]
        old_block = re.search(pattern, original, re.S)
        updated = (book / name).read_bytes()
        if old_block:
            fresh = re.search(pattern, (expected / name).read_bytes(), re.S)
            require(fresh is not None, 'New notebook lacks issue routing')
            require(updated == original.replace(old_block.group(), fresh.group(), 1),
                    'Issue setup changed bytes outside the managed retrospective routing')
        else:
            require(updated.startswith(original), 'Prerequisite changed custom root')
    require((book / '.git/index').read_bytes() == index, 'Prerequisite changed raw index')
    require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=book.parent) == head,
            'Prerequisite changed history')
    check_features(book, expected, host=host, source=source)
    repeated = preview()
    require(repeated['already_current'], 'Prerequisite retry not current')
    require(snapshot(book) == after, 'Prerequisite retry wrote files')
    return before, after, index, head


def exercise(python, book, expected, env, *, host, source, prepared=False):
    """Preview/apply, exact resources, refusals and byte preservation."""
    hosts = ('codex', 'claude') if host == 'both' else (host,)
    roots = ['AGENTS.md' if h == 'codex' else 'CLAUDE.md' for h in hosts]
    for name in roots:
        fresh = (expected / name).read_bytes()
        require(b'novel-creator:issue-retro:start' in fresh and b'approved but unwritten' in fresh,
                'New notebook root lacks explicit local-review/save-state routing')
    for name in roots:
        path = book / name
        path.write_bytes(path.read_bytes() + b'\r\n## Custom writer direction\r\nKeep my exact bytes.\r\n')
    (book / 'notebook/writer-preserved.md').write_bytes(b'Synthetic accepted writer text.\n')
    if not prepared:
        staged = book / 'writer-staging.txt'
        staged.write_bytes(b'Staged writer bytes\n')
        run(['git', '-C', book, 'add', '--', staged.name], env=env, cwd=book.parent)
        staged.write_bytes(b'Unstaged writer bytes\n')
    before = snapshot(book)
    root_bytes = {n: (book / n).read_bytes() for n in roots}
    index = (book / '.git/index').read_bytes()
    head = run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=book.parent)
    command = [python, '-I', '-B', '-c', procedure()]

    def preview():
        return json.loads(run([*command, 'preview'], env=env, cwd=book))

    review = preview()
    require(snapshot(book) == before, 'Preview wrote notebook files')
    # Root edits after preview and explicit HEAD mismatches must refuse all writes.
    path = book / roots[0]
    raw = path.read_bytes()
    path.write_bytes(raw + b'Late writer edit.\n')
    changed = snapshot(book)
    run([*command, 'apply', review['preview_id'], review['reviewed_head']],
        env=env, cwd=book, expected_exit=1)
    require(snapshot(book) == changed, 'Stale preview mutated files')
    path.write_bytes(raw)
    run([*command, 'apply', review['preview_id'], '0' * 40], env=env, cwd=book, expected_exit=1)
    require(snapshot(book) == before, 'Changed HEAD argument mutated files')
    # All six workflows, including an otherwise-identical guide, are protected.
    for name in GUIDES:
        path = book / '.novel-notebook/workflows' / name
        raw = path.read_bytes()
        path.write_bytes(raw + b'Custom workflow direction.\n')
        changed = snapshot(book)
        run([*command, 'preview'], env=env, cwd=book, expected_exit=1)
        require(snapshot(book) == changed, 'Customized guide changed')
        path.write_bytes(raw)
    path = book / '.novel-notebook/workflows/conversation.md'
    raw = path.read_bytes()
    outside = book.parent / (book.name + '-hardlink.md')
    outside.write_bytes(raw)
    path.unlink()
    os.link(outside, path)
    changed = snapshot(book)
    try:
        run([*command, 'preview'], env=env, cwd=book, expected_exit=1)
        require(snapshot(book) == changed and outside.read_bytes() == raw, 'Hardlink changed')
    finally:
        path.unlink()
        path.write_bytes(raw)
    # Restoring a file changes its identity; take a new explicit review.
    review = preview()
    result = json.loads(run([*command, 'apply', review['preview_id'], review['reviewed_head']],
                            env=env, cwd=book))
    require(result['applied'], 'Explicit application failed')
    after = snapshot(book)
    allowed = set(roots) | {'.novel-notebook/workflows/' + n for n in GUIDES}
    changed = {n for n in before.keys() | after.keys() if before.get(n) != after.get(n)}
    require(changed <= allowed, 'Unexpected delivery changes')
    for name in GUIDES:
        relative = '.novel-notebook/workflows/' + name
        require((book / relative).read_bytes().replace(b'\r\n', b'\n') ==
                (expected / relative).read_bytes().replace(b'\r\n', b'\n'), 'Wrong rendered workflow')
    for name in roots:
        raw = (book / name).read_bytes()
        require(raw.startswith(root_bytes[name]) and raw.count(b'novel-creator:session-guidance:start') == 1,
                'Custom root bytes or bounded routing lost')
        require(b'approved but unwritten' in raw.lower() and b'novel-creator:issue-retro:start' in raw,
                'Save-state/local-retro routing missing')
    check_links(book)
    if source == 'plugin':
        require(not (book / '.agents/skills').exists() and not (book / '.claude/skills').exists(),
                'Duplicated plugin skills')
    else:
        for h in hosts:
            directory = '.agents' if h == 'codex' else '.claude'
            require((book / directory / 'skills/novel-character-develop/SKILL.md').is_file(),
                    'Actual installed character-development entry missing')
    review = preview()
    require(review['changes'] == [], 'Repeated preview not current')
    run([*command, 'apply', review['preview_id'], review['reviewed_head']], env=env, cwd=book)
    require(snapshot(book) == after, 'Identical retry changed files')
    require((book / '.git/index').read_bytes() == index, 'Delivery altered staging')
    require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=book.parent) == head,
            'Delivery altered history')
    return dict(preview_apply=True, exact_rendered_workflows=True, skill_and_role_links=True,
                customized_stale_hardlink_refused=True,
                story_root_skills_roles_index_history_preserved=True)
