"""Portable manifests and cached skills are standalone marketplace artifacts."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / 'plugins/novel-creator'


class PluginBundleTests(unittest.TestCase):
    def test_entry_inventory_and_cache_relative_routing(self):
        expected = {p.parent.name for p in (ROOT / 'adapters/codex/notebook/skills').glob('*/SKILL.md')} | {'setup'}
        actual = {p.parent.name for p in (PLUGIN / 'skills').glob('*/SKILL.md')}
        self.assertEqual(actual, expected)
        for path in (PLUGIN / 'skills').glob('*/SKILL.md'):
            text = path.read_text()
            self.assertRegex(text, r'\ndescription: Use when ')
            self.assertNotIn('../../../.novel-notebook', text)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                self.assertTrue((path.parent / target).is_file(), (path, target))
            if path.parent.name != 'setup':
                self.assertIn('../../references/notebook.md', text)
                self.assertIn('novel_path', text)

    def test_routing_and_creative_contracts(self):
        ref = (PLUGIN / 'references/notebook.md').read_text()
        for term in ('integration.json', '"version": 1', 'skill_source', 'plugin',
                     'notebook/project.md', 'notebook/working-summary.md', 'story content',
                     'actual', 'enabled', 'snapshot', '$novel-creator:', '/novel-creator:'):
            self.assertIn(term, ref)
        self.assertNotIn('`.agents/skills/`', ref)
        for name in ('novel-analyze', 'novel-help'):
            text = (PLUGIN / f'skills/{name}/SKILL.md').read_text()
            for term in ('read-only', 'notes', 'checkpoints'):
                self.assertIn(term, text)
        clarify = (PLUGIN / 'skills/novel-clarify/SKILL.md').read_text()
        for term in ('one question at a time', 'suggested answers', 'custom', 'clear answers'):
            self.assertIn(term, clarify)
        self.assertIn('explicit', (PLUGIN / 'skills/novel-outline/SKILL.md').read_text())

    def test_setup_contract(self):
        text = (PLUGIN / 'skills/setup/SKILL.md').read_text()
        for term in ('3.11', '2.39', 'runtime_python', '--host both', '--skill-source plugin',
                     '--json', '--language', 'Git identity', 'same chat', 'activation',
                     'existing', 'partial', 'Windows', 'Linux'):
            self.assertIn(term, text)

    def test_generated_manifests_catalogs_and_archives(self):
        script = ROOT / 'scripts/build_plugins.py'
        self.assertTrue(script.is_file(), 'Plugin builder is missing')
        checked = subprocess.run([sys.executable, str(script), '--check'], capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        version = re.search(r'__version__ = "([^"]+)"', (ROOT / 'src/novel_creator/__init__.py').read_text())[1]
        manifest = json.loads((PLUGIN / 'plugin.json').read_text())
        self.assertEqual(manifest['version'], version)
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertEqual(manifest['extensions']['com.openai']['onboardingSkill'], './skills/setup/SKILL.md')
        self.assertEqual(json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())['version'], version)
        for location in ('.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
            catalog = json.loads((ROOT / location).read_text())
            self.assertEqual(catalog['name'], 'novel-creator-marketplace')
            self.assertEqual(catalog['plugins'][0]['name'], 'novel-creator')
        codex = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(codex['plugins'][0]['source'], {'source': 'local', 'path': './plugins/novel-creator'})
        self.assertEqual(codex['plugins'][0]['policy'], {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'})
        self.assertEqual(codex['plugins'][0]['category'], 'Productivity')
        claude = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(claude['owner'], {'name': 'bjarkig82'})
        self.assertEqual(claude['plugins'][0]['source'], './plugins/novel-creator')
        self.assertEqual(claude['plugins'][0]['version'], version)
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run([sys.executable, str(script), '--output', temporary], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for suffix in ('plugin', 'marketplace'):
                path = Path(temporary) / f'novel-creator-{suffix}-{version}.zip'
                with zipfile.ZipFile(path) as archive:
                    names = archive.namelist()
                    prefix = '' if suffix == 'plugin' else 'plugins/novel-creator/'
                    self.assertIn(prefix + 'plugin.json', names)
                    self.assertIn(prefix + 'scripts/bootstrap.py', names)
                    self.assertEqual(sum(n.endswith('/SKILL.md') for n in names), 15)
                    if suffix == 'marketplace':
                        self.assertIn('.agents/plugins/marketplace.json', names)
                        self.assertIn('.claude-plugin/marketplace.json', names)
                    self.assertFalse(any('__pycache__' in n or n.startswith('/') or '.pyc' in n for n in names))

    def test_source_distribution_includes_rebuild_inputs(self):
        manifest = (ROOT / 'MANIFEST.in').read_text()
        for path in ('plugins', 'scripts/build_plugins.py', '.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
            self.assertIn(path, manifest)

    def test_version_drift_is_detected_without_rewriting_manifests(self):
        with tempfile.TemporaryDirectory() as temporary:
            clean = Path(temporary)
            for name in ('scripts/build_plugins.py', 'src/novel_creator/__init__.py',
                         'plugins/novel-creator/plugin.json', 'plugins/novel-creator/.claude-plugin/plugin.json',
                         '.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
                path = clean / name
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, path)
            version_file = clean / 'src/novel_creator/__init__.py'
            version_file.write_text('__version__ = "99.0.0"\n')
            result = subprocess.run([sys.executable, str(clean / 'scripts/build_plugins.py'), '--check'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('drift', result.stderr)
            self.assertNotEqual(json.loads((clean / 'plugins/novel-creator/plugin.json').read_text())['version'], '99.0.0')
            self.assertFalse((clean / 'dist').exists())

    def test_actual_sdist_rebuilds_plugin_and_wheel_contains_claude(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            clean = base / 'source'
            clean.mkdir()
            for name in ('pyproject.toml', 'README.md', 'MANIFEST.in'):
                shutil.copyfile(ROOT / name, clean / name)
            for name in ('src', 'schemas', 'workflows', 'languages', 'adapters', 'notebook',
                         'plugins', 'scripts', '.agents', '.claude-plugin'):
                shutil.copytree(ROOT / name, clean / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            output = base / 'artifacts'
            output.mkdir()
            code = 'from setuptools.build_meta import build_sdist, build_wheel; build_sdist(' + repr(str(output)) + '); build_wheel(' + repr(str(output)) + ')'
            result = subprocess.run([sys.executable, '-c', code], cwd=clean, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            source = next(output.glob('*.tar.gz'))
            unpacked = base / 'unpacked'
            unpacked.mkdir()
            with tarfile.open(source) as archive:
                names = archive.getnames()
                prefix = names[0].split('/')[0] + '/'
                for name in ('plugins/novel-creator/plugin.json', 'plugins/novel-creator/.claude-plugin/plugin.json',
                             'plugins/novel-creator/scripts/bootstrap.py', 'scripts/build_plugins.py',
                             '.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json'):
                    self.assertIn(prefix + name, names)
                self.assertEqual(sum('/plugins/novel-creator/skills/' in name and name.endswith('/SKILL.md') for name in names), 15)
                for member in archive.getmembers():
                    self.assertFalse(member.issym() or member.islnk())
                    self.assertNotIn('..', Path(member.name).parts)
                    self.assertFalse(Path(member.name).is_absolute())
                    if member.isfile():
                        target = unpacked / member.name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(archive.extractfile(member).read())
            rebuilt = subprocess.run([sys.executable, str(unpacked / prefix / 'scripts/build_plugins.py'), '--output', str(base / 'rebuilt')],
                                     capture_output=True, text=True)
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stdout + rebuilt.stderr)
            with zipfile.ZipFile(next((base / 'rebuilt').glob('*-plugin-*.zip'))) as archive:
                self.assertIn('scripts/bootstrap.py', archive.namelist())
            with zipfile.ZipFile(next(output.glob('*.whl'))) as archive:
                self.assertIn('novel_creator/claude/notebook/CLAUDE.fragment.md', archive.namelist())
                self.assertFalse(any('/plugins/novel-creator/' in name for name in archive.namelist()))
