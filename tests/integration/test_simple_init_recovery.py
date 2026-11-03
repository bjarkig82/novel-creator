import copy
import json
from unittest.mock import patch

from novel_creator.cli import ToolError
from novel_creator.install import initialize
from novel_creator import storage
from tests.helpers import FailAt, git
from tests.integration.test_simple_initialize import SimpleInitialization


class SimpleRecovery(SimpleInitialization):
    def test_competing_reservations_preserve_one_original_state(self):
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        from novel_creator.install import _reserve_setup
        path = self.root / '.novel-creator/local/setup/state.json'
        path.parent.mkdir(parents=True)
        barrier = Barrier(2)
        def reserve(number):
            barrier.wait(timeout=10)
            try:
                _reserve_setup(path, {'owner': number})
                return number, 0
            except ToolError as error:
                return number, error.code
        with ThreadPoolExecutor(max_workers=2) as workers:
            outcomes = list(workers.map(reserve, [1, 2]))
        winners = [number for number, code in outcomes if code == 0]
        self.assertEqual(len(winners), 1)
        self.assertTrue(all(code in (0, 3, 6) for _, code in outcomes))
        self.assertEqual(json.loads(path.read_text()), {'owner': winners[0]})

    def test_request_change_cannot_reuse_the_same_brief(self):
        with self.assertRaises(ToolError):
            initialize(self.root, '{"title":"Bréf"}', request=self.request, fault=FailAt('before_ref'))
        state = json.loads((self.root / '.novel-creator/local/setup/state.json').read_text())
        changed = dict(self.request, name='Different name')
        with self.assertRaises(ToolError) as conflict:
            initialize(self.root, '{"title":"Bréf"}', request=changed)
        self.assertEqual(conflict.exception.code, 3)
        with self.assertRaises(ToolError):
            initialize(self.root, '{"title":"Bréf"}')
        result = initialize(self.root / '.', '{"title":"Bréf"}', request=dict(reversed(list(self.request.items()))))
        self.assertEqual(result['checkpoint']['exchange_id'], state['bundle']['exchange_id'])
        self.assertEqual(len(storage.read_history(self.root)), 1)

    def test_published_cleanup_is_saved_but_not_ready(self):
        result = initialize(self.root, '{}', request=self.request, fault=FailAt('before_cleanup'))
        self.assertTrue(result['data']['saved'])
        self.assertFalse(result['data']['ready'])
        self.assertIn('recover', result['data']['next_action'])

    def test_old_manifest_without_guide_uses_package_without_novel_changes(self):
        from novel_creator.install import bundle_files
        old_files = bundle_files()
        old_files.pop('.novel-creator/workflows/getting-started.md')
        with patch('novel_creator.install.bundle_files', return_value=old_files):
            initialize(self.root, '{}')
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*')
                  if p.is_file() and '.git' not in p.relative_to(self.root).parts}
        head = git(self.root, 'rev-parse', 'HEAD')
        result = initialize(self.root, '{}', request=self.request)
        self.assertTrue(result['data']['ready'])
        self.assertIn('Package-guide fallback', ' '.join(result['warnings']))
        self.assertFalse((self.root / '.novel-creator/workflows/getting-started.md').exists())
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*')
                 if p.is_file() and '.git' not in p.relative_to(self.root).parts}
        self.assertEqual(before, after)
        self.assertEqual(head, git(self.root, 'rev-parse', 'HEAD'))
