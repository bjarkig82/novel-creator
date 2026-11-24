"""Real legacy saves, failures, recovery and explicit debug-session propagation."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from uuid import UUID

from novel_creator import debug, storage
from novel_creator.cli import main, ToolError
from tests.helpers import envelope, repository, FailAt


class LegacyDebugging(unittest.TestCase):
    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(map(str, args)))
        return code, json.loads(out.getvalue()), err.getvalue()

    def events(self, root, identifier):
        path = root / '.novel-creator/local/debug' / identifier / 'events.jsonl'
        return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]

    @contextlib.contextmanager
    def migrated_repository(self, duplicate_id=False):
        with repository() as root:
            legacy = debug.start(root)
            manifest = root / '.novel-creator/manifest.json'
            saved_manifest = manifest.read_bytes()
            manifest.unlink()
            (root / 'notebook').mkdir()
            (root / 'notebook/project.md').write_text('# Migrated novel\n', encoding='utf-8')
            (root / '.novel-notebook/workflows').mkdir(parents=True)
            with (root / '.gitignore').open('a', encoding='utf-8') as ignore:
                ignore.write('.novel-notebook/local/\n')
            if duplicate_id:
                with patch('novel_creator.debug.uuid.uuid4', return_value=UUID(legacy['debug_session'])):
                    notebook = debug.start(root)
            else:
                notebook = debug.start(root)
            manifest.write_bytes(saved_manifest)
            yield root, legacy, notebook

    def test_status_finds_either_session_id_in_a_migrated_notebook(self):
        with self.migrated_repository() as (root, legacy, notebook):
            for session in (notebook, legacy):
                identifier = session['debug_session']
                with self.subTest(project_format=session['format']):
                    directory = Path(session['directory'])
                    original = {path.name: path.read_bytes() for path in directory.iterdir()}
                    code, result, stderr = self.call('debug', 'status', '--novel', root,
                                                     '--debug-session', identifier, '--json')
                    self.assertEqual(code, 0, result)
                    self.assertEqual(stderr, '')
                    self.assertEqual(result['data']['debug_session'], identifier)
                    self.assertEqual(result['data']['format'], session['format'])
                    self.assertEqual(result['data']['directory'], session['directory'])
                    self.assertEqual(result['data']['state'], 'recording')
                    self.assertEqual(result['data']['event_count'], 1)
                    self.assertEqual({path.name: path.read_bytes() for path in directory.iterdir()}, original)

    def test_status_can_disambiguate_a_session_id_retained_in_both_layouts(self):
        with self.migrated_repository(duplicate_id=True) as (root, legacy, notebook):
            args = ('debug', 'status', '--novel', root, '--debug-session', legacy['debug_session'], '--json')
            code, result, _ = self.call(*args)
            self.assertEqual(code, 2, result)
            self.assertFalse(result['ok'])
            self.assertIn('--format', result['error']['message'])
            for session in (notebook, legacy):
                with self.subTest(project_format=session['format']):
                    self.assertIn(session['format'], result['error']['message'])
                    selected_code, selected, stderr = self.call(*args, '--format', session['format'])
                    self.assertEqual(selected_code, 0, selected)
                    self.assertEqual(stderr, '')
                    self.assertEqual(selected['data']['format'], session['format'])
                    self.assertEqual(selected['data']['directory'], session['directory'])

    def test_status_finds_the_session_when_the_other_layout_has_only_a_directory(self):
        with self.migrated_repository() as (root, legacy, notebook):
            identifier = legacy['debug_session']
            orphan = Path(notebook['directory']).with_name(identifier)
            orphan.mkdir()
            code, result, _ = self.call('debug', 'status', '--novel', root, '--debug-session', identifier, '--json')
            self.assertEqual(code, 0, result)
            self.assertEqual(result['data']['directory'], legacy['directory'])
            self.assertEqual(list(orphan.iterdir()), [])

    def test_status_reports_incomplete_session_without_creating_files(self):
        with self.migrated_repository() as (root, legacy, notebook):
            identifier = legacy['debug_session']
            orphan = Path(notebook['directory']).with_name(identifier)
            orphan.mkdir()
            code, result, _ = self.call('debug', 'status', '--novel', root, '--debug-session', identifier,
                                        '--format', 'novel-notebook', '--json')
            self.assertEqual(code, 4, result)
            self.assertIn('incomplete', result['error']['message'])
            self.assertIn('session.json', result['error']['message'])
            self.assertEqual(list(orphan.iterdir()), [])

    def test_status_rejects_redirected_metadata_in_the_other_layout(self):
        with self.migrated_repository() as (root, legacy, notebook):
            identifier = legacy['debug_session']
            candidate = Path(notebook['directory']).with_name(identifier)
            candidate.mkdir()
            (candidate / 'session.json').symlink_to(Path(legacy['directory']) / 'session.json')
            code, result, _ = self.call('debug', 'status', '--novel', root, '--debug-session', identifier, '--json')
            self.assertEqual(code, 2, result)
            self.assertIn('redirected', result['error']['message'])

    def test_status_inventory_can_select_the_notebook_layout(self):
        with self.migrated_repository() as (root, legacy, notebook):
            args = ('debug', 'status', '--novel', root, '--json')
            for options, session in (((), legacy), (('--format', 'novel-notebook'), notebook)):
                with self.subTest(options=options):
                    code, result, _ = self.call(*args, *options)
                    self.assertEqual(code, 0, result)
                    self.assertEqual([entry['debug_session'] for entry in result['data']['sessions']],
                                     [session['debug_session']])
                    self.assertFalse(result['data']['automatic_activation'])

    def test_status_rejects_invalid_missing_or_wrong_format_session_ids(self):
        with self.migrated_repository() as (root, _, notebook):
            args = ('debug', 'status', '--novel', root, '--json', '--debug-session')
            for options, message in (
                (('../outside',), 'canonical debug-session UUID'),
                (('00000000-0000-4000-8000-000000000000',), 'session was not found'),
                ((notebook['debug_session'], '--format', 'legacy'), 'session was not found'),
            ):
                with self.subTest(options=options):
                    code, result, _ = self.call(*args, *options)
                    self.assertEqual(code, 2, result)
                    self.assertIn(message, result['error']['message'])

    def test_status_rejects_a_redirected_session_in_the_notebook_layout(self):
        with self.migrated_repository() as (root, legacy, notebook):
            legacy_dir = Path(legacy['directory'])
            notebook_candidate = Path(notebook['directory']).with_name(legacy['debug_session'])
            notebook_candidate.symlink_to(legacy_dir, target_is_directory=True)
            code, result, _ = self.call('debug', 'status', '--novel', root,
                                        '--debug-session', legacy['debug_session'], '--json')
            self.assertEqual(code, 2, result)
            self.assertIn('redirected', result['error']['message'])

    def test_status_keeps_legacy_only_sessions_available(self):
        with repository() as root:
            session = debug.start(root)
            code, result, stderr = self.call('debug', 'status', '--novel', root,
                                             '--debug-session', session['debug_session'], '--json')
            self.assertEqual(code, 0, result)
            self.assertEqual(stderr, '')
            self.assertEqual(result['data']['format'], 'legacy')
            self.assertEqual(result['data']['directory'], session['directory'])

    def test_status_finds_legacy_session_with_regular_files_at_notebook_marker_parents(self):
        for blocker in ('notebook', '.novel-notebook'):
            with self.subTest(blocker=blocker), repository() as root:
                session = debug.start(root)
                if blocker == '.novel-notebook':
                    (root / 'notebook').mkdir()
                    (root / 'notebook/project.md').write_text('# Notebook draft\n', encoding='utf-8')
                (root / blocker).write_text('Unrelated regular file\n', encoding='utf-8')
                code, result, _ = self.call('debug', 'status', '--novel', root,
                                            '--debug-session', session['debug_session'], '--json')
                self.assertEqual(code, 0, result)
                self.assertEqual(result['data']['directory'], session['directory'])

    def test_status_finds_notebook_session_with_regular_file_at_legacy_marker_parent(self):
        with self.migrated_repository() as (root, _, notebook):
            legacy_root = root / '.novel-creator'
            legacy_root.rename(root / 'retained-legacy')
            legacy_root.write_text('Unrelated regular file\n', encoding='utf-8')
            code, result, _ = self.call('debug', 'status', '--novel', root,
                                        '--debug-session', notebook['debug_session'], '--json')
            self.assertEqual(code, 0, result)
            self.assertEqual(result['data']['directory'], notebook['directory'])

    def test_save_context_and_error_recording_leave_results_unchanged(self):
        with repository() as root, tempfile.TemporaryDirectory() as directory:
            identifier = debug.start(root)['debug_session']
            payload = envelope(root)
            source = Path(directory) / 'exchange.json'
            source.write_text(json.dumps(payload), encoding='utf-8')
            code, saved, stderr = self.call('exchange', 'save', '--novel', root, '--input', source,
                                           '--debug-session', identifier, '--json')
            self.assertEqual(code, 0, stderr)
            self.assertTrue(saved['data']['saved'])
            self.assertEqual(storage.read_history(root), [payload])
            code, context, stderr = self.call('context', '--novel', root, '--view', 'working',
                                             '--debug-session', identifier, '--json')
            self.assertEqual(code, 0, stderr)
            self.assertTrue(context['ok'])
            arguments = ('inspect', '--novel', root, '--id', 'unavailable', '--json')
            baseline = self.call(*arguments)
            observed = self.call(*arguments, '--debug-session', identifier)
            self.assertEqual(baseline, observed)
            events = self.events(root, identifier)
            operations = {event['operation'] for event in events}
            self.assertTrue({'persistence.save', 'validation.exchange', 'git', 'context.snapshot',
                             'context.projection', 'context.result', 'exchange.result'}.issubset(operations), operations)
            self.assertTrue(any(event['outcome'] == 'failure' for event in events))
            snapshots = [ref for event in events for ref in event.get('files', [])]
            self.assertEqual({ref['phase'] for ref in snapshots}, {'before', 'after'})
            self.assertFalse(next(ref for ref in snapshots if ref['phase'] == 'before')['exists'])
            self.assertTrue(next(ref for ref in snapshots if ref['phase'] == 'after')['exists'])
            error_event = next(event for event in events if event['operation'] == 'command.error')
            self.assertEqual(error_event['metadata']['code'], 4)
            self.assertTrue(all(event['source'] == 'package-measured' for event in events))
            self.assertTrue(any(event['metadata'].get('subcommand') == 'rev-parse'
                                for event in events if event['operation'] == 'git'))
            count = len(events)
            self.assertEqual(self.call('context', '--novel', root, '--view', 'working', '--json')[0], 0)
            self.assertEqual(len(self.events(root, identifier)), count, 'opening an uninstrumented command must not resume capture')

    def test_current_input_capture_excludes_prior_transcript_from_debug_content(self):
        with repository() as root, tempfile.TemporaryDirectory() as directory:
            identifier = debug.start(root)['debug_session']
            current = '  Þóra asks.\r\n\n'
            earlier = 'PRIOR_TRANSCRIPT_SHOULD_NOT_BE_CAPTURED'
            snapshot = {'text': '<realtime_delegation>\n  <input>' + current + '</input>\n'
                        '  <transcript_delta>' + earlier + '</transcript_delta>\n</realtime_delegation>',
                        'truncated': False}
            source = Path(directory) / 'input.json'
            source.write_text(json.dumps(snapshot, ensure_ascii=False), encoding='utf-8')
            code, result, stderr = self.call('input', 'capture', '--novel', root, '--capture-file', source,
                                            '--source', 'realtime_delegation', '--debug-session', identifier, '--json')
            self.assertEqual(code, 0, stderr)
            self.assertEqual(result['data']['text'], current)
            archive = Path(directory) / 'report.zip'
            self.assertEqual(self.call('debug', 'export', '--novel', root, '--debug-session', identifier,
                                      '--output', archive, '--json')[0], 0)
            with zipfile.ZipFile(archive) as bundle:
                combined = b'\n'.join(bundle.read(name) for name in bundle.namelist())
                self.assertNotIn(earlier.encode(), combined)
                self.assertIn('Þóra'.encode(), combined)

    def test_pending_recovery_and_export_remain_available_with_maintenance_hold(self):
        with repository() as root, tempfile.TemporaryDirectory() as directory:
            identifier = debug.start(root)['debug_session']
            payload = envelope(root)
            before = storage.head(root)
            with self.assertRaises(ToolError), debug.activate(root, identifier, 'injected.save'):
                storage.save(root, payload, fault=FailAt('after_file'))
            code, recovered, stderr = self.call('recover', '--novel', root, '--exchange', payload['exchange_id'],
                                                '--retry', '--expected-head', before,
                                                '--debug-session', identifier, '--json')
            self.assertEqual(code, 0, stderr)
            self.assertTrue(recovered['data']['saved'])
            self.assertEqual(storage.read_history(root), [payload])
            hold = root / '.novel-creator/local/update/active.json'
            hold.parent.mkdir(parents=True, exist_ok=True)
            hold.write_text('{}', encoding='utf-8')
            archive = Path(directory) / 'report.zip'
            code, result, stderr = self.call('debug', 'export', '--novel', root, '--debug-session', identifier,
                                            '--output', archive, '--json')
            self.assertEqual(code, 0, stderr)
            self.assertTrue(archive.is_file())

    def test_unknown_debug_session_warns_without_changing_a_read_result(self):
        with repository() as root:
            storage.save(root, envelope(root))
            baseline = self.call('validate', '--novel', root, '--json')
            observed = self.call('validate', '--novel', root, '--debug-session',
                                 '00000000-0000-4000-8000-000000000000', '--json')
            self.assertEqual(observed[:2], baseline[:2])
            self.assertIn('debug', observed[2].lower())
            self.assertFalse((root / '.novel-creator/local/debug').exists())

    def test_recorder_write_failure_does_not_change_command_success(self):
        with repository() as root:
            storage.save(root, envelope(root))
            identifier = debug.start(root)['debug_session']
            baseline = self.call('validate', '--novel', root, '--json')
            with patch('novel_creator.debug._record', side_effect=OSError('disk unavailable')):
                observed = self.call('validate', '--novel', root, '--debug-session', identifier, '--json')
            self.assertEqual(observed[:2], baseline[:2])
            self.assertIn('debug', observed[2].lower())

    def test_generated_launcher_retains_update_gate_and_external_controls_export(self):
        from novel_creator.install import initialize
        from tests.helpers import git
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory).resolve()
            root = parent / 'novel'
            root.mkdir()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Debug Test')
            git(root, 'config', 'user.email', 'debug@example.invalid')
            initialize(root, '{"title":"Þóra"}')
            launcher = root / '.novel-creator/run.py'
            original_launcher = launcher.read_bytes()
            env = dict(os.environ, PYTHONPATH='')

            def invoke(prefix, *arguments):
                result = subprocess.run([sys.executable, '-I', *prefix, 'debug', *map(str, arguments),
                                         '--novel', str(root), '--json'],
                                        cwd=parent, env=env, capture_output=True, text=True, encoding='utf-8')
                return result, json.loads(result.stdout)

            result, started = invoke([str(launcher)], 'start')
            self.assertEqual(result.returncode, 0, result.stderr)
            identifier = started['data']['debug_session']
            hold = root / '.novel-creator/local/update/active.json'
            hold.parent.mkdir(parents=True, exist_ok=True)
            hold.write_text('{}', encoding='utf-8')
            archive = parent / 'external-report.zip'
            blocked, failure = invoke([str(launcher)], 'export', '--debug-session', identifier,
                                      '--output', archive)
            self.assertEqual(blocked.returncode, 6)
            self.assertFalse(failure['ok'])
            self.assertFalse(archive.exists())
            for action in ('status', 'stop', 'export'):
                extra = ['--output', archive] if action == 'export' else []
                result, report = invoke(['-m', 'novel_creator'], action, '--debug-session', identifier, *extra)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(report['ok'])
            self.assertTrue(archive.is_file())
            self.assertEqual(launcher.read_bytes(), original_launcher)
            self.assertTrue(hold.is_file(), 'debug controls must not remove or bypass the update hold')
