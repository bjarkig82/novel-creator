import json
from pathlib import Path
import tempfile
import unittest

from novel_creator import install, storage
from tests.helpers import git


class OwnershipTests(unittest.TestCase):
    def test_new_format_separates_shared_files_and_continuation_preserves_custom_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'Book'
            root.mkdir()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Disposable Test')
            git(root, 'config', 'user.email', 'test@example.invalid')
            install.initialize(root, '{}')
            manifest = json.loads((root / '.novel-creator/manifest.json').read_bytes())
            self.assertEqual(manifest['installation_format'], 2)
            for name in ('AGENTS.md', '.gitignore', '.gitattributes'):
                self.assertNotIn(name, manifest['checksums'])
                self.assertIn(name, manifest['ownership']['shared'])
                self.assertIn(name, storage.committed_entries(root, storage.head(root)))
            (root / 'AGENTS.md').write_bytes(b'# Custom writing instructions\n')
            self.assertFalse(install.initialize(root, '{}')['data']['cleanup_required'])
            self.assertEqual((root / 'AGENTS.md').read_bytes(), b'# Custom writing instructions\n')
