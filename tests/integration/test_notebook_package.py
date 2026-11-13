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
                    print(f'{label}: {len(resources)} artifact resources match source bytes; '
                          'isolated install and en/is notebook resource checks passed')

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
