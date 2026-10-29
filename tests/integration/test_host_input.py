"""Installed explicit capture and committed source labels, not host capability proof."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator import records, storage
from novel_creator.install import initialize
from tests.helpers import git, uid
from tests.unit.test_host_input import snapshot


class InstalledHostInputTests(unittest.TestCase):
    def test_installed_capture_preserves_labels_through_save_and_fresh_context(self):
        with tempfile.TemporaryDirectory() as folder:
            parent = Path(folder).resolve()
            root = parent / 'novel'; root.mkdir()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Disposable Input Test')
            git(root, 'config', 'user.email', 'input@example.invalid')
            initialize(root, '{}')
            evidence = root / '.novel-creator/local/evidence'; evidence.mkdir()
            capture_file = evidence / 'public-input.json'
            env = dict(os.environ, PYTHONPATH='', PYTHONUTF8='1')
            launcher = root / '.novel-creator/run.py'

            def invoke(*args, code=0):
                output = subprocess.run([sys.executable, '-I', '-B', str(launcher), *args, '--json'],
                    capture_output=True, encoding='utf-8', cwd=parent, env=env)
                self.assertEqual(output.returncode, code, output.stderr)
                self.assertNotIn('Traceback', output.stderr)
                return json.loads(output.stdout)

            for source in ('delegated', 'native_user'):
                capture_file.write_bytes(json.dumps(snapshot(source=source), ensure_ascii=False).encode('utf-8'))
                args = ('input', 'capture', '--capture-file', str(capture_file), '--thread-id', 'current',
                        '--turn-id', 'turn', '--source', source)
                if source == 'delegated':
                    before = storage.head(root)
                    self.assertFalse(invoke(*args, code=2)['ok'])
                    self.assertEqual(storage.head(root), before)
                    args += ('--source-thread-id', 'parent', '--evaluation-only')
                captured = invoke(*args)['data']
                history = storage.read_history(root)
                exchange = records.new_exchange(history[-1]['novel_id'], previous=history[-1],
                    expected_head=storage.head(root), messages=[
                        {'message_id': uid(), 'role': 'user', 'text': captured['text']},
                        {'message_id': uid(), 'role': 'assistant', 'text': 'Svar.\r\n'}])
                exchange['input_artifacts'] = [captured['input_artifact']]
                exchange['payload_digest'] = records.digest(exchange)
                payload = evidence / 'prepared.json'
                payload.write_bytes(json.dumps(exchange, ensure_ascii=False).encode('utf-8'))
                saved = invoke('exchange', 'save', '--novel', str(root), '--input', str(payload))
                self.assertTrue(saved['data']['saved'])
                reopened = storage.read_history(root)[-1]
                self.assertEqual(reopened['messages'], exchange['messages'])
                self.assertEqual(reopened['input_artifacts'], exchange['input_artifacts'])
                self.assertEqual(reopened['input_artifacts'][0]['parsed_value']['source_type'], source)
                self.assertEqual(invoke('context', '--novel', str(root))['checkpoint'], saved['checkpoint'])
