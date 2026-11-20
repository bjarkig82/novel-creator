"""Installed-artifact feature delivery checks; disposable books only."""
from importlib.resources import files
import os
from pathlib import Path
import re
from types import SimpleNamespace

try:
    from tests.verify_plugin_install import require, run, snapshot
    from tests.session_guidance_checks import check_links
except ModuleNotFoundError:
    from verify_plugin_install import require, run, snapshot
    from session_guidance_checks import check_links


def feature_paths(host, source, feature):
    hosts = ('codex', 'claude') if host == 'both' else (host,)
    paths = {'.novel-notebook/workflows/' + feature + '.md'}
    if source == 'project':
        skill = 'novel-side-character' if feature == 'side-character' else 'novel-retro'
        paths |= {('.agents' if h == 'codex' else '.claude') + '/skills/' + skill + '/SKILL.md'
                  for h in hosts}
    return paths


def check_features(book, expected, *, host, source):
    """Exact rendered workflows/skills and root blocks, with actual local links."""
    roots = ('AGENTS.md', 'CLAUDE.md') if host == 'both' else (
        'AGENTS.md' if host == 'codex' else 'CLAUDE.md',)
    paths = feature_paths(host, source, 'side-character') | feature_paths(host, source, 'retrospective')
    paths |= {'.novel-notebook/workflows/' + n + '.md' for n in ('help', 'conversation', 'debugging')}
    for name in paths:
        require((book / name).read_bytes().replace(b'\r\n', b'\n') ==
                (expected / name).read_bytes().replace(b'\r\n', b'\n'), 'Wrong feature bytes: ' + name)
    for name in roots:
        for marker in ('side-character', 'issue-retro'):
            pattern = ('<!-- novel-creator:' + marker + ':start -->.*?<!-- novel-creator:' + marker + ':end -->').encode()
            actual = re.search(pattern, (book / name).read_bytes(), re.S)
            fresh = re.search(pattern, (expected / name).read_bytes(), re.S)
            require(actual is not None and fresh is not None and actual.group() == fresh.group(),
                    'Wrong feature routing: ' + name + ' / ' + marker)
    workflow = (book / '.novel-notebook/workflows/side-character.md').read_bytes()
    require(b'chat-only' in workflow and b'approval' in workflow.lower(), 'Draft boundary missing')
    retro = (book / '.novel-notebook/workflows/retrospective.md').read_bytes()
    require(b'opt-in' in retro and b'approval' in retro.lower(), 'Retro consent boundary missing')
    check_links(book)
    # Check root and workflow links too, including routing outside the new blocks.
    for name in set(roots) | paths:
        path = book / name
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text(encoding='utf-8')):
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                target = (path.parent / link).resolve()
                require(target.is_relative_to(book) and target.is_file(), 'Unresolved feature/root link: ' + name)
    if source == 'plugin':
        require(not (book / '.agents/skills').exists() and not (book / '.claude/skills').exists(),
                'Plugin setup duplicated project skills')


def exercise(python, book, expected, env, *, host, source, default=False):
    from novel_creator import notebook, notebook_side_character, retro_issue_setup
    from novel_creator.cli import ToolError
    roots = ('AGENTS.md', 'CLAUDE.md') if host == 'both' else (
        'AGENTS.md' if host == 'codex' else 'CLAUDE.md',)
    for name in roots:
        with (book / name).open('ab') as stream:
            stream.write(b'\n## Writer directions\nKeep my exact custom writer bytes.\n')
    (book / 'notebook/writer-preserved.md').write_bytes(b'Synthetic accepted text.\n')
    staged = book / 'writer-staging.txt'
    staged.write_bytes(b'Staged writer text\n')
    run(['git', '-C', book, 'add', '--', staged.name], env=env, cwd=book.parent)
    staged.write_bytes(b'Unstaged writer text\n')
    before = snapshot(book)
    index = (book / '.git/index').read_bytes()
    head = run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=book.parent)
    root_bytes = {name: (book / name).read_bytes() for name in roots}

    def side(review=None):
        helper = notebook if default else notebook_side_character
        return helper.update(book, apply=review is not None,
                             preview_id=None if review is None else review['preview_id'],
                             expected_head=None if review is None else review['reviewed_head'])['data']

    def retro(review=None):
        return retro_issue_setup.setup(SimpleNamespace(novel=book, apply=review is not None,
            preview=None if review is None else review['preview_id'],
            expected_head=None if review is None else review['reviewed_head']))

    def refuses(call):
        state = snapshot(book)
        try:
            call()
        except ToolError as error:
            require(error.code == 3, 'Unexpected refusal code')
        else:
            raise AssertionError('Unsafe/customized/stale feature setup was accepted')
        require(snapshot(book) == state, 'Refusal changed book bytes')

    for name, helper, resource in (
            ('side-character', side, '.novel-notebook/workflows/side-character.md'),
            ('retrospective', retro, '.novel-notebook/workflows/conversation.md')):
        state = snapshot(book)
        review = helper()
        require(snapshot(book) == state, 'Feature preview changed files')
        path = book / resource
        raw = path.read_bytes() if path.exists() else None
        path.write_bytes((raw or b'') + b'Writer customized resource.\n')
        refuses(helper)
        if raw is None:
            path.unlink()
        else:
            path.write_bytes(raw)
        root = book / roots[0]
        original = root.read_bytes()
        review = helper()
        root.write_bytes(original + b'Late writer edit.\n')
        refuses(lambda: helper(review))
        root.write_bytes(original)
        outside = book.parent / (book.name + '-' + name + '-outside.md')
        outside.write_bytes(original)
        root.unlink()
        os.link(outside, root)
        try:
            refuses(helper)
            require(outside.read_bytes() == original, 'Refusal changed linked outside bytes')
        finally:
            root.unlink()
            root.write_bytes(original)
        review = helper()
        result = helper(review)
        require(result['applied'], 'Reviewed feature setup did not apply')
        after = snapshot(book)
        changed = {p for p in state.keys() | after.keys() if state.get(p) != after.get(p)}
        expected_paths = set(roots) | feature_paths(host, source, name)
        if name == 'side-character' and default:
            # Public 0.10.1 has current character guidance; default setup also
            # refreshes help and adds the absent passive retro prerequisite.
            expected_paths |= {'.novel-notebook/workflows/retrospective.md',
                               '.novel-notebook/workflows/help.md'}
        if name == 'retrospective':
            expected_paths |= {'.gitignore', '.novel-notebook/workflows/conversation.md',
                               '.novel-notebook/workflows/help.md', '.novel-notebook/workflows/debugging.md'}
            # Compare only this explicit feature inventory with fresh installed
            # rendering; never derive an allowlist from the update's output.
            fresh = snapshot(expected)
            expected_paths = {p for p in expected_paths if state.get(p) != fresh.get(p)}
        require(changed == expected_paths, 'Unexpected ' + name + ' delivery: ' + str(sorted(changed)))
        current = helper()
        require(current['already_current'], 'Feature retry did not report current')
        helper(current)
        require(snapshot(book) == after, 'Current feature apply changed bytes')
    for name, value in before.items():
        if name not in roots and not name.startswith(('.novel-notebook/workflows/', '.agents/skills/', '.claude/skills/')) and name != '.gitignore':
            require(snapshot(book)[name] == value, 'Writer/integration/role bytes changed: ' + name)
    from novel_creator.retro_issue_setup import OLD_ROOT
    for name in roots:
        # Only the exact shipped obsolete paragraph is replaced by retro setup.
        preserved = root_bytes[name].replace(OLD_ROOT.encode(), b'')
        require((book / name).read_bytes().startswith(preserved), 'Custom root bytes changed')
    require((book / '.git/index').read_bytes() == index, 'Feature setup changed staging')
    require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=book.parent) == head,
            'Feature setup changed history')
    check_features(book, expected, host=host, source=source)
    check_features(expected, expected, host=host, source=source)
    return dict(new_notebook=True, previous_public='0.10.1',
                default_updater=default, feature_only_side_helper=not default,
                issue_setup=True, exact_resources_root_and_links=True,
                modified_stale_hardlink_refused=True, current_noop=True,
                writer_history_custom_roots_staging_integration_preserved=True)


def check_legacy_routing(book, *, fresh_root=False):
    """Fresh roots and managed entries must use the installed legacy routing."""
    resources = {'.novel-creator/workflows/entry.md':
                 files('novel_creator.workflows').joinpath('entry.md').read_bytes().replace(b'\r\n', b'\n')}
    if fresh_root:
        resources['AGENTS.md'] = files('novel_creator.codex').joinpath('AGENTS.production.md').read_bytes()
    for name, expected in resources.items():
        path = book / name
        require(path.read_bytes() == expected, 'Wrong legacy routing bytes: ' + name)
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text(encoding='utf-8')):
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                target = (path.parent / link).resolve()
                require(target.is_relative_to(book) and target.is_file(), 'Unresolved legacy routing link: ' + name)


def check_legacy_features(book, *, fresh_root=False):
    """Managed legacy delivery; notebook save/setup modules stay external."""
    for feature, skill in (('side-character', 'novel-side-character'), ('retrospective', 'novel-retro')):
        workflow = book / '.novel-creator/workflows' / (feature + '.md')
        entry = book / '.agents/skills' / skill / 'SKILL.md'
        require(workflow.read_bytes() == files('novel_creator.workflows').joinpath(feature + '.md').read_bytes(),
                'Wrong legacy feature workflow bytes')
        require(entry.read_bytes() == files('novel_creator.codex').joinpath('skills', skill, 'SKILL.md').read_bytes(),
                'Wrong legacy feature skill bytes')
    for module in ('notebook.py', 'notebook_side_character.py'):
        require(not (book / '.novel-creator/src/novel_creator' / module).exists(),
                'Notebook-only runtime copied into legacy novel')
    check_links(book)
    check_legacy_routing(book, fresh_root=fresh_root)


def check_legacy_continuity(book, *, fresh_root=False):
    check_legacy_features(book, fresh_root=fresh_root)
    for name, phrase in (('brainstorm.md', b'Keep knowledge and practical leverage distinct.'),
                         ('resume.md', b'[brainstorming guidance](brainstorm.md)')):
        expected = files('novel_creator.workflows').joinpath(name).read_bytes().replace(b'\r\n', b'\n')
        actual = (book / '.novel-creator/workflows' / name).read_bytes().replace(b'\r\n', b'\n')
        require(actual == expected and phrase in actual, 'Wrong legacy continuity guide: ' + name)


def check_legacy_retro_refresh(book):
    """Verify the revised legacy workflows installed by setup or update."""
    for name in ('debugging.md', 'help.md', 'retrospective.md'):
        expected = files('novel_creator.workflows').joinpath(name).read_bytes().replace(b'\r\n', b'\n')
        actual = (book / '.novel-creator/workflows' / name).read_bytes().replace(b'\r\n', b'\n')
        require(actual == expected, 'Wrong installed legacy workflow: ' + name)
    retrospective = (book / '.novel-creator/workflows/retrospective.md').read_bytes()
    require(b'--keep-debugging' in retrospective and b'GitHub issue candidate in the first reply' in retrospective,
            'Legacy retrospective lacks live snapshot or local candidate guidance')
