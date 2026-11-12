"""Opt-in 0.7.2 notebook update checks against a locally installed candidate.

Downloads the frozen public previous wheel unless --previous-wheel is supplied.
All installations, books and Git identities are disposable process-local state.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.request
from urllib.parse import urlparse

try:
    from tests.verify_plugin_install import bootstrap, require, run, snapshot, temporary_environment, write_report
except ModuleNotFoundError:
    from verify_plugin_install import bootstrap, require, run, snapshot, temporary_environment, write_report


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_VERSION = '0.7.2'
PREVIOUS_FILENAME = 'novel_creator-0.7.2-py3-none-any.whl'
PREVIOUS_SHA256 = '8ee343c10bfcc8129d860a8502c669856deaa92f62b5059f915a4027fc11c9f5'


def previous_wheel(scratch, supplied):
    if supplied is not None:
        path = supplied.resolve()
        raw = path.read_bytes()
    else:
        with urllib.request.urlopen(f'https://pypi.org/pypi/novel-creator/{PREVIOUS_VERSION}/json',
                                    timeout=30) as response:
            metadata = json.load(response)
        entries = [entry for entry in metadata['urls']
                   if entry['packagetype'] == 'bdist_wheel' and entry['filename'] == PREVIOUS_FILENAME]
        require(len(entries) == 1, 'Expected exactly one frozen previous-release wheel')
        entry = entries[0]
        require(entry['digests']['sha256'] == PREVIOUS_SHA256, 'Public wheel identity changed')
        url = urlparse(entry['url'])
        require(url.scheme == 'https' and url.hostname == 'files.pythonhosted.org',
                'Unexpected previous-wheel download origin')
        with urllib.request.urlopen(entry['url'], timeout=60) as response:
            raw = response.read()
        path = scratch / PREVIOUS_FILENAME
        path.write_bytes(raw)
    require(hashlib.sha256(raw).hexdigest() == PREVIOUS_SHA256, 'Previous wheel SHA-256 mismatch')
    return path


def verify(*, plugin, wheel, previous):
    with tempfile.TemporaryDirectory(prefix='novel-marketplace-previous-') as temporary:
        scratch = Path(temporary).resolve()
        env = temporary_environment(scratch)
        old_wheel = previous_wheel(scratch, previous)
        runtime = bootstrap(plugin, wheel, scratch, env)
        python = runtime['runtime_python']
        old_product = scratch / 'old-product'
        # The already hash-verified wheel has no dependencies to resolve here.
        install_env = dict(env, PIP_CONFIG_FILE=os.devnull)
        run([python, '-I', '-m', 'pip', 'install', '--no-input', '--disable-pip-version-check',
             '--no-deps', '--no-user', '--target', old_product, old_wheel], env=install_env, cwd=scratch)
        old_cli = ('import sys;sys.path.insert(0,sys.argv[1]);import novel_creator;'
                   f'assert novel_creator.__version__ == {PREVIOUS_VERSION!r};'
                   'from novel_creator.cli import main;raise SystemExit(main(sys.argv[2:]))')
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
            require(changed <= {'AGENTS.md'}, f'Unexpected resource changes: {sorted(changed)}')
            require((book / '.git/index').read_bytes() == index, 'Update changed unrelated staging')
            require(run(['git', '-C', book, 'rev-parse', 'HEAD'], env=env, cwd=scratch) == head,
                    'Update changed project history')
            require(not (book / '.novel-notebook/integration.json').exists(),
                    'Update silently adopted plugin integration')
            current = json.loads(run([*command, '--json'], env=env, cwd=scratch))['data']
            require(current['already_current'], 'Repeated update did not report current resources')
            cases.append({'language': language, 'source_version': PREVIOUS_VERSION,
                          'target_version': runtime['version'],
                          'story_custom_instructions_history_and_staging_preserved': True,
                          'focused_update': 'compatible', 'implicit_plugin_adoption': False})
        return {'ok': True, 'source_sha256': PREVIOUS_SHA256,
                'candidate_wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
                'notebooks': cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', type=Path, required=True, help='Exact local candidate wheel')
    parser.add_argument('--plugin', type=Path, default=ROOT / 'plugins/novel-creator', help='Candidate plugin root')
    parser.add_argument('--previous-wheel', type=Path, help='Use a local hash-verified 0.7.2 wheel instead of downloading')
    parser.add_argument('--report', type=Path, required=True, help='Success JSON report destination')
    args = parser.parse_args()
    write_report(args.report.resolve(), verify(plugin=args.plugin.resolve(), wheel=args.wheel.resolve(),
                                              previous=args.previous_wheel))


if __name__ == '__main__':
    main()
