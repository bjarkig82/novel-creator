"""Structural installed-fixture checks; these do not prove native host behavior."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures/host-spike'


class HostFixtureTests(unittest.TestCase):
    def test_native_user_message_input_preserves_exact_whitespace(self):
        with tempfile.TemporaryDirectory() as parent:
            parent = Path(parent).resolve()
            root = parent / 'novel'
            setup = subprocess.run([sys.executable, str(FIXTURE / 'setup.py'), '--path', str(root)],
                                   capture_output=True, text=True)
            self.assertEqual(setup.returncode, 0, setup.stderr)
            source = root / '.novel-creator/local/evidence/native-user-message.json'
            source.parent.mkdir(parents=True)
            response = parent / 'response.txt'
            response.write_bytes('Svar: Þóra.\n'.encode('utf-8'))
            for text in ('Þóra\n', '  Þóra\n\n\n', '\r\nÍslenska og ensk texti.\r\n', 'No ending newline'):
                with self.subTest(text=repr(text)):
                    source.write_text(json.dumps({'type': 'userMessage', 'id': 'native-current-message',
                        'content': [{'type': 'text', 'text': text}]}, ensure_ascii=False), encoding='utf-8')
                    prepare = subprocess.run([sys.executable, str(root / '.novel-creator/src/fixture-prepare.py'),
                        '--user-message-file', str(source), '--response-file', str(response)],
                        capture_output=True, text=True, cwd=parent)
                    self.assertEqual(prepare.returncode, 0, prepare.stderr)
                    prepared = json.loads(prepare.stdout)
                    payload = json.loads(Path(prepared['payload_file']).read_bytes())
                    self.assertEqual(payload['messages'][0]['text'], text)
                    self.assertEqual(payload['messages'][1]['text'], 'Svar: Þóra.\n')
                    save = subprocess.run([sys.executable, str(root / '.novel-creator/run.py'), 'exchange',
                        'save', '--novel', str(root), '--input', prepared['payload_file'], '--json'],
                        capture_output=True, text=True, cwd=parent)
                    self.assertEqual(save.returncode, 0, save.stderr)
                    self.assertFalse(json.loads(save.stdout)['data']['cleanup_required'])
                    context = subprocess.run([sys.executable, str(root / '.novel-creator/src/fixture-context.py')],
                        capture_output=True, text=True, cwd=parent)
                    self.assertEqual(context.returncode, 0, context.stderr)
                    self.assertEqual(json.loads(context.stdout)['saved_messages'][0]['text'], text)
            for invalid in ({'type': 'agentMessage', 'id': 'wrong-role', 'text': 'Not a user'},
                            {'type': 'userMessage', 'id': 'ambiguous', 'content': [
                                {'type': 'text', 'text': 'one'}, {'type': 'text', 'text': 'two'}]},
                            {'type': 'userMessage', 'id': 'image', 'content': [{'type': 'image', 'url': 'image'}]}):
                with self.subTest(invalid=invalid['id']):
                    source.write_text(json.dumps(invalid), encoding='utf-8')
                    prepare = subprocess.run([sys.executable, str(root / '.novel-creator/src/fixture-prepare.py'),
                        '--user-message-file', str(source), '--response-file', str(response)],
                        capture_output=True, text=True, cwd=parent)
                    self.assertEqual(prepare.returncode, 2)
                    self.assertNotIn('Traceback', prepare.stderr)
                    self.assertEqual(prepare.stdout, '')

    def test_installed_fixture_is_independent_and_preserves_exact_visible_text(self):
        with tempfile.TemporaryDirectory() as parent:
            parent = Path(parent).resolve()
            root = Path(parent) / 'novel'
            result = subprocess.run([sys.executable, str(FIXTURE / 'setup.py'), '--path', str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)['data']['cleanup_required'])
            launcher = root / '.novel-creator/run.py'
            user = Path(parent) / 'user.txt'
            response = Path(parent) / 'response.txt'
            user.write_text('Explore Þóra.\nKeep this line.\n', encoding='utf-8')
            response.write_text('What does Þóra want?\n', encoding='utf-8')
            prepare = subprocess.run([sys.executable, str(root / '.novel-creator/src/fixture-prepare.py'), '--user-file', str(user), '--response-file', str(response)], capture_output=True, text=True, cwd=parent)
            self.assertEqual(prepare.returncode, 0, prepare.stderr)
            payload = json.loads(prepare.stdout)['payload_file']
            save = subprocess.run([sys.executable, str(launcher), 'exchange', 'save', '--novel', str(root), '--input', payload, '--json'], capture_output=True, text=True, cwd=parent)
            self.assertEqual(save.returncode, 0, save.stderr)
            self.assertFalse(json.loads(save.stdout)['data']['cleanup_required'])
            context = subprocess.run([sys.executable, str(root / '.novel-creator/src/fixture-context.py')], capture_output=True, text=True, cwd=parent)
            self.assertEqual(context.returncode, 0, context.stderr)
            data = json.loads(context.stdout)
            # Compare exact UTF-8 input, including Windows CRLF and trailing
            # newlines; read_text's universal-newline conversion hides them.
            self.assertEqual(data['saved_messages'][0]['text'], user.read_bytes().decode('utf-8'))
            self.assertEqual(data['saved_messages'][1]['text'], response.read_bytes().decode('utf-8'))
            self.assertFalse(data['display_confirmed'])
            manifest = json.loads((root / '.novel-creator/manifest.json').read_text())
            self.assertTrue(manifest['fixture_only'])
            # Installed scripts must not depend on a framework checkout path.
            self.assertNotIn(str(FIXTURE.parents[2]), launcher.read_text())

    def test_fixture_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as parent:
            parent = Path(parent).resolve()
            result = subprocess.run([sys.executable, str(FIXTURE / 'setup.py'), '--path', parent], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(parent) / '.git').exists())
