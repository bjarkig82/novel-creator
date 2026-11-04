import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator
from tests.helpers import envelope
from novel_creator.cli import ToolError


class UpdateProtocolTests(unittest.TestCase):
    def test_process_lifetime_identity_distinguishes_live_owner_and_reused_pid(self):
        import os
        from novel_creator import maintenance
        identity = maintenance.owner_identity()
        self.assertFalse(maintenance.owner_is_dead(os.getpid(), identity))
        prefix, number = identity.rsplit(':', 1)
        self.assertTrue(maintenance.owner_is_dead(os.getpid(), prefix + ':' + str(int(number) + 1)))
        with self.assertRaises(ToolError):
            maintenance.owner_is_dead(os.getpid(), 'unknown-process')

    def test_operational_schema_rejects_unknown_versions_kinds_and_unsafe_paths(self):
        schema = json.loads((Path(__file__).resolve().parents[2] / 'schemas/v1/update.schema.json').read_bytes())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        valid = {'kind': 'active', 'document_version': 1,
                 'operation_id': '00000000-0000-4000-8000-000000000000'}
        self.assertTrue(validator.is_valid(valid))
        for update in ({'document_version': 2}, {'kind': 'unknown'}, {'extra': True}, {'operation_id': '../x'}):
            self.assertFalse(validator.is_valid(dict(valid, **update)))
        # Evaluate the path definition without retaining the root's document union.
        path_schema = {'$defs': schema['$defs'], '$ref': '#/$defs/path'}
        path_validator = Draft202012Validator(path_schema)
        for path in ('../x', '/absolute', 'a/../x', 'a\\x', 'a\nx'):
            self.assertFalse(path_validator.is_valid(path), path)

    def test_export_protocol_contains_only_verified_regular_bundle_resources(self):
        from novel_creator import update_release
        result = update_release.export_bundle()
        self.assertEqual(result['protocol']['protocol_version'], 1)
        self.assertIn('.novel-creator/run.py', result['files'])
        self.assertIn('.novel-creator/src/novel_creator/update-release.json', result['files'])
        self.assertEqual(len(result['bundle_digest']), 64)
        self.assertNotIn('AGENTS.md', result['files'])

    def test_snapshot_validation_is_read_only_and_does_not_call_retro_services(self):
        from novel_creator import update_release
        snapshot = {'history': [envelope()], 'retro_documents': []}
        before = copy.deepcopy(snapshot)
        with patch('novel_creator.retro.Retro', side_effect=AssertionError('service must not be constructed')):
            self.assertEqual(update_release.validate_snapshot(snapshot), {'valid': True, 'exchange_count': 1})
        self.assertEqual(snapshot, before)
        invalid = copy.deepcopy(snapshot)
        invalid['history'][0]['schema_version'] = '999'
        with self.assertRaises(ToolError):
            update_release.validate_snapshot(invalid)
        invalid = copy.deepcopy(snapshot)
        invalid['retro_documents'] = [{'kind': 'notice', 'value': {'retro_version': 999}}]
        with patch('novel_creator.retro.Retro', side_effect=AssertionError('service must not be constructed')):
            with self.assertRaises(ToolError):
                update_release.validate_snapshot(invalid)
        self.assertEqual(snapshot, before)

    def test_fence_confirmation_cannot_precede_its_durable_phase(self):
        from novel_creator.update_release import validate_document
        identifier = '00000000-0000-4000-8000-000000000000'
        preview = {
            'kind': 'preview', 'document_version': 1, 'preview_id': identifier,
            'novel_id': identifier, 'novel_root': '/synthetic/book',
            'branch': 'refs/heads/main', 'source_head': 'a' * 40,
            'source_manifest_digest': 'a' * 64, 'source_version': '0.2.0',
            'target_version': '1.0.0', 'fingerprint': 'a' * 64,
            'runtime_python': '/synthetic/python', 'runtime_fingerprint': 'a' * 64,
            'artifact': {'project': 'novel-creator', 'version': '1.0.0',
                         'filename': 'novel_creator-1.0.0-py3-none-any.whl',
                         'sha256': 'a' * 64, 'size': 1,
                         'url': 'https://files.pythonhosted.org/synthetic.whl'},
            'bundle_digest': 'a' * 64, 'changes': [],
            'source_manifest': {}, 'target_manifest': {}}
        operation = {'kind': 'operation', 'document_version': 1,
            'operation_id': identifier, 'preview': preview, 'state': 'prepared',
            'candidate': 'b' * 40, 'index_baseline': {},
            'fence': {'token': identifier, 'owner_pid': 123,
                      'owner_identity': 'synthetic', 'ownership_confirmed': False,
                      'confirm_quiescent': True}}
        validate_document('operation', operation)
        operation['fence']['ownership_confirmed'] = True
        with self.assertRaises(ToolError):
            validate_document('operation', operation)
        operation['state'] = 'fenced'
        validate_document('operation', operation)
        operation['fence']['ownership_confirmed'] = False
        with self.assertRaises(ToolError):
            validate_document('operation', operation)
