import json
import os
from pathlib import Path
import subprocess
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

from novel_creator import update, storage, maintenance, update_release
from novel_creator.cli import ToolError
from tests.integration.test_update_apply import reviewed, apply_review
from tests.update_helpers import snapshot


def killed_apply(book, preview, point, *, runtime=None):
    cache = update_release.cache_home()
    acknowledgement = cache / 'crash-ack.txt'
    program = '''
import sys,os,json
from pathlib import Path
from novel_creator import update,update_release
root,cache,preview,point,runtime=sys.argv[1:]
update_release.cache_home=lambda:Path(cache)
if runtime != 'null':
 fixed_runtime=json.loads(runtime)
 update_release.runtime_info=lambda python=None:fixed_runtime
document=json.loads(preview)
def fault(actual):
 if actual == point:
  with (Path(cache)/'crash-ack.txt').open('w') as stream:
   stream.write(actual); stream.flush(); os.fsync(stream.fileno())
  os._exit(91)
update.apply(root,preview_id=document['preview_id'],version=document['target_version'],
 expected_head=document['reviewed_head'],confirm_quiescent=True,fault=fault)
'''
    result = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', '-c', program,
        str(book.root), str(cache), json.dumps(preview), point, json.dumps(runtime)], capture_output=True, timeout=180,
        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode != 91:
        raise AssertionError('Child did not reach requested crash point: ' + result.stderr.decode('utf-8'))
    if acknowledgement.read_text() != point:
        raise AssertionError('Crash checkpoint was not durably acknowledged')


class UpdateRecoveryTests(unittest.TestCase):
    def test_recovery_cache_cannot_move_inside_book(self):
        with reviewed() as (book, preview, _):
            killed_apply(book, preview, 'after_launcher_swap')
            before = snapshot(book.root)
            with patch('novel_creator.update_release.cache_home', return_value=book.root / 'unrequested-cache'):
                with self.assertRaises(ToolError) as caught:
                    update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                                   expected_head=storage.head(book.root))
                self.assertEqual(caught.exception.code, 3)
            self.assertEqual(snapshot(book.root), before)

    def test_hard_death_after_obsolete_resource_removal_recovers_deletion(self):
        from tests.update_helpers import historical_book, artifact
        from tests.update_release_helpers import product_wheel, release_listing
        from tests.integration.test_update_apply import apply_review
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as directory:
            raw, _ = product_wheel(exclude=['novel_creator/workflows/brainstorm.md'])
            transport = release_listing({'0.2.0': artifact('0.2.0')[0].read_bytes(), '0.3.0': raw})
            with patch('novel_creator.update_release.cache_home', return_value=Path(directory)):
                preview = update.preview(book.root, transport=transport)['data']
                path = '.novel-creator/workflows/brainstorm.md'
                killed_apply(book, preview, 'after_replace:' + path)
                self.assertFalse((book.root / path).exists())
                result = update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                    expected_head=storage.head(book.root))
                self.assertTrue(result['data']['ready'])
                self.assertFalse((book.root / path).exists())
                self.assertEqual(storage.index_entries(book.root, [path]), b'')

    def test_hard_death_after_each_resource_action_preserves_exact_retry(self):
        with reviewed(writer_work=False) as (book, preview, _):
            cache = update_release.cache_home()
            backup = cache / 'book-before-resource-crashes'
            shutil.copytree(book.root, backup)
            original_root = book.root.resolve()
            points = ['after_replace:' + item['path'] for item in preview['changes']
                      if item['path'] != update.LAUNCHER]
            for point in points:
                try:
                    with self.subTest(point=point):
                        killed_apply(book, preview, point)
                        result = update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                            expected_head=storage.head(book.root))
                        self.assertTrue(result['data']['ready'])
                        self.assertEqual(git_parent(book.root), preview['reviewed_head'])
                        print('Recovered resource checkpoint: ' + point, flush=True)
                finally:
                    # Both paths are owned by this disposable fixture. Never
                    # derive a deletion target from a journal or CLI input.
                    self.assertEqual(book.root.resolve(), original_root)
                    self.assertTrue(original_root.parent.name.startswith('novel-update-legacy-'))
                    def writable(function, path, error):
                        self.assertTrue(Path(path).absolute().is_relative_to(original_root))
                        if function not in (os.unlink, os.rmdir):
                            raise error
                        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
                        function(path)
                    shutil.rmtree(original_root, onexc=writable)
                    shutil.copytree(backup, original_root)

    def test_changed_journal_artifact_files_and_index_are_preserved(self):
        with reviewed() as (book, preview, _):
            killed_apply(book, preview, 'after_launcher_swap')
            identifier = preview['preview_id']
            journal = maintenance.operation_path(book.root, identifier)
            wheel = journal.parent / 'target.whl'
            resource = book.root / '.novel-creator/manifest.json'
            original_journal, original_wheel, original_resource = journal.read_bytes(), wheel.read_bytes(), resource.read_bytes()
            def retry_refuses():
                before = snapshot(book.root)
                with self.assertRaises(ToolError):
                    update.recover(book.root, operation_id=identifier, retry=True, expected_head=storage.head(book.root))
                self.assertEqual(snapshot(book.root), before)
            wheel.write_bytes(original_wheel + b'changed')
            retry_refuses()
            wheel.write_bytes(original_wheel)
            value = json.loads(original_journal)
            value['candidate'] = value['preview']['source_head']
            journal.write_text(json.dumps(value))
            retry_refuses()
            journal.write_bytes(original_journal)
            resource.write_bytes(original_resource + b'\n')
            retry_refuses()
            resource.write_bytes(original_resource)
            index = book.root / '.git/index'
            original_index = index.read_bytes()
            resource.write_bytes(b'{"external":"staged"}')
            storage.git(book.root, 'add', '.novel-creator/manifest.json')
            resource.write_bytes(original_resource)
            retry_refuses()
            index.write_bytes(original_index)
            self.assertTrue(update.recover(book.root, operation_id=identifier, retry=True,
                expected_head=storage.head(book.root))['data']['ready'])

    def test_actual_legacy_fence_and_guarded_restart_for_both_historical_origins(self):
        from tests.integration.test_update_legacy import SAVE_PROBE
        for version, language in (('0.1.0', 'en'), ('0.2.0', 'is')):
            with self.subTest(version=version), reviewed(version, language=language) as (book, preview, _):
                original = storage.read_history(book.root)
                killed_apply(book, preview, 'after_launcher_swap')
                self.assertEqual(json.loads(book.run(SAVE_PROBE)), {'code': 6})
                self.assertEqual(book.launch('validate', '--novel', book.root, '--json').returncode, 6)
                result = update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                    expected_head=storage.head(book.root))
                self.assertTrue(result['data']['ready'])
                checked = book.launch('validate', '--novel', book.root, '--json')
                self.assertEqual(checked.returncode, 0, checked.stderr)
                self.assertEqual(storage.read_history(book.root), original)
                saved = json.loads(book.run('''
import json,uuid
from pathlib import Path
from novel_creator import records,storage
from novel_creator.context import read
root=Path(sys.argv[1]); previous=storage.read_history(root)[-1]
exchange=records.new_exchange(previous['novel_id'],previous=previous,expected_head=storage.head(root),
 messages=[{'message_id':str(uuid.uuid4()),'role':'user','text':'Höldum áfram.'},
           {'message_id':str(uuid.uuid4()),'role':'assistant','text':'Saved synthetic reply.'}])
session=records.start_session(exchange,topic='Synthetic resume fixture')
exchange.update(session_id=session['id'],record_versions=[session])
exchange['payload_digest']=records.digest(exchange)
result=storage.save(root,exchange)
assert read(root)['data']['manuscript_language'] == sys.argv[2]
assert all(Path(module.__file__).resolve().is_relative_to(root/'.novel-creator/src')
 for name,module in sys.modules.items() if name.startswith('novel_creator') and getattr(module,'__file__',None))
print(json.dumps(result))
''', language, pinned=True))
                self.assertTrue(saved['data']['saved'])
                self.assertFalse(saved['data']['cleanup_required'])

    def test_unconfirmed_directory_never_allows_automatic_takeover(self):
        for point in ('before_fence_owner', 'before_fence_confirmation'):
            with self.subTest(point=point), reviewed(writer_work=False) as (book, preview, _):
                before = snapshot(book.root)
                killed_apply(book, preview, point)
                after = snapshot(book.root)
                for path, value in before['files'].items():
                    self.assertEqual(after['files'][path], value)
                self.assertEqual(after['head'], before['head'])
                self.assertEqual(after['index'], before['index'])
                inspected = update.recover(book.root, operation_id=preview['preview_id'])
                self.assertEqual(inspected['data']['blockers'][0]['reason'], 'ownership_unproven')
                with self.assertRaises(ToolError) as caught:
                    update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                                   expected_head=storage.head(book.root))
                self.assertEqual(caught.exception.code, 6)
                self.assertEqual(snapshot(book.root), after)

    def test_hard_death_at_durable_transitions_recovers_exact_candidate(self):
        points = ('after_preparation', 'after_fence_confirmation', 'after_launcher_swap',
                  'after_replace:.novel-creator/manifest.json', 'after_ref_publication',
                  'after_index_sync', 'after_verification', 'after_final_launcher',
                  'after_completion', 'after_active_release', 'before_fence_release', 'after_fence_release')
        for point in points:
            with self.subTest(point=point), reviewed() as (book, preview, transport):
                before = storage.read_history(book.root)
                killed_apply(book, preview, point)
                operation = maintenance.read_operation(book.root, preview['preview_id'])
                observed = snapshot(book.root)
                with patch('novel_creator.update_release.PublicReleaseTransport.get', side_effect=AssertionError('network')):
                    inspected = update.recover(book.root, operation_id=preview['preview_id'])
                    self.assertEqual(snapshot(book.root), observed)
                    result = update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                                           expected_head=storage.head(book.root))
                self.assertTrue(result['data']['ready'])
                self.assertEqual(storage.head(book.root), operation['candidate'])
                print('Recovered durable checkpoint: ' + point, flush=True)
                self.assertEqual(git_parent(book.root), preview['reviewed_head'])
                self.assertEqual(storage.read_history(book.root), before)
                repeated = update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                                          expected_head=storage.head(book.root))
                self.assertTrue(repeated['data']['ready'])
                self.assertEqual(storage.head(book.root), operation['candidate'])

    def test_live_holder_and_changed_worktree_refuse_recovery(self):
        with reviewed() as (book, preview, _):
            def fault(point):
                if point == 'after_launcher_swap':
                    raise OSError('synthetic interruption')
            with self.assertRaises(ToolError):
                apply_review(book, preview, fault=fault)
            before = snapshot(book.root)
            with self.assertRaises(ToolError) as caught:
                update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                               expected_head=storage.head(book.root))
            self.assertEqual(caught.exception.code, 6)
            self.assertEqual(snapshot(book.root), before)


def git_parent(root):
    return storage.git(root, 'rev-parse', 'HEAD^').decode().strip()
