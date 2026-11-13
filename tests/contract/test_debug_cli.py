"""Debug controls preserve the existing single-JSON CLI boundary."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch

from novel_creator.cli import main, parser


class DebugCLI(unittest.TestCase):
    def call(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(args))
        return code, json.loads(stdout.getvalue()), stderr.getvalue()

    def test_controls_reject_missing_and_duplicate_arguments(self):
        for arguments in (
            ('debug', 'start'),
            ('debug', 'record', '--novel', 'N', '--input', 'event.json'),
            ('debug', 'stop', '--novel', 'N'),
            ('debug', 'export', '--novel', 'N'),
            ('debug', 'status', '--novel', 'N', '--novel', 'M'),
            ('input', 'capture', '--capture-file', 'input.json', '--source', 'realtime_delegation',
             '--debug-session', 'id'),
        ):
            with self.subTest(arguments=arguments):
                code, result, stderr = self.call(*arguments)
                self.assertEqual(code, 2)
                self.assertFalse(result['ok'])
                self.assertIn('error', result)
                self.assertNotIn('Traceback', stderr)

    def test_existing_debug_flags_are_explicit_and_separate_from_story_session(self):
        args = parser().parse_args(['context', '--novel', 'N', '--session', 'story', '--debug-session', 'debug'])
        self.assertEqual(args.session, 'story')
        self.assertEqual(args.debug_session, 'debug')
        self.assertIsNone(parser().parse_args(['context', '--novel', 'N']).debug_session)

    def test_debug_controls_skip_legacy_maintenance_and_wrap_result(self):
        with patch('novel_creator.debug.dispatch', return_value={'debug_session': 'id'}) as dispatch, \
                patch('novel_creator.maintenance.ensure_ready', side_effect=AssertionError('must bypass')):
            code, result, stderr = self.call('debug', 'status', '--novel', 'N', '--json')
        self.assertEqual(code, 0)
        self.assertEqual(result, {'ok': True, 'data': {'debug_session': 'id'}})
        self.assertEqual(stderr, '')
        self.assertEqual(dispatch.call_args.args[0].debug_action, 'status')
