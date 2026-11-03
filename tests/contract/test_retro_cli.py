import io
import json
import unittest
from contextlib import redirect_stdout, redirect_stderr
from novel_creator.cli import main
from tests.retro_helpers import fixtures


class RetroCLI(unittest.TestCase):
    def test_default_off_json_without_github(self):
        with fixtures() as (root, *unused):
            output = io.StringIO()
            with redirect_stdout(output), redirect_stderr(io.StringIO()):
                result = main(['retro', 'status', '--novel', str(root), '--json'])
            self.assertEqual(result, 0)
            self.assertFalse(json.loads(output.getvalue())['data']['enabled'])

    def test_enable_requires_explicit_flag(self):
        with fixtures() as (root, checkout, *unused):
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                result = main(['retro', 'enable', '--novel', str(root), '--checkout', str(checkout)])
            self.assertEqual(result, 2)
