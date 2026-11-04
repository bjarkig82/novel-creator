"""Verify a built wheel outside the checkout; no model or publishing operation.

Run with the project's dependency environment:
    python tests/verify_wheel.py dist/novel_creator-0.1.0-py3-none-any.whl
The disposable venv reuses dependency packages, then installs the wheel locally.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig
import tempfile
import venv
import zipfile


def run(args, *, cwd, env, expected_exit=0):
    result = subprocess.run([str(arg) for arg in args], cwd=cwd, env=env,
                            capture_output=True, text=True, encoding='utf-8')
    if result.returncode != expected_exit:
        raise RuntimeError(f'{args!r}: exit {result.returncode}\n{result.stdout}\n{result.stderr}')
    return result.stdout


def verify_notebook(console, scratch, env, language):
    """Exercise installed resources and setup in a new independent repository."""
    import re
    root = scratch / ('Bréf notebook ' + language)
    result = json.loads(run([console, 'notebook', 'init', 'Bréf', '--path', root,
                             '--title', 'Bréf frá morgundeginum', '--language', language, '--json'],
                            cwd=scratch, env=env))
    assert result['ok'] and result['data']['language'] == language
    assert Path(result['data']['novel_path']) == root
    assert 'Bréf frá morgundeginum' in (root / 'notebook/project.md').read_text(encoding='utf-8')
    project = (root / 'notebook/project.md').read_text(encoding='utf-8')
    summary = (root / 'notebook/working-summary.md').read_text(encoding='utf-8')
    if language == 'en':
        assert '## Concept\n\nUnknown.' in project
        assert 'Guided conversation is the default' in project
        assert '# Working summary\n' in summary
        assert 'Derived navigation, not canon. Do not display automatically' in summary
        assert 'Hugmynd' not in project and 'Vinnuyfirlit' not in summary
    else:
        assert '## Hugmynd\n\nÓþekkt.' in project
        assert 'Sjálfgefið er leiðbeinandi samtal' in project
        assert '# Vinnuyfirlit\n' in summary
        assert 'Leiðarvísir, ekki sjálfstæðar sögustaðreyndir. Ekki birta sjálfkrafa' in summary
        assert 'Concept' not in project and 'Working summary' not in summary
    assert (root / '.novel-notebook/languages' / (language + '.md')).is_file()
    assert not (root / '.novel-notebook/languages' / (('is' if language == 'en' else 'en') + '.md')).exists()
    assert not (root / '.novel-creator').exists()
    assert not list(root.rglob('*.py'))
    for reference in ('.novel-notebook/workflows/conversation.md', '.novel-notebook/workflows/format.md',
                      'notebook/project.md', 'notebook/working-summary.md'):
        assert (root / reference).is_file(), reference
    for path in [root / 'AGENTS.md', *(root / '.novel-notebook').rglob('*.md')]:
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text(encoding='utf-8')):
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                assert (path.parent / link).is_file(), (path, link)
    run(['git', '-C', root, 'log', '-1', '--format=%s'], cwd=scratch, env=env)
    return {'language': language, 'created': True, 'guidance_links': True}


def verify(wheel):
    wheel = wheel.resolve(strict=True)
    # Check against source bytes, including resources that a successful import
    # alone would not exercise. Build outputs are never the source of truth.
    checkout = Path(__file__).resolve().parents[1]
    expected = {}
    for source, target, pattern in (
            ('src/novel_creator', 'novel_creator', '*.py'),
            ('src/novel_creator', 'novel_creator', '*.json'),
            ('schemas', 'novel_creator/schemas', '*.json'),
            ('workflows', 'novel_creator/workflows', '*.md'),
            ('languages', 'novel_creator/languages', '*.md'),
            ('adapters/codex', 'novel_creator/codex', '*.md'),
            ('notebook', 'novel_creator/notebook_resources', '*.md'),
            ('notebook', 'novel_creator/notebook_resources', '__init__.py')):
        folder = checkout / source
        for path in folder.rglob(pattern):
            expected[target + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
    with zipfile.ZipFile(wheel) as archive:
        for name, raw in expected.items():
            if archive.read(name) != raw:
                raise RuntimeError(f'Wheel is stale or changed: {name}')

    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1',
               PIP_DISABLE_PIP_VERSION_CHECK='1', PIP_NO_INDEX='1', PIP_CONFIG_FILE=os.devnull)
    for name in ('PYTHONPATH', 'PYTHONHOME', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        env.pop(name, None)
    with tempfile.TemporaryDirectory(prefix='novel-wheel-') as directory:
        scratch = Path(directory).resolve()
        environment = scratch / 'environment'
        # Only dependency packages are inherited; the wheel is installed over
        # any editable project. The child verifies every product module's path.
        # Reuse the calling environment's pip too, avoiding an ensurepip or
        # network requirement on minimal Linux Python installations.
        venv.EnvBuilder(with_pip=False).create(environment)
        scripts = environment / ('Scripts' if os.name == 'nt' else 'bin')
        python = scripts / ('python.exe' if os.name == 'nt' else 'python')
        console = scripts / ('novel-creator.exe' if os.name == 'nt' else 'novel-creator')
        site = Path(run([python, '-I', '-c', "import sysconfig; print(sysconfig.get_path('purelib'))"],
                        cwd=scratch, env=env).strip())
        # A venv created from a venv inherits the base interpreter's site,
        # not the calling venv's dependencies. Add only its package directories;
        # do not execute the calling environment's editable-install .pth files.
        dependency_sites = dict.fromkeys(str(Path(path).absolute()) for path in sys.path
                                       if Path(path).name in ('site-packages', 'dist-packages'))
        (site / 'verification-dependencies.pth').write_text(
            ''.join(path + '\n' for path in dependency_sites), encoding='utf-8')
        run([python, '-I', '-B', '-m', 'pip', '--isolated', 'install', '--no-index',
             '--no-deps', '--ignore-installed', '--no-compile', '--no-cache-dir', wheel], cwd=scratch, env=env)
        run([console, '--help'], cwd=scratch, env=env)
        probe = """
import json
from pathlib import Path
import sys
from novel_creator.install import bundle_files
from novel_creator import context, records, storage, validation, validation_cache
from novel_creator.update_release import protocol, export_bundle
metadata=protocol()
assert metadata['protocol_version'] == 1 and metadata['source_installation_formats'] == [1,2]
exported=export_bundle()
assert '.novel-creator/workflows/update.md' in exported['files']
assert '.agents/skills/novel-update/SKILL.md' in exported['files']
paths = [str(Path(module.__file__).resolve()) for name, module in sys.modules.items()
         if name.startswith('novel_creator') and getattr(module, '__file__', None)]
assert paths and all(Path(path).is_relative_to(Path(sys.prefix)) for path in paths), paths
print(json.dumps({'modules': paths, 'bundle_file_count': len(bundle_files()), 'update_protocol': metadata}))
"""
        package = json.loads(run([python, '-I', '-B', '-c', probe], cwd=scratch, env=env))
        cases = []
        for label, brief in [('unknown', {}), ('icelandic', {
                'title': 'Bréf Þóru', 'original_concept': 'Þóra fær bréf.\n',
                'manuscript_language': 'is', 'creative_brief': {'genre': 'Leyndardómur', 'tone': None}})]:
            root = scratch / label
            root.mkdir()
            for args in [('init', '-b', 'main'), ('config', 'user.name', 'Wheel Verification'),
                         ('config', 'user.email', 'wheel@example.invalid')]:
                run(['git', '-C', root, *args], cwd=scratch, env=env)
            brief_file = scratch / (label + '.json')
            brief_file.write_text(json.dumps(brief, ensure_ascii=False), encoding='utf-8')
            initialized = json.loads(run([console, 'init', '--path', root, '--brief-file', brief_file, '--json'],
                                         cwd=scratch, env=env))
            launcher = root / '.novel-creator/run.py'
            def invoke(*args, expected_exit=0):
                argv = [str(launcher), *args, '--novel', str(root), '--json']
                # -I ignores PYTHONIOENCODING. Force legacy streams inside the
                # isolated child so this checks UTF-8 output on every platform.
                code = ("import runpy, sys; sys.stdout.reconfigure(encoding='ascii'); "
                        "sys.stderr.reconfigure(encoding='ascii'); "
                        f"sys.argv = {argv!r}; runpy.run_path({str(launcher)!r}, run_name='__main__')")
                return json.loads(run([python, '-I', '-B', '-c', code], cwd=scratch, env=env,
                                      expected_exit=expected_exit))
            context = invoke('context')
            assert invoke('retro', 'status')['data']['enabled'] is False
            assert (root / '.novel-creator/workflows/retrospective.md').is_file()
            assert (root / '.novel-creator/src/novel_creator/retro.py').is_file()
            assert (root / '.novel-creator/src/novel_creator/retro_github.py').is_file()
            assert (root / '.novel-creator/src/novel_creator/schemas/v1/retro.schema.json').is_file()
            project = context['data']['project']
            assert project['creative_brief']['tone']['state'] == 'unknown'
            if brief:
                assert project['title']['original_text'] == brief['title']
                assert project['original_concept']['original_text'] == brief['original_concept']
                assert project['manuscript_language'] == 'is'
            assert invoke('session', 'list')['data']['sessions'] == []
            assert invoke('validate')['data']['exchange_count'] == 1
            assert invoke('inspect', '--kind', 'assertion')['ok']
            missing = 'Ófundið — 東京 🌒'
            unavailable = invoke('inspect', '--id', missing, expected_exit=4)
            assert unavailable['error']['affected_refs'] == [missing]
            recovered = invoke('recover', '--exchange', initialized['checkpoint']['exchange_id'])
            assert recovered['data']['saved']
            assert recovered['checkpoint'] == initialized['checkpoint']
            # Use only the pinned novel modules, even while the wheel remains
            # installed. The existing portable journey covers deeper transitions.
            pinned = f"""
import json, sys, uuid
from pathlib import Path
root = Path({str(root)!r})
sys.path.insert(0, str(root / '.novel-creator/src'))
from novel_creator import records, storage
assert Path(storage.__file__).resolve().is_relative_to(root)
previous = storage.read_history(root)[-1]
exchange = records.new_exchange(previous['novel_id'], previous=previous,
    expected_head=storage.head(root), messages=[
    {{'message_id': str(uuid.uuid4()), 'role': 'user', 'text': 'Höldum áfram.\\n'}},
    {{'message_id': str(uuid.uuid4()), 'role': 'assistant', 'text': 'Hvaða bréf?\\n'}}])
session = records.start_session(exchange, topic='Bréfin')
exchange.update(session_id=session['id'], record_versions=[session])
exchange['payload_digest'] = records.digest(exchange)
result = storage.save(root, exchange)
assert result['data']['saved'] and not result['data']['cleanup_required']
assert storage.read_history(root)[-1]['messages'] == exchange['messages']
print(json.dumps(result))
"""
            saved = json.loads(run([python, '-I', '-B', '-c', pinned], cwd=scratch, env=env))
            assert invoke('validate')['data']['exchange_count'] == 2
            assert invoke('session', 'list')['data']['sessions'][0]['topic'] == 'Bréfin'
            assert invoke('context')['checkpoint'] == saved['checkpoint']
            cases.append({'case': label, 'initialized': True, 'pinned_save_and_reopen': True})
        simple = scratch / 'Simple Novel'
        simple.mkdir()
        for args in [('init', '-b', 'main'), ('config', 'user.name', 'Wheel Verification'),
                     ('config', 'user.email', 'wheel@example.invalid')]:
            run(['git', '-C', simple, *args], cwd=scratch, env=env)
        shorthand = json.loads(run([console, 'init', 'Simple Novel', '--json'], cwd=scratch, env=env))
        assert shorthand['data']['ready']
        assert Path(shorthand['data']['getting_started_path']).read_bytes() == expected['novel_creator/workflows/getting-started.md']
        version = run([console, '--version'], cwd=scratch, env=env).strip()
        cases.append({'case': 'name-only', 'ready': True, 'version': version,
                      'request_artifact': True, 'guide_identity': True})
        history = json.loads(next((simple / 'story/exchanges').glob('*.json')).read_text(encoding='utf-8'))
        assert history['input_artifacts'][1]['parsed_value']['name'] == 'Simple Novel'
        env.update(GIT_AUTHOR_NAME='Wheel Verification', GIT_AUTHOR_EMAIL='wheel@example.invalid',
                   GIT_COMMITTER_NAME='Wheel Verification', GIT_COMMITTER_EMAIL='wheel@example.invalid')
        notebook_cases = [verify_notebook(console, scratch, env, language) for language in ('en', 'is')]
        update_probe = '''
import sys,json
from pathlib import Path
from packaging.version import Version
from novel_creator import __version__
import novel_creator
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))
sys.path.append(sys.argv[1])
from tests.update_helpers import SOURCE_WHEELS
from tests.verify_update import installed_matrix
sources=[str(Path(sys.argv[1])/path) for version,(path,digest) in SOURCE_WHEELS.items() if Version(version)<Version(__version__)]
assert sources
result=installed_matrix(sources,sys.argv[2])
assert all(Path(module.__file__).resolve().is_relative_to(Path(sys.prefix))
 for name,module in sys.modules.items() if name.startswith('novel_creator') and getattr(module,'__file__',None))
print(json.dumps(result))
'''
        update_cases = json.loads(run([python, '-I', '-B', '-X', 'utf8', '-c', update_probe, checkout, wheel],
                                      cwd=scratch, env=env))['cases']
    return {'ok': True, 'wheel': wheel.name,
            'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
            'verified_source_files': len(expected), 'package': package, 'cases': cases, 'notebook_cases': notebook_cases, 'update_cases': update_cases,
            'dependency_isolation': 'calling environment package directories reused; product module origins checked',
            'semantic_host_or_human_evidence': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wheel', type=Path)
    arguments = parser.parse_args()
    print(json.dumps(verify(arguments.wheel), ensure_ascii=False, indent=2))
