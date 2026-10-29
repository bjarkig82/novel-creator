import json
from pathlib import Path
import tempfile
import unittest

from novel_creator import storage, validation
from novel_creator.install import initialize
from tests.helpers import git


class SimpleInitialization(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'Bréf'
        self.root.mkdir()
        git(self.root, 'init', '-b', 'main')
        git(self.root, 'config', 'user.name', 'Disposable Init')
        git(self.root, 'config', 'user.email', 'init@example.invalid')
        self.request = dict(request_type='cli_init_v1', name='Bréf',
                            resolved_destination=str(self.root), title_argument=None, language_argument=None)

    def test_request_is_saved_without_creative_invention(self):
        result = initialize(self.root, '{"title":"Bréf"}', request=self.request)
        self.assertTrue(result['data']['ready'])
        self.assertTrue(Path(result['data']['getting_started_path']).is_file())
        history = storage.read_history(self.root)
        self.assertEqual(history[0]['input_artifacts'][1]['parsed_value'], self.request)
        project = validation.validate_exchange(history[0], [])[result['novel_id']]
        self.assertEqual(project['title']['original_text'], 'Bréf')
        self.assertEqual(project['manuscript_language'], 'en')
        self.assertEqual(project['original_concept']['state'], 'unknown')
        self.assertFalse(history[0]['messages'])
        before = git(self.root, 'rev-parse', 'HEAD')
        again = initialize(self.root, '{}', request=self.request)
        self.assertTrue(again['data']['already_initialized'])
        self.assertEqual(git(self.root, 'rev-parse', 'HEAD'), before)
        manifest = json.loads((self.root / '.novel-creator/manifest.json').read_text())
        from novel_creator import __version__
        self.assertEqual(manifest['bundle_version'], __version__)
