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
GUIDES = ('conversation.md', 'character-development.md', 'debugging.md', 'agents.md')


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


def exercise(python, book, expected, env, *, host, source):
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
    # All four workflows, including an otherwise-identical guide, are protected.
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
    require(changed <= allowed and set(roots) <= changed, 'Unexpected delivery changes')
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
