import contextlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from novel_creator.cli import main


class SimpleInitCLI(unittest.TestCase):
    def test_explicit_empty_destination_never_falls_back_to_name(self):
        with patch('novel_creator.install.initialize', return_value={'ok': True}) as initialize:
            code, out, _ = self.call('init', 'Uncreated Novel', '--path', '', '--json')
        self.assertEqual(code, 2)
        self.assertIn('destination', json.loads(out)['error']['message'].lower())
        initialize.assert_not_called()

    def test_missing_git_identity_is_named_without_global_edits(self):
        from novel_creator.install import _preflight
        from novel_creator.cli import ToolError
        def fake_git(root, *args, **kwargs):
            if args[0] == '--version':
                return b'git version 2.43.0'
            raise ToolError(5, 'Local Git operation failed')
        with patch('novel_creator.install.storage.git', side_effect=fake_git):
            with self.assertRaises(ToolError) as failure:
                _preflight(Path.cwd())
        self.assertEqual(failure.exception.code, 5)
        self.assertIn('identity', str(failure.exception).lower())

    def test_missing_dependency_has_an_actionable_json_diagnostic(self):
        with patch('novel_creator.install.initialize', side_effect=ModuleNotFoundError(name='jsonschema')):
            code, out, _ = self.call('init', 'N', '--json')
        self.assertEqual(code, 4)
        self.assertIn('environment', json.loads(out)['error']['message'])

    def test_runtime_handoff_does_not_dereference_environment_interpreter(self):
        from novel_creator.install import _command_result
        from unittest.mock import Mock
        manifest = Mock()
        manifest.read_bytes.return_value = b'{"checksums":{}}'
        result = {'warnings': [], 'data': {'saved': True, 'cleanup_required': False, 'already_initialized': False}}
        with patch('novel_creator.install.storage.safe_path', return_value=manifest), \
             patch('novel_creator.install.sys.executable', str(Path.cwd() / 'venv/bin/python')), \
             patch('novel_creator.install.Path.resolve', return_value=Path('/base/python')):
            output = _command_result(Path.cwd(), result)
        self.assertEqual(output['data']['runtime_python'], str(Path.cwd() / 'venv/bin/python'))

    def test_optional_settings_preserve_unicode_and_full_destination(self):
        with patch('novel_creator.install.initialize', return_value={'ok': True}) as initialize:
            code, out, _ = self.call('init', 'Folder', '--title', 'Bréf frá morgundeginum',
                                     '--language', 'is', '--path', 'other folder', '--json')
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)['ok'])
        self.assertEqual(Path(initialize.call_args.args[0]), Path.cwd() / 'other folder')
        self.assertEqual(json.loads(initialize.call_args.args[1]),
                         {'title': 'Bréf frá morgundeginum', 'manuscript_language': 'is'})
        request = initialize.call_args.kwargs['request']
        self.assertEqual(request['name'], 'Folder')
        self.assertEqual(request['title_argument'], 'Bréf frá morgundeginum')
        self.assertEqual(request['language_argument'], 'is')

    def test_invalid_optional_settings_are_read_only(self):
        for args in [('init', 'N', '--title', ''), ('init', 'N', '--language', 'fr'),
                     ('init', '--path', 'N', '--brief-file', 'b.json', '--title', 'Title'),
                     ('init', 'N', '--language', 'en', '--language', 'is')]:
            with self.subTest(args=args), patch('novel_creator.install.initialize') as initialize:
                code, out, _ = self.call(*args)
                self.assertEqual(code, 2)
                initialize.assert_not_called()

    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_name_only_invokes_existing_initializer_with_source_evidence(self):
        result = {'ok': True, 'data': {'saved': True, 'cleanup_required': False,
                  'ready': True, 'novel_path': '/novels/Bréf', 'runtime_python': '/runtime/python',
                  'launcher_path': '/novels/Bréf/.novel-creator/run.py',
                  'getting_started_path': '/guide.md', 'next_action': 'Open Codex; $novel-init'}}
        with patch('novel_creator.install.initialize', return_value=result) as initialize:
            code, out, _ = self.call('init', 'Bréf')
        self.assertEqual(code, 0)
        self.assertIn('Bréf', out)
        self.assertIn('/runtime/python', out)
        self.assertIn('$novel-init', out)
        self.assertEqual(json.loads(initialize.call_args.args[1]), {'title': 'Bréf'})
        self.assertEqual(initialize.call_args.kwargs['request']['name'], 'Bréf')
        self.assertEqual(Path(initialize.call_args.args[0]), Path.cwd() / 'Bréf')

    def test_invalid_names_and_modes_never_call_initializer(self):
        cases = [('init', name) for name in ['', ' ', '.', '..', '../escape', 'a/b', 'a\\b', 'a\x01']]
        cases += [('init', 'N', '--brief-file', 'brief.json'), ('init', '--path', 'N'),
                  ('init', 'N', '--unknown'), ('init', 'N', '--path', 'A', '--path', 'B')]
        for args in cases:
            with self.subTest(args=args), patch('novel_creator.install.initialize') as initialize:
                code, out, _ = self.call(*args)
                self.assertEqual(code, 2)
                self.assertFalse(json.loads(out)['ok'])
                initialize.assert_not_called()

    def test_version_and_help_do_not_initialize(self):
        from novel_creator import __version__
        for args, expected in [(('--version',), __version__), (('init', '--help'), 'getting-started')]:
            out = io.StringIO()
            with patch('novel_creator.install.initialize') as initialize, contextlib.redirect_stdout(out):
                with self.assertRaises(SystemExit) as exited:
                    main(list(args))
                self.assertEqual(exited.exception.code, 0)
                initialize.assert_not_called()
            self.assertIn(expected, out.getvalue())
