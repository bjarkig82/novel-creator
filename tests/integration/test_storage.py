import hashlib
import json
import os
from pathlib import Path
import unittest

from novel_creator import storage
from novel_creator.cli import ToolError
from tests.helpers import repository, git, envelope, seal, FailAt, uid


class StorageTests(unittest.TestCase):
    def test_byte_hash_guard_rejects_same_size_same_timestamp_edits_for_both_git_formats(self):
        for object_format in ('sha1', 'sha256'):
            with self.subTest(object_format=object_format), repository(object_format=object_format) as root:
                initial = envelope(root)
                initial['continuity_review']['summary'] = 'Fixture only: Þóra\r\n'
                initial = seal(initial)
                storage.save(root, initial)
                checkpoint = storage.head(root)
                self.assertEqual(len(checkpoint), 40 if object_format == 'sha1' else 64)
                path = root / storage.bundle_path(initial)
                before = path.stat()
                raw = path.read_bytes()
                changed = raw.replace(b'Fixture only', b'Fixture evil')
                self.assertNotEqual(raw, changed)
                self.assertEqual(len(raw), len(changed))
                path.write_bytes(changed)
                os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
                index = (root / '.git/index').read_bytes()
                with self.assertRaises(ToolError) as error:
                    storage.save(root, envelope(root, previous=initial))
                self.assertEqual(error.exception.code, 3)
                self.assertEqual(storage.head(root), checkpoint)
                self.assertEqual((root / '.git/index').read_bytes(), index)
                self.assertEqual(path.read_bytes(), changed)

    def test_clean_save_continuation_and_retry_leave_managed_index_synchronized(self):
        for unborn in (False, True):
            with self.subTest(unborn=unborn), repository(unborn=unborn) as root:
                first = envelope(root)
                for data in (first, envelope(root, previous=first)):
                    # The next exchange must expect the checkpoint just saved.
                    data = seal(dict(data, expected_git_head=storage.head(root)))
                    saved = storage.save(root, data)
                    self.assertFalse(saved['data']['cleanup_required'])
                    self.assertEqual(git(root, 'diff', '--cached', '--name-only'), '')
                    receipt = root / '.novel-creator/local' / (data['exchange_id'] + '.json')
                    self.assertFalse(json.loads(receipt.read_text())['cleanup_required'])
                    retry = storage.save(root, data)
                    self.assertEqual(retry['checkpoint'], saved['checkpoint'])
                    self.assertTrue(retry['data']['already_saved'])
                    self.assertFalse(retry['data']['cleanup_required'])
                self.assertEqual(len(storage.read_history(root)), 2)

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
            self.assertEqual(error.exception.result()['error'].get('expected_git_head'), data['expected_git_head'])
            self.assertEqual(error.exception.result()['error'].get('actual_git_head'), competitor[0])
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

    def test_stale_checkpoint_diagnostics_include_expected_and_actual_heads(self):
        for unborn in (False, True):
            with self.subTest(unborn=unborn), repository(unborn=unborn) as root:
                actual = storage.head(root)
                data = envelope(root, expected_git_head='0' * 40)
                with self.assertRaises(ToolError) as error:
                    storage.save(root, data)
                details = error.exception.result()['error']
                self.assertEqual(error.exception.code, 3)
                self.assertEqual(details.get('expected_git_head'), '0' * 40)
                self.assertIn('actual_git_head', details)
                self.assertEqual(details['actual_git_head'], actual)
                self.assertEqual(storage.head(root), actual)
                self.assertFalse((root / storage.bundle_path(data)).exists())

    def test_held_lock_reports_failure_context_without_mutating_owner_or_saved_work(self):
        for context in ('saved', 'unborn', 'unreadable', 'non_utf8'):
            if context == 'non_utf8' and os.name == 'nt':
                continue  # Windows filenames do not expose arbitrary byte names.
            with self.subTest(context=context), repository(unborn=context == 'unborn') as root:
                expected = None
                if context in ('saved', 'non_utf8'):
                    first = envelope(root)
                    expected = storage.save(root, first)['checkpoint']
                    data = envelope(root, previous=first)
                else:
                    data = envelope(root)
                affected = []
                if context == 'unreadable':
                    relative = storage.bundle_path(data)
                    (root / relative).parent.mkdir(parents=True)
                    (root / relative).write_text('[]')
                    git(root, 'add', relative)
                    git(root, 'commit', '-m', 'Unreadable fixture')
                    affected = [relative]
                if context == 'non_utf8':
                    with open(os.fsencode(root) + b'/notes-\xff.txt', 'wb') as stream:
                        stream.write(b'Unrelated user file')
                    git(root, 'add', '--all')
                    git(root, 'commit', '-m', 'Byte filename fixture')
                    expected = None  # Inspection cannot validate this committed tree.
                (root / 'notes.txt').write_text('Unrelated staged work')
                git(root, 'add', 'notes.txt')
                lock = root / '.novel-creator/local/write.lock'
                lock.mkdir()
                (lock / 'owner.json').write_text('{"pid":12345,"note":"existing owner"}')
                initial = storage.head(root)
                index = (root / '.git/index').read_bytes()
                managed = {path.relative_to(root): path.read_bytes() for directory in
                           (root / 'story', root / '.novel-creator')
                           for path in directory.rglob('*') if path.is_file()}
                with self.assertRaises(ToolError) as error:
                    storage.save(root, data)
                self.assertEqual(error.exception.code, 6)
                self.assertEqual(error.exception.pending, data['exchange_id'])
                self.assertEqual(error.exception.checkpoint, expected)
                self.assertEqual(error.exception.affected_refs, affected)
                self.assertEqual(storage.head(root), initial)
                self.assertEqual((root / '.git/index').read_bytes(), index)
                self.assertTrue(lock.is_dir())
                self.assertEqual({path.relative_to(root): path.read_bytes() for directory in
                                  (root / 'story', root / '.novel-creator')
                                  for path in directory.rglob('*') if path.is_file()}, managed)

    def test_traversal_and_payload_paths_rejected(self):
        with repository() as root:
            for path in ('../outside', 'story/../chapter.md', '/tmp/outside', 'chapter.md'):
                with self.subTest(path=path), self.assertRaises(ToolError): storage.safe_path(root, path)
        with repository() as root:
            data = envelope(root, destination='../chapter.md')
            with self.assertRaises(ToolError): storage.save(root, data)

    def test_real_symlink_path_rejected_when_creation_is_available(self):
        with repository() as root:
            try:
                (root / 'story').symlink_to(root / '.novel-creator', target_is_directory=True)
            except OSError as error:
                if getattr(error, 'winerror', None) == 1314:
                    self.skipTest('Real symlink rejection unverified: Windows symlink privilege unavailable (1314)')
                raise
            with self.assertRaises(ToolError):
                storage.save(root, envelope(root))

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

    def test_nonobject_committed_json_is_unavailable(self):
        for raw in ('[]', 'null', '"not an envelope"', '42'):
            with self.subTest(raw=raw), repository() as root:
                data = envelope(root)
                relative = storage.bundle_path(data)
                path = root / relative
                path.parent.mkdir(parents=True)
                path.write_text(raw)
                git(root, 'add', relative)
                git(root, 'commit', '-m', 'Malformed fixture')
                initial = git(root, 'rev-parse', 'HEAD')
                index = (root / '.git/index').read_bytes()
                with self.assertRaises(ToolError) as error:
                    storage.read_history(root)
                self.assertEqual(error.exception.code, 4)
                self.assertIn(relative, error.exception.affected_refs)
                self.assertEqual(git(root, 'rev-parse', 'HEAD'), initial)
                self.assertEqual((root / '.git/index').read_bytes(), index)

    def test_unreadable_successor_retains_last_verifiable_checkpoint(self):
        for damage in ('[]', '{', 'unsupported'):
            with self.subTest(damage=damage), repository() as root:
                first = envelope(root)
                saved = storage.save(root, first)
                second = envelope(root, previous=first)
                relative = storage.bundle_path(second)
                raw = json.dumps(seal(dict(second, schema_version='2.0'))) if damage == 'unsupported' else damage
                (root / relative).write_text(raw)
                git(root, 'add', relative)
                git(root, 'commit', '-m', 'Unreadable successor fixture')
                initial = git(root, 'rev-parse', 'HEAD')
                index = (root / '.git/index').read_bytes()
                data = envelope(root, previous=second)
                for operation in (lambda: storage.read_history(root), lambda: storage.save(root, data)):
                    with self.assertRaises(ToolError) as error:
                        operation()
                    self.assertEqual(error.exception.code, 4)
                    self.assertEqual(error.exception.checkpoint, saved['checkpoint'])
                    self.assertIn(relative, error.exception.affected_refs)
                self.assertEqual(git(root, 'rev-parse', 'HEAD'), initial)
                self.assertEqual((root / '.git/index').read_bytes(), index)
                self.assertFalse((root / storage.bundle_path(data)).exists())

    def test_valid_prefix_never_labels_a_damaged_commit_as_a_checkpoint(self):
        with repository() as root:
            first = envelope(root)
            saved = storage.save(root, first)
            edited = seal(dict(first, recorded_at='2026-10-21T13:00:00Z'))
            (root / storage.bundle_path(first)).write_text(json.dumps(edited))
            second = envelope(root, previous=edited)
            (root / storage.bundle_path(second)).write_text('[]')
            git(root, 'add', storage.bundle_path(first), storage.bundle_path(second))
            git(root, 'commit', '-m', 'Altered prefix and damaged successor')
            with self.assertRaises(ToolError) as error:
                storage.read_history(root)
            self.assertEqual(error.exception.checkpoint,
                             {'git_head': None, 'exchange_id': first['exchange_id'], 'sequence': 1})
            self.assertNotEqual(error.exception.checkpoint['git_head'], saved['checkpoint']['git_head'])

    def test_malformed_receipts_block_retry_and_further_saves(self):
        for raw in ('[]', 'null', '{}', '{', '{"state":"pending","bundle":[]}'):
            with self.subTest(raw=raw), repository() as root:
                first = envelope(root)
                saved = storage.save(root, first)
                relative = f'.novel-creator/local/{first["exchange_id"]}.json'
                receipt = root / relative
                receipt.write_text(raw)
                index = (root / '.git/index').read_bytes()
                for data in (first, envelope(root, previous=first)):
                    with self.subTest(retry=data == first), self.assertRaises(ToolError) as error:
                        storage.save(root, data)
                    self.assertEqual(error.exception.code, 4)
                    self.assertIn(relative, error.exception.affected_refs)
                    self.assertEqual(error.exception.checkpoint, saved['checkpoint'])
                self.assertEqual(git(root, 'rev-parse', 'HEAD'), saved['checkpoint']['git_head'])
                self.assertEqual((root / '.git/index').read_bytes(), index)
                self.assertEqual(receipt.read_text(), raw)

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
