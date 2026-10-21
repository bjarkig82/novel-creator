import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator import records, storage
from novel_creator.install import initialize
from tests.helpers import git, uid


class InitializationJourney(unittest.TestCase):
    def test_empty_and_supplied_briefs_reopen_and_change_settings_through_installed_cli(self):
        with tempfile.TemporaryDirectory() as folder:
            parent = Path(folder).resolve()
            for index, brief in enumerate(({}, {'title': 'Bréf', 'original_concept': 'Þóra fær bréf.\n',
                    'manuscript_language': 'is', 'creative_brief': {'genre': 'Leyndardómur', 'audience': None},
                    'workflow_preferences': {'suggestions': 'Few'}})):
                with self.subTest(brief=brief):
                    root = parent / str(index)
                    root.mkdir()
                    git(root, 'init', '-b', 'main')
                    git(root, 'config', 'user.name', 'Journey Test')
                    git(root, 'config', 'user.email', 'journey@example.invalid')
                    source = parent / f'brief-{index}.json'
                    source.write_bytes(json.dumps(brief, ensure_ascii=False).encode('utf-8'))
                    env = dict(os.environ, PYTHONUTF8='1')
                    output = subprocess.run([sys.executable, '-B', '-m', 'novel_creator', 'init', '--path', str(root),
                        '--brief-file', str(source), '--json'], capture_output=True, text=True, env=env, encoding='utf-8')
                    self.assertEqual(output.returncode, 0, output.stderr)
                    result = json.loads(output.stdout)
                    before = storage.read_history(root)
                    project = before[0]['record_versions'][0]
                    messages = [{'message_id': uid(), 'role': 'user', 'text': 'Rename it Tomorrow; fewer suggestions.'},
                                {'message_id': uid(), 'role': 'assistant', 'text': 'Renamed. Brainstorming is optional.'}]
                    exchange = records.new_exchange(result['novel_id'], previous=before[-1],
                        expected_head=storage.head(root), messages=messages)
                    exchange['record_versions'] = [records.revise_project(project,
                        {'title': 'Tomorrow', 'workflow_preferences': {'suggestions': 'Fewer'}}, exchange)]
                    exchange['payload_digest'] = records.digest(exchange)
                    payload = root / '.novel-creator/local/evidence/settings.json'
                    payload.parent.mkdir(parents=True)
                    payload.write_text(json.dumps(exchange, ensure_ascii=False), encoding='utf-8')
                    launcher = str(root / '.novel-creator/run.py')
                    output = subprocess.run([sys.executable, '-B', launcher, 'exchange', 'save', '--novel', str(root),
                        '--input', str(payload), '--json'], cwd=parent, env=dict(env, PYTHONPATH=''),
                        capture_output=True, text=True, encoding='utf-8')
                    self.assertEqual(output.returncode, 0, output.stderr)
                    after = records.fold(storage.read_history(root))[project['id']]
                    self.assertEqual(after['id'], project['id'])
                    self.assertEqual(after['original_concept'], project['original_concept'])
                    self.assertEqual(after['creative_brief'], project['creative_brief'])
                    self.assertEqual(after['title']['original_text'], 'Tomorrow')
                    self.assertEqual(after['workflow_preferences']['suggestions']['original_text'], 'Fewer')
                    self.assertTrue(all(r['kind'] == 'novel_project' for e in storage.read_history(root) for r in e['record_versions']))
