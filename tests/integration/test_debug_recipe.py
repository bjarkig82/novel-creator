"""Execute the published recording recipes against disposable projects and real CLI."""
from contextlib import contextmanager
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from novel_creator.install import initialize
from tests.helpers import git


SOURCE = Path(__file__).resolve().parents[2]
GUIDES = {'notebook': SOURCE / 'notebook/workflows/debugging.md',
          'legacy': SOURCE / 'workflows/debugging.md'}


def recipe(kind, language='python'):
    text = GUIDES[kind].read_text(encoding='utf-8')
    return re.search(r'```' + language + r'\n(.*?)\n```', text, re.DOTALL).group(1) + '\n'


class DebugRecordingRecipe(unittest.TestCase):
    @contextmanager
    def project(self, kind):
        with tempfile.TemporaryDirectory(prefix='debug recipe ') as temporary:
            root = Path(temporary).resolve() / 'novel with spaces'
            root.mkdir()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Recipe Test')
            git(root, 'config', 'user.email', 'recipe@example.invalid')
            launcher = None
            if kind == 'legacy':
                initialize(root, '{"title":"Synthetic recipe"}')
                launcher = root / '.novel-creator/run.py'
            else:
                (root / 'notebook').mkdir()
                (root / 'notebook/project.md').write_text('Synthetic notebook', encoding='utf-8')
                (root / '.novel-notebook/workflows').mkdir(parents=True)
                (root / '.gitignore').write_text('.novel-notebook/local/\n', encoding='utf-8')
            prefix = [sys.executable, str(launcher)] if launcher else [sys.executable, '-m', 'novel_creator']
            started = subprocess.run(prefix + ['debug', 'start', '--novel', str(root), '--json'],
                                     capture_output=True, text=True, encoding='utf-8', check=True)
            session = json.loads(started.stdout)['data']
            directory = Path(session['directory'])
            helper = directory / 'record-observation.py'
            helper.write_text(recipe(kind), encoding='utf-8')
            yield root, session['debug_session'], directory, helper, launcher

    def record(self, project, *arguments):
        root, session, _, helper, launcher = project
        command = [sys.executable, str(helper), str(root), session]
        if launcher:
            command += ['--launcher', str(launcher)]
        return subprocess.run(command + list(arguments), capture_output=True, text=True, encoding='utf-8')

    def events(self, directory):
        return [json.loads(line) for line in (directory / 'events.jsonl').read_text(encoding='utf-8').splitlines()]

    def test_documented_helper_preserves_unicode_whitespace_and_all_phases(self):
        self.assertEqual(recipe('notebook'), recipe('legacy'))
        original = '  \u00de\u00f3ra\u2019s \u201cidea\u201d \u2014 don\u2019t writer\'s $() ` interpolate\r\nSecond line\n\n  '
        for kind in GUIDES:
            with self.subTest(kind=kind), self.project(kind) as project:
                root, _, directory, _, _ = project
                text = directory / 'public text.txt'
                text.write_bytes(original.encode('utf-8'))
                working = root / ('story/recipe.json' if kind == 'legacy' else 'notebook/recipe.md')
                working.parent.mkdir(exist_ok=True)
                working.write_bytes(original.encode('utf-8'))
                for phase in ('before', 'context', 'after'):
                    result = self.record(project, '--text-file', str(text), '--file',
                                         working.relative_to(root).as_posix(), '--phase', phase)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    saved = json.loads(result.stdout)
                    self.assertTrue(saved['ok'])
                    self.assertEqual(len(saved['data']['recorded_sequences']), 1)
                    event = self.events(directory)[-1]
                    self.assertEqual(event['files'][0]['phase'], phase)
                    self.assertEqual((directory / event['files'][0]['attachment']).read_bytes(), original.encode('utf-8'))
                    content = json.loads((directory / event['content']['attachment']).read_bytes())
                    self.assertEqual(content, original)
                for story_root in ('notebook', 'manuscript', 'research', 'reviews', 'story'):
                    result = self.record(project, '--file', story_root + '/not-yet-created.TXT')
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(self.events(directory)[-1]['files'], [
                        {'path': story_root + '/not-yet-created.TXT', 'phase': 'context', 'exists': False}])

    def test_reserved_names_and_unsupported_paths_fail_without_appending(self):
        for kind in GUIDES:
            with self.subTest(kind=kind), self.project(kind) as project:
                directory = project[2]
                original = self.events(directory)
                for operation in ('', '   ', 'debug.started', 'debug.anything'):
                    result = self.record(project, '--operation', operation)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('Capture unconfirmed', result.stderr)
                    self.assertIn('nonreserved operation', result.stderr)
                    self.assertEqual(self.events(directory), original)
                for path in ('AGENTS.md', '.novel-notebook/local/event.json', '../story/note.md',
                             '/story/note.md', 'story\\note.md', 'story/note.csv', 'story/.hidden.md',
                             'story/private/note.md', 'story/Secrets/note.md', 'story/password-note.txt',
                             'story/trailing./note.md', 'story/colon:name.md'):
                    result = self.record(project, '--file', path, '--phase', 'before')
                    self.assertNotEqual(result.returncode, 0, path)
                    self.assertIn('outside supported public story files', result.stderr)
                    self.assertEqual(self.events(directory), original)

    def test_failed_before_then_gap_and_late_snapshot_preserve_honest_evidence(self):
        for kind in GUIDES:
            with self.subTest(kind=kind), self.project(kind) as project:
                root, _, directory, _, _ = project
                working = root / 'research/recipe.md'
                working.parent.mkdir(exist_ok=True)
                working.write_bytes(b'Original synthetic bytes\n')
                # Non-UTF-8 bytes make the actual before capture fail.
                working.write_bytes(b'Original synthetic bytes\xff\n')
                failed = self.record(project, '--file', 'research/recipe.md', '--phase', 'before')
                self.assertNotEqual(failed.returncode, 0)
                self.assertIn('Snapshot must contain UTF-8', failed.stderr)
                self.assertEqual(len(self.events(directory)), 1)
                # Otherwise authorized writing can proceed; its original was not captured.
                working.write_bytes(b'Later synthetic bytes\n')
                gap = directory / 'gap.txt'
                gap.write_text('Before capture failed; original bytes are unavailable in this log.', encoding='utf-8')
                result = self.record(project, '--operation', 'capture.gap', '--text-file', str(gap))
                self.assertEqual(result.returncode, 0, result.stderr)
                result = self.record(project, '--file', 'research/recipe.md', '--phase', 'context')
                self.assertEqual(result.returncode, 0, result.stderr)
                events = self.events(directory)
                self.assertEqual([event['operation'] for event in events], ['debug.started', 'capture.gap', 'context.read'])
                snapshots = [ref for event in events for ref in event.get('files', [])]
                self.assertEqual([ref['phase'] for ref in snapshots], ['context'])
                self.assertEqual((directory / snapshots[0]['attachment']).read_bytes(), b'Later synthetic bytes\n')
                self.assertFalse(any(b'Original synthetic' in item.read_bytes() for item in (directory / 'attachments').iterdir()))

    @unittest.skipUnless(shutil.which('powershell') or shutil.which('pwsh'), 'PowerShell is unavailable')
    def test_documented_powershell_invocation_and_legacy_update_hold(self):
        shell = shutil.which('powershell') or shutil.which('pwsh')
        for kind in GUIDES:
            with self.subTest(kind=kind), self.project(kind) as project:
                root, session, directory, helper, _ = project
                text = directory / 'public-text.txt'
                text.write_bytes('Synthetic \u00de\u00f3ra\u2019s text\r\n'.encode())
                script = recipe(kind, 'powershell')
                for placeholder, value in {
                    'C:\\verified-runtime\\python.exe': sys.executable,
                    'C:\\books\\My Novel': str(root),
                    'RETURNED-DEBUG-SESSION-ID': session,
                    'RETURNED-SESSION-DIRECTORY\\record-observation.py': str(helper),
                    'RETURNED-SESSION-DIRECTORY\\public-text.txt': str(text),
                }.items():
                    script = script.replace(placeholder, value)
                # These are commands entered at a PowerShell prompt, rather than
                # an unsigned .ps1 requiring a machine execution-policy change.
                command = [shell, '-NoProfile', '-NonInteractive', '-Command', '-']
                completed = subprocess.run(command, input=script, capture_output=True, text=True)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(len(self.events(directory)), 2)
                if kind == 'legacy':
                    hold = root / '.novel-creator/local/update/active.json'
                    hold.parent.mkdir(parents=True, exist_ok=True)
                    hold.write_text('{}', encoding='utf-8')
                    before = self.events(directory)
                    completed = subprocess.run(command, input=script, capture_output=True, text=True)
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertEqual(self.events(directory), before)
                    self.assertTrue(hold.is_file())
