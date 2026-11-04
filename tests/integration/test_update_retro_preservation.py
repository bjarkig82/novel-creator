import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

from novel_creator import update, storage, retro, maintenance
from novel_creator.cli import ToolError
from tests.helpers import repository
from tests.update_helpers import historical_book, snapshot
from tests.integration.test_update_preview import transport_for
from tests.integration.test_update_apply import apply_review


def authorization(root, checkout, *, enabled=True):
    manifest = json.loads((root / '.novel-creator/manifest.json').read_bytes())
    return retro.document('authorization', enabled=enabled, grant_id=str(uuid.uuid4()), generation=1,
        novel_id=manifest['novel_id'], novel_root=str(root), checkout_root=str(checkout),
        git_common_dir=str(checkout / '.git'), repository='bjarkig82/novel-creator',
        github_login='offline-fixture', authorization_source='direct_cli')


class UpdateRetroPreservationTests(unittest.TestCase):
    grant_states = ('absent', 'disabled', 'revoked', 'mismatched', 'unbound', 'enabled')

    def test_authorization_and_pending_notice_bytes_survive_all_grant_states(self):
        for state in self.grant_states:
            with self.subTest(state=state), historical_book('0.2.0') as book, repository() as checkout, tempfile.TemporaryDirectory() as directory:
                cache = Path(directory).resolve()
                with patch.dict(os.environ, {'LOCALAPPDATA': str(cache / 'machine'), 'XDG_CONFIG_HOME': str(cache / 'machine')}), patch('novel_creator.update_release.cache_home', return_value=cache / 'cache'):
                    base = book.root / '.novel-creator/local/retro'
                    base.mkdir(parents=True, exist_ok=True)
                    grant = authorization(book.root, checkout, enabled=state not in ('disabled', 'revoked'))
                    if state == 'unbound':
                        grant['novel_root'] = str(book.root.parent / 'previous-location')
                    registry = (cache / 'machine/NovelCreator/retro/grants' if os.name == 'nt' else
                                cache / 'machine/novel-creator/retro/grants')
                    machine = registry / (grant['grant_id'] + '.json')
                    if state != 'absent':
                        storage.atomic_json(base / 'authorization.json', grant)
                        value = dict(grant, generation=2) if state == 'mismatched' else grant
                        if state != 'revoked':
                            storage.atomic_json(machine, value)
                    note = retro.document('notice', notice_id=str(uuid.uuid4()), text='Óbirt prófunartilkynning.',
                        text_digest=__import__('hashlib').sha256('Óbirt prófunartilkynning.'.encode()).hexdigest(),
                        url=None, state='pending', reservation_id=None, included_exchange_id=None,
                        language='is', notice_kind='problem', reason_code='operation_unavailable')
                    retro.write(base / 'notices' / (note['notice_id'] + '.json'), note, 'notice')
                    before = {path.relative_to(base).as_posix(): path.read_bytes() for path in base.rglob('*.json')}
                    machine_before = machine.read_bytes() if machine.exists() else None
                    original_git = storage.git
                    def no_disabled_checkout(path, *args, **kwargs):
                        if state != 'enabled' and Path(path) == checkout:
                            raise AssertionError('Disabled/unbound external checkout inspected')
                        return original_git(path, *args, **kwargs)
                    with patch('novel_creator.retro.Retro', side_effect=AssertionError('contributor service constructed')), patch('novel_creator.storage.git', side_effect=no_disabled_checkout):
                        preview = update.preview(book.root, transport=transport_for('0.2.0'))['data']
                        self.assertTrue(apply_review(book, preview)['data']['ready'])
                    self.assertEqual({path.relative_to(base).as_posix(): path.read_bytes() for path in base.rglob('*.json')}, before)
                    self.assertEqual(machine.read_bytes() if machine.exists() else None, machine_before)

    def test_unknown_schema_and_reserved_notice_refuse_without_changes(self):
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as directory:
            base = book.root / '.novel-creator/local/retro/notices'
            base.mkdir(parents=True)
            value = retro.document('notice', notice_id=str(uuid.uuid4()), text='Synthetic notice', text_digest='a' * 64,
                url=None, state='reserved', reservation_id=str(uuid.uuid4()), included_exchange_id=None,
                language='en', notice_kind='problem', reason_code='operation_unavailable')
            path = base / (value['notice_id'] + '.json')
            with patch('novel_creator.update_release.cache_home', return_value=Path(directory)):
                for version in (1, 999):
                    value['retro_version'] = version
                    storage.atomic_json(path, value)
                    before = snapshot(book.root)
                    with self.assertRaises(ToolError):
                        update.preview(book.root, transport=transport_for('0.2.0'))
                    self.assertEqual(snapshot(book.root), before)

    def test_unfinished_runs_uncertain_publication_and_terminal_owner_cleanup_block(self):
        with historical_book('0.2.0') as book, repository() as checkout, tempfile.TemporaryDirectory() as directory:
            cache = Path(directory).resolve()
            grant = authorization(book.root, checkout)
            base = book.root / '.novel-creator/local/retro'
            registry = (cache / 'machine/NovelCreator/retro/grants' if os.name == 'nt' else
                        cache / 'machine/novel-creator/retro/grants')
            with patch.dict(os.environ, {'LOCALAPPDATA': str(cache / 'machine'), 'XDG_CONFIG_HOME': str(cache / 'machine')}), patch('novel_creator.update_release.cache_home', return_value=cache / 'cache'):
                storage.atomic_json(base / 'authorization.json', grant)
                storage.atomic_json(registry / (grant['grant_id'] + '.json'), grant)
                run = retro.document('run', run_id=str(uuid.uuid4()), task_key='a' * 64,
                    completion_exchange_id=storage.read_history(book.root)[-1]['exchange_id'],
                    checkpoint=storage.head(book.root), grant_id=grant['grant_id'], authorization_generation=1,
                    bindings={key: grant[key] for key in ('checkout_root', 'git_common_dir', 'github_login')},
                    status='reviewing', reason_code='fixture', evidence_refs=[], finding=None, contribution=None, notice=None)
                path = base / 'runs' / (run['run_id'] + '.json')
                for status in ('reviewing', 'preparing', 'publishing', 'blocked', 'disabled'):
                    run['status'] = status
                    retro.write(path, run, 'run')
                    before = snapshot(book.root)
                    with self.assertRaises(ToolError):
                        update.preview(book.root, transport=transport_for('0.2.0'))
                    self.assertEqual(snapshot(book.root), before)
                run['status'] = 'published'
                run['contribution'] = {'base': {'branch': 'main', 'sha': storage.head(checkout)},
                    'worktree': str(cache / 'retained-worktree'), 'branch': 'codex/fixture', 'stage': 'publication_unknown',
                    'commit': None, 'validation': None, 'pr': None, 'fingerprint': 'a' * 64, 'public_id': str(uuid.uuid4())}
                retro.write(path, run, 'run')
                with self.assertRaises(ToolError):
                    update.preview(book.root, transport=transport_for('0.2.0'))
                run['contribution']['stage'] = 'published'
                retro.write(path, run, 'run')
                preview = update.preview(book.root, transport=transport_for('0.2.0'))['data']
                owner = checkout / '.git/novel-creator-retro/owner.json'
                retro.write(owner, retro.document('owner', run_id=run['run_id'], grant_id=grant['grant_id'],
                    novel_root=str(book.root)), 'owner')
                before = owner.read_bytes()
                with self.assertRaises(ToolError):
                    apply_review(book, preview)
                self.assertEqual(owner.read_bytes(), before)
