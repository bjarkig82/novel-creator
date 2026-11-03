import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from novel_creator import records, storage
from novel_creator.cli import ToolError
from tests.helpers import git


class InstallationTests(unittest.TestCase):
    def test_shorthand_replacement_options_do_not_mutate_recognized_novel(self):
        from novel_creator.install import initialize
        request = dict(request_type='cli_init_v1', name='Novel', resolved_destination=str(self.root),
                       title_argument='Original', language_argument='is')
        first = initialize(self.root, '{"title":"Original","manuscript_language":"is"}', request=request)
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*')
                  if p.is_file() and '.git' not in p.relative_to(self.root).parts}
        second = initialize(self.root, '{"title":"Replacement"}', request=dict(request, title_argument='Replacement'))
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*')
                 if p.is_file() and '.git' not in p.relative_to(self.root).parts}
        self.assertEqual(first['checkpoint'], second['checkpoint'])
        self.assertEqual(before, after)
        self.assertTrue(second['data']['already_initialized'])
        self.assertIn('not applied', ' '.join(second['warnings']))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name).resolve()
        self.root = self.parent / 'novel'
        self.root.mkdir()
        git(self.root, 'init', '-b', 'main')
        git(self.root, 'config', 'user.name', 'Installation Test')
        git(self.root, 'config', 'user.email', 'install@example.invalid')

    def install(self, brief=None, **kwargs):
        from novel_creator.install import initialize
        raw = json.dumps({} if brief is None else brief, ensure_ascii=False)
        return initialize(self.root, raw, **kwargs)

    def test_independent_pinned_install_and_recognized_continuation(self):
        result = self.install({'title': 'Þóra'})
        self.assertEqual(result['operation'], 'init')
        self.assertTrue(result['data']['saved'])
        self.assertFalse(result['data']['cleanup_required'])
        self.assertTrue(result['data']['brainstorming_optional'])
        manifest = records.loads((self.root / '.novel-creator/manifest.json').read_bytes())
        self.assertFalse(manifest.get('fixture_only', False))
        for relative, digest in manifest['checksums'].items():
            self.assertEqual(hashlib.sha256((self.root / relative).read_bytes()).hexdigest(), digest)
        env = dict(os.environ, PYTHONPATH='')
        for command in [('context',), ('validate',)]:
            output = subprocess.run([sys.executable, '-B', str(self.root / '.novel-creator/run.py'),
                *command, '--novel', str(self.root), '--json'], cwd=self.parent, env=env,
                capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(output.returncode, 0, output.stderr)
            self.assertEqual(json.loads(output.stdout)['novel_id'], result['novel_id'])
        before = git(self.root, 'rev-parse', 'HEAD')
        again = self.install({'title': 'Do not replace'})
        self.assertEqual(again['novel_id'], result['novel_id'])
        self.assertTrue(again['data']['already_initialized'])
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), before)
        self.assertEqual(git(self.root, 'status', '--porcelain'), '')

    def test_crlf_framework_resources_install_as_lf_without_changing_original_brief(self):
        from novel_creator import install
        original = install.files
        class Resource:
            def __init__(self, value):
                self.value = value
            def __getattr__(self, name):
                return getattr(self.value, name)
            def iterdir(self):
                return [Resource(child) for child in self.value.iterdir()]
            def joinpath(self, *parts):
                return Resource(self.value.joinpath(*parts))
            def read_bytes(self):
                return self.value.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
        brief = 'Þóra\r\nOriginal concept.'
        with patch.object(install, 'files', side_effect=lambda name: Resource(original(name))):
            self.install({'original_concept': brief})
        self.assertNotIn(b'\r\n', (self.root / '.novel-creator/workflows/entry.md').read_bytes())
        self.assertNotIn(b'\r\n', (self.root / '.agents/skills/novel-init/SKILL.md').read_bytes())
        project = next(r for r in records.fold(storage.read_history(self.root)).values() if r['kind'] == 'novel_project')
        self.assertEqual(project['original_concept']['original_text'], brief)
        self.assertEqual(git(self.root, 'status', '--porcelain'), '')

    def test_existing_instructions_preserved_and_unrelated_content_refused(self):
        (self.root / 'AGENTS.md').write_bytes(b'# Existing instructions\r\n')
        self.install()
        self.assertEqual((self.root / 'AGENTS.md').read_bytes(), b'# Existing instructions\r\n')
        other = self.parent / 'occupied'
        other.mkdir()
        manuscript = other / 'chapter.md'
        manuscript.write_bytes(b'Approved manuscript')
        from novel_creator.install import initialize
        with self.assertRaises(ToolError) as error:
            initialize(other, '{}')
        self.assertEqual(error.exception.code, 3)
        self.assertEqual(manuscript.read_bytes(), b'Approved manuscript')
        self.assertFalse((other / '.git').exists())

    def test_nested_repository_is_refused_without_changes(self):
        from novel_creator.install import initialize
        child = self.root / 'nested'
        with self.assertRaises(ToolError) as error:
            initialize(child, '{}')
        self.assertEqual(error.exception.code, 3)
        self.assertFalse(child.exists())

    def test_interrupted_bootstrap_retries_exact_original_payload(self):
        from tests.helpers import FailAt
        with self.assertRaises(ToolError) as error:
            self.install({'original_concept': 'Þóra\n'}, fault=FailAt('after_file'))
        self.assertEqual(error.exception.code, 5)
        self.assertIsNone(storage.head(self.root))
        state_path = self.root / '.novel-creator/local/setup/state.json'
        before = records.loads(state_path.read_bytes())
        recovered = self.install({'original_concept': 'Þóra\n'})
        history = storage.read_history(self.root)
        self.assertEqual(history, [before['bundle']])
        self.assertEqual(recovered['checkpoint']['exchange_id'], before['bundle']['exchange_id'])
        self.assertFalse(recovered['data']['cleanup_required'])

    def test_partial_retry_refuses_changed_brief_and_managed_files(self):
        from tests.helpers import FailAt
        with self.assertRaises(ToolError):
            self.install(fault=FailAt('before_file'))
        with self.assertRaises(ToolError) as error:
            self.install({'title': 'Changed'})
        self.assertEqual(error.exception.code, 3)
        launcher = self.root / '.novel-creator/run.py'
        launcher.write_text('# changed', encoding='utf-8')
        with self.assertRaises(ToolError) as error:
            self.install()
        self.assertEqual(error.exception.code, 3)
        self.assertEqual(launcher.read_text(), '# changed')

    def test_recognized_novel_does_not_hide_published_cleanup(self):
        from tests.helpers import FailAt
        saved = self.install(fault=FailAt('before_cleanup'))
        self.assertTrue(saved['data']['cleanup_required'])
        again = self.install()
        self.assertTrue(again['data']['cleanup_required'])
        self.assertIn('recover', again['data']['next_action'])

    def test_missing_identity_does_not_install(self):
        from novel_creator.install import initialize
        original = storage.git
        def denied(root, *args, **kwargs):
            if args and args[0] == 'var':
                raise ToolError(5, 'Missing identity')
            return original(root, *args, **kwargs)
        with patch.object(storage, 'git', side_effect=denied), self.assertRaises(ToolError):
            initialize(self.root, '{}')
        self.assertFalse((self.root / '.novel-creator').exists())

    def test_new_directory_creates_independent_repository_using_existing_identity(self):
        from novel_creator.install import initialize
        home = self.parent / 'isolated-home'
        home.mkdir()
        (home / '.gitconfig').write_text('[user]\nname = Isolated Test\nemail = isolated@example.invalid\n', encoding='utf-8')
        target = self.parent / 'brand-new'
        with patch.dict(os.environ, HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / 'config')):
            result = initialize(target, '{}')
        self.assertTrue(result['data']['saved'])
        self.assertEqual(Path(git(target, 'rev-parse', '--show-toplevel')).resolve(), target)
        self.assertTrue((target / '.git').is_dir())
        self.assertEqual(git(target, 'status', '--porcelain'), '')
