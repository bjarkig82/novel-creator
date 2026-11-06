import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator.install import initialize
from tests.helpers import git


class PortableInstallTests(unittest.TestCase):
    def test_historical_updated_books_restore_guided_session_and_save_in_both_languages(self):
        from unittest.mock import patch
        from novel_creator import update, storage
        from tests.update_helpers import historical_book
        from tests.integration.test_update_preview import transport_for
        from tests.integration.test_update_apply import apply_review
        for version, language in (('0.1.0', 'en'), ('0.2.0', 'is')):
            with self.subTest(version=version), historical_book(version, language=language) as book, tempfile.TemporaryDirectory() as cache:
                session = json.loads(book.run('''
import json,uuid
from novel_creator import records,storage
root=sys.argv[1]; previous=storage.read_history(root)[-1]
exchange=records.new_exchange(previous['novel_id'],previous=previous,expected_head=storage.head(root),messages=[
 {'message_id':str(uuid.uuid4()),'role':'user','text':'Start synthetic guided session.'},
 {'message_id':str(uuid.uuid4()),'role':'assistant','text':'Synthetic saved response.'}])
session=records.start_session(exchange,topic='Þóra / synthetic fixture')
exchange.update(session_id=session['id'],record_versions=[session]);exchange['payload_digest']=records.digest(exchange)
assert storage.save(root,exchange)['data']['saved']
print(json.dumps(session))
'''))
                before = storage.read_history(book.root)
                with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                    preview = update.preview(book.root, transport=transport_for(version))['data']
                    self.assertTrue(apply_review(book, preview)['data']['ready'])
                self.assertEqual(storage.read_history(book.root), before)
                result = json.loads(book.run('''
import json,uuid
from pathlib import Path
from novel_creator import records,storage
from novel_creator.context import read
root=Path(sys.argv[1]); session=json.loads(sys.argv[2]); language=sys.argv[3]
context=read(root,session=session['id'])
assert context['data']['selected_session'] == session
assert context['data']['manuscript_language'] == language
assert context['data']['selected_session']['mode'] == 'guided'
previous=storage.read_history(root)[-1]
exchange=records.new_exchange(previous['novel_id'],previous=previous,expected_head=storage.head(root),session_id=session['id'],messages=[
 {'message_id':str(uuid.uuid4()),'role':'user','text':'Höldum áfram / continue.'},
 {'message_id':str(uuid.uuid4()),'role':'assistant','text':'Synthetic saved continuation.'}])
exchange['record_versions']=[records.revise_session(session,exchange)]
exchange['payload_digest']=records.digest(exchange)
result=storage.save(root,exchange)
assert all(Path(module.__file__).resolve().is_relative_to(root/'.novel-creator/src')
 for name,module in sys.modules.items() if name.startswith('novel_creator') and getattr(module,'__file__',None))
print(json.dumps(result))
''', json.dumps(session), language, pinned=True))
                self.assertTrue(result['data']['saved'])
                self.assertFalse(result['data']['cleanup_required'])
                self.assertEqual(storage.read_history(book.root)[:-1], before)

    def test_isolated_interpreter_loads_every_product_module_from_novel_bundle(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Portable Test')
            git(root, 'config', 'user.email', 'portable@example.invalid')
            result = initialize(root, '{"title":"Þóra"}')
            code = f'''
import json, sys
from pathlib import Path
root = Path({str(root)!r})
sys.path.insert(0, str(root / '.novel-creator/src'))
from novel_creator.context import read
from novel_creator.retro import Retro
assert Retro(root).status()['enabled'] is False
assert (root / '.novel-creator/workflows/retrospective.md').is_file()
assert (root / '.novel-creator/src/novel_creator/schemas/v1/retro.schema.json').is_file()
from novel_creator import validation
from novel_creator import memory, records, storage
data = read(root)
previous = storage.read_history(root)[-1]
exchange = records.new_exchange(data['novel_id'], previous=previous, expected_head=storage.head(root),
    messages=[{{'message_id': str(__import__('uuid').uuid4()), 'role': 'user', 'text': 'Höldum áfram / continue.'}},
              {{'message_id': str(__import__('uuid').uuid4()), 'role': 'assistant', 'text': 'Hvaða leyndarmál?'}}])
session = records.start_session(exchange, topic='Bréfin / letters')
exchange.update(session_id=session['id'], record_versions=[session])
exchange['payload_digest'] = records.digest(exchange)
receipt = storage.save(root, exchange)
assert receipt['data']['saved'] and not receipt['data']['cleanup_required']
assert read(root, operation='validate')['data']['exchange_count'] == 2
assert read(root, operation='session')['data']['sessions'][0]['topic'] == 'Bréfin / letters'
assert read(root, operation='inspect', identifier=session['id'])['data']['history'][0]['mode'] == 'guided'
current = read(root, view='current')
assert current['checkpoint'] == receipt['checkpoint'] and 'exchanges' not in current['data']
working = read(root, view='working', focus=[session['id']], limit=1)
assert working['data']['records'] == [session]
assert working['data']['retrieval']['source_checkpoint'] == receipt['checkpoint']
assert working['data']['retrieval']['source_novel_id'] == data['novel_id']
assert working['data']['project'] == data['data']['project']
assert read(root, view='working', query='BRÉFIN')['data']['records'] == [session]
paths = [str(Path(module.__file__).resolve()) for name, module in sys.modules.items()
         if name.startswith('novel_creator') and getattr(module, '__file__', None)]
assert paths and all(Path(p).is_relative_to(root) for p in paths), paths
assert data['data']['project']['title']['original_text'] == 'Þóra'
print(json.dumps({{'novel_id': data['novel_id'], 'paths': paths}}))
'''
            output = subprocess.run([sys.executable, '-I', '-B', '-c', code], cwd=root.parent,
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(output.returncode, 0, output.stderr)
            self.assertEqual(json.loads(output.stdout)['novel_id'], result['novel_id'])
