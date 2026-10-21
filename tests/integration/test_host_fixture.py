"""Structural installed-fixture checks; these do not prove native host behavior."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


FIXTURE = Path(__file__).resolve().parents[1] / 'fixtures/host-spike'


class HostFixtureTests(unittest.TestCase):
    def test_installed_fixture_is_independent_and_preserves_exact_visible_text(self):
        with tempfile.TemporaryDirectory() as parent:
            root = Path(parent) / 'novel'
            result = subprocess.run([sys.executable, str(FIXTURE / 'setup.py'), '--path', str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
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
            context = subprocess.run([sys.executable, str(root / '.novel-creator/src/fixture-context.py')], capture_output=True, text=True, cwd=parent)
            self.assertEqual(context.returncode, 0, context.stderr)
            data = json.loads(context.stdout)
            self.assertEqual(data['saved_messages'][0]['text'], user.read_text(encoding='utf-8'))
            self.assertEqual(data['saved_messages'][1]['text'], response.read_text(encoding='utf-8'))
            self.assertFalse(data['display_confirmed'])
            manifest = json.loads((root / '.novel-creator/manifest.json').read_text())
            self.assertTrue(manifest['fixture_only'])
            # Installed scripts must not depend on a framework checkout path.
            self.assertNotIn(str(FIXTURE.parents[2]), launcher.read_text())

    def test_fixture_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as parent:
            result = subprocess.run([sys.executable, str(FIXTURE / 'setup.py'), '--path', parent], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(parent) / '.git').exists())
