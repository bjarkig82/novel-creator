"""Opt-in 0.7.2 and 0.8.0 notebook update checks against a locally installed candidate.

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
}


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
        cases = []
        for language in ('en', 'is'):
            book = scratch / f'Book {language}'
            created = json.loads(run([python, '-I', '-B', '-c', old_cli, old_product, 'notebook',
                                      'init', book.name, '--path', book, '--language', language, '--json'],
                                     env=env, cwd=scratch))
            require(created.get('ok') and created['data']['ready'], f'Previous notebook not ready: {created}')
            instructions = (book / 'AGENTS.md').read_bytes() + b'\nPreserve this custom writer direction.\n'
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
            allowed = {'AGENTS.md', '.agents/skills/novel-character-develop/SKILL.md',
                       '.novel-notebook/workflows/character-development.md',
                       '.novel-notebook/workflows/help.md'}
            require(changed == allowed, f'Unexpected resource changes: {sorted(changed)}')
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
    parser.add_argument('--sdist', type=Path, help='Also test installation from the exact candidate sdist')
    parser.add_argument('--report', type=Path, required=True, help='Success JSON report destination')
    args = parser.parse_args()
    reports = []
    for source_version, previous in (('0.7.2', args.previous_wheel), ('0.8.0', args.previous_080_wheel)):
        for sdist in ((None, args.sdist.resolve()) if args.sdist else (None,)):
            reports.append(verify(plugin=args.plugin.resolve(), wheel=args.wheel.resolve(),
                                  previous=previous, source_version=source_version, sdist=sdist))
    write_report(args.report.resolve(), {'ok': True, 'checks': reports})


if __name__ == '__main__':
    main()
