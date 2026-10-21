"""Structural installed-tool journeys; authored replies are not host judgments."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator import records, storage
from novel_creator.install import initialize
from tests.helpers import git, idea, uid


class GuidanceJourney(unittest.TestCase):
    def test_installed_turns_preserve_mode_topic_preferences_and_exact_messages(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Guidance Test')
            git(root, 'config', 'user.email', 'guidance@example.invalid')
            initialize(root, '{}')
            launcher = root / '.novel-creator/run.py'
            env = dict(os.environ, PYTHONPATH='', PYTHONUTF8='1')

            def cli(*args):
                result = subprocess.run([sys.executable, '-B', str(launcher), *args,
                    '--novel', str(root), '--json'], cwd=root.parent, env=env,
                    capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                return json.loads(result.stdout)

            turns = [
                ('Explore the lighthouse.', 'What draws the keeper to the lighthouse?\n',
                 'guided', 'The lighthouse', False),
                ("Let us explore freely. Focus on the keeper's childhood.\n",
                 'An abandoned signal station is one possibility.\n',
                 'open', "The keeper's childhood", False),
                ('Fewer suggestions, please. Þóra might have hidden the seal.\n\n',
                 'We can stay with that possibility.\n',
                 'open', "The keeper's childhood", True),
                ('Guide me again. Focus on the missing letter.',
                 'Why would the letter matter to the keeper?',
                 'guided', 'The missing letter', False),
            ]
            session = None
            proposals = []
            expected_messages = []
            for user, reply, mode, topic, fewer in turns:
                history = storage.read_history(root)
                project = records.fold(history)[history[0]['novel_id']]
                messages = [{'message_id': uid(), 'role': 'user', 'text': user},
                            {'message_id': uid(), 'role': 'assistant', 'text': reply}]
                exchange = records.new_exchange(project['id'], previous=history[-1],
                    expected_head=storage.head(root), messages=messages)
                if session is None:
                    session = records.start_session(exchange, topic=topic)
                else:
                    session = records.revise_session(session, exchange, mode=mode, topic=topic)
                proposal = idea(exchange, origin='supplied',
                    source_refs=[records.current_user_source(exchange)])
                proposal['statement'] = 'Structural possibility ' + str(len(proposals))
                proposals.append(proposal)
                session['related_record_ids'] = [r['id'] for r in proposals]
                versions = [session, proposal]
                if fewer:
                    versions.append(records.revise_project(project,
                        {'workflow_preferences': {'suggestions': 'Fewer'}}, exchange))
                exchange.update(session_id=session['id'], record_versions=versions)
                exchange['payload_digest'] = records.digest(exchange)
                payload = root / '.novel-creator/local/evidence/guidance.json'
                payload.parent.mkdir(parents=True, exist_ok=True)
                payload.write_bytes(json.dumps(exchange, ensure_ascii=False).encode('utf-8'))
                receipt = cli('exchange', 'save', '--input', str(payload))
                context = cli('context', '--session', session['id'])
                self.assertEqual(context['checkpoint'], receipt['checkpoint'])
                self.assertEqual(context['data']['selected_session']['mode'], mode)
                self.assertEqual(context['data']['selected_session']['topic'], topic)
                self.assertEqual(context['data']['last_saved_response'], reply)
                self.assertEqual(context['data']['saved_response_display'], 'unconfirmed')
                self.assertEqual(context['data']['current_canon'], [])
                actual_proposals = [r for r in context['data']['records'] if r['kind'] == 'idea']
                self.assertEqual(actual_proposals, proposals)
                if len(proposals) >= 3:
                    self.assertEqual(context['data']['project']['workflow_preferences']
                        ['suggestions']['original_text'], 'Fewer')
                expected_messages.append(messages)

            saved = storage.read_history(root)
            self.assertEqual([e['messages'] for e in saved[1:]], expected_messages)
            inspected = cli('inspect', '--id', session['id'])['data']['history']
            self.assertEqual([s['mode'] for s in inspected], ['guided', 'open', 'open', 'guided'])
            self.assertEqual([s['revision'] for s in inspected], [1, 2, 3, 4])
            self.assertEqual(inspected[0]['topic'], 'The lighthouse')
            for exchange in saved[1:]:
                for version in exchange['record_versions']:
                    self.assertEqual(version['source_refs'], [records.current_user_source(exchange)])
