import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


class CliContract(unittest.TestCase):
    def test_legacy_init_without_json_preserves_raw_brief_and_machine_output(self):
        import contextlib
        import io
        import tempfile
        from unittest.mock import patch
        from novel_creator.cli import main
        with tempfile.TemporaryDirectory() as folder:
            brief = Path(folder) / 'brief.json'
            raw = '{"title":"Bréf"}\r\n'
            brief.write_bytes(raw.encode('utf-8'))
            output = io.StringIO()
            with patch('novel_creator.install.initialize', return_value={'ok': True}) as initialize, \
                 contextlib.redirect_stdout(output):
                code = main(['init', '--path', str(Path(folder) / 'novel'), '--brief-file', str(brief)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue()), {'ok': True})
            self.assertEqual(initialize.call_args.args[1], raw)
            self.assertEqual(initialize.call_args.kwargs, {})

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
            self.assertFalse(receipt['data']['cleanup_required'])
            retry = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
            self.assertTrue(json.loads(retry.stdout)['data']['already_saved'])
            self.assertFalse(json.loads(retry.stdout)['data']['cleanup_required'])
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

    def test_malformed_stored_data_returns_one_unavailable_json_error(self):
        import tempfile
        from novel_creator import storage
        from tests.helpers import repository, envelope, git
        for area in ('committed', 'receipt'):
            for raw in ('[]', 'null', '{'):
                with self.subTest(area=area, raw=raw), repository() as root, tempfile.TemporaryDirectory() as folder:
                    first = envelope(root)
                    storage.save(root, first)
                    data = envelope(root, previous=first)
                    if area == 'committed':
                        relative = storage.bundle_path(data)
                        (root / relative).write_text(raw)
                        git(root, 'add', relative)
                        git(root, 'commit', '-m', 'Malformed fixture')
                    else:
                        relative = f'.novel-creator/local/{first["exchange_id"]}.json'
                        (root / relative).write_text(raw)
                    initial = git(root, 'rev-parse', 'HEAD')
                    payload = Path(folder) / 'turn.json'
                    payload.write_text(json.dumps(data))
                    result = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
                    self.assertEqual(result.returncode, 4, result.stderr)
                    error = json.loads(result.stdout)
                    self.assertFalse(error['ok'])
                    self.assertIn(relative, error['error']['affected_refs'])
                    self.assertNotIn('Traceback', result.stderr)
                    self.assertEqual(git(root, 'rev-parse', 'HEAD'), initial)

    def test_unavailable_journal_error_discloses_last_valid_checkpoint(self):
        import tempfile
        from novel_creator import storage
        from tests.helpers import repository, envelope, seal, git
        with repository() as root, tempfile.TemporaryDirectory() as folder:
            first = envelope(root)
            saved = storage.save(root, first)
            broken = envelope(root, previous=first)
            relative = storage.bundle_path(broken)
            (root / relative).write_text(json.dumps(seal(dict(broken, schema_version='2.0'))))
            git(root, 'add', relative)
            git(root, 'commit', '-m', 'Unsupported successor fixture')
            data = envelope(root, previous=broken)
            payload = Path(folder) / 'turn.json'
            payload.write_text(json.dumps(data))
            result = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
            self.assertEqual(result.returncode, 4, result.stderr)
            error = json.loads(result.stdout)
            self.assertEqual(error['last_confirmed_checkpoint'], saved['checkpoint'])
            self.assertEqual(error['pending_exchange_id'], data['exchange_id'])
            self.assertIn(relative, error['error']['affected_refs'])
            self.assertNotIn('Traceback', result.stderr)

    def test_stale_write_json_includes_expected_and_actual_heads(self):
        import tempfile
        from tests.helpers import repository, envelope, git
        with repository() as root, tempfile.TemporaryDirectory() as folder:
            actual = git(root, 'rev-parse', 'HEAD')
            data = envelope(root, expected_git_head='0' * 40)
            payload = Path(folder) / 'turn.json'
            payload.write_text(json.dumps(data))
            result = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
            self.assertEqual(result.returncode, 3, result.stderr)
            error = json.loads(result.stdout)
            self.assertEqual(error['error'].get('expected_git_head'), '0' * 40)
            self.assertEqual(error['error'].get('actual_git_head'), actual)
            self.assertEqual(error['last_confirmed_checkpoint']['git_head'], actual)
            self.assertEqual(error['pending_exchange_id'], data['exchange_id'])
            self.assertEqual(git(root, 'rev-parse', 'HEAD'), actual)

    def test_held_lock_json_discloses_pending_id_and_only_verifiable_checkpoint(self):
        import os
        import tempfile
        from novel_creator import storage
        from tests.helpers import repository, envelope, git
        for context in ('saved', 'unborn', 'unreadable', 'non_utf8'):
            if context == 'non_utf8' and os.name == 'nt':
                continue  # Windows filenames do not expose arbitrary byte names.
            with self.subTest(context=context), repository(unborn=context == 'unborn') as root, tempfile.TemporaryDirectory() as folder:
                expected = None
                first = envelope(root)
                if context in ('saved', 'non_utf8'):
                    expected = storage.save(root, first)['checkpoint']
                    data = envelope(root, previous=first)
                else:
                    data = first
                if context == 'unreadable':
                    path = root / storage.bundle_path(first)
                    path.parent.mkdir(parents=True)
                    path.write_text('[]')
                    git(root, 'add', storage.bundle_path(first))
                    git(root, 'commit', '-m', 'Unreadable fixture')
                if context == 'non_utf8':
                    with open(os.fsencode(root) + b'/notes-\xff.txt', 'wb') as stream:
                        stream.write(b'Unrelated user file')
                    git(root, 'add', '--all')
                    git(root, 'commit', '-m', 'Byte filename fixture')
                    expected = None
                lock = root / '.novel-creator/local/write.lock'
                lock.mkdir()
                initial = storage.head(root)
                payload = Path(folder) / 'turn.json'
                payload.write_text(json.dumps(data))
                result = self.invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), '--json')
                self.assertEqual(result.returncode, 6, result.stderr)
                error = json.loads(result.stdout)
                self.assertFalse(error['ok'])
                self.assertTrue(error['error']['retryable'])
                self.assertEqual(error['pending_exchange_id'], data['exchange_id'])
                self.assertEqual(error['last_confirmed_checkpoint'], expected)
                self.assertNotIn('Traceback', result.stderr)
                self.assertTrue(lock.is_dir())
                self.assertEqual(storage.head(root), initial)

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
