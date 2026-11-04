from contextlib import contextmanager
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from novel_creator import update, storage, records, maintenance
from novel_creator.cli import ToolError
from tests.helpers import git
from tests.update_helpers import historical_book, snapshot, add_writer_work
from tests.integration.test_update_preview import transport_for
from tests.update_helpers import artifact
from tests.update_release_helpers import product_wheel, release_listing


@contextmanager
def reviewed(version='0.2.0', *, writer_work=True, language='en'):
    with historical_book(version, language=language) as book, tempfile.TemporaryDirectory() as cache:
        if writer_work:
            add_writer_work(book.root)
        with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
            transport = transport_for(version)
            result = update.preview(book.root, transport=transport)
            yield book, result['data'], transport


def apply_review(book, preview, **kwargs):
    return update.apply(book.root, preview_id=preview['preview_id'], version=preview['target_version'],
                        expected_head=preview['reviewed_head'], confirm_quiescent=True, **kwargs)


class ApplyTests(unittest.TestCase):
    def test_cached_preview_field_tampering_is_refused_before_runtime_or_book_mutation(self):
        from novel_creator import update_release
        with reviewed() as (book, preview, _):
            file = update_release.cache_home() / 'previews' / (preview['preview_id'] + '.json')
            original = file.read_bytes()
            before = snapshot(book.root)
            for field, value in (('novel_id', '00000000-0000-4000-8000-000000000000'),
                                 ('runtime_python', str(book.root / 'untrusted-python')),
                                 ('source_manifest_digest', 'f' * 64)):
                with self.subTest(field=field):
                    document = json.loads(original)
                    document[field] = value
                    file.write_text(json.dumps(document))
                    with patch('novel_creator.update_release.runtime_info', side_effect=AssertionError('untrusted runtime executed')):
                        with self.assertRaises(ToolError) as caught:
                            apply_review(book, preview)
                    self.assertEqual(caught.exception.code, 3)
                    self.assertEqual(snapshot(book.root), before)
            file.write_bytes(original)

    def test_late_edit_after_completion_keeps_owned_fence_and_reports_published(self):
        with reviewed() as (book, preview, _):
            path = book.root / '.novel-creator/src/novel_creator/records.py'
            changed = []
            def fault(point):
                if point == 'after_completion':
                    raw = path.read_bytes() + b'\n# edit after completion checkpoint\n'
                    path.write_bytes(raw)
                    changed.append(raw)
            with self.assertRaises(ToolError) as caught:
                apply_review(book, preview, fault=fault)
            self.assertEqual(caught.exception.code, 5)
            self.assertEqual(path.read_bytes(), changed[0])
            self.assertTrue((book.root / '.novel-creator/local/write.lock/owner.json').is_file())
            report = update.status(book.root)
            self.assertEqual(report['data']['state'], 'published')
            self.assertFalse(report['data']['ready'])

    def test_late_launcher_or_unchanged_resource_edit_cannot_return_ready(self):
        for resource in (update.LAUNCHER, '.novel-creator/src/novel_creator/records.py'):
            with self.subTest(resource=resource), reviewed() as (book, preview, _):
                if resource != update.LAUNCHER:
                    self.assertNotIn(resource, [item['path'] for item in preview['changes']])
                changed = []
                def fault(point):
                    if point == 'after_final_launcher':
                        path = book.root / resource
                        raw = update.MAINTENANCE_LAUNCHER if resource == update.LAUNCHER else path.read_bytes() + b'\n# external late edit\n'
                        path.write_bytes(raw)
                        changed.append(raw)
                with self.assertRaises(ToolError) as caught:
                    apply_review(book, preview, fault=fault)
                self.assertEqual(caught.exception.code, 5)
                self.assertEqual((book.root / resource).read_bytes(), changed[0])
                self.assertTrue((book.root / '.novel-creator/local/write.lock').exists())
                self.assertFalse(caught.exception.result()['data']['ready'])

    def test_reference_transaction_hook_cannot_add_unrequested_side_effects(self):
        import os
        with reviewed() as (book, preview, _):
            marker = book.root / 'unexpected-hook-side-effect'
            for name in ('reference-transaction', 'post-index-change'):
                hook = book.root / '.git/hooks' / name
                hook.write_text("#!/bin/sh\nprintf ran > '" + marker.as_posix().replace("'", "'\\''") + "'\n")
                os.chmod(hook, 0o755)
            self.assertTrue(apply_review(book, preview)['data']['ready'])
            self.assertFalse(marker.exists())

    def test_exact_framework_commit_preserves_history_custom_work_and_partial_staging(self):
        with reviewed() as (book, preview, transport):
            before = snapshot(book.root)
            before_history = storage.read_history(book.root)
            requests = list(transport.requests)
            result = apply_review(book, preview)
            self.assertTrue(result['data']['ready'])
            self.assertEqual(result['data']['state'], 'complete')
            after = snapshot(book.root)
            self.assertNotEqual(after['head'], before['head'])
            self.assertEqual(git(book.root, 'rev-parse', 'HEAD^'), before['head'])
            self.assertEqual(storage.read_history(book.root), before_history)
            self.assertEqual(storage.index_entries(book.root, ['notes.txt']),
                next(row + b'\0' for row in before['index'].encode().split(b'\0') if row.endswith(b'\tnotes.txt')))
            self.assertEqual((book.root / 'notes.txt').read_bytes(), b'working\n')
            self.assertEqual((book.root / 'untracked.txt').read_bytes(), b'preserve untracked\n')
            self.assertEqual(transport.requests, requests)
            manifest = records.loads((book.root / update.MANIFEST).read_bytes())
            self.assertEqual(manifest['installation_format'], 2)
            self.assertNotIn('AGENTS.md', manifest['managed_paths'])
            self.assertEqual(manifest['last_update']['artifact_sha256'], preview['artifact_sha256'])
            self.assertEqual(apply_review(book, preview)['checkpoint'], result['checkpoint'])

    def test_stale_preview_and_missing_legacy_confirmation_do_not_start_operation(self):
        with reviewed() as (book, preview, _):
            before = snapshot(book.root)
            with self.assertRaises(ToolError):
                update.apply(book.root, preview_id=preview['preview_id'], version=preview['target_version'],
                    expected_head=preview['reviewed_head'])
            self.assertEqual(snapshot(book.root), before)
            (book.root / 'new-writer-work.txt').write_text('preserve')
            changed = snapshot(book.root)
            with self.assertRaises(ToolError) as caught:
                apply_review(book, preview)
            self.assertEqual(caught.exception.code, 3)
            self.assertEqual(snapshot(book.root), changed)

    def test_bootstrap_only_updated_book_has_clean_recovery_and_continuation(self):
        with reviewed('0.1.0', writer_work=False) as (book, preview, _):
            history = storage.read_history(book.root)
            result = apply_review(book, preview)
            self.assertFalse(storage.recover(book.root, history[0]['exchange_id'])['data']['cleanup_required'])
            continuation = json.loads(book.run(
                "import json; from novel_creator.install import initialize; print(json.dumps(initialize(sys.argv[1], '{}')))",
                pinned=True))
            self.assertFalse(continuation['data']['cleanup_required'])
            self.assertEqual(storage.head(book.root), result['checkpoint']['git_head'])
            retry = storage.save(book.root, history[0])
            self.assertFalse(retry['data']['cleanup_required'])

    def test_affected_index_race_is_retained_after_publication(self):
        with reviewed() as (book, preview, _):
            selected = next(item['path'] for item in preview['changes'] if item['action'] == 'replace')
            def fault(point):
                if point == 'before_index_sync':
                    path = book.root / selected
                    original = path.read_bytes()
                    path.write_bytes(b'new staged external content')
                    git(book.root, 'add', selected)
                    path.write_bytes(original)
            with self.assertRaises(ToolError) as caught:
                apply_review(book, preview, fault=fault)
            self.assertEqual(caught.exception.code, 5)
            self.assertEqual(caught.exception.result()['data']['state'], 'published')
            self.assertTrue((book.root / '.novel-creator/local/write.lock').exists())
            self.assertNotEqual(storage.head(book.root), preview['reviewed_head'])

    def test_custom_instructions_and_shared_rules_survive_update(self):
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as cache:
            instructions = b'# Exact custom instructions\nDo not overwrite.\n'
            (book.root / 'AGENTS.md').write_bytes(instructions)
            (book.root / '.gitignore').write_bytes(b'# custom\n.novel-creator/local/\n')
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                preview = update.preview(book.root, transport=transport_for('0.2.0'))['data']
                self.assertTrue(apply_review(book, preview)['data']['ready'])
            self.assertEqual((book.root / 'AGENTS.md').read_bytes(), instructions)
            self.assertEqual((book.root / '.gitignore').read_bytes(), b'# custom\n.novel-creator/local/\n__pycache__/\n*.pyc\n')

    def test_removed_resource_is_deleted_from_worktree_and_index_without_touching_writer_work(self):
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as cache:
            add_writer_work(book.root)
            raw, _ = product_wheel(exclude=['novel_creator/workflows/brainstorm.md'])
            transport = release_listing({'0.2.0': artifact('0.2.0')[0].read_bytes(), '0.3.0': raw})
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                preview = update.preview(book.root, transport=transport)['data']
                path = '.novel-creator/workflows/brainstorm.md'
                self.assertIn({'path': path, 'action': 'remove'}, preview['changes'])
                self.assertTrue(apply_review(book, preview)['data']['ready'])
                self.assertFalse((book.root / path).exists())
                self.assertEqual(storage.index_entries(book.root, [path]), b'')
                self.assertEqual((book.root / 'notes.txt').read_bytes(), b'working\n')
