from importlib.resources import files
from pathlib import Path
import unittest


class GettingStarted(unittest.TestCase):
    def test_missing_old_novel_fallback_has_a_diagnostic(self):
        from novel_creator.cli import ToolError
        from novel_creator.install import _command_result
        from unittest.mock import Mock, patch
        manifest = Mock()
        manifest.read_bytes.return_value = b'{"checksums":{}}'
        missing = Mock()
        missing.joinpath.return_value = Path('/nonexistent-novel-guide-fixture/getting-started.md')
        result = {'warnings': [], 'data': {'saved': True, 'cleanup_required': False, 'already_initialized': True}}
        with patch('novel_creator.install.storage.safe_path', return_value=manifest), \
             patch('novel_creator.install.files', return_value=missing):
            with self.assertRaises(ToolError) as failed:
                _command_result(Path.cwd(), result)
        self.assertEqual(failed.exception.code, 4)
        self.assertIn('documentation', str(failed.exception))

    def test_complete_shipped_guide_and_readme_discovery(self):
        guide = files('novel_creator.workflows').joinpath('getting-started.md').read_text(encoding='utf-8')
        for text in ['PowerShell', 'Bash', 'pip install', '$novel-init', '$novel-resume',
                     'inspect', '--language', '--title', '--path', 'command not found',
                     'Git identity', 'permissions', 'interrupted', 'no story idea']:
            with self.subTest(text=text):
                self.assertIn(text.lower(), guide.lower())
        root = Path(__file__).resolve().parents[2]
        self.assertIn('workflows/getting-started.md', (root / 'README.md').read_text(encoding='utf-8'))

    def test_supported_shells_have_copyable_sections(self):
        guide = files('novel_creator.workflows').joinpath('getting-started.md').read_text(encoding='utf-8')
        self.assertIn('```powershell', guide)
        self.assertIn('```bash', guide)
        self.assertIn('sys.executable', guide)
