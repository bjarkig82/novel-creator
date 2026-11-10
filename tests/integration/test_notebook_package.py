"""Install both built distributions offline and initialize outside the checkout."""
import os
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
            with zipfile.ZipFile(wheel) as archive:
                for relative, (_, member) in resources.items():
                    self.assertEqual(archive.read(member), expected[relative], member)
            with tarfile.open(sdist, 'r:gz') as archive:
                prefix = sdist.name.removesuffix('.tar.gz')
                for relative, (source, _) in resources.items():
                    member = prefix + '/' + source.relative_to(checkout).as_posix()
                    stream = archive.extractfile(member)
                    self.assertIsNotNone(stream, member)
                    with stream:
                        self.assertEqual(stream.read(), expected[relative], member)
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
                    print(f'{label}: {len(resources)} artifact resources match source bytes; '
                          'isolated install and en/is notebook resource checks passed')


if __name__ == '__main__':
    unittest.main()
