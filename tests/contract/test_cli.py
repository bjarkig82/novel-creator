import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


class CliContract(unittest.TestCase):
    def invoke(self, *args):
        env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[2] / "src"))
        return subprocess.run([sys.executable, "-m", "novel_creator", *args], env=env, capture_output=True, text=True)

    def test_help(self):
        result = self.invoke("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("exchange", result.stdout)

    def test_invalid_arguments_are_single_json_error(self):
        result = self.invoke("exchange", "save", "--json")
        self.assertEqual(result.returncode, 2)
        error = json.loads(result.stdout)
        self.assertFalse(error["ok"])
        self.assertIsNone(error["last_confirmed_checkpoint"])
        self.assertIn("affected_refs", error["error"])

    def test_save_and_retry_through_subprocess(self):
        import tempfile
        from tests.helpers import repository, envelope, seal
        with repository() as root, tempfile.TemporaryDirectory() as folder:
            payload = Path(folder) / 'turn.json'
            data = envelope(root)
            payload.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            result = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt = json.loads(result.stdout)
            self.assertTrue(receipt['data']['saved'])
            retry = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
            self.assertTrue(json.loads(retry.stdout)['data']['already_saved'])
            self.assertEqual(json.loads(retry.stdout)['checkpoint'], receipt['checkpoint'])
            payload.write_text(json.dumps(seal(dict(data, recorded_at='2026-10-21T13:00:00Z'))))
            conflict = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
            self.assertEqual(conflict.returncode, 3)
            self.assertEqual(json.loads(conflict.stdout)['last_confirmed_checkpoint'], receipt['checkpoint'])

    def test_malformed_input_is_json_error_not_traceback(self):
        import tempfile
        from tests.helpers import repository
        with repository() as root, tempfile.TemporaryDirectory() as folder:
            payload = Path(folder) / 'bad.json'
            for raw in (b'\xff', b'{', b'{"value":NaN}'):
                payload.write_bytes(raw)
                result = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse(json.loads(result.stdout)['ok'])
                self.assertNotIn('Traceback', result.stderr)

    def test_published_save_with_lock_cleanup_failure_is_cli_success(self):
        from contextlib import redirect_stdout, redirect_stderr
        import io
        import tempfile
        from unittest.mock import patch
        from novel_creator.cli import main
        from tests.helpers import repository, envelope
        with repository() as root, tempfile.TemporaryDirectory() as parent:
            data = envelope(root)
            payload = Path(parent) / 'payload.json'
            payload.write_text(json.dumps(data))
            original = Path.rmdir
            def fail_lock(path):
                if path.name == 'write.lock':
                    raise OSError('Writer lock cleanup failed')
                return original(path)
            output, diagnostics = io.StringIO(), io.StringIO()
            with patch.object(Path,'rmdir',fail_lock), redirect_stdout(output), redirect_stderr(diagnostics):
                code = main(['exchange','save','--novel',str(root),'--input',str(payload),'--json'])
            result = json.loads(output.getvalue())
            self.assertEqual(code,0)
            self.assertTrue(result['ok'])
            self.assertTrue(result['data']['saved'])
            self.assertTrue(result['data']['cleanup_required'])
            self.assertEqual(result['checkpoint']['exchange_id'],data['exchange_id'])
