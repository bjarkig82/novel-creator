"""JSON output must remain UTF-8 even under a legacy terminal encoding."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator.install import initialize
from tests.helpers import git


class CliEncodingContract(unittest.TestCase):
    def test_success_and_error_json_remain_utf8_with_legacy_stdio(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Encoding Test')
            git(root, 'config', 'user.email', 'encoding@example.invalid')
            title = 'Bréf Þóru — 東京 🌒'
            initialize(root, json.dumps({'title': title}, ensure_ascii=False))
            launcher = root / '.novel-creator/run.py'
            for encoding in ('ascii', 'cp1252'):
                env = dict(os.environ, PYTHONIOENCODING=encoding, PYTHONUTF8='0')
                for command, code in [(('context',), 0), (('inspect', '--id', title), 4)]:
                    with self.subTest(encoding=encoding, command=command):
                        result = subprocess.run([sys.executable, '-B', launcher, *command,
                            '--novel', str(root), '--json'], cwd=root.parent, env=env,
                            capture_output=True)
                        self.assertEqual(result.returncode, code, result.stderr)
                        payload = json.loads(result.stdout.decode('utf-8'))
                        if code == 0:
                            self.assertEqual(payload['data']['project']['title']['original_text'], title)
                        else:
                            self.assertEqual(payload['error']['affected_refs'], [title])
                        self.assertNotIn(b'Traceback', result.stderr)
