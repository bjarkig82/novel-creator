"""Exercise the read-only CLI against a real worktree with staged and unstaged edits."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class NotebookIndex(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.notes = self.root / 'notebook'
        fixture = Path(__file__).resolve().parents[1] / 'fixtures/notebook-grouped/after'
        shutil.copytree(fixture, self.notes)
        self.summary = self.notes / 'working-summary.md'
        self.topic = self.notes / 'topics/keeper.md'
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        subprocess.run(['git', '-C', self.root, 'add', '.'], check=True)

    def run_check(self, code, json_output=True):
        def snapshot():
            return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        before = snapshot()
        command = [sys.executable, '-m', 'novel_creator', 'notebook', 'check-index', '--path', self.root]
        if json_output:
            command.append('--json')
        result = subprocess.run(command, text=True, encoding='utf-8', capture_output=True)
        self.assertEqual(snapshot(), before)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout)['data'] if json_output else result.stdout

    def test_stale_then_matching(self):
        original = self.summary.read_text(encoding='utf-8')
        self.summary.write_text(original.replace('5 | 1 | 0 | 1 | 1', '3 | 4 | 2 | 0 | 2'), encoding='utf-8')
        data = self.run_check(1)
        mismatch, = data['mismatches']
        self.assertEqual(mismatch['topic'], 'keeper')
        self.assertEqual(mismatch['displayed'], dict(accepted=3, proposed=4, rejected=2, open=0, resolved=2))
        self.assertEqual(mismatch['correct'], dict(accepted=5, proposed=1, rejected=0, open=1, resolved=1))
        self.assertIn('accepted=5', self.run_check(1, False))
        self.summary.write_text(original, encoding='utf-8')
        self.assertEqual(self.run_check(0)['checked_rows'], 1)

    def test_partial_icelandic_columns_and_history_followed_by_current_items(self):
        body = self.topic.read_text(encoding='utf-8').replace('## Revisions', '## Breytingasaga')
        self.topic.write_text(body + '\n## Núverandi atriði\n### Annað\nItem-ID: test\nType: statement\nState: rejected\nPerspective: objective\nOrigin: writer\nLinks: none\n', encoding='utf-8')
        project = self.notes / 'project.md'
        project.write_text(project.read_text(encoding='utf-8').replace('"en"', '"is"'), encoding='utf-8')
        header = self.summary.read_text(encoding='utf-8').split('| Topic')[0]
        self.summary.write_text(header + '| Opnar spurningar | Efni | Hafnað |\n| --- | --- | --- |\n| 1 | [Alex](topics/keeper.md) | 0 |\n', encoding='utf-8')
        row, = self.run_check(1)['mismatches']
        self.assertEqual(row['displayed'], {'open': 1, 'rejected': 0})
        self.assertEqual(row['correct']['rejected'], 1)

    def test_failed_row_does_not_hide_sibling_mismatch(self):
        first = self.summary.read_text(encoding='utf-8').replace('| 5 |', '| 2 |')
        for cell in ('[Lost](topics/missing.md) | 1', '[Escape](../project.md) | 1',
                     '[Alex](topics/keeper.md) | unknown'):
            with self.subTest(cell=cell):
                self.summary.write_text(first + '| ' + cell + ' | 0 | 0 | 0 | 0 |\n', encoding='utf-8')
                data = self.run_check(1)
                self.assertEqual(len(data['mismatches']), 1)
                self.assertTrue(data['unavailable'])

    def test_invalid_current_state_and_unsupported_table(self):
        body = self.topic.read_text(encoding='utf-8')
        self.topic.write_text(body.replace('State: accepted', 'State: open', 1), encoding='utf-8')
        self.assertTrue(self.run_check(1)['unavailable'])
        self.topic.write_text(body, encoding='utf-8')
        summary = self.summary.read_text(encoding='utf-8')
        self.summary.write_text(summary.replace('| Accepted |', '| Unknown |'), encoding='utf-8')
        self.assertTrue(self.run_check(1)['unavailable'])

    def test_fenced_examples_and_navigation_are_not_counts(self):
        example = ('~~~text\n## Revisions\nItem-ID: name\nType: question\nState: resolved\n~~~\n')
        body = self.topic.read_text(encoding='utf-8')
        self.topic.write_text(body.replace('## Current profile', example + '## Current profile'), encoding='utf-8')
        summary = self.summary.read_text(encoding='utf-8')
        self.summary.write_text(summary + '\nRecent focus: open [Chapter 2](topics/chapter-2.md).\n\n~~~md\n' + summary.split('historical revisions excluded.')[1]
                                + '~~~\n\n| Topic | Notes |\n| --- | --- |\n'
                                + '| [Alex](topics/keeper.md) | Chapter 2 |\n', encoding='utf-8')
        self.assertEqual(self.run_check(0)['checked_rows'], 1)

    def test_unsupported_format_and_incomplete_item(self):
        body = self.topic.read_text(encoding='utf-8')
        for invalid in (body.replace('"version": 1', '"version": true'),
                        body.replace('Item-ID: name', 'Item-ID: motive'),
                        body.replace('State: accepted', 'State: unknown', 1),
                        body.replace('Origin: Writer chose the name Alex.', ''),
                        body.replace('Type: statement', 'Type: question', 1)):
            with self.subTest(invalid=invalid[:80]):
                self.topic.write_text(invalid, encoding='utf-8')
                self.assertTrue(self.run_check(1)['unavailable'])

    def test_setext_history_excludes_former_only_id_and_ends_at_peer(self):
        current = self.topic.read_text(encoding='utf-8').split('## Revisions')[0]
        template = ('Item-ID: {}\nType: statement\nState: accepted\nPerspective: objective\n'
                    'Origin: writer\nLinks: none\n')
        self.topic.write_text(current + '\nRevisions\n---------\n' + template.format('retired')
                              + '\nCurrent additions\n-----------------\n' + template.format('additional'),
                              encoding='utf-8')
        mismatch, = self.run_check(1)['mismatches']
        self.assertEqual(mismatch['correct']['accepted'], 6)

    def test_empty_and_escaped_navigation_cells_preserve_counts(self):
        original = self.summary.read_text(encoding='utf-8')
        intro = original.split('| Topic')[0]
        for title, value in [('Notes', ''), ('Notes', r'past \| present'), ('Last updated', 'Yesterday')]:
            with self.subTest(title=title, value=value):
                self.summary.write_text(intro + f'| Topic | Accepted | {title} |\n| --- | --- | --- |\n'
                                        + f'| [Alex](topics/keeper.md) | 3 |{value}|\n', encoding='utf-8')
                result = self.run_check(1)
                self.assertFalse(result['unavailable'])
                mismatch, = result['mismatches']
                self.assertEqual(mismatch['correct']['accepted'], 5)

    def test_unknown_numeric_or_duplicate_count_column_is_unavailable(self):
        original = self.summary.read_text(encoding='utf-8')
        for column in ('Other counts', 'Accepted statements'):
            with self.subTest(column=column):
                self.summary.write_text(original.replace('Proposed |', column + ' |'), encoding='utf-8')
                self.assertTrue(self.run_check(1)['unavailable'])

    def test_no_count_rows(self):
        self.summary.write_text(self.summary.read_text(encoding='utf-8').split('| Topic')[0], encoding='utf-8')
        self.assertEqual(self.run_check(0)['checked_rows'], 0)
        self.assertIn('No topic-index count rows', self.run_check(0, False))
