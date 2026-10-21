import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from novel_creator import records, storage
from novel_creator.install import initialize
from tests.helpers import git, uid, record, idea


class ResumeJourney(unittest.TestCase):
    def test_three_sessions_recover_twenty_ideas_ten_decisions_five_questions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Resume Test')
            git(root, 'config', 'user.email', 'resume@example.invalid')
            initialize(root, '{}')
            expected = {'idea': set(), 'decision': set(), 'question': set()}
            sessions = []
            first_idea = None
            for number, (nideas, ndecisions, nquestions) in enumerate(((7, 4, 2), (7, 3, 2), (6, 3, 1))):
                previous = storage.read_history(root)[-1]
                text = f'Explore session {number}; defer these decisions.'
                exchange = records.new_exchange(previous['novel_id'], previous=previous, expected_head=storage.head(root),
                    messages=[{'message_id': uid(), 'role': 'user', 'text': text},
                              {'message_id': uid(), 'role': 'assistant', 'text': 'Possibilities retained; no canon established.'}])
                source = records.current_user_source(exchange)
                session = records.start_session(exchange, topic='Same topic', mode='open' if number == 1 else 'guided')
                sessions.append(session)
                proposals = [dict(idea(exchange, origin='supplied', source_refs=[source]),
                                  statement=f'Possibility {number}/{i}') for i in range(nideas)]
                if first_idea is None:
                    first_idea = proposals[0]
                decisions = [record(exchange, 'decision', origin='supplied', source_refs=[source], action='defer',
                    user_message_ref=source, span={'start': 0, 'end': len(text)}, target_refs=[{'id': proposals[i]['id']}],
                    selected_parts=[], prior_refs=[], result_refs=[], reason='Explicit defer fixture',
                    affected_refs=[], review_required_refs=[]) for i in range(ndecisions)]
                questions = [record(exchange, 'question', origin='supplied', source_refs=[source], text=f'Question {number}/{i}?',
                    related_refs=[{'id': proposals[i]['id']}], alternative_ids=[], state='open', resolution_decision_id=None)
                    for i in range(nquestions)]
                session['related_record_ids'] = [r['id'] for r in proposals + decisions]
                session['unresolved_question_ids'] = [r['id'] for r in questions]
                exchange.update(session_id=session['id'], record_versions=[session, *proposals, *decisions, *questions])
                exchange['payload_digest'] = records.digest(exchange)
                storage.save(root, exchange)
                for r in proposals + decisions + questions:
                    expected[r['kind']].add(r['id'])
            # Fresh interpreter, installed launcher, no framework PYTHONPATH.
            result = subprocess.run([sys.executable, '-B', str(root / '.novel-creator/run.py'), 'context',
                '--novel', str(root), '--json'], cwd=root.parent, env=dict(os.environ, PYTHONPATH='', PYTHONUTF8='1'),
                capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            context = json.loads(result.stdout)['data']
            self.assertEqual(len(context['sessions']), 3)
            for kind, identifiers in expected.items():
                found = [r for r in context['records'] if r['kind'] == kind]
                self.assertEqual({r['id'] for r in found}, identifiers)
                self.assertTrue(all(r['source_refs'] for r in found))
            self.assertEqual({s['mode'] for s in context['sessions']}, {'guided', 'open'})
            self.assertEqual(context['saved_response_display'], 'unconfirmed')
            self.assertFalse(any(r.get('status') == 'accepted' for r in context['records']))
            for command, field, count in [(('session', 'list'), 'sessions', 3), (('inspect', '--kind', 'decision'), 'records', 10)]:
                result = subprocess.run([sys.executable, '-B', str(root / '.novel-creator/run.py'), *command,
                    '--novel', str(root), '--json'], cwd=root.parent,
                    env=dict(os.environ, PYTHONPATH='', PYTHONUTF8='1'), capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(len(json.loads(result.stdout)['data'][field]), count)
            previous = storage.read_history(root)[-1]
            correction = records.new_exchange(previous['novel_id'], previous=previous, expected_head=storage.head(root),
                session_id=sessions[0]['id'], messages=[{'message_id': uid(), 'role': 'user', 'text': 'Correction: the keeper hid the seal, not the letter.'},
                {'message_id': uid(), 'role': 'assistant', 'text': 'The corrected possibility is retained; it is not canon.'}])
            corrected = dict(first_idea, revision=2, previous_revision=1, statement='The keeper hid the seal.',
                             source_refs=[records.current_user_source(correction)], origin='supplied')
            correction['record_versions'] = [corrected, records.revise_session(sessions[0], correction)]
            correction['payload_digest'] = records.digest(correction)
            storage.save(root, correction)
            saved = storage.read_history(root)
            versions = [r for e in saved for r in e['record_versions'] if r['id'] == first_idea['id']]
            self.assertEqual(versions, [first_idea, corrected])
            self.assertEqual(corrected['status'], 'proposed')
