import json
import unittest
from novel_creator import storage
from novel_creator.cli import ToolError
from tests.helpers import envelope, repository, git, FailAt


class RecoveryTests(unittest.TestCase):
    def test_pending_inspection_and_unchanged_retry(self):
        with repository() as root:
            bundle = envelope(root)
            before = storage.head(root)
            with self.assertRaises(ToolError):
                storage.save(root, bundle, fault=FailAt('after_file'))
            report = storage.recover(root, bundle['exchange_id'])
            self.assertEqual(report['data']['state'], 'pending')
            self.assertEqual(report['checkpoint']['git_head'], before)
            with self.assertRaises(ToolError) as error:
                storage.recover(root, bundle['exchange_id'], retry=True, expected_head='0' * 40)
            self.assertEqual(error.exception.code, 3)
            saved = storage.recover(root, bundle['exchange_id'], retry=True, expected_head=before)
            self.assertTrue(saved['data']['saved'])
            self.assertEqual(storage.read_history(root), [bundle])

    def test_published_cleanup_preserves_unrelated_index_and_does_not_replay(self):
        with repository() as root:
            first = envelope(root)
            saved = storage.save(root, first, fault=FailAt('before_cleanup'))
            self.assertTrue(saved['data']['cleanup_required'])
            (root / 'chapter.md').write_bytes(b'Approved manuscript')
            git(root, 'add', '--', 'chapter.md')
            unrelated = storage.index_entries(root, ['chapter.md'])
            report = storage.recover(root, first['exchange_id'])
            self.assertEqual(report['data']['state'], 'cleanup_needed')
            head = storage.head(root)
            recovered = storage.recover(root, first['exchange_id'], retry=True, expected_head=head)
            self.assertFalse(recovered['data']['cleanup_required'])
            self.assertEqual(storage.head(root), head)
            self.assertEqual(storage.index_entries(root, ['chapter.md']), unrelated)
            self.assertEqual(storage.read_history(root), [first])
            following = envelope(root, previous=first)
            self.assertTrue(storage.save(root, following)['data']['saved'])

    def test_lost_receipt_reconstructs_published_cleanup_without_replay(self):
        with repository() as root:
            bundle = envelope(root)
            storage.save(root, bundle, fault=FailAt('after_ref'))
            (root / f".novel-creator/local/{bundle['exchange_id']}.json").unlink()
            head = storage.head(root)
            report = storage.recover(root, bundle['exchange_id'], retry=True, expected_head=head)
            self.assertFalse(report['data']['cleanup_required'])
            self.assertEqual(storage.head(root), head)
            self.assertEqual(git(root, 'status', '--porcelain'), '')

    def test_lock_is_disclosed_and_never_removed(self):
        with repository() as root:
            bundle = envelope(root)
            storage.save(root, bundle)
            lock = root / '.novel-creator/local/write.lock'
            lock.mkdir()
            report = storage.recover(root, bundle['exchange_id'])
            self.assertTrue(report['data']['writer_lock_held'])
            with self.assertRaises(ToolError) as error:
                storage.recover(root, bundle['exchange_id'], retry=True, expected_head=storage.head(root))
            self.assertEqual(error.exception.code, 6)
            self.assertTrue(lock.is_dir())

    def test_changed_pending_file_is_not_overwritten(self):
        with repository() as root:
            bundle = envelope(root)
            with self.assertRaises(ToolError):
                storage.save(root, bundle, fault=FailAt('after_file'))
            path = root / storage.bundle_path(bundle)
            original = path.read_bytes()
            path.write_bytes(original + b'changed')
            with self.assertRaises(ToolError):
                storage.recover(root, bundle['exchange_id'], retry=True, expected_head=storage.head(root))
            self.assertEqual(path.read_bytes(), original + b'changed')
