"""Regressions from PR #4; runtime probes remain real except fixed test metadata."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from novel_creator import maintenance, storage, update, update_release
from novel_creator.cli import ToolError
from tests.helpers import git, repository
from tests.integration.test_update_apply import apply_review
from tests.integration.test_update_maintenance import prepared
from tests.integration.test_update_recovery import killed_apply
from tests.update_helpers import artifact, historical_book, snapshot
from tests.update_release_helpers import product_wheel, release_listing


class ReviewContractTests(unittest.TestCase):
    def test_unchanged_launcher_accepts_only_exact_temporary_stub_until_finalization(self):
        with repository() as root:
            launcher = root / update.LAUNCHER
            launcher.write_bytes(update.MAINTENANCE_LAUNCHER)
            target = {'files': {update.LAUNCHER: b'final launcher\n'},
                      'modes': {update.LAUNCHER: '100644'}}
            value = {'preview': {'changes': []}}
            update._check_untouched_resources(root, value, target)
            with self.assertRaises(ToolError):
                update._check_untouched_resources(root, value, target, allow_launcher=False)
            launcher.write_bytes(b'unexpected launcher\n')
            with self.assertRaises(ToolError):
                update._check_untouched_resources(root, value, target)

    def test_shared_rule_addition_refuses_unstaged_custom_bytes_without_mutation(self):
        for relative in ('.gitignore', '.gitattributes'):
            with self.subTest(relative=relative), repository() as root:
                path = root / relative
                baseline = b'# existing rules\n.novel-creator/local/\n' if relative == '.gitignore' else b'# existing attributes\n'
                path.write_bytes(baseline)
                git(root, 'add', relative)
                git(root, 'commit', '-m', 'Existing shared rules')
                path.write_bytes(baseline + b'# unrelated unstaged writer comment\n')
                raw = (root / update.MANIFEST).read_bytes()
                manifest = json.loads(raw)
                manifest.update(managed_paths=[], checksums={})
                raw = update_release.canonical(manifest) + b'\n'
                (root / update.MANIFEST).write_bytes(raw)
                git(root, 'add', update.MANIFEST)
                git(root, 'commit', '-m', 'Synthetic ownership metadata')
                before = snapshot(root)
                target = {'files': {}, 'version': '0.3.0', 'checksums': {}, 'modes': {},
                          'artifact': {'sha256': 'a' * 64}}
                with self.assertRaises(ToolError) as caught:
                    update._plan_changes(root, manifest, raw, {}, None, target, 'synthetic')
                self.assertEqual(caught.exception.code, 3)
                self.assertIn(relative, caught.exception.affected_refs)
                self.assertEqual(snapshot(root), before)

    def test_completed_recovery_inspection_after_writer_commit_is_read_only_and_ready(self):
        with repository() as root:
            operation = prepared(root)
            operation['state'] = 'complete'
            operation['fence']['ownership_confirmed'] = True
            storage.atomic_json(maintenance.operation_path(root, operation['operation_id']), operation)
            (root / '.novel-creator/local/update/active.json').unlink()
            git(root, 'commit', '--allow-empty', '-m', 'Writer progress')
            before = snapshot(root)
            with patch('novel_creator.update_release.prepare', side_effect=AssertionError('prepared product')):
                status = update.status(root, operation_id=operation['operation_id'])
                report = update.recover(root, operation_id=operation['operation_id'])
            self.assertEqual(report['data']['state'], status['data']['state'])
            self.assertTrue(report['data']['ready'])
            self.assertFalse(report['data']['cleanup_required'])
            self.assertFalse(report['data']['retry_eligible'])
            self.assertEqual(report['data']['blockers'], [])
            self.assertEqual(snapshot(root), before)


class SuccessiveUpdateTests(unittest.TestCase):
    def test_successive_updates_with_identical_launcher_apply_and_recover(self):
        runtime = update_release.runtime_info()
        versions = {version: product_wheel(version)[0] for version in ('0.3.0', '0.4.0', '0.5.0')}
        versions['0.2.0'] = artifact('0.2.0')[0].read_bytes()
        transport = release_listing(versions)
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as cache:
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)), \
                    patch('novel_creator.update_release.runtime_info', return_value=runtime):
                first = update.preview(book.root, version='0.3.0', transport=transport)['data']
                self.assertTrue(apply_review(book, first)['data']['ready'])
                original_history = storage.read_history(book.root)
                second = update.preview(book.root, version='0.4.0', transport=transport)['data']
                self.assertNotIn(update.LAUNCHER, [change['path'] for change in second['changes']])
                killed_apply(book, second, 'after_launcher_swap', runtime=runtime)
                inspection = update.recover(book.root, operation_id=second['preview_id'])
                self.assertTrue(inspection['data']['retry_eligible'])
                recovered = update.recover(book.root, operation_id=second['preview_id'], retry=True,
                                           expected_head=storage.head(book.root))
                self.assertTrue(recovered['data']['ready'])
                self.assertFalse(recovered['data']['cleanup_required'])
                self.assertFalse((book.root / '.novel-creator/local/write.lock').exists())
                self.assertEqual(git(book.root, 'rev-parse', 'HEAD^'), second['reviewed_head'])
                self.assertEqual(storage.read_history(book.root), original_history)
                third = update.preview(book.root, version='0.5.0', transport=transport)['data']
                self.assertNotIn(update.LAUNCHER, [change['path'] for change in third['changes']])
                self.assertTrue(apply_review(book, third)['data']['ready'])
                self.assertEqual(git(book.root, 'rev-parse', 'HEAD^'), third['reviewed_head'])
                self.assertTrue(apply_review(book, third)['data']['ready'])
