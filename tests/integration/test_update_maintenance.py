import json
import os
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import uuid

from novel_creator import maintenance, storage
from novel_creator.cli import ToolError
from tests.helpers import repository, envelope
from tests.update_helpers import snapshot


def prepared(root):
    identifier = str(uuid.uuid4())
    manifest = json.loads((root / '.novel-creator/manifest.json').read_bytes())
    preview = {'kind': 'preview', 'document_version': 1, 'preview_id': identifier,
        'novel_id': manifest['novel_id'], 'novel_root': str(root),
        'branch': 'refs/heads/main', 'source_head': storage.head(root),
        'source_manifest_digest': 'a' * 64, 'source_version': '0.2.0',
        'target_version': '1.0.0', 'fingerprint': 'a' * 64,
        'runtime_python': os.path.abspath(__import__('sys').executable), 'runtime_fingerprint': 'a' * 64,
        'artifact': {'project': 'novel-creator', 'version': '1.0.0',
                     'filename': 'novel_creator-1.0.0-py3-none-any.whl',
                     'sha256': 'a' * 64, 'size': 1,
                     'url': 'https://files.pythonhosted.org/synthetic.whl'},
        'bundle_digest': 'a' * 64, 'changes': [], 'source_manifest': manifest, 'target_manifest': manifest}
    value = {'kind': 'operation', 'document_version': 1, 'operation_id': identifier,
        'preview': preview, 'state': 'prepared', 'candidate': storage.head(root), 'index_baseline': {},
        'fence': {'token': str(uuid.uuid4()), 'owner_pid': os.getpid(),
                  'owner_identity': maintenance.owner_identity(), 'ownership_confirmed': False,
                  'confirm_quiescent': True}}
    storage.atomic_json(maintenance.operation_path(root, identifier), value)
    storage.atomic_json(root / '.novel-creator/local/update/active.json',
                        {'kind': 'active', 'document_version': 1, 'operation_id': identifier})
    return value


class MaintenanceTests(unittest.TestCase):
    def test_normal_operations_share_access_but_exclude_maintenance(self):
        with repository() as root, ThreadPoolExecutor(max_workers=1) as workers:
            def mutation():
                with maintenance.normal_operation(root):
                    return 'allowed'
            with maintenance.normal_operation(root):
                self.assertEqual(workers.submit(mutation).result(timeout=30), 'allowed')
                with self.assertRaises(ToolError) as caught:
                    with maintenance.access_guard(root, exclusive=True):
                        self.fail('Exclusive maintenance entered an active normal operation')
                self.assertEqual(caught.exception.code, 6)
            with maintenance.access_guard(root, exclusive=True):
                with self.assertRaises(ToolError):
                    workers.submit(mutation).result(timeout=30)

    def test_pending_update_blocks_direct_services_before_any_mutation(self):
        from novel_creator.context import read
        from novel_creator.install import initialize
        from novel_creator.retro import Retro
        with repository() as root:
            prepared(root)
            before = snapshot(root)
            service = Retro(root)
            for action in (lambda: storage.save(root, envelope(root)),
                           lambda: read(root), lambda: initialize(root, '{}'),
                           lambda: service.disable(), lambda: service.notices_pending('is')):
                with self.subTest(action=action), self.assertRaises(ToolError) as caught:
                    action()
                self.assertEqual(caught.exception.code, 6)
                self.assertEqual(snapshot(root), before)

    def test_retro_dispatch_rejection_does_not_construct_service_or_journal_failure(self):
        from novel_creator.retro import dispatch
        with repository() as root:
            prepared(root)
            before = snapshot(root)
            args = SimpleNamespace(novel=str(root), action='prepare', run=str(uuid.uuid4()))
            with patch('novel_creator.retro.Retro', side_effect=AssertionError('service constructed')):
                with self.assertRaises(ToolError) as caught:
                    dispatch(args)
            self.assertEqual(caught.exception.code, 6)
            self.assertEqual(snapshot(root), before)

    def test_interrupted_empty_fence_is_retained_and_not_claimed_from_prepared_token(self):
        with repository() as root:
            value = prepared(root)
            def fault(point):
                if point == 'before_fence_owner':
                    raise OSError('Synthetic interruption before ownership')
            with maintenance.access_guard(root, exclusive=True):
                before = snapshot(root)
                with self.assertRaises(OSError):
                    maintenance.claim_fence(root, value['operation_id'], fault=fault)
                self.assertEqual(snapshot(root), before)
                self.assertEqual(list((root / '.novel-creator/local/write.lock').iterdir()), [])
                self.assertFalse(maintenance.confirmed_owner(root, value))
                with self.assertRaises(ToolError) as caught:
                    maintenance.claim_fence(root, value['operation_id'])
                self.assertEqual(caught.exception.code, 6)
                self.assertEqual(snapshot(root), before)

    def test_fence_is_confirmed_only_after_owner_and_journal_are_durable(self):
        with repository() as root:
            value = prepared(root)
            with maintenance.access_guard(root, exclusive=True):
                confirmed = maintenance.claim_fence(root, value['operation_id'])
                self.assertEqual(confirmed['state'], 'fenced')
                self.assertTrue(maintenance.confirmed_owner(root, confirmed))
                self.assertEqual(maintenance.read_operation(root, value['operation_id']), confirmed)
                with self.assertRaises(ToolError):
                    maintenance.ensure_ready(root)

    def test_legacy_state_guard_is_bridged_without_constructing_a_retro_service(self):
        from novel_creator.retro import inspection_guard
        with repository() as root:
            value = prepared(root)
            base = root / '.novel-creator/local/retro'
            base.mkdir(parents=True)
            with maintenance.access_guard(root, exclusive=True):
                confirmed = maintenance.claim_fence(root, value['operation_id'])
                with patch('novel_creator.retro.Retro', side_effect=AssertionError('service constructed')):
                    with maintenance.legacy_exclusions(root, confirmed) as state:
                        self.assertEqual(state['documents'], [])
                        with self.assertRaises(ToolError):
                            with inspection_guard(base, 'state.lock.guard'):
                                self.fail('Old bookkeeping guard was not excluded')
                        with self.assertRaises(ToolError):
                            with inspection_guard(base, 'authorization.lock.guard'):
                                self.fail('Old authorization guard was not excluded')
