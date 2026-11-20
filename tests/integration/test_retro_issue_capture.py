"""Explicit issue captures through the CLI with disposable notebook evidence."""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import uuid
import zipfile

from novel_creator import debug
from novel_creator.cli import main


class IssueCaptureCLI(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'notebook').mkdir()
        (self.root / 'notebook/project.md').write_text('Synthetic notebook', encoding='utf-8')
        (self.root / '.novel-notebook/workflows').mkdir(parents=True)
        (self.root / '.gitignore').write_text('.novel-notebook/local/\n', encoding='utf-8')
        self.issue_dir = self.root / '.novel-notebook/local/retro-issues'

    def call(self, *args, data=None, expected=0):
        arguments = [*args, '--novel', str(self.root), '--json']
        if data is not None:
            path = self.root / 'test-input.json'
            path.write_text(json.dumps(data), encoding='utf-8')
            arguments.extend(('--input', str(path)))
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(arguments)
        self.assertEqual(code, expected, stdout.getvalue() + stderr.getvalue())
        result = json.loads(stdout.getvalue())
        self.assertEqual(result['ok'], expected == 0)
        return result if expected else result['data']

    def begin(self, *, expected=0, live=False, version=1, **options):
        flags = ('--keep-debugging',) if live else ()
        return self.call('retro', 'issue', 'begin', *flags, expected=expected,
                         data=dict(version=version, request_key='explicit-retro', host_session='current', **options))

    def test_live_capture_freezes_evidence_and_keeps_the_selected_session_recording(self):
        selected = self.call('debug', 'start')['debug_session']
        other = self.call('debug', 'start')['debug_session']
        options = dict(debug_session=selected, live=True)
        run = self.begin(**options)
        capture = run['capture']
        self.assertEqual(capture['state'], 'frozen')
        self.assertIs(capture.get('partial'), True)
        self.assertTrue(any('Partial debug snapshot' in text for text in capture['limitations']))
        archive_path = Path(capture['path'])
        original = archive_path.read_bytes()
        with zipfile.ZipFile(archive_path) as archive:
            metadata = json.loads(archive.read('session.json'))
            self.assertEqual(metadata['debug_session'], selected)
            self.assertEqual(metadata['state'], 'recording')
            self.assertTrue(metadata['partial'])
            self.assertIn(b'Partial', archive.read('report.md'))
        self.assertEqual(self.call('debug', 'status', '--debug-session', other)['state'], 'recording')

        later = self.call('debug', 'record', '--debug-session', selected,
                          data={'operation': 'message.user', 'content': 'Synthetic follow-up event'})
        self.assertEqual(later['recorded_sequences'], [2])
        status = self.call('debug', 'status', '--debug-session', selected)
        self.assertEqual(status['state'], 'recording')
        self.assertEqual(status['event_count'], 2)
        self.assertEqual(self.begin(**options), run)
        self.assertEqual(archive_path.read_bytes(), original)
        with zipfile.ZipFile(archive_path) as archive:
            events = [json.loads(line) for line in archive.read('events.jsonl').splitlines()]
            self.assertEqual([event['operation'] for event in events], ['debug.started'])
        self.begin(expected=3, debug_session=selected)
        self.assertEqual(self.call('debug', 'status', '--debug-session', selected)['state'], 'recording')

        finding = str(uuid.uuid4())
        data = {name: 'Synthetic ' + name for name in ('title', 'problem', 'environment', 'reproduction',
                'expected', 'actual', 'evidence', 'uncertainties', 'acceptance_criteria')}
        reference = ('--run', run['run_id'], '--finding', finding)
        draft = self.call('retro', 'issue', 'draft', *reference, data=dict(version=1, sharing='full_debug', **data))
        self.assertEqual(Path(draft['attachments'][0]['path']).read_bytes(), original)
        self.assertEqual(draft['attachments'][0]['sha256'], capture['sha256'])
        self.assertIsNone(draft['approval'])
        blocked = self.call('retro', 'issue', 'publish', *reference, expected=3,
                            data=dict(version=1, stage='preflight', observed_publication_direction=True))
        self.assertIn('approval', blocked['error']['message'])
        self.call('retro', 'issue', 'attachment', *reference, expected=3, data=dict(
            version=1, action='start', observed_upload_consent=True,
            issue_url='https://github.com/bjarkig82/novel-creator/issues/1'))

    def test_invalid_live_requests_leave_capture_and_run_storage_untouched(self):
        selected = self.call('debug', 'start')['debug_session']
        self.begin(expected=2, debug_session=selected, keep_debugging=True)
        for version in (True, 1.0):
            with self.subTest(version=version):
                self.begin(expected=2, debug_session=selected, live=True, version=version)
        self.begin(expected=2, live=True)
        self.begin(expected=2, debug_session=selected, live=True, trigger='session_end',
                   observed_session_end_authorization=True)
        self.assertFalse(self.issue_dir.exists())
        status = self.call('debug', 'status', '--debug-session', selected)
        self.assertEqual((status['state'], status['event_count']), ('recording', 1))
        absent = self.begin()
        self.assertEqual(absent['capture']['state'], 'absent')
        self.assertEqual(self.call('debug', 'status', '--debug-session', selected)['state'], 'recording')

    def test_live_export_rejects_a_stop_after_capture_reservation(self):
        session = self.call('debug', 'start')['debug_session']
        options = dict(debug_session=session, live=True)
        export = debug.export

        def stop_before_export(*args, **kwargs):
            run_id, = self.call('retro', 'issue', 'status')['runs']
            reserved = self.call('retro', 'issue', 'status', '--run', run_id)['capture']
            self.assertEqual(reserved['state'], 'exporting')
            self.assertIs(reserved.get('keep_debugging'), True)
            debug.stop(self.root, session)
            return export(*args, **kwargs)

        with patch.object(debug, 'export', side_effect=stop_before_export):
            result = self.begin(expected=3, **options)
        self.assertIn('recording', result['error']['message'])
        run_id, = self.call('retro', 'issue', 'status')['runs']
        self.assertEqual(result['data']['run_id'], run_id)
        capture = self.call('retro', 'issue', 'status', '--run', run_id)['capture']
        self.assertEqual(capture['state'], 'failed')
        self.assertFalse((self.issue_dir / run_id / 'debug.zip').exists())
        self.begin(expected=3, **options)

    def test_live_capture_retry_refuses_changed_or_missing_frozen_evidence(self):
        session = self.call('debug', 'start')['debug_session']
        options = dict(debug_session=session, live=True)
        run = self.begin(**options)
        archive = Path(run['capture']['path'])
        archive.write_bytes(b'Changed evidence')
        result = self.begin(expected=3, **options)
        self.assertIn('changed', result['error']['message'].lower())
        self.assertEqual(archive.read_bytes(), b'Changed evidence')
        archive.unlink()
        result = self.begin(expected=3, **options)
        self.assertIn('missing', result['error']['message'].lower())
        self.assertFalse(archive.exists())
        self.assertEqual(self.call('retro', 'issue', 'status', '--run', run['run_id']), run)
        self.assertEqual(self.call('debug', 'status', '--debug-session', session)['state'], 'recording')

    def test_default_stop_capture_remains_compatible_with_prior_run_state(self):
        session = self.call('debug', 'start')['debug_session']
        run = self.begin(debug_session=session)
        with zipfile.ZipFile(run['capture']['path']) as archive:
            self.assertFalse(json.loads(archive.read('session.json'))['partial'])
        status = self.call('debug', 'status', '--debug-session', session)
        self.assertEqual(status['state'], 'stopped')
        run['capture'].pop('keep_debugging', None)
        run['capture'].pop('partial', None)
        path = self.issue_dir / run['run_id'] / 'state.json'
        path.write_text(json.dumps(run), encoding='utf-8')
        self.assertEqual(self.begin(debug_session=session), run)
        self.begin(expected=3, debug_session=session, live=True)
