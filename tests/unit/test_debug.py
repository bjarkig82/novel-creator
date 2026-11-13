"""Real filesystem tests for explicit local diagnostic sessions."""
from concurrent.futures import ThreadPoolExecutor
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from novel_creator import debug
from novel_creator.cli import ToolError


class DebugRecorder(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='session-debug-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        self.env.update(GIT_AUTHOR_NAME='Debug Test', GIT_AUTHOR_EMAIL='debug@example.invalid',
                        GIT_COMMITTER_NAME='Debug Test', GIT_COMMITTER_EMAIL='debug@example.invalid')
        subprocess.run(['git', 'init', '-q', str(self.root)], env=self.env, check=True)
        (self.root / 'notebook').mkdir()
        (self.root / 'notebook/project.md').write_text('Notebook', encoding='utf-8')
        (self.root / '.novel-notebook/workflows').mkdir(parents=True)
        (self.root / '.gitignore').write_text('.novel-notebook/local/\n', encoding='utf-8')
        (self.root / 'AGENTS.md').write_text('Keep custom guidance.\n', encoding='utf-8')

    def start(self):
        return debug.start(self.root)['debug_session']

    def directory(self, identifier):
        return self.root / '.novel-notebook/local/debug' / identifier

    def events(self, identifier):
        return [json.loads(line) for line in (self.directory(identifier) / 'events.jsonl').read_text().splitlines()]

    def test_lifecycle_unicode_content_snapshots_zip_and_no_overwrite(self):
        identifier = self.start()
        original = '  Þóra\r\n\n  '
        path = self.root / 'notebook/topic.md'
        path.write_bytes(original.encode())
        debug.record(self.root, identifier, {'operation': 'turn', 'content': original,
                     'files': [{'path': 'notebook/topic.md', 'phase': 'before'}],
                     'observed_at': '2026-11-12T12:00:00Z', 'correlation_ids': {'turn_id': 'public-id'}})
        path.write_bytes(b'Changed\n')
        debug.record(self.root, identifier, {'operation': 'save', 'files': [{'path': 'notebook/topic.md', 'phase': 'after'}]})
        partial = debug.export(self.root, identifier)
        self.assertTrue(partial['partial'])
        with zipfile.ZipFile(partial['output']) as archive:
            self.assertEqual({'events.jsonl', 'session.json', 'report.md'} - set(archive.namelist()), set())
            blobs = [archive.read(name) for name in archive.namelist() if name.startswith('attachments/')]
            self.assertIn(original.encode(), blobs)
            self.assertIn(original, [json.loads(b) for b in blobs if b.startswith(b'"')])
            self.assertIn('Partial', archive.read('report.md').decode())
            self.assertIn('agent-recorded', archive.read('report.md').decode())
        with self.assertRaises(ToolError):
            debug.export(self.root, identifier)
        before = len(self.events(identifier))
        debug.stop(self.root, identifier)
        debug.stop(self.root, identifier)
        self.assertEqual(len(self.events(identifier)), before + 1)
        with self.assertRaises(ToolError):
            debug.record(self.root, identifier, {'operation': 'late'})
        exported = debug.export(self.root, identifier, self.root / 'stopped.zip')
        self.assertFalse(exported['partial'])

    def test_off_by_default_and_explicit_session_isolation(self):
        debug.capture('off', content='must not be recorded')
        self.assertFalse((self.root / '.novel-notebook/local').exists())
        first, second = self.start(), self.start()
        with debug.activate(self.root, first, 'command'):
            with debug.span('phase'):
                debug.capture('public', content='only first')
        self.assertEqual(len(self.events(second)), 1)
        measured = self.events(first)
        self.assertTrue(all(e['source'] == 'package-measured' for e in measured))
        self.assertTrue(all(e['duration_ms'] >= 0 for e in measured if 'duration_ms' in e))
        before = len(measured)
        debug.capture('off-again')
        self.assertEqual(len(self.events(first)), before)
        other = self.root / 'another'
        other.mkdir()
        with self.assertRaises(ToolError):
            debug.status(other, first)

    def test_capture_failure_never_changes_operation_outcome_and_resets(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with debug.activate(self.root, 'missing', 'save'):
                debug.capture('save.result', content='saved')
            with self.assertRaisesRegex(RuntimeError, 'original'):
                with debug.activate(self.root, 'missing', 'save'):
                    raise RuntimeError('original')
        self.assertIn('report may have gaps', stderr.getvalue())
        self.assertIsNone(debug._ACTIVE.get())

    def test_concurrent_recorders_serialize_event_sequence(self):
        identifier = self.start()
        with ThreadPoolExecutor(max_workers=5) as executor:
            list(executor.map(lambda n: debug.record(self.root, identifier, {'operation': 'parallel', 'metadata': {'n': n}}), range(15)))
        self.assertEqual([e['sequence'] for e in self.events(identifier)], list(range(1, 17)))

    def test_corrupt_log_is_exportable_but_cannot_be_extended(self):
        identifier = self.start()
        log = self.directory(identifier) / 'events.jsonl'
        with log.open('ab') as stream:
            stream.write(b'{"incomplete":')
        result = debug.export(self.root, identifier)
        self.assertTrue(result['warnings'])
        with zipfile.ZipFile(result['output']) as archive:
            self.assertEqual(archive.read('events.jsonl'), log.read_bytes())
        with self.assertRaises(ToolError):
            debug.record(self.root, identifier, {'operation': 'after-corruption'})

    def test_file_references_reject_private_redirected_and_special_paths(self):
        identifier = self.start()
        unsafe = ['../outside.md', '/etc/passwd', 'notebook/../secret.txt', 'notebook\\topic.md',
                  '.git/config', 'notebook/.env', 'notebook/.private/topic.md',
                  'notebook/credentials.json', 'notebook/api-token.txt', 'C:/secrets.txt',
                  'notebook/topic.md:private.md', 'notebook/private /topic.md', 'notebook/private./topic.md']
        outside = self.root / 'outside.md'
        outside.write_text('private', encoding='utf-8')
        if hasattr(os, 'symlink'):
            (self.root / 'notebook/link.md').symlink_to(outside)
            unsafe.append('notebook/link.md')
        for name in unsafe:
            with self.subTest(path=name), self.assertRaises(ToolError):
                debug.record(self.root, identifier, {'operation': 'read', 'files': [{'path': name}]})
        self.assertEqual(len(self.events(identifier)), 1)

    def test_malformed_inputs_have_controlled_errors(self):
        identifier = self.start()
        for payload in (None, [], {'events': []}, {'operation': 3}, {'operation': 'debug.stopped'},
                        {'operation': 'x', 'duration_ms': 3}, {'operation': 'x', 'files': 'all'},
                        {'operation': 'x', 'metadata': []}, {'operation': 'x', 'observed_at': 12},
                        {'operation': 'x', 'content': float('nan')}):
            with self.subTest(payload=payload), self.assertRaises(ToolError):
                debug.record(self.root, identifier, payload)

    def test_missing_new_files_are_explicit_snapshots(self):
        identifier = self.start()
        debug.record(self.root, identifier, {'operation': 'new.file', 'files': [{'path': 'notebook/new.md', 'phase': 'before'}]})
        self.assertEqual(self.events(identifier)[-1]['files'], [{'path': 'notebook/new.md', 'phase': 'before', 'exists': False}])

    def test_setup_preserves_custom_work_and_reports_conflicts_before_writes(self):
        guide = b'# Session debugging\n'
        class Resource:
            def joinpath(self, name):
                return self
            def read_bytes(self):
                return guide
        (self.root / '.gitignore').write_bytes(b'# Existing\n')
        subprocess.run(['git', '-C', str(self.root), 'add', '--', 'AGENTS.md'], env=self.env, check=True)
        before_index = (self.root / '.git/index').read_bytes()
        with patch('novel_creator.debug.resources', return_value=Resource()):
            result = debug.setup(self.root)
            self.assertEqual(len(result['changed_paths']), 3)
            self.assertTrue((self.root / 'AGENTS.md').read_text().startswith('Keep custom guidance.'))
            self.assertEqual((self.root / '.git/index').read_bytes(), before_index)
            self.assertEqual(debug.setup(self.root)['changed_paths'], [])
            workflow = self.root / '.novel-notebook/workflows/debugging.md'
            workflow.write_bytes(b'custom changed guide')
            agents = (self.root / 'AGENTS.md').read_bytes()
            with self.assertRaises(ToolError):
                debug.setup(self.root)
            self.assertEqual((self.root / 'AGENTS.md').read_bytes(), agents)

    def test_setup_routes_each_host_and_skill_source_without_touching_index(self):
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                with self.subTest(host=host, source=source), tempfile.TemporaryDirectory() as area:
                    root = Path(area).resolve()
                    subprocess.run(['git', 'init', '-q', str(root)], env=self.env, check=True)
                    (root / 'notebook').mkdir()
                    (root / 'notebook/project.md').write_text('Notebook', encoding='utf-8')
                    (root / '.novel-notebook/workflows').mkdir(parents=True)
                    (root / '.novel-notebook/integration.json').write_text(json.dumps(
                        {'version': 1, 'host': host, 'skill_source': source}), encoding='utf-8')
                    selected = ['AGENTS.md'] if host == 'codex' else ['CLAUDE.md'] if host == 'claude' else ['AGENTS.md', 'CLAUDE.md']
                    for name in selected:
                        (root / name).write_text('Custom instruction.\n', encoding='utf-8')
                    (root / '.gitignore').write_text('# Existing\n', encoding='utf-8')
                    subprocess.run(['git', '-C', str(root), 'add', '--', *selected], env=self.env, check=True)
                    before = (root / '.git/index').read_bytes()
                    result = debug.setup(root)
                    self.assertTrue(result['ready'])
                    self.assertEqual((root / '.git/index').read_bytes(), before)
                    for name in selected:
                        content = (root / name).read_text(encoding='utf-8')
                        self.assertTrue(content.startswith('Custom instruction.\n'))
                        self.assertIn('.novel-notebook/workflows/debugging.md', content)
                    for name in {'AGENTS.md', 'CLAUDE.md'} - set(selected):
                        self.assertFalse((root / name).exists())
                    self.assertEqual(debug.setup(root)['changed_paths'], [])
                    self.assertTrue(debug.start(root)['debug_session'])

    def test_setup_rejects_invalid_host_marker_before_writes(self):
        marker = self.root / '.novel-notebook/integration.json'
        marker.write_text('{"version":1,"host":"unknown","skill_source":"plugin"}', encoding='utf-8')
        original = (self.root / 'AGENTS.md').read_bytes()
        with self.assertRaises(ToolError):
            debug.setup(self.root)
        self.assertEqual((self.root / 'AGENTS.md').read_bytes(), original)
        self.assertFalse((self.root / '.novel-notebook/workflows/debugging.md').exists())

    @unittest.skipUnless(hasattr(os, 'link'), 'hard links unavailable')
    def test_setup_rejects_hard_linked_targets_before_any_writes(self):
        marker = self.root / '.novel-notebook/integration.json'
        marker.write_text('{"version":1,"host":"both","skill_source":"project"}', encoding='utf-8')
        (self.root / 'CLAUDE.md').write_text('Custom Claude instructions.\n', encoding='utf-8')
        (self.root / '.gitignore').write_text('# Existing\n', encoding='utf-8')
        for name in ('AGENTS.md', 'CLAUDE.md', '.gitignore'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                target = self.root / name
                original = target.read_bytes()
                outside = Path(directory) / 'outside'
                target.unlink()
                outside.write_bytes(original)
                try:
                    os.link(outside, target)
                except OSError as error:
                    self.skipTest('hard links unavailable: ' + str(error))
                try:
                    with self.assertRaises(ToolError):
                        debug.setup(self.root)
                    self.assertEqual(outside.read_bytes(), original)
                    self.assertFalse((self.root / '.novel-notebook/workflows/debugging.md').exists())
                finally:
                    target.unlink()
                    target.write_bytes(original)

    def test_unignored_or_redirected_local_paths_are_rejected(self):
        (self.root / '.gitignore').write_text('', encoding='utf-8')
        with self.assertRaises(ToolError):
            self.start()
        (self.root / '.gitignore').write_text('.novel-notebook/local/\n', encoding='utf-8')
        outside = self.root / 'other'
        outside.mkdir()
        (self.root / '.novel-notebook/local').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ToolError):
            self.start()
        self.assertEqual(list(outside.iterdir()), [])

    def test_legacy_paths_and_environment_metadata(self):
        (self.root / '.novel-creator').mkdir()
        (self.root / '.novel-creator/manifest.json').write_text('{}', encoding='utf-8')
        (self.root / '.gitignore').write_text('.novel-creator/local/\n', encoding='utf-8')
        info = debug.start(self.root)
        self.assertEqual(info['format'], 'legacy')
        self.assertIn('.novel-creator/local/debug', info['directory'])
        self.assertEqual(info['environment']['model'], 'unknown')
        self.assertEqual(info['environment']['host'], 'unknown')
        with self.assertRaises(ToolError):
            debug.setup(self.root)

    def test_status_inventory_ignores_non_session_inputs_and_exports(self):
        identifier = self.start()
        base = self.directory(identifier).parent
        (base / 'input.json').write_text('{}', encoding='utf-8')
        (base / 'report.zip').write_bytes(b'archive')
        self.assertEqual([s['debug_session'] for s in debug.status(self.root)['sessions']], [identifier])

    def test_malformed_stored_events_and_metadata_are_controlled(self):
        identifier = self.start()
        log = self.directory(identifier) / 'events.jsonl'
        first = log.read_bytes()
        for fields in ({'files': 42}, {'files': [None]}, {'content': []}):
            malformed = dict(self.events(identifier)[0], sequence=2, **fields)
            log.write_bytes(first + json.dumps(malformed).encode() + b'\n')
            exported = debug.export(self.root, identifier, self.root / ('bad-' + next(iter(fields)) + '-' + str(len(json.dumps(fields))) + '.zip'))
            self.assertTrue(exported['warnings'])
        metadata = self.directory(identifier) / 'session.json'
        info = json.loads(metadata.read_text())
        info['environment'] = []
        metadata.write_text(json.dumps(info))
        with self.assertRaises(ToolError):
            debug.export(self.root, identifier, self.root / 'broken-metadata.zip')

    def test_stop_recovers_interruption_between_event_and_metadata(self):
        identifier = self.start()
        directory = self.directory(identifier)
        before = (directory / 'session.json').read_bytes()
        debug.stop(self.root, identifier)
        count = len(self.events(identifier))
        (directory / 'session.json').write_bytes(before)
        self.assertEqual(debug.status(self.root, identifier)['state'], 'stopped')
        exported = debug.export(self.root, identifier)
        self.assertFalse(exported['partial'])
        with self.assertRaises(ToolError):
            debug.record(self.root, identifier, {'operation': 'late'})
        self.assertEqual(debug.stop(self.root, identifier)['state'], 'stopped')
        self.assertEqual(len(self.events(identifier)), count)

    def test_private_structured_fields_and_invalid_batch_do_not_record(self):
        identifier = self.start()
        for field in ('hidden_reasoning', 'environment', 'credentials', 'api_key'):
            with self.subTest(field=field), self.assertRaises(ToolError):
                debug.record(self.root, identifier, {'operation': 'capture', 'metadata': {field: 'private'}})
        with self.assertRaises(ToolError):
            debug.record(self.root, identifier, {'events': [{'operation': 'valid'}, {'operation': 'bad', 'files': [{'path': '.git/config'}]}]})
        self.assertEqual(len(self.events(identifier)), 1)

    def test_measured_failure_has_safe_error_metadata(self):
        identifier = self.start()
        with self.assertRaises(ToolError):
            with debug.activate(self.root, identifier, 'save'):
                raise ToolError(6, 'Do not capture arbitrary exception text')
        failure = self.events(identifier)[-1]
        self.assertEqual(failure['metadata']['error_code'], 6)
        self.assertEqual(failure['metadata']['exception_type'], 'ToolError')
        self.assertNotIn('Do not capture', json.dumps(failure))
