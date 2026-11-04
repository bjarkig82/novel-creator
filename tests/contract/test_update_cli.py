import contextlib
import hashlib
import io
import json
import unittest
from unittest.mock import patch

from novel_creator import cli, update, storage, maintenance
from tests.helpers import repository, git
from tests.update_helpers import snapshot
from tests.integration.test_update_maintenance import prepared


def invoke(*arguments):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        code = cli.main(list(arguments))
    return code, json.loads(stream.getvalue())


class UpdateCliTests(unittest.TestCase):
    def test_completed_status_rejects_replaced_non_descendant_history(self):
        with repository() as root:
            operation = prepared(root)
            operation['state'] = 'complete'
            operation['fence']['ownership_confirmed'] = True
            storage.atomic_json(maintenance.operation_path(root, operation['operation_id']), operation)
            (root / '.novel-creator/local/update/active.json').unlink()
            git(root, 'commit', '--allow-empty', '-m', 'Writer progress')
            writer_head = storage.head(root)
            tree = git(root, 'rev-parse', 'HEAD^{tree}')
            unrelated = git(root, 'commit-tree', tree, '-m', 'Unrelated history')
            git(root, 'replace', unrelated, writer_head)
            git(root, 'update-ref', 'refs/heads/main', unrelated, writer_head)
            before = snapshot(root)
            result = update.status(root, operation_id=operation['operation_id'])
            self.assertEqual(result['data']['state'], 'conflict')
            self.assertIn({'reason': 'checkpoint_changed'}, result['data']['blockers'])
            self.assertFalse(result['data']['ready'])
            self.assertEqual(snapshot(root), before)

    def test_completed_status_rechecks_resource_integrity_after_writer_progress(self):
        with repository() as root:
            relative = '.novel-creator/src/novel_creator/records.py'
            (root / relative).parent.mkdir(parents=True)
            (root / relative).write_bytes(b'verified resource\n')
            manifest_path = root / '.novel-creator/manifest.json'
            manifest = json.loads(manifest_path.read_bytes())
            manifest['checksums'] = {relative: hashlib.sha256(b'verified resource\n').hexdigest()}
            manifest_path.write_text(json.dumps(manifest))
            git(root, 'add', relative, '.novel-creator/manifest.json')
            git(root, 'commit', '-m', 'Synthetic installed resource')
            operation = prepared(root)
            operation['state'] = 'complete'
            operation['fence']['ownership_confirmed'] = True
            storage.atomic_json(maintenance.operation_path(root, operation['operation_id']), operation)
            (root / '.novel-creator/local/update/active.json').unlink()
            git(root, 'commit', '--allow-empty', '-m', 'Writer progress')
            self.assertTrue(update.status(root, operation_id=operation['operation_id'])['data']['ready'])
            (root / relative).write_bytes(b'changed resource\n')
            before = snapshot(root)
            result = update.status(root, operation_id=operation['operation_id'])
            self.assertEqual(result['data']['state'], 'conflict')
            self.assertIn({'reason': 'installed_resource_changed', 'path': relative}, result['data']['blockers'])
            self.assertFalse(result['data']['ready'])
            self.assertEqual(snapshot(root), before)

    def test_malformed_internal_metadata_is_one_redacted_json_error(self):
        with patch('novel_creator.update.preview', side_effect=ValueError('PRIVATE-STORY-SECRET')):
            code, result = invoke('update', '--novel', 'book', '--json')
        self.assertEqual(code, 4)
        self.assertNotIn('PRIVATE-STORY-SECRET', json.dumps(result))

    def test_explicit_apply_and_offline_recovery_routes_bind_exact_arguments(self):
        identifier = '00000000-0000-4000-8000-000000000000'
        head = 'a' * 40
        expected = {'ok': True, 'data': {'ready': True}}
        with patch('novel_creator.update.apply', return_value=expected) as apply:
            code, _ = invoke('update', '--novel', 'book', '--apply', '--preview', identifier,
                '--version', '0.3.0', '--expected-head', head, '--confirm-quiescent', '--json')
            self.assertEqual(code, 0)
            apply.assert_called_once_with('book', preview_id=identifier, version='0.3.0',
                expected_head=head, confirm_quiescent=True)
        with patch('novel_creator.update.recover', return_value=expected) as recover:
            code, _ = invoke('update', 'recover', '--novel', 'book', '--operation', identifier,
                             '--retry', '--expected-head', head, '--json')
            self.assertEqual(code, 0)
            recover.assert_called_once_with('book', operation_id=identifier, retry=True, expected_head=head)

    def test_conflicting_apply_recovery_arguments_never_call_services(self):
        cases = [('--apply', '--preview', 'id'), ('recover', '--retry', '--operation', 'id'),
                 ('recover', '--operation', 'id', '--expected-head', 'a' * 40),
                 ('status', '--apply'), ('--apply', '--apply'), ('--confirm-quiescent',),
                 ('recover', '--operation', 'id', '--python', '/configured/python')]
        with patch('novel_creator.update.apply', side_effect=AssertionError('apply called')), patch('novel_creator.update.recover', side_effect=AssertionError('recovery called')):
            for arguments in cases:
                with self.subTest(arguments=arguments):
                    code, result = invoke('update', '--novel', 'book', *arguments)
                    self.assertEqual(code, 2)

    def test_operation_error_keeps_update_identity_out_of_exchange_identity(self):
        identifier = '00000000-0000-4000-8000-000000000000'
        error = cli.ToolError(5, 'Published cleanup required', data={'operation_id': identifier, 'state': 'published'})
        with patch('novel_creator.update.recover', side_effect=error):
            code, result = invoke('update', 'recover', '--novel', 'book', '--operation', identifier,
                '--retry', '--expected-head', 'a' * 40)
        self.assertEqual(code, 5)
        self.assertIsNone(result['pending_exchange_id'])
        self.assertEqual(result['data']['operation_id'], identifier)

    def test_default_routes_selected_interpreter_only_on_explicit_request(self):
        expected = {'ok': True, 'data': {'state': 'preview'}}
        with patch('novel_creator.update.preview', return_value=expected) as preview:
            code, result = invoke('update', '--novel', 'book', '--python', '/selected/python', '--version', '0.3.0', '--json')
            self.assertEqual(code, 0)
            self.assertEqual(result, expected)
            preview.assert_called_once_with('book', version='0.3.0', python='/selected/python')

    def test_invalid_options_do_not_call_controller(self):
        cases = [('--force',), ('--index-url', 'https://evil.invalid'),
                 ('--version', '0.3.0', '--version', '0.4.0'), ('--apply',)]
        with patch('novel_creator.update.preview', side_effect=AssertionError('controller called')):
            for arguments in cases:
                with self.subTest(arguments=arguments):
                    code, _ = invoke('update', '--novel', 'book', *arguments)
                    self.assertEqual(code, 2)

    def test_status_reads_no_operation_pending_unproven_conflict_and_complete_without_writes(self):
        with repository() as root, patch('novel_creator.update_release.PublicReleaseTransport.get', side_effect=AssertionError('network')):
            before = snapshot(root)
            self.assertEqual(update.status(root)['data']['state'], 'no_operation')
            self.assertEqual(snapshot(root), before)
            operation = prepared(root)
            before = snapshot(root)
            self.assertEqual(update.status(root)['data']['state'], 'pending')
            self.assertEqual(snapshot(root), before)
            fence = root / '.novel-creator/local/write.lock'
            fence.mkdir()
            before = snapshot(root)
            result = update.status(root)
            self.assertEqual(result['data']['blockers'][0]['reason'], 'ownership_unproven')
            self.assertEqual(snapshot(root), before)
            fence.rmdir()
            # A different branch/HEAD must never appear ready.
            git(root, 'checkout', '-b', 'other')
            before = snapshot(root)
            self.assertEqual(update.status(root)['data']['state'], 'conflict')
            self.assertEqual(snapshot(root), before)
            git(root, 'checkout', 'main')
            operation['state'] = 'complete'
            operation['fence']['ownership_confirmed'] = True
            storage.atomic_json(maintenance.operation_path(root, operation['operation_id']), operation)
            (root / '.novel-creator/local/update/active.json').unlink()
            before = snapshot(root)
            code, result = invoke('update', 'status', '--novel', str(root), '--operation', operation['operation_id'], '--json')
            self.assertEqual(code, 0)
            self.assertEqual(result['data']['state'], 'complete')
            self.assertEqual(snapshot(root), before)
            # A normal writer commit after completed maintenance is not cleanup.
            git(root, 'commit', '--allow-empty', '-m', 'Writer progress after update')
            before = snapshot(root)
            code, result = invoke('update', 'status', '--novel', str(root), '--operation', operation['operation_id'], '--json')
            self.assertEqual(code, 0)
            self.assertEqual(result['data']['state'], 'complete')
            self.assertTrue(result['data']['ready'])
            self.assertFalse(result['data']['cleanup_required'])
            self.assertEqual(snapshot(root), before)
            # The same descendant checkpoint is unsafe for unfinished work.
            operation['state'] = 'published'
            storage.atomic_json(maintenance.operation_path(root, operation['operation_id']), operation)
            before = snapshot(root)
            result = update.status(root, operation_id=operation['operation_id'])
            self.assertEqual(result['data']['state'], 'conflict')
            self.assertFalse(result['data']['ready'])
            self.assertEqual(snapshot(root), before)

    def test_status_reports_published_cleanup_even_when_journal_lags(self):
        with repository() as root:
            operation = prepared(root)
            # Synthetic recorded candidate differs from the original parent.
            git(root, 'commit', '--allow-empty', '-m', 'synthetic candidate')
            operation['candidate'] = storage.head(root)
            storage.atomic_json(maintenance.operation_path(root, operation['operation_id']), operation)
            before = snapshot(root)
            result = update.status(root)
            self.assertEqual(result['data']['state'], 'published')
            self.assertTrue(result['data']['cleanup_required'])
            self.assertFalse(result['data']['ready'])
            self.assertEqual(snapshot(root), before)

    def test_malformed_status_evidence_stays_preserved(self):
        with repository() as root:
            path = root / '.novel-creator/local/update/active.json'
            path.parent.mkdir(parents=True)
            path.write_text('{"bad":true}')
            before = snapshot(root)
            result = update.status(root)
            self.assertFalse(result['data']['ready'])
            self.assertEqual(result['data']['state'], 'conflict')
            self.assertEqual(snapshot(root), before)
