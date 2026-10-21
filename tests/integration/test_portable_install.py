import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator.install import initialize
from tests.helpers import git


class PortableInstallTests(unittest.TestCase):
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
from novel_creator import validation
from novel_creator import records, storage
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
