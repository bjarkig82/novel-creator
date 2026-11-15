"""Focused wheel/sdist installs and offline previous-public feature upgrades."""
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
import venv
import zipfile

from tests.release_fixtures import published_wheel
from tests.verify_plugin_install import temporary_environment, run


PROBE = r'''
import json,sys
from pathlib import Path
from unittest.mock import patch
import novel_creator
from novel_creator import notebook, notebook_side_character, storage, update, update_release
from novel_creator.install import initialize
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))
area, previous_python, wheel, previous_wheel, checkout = map(Path, sys.argv[1:])
sys.path.append(str(checkout))
from tests.update_release_helpers import release_listing
from tests.verify_plugin_install import run
from tests.verify_marketplace_previous import initialize_legacy_fixture
import os
env = dict(os.environ)

def git(root, *args):
    return run(['git', '-C', root, *args], cwd=area, env=env)

def legacy(python, root):
    initialize_legacy_fixture(python, root, 'en', area, env)

def check(root, legacy=False, host='codex', source='project'):
    base = '.novel-creator' if legacy else '.novel-notebook'
    assert (root / base / 'workflows/side-character.md').is_file()
    roots = ('AGENTS.md','CLAUDE.md') if host == 'both' else ('AGENTS.md' if host == 'codex' else 'CLAUDE.md',)
    for name in roots:
        assert b'novel-side-character' in (root / name).read_bytes()
    for selected in (('codex','claude') if host == 'both' else (host,)):
        path = root / ('.agents' if selected == 'codex' else '.claude') / 'skills/novel-side-character/SKILL.md'
        assert path.is_file() == (source == 'project')
        if path.is_file():
            import re
            for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text(encoding='utf-8')):
                assert (path.parent / link).resolve().is_file(), link
    if legacy:
        assert not (root / '.novel-creator/src/novel_creator/notebook_side_character.py').exists()
        assert not (root / '.novel-creator/src/novel_creator/notebook.py').exists()

new = area / 'new-legacy'
legacy(sys.executable, new)
check(new, legacy=True)
for host,source,language in [('codex','project','en'),('both','plugin','is')]:
    root = area / ('new-' + host)
    notebook.initialize(root,host=host,skill_source=source,language=language)
    check(root,host=host,source=source)

for host,source,language in [('codex','project','en'),('claude','project','is'),('both','plugin','en')]:
    root = area / ('old-' + host)
    code = 'import sys;from novel_creator.notebook import initialize;initialize(sys.argv[1],host=sys.argv[2],skill_source=sys.argv[3],language=sys.argv[4])'
    run([previous_python,'-I','-B','-c',code,root,host,source,language],cwd=area,env=env)
    roots = ('AGENTS.md','CLAUDE.md') if host == 'both' else ('AGENTS.md' if host == 'codex' else 'CLAUDE.md',)
    original = {}
    for name in roots:
        p=root/name;p.write_bytes(p.read_bytes()+b'\n## Writer directions\nKeep custom writer instructions.\n');original[name]=p.read_bytes()
    (root/'writer.txt').write_bytes(b'staged');git(root,'add','writer.txt');(root/'writer.txt').write_bytes(b'working')
    index=(root/'.git/index').read_bytes();head=git(root,'rev-parse','HEAD')
    story={str(p.relative_to(root)):p.read_bytes() for p in (root/'notebook').rglob('*.md')}
    before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
    helper=notebook if host=='codex' else notebook_side_character
    preview=helper.update(root)['data']
    assert before=={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
    result=helper.update(root,apply=True,preview_id=preview['preview_id'],expected_head=preview['reviewed_head'])['data']
    assert result['ready'];assert helper.update(root)['data']['already_current']
    assert (root/'.git/index').read_bytes()==index and git(root,'rev-parse','HEAD')==head
    assert (root/'writer.txt').read_bytes()==b'working'
    for name,raw in story.items():assert (root/name).read_bytes()==raw
    for name,raw in original.items():assert (root/name).read_bytes().startswith(raw)
    check(root,host=host,source=source)

root=area/'old-legacy'
legacy(previous_python,root)
assert json.loads((root/'.novel-creator/manifest.json').read_bytes())['bundle_version']=='0.10.1'
(root/'writer.txt').write_bytes(b'staged');git(root,'add','writer.txt');(root/'writer.txt').write_bytes(b'working')
root_instructions=(root/'AGENTS.md').read_bytes()+b'\nKeep custom writer directions.\n'
(root/'AGENTS.md').write_bytes(root_instructions)
history=storage.read_history(root);head=storage.head(root);staged=storage.index_entries(root,['writer.txt'])
story={str(p.relative_to(root)):p.read_bytes() for p in (root/'story').rglob('*') if p.is_file()}
transport=release_listing({'0.10.1':previous_wheel.read_bytes(),'0.10.2':wheel.read_bytes()})
with patch.object(update_release,'cache_home',return_value=area/'release-cache'):
    preview=update.preview(root,version='0.10.2',python=sys.executable,transport=transport)['data']
    assert not preview['blockers'],preview
    result=update.apply(root,preview_id=preview['preview_id'],version='0.10.2',expected_head=preview['reviewed_head'])
    assert result['data']['ready'],result
assert git(root,'rev-parse','HEAD^').strip()==head
assert storage.read_history(root)==history and storage.index_entries(root,['writer.txt'])==staged
assert (root/'AGENTS.md').read_bytes()==root_instructions
assert (root/'writer.txt').read_bytes()==b'working'
for name,raw in story.items():assert (root/name).read_bytes()==raw
# Custom root is protected, so legacy routing comes through its managed skill/workflow.
assert (root/'.agents/skills/novel-side-character/SKILL.md').is_file()
assert (root/'.novel-creator/workflows/side-character.md').is_file()
assert not (root/'.novel-creator/src/novel_creator/notebook_side_character.py').exists()
print(json.dumps(dict(ok=True,new_legacy=True,new_notebooks=2,previous_legacy='0.10.1->0.10.2',previous_notebooks=3,story_history_custom_staging_preserved=True)))
'''


class SideCharacterPackage(unittest.TestCase):
    def test_notebook_only_modules_are_not_legacy_exports(self):
        from novel_creator.install import bundle_files
        from novel_creator.update_release import bundle_inventory
        inventory = {'novel_creator/notebook.py': b'notebook',
                     'novel_creator/notebook_side_character.py': b'external notebook helper',
                     'novel_creator/ordinary.py': b'ordinary runtime'}
        derived = bundle_inventory(inventory)
        bundled = bundle_files()
        for name in ('notebook.py', 'notebook_side_character.py'):
            relative = '.novel-creator/src/novel_creator/' + name
            self.assertNotIn(relative, derived)
            self.assertNotIn(relative, bundled)
        self.assertEqual(derived['.novel-creator/src/novel_creator/ordinary.py'], b'ordinary runtime')

    def test_built_artifacts_and_installed_previous_public_upgrades(self):
        checkout = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory(prefix='side-character-package-') as directory:
            scratch = Path(directory).resolve()
            env = temporary_environment(scratch)
            env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PIP_NO_INDEX='1',
                       PIP_DISABLE_PIP_VERSION_CHECK='1', PIP_CONFIG_FILE=os.devnull)
            artifacts = scratch / 'artifacts'
            artifacts.mkdir()
            run([sys.executable, '-B', '-c', 'from setuptools.build_meta import build_wheel,build_sdist;'
                 'import sys;destination=sys.argv[1];build_wheel(destination);build_sdist(destination)', artifacts], cwd=checkout, env=env)
            wheel = next(artifacts.glob('*.whl'))
            sdist = next(artifacts.glob('*.tar.gz'))
            members = {
                'src/novel_creator/notebook_side_character.py': 'novel_creator/notebook_side_character.py',
                'workflows/side-character.md': 'novel_creator/workflows/side-character.md',
                'notebook/workflows/side-character.md': 'novel_creator/notebook_resources/workflows/side-character.md',
                'adapters/codex/skills/novel-side-character/SKILL.md': 'novel_creator/codex/skills/novel-side-character/SKILL.md',
                'adapters/codex/notebook/skills/novel-side-character/SKILL.md': 'novel_creator/codex/notebook/skills/novel-side-character/SKILL.md',
            }
            with zipfile.ZipFile(wheel) as archive:
                for source, member in members.items():
                    self.assertEqual(archive.read(member), (checkout / source).read_bytes())
            with tarfile.open(sdist) as archive:
                prefix = sdist.name.removesuffix('.tar.gz')
                for source in (*members, 'plugins/novel-creator/skills/novel-side-character/SKILL.md'):
                    self.assertEqual(archive.extractfile(prefix + '/' + source).read(), (checkout / source).read_bytes())

            def install(path, artifact):
                venv.EnvBuilder(with_pip=False).create(path)
                python = path / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
                site = Path(run([python, '-I', '-c', "import sysconfig;print(sysconfig.get_path('purelib'))"], cwd=scratch, env=env).strip())
                dependencies = dict.fromkeys(str(Path(p).absolute()) for p in sys.path if Path(p).name in ('site-packages','dist-packages'))
                (site / 'dependencies.pth').write_text(''.join(p + '\n' for p in dependencies), encoding='utf-8')
                run([sys.executable, '-I', '-m', 'pip', '--isolated', '--python', python, 'install', '--no-index',
                     '--no-deps', '--no-build-isolation', '--no-cache-dir', artifact], cwd=scratch, env=env)
                return python

            previous_wheel = published_wheel('0.10.1')
            previous_python = install(scratch / 'previous-environment', previous_wheel)
            probe = scratch / 'probe.py'
            probe.write_text(PROBE, encoding='utf-8')
            for label, artifact in (('wheel', wheel), ('sdist', sdist)):
                with self.subTest(artifact=label):
                    python = install(scratch / (label + '-environment'), artifact)
                    area = scratch / (label + '-books')
                    area.mkdir()
                    result = run([python, '-I', '-B', probe, area, previous_python, wheel,
                                  previous_wheel, checkout], cwd=area, env=env)
                    print(label + ': ' + result.strip(), flush=True)


if __name__ == '__main__':
    unittest.main()
