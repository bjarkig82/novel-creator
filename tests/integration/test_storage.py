import hashlib
import json
import os
from pathlib import Path
import unittest

from novel_creator import storage
from novel_creator.cli import ToolError
from tests.helpers import repository, git, envelope, seal, FailAt, uid


class StorageTests(unittest.TestCase):
    def test_private_index_preserves_unrelated_staged_and_manuscript(self):
        with repository() as root:
            manuscript = root / 'chapter.md'
            manuscript.write_text('Approved Þóra text')
            git(root, 'add', 'chapter.md')
            baseline = git(root, 'ls-files', '--stage', '--', 'chapter.md')
            original = hashlib.sha256(manuscript.read_bytes()).hexdigest()
            data = envelope(root)
            result = storage.save(root, data)
            self.assertTrue(result['data']['saved'])
            self.assertEqual(git(root, 'ls-files', '--stage', '--', 'chapter.md'), baseline)
            self.assertEqual(hashlib.sha256(manuscript.read_bytes()).hexdigest(), original)
            self.assertEqual(git(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'), storage.bundle_path(data))
            self.assertEqual(git(root, 'diff', '--cached', '--name-only'), 'chapter.md')
            self.assertEqual(storage.read_history(root)[0], data)

    def test_unborn_bootstrap_and_identical_changed_retry(self):
        with repository(unborn=True) as root:
            data = envelope(root)
            result = storage.save(root, data)
            checkpoint = result['checkpoint']
            self.assertEqual(git(root, 'rev-list', '--count', 'HEAD'), '1')
            self.assertEqual(storage.save(root, data)['checkpoint'], checkpoint)
            self.assertTrue(storage.save(root, data)['data']['already_saved'])
            changed = seal(dict(data, recorded_at='2026-10-21T13:00:00Z'))
            with self.assertRaises(ToolError) as error: storage.save(root, changed)
            self.assertEqual(error.exception.code, 3)
            self.assertEqual(git(root, 'rev-list', '--count', 'HEAD'), '1')

    def test_competing_commit_before_publication_never_contains_candidate(self):
        with repository() as root:
            data = envelope(root)
            (root / 'notes.txt').write_text('Unrelated staged')
            git(root, 'add', 'notes.txt')
            index = (root / '.git/index').read_bytes()
            competitor = []
            def compete(point):
                if point == 'before_ref':
                    tree = git(root, 'rev-parse', 'HEAD^{tree}')
                    candidate = git(root, 'commit-tree', tree, '-p', 'HEAD', '-m', 'External writer')
                    git(root, 'update-ref', 'refs/heads/main', candidate, git(root, 'rev-parse', 'HEAD'))
                    competitor.append(candidate)
            with self.assertRaises(ToolError) as error: storage.save(root, data, fault=compete)
            self.assertEqual(error.exception.code, 3)
            self.assertEqual(git(root, 'rev-parse', 'HEAD'), competitor[0])
            self.assertEqual((root / '.git/index').read_bytes(), index)
            self.assertEqual(storage.read_history(root), [])
            self.assertEqual(git(root, 'log', '--oneline', '--all', '--', storage.bundle_path(data)), '')
            self.assertTrue((root / storage.bundle_path(data)).exists())

    def test_fault_windows_preserve_authority_and_pending_payload(self):
        for point in ('before_file', 'after_file', 'after_candidate', 'before_ref'):
            with self.subTest(point=point), repository() as root:
                data = envelope(root)
                head = git(root, 'rev-parse', 'HEAD')
                with self.assertRaises(ToolError) as error: storage.save(root, data, fault=FailAt(point))
                self.assertEqual(error.exception.code, 5)
                self.assertEqual(error.exception.pending, data['exchange_id'])
                self.assertEqual(git(root, 'rev-parse', 'HEAD'), head)
                self.assertEqual(storage.read_history(root), [])
                self.assertTrue(storage.save(root, data)['data']['saved'])

    def test_published_cleanup_failure_is_saved_and_pauses_writes(self):
        with repository() as root:
            first = envelope(root)
            result = storage.save(root, first, fault=FailAt('before_cleanup'))
            self.assertTrue(result['ok'])
            self.assertTrue(result['data']['cleanup_required'])
            self.assertEqual(storage.read_history(root), [first])
            with self.assertRaises(ToolError): storage.save(root, envelope(root, previous=first))
            retry = storage.save(root, first)
            self.assertTrue(retry['data']['already_saved'])
            self.assertTrue(retry['data']['cleanup_required'])

    def test_receipt_failure_returns_published_checkpoint_without_replay(self):
        with repository() as root:
            data = envelope(root)
            result = storage.save(root, data, fault=FailAt('before_receipt'))
            self.assertTrue(result['data']['saved'])
            again = storage.save(root, data)
            self.assertTrue(again['data']['already_saved'])
            self.assertEqual(again['checkpoint'], result['checkpoint'])

    def test_lock_stale_parent_and_managed_changes(self):
        with repository() as root:
            data = envelope(root)
            lock = root / '.novel-creator/local/write.lock'
            lock.mkdir()
            with self.assertRaises(ToolError) as error: storage.save(root, data)
            self.assertEqual(error.exception.code, 6)
            lock.rmdir()
            with self.assertRaises(ToolError) as error: storage.save(root, seal(dict(data, expected_git_head='0' * 40)))
            self.assertEqual(error.exception.code, 3)
            (root / '.novel-creator/manifest.json').write_text('{}')
            with self.assertRaises(ToolError): storage.save(root, data)

    def test_traversal_symlink_and_payload_paths_rejected(self):
        with repository() as root:
            for path in ('../outside', 'story/../chapter.md', '/tmp/outside', 'chapter.md'):
                with self.subTest(path=path), self.assertRaises(ToolError): storage.safe_path(root, path)
            data = envelope(root)
            (root / 'story').symlink_to(root / '.novel-creator', target_is_directory=True)
            with self.assertRaises(ToolError): storage.save(root, data)
        with repository() as root:
            data = envelope(root, destination='../chapter.md')
            with self.assertRaises(ToolError): storage.save(root, data)

    def test_unrelated_index_change_during_save_survives_cleanup(self):
        with repository() as root:
            def stage(point):
                if point == 'before_ref':
                    (root / 'new.txt').write_text('User change')
                    git(root, 'add', 'new.txt')
            result = storage.save(root, envelope(root), fault=stage)
            self.assertFalse(result['data']['cleanup_required'])
            self.assertEqual(git(root, 'diff', '--cached', '--name-only'), 'new.txt')

    def test_pending_bundle_change_after_candidate_is_rejected(self):
        with repository() as root:
            data = envelope(root)
            initial = git(root, 'rev-parse', 'HEAD')
            def tamper(point):
                if point == 'before_ref':
                    (root / storage.bundle_path(data)).write_text('{}')
            with self.assertRaises(ToolError): storage.save(root, data, fault=tamper)
            self.assertEqual(git(root, 'rev-parse', 'HEAD'), initial)

    def test_managed_staged_change_during_save_reports_conflict(self):
        with repository() as root:
            data = envelope(root)
            initial = git(root, 'rev-parse', 'HEAD')
            def stage(point):
                if point == 'before_ref':
                    git(root, 'add', storage.bundle_path(data))
            with self.assertRaises(ToolError): storage.save(root, data, fault=stage)
            self.assertEqual(git(root, 'rev-parse', 'HEAD'), initial)
            self.assertIn(storage.bundle_path(data), git(root, 'diff', '--cached', '--name-only'))

    def test_post_ref_interruption_returns_saved_cleanup_warning(self):
        with repository() as root:
            data = envelope(root)
            result = storage.save(root, data, fault=FailAt('after_ref'))
            self.assertTrue(result['data']['saved'])
            self.assertTrue(result['data']['cleanup_required'])
            self.assertTrue(storage.save(root, data)['data']['cleanup_required'])

    def test_unsupported_committed_schema_is_unavailable(self):
        with repository() as root:
            data = envelope(root)
            path = root / storage.bundle_path(data)
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(seal(dict(data, schema_version='2.0'))))
            git(root, 'add', storage.bundle_path(data))
            git(root, 'commit', '-m', 'Unsupported record')
            with self.assertRaises(ToolError) as error: storage.read_history(root)
            self.assertEqual(error.exception.code, 4)

    def test_lock_cleanup_error_after_publication_still_returns_saved(self):
        from unittest.mock import patch
        with repository() as root:
            data = envelope(root)
            original = Path.rmdir
            def fail_lock(path):
                if path.name == 'write.lock':
                    raise OSError('Injected writer-lock cleanup failure')
                return original(path)
            with patch.object(Path, 'rmdir', fail_lock):
                result = storage.save(root, data)
            self.assertTrue(result['data']['saved'])
            self.assertTrue(result['data']['cleanup_required'])
            self.assertTrue(result['warnings'])
            self.assertEqual(storage.read_history(root), [data])

    def test_lost_receipt_after_publication_detects_index_cleanup(self):
        with repository() as root:
            data = envelope(root)
            result = storage.save(root, data, fault=FailAt('before_cleanup'))
            (root / '.novel-creator/local' / (data['exchange_id'] + '.json')).unlink()
            retry = storage.save(root, data)
            self.assertTrue(retry['data']['already_saved'])
            self.assertTrue(retry['data']['cleanup_required'])
            self.assertEqual(retry['checkpoint'], result['checkpoint'])

    def test_missing_git_identity_leaves_pending_and_authority_unchanged(self):
        with repository() as root:
            data = envelope(root)
            initial = git(root, 'rev-parse', 'HEAD')
            git(root, 'config', 'user.name', '')
            with self.assertRaises(ToolError) as error: storage.save(root, data)
            self.assertEqual(error.exception.code, 5)
            self.assertEqual(git(root, 'rev-parse', 'HEAD'), initial)
            self.assertEqual(error.exception.checkpoint['git_head'], initial)

    def test_lost_receipt_after_cleanup_remains_clean_identical_success(self):
        with repository() as root:
            data = envelope(root)
            result = storage.save(root,data)
            (root / '.novel-creator/local' / (data['exchange_id']+'.json')).unlink()
            retry = storage.save(root,data)
            self.assertTrue(retry['data']['already_saved'])
            self.assertFalse(retry['data']['cleanup_required'])
            self.assertEqual(retry['checkpoint'],result['checkpoint'])
