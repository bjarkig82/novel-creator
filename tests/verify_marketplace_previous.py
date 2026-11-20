"""Opt-in public notebook upgrade checks against a locally installed candidate.

Downloads the frozen public previous wheel unless --previous-wheel is supplied.
All installations, books and Git identities are disposable process-local state.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import tempfile
import urllib.request
from urllib.parse import urlparse
from packaging.version import Version

try:
    from tests.verify_plugin_install import bootstrap, require, run, snapshot, temporary_environment, write_report
    from tests.verify_previous_release import check_target_inventory
except ModuleNotFoundError:
    from verify_previous_release import check_target_inventory
    from verify_plugin_install import bootstrap, require, run, snapshot, temporary_environment, write_report


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_VERSION = '0.7.2'
PREVIOUS_FILENAME = 'novel_creator-0.7.2-py3-none-any.whl'
PREVIOUS_SHA256 = '8ee343c10bfcc8129d860a8502c669856deaa92f62b5059f915a4027fc11c9f5'
PUBLIC_WHEELS = {
    '0.7.2': (PREVIOUS_FILENAME, PREVIOUS_SHA256),
    '0.8.0': ('novel_creator-0.8.0-py3-none-any.whl',
              '390c6e208fe71a803783cd2cf979bada3e20988518a0032572fcf9a1b8711c5b'),
    '0.10.0': ('novel_creator-0.10.0-py3-none-any.whl',
               '097e9d093424a04fdf0d50fcfbc47c3ed7fd0e6d4d081167b3a78cda497ce4d6'),
    '0.9.0': ('novel_creator-0.9.0-py3-none-any.whl',
              '59050772544faa3056fa173f06c7c410e5f07e352fdad38d41bf88185e86667f'),
    '0.10.4': ('novel_creator-0.10.4-py3-none-any.whl',
               'dc5988f53929ae2783169408fcab35e21305123434b305735a6ea6e38bf2bad3'),
    '0.10.3': ('novel_creator-0.10.3-py3-none-any.whl',
               'c29f36dad95f8289a9a2b19d0d0fe3246d8a6c2c2d2860bd736c2b981c6629f9'),
    '0.10.2': ('novel_creator-0.10.2-py3-none-any.whl',
               '24117c4c17c7a56a981edbf1852440bbca94f668ea4f4fdf9aef4b940a000659'),
    '0.10.1': ('novel_creator-0.10.1-py3-none-any.whl',
               '6721c5a527f1b7e567743f2760ec5e13aec2d0394f520913e98589ac54b8b11a'),
}


def default_update_inventory(target_version, source_version, before):
    """Explicit feature inventory, retaining the historical target contract."""
    changed = {'AGENTS.md'}
    if Version(source_version) < Version('0.9.0'):
        changed |= {'.agents/skills/novel-character-develop/SKILL.md',
                    '.novel-notebook/workflows/character-development.md',
                    '.novel-notebook/workflows/help.md'}
    elif Version(source_version) < Version('0.10.1'):
        changed.add('.novel-notebook/workflows/character-development.md')
    if Version(target_version) >= Version('0.10.2'):
        changed |= {'.agents/skills/novel-side-character/SKILL.md',
                    '.novel-notebook/workflows/side-character.md',
                    '.novel-notebook/workflows/help.md'}
        # The default updater only supplies absent passive prerequisites.
        relative = '.novel-notebook/workflows/retrospective.md'
        if relative not in before:
            changed.add(relative)
    return changed


def check_default_delivery(book, expected, changed):
    """Verify actual changed resource bytes and bounded new feature routing."""
    for name in changed - {'AGENTS.md'}:
        require((book / name).read_bytes().replace(b'\r\n', b'\n') ==
                (expected / name).read_bytes().replace(b'\r\n', b'\n'),
                'Wrong default-update resource bytes: ' + name)
    root = (book / 'AGENTS.md').read_bytes()
    if '.novel-notebook/workflows/side-character.md' in changed:
        pattern = rb'<!-- novel-creator:side-character:start -->.*?<!-- novel-creator:side-character:end -->'
        actual = re.search(pattern, root, re.S)
        fresh = re.search(pattern, (expected / 'AGENTS.md').read_bytes(), re.S)
        require(actual is not None and fresh is not None and actual.group() == fresh.group(),
                'Wrong bounded side-character root routing')
        workflow = (book / '.novel-notebook/workflows/side-character.md').read_bytes()
        require(b'chat-only' in workflow and b'approval' in workflow.lower(),
                'Side-character draft/save boundary missing')
    try:
        from tests.session_guidance_checks import check_links
    except ModuleNotFoundError:
        from session_guidance_checks import check_links
    check_links(book)


def previous_wheel(scratch, supplied=None, *, version=PREVIOUS_VERSION):
    filename, digest = PUBLIC_WHEELS[version]
    if supplied is not None:
        path = supplied.resolve()
        raw = path.read_bytes()
    else:
        with urllib.request.urlopen(f'https://pypi.org/pypi/novel-creator/{version}/json',
                                    timeout=30) as response:
            metadata = json.load(response)
        entries = [entry for entry in metadata['urls']
                   if entry['packagetype'] == 'bdist_wheel' and entry['filename'] == filename]
        require(len(entries) == 1, 'Expected exactly one frozen previous-release wheel')
        entry = entries[0]
        require(entry['digests']['sha256'] == digest, 'Public wheel identity changed')
        url = urlparse(entry['url'])
        require(url.scheme == 'https' and url.hostname == 'files.pythonhosted.org',
                'Unexpected previous-wheel download origin')
        with urllib.request.urlopen(entry['url'], timeout=60) as response:
            raw = response.read()
        path = scratch / filename
        path.write_bytes(raw)
    require(hashlib.sha256(raw).hexdigest() == digest, 'Previous wheel SHA-256 mismatch')
    return path


def candidate_runtime(plugin, wheel, scratch, env, *, sdist=None):
    """Disposable installed candidate; shared by manual host-layout probes."""
    runtime = bootstrap(plugin, wheel, scratch, env)
    if sdist is not None:
        run([runtime['runtime_python'], '-I', '-m', 'pip', 'install', '--no-input',
             '--disable-pip-version-check', '--no-deps', '--no-user', '--no-cache-dir',
             '--force-reinstall', sdist], env=dict(env, PIP_CONFIG_FILE=os.devnull), cwd=scratch)
    runtime['verified_product_files'] = check_target_inventory(
        runtime['runtime_python'], wheel, runtime['version'], cwd=scratch, env=env)
    return runtime


def install_previous(python, scratch, env, *, version, supplied=None):
    """Hash-verify and privately install a frozen public notebook initializer."""
    old_wheel = previous_wheel(scratch, supplied, version=version)
    old_product = scratch / ('old-product-' + version)
    run([python, '-I', '-m', 'pip', 'install', '--no-input', '--disable-pip-version-check',
         '--no-deps', '--no-user', '--target', old_product, old_wheel],
        env=dict(env, PIP_CONFIG_FILE=os.devnull), cwd=scratch)
    old_cli = ('import sys;sys.path.insert(0,sys.argv[1]);import novel_creator;'
               f'assert novel_creator.__version__ == {version!r};'
               'from novel_creator.cli import main;raise SystemExit(main(sys.argv[2:]))')
    return old_product, old_cli


def verify(*, plugin, wheel, previous=None, source_version=PREVIOUS_VERSION, sdist=None):
    with tempfile.TemporaryDirectory(prefix='novel-marketplace-previous-') as temporary:
        scratch = Path(temporary).resolve()
        env = temporary_environment(scratch)
        runtime = candidate_runtime(plugin, wheel, scratch, env, sdist=sdist)
        python = runtime['runtime_python']
        old_product, old_cli = install_previous(python, scratch, env,
                                               version=source_version, supplied=previous)
        if source_version == '0.10.1':
            source = previous_wheel(scratch, previous or (scratch / PUBLIC_WHEELS[source_version][0]),
                                    version=source_version)
            return {'ok': True, 'source_sha256': PUBLIC_WHEELS[source_version][1],
                    'verified_product_files': runtime['verified_product_files'],
                    'candidate_artifact': 'sdist' if sdist else 'wheel',
                    'candidate_artifact_sha256': hashlib.sha256((sdist or wheel).read_bytes()).hexdigest(),
                    'candidate_wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
                    'notebooks': verify_feature_upgrade(python, old_product, old_cli, scratch, env),
                    'legacy': verify_debug_legacy(python, source, wheel, scratch, env, runtime['version'],
                                                  source_version=source_version)}
        if source_version in ('0.10.0', '0.10.2', '0.10.3', '0.10.4'):
            source = previous_wheel(scratch, previous or (scratch / PUBLIC_WHEELS[source_version][0]),
                                    version=source_version)
            return {'ok': True, 'source_sha256': PUBLIC_WHEELS[source_version][1],
                    'verified_product_files': runtime['verified_product_files'],
                    'candidate_artifact': 'sdist' if sdist else 'wheel',
                    'candidate_artifact_sha256': hashlib.sha256((sdist or wheel).read_bytes()).hexdigest(),
                    'candidate_wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
                    'notebooks': verify_session_upgrade(python, old_product, old_cli, scratch, env,
                                                        source_version=source_version),
                    'legacy': verify_debug_legacy(python, source, wheel, scratch, env, runtime['version'],
                                                  source_version=source_version)}
        if source_version == '0.9.0':
            source = previous_wheel(scratch, previous or (scratch / PUBLIC_WHEELS[source_version][0]),
                                    version=source_version)
            return {'ok': True, 'source_sha256': PUBLIC_WHEELS[source_version][1],
                    'verified_product_files': runtime['verified_product_files'],
                    'candidate_artifact': 'sdist' if sdist else 'wheel',
                    'candidate_artifact_sha256': hashlib.sha256((sdist or wheel).read_bytes()).hexdigest(),
                    'candidate_wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
                    'notebooks': verify_debug_upgrade(python, old_product, old_cli, scratch, env,
                                                      target_version=runtime['version']),
                    'legacy': verify_debug_legacy(python, source, wheel, scratch, env, runtime['version'])}
        cases = []
        for language in ('en', 'is'):
            book = scratch / f'Book {language}'
            created = json.loads(run([python, '-I', '-B', '-c', old_cli, old_product, 'notebook',
                                      'init', book.name, '--path', book, '--language', language, '--json'],
                                     env=env, cwd=scratch))
            require(created.get('ok') and created['data']['ready'], f'Previous notebook not ready: {created}')
            instructions = (book / 'AGENTS.md').read_bytes() + b'\n## Writer directions\nPreserve this custom writer direction.\n'
            (book / 'AGENTS.md').write_bytes(instructions)
            (book / 'notebook/writer-preserved.md').write_text('Accepted writer text.\n', encoding='utf-8')
            staged = book / 'writer-staging.txt'
            staged.write_text('Staged version\n', encoding='utf-8')
            run(['git', '-C', book, 'add', 'writer-staging.txt'], env=env, cwd=scratch)
            staged.write_text('Unstaged version\n', encoding='utf-8')
            before = snapshot(book)
            head = run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch)
            index = (book / '.git/index').read_bytes()
            command = [python, '-I', '-m', 'novel_creator', 'notebook', 'update', '--path', book]
            preview = json.loads(run([*command, '--json'], env=env, cwd=scratch))['data']
            require(snapshot(book) == before, 'Update preview changed project files')
            applied = json.loads(run([*command, '--apply', '--preview', preview['preview_id'],
                                      '--expected-head', preview['reviewed_head'], '--json'],
                                     env=env, cwd=scratch))['data']
            require(applied['applied'], 'Reviewed update was not applied')
            after = snapshot(book)
            require((book / 'AGENTS.md').read_bytes().startswith(instructions),
                    'Update changed existing custom instructions')
            changed = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
            allowed = default_update_inventory(runtime['version'], source_version, before)
            require(changed == allowed, f'Unexpected resource changes: {sorted(changed)}')
            expected = scratch / ('New ' + book.name)
            run([python, '-I', '-B', '-m', 'novel_creator', 'notebook', 'init', expected.name,
                 '--path', expected, '--language', language, '--json'], env=env, cwd=scratch)
            check_default_delivery(book, expected, changed)
            require(b'## Character development' in (book / 'AGENTS.md').read_bytes(),
                    'Character-development routing missing')
            require(b'chat-only' in (book / '.novel-notebook/workflows/character-development.md').read_bytes(),
                    'Character-development save boundary missing')
            require(b'novel-character-develop' in (book / '.novel-notebook/workflows/help.md').read_bytes(),
                    'Help catalog lacks the installed skill')
            probe_guards(command, book, scratch, env)
            require((book / '.git/index').read_bytes() == index, 'Update changed unrelated staging')
            require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch) == head,
                    'Update changed project history')
            require(not (book / '.novel-notebook/integration.json').exists(),
                    'Update silently adopted plugin integration')
            current = json.loads(run([*command, '--json'], env=env, cwd=scratch))['data']
            require(current['already_current'], 'Repeated update did not report current resources')
            cases.append({'language': language, 'source_version': source_version,
                          'target_version': runtime['version'],
                          'story_custom_instructions_history_and_staging_preserved': True,
                          'focused_update': 'compatible', 'implicit_plugin_adoption': False})
        manual = (verify_manual(python, old_product, old_cli, scratch, env)
                  if source_version == '0.8.0' else [])
        return {'ok': True, 'manual_notebooks': manual,
                'source_sha256': PUBLIC_WHEELS[source_version][1],
                'verified_product_files': runtime['verified_product_files'],
                'candidate_artifact': 'sdist' if sdist else 'wheel',
                'candidate_artifact_sha256': hashlib.sha256((sdist or wheel).read_bytes()).hexdigest(),
                'candidate_wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
                'notebooks': cases}


def verify_feature_upgrade(python, old_product, old_cli, scratch, env):
    """Actual previous-public initializers and installed feature APIs, all layouts."""
    cases = []
    probe = '''
import sys,json,os
from pathlib import Path
import novel_creator
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))
sys.path.append(sys.argv[1])
from tests.feature_upgrade_checks import exercise
print(json.dumps(exercise(sys.executable,Path(sys.argv[2]),Path(sys.argv[3]),dict(os.environ),
 host=sys.argv[4],source=sys.argv[5],default=sys.argv[6]=='default')))
'''
    for host in ('codex', 'claude', 'both'):
        for source in ('project', 'plugin'):
            for language in ('en', 'is'):
                modes = ('feature', 'default') if (host, source) == ('codex', 'project') else ('feature',)
                for mode in modes:
                    book = scratch / f'Features {host} {source} {language} {mode}'
                    expected = scratch / ('New ' + book.name)
                    for path, command in ((book, [python, '-I', '-B', '-c', old_cli, old_product]),
                                          (expected, [python, '-I', '-B', '-m', 'novel_creator'])):
                        created = json.loads(run([*command, 'notebook', 'init', path.name, '--path', path,
                            '--language', language, '--host', host, '--skill-source', source, '--json'],
                            env=env, cwd=scratch))
                        require(created.get('ok') and created['data']['ready'], 'Feature notebook init failed')
                    result = json.loads(run([python, '-I', '-B', '-X', 'utf8', '-c', probe, ROOT, book,
                                             expected, host, source, mode], env=env, cwd=scratch))
                    cases.append(dict(host=host, skill_source=source, language=language, **result))
    for language in ('en', 'is'):
        book = scratch / ('Feature new legacy ' + language)
        initialize_legacy_fixture(python, book, language, scratch, env)
        check = ('import sys;from pathlib import Path;sys.path.append(sys.argv[1]);'
                 'from tests.feature_upgrade_checks import check_legacy_features;'
                 'check_legacy_features(Path(sys.argv[2]),fresh_root=True)')
        run([python, '-I', '-B', '-c', check, ROOT, book], env=env, cwd=scratch)
    return cases


def verify_session_upgrade(python, old_product, old_cli, scratch, env, *, source_version='0.10.0'):
    """Frozen public notebooks and actual candidate new setup, all twelve layouts."""
    try:
        from tests.session_guidance_checks import exercise, check_links, procedure, prepare_retro
        from tests.feature_upgrade_checks import check_features, feature_paths
    except ModuleNotFoundError:
        from session_guidance_checks import exercise, check_links, procedure, prepare_retro
        from feature_upgrade_checks import check_features, feature_paths
    target = json.loads(run([python, '-I', '-c',
        'import json,novel_creator;print(json.dumps(novel_creator.__version__))'], env=env, cwd=scratch))
    cases = []
    for host in ('codex', 'claude', 'both'):
        for source in ('project', 'plugin'):
            for language in ('en', 'is'):
                book = scratch / f'Session {host} {source} {language}'
                expected = scratch / ('New ' + book.name)
                for path, command in ((book, [python, '-I', '-B', '-c', old_cli, old_product]),
                                      (expected, [python, '-I', '-B', '-m', 'novel_creator'])):
                    created = json.loads(run([*command, 'notebook', 'init', path.name,
                        '--path', path, '--language', language, '--host', host,
                        '--skill-source', source, '--json'], env=env, cwd=scratch))
                    require(created.get('ok') and created['data']['ready'], 'Notebook init failed')
                if source_version in ('0.10.3', '0.10.4'):
                    live_snapshots = Version(target) >= Version('0.10.5')
                    changed_paths = {'.novel-notebook/workflows/conversation.md'}
                    if live_snapshots:
                        changed_paths |= feature_paths(host, source, 'retrospective') | {
                            '.novel-notebook/workflows/' + name + '.md' for name in ('help', 'debugging')}
                        changed_paths |= {'AGENTS.md', 'CLAUDE.md'} if host == 'both' else {
                            'AGENTS.md' if host == 'codex' else 'CLAUDE.md'}
                    prepare_retro(python, book, expected, env, host=host, source=source,
                                  expected_changes=changed_paths)
                    guide = (book / '.novel-notebook/workflows/conversation.md').read_bytes()
                    require(b'Keep knowledge and practical leverage distinct.' in guide and
                            b'unclear speaker cannot supply writer acceptance or save approval' in guide,
                            'Installed conversation guide lacks story status or attribution guidance')
                    if live_snapshots:
                        retro = (book / '.novel-notebook/workflows/retrospective.md').read_bytes()
                        require(b'--keep-debugging' in retro and b'GitHub issue candidate in the first reply' in retro,
                                'Installed retrospective lacks live snapshot or local candidate guidance')
                    cases.append(dict(host=host, skill_source=source, language=language,
                                      source_version=source_version, new_notebook=True, issue_setup=True,
                                      conversation_only=not live_snapshots, live_snapshot_and_candidates=live_snapshots,
                                      exact_resources_root_and_links=True, custom_stale_hardlink_refused=True,
                                      writer_index_history_preserved=True))
                    continue
                if not cases and source_version == '0.10.0':
                    before = snapshot(book)
                    old_probe = ('import sys;sys.path.insert(0,sys.argv.pop(1));exec(' +
                                 repr(procedure()) + ')')
                    run([python, '-I', '-B', '-c', old_probe, old_product, 'preview'],
                        env=env, cwd=book, expected_exit=1)
                    require(snapshot(book) == before, 'Old package capability refusal changed files')
                if source_version == '0.10.0' and host == 'codex' and source == 'project':
                    # Retain the established default-layout updater journey too.
                    focused = [python, '-I', '-B', '-m', 'novel_creator', 'notebook',
                               'update', '--path', book]
                    before = snapshot(book)
                    review = json.loads(run([*focused, '--json'], env=env, cwd=scratch))['data']
                    require(snapshot(book) == before, 'Focused preview changed notebook')
                    run([*focused, '--apply', '--preview', review['preview_id'],
                         '--expected-head', review['reviewed_head'], '--json'], env=env, cwd=scratch)
                    after = snapshot(book)
                    changed = {n for n in before.keys() | after.keys() if before.get(n) != after.get(n)}
                    require(changed == default_update_inventory(target, '0.10.0', before),
                            f'Focused updater changed unexpected guidance: {sorted(changed)}')
                    check_default_delivery(book, expected, changed)
                    repeated = json.loads(run([*focused, '--json'], env=env, cwd=scratch))['data']
                    require(repeated['already_current'], 'Focused update retry failed')
                check_links(expected)
                if Version(target) >= Version('0.10.2'):
                    # The current six-guide procedure needs explicit side-character
                    # and issue setup first. Old nondefault notebooks lack the
                    # feature; keep the documented procedure's checks intact.
                    if not (book / '.novel-notebook/workflows/side-character.md').is_file():
                        feature = ('from novel_creator.notebook_side_character import update;'
                                   'import sys;p=update(sys.argv[1])["data"];'
                                   'update(sys.argv[1],apply=True,preview_id=p["preview_id"],'
                                   'expected_head=p["reviewed_head"])')
                        run([python, '-I', '-B', '-c', feature, book], env=env, cwd=scratch)
                    if source_version == '0.10.2':
                        preserved, _, raw_index, original_head = prepare_retro(
                            python, book, expected, env, host=host, source=source)
                    else:
                        command = [python, '-I', '-B', '-m', 'novel_creator', 'retro', 'issue',
                                   'setup', '--novel', book]
                        review = json.loads(run([*command, '--json'], env=env, cwd=scratch))['data']
                        run([*command, '--apply', '--preview', review['preview_id'],
                             '--expected-head', review['reviewed_head'], '--json'], env=env, cwd=scratch)
                result = exercise(python, book, expected, env, host=host, source=source,
                                  prepared=source_version == '0.10.2')
                if source_version == '0.10.2':
                    check_features(book, expected, host=host, source=source)
                    require((book / '.git/index').read_bytes() == raw_index,
                            'Full guidance sequence changed original raw staging')
                    require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch) == original_head,
                            'Full guidance sequence changed original history')
                    for name in ('notebook/prerequisite-writer.md', 'prerequisite-staging.txt'):
                        require(snapshot(book)[name] == preserved[name], 'Original writer bytes changed')
                cases.append(dict(host=host, skill_source=source, language=language,
                                  source_version=source_version, new_notebook=True, **result))
    # New legacy books retain their supported methods; notebook-only guidance
    # must not silently introduce notebook save semantics or a retro CLI there.
    for language in ('en', 'is'):
        book = scratch / ('New legacy ' + language)
        initialize_legacy_fixture(python, book, language, scratch, env)
        require((book / '.novel-creator/workflows/debugging.md').is_file(), 'New legacy debug guide missing')
        require((book / '.agents/skills/novel-clarify/SKILL.md').is_file(), 'Legacy clarification entry missing')
        check_links(book)
        if source_version in ('0.10.3', '0.10.4'):
            probe = ('import sys;from pathlib import Path;sys.path.append(sys.argv[1]);'
                     'from tests.feature_upgrade_checks import check_legacy_continuity, check_legacy_retro_refresh;'
                     'root=Path(sys.argv[2]);check_legacy_continuity(root,fresh_root=True);'
                     'check_legacy_retro_refresh(root) if sys.argv[3] == "0.10.4" else None')
            run([python, '-I', '-B', '-c', probe, ROOT, book, source_version], env=env, cwd=scratch)
    return cases


def initialize_legacy_fixture(python, book, language, scratch, env):
    """Give this disposable book its own identity, independent of developer Git."""
    book.mkdir()
    run(['git', '-C', book, 'init', '-b', 'main'], env=env, cwd=scratch)
    # Production storage.git intentionally drops inherited GIT_* overrides.
    # Configure only this synthetic repository; never rely on a global identity.
    run(['git', '-C', book, 'config', '--local', 'user.name', 'Previous Release Qualification'],
        env=env, cwd=scratch)
    run(['git', '-C', book, 'config', '--local', 'user.email', 'test@example.invalid'],
        env=env, cwd=scratch)
    probe = ("from novel_creator.install import initialize;import sys,json;"
             "r=initialize(sys.argv[1],json.dumps({'title':'Synthetic new legacy',"
             "'manuscript_language':sys.argv[2]}));assert r['data']['saved']")
    run([python, '-I', '-B', '-c', probe, book, language], env=env, cwd=scratch)
    # Assert ownership on every caller, including isolated wheel/sdist probes.
    for key, expected in (('user.name', 'Previous Release Qualification'),
                          ('user.email', 'test@example.invalid')):
        require(run(['git', '-C', book, 'config', '--local', '--get', key],
                    env=env, cwd=scratch).strip() == expected,
                'Synthetic legacy repository identity changed: ' + key)
    identity = run(['git', '-C', book, 'log', '-1', '--format=%an%n%ae%n%cn%n%ce'],
                   env=env, cwd=scratch).splitlines()
    require(identity == ['Previous Release Qualification', 'test@example.invalid',
                         'Previous Release Qualification', 'test@example.invalid'],
            'Synthetic legacy initial commit must use its repository identity')


def verify_debug_legacy(python, source, wheel, scratch, env, version, *, source_version="0.9.0"):
    """Upgrade a frozen public pinned book via the installed candidate controller."""
    probe = r'''
import json,sys,re
from pathlib import Path
from contextlib import contextmanager
import novel_creator
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))
assert novel_creator.__version__ == sys.argv[4]
sys.path.append(sys.argv[1])
from tests import update_helpers
from tests.verify_update import installed_matrix
update_helpers.SOURCE_WHEELS[sys.argv[6]] = (sys.argv[2], sys.argv[5])
original = update_helpers.historical_book
@contextmanager
def checked_book(*args, **kwargs):
 with original(*args, **kwargs) as book:
  yield book
  pinned = book.root / '.novel-creator/src/novel_creator/debug.py'
  assert pinned.is_file()
  assert (book.root / '.novel-creator/workflows/debugging.md').is_file()
  for skill in ('novel-clarify', 'novel-analyze', 'novel-help'):
   entry = book.root / '.agents/skills' / skill / 'SKILL.md'
   assert entry.is_file()
   for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', entry.read_text(encoding='utf-8')):
    assert (entry.parent / link).is_file()
  if sys.argv[6] in ('0.10.1', '0.10.2'):
   from tests.feature_upgrade_checks import check_legacy_features
   check_legacy_features(book.root)
  if sys.argv[6] in ('0.10.3', '0.10.4'):
   from tests.feature_upgrade_checks import check_legacy_continuity, check_legacy_retro_refresh
   check_legacy_continuity(book.root)
   if sys.argv[6] == '0.10.4':
    check_legacy_retro_refresh(book.root)
  started = book.launch('debug','start','--novel',book.root,'--json')
  assert started.returncode == 0, started.stderr
  session = json.loads(started.stdout)['data']['debug_session']
  stopped = book.launch('debug','stop','--novel',book.root,'--debug-session',session,'--json')
  assert stopped.returncode == 0, stopped.stderr
  exported = book.launch('debug','export','--novel',book.root,'--debug-session',session,'--json')
  assert exported.returncode == 0, exported.stderr
  result = json.loads(exported.stdout)['data']
  assert Path(result['output']).is_file() and not result['partial']
  if sys.argv[6] == '0.10.2':
   from importlib.resources import files
   import zipfile
   for name in ('entry.md','clarify.md','brainstorm.md','debugging.md','retrospective.md'):
    assert (book.root/'.novel-creator/workflows'/name).read_bytes().replace(b'\r\n',b'\n') == files('novel_creator.workflows').joinpath(name).read_bytes().replace(b'\r\n',b'\n')
   with zipfile.ZipFile(result['output']) as archive:
    reports = [archive.read(n) for n in archive.namelist() if n.endswith('report.md')]
    assert len(reports) == 1 and b'These saved values describe session startup.' in reports[0]

update_helpers.historical_book = checked_book
result = installed_matrix([sys.argv[2]], sys.argv[3])
print(json.dumps(result))
'''
    return json.loads(run([python, '-I', '-B', '-X', 'utf8', '-c', probe, ROOT, source, wheel,
                           version, PUBLIC_WHEELS[source_version][1], source_version], env=env, cwd=scratch))


def verify_debug_upgrade(python, old_product, old_cli, scratch, env, *, target_version):
    """Use the real previous initializer and installed candidate on disposable books."""
    cases = []
    for host in ('codex', 'claude', 'both'):
        for source in ('project', 'plugin'):
            for language in ('en', 'is'):
                book = scratch / f'Debug {host} {source} {language}'
                created = json.loads(run([python, '-I', '-B', '-c', old_cli, old_product,
                                          'notebook', 'init', book.name, '--path', book,
                                          '--language', language, '--host', host,
                                          '--skill-source', source, '--json'], env=env, cwd=scratch))
                require(created.get('ok') and created['data']['ready'], 'Public 0.9.0 init failed')
                roots = (['AGENTS.md', 'CLAUDE.md'] if host == 'both' else
                         ['AGENTS.md' if host == 'codex' else 'CLAUDE.md'])
                for name in roots:
                    path = book / name
                    path.write_bytes(path.read_bytes() + b'\nPreserve custom writer instructions.\n')
                (book / 'notebook/writer-preserved.md').write_bytes(b'Accepted writer text.\n')
                staged = book / 'writer-staging.txt'
                staged.write_bytes(b'Staged writer bytes\n')
                run(['git', '-C', book, 'add', '--', staged.name], env=env, cwd=scratch)
                staged.write_bytes(b'Unstaged writer bytes\n')
                before = snapshot(book)
                instructions = {name: (book / name).read_bytes() for name in roots}
                head = run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch)
                index = (book / '.git/index').read_bytes()
                command = [python, '-I', '-m', 'novel_creator', 'debug']
                setup = json.loads(run([*command, 'setup', '--novel', book, '--json'], env=env, cwd=scratch))
                require(setup.get('ok'), 'Debug setup failed on public 0.9.0 notebook')
                after = snapshot(book)
                allowed = set(roots) | {'.gitignore', '.novel-notebook/workflows/debugging.md'}
                if Version(target_version) >= Version('0.10.2') and '.novel-notebook/workflows/retrospective.md' not in before:
                    allowed.add('.novel-notebook/workflows/retrospective.md')
                changed = {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)}
                require(changed <= allowed and '.novel-notebook/workflows/debugging.md' in changed,
                        f'Unexpected debug setup changes: {sorted(changed)}')
                for name in roots:
                    data = (book / name).read_bytes()
                    require(data.startswith(instructions[name]) and b'.novel-notebook/workflows/debugging.md' in data,
                            'Custom host instructions or debug routing not preserved')
                require((book / 'notebook/writer-preserved.md').read_bytes() == b'Accepted writer text.\n',
                        'Story content changed')
                repeat = json.loads(run([*command, 'setup', '--novel', book, '--json'], env=env, cwd=scratch))
                require(repeat['data']['changed_paths'] == [] and snapshot(book) == after,
                        'Repeated debug setup changed the book')
                workflow = book / '.novel-notebook/workflows/debugging.md'
                original = workflow.read_bytes()
                workflow.write_bytes(original + b'Custom divergent guidance.\n')
                conflicted = snapshot(book)
                refused = json.loads(run([*command, 'setup', '--novel', book, '--json'],
                                         env=env, cwd=scratch, expected_exit=3))
                require(not refused['ok'] and snapshot(book) == conflicted, 'Customized debug guidance changed')
                workflow.write_bytes(original)
                started = json.loads(run([*command, 'start', '--novel', book, '--json'], env=env, cwd=scratch))
                session = started['data']['debug_session']
                event = scratch / 'debug-event.json'
                event.write_text(json.dumps({'operation': 'context.read', 'content': 'Þóra',
                    'files': [{'path': 'notebook/project.md', 'phase': 'context'}]}, ensure_ascii=False), encoding='utf-8')
                run([*command, 'record', '--novel', book, '--debug-session', session,
                     '--input', event, '--json'], env=env, cwd=scratch)
                run([*command, 'stop', '--novel', book, '--debug-session', session, '--json'], env=env, cwd=scratch)
                output = scratch / (book.name + '.zip')
                exported = json.loads(run([*command, 'export', '--novel', book, '--debug-session', session,
                                           '--output', output, '--json'], env=env, cwd=scratch))
                require(exported['ok'] and output.is_file() and not exported['data']['partial'], 'Debug export failed')
                require((book / '.git/index').read_bytes() == index, 'Debug setup changed unrelated staging')
                require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch) == head,
                        'Debug setup changed project history')
                cases.append(dict(host=host, skill_source=source, language=language,
                                  source_version='0.9.0', debug_setup_and_export=True,
                                  story_custom_instructions_index_history_preserved=True))
    return cases


def verify_manual(python, old_product, old_cli, scratch, env):
    """Execute the guide in actual public 0.8 books under this installed artifact."""
    doc = (ROOT / 'docs/character-development.md').read_text(encoding='utf-8')
    snippets = re.findall(r'```python\n(.*?)\n```', doc, re.S)
    require(len(snippets) == 1, 'Expected the actual one-off documented procedure')
    procedure = snippets[0]
    cases = []
    for host in ('codex', 'claude', 'both'):
        for source in ('project', 'plugin'):
            for language in ('en', 'is'):
                book = scratch / f'Manual {host} {source} {language}'
                created = json.loads(run([python, '-I', '-B', '-c', old_cli, old_product,
                                          'notebook', 'init', book.name, '--path', book,
                                          '--language', language, '--host', host,
                                          '--skill-source', source, '--json'], env=env, cwd=scratch))
                require(created.get('ok') and created['data']['ready'], 'Public 0.8 init failed')
                hosts = ('codex', 'claude') if host == 'both' else (host,)
                roots = ['AGENTS.md' if selected == 'codex' else 'CLAUDE.md' for selected in hosts]
                for name in roots:
                    path = book / name
                    path.write_bytes(path.read_bytes() + b'\nCustom writer direction.\n'
                                     b'[Unrelated custom link](outside.md)\n')
                (book / 'notebook/writer-preserved.md').write_bytes(b'Accepted writer text.\n')
                staged = book / 'writer-staging.txt'
                staged.write_bytes(b'Staged writer bytes\n')
                run(['git', '-C', book, 'add', '--', staged.name], env=env, cwd=scratch)
                staged.write_bytes(b'Unstaged writer bytes\n')
                root_bytes = {name: (book / name).read_bytes() for name in roots}
                before = snapshot(book)
                head = run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch)
                index = (book / '.git/index').read_bytes()
                command = [python, '-I', '-B', '-c', procedure]
                run(command, env=env, cwd=book)
                after = snapshot(book)
                skills = {f'{".agents" if selected == "codex" else ".claude"}/skills/'
                          'novel-character-develop/SKILL.md' for selected in hosts} if source == 'project' else set()
                additions = skills | {'.novel-notebook/workflows/character-development.md'}
                require(set(after) - set(before) == additions, 'Unexpected manual resource additions')
                require({name for name in before if before[name] != after[name]} == set(roots),
                        'Manual installation changed unrelated files')
                for name in roots:
                    require((book / name).read_bytes().startswith(root_bytes[name]), 'Custom root bytes changed')
                # Compare actual bytes to the installed artifact rendered exactly as new setup.
                probe = ("from novel_creator.notebook import initialize;from pathlib import Path;"
                         f"initialize(Path({str(scratch / ('Expected ' + book.name))!r}), "
                         f"language={language!r},host={host!r},skill_source={source!r})")
                run([python, '-I', '-B', '-c', probe], env=env, cwd=scratch)
                expected = scratch / ('Expected ' + book.name)
                for name in additions:
                    require((book / name).read_bytes() == (expected / name).read_bytes(),
                            'Rendered feature bytes differ')
                for name in roots:
                    text = (expected / name).read_text(encoding='utf-8')
                    section = re.search(r'^## Character development\n.*?(?=^## |\Z)',
                                        text, re.M | re.S).group().rstrip() + '\n'
                    require((book / name).read_bytes().endswith(section.encode('utf-8')),
                            'Rendered root feature section differs')
                run(command, env=env, cwd=book)
                require(snapshot(book) == after, 'Manual retry changed files')
                feature = book / '.novel-notebook/workflows/character-development.md'
                original = feature.read_bytes()
                feature.write_bytes(original + b'Writer divergent feature policy\n')
                conflicted = snapshot(book)
                run(command, env=env, cwd=book, expected_exit=1)
                require(snapshot(book) == conflicted, 'Manual conflict mutated files')
                feature.write_bytes(original)
                require((book / '.git/index').read_bytes() == index, 'Manual installation changed staging')
                require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch) == head,
                        'Manual installation changed history')
                cases.append(dict(host=host, skill_source=source, language=language,
                                  source_version='0.8.0', exact_rendered_bytes=True,
                                  conflict_retry_story_custom_instructions_index_history_preserved=True))
    return cases


def probe_guards(command, book, scratch, env):
    """Installed updater must reject customized/stale/redirected feature copies."""
    resource = book / '.novel-notebook/workflows/character-development.md'
    original = resource.read_bytes()
    resource.write_bytes(original + b'Writer custom feature guidance.\n')
    before = snapshot(book)
    refused = json.loads(run([*command, '--json'], env=env, cwd=scratch, expected_exit=3))
    require(not refused['ok'] and snapshot(book) == before, 'Divergent feature resource was mutated')
    resource.write_bytes(original)
    preview = json.loads(run([*command, '--json'], env=env, cwd=scratch))['data']
    agents = book / 'AGENTS.md'
    original_agents = agents.read_bytes()
    agents.write_bytes(agents.read_bytes() + b'\n## Writer change after preview\n')
    before = snapshot(book)
    refused = json.loads(run([*command, '--apply', '--preview', preview['preview_id'],
                              '--expected-head', preview['reviewed_head'], '--json'],
                             env=env, cwd=scratch, expected_exit=3))
    require(not refused['ok'] and snapshot(book) == before, 'Stale preview changed files')
    agents.write_bytes(original_agents)
    # Hard links are supported without Windows developer-mode symlink privileges.
    outside = scratch / ('redirect-' + book.name + '.md')
    outside.write_bytes(original + b'Outside writer text.\n')
    redirected = outside.read_bytes()
    resource.unlink()
    try:
        os.link(outside, resource)
        before = snapshot(book)
        refused = json.loads(run([*command, '--json'], env=env, cwd=scratch, expected_exit=3))
        require(not refused['ok'] and snapshot(book) == before and outside.read_bytes() == redirected,
                'Redirected divergent feature resource was changed')
    finally:
        resource.unlink(missing_ok=True)
        resource.write_bytes(original)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', type=Path, required=True, help='Exact local candidate wheel')
    parser.add_argument('--plugin', type=Path, default=ROOT / 'plugins/novel-creator', help='Candidate plugin root')
    parser.add_argument('--previous-wheel', type=Path, help='Use a local hash-verified 0.7.2 wheel instead of downloading')
    parser.add_argument('--previous-080-wheel', type=Path, help='Local hash-verified public 0.8.0 wheel')
    parser.add_argument('--previous-090-wheel', type=Path, help='Local hash-verified public 0.9.0 wheel')
    parser.add_argument('--previous-0100-wheel', type=Path, help='Local hash-verified public 0.10.0 wheel')
    parser.add_argument('--previous-0101-wheel', type=Path, help='Local hash-verified public 0.10.1 wheel')
    parser.add_argument('--previous-0102-wheel', type=Path, help='Local hash-verified public 0.10.2 wheel')
    parser.add_argument('--previous-0103-wheel', type=Path, help='Local hash-verified public 0.10.3 wheel')
    parser.add_argument('--previous-0104-wheel', type=Path, help='Local hash-verified public 0.10.4 wheel')
    parser.add_argument('--sdist', type=Path, help='Also test installation from the exact candidate sdist')
    parser.add_argument('--report', type=Path, required=True, help='Success JSON report destination')
    args = parser.parse_args()
    reports = []
    for source_version, previous in (('0.7.2', args.previous_wheel), ('0.8.0', args.previous_080_wheel),
                                     ('0.9.0', args.previous_090_wheel), ('0.10.0', args.previous_0100_wheel),
                                     ('0.10.1', args.previous_0101_wheel), ('0.10.2', args.previous_0102_wheel),
                                     ('0.10.3', args.previous_0103_wheel), ('0.10.4', args.previous_0104_wheel)):
        for sdist in ((None, args.sdist.resolve()) if args.sdist else (None,)):
            reports.append(verify(plugin=args.plugin.resolve(), wheel=args.wheel.resolve(),
                                  previous=previous, source_version=source_version, sdist=sdist))
    write_report(args.report.resolve(), {'ok': True, 'checks': reports})


if __name__ == '__main__':
    main()
