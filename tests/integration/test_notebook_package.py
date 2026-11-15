"""Install both built distributions offline and initialize outside the checkout."""
import os
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
import venv
import zipfile

from tests.release_fixtures import published_wheel
from tests.notebook_resource_checks import resource_paths
from tests.verify_wheel import run, verify_notebook


class NotebookPackageTest(unittest.TestCase):
    def test_wheel_and_sdist_install_and_initialize(self):
        checkout = Path(__file__).resolve().parents[2]
        resources = resource_paths(checkout)
        expected = {relative: source.read_bytes() for relative, (source, _) in resources.items()}
        env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1',
                   PIP_NO_INDEX='1', PIP_DISABLE_PIP_VERSION_CHECK='1', PIP_CONFIG_FILE=os.devnull,
                   GIT_AUTHOR_NAME='Package Test', GIT_AUTHOR_EMAIL='package@example.invalid',
                   GIT_COMMITTER_NAME='Package Test', GIT_COMMITTER_EMAIL='package@example.invalid')
        for key in ('PYTHONPATH', 'PYTHONHOME', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
            env.pop(key, None)
        with tempfile.TemporaryDirectory(prefix='notebook-package-') as tmp:
            scratch = Path(tmp).resolve()
            artifacts = scratch / 'artifacts'
            artifacts.mkdir()
            build = ("from setuptools.build_meta import build_wheel, build_sdist; "
                     f"build_wheel({str(artifacts)!r}); build_sdist({str(artifacts)!r})")
            run([sys.executable, '-c', build], cwd=checkout, env=env)
            wheel = next(artifacts.glob('*.whl'))
            sdist = next(artifacts.glob('*.tar.gz'))
            added = {
                'src/novel_creator/debug.py': 'novel_creator/debug.py',
                'workflows/debugging.md': 'novel_creator/workflows/debugging.md',
                'src/novel_creator/retro_issues.py': 'novel_creator/retro_issues.py',
                'src/novel_creator/retro_issue_setup.py': 'novel_creator/retro_issue_setup.py',
                'src/novel_creator/retro_issue_provenance.py': 'novel_creator/retro_issue_provenance.py',
                'workflows/retrospective.md': 'novel_creator/workflows/retrospective.md',
                'adapters/codex/skills/novel-retro/SKILL.md': 'novel_creator/codex/skills/novel-retro/SKILL.md',
            }
            with zipfile.ZipFile(wheel) as archive:
                for relative, (_, member) in resources.items():
                    self.assertEqual(archive.read(member), expected[relative], member)
                for source, member in added.items():
                    self.assertEqual(archive.read(member), (checkout / source).read_bytes(), member)
            with tarfile.open(sdist, 'r:gz') as archive:
                prefix = sdist.name.removesuffix('.tar.gz')
                for relative, (source, _) in resources.items():
                    member = prefix + '/' + source.relative_to(checkout).as_posix()
                    stream = archive.extractfile(member)
                    self.assertIsNotNone(stream, member)
                    with stream:
                        self.assertEqual(stream.read(), expected[relative], member)
                for source in added:
                    member = prefix + '/' + source
                    stream = archive.extractfile(member)
                    self.assertIsNotNone(stream, member)
                    with stream:
                        self.assertEqual(stream.read(), (checkout / source).read_bytes(), member)
                plugin = prefix + '/plugins/novel-creator/skills/novel-retro/SKILL.md'
                self.assertEqual(archive.extractfile(plugin).read(),
                                 (checkout / 'plugins/novel-creator/skills/novel-retro/SKILL.md').read_bytes())
            for label, archive in [('wheel', wheel), ('sdist', sdist)]:
                with self.subTest(artifact=label):
                    area = scratch / label
                    area.mkdir()
                    environment = area / 'environment'
                    venv.EnvBuilder(with_pip=False).create(environment)
                    scripts = environment / ('Scripts' if os.name == 'nt' else 'bin')
                    python = scripts / ('python.exe' if os.name == 'nt' else 'python')
                    console = scripts / ('novel-creator.exe' if os.name == 'nt' else 'novel-creator')
                    site = Path(run([python, '-I', '-c', "import sysconfig; print(sysconfig.get_path('purelib'))"], cwd=area, env=env).strip())
                    sites = dict.fromkeys(str(Path(p).absolute()) for p in sys.path if Path(p).name in ('site-packages', 'dist-packages'))
                    (site / 'dependencies.pth').write_text(''.join(p + '\n' for p in sites), encoding='utf-8')
                    run([sys.executable, '-I', '-m', 'pip', '--isolated', '--python', python, 'install',
                         '--no-index', '--no-deps', '--no-build-isolation', '--no-cache-dir', archive], cwd=area, env=env)
                    probe = "import novel_creator,sys; from pathlib import Path; assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))"
                    run([python, '-I', '-c', probe], cwd=area, env=env)
                    for language in ('en', 'is'):
                        result = verify_notebook(console, area, env, language, expected)
                        self.assertEqual(result['verified_resource_count'], len(expected))
                    self.verify_debug(console, area, env)
                    self.verify_issue_setup(console, area, env)
                    legacy = area / 'New legacy'
                    legacy.mkdir()
                    run(['git', '-C', legacy, 'init', '-b', 'main'], cwd=area, env=env)
                    code = ("import json,sys; from novel_creator.install import initialize; "
                            "r=initialize(sys.argv[1],json.dumps({'title':'Synthetic legacy','manuscript_language':'en'})); "
                            "assert r['data']['saved'],r")
                    run([python, '-I', '-c', code, legacy], cwd=area, env=env)
                    legacy_skill = legacy / '.agents/skills/novel-retro/SKILL.md'
                    self.assertTrue(legacy_skill.is_file())
                    self.assertTrue((legacy / '.novel-creator/workflows/retrospective.md').is_file())
                    self.assertIn('retro', (legacy / 'AGENTS.md').read_text(encoding='utf-8'))
                    refused = subprocess.run([python, '-I', str(legacy / '.novel-creator/run.py'),
                                              'retro', 'issue', 'setup', '--novel', str(legacy), '--json'],
                                             cwd=area, env=env, capture_output=True, text=True, encoding='utf-8')
                    self.assertEqual(refused.returncode, 3, refused.stdout + refused.stderr)
                    self.assertFalse(json.loads(refused.stdout)['ok'])
                    self.assertIn('framework update', refused.stdout)
                    self.assertNotIn('Traceback', refused.stderr)
                    # Valid mixed-marker metadata still needs the external notebook runtime.
                    (legacy / 'notebook').mkdir()
                    (legacy / 'notebook/project.md').write_bytes((area / 'Bréf notebook en/notebook/project.md').read_bytes())
                    (legacy / 'notebook/working-summary.md').write_bytes((area / 'Bréf notebook en/notebook/working-summary.md').read_bytes())
                    languages = legacy / '.novel-notebook/languages'
                    languages.mkdir(parents=True)
                    (languages / 'en.md').write_bytes((area / 'Bréf notebook en/.novel-notebook/languages/en.md').read_bytes())
                    mixed = subprocess.run([python, '-I', str(legacy / '.novel-creator/run.py'),
                                            'retro', 'issue', 'setup', '--novel', str(legacy), '--json'],
                                           cwd=area, env=env, capture_output=True, text=True, encoding='utf-8')
                    self.assertEqual(mixed.returncode, 3, mixed.stdout + mixed.stderr)
                    self.assertIn('external current runtime', mixed.stdout)
                    self.assertNotIn('Traceback', mixed.stderr)


                    print(f'{label}: {len(resources)} artifact resources match source bytes; '
                          'isolated install and en/is notebook resource checks passed')

    def verify_issue_setup(self, console, area, env):
        """Actual installed CLI upgrades old snapshots without story/index writes."""
        previous = published_wheel('0.10.1')
        root = area / 'Bréf notebook en'
        from novel_creator.retro_issue_setup import ROUTING, OLD_ROOT
        with zipfile.ZipFile(previous) as archive:
            for name in ('conversation', 'debugging', 'help'):
                (root / '.novel-notebook/workflows' / (name + '.md')).write_bytes(
                    archive.read('novel_creator/notebook_resources/workflows/' + name + '.md'))
        (root / '.novel-notebook/workflows/retrospective.md').unlink()
        (root / '.agents/skills/novel-retro/SKILL.md').unlink()
        instruction = root / 'AGENTS.md'
        instruction.write_text(instruction.read_text(encoding='utf-8').replace(ROUTING, OLD_ROOT), encoding='utf-8')
        story = (root / 'notebook/project.md').read_bytes()
        index = (root / '.git/index').read_bytes()
        def invoke(*args):
            value = json.loads(run([console, 'retro', 'issue', 'setup', '--novel', root, '--json', *args], cwd=area, env=env))
            self.assertTrue(value['ok'], value)
            return value['data']
        preview = invoke()
        self.assertTrue(invoke('--apply', '--preview', preview['preview_id'], '--expected-head', preview['reviewed_head'])['applied'])
        self.assertTrue(invoke()['already_current'])
        self.assertEqual((root / 'notebook/project.md').read_bytes(), story)
        self.assertEqual((root / '.git/index').read_bytes(), index)
        skill = root / '.agents/skills/novel-retro/SKILL.md'
        self.assertIn('retrospective.md', skill.read_text())

    def verify_debug(self, console, area, env):
        """Exercise the recorder from the installed distribution, outside source."""
        root = area / 'Bréf notebook en'
        def debug(*args):
            result = json.loads(run([console, 'debug', *args, '--novel', root, '--json'],
                                    cwd=area, env=env))
            self.assertTrue(result['ok'], result)
            return result['data']

        # Existing-book setup must preserve the installed guidance and Git state.
        before = run(['git', '-C', root, 'status', '--porcelain'], cwd=area, env=env)
        debug('setup')
        self.assertEqual(run(['git', '-C', root, 'status', '--porcelain'], cwd=area, env=env), before)
        session = debug('start')['debug_session']
        payload = area / 'debug-input.json'
        content = '  Þóra\r\n\nPublic observation.  '
        payload.write_text(json.dumps({'events': [{
            'operation': 'context.read', 'content': content,
            'files': [{'path': 'notebook/project.md', 'phase': 'context'}]}]}, ensure_ascii=False), encoding='utf-8')
        debug('record', '--debug-session', session, '--input', payload)
        debug('stop', '--debug-session', session)
        output = area / 'debug-report.zip'
        debug('export', '--debug-session', session, '--output', output)
        with zipfile.ZipFile(output) as report:
            self.assertIn('report.md', report.namelist())
            events = [json.loads(line) for line in report.read('events.jsonl').decode('utf-8').splitlines()]
            self.assertTrue(any(event['operation'] == 'context.read' for event in events))
            self.assertTrue(any(json.loads(report.read(name)) == content
                                for name in report.namelist() if name.startswith('attachments/')
                                and name.endswith('.json')))
        self.assertEqual(run(['git', '-C', root, 'status', '--porcelain'], cwd=area, env=env), before)


if __name__ == '__main__':
    unittest.main()
