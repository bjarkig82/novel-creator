"""FUP-001 investigation; these are test-only fences, not an implemented updater."""
import json
from pathlib import Path
import unittest

from tests.update_helpers import historical_book, snapshot, acknowledged


SAVE_PROBE = '''
import json, uuid
from novel_creator import storage, records
from novel_creator.cli import ToolError
root=sys.argv[1]
previous=storage.read_history(root)[-1]
bundle=records.new_exchange(previous['novel_id'],previous=previous,
    expected_head=storage.head(root),messages=[
        {'message_id':str(uuid.uuid4()),'role':'user','text':'Synthetic question'},
        {'message_id':str(uuid.uuid4()),'role':'assistant','text':'Synthetic answer'}])
session=records.start_session(bundle,topic='Synthetic fence probe')
bundle.update(session_id=session['id'],record_versions=[session])
bundle['payload_digest']=records.digest(bundle)
try:
    storage.save(root,bundle)
except ToolError as error:
    print(json.dumps({'code':error.code}))
else:
    raise AssertionError('Legacy save bypassed the persistent writer fence')
'''

STANDALONE_GATE = b'''import json, sys
assert not any(name.startswith('novel_creator') for name in sys.modules)
print(json.dumps({'ok':False,'error':{'code':6,'message':'Maintenance pending; use external controller recovery'}}))
raise SystemExit(6)
'''


class LegacyUpdateInvestigation(unittest.TestCase):
    def test_both_pinned_legacy_versions_honor_persistent_writer_fence(self):
        for version in ('0.1.0', '0.2.0'):
            with self.subTest(version=version), historical_book(version) as book:
                before = snapshot(book.root)
                fence = book.root / '.novel-creator/local/write.lock'
                fence.mkdir()
                self.assertEqual(json.loads(book.run(SAVE_PROBE, pinned=True)), {'code': 6})
                self.assertTrue(fence.is_dir())
                self.assertEqual(snapshot(book.root), before)

    def test_fresh_legacy_launchers_can_be_fenced_without_product_imports(self):
        for version in ('0.1.0', '0.2.0'):
            with self.subTest(version=version), historical_book(version) as book:
                before = snapshot(book.root)
                (book.root / '.novel-creator/run.py').write_bytes(STANDALONE_GATE)
                result = book.launch('context', '--novel', book.root, '--json')
                self.assertEqual(result.returncode, 6, result.stderr)
                self.assertIn('external controller', json.loads(result.stdout)['error']['message'])
                after = snapshot(book.root)
                self.assertEqual(after['head'], before['head'])
                self.assertEqual(after['index'], before['index'])
                changed = {path for path in before['files']
                           if before['files'][path] != after['files'][path]}
                self.assertEqual(changed, {'.novel-creator/run.py'})

    def test_legacy_retro_guard_blocks_live_calls_but_cannot_fence_preloaded_client_after_death(self):
        with historical_book('0.2.0') as book:
            book.run('''
from novel_creator.retro import Retro
import uuid
service=Retro(sys.argv[1])
service.notice({'run_id':str(uuid.uuid4()),'status':'blocked','reason_code':'operation_unavailable'},
               'Synthetic retrospective problem')
''', pinned=True)
            notice = next((book.root / '.novel-creator/local/retro/notices').glob('*.json'))
            original = notice.read_bytes()
            fence = book.root / '.novel-creator/local/write.lock'
            fence.mkdir()
            preloaded = '''
import json
from novel_creator.retro import Retro
service=Retro(sys.argv[1])
print('PRELOADED',flush=True)
sys.stdin.readline()
print(json.dumps(service.notices_pending('is')),flush=True)
'''
            owner = '''
from pathlib import Path
from novel_creator.retro import inspection_guard
with inspection_guard(Path(sys.argv[1])/'.novel-creator/local/retro','state.lock.guard'):
    print('HELD',flush=True)
    sys.stdin.readline()
'''
            with book.spawn(preloaded) as client, book.spawn(owner) as holder:
                acknowledged(client, 'PRELOADED')
                acknowledged(holder, 'HELD')
                output = book.run('''
import json
from novel_creator.retro import Retro
from novel_creator.cli import ToolError
try:
    Retro(sys.argv[1]).notices_pending('is')
except ToolError as error:
    print(json.dumps({'code':error.code}))
else:
    raise AssertionError('Live guard did not exclude a legacy notice mutation')
''', pinned=True)
                self.assertEqual(json.loads(output), {'code': 6})
                self.assertEqual(notice.read_bytes(), original)
                holder.kill()
                holder.wait(timeout=30)
                self.assertTrue(fence.is_dir())
                client.stdin.write('continue\n')
                client.stdin.flush()
                output, errors = client.communicate(timeout=30)
                self.assertEqual(client.returncode, 0, errors)
                self.assertTrue(json.loads(output)['notices'])
                self.assertNotEqual(notice.read_bytes(), original)
                self.assertEqual(json.loads(notice.read_bytes())['language'], 'is')
                self.assertTrue(fence.is_dir())

    def test_hard_stop_after_directory_creation_leaves_no_claim_of_ownership(self):
        with historical_book('0.2.0') as book:
            before = snapshot(book.root)
            code = '''
from pathlib import Path
from novel_creator.retro import inspection_guard
fence=Path(sys.argv[1])/'.novel-creator/local/write.lock'
fence.mkdir()
print('DIRECTORY_ONLY',flush=True)
sys.stdin.readline()
'''
            with book.spawn(code) as process:
                acknowledged(process, 'DIRECTORY_ONLY')
                process.kill()
                process.wait(timeout=30)
            fence = book.root / '.novel-creator/local/write.lock'
            self.assertTrue(fence.is_dir())
            self.assertEqual(list(fence.iterdir()), [])
            self.assertEqual(snapshot(book.root), before)
            self.assertEqual(json.loads(book.run(SAVE_PROBE, pinned=True)), {'code': 6})
