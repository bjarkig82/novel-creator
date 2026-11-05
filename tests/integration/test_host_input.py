"""Installed explicit capture and committed source labels, not host capability proof."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator import records, storage, validation
from novel_creator.install import initialize
from tests.helpers import git, uid
from tests.unit.test_host_input import realtime, snapshot


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

            for source in ('delegated', 'native_user', 'realtime_delegation'):
                capture_file.write_bytes(json.dumps(realtime() if source == 'realtime_delegation' else snapshot(source=source), ensure_ascii=False).encode('utf-8'))
                args = ('input', 'capture', '--capture-file', str(capture_file), '--source', source)
                if source != 'realtime_delegation':
                    args += ('--thread-id', 'current', '--turn-id', 'turn')
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
                fresh = invoke('context', '--novel', str(root))
                self.assertEqual(fresh['checkpoint'], saved['checkpoint'])
                self.assertEqual(fresh['data']['exchanges'][-1]['input_artifacts'], exchange['input_artifacts'])

                if source == 'realtime_delegation':
                    self.assertEqual(captured['text'], '  Þóra\r\n東京 🌒 & <quoted>\n')
                    provenance = reopened['input_artifacts'][0]['parsed_value']
                    self.assertEqual(provenance['transcript_delta'], 'Assistant: earlier suggestion.\r\nUser: earlier reply.')
                    self.assertFalse(provenance['evaluation_only'])
                    self.assertIsNone(provenance.get('thread_id'))
                    self.assertEqual(invoke('exchange', 'save', '--novel', str(root), '--input', str(payload))['checkpoint'], saved['checkpoint'])
                    before = (storage.head(root), storage.read_history(root))
                    for flags in (('--thread-id', 'fixture'), ('--evaluation-only',), ('--source-thread-id', 'fixture')):
                        self.assertFalse(invoke(*args, *flags, code=2)['ok'])
                        self.assertEqual((storage.head(root), storage.read_history(root)), before)
                    capture_file.write_text(json.dumps(dict(realtime(), truncated=True)), encoding='utf-8')
                    self.assertFalse(invoke(*args, code=2)['ok'])
                    self.assertEqual((storage.head(root), storage.read_history(root)), before)
                    changed = records.new_exchange(reopened['novel_id'], previous=reopened,
                        expected_head=storage.head(root), messages=[
                            {'message_id': uid(), 'role': 'user', 'text': provenance['transcript_delta']},
                            {'message_id': uid(), 'role': 'assistant', 'text': 'Synthetic reply.'}])
                    artifact = copy.deepcopy(captured['input_artifact'])
                    artifact['artifact_id'] = uid()
                    changed['input_artifacts'] = [artifact]
                    changed['payload_digest'] = records.digest(changed)
                    with self.assertRaisesRegex(ValueError, 'current message or source'):
                        validation.validate_exchange(changed, storage.read_history(root))
                    payload.write_text(json.dumps(changed), encoding='utf-8')
                    rejected = invoke('exchange', 'save', '--novel', str(root), '--input', str(payload), code=2)
                    self.assertFalse(rejected['ok'])
                    self.assertEqual((storage.head(root), storage.read_history(root)), before)

    def test_realtime_save_and_retrospective_prerequisites_are_independent(self):
        from novel_creator import host_input, retro
        from novel_creator.cli import ToolError
        from tests.helpers import envelope, seal
        from tests.retro_helpers import fixtures
        with fixtures() as (root, checkout, registry, fake, first):
            captured = host_input.capture(realtime('Synthetic current request.'), source='realtime_delegation')
            completion = envelope(root, previous=first, messages=[
                {'message_id': uid(), 'role': 'user', 'text': captured['text']},
                {'message_id': uid(), 'role': 'assistant', 'text': 'Synthetic completion.'}],
                input_artifacts=[captured['input_artifact']])
            service = retro.Retro(root, github=fake, registry=registry)
            request = {'host_kind': 'codex', 'thread_id': 'fixture-host-thread',
                       'initiating_turn_id': 'fixture-host-initiating-turn',
                       'completion_exchange_id': completion['exchange_id'], 'checkpoint': storage.head(root)}
            self.assertFalse(service.begin(request)['eligible'])
            service.enable(checkout, authorize=True)
            with self.assertRaises(ToolError):
                service.begin(request)  # Completion is not saved.
            storage.save(root, seal(completion))
            request['checkpoint'] = storage.head(root)
            for field in ('thread_id', 'initiating_turn_id'):
                for missing in (None, '', ' '):
                    with self.subTest(field=field, missing=missing), self.assertRaises(ToolError):
                        service.begin(dict(request, **{field: missing}))
            self.assertEqual(list(service.path('runs').glob('*.json')), [])
            result = service.begin(request)
            self.assertTrue(result['eligible'])
            self.assertTrue(result['review_required'])
            retry = service.begin(request)
            self.assertEqual(retry['run_id'], result['run_id'])
            self.assertFalse(retry['review_required'])
