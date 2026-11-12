import contextlib
import io
import json
import unittest
from unittest.mock import patch

from novel_creator.cli import main


class NotebookCLI(unittest.TestCase):
    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_notebook_command_is_available(self):
        from novel_creator.cli import parser
        self.assertIn('notebook', parser().format_help())

    def test_invalid_requests_never_create_a_notebook(self):
        for args in (('N', '--path', ''), ('../escape',), ('N', '--title', ''),
                     ('N', '--language', 'fr'), ('N', '--title', 'A', '--title', 'B')):
            with self.subTest(args=args):
                code, out, _ = self.call('notebook', 'init', *args, '--json')
                self.assertEqual(code, 2)
                self.assertFalse(json.loads(out)['ok'])

    def test_additive_dispatch_preserves_unicode(self):
        # Import happens only after this new route is selected.
        with patch('novel_creator.notebook.initialize', return_value={
                'ok': True, 'data': {'ready': True, 'novel_path': 'N',
                                     'next_action': 'Open the folder in Codex.'}}) as create:
            code, out, _ = self.call('notebook', 'init', 'Folder', '--title', 'Þóra',
                                     '--language', 'is', '--json')
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)['ok'])
        self.assertEqual(create.call_args.kwargs['title'], 'Þóra')
        self.assertEqual(create.call_args.kwargs['language'], 'is')

    def test_host_and_skill_source_dispatch(self):
        with patch('novel_creator.notebook.initialize', return_value={
                'ok': True, 'data': {'ready': True}}) as create:
            code, out, _ = self.call('notebook', 'init', 'Folder', '--host', 'both',
                                     '--skill-source', 'plugin', '--json')
        self.assertEqual(code, 0)
        self.assertEqual(create.call_args.kwargs['host'], 'both')
        self.assertEqual(create.call_args.kwargs['skill_source'], 'plugin')

    def test_invalid_or_repeated_host_options_never_initialize(self):
        for args in (('--host', 'other'), ('--skill-source', 'other'),
                     ('--host', 'both', '--host', 'claude'),
                     ('--skill-source', 'plugin', '--skill-source', 'project')):
            with self.subTest(args=args), patch('novel_creator.notebook.initialize') as create:
                code, out, _ = self.call('notebook', 'init', 'Folder', *args, '--json')
                self.assertEqual(code, 2)
                create.assert_not_called()

    def test_human_success_reports_format_version_language_and_next_action(self):
        with patch('novel_creator.notebook.initialize', return_value={
                'ok': True, 'data': {'ready': True, 'novel_path': 'Story folder',
                                     'format': 'novel-notebook', 'version': 1,
                                     'language': 'is', 'next_action': 'Open the folder in Codex.'}}):
            code, out, _ = self.call('notebook', 'init', 'Story', '--language', 'is')
        self.assertEqual(code, 0)
        for expected in ('Story folder', 'novel-notebook', 'version 1',
                         'Language: is', 'Open the folder in Codex.'):
            self.assertIn(expected, out)

    def test_duplicate_json_is_rejected_before_setup(self):
        with patch('novel_creator.notebook.initialize', return_value={'ok': True}) as create:
            code, out, _ = self.call('notebook', 'init', 'Story', '--json', '--json')
        self.assertEqual(code, 2)
        self.assertFalse(json.loads(out)['ok'])
        create.assert_not_called()
