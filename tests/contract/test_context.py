import unittest
from novel_creator import records, storage
from novel_creator.cli import ToolError
from novel_creator.context import read
from tests.helpers import envelope, idea, record, repository, seal


class ContextContract(unittest.TestCase):
    def test_sessions_focus_history_and_saved_display_unconfirmed(self):
        with repository() as root:
            initial = envelope(root)
            storage.save(root, initial)
            history = [initial]
            sessions = []
            ideas = []
            for index in range(2):
                exchange = envelope(root, previous=history[-1])
                session = record(exchange, 'session', topic='Same name', mode='guided' if index == 0 else 'open',
                    state='open', started_exchange_id=exchange['exchange_id'], last_exchange_id=exchange['exchange_id'],
                    related_record_ids=[], unresolved_question_ids=[], derived_context_ref=None)
                proposal = idea(exchange, id=__import__('uuid').uuid4().__str__())
                session['related_record_ids'] = [proposal['id']]
                exchange.update(session_id=session['id'], record_versions=[session, proposal])
                exchange = seal(exchange)
                storage.save(root, exchange)
                history.append(exchange)
                sessions.append(session)
                ideas.append(proposal)
            listed = read(root, operation='session')
            self.assertEqual(len(listed['data']['sessions']), 2)
            focused = read(root, session=sessions[0]['id'])
            ids = {r['id'] for r in focused['data']['records']}
            self.assertIn(ideas[0]['id'], ids)
            self.assertNotIn(ideas[1]['id'], ids)
            self.assertEqual(focused['data']['selected_session']['mode'], 'guided')
            self.assertEqual(focused['data']['saved_response_display'], 'unconfirmed')
            inspected = read(root, operation='inspect', identifier=ideas[0]['id'])
            self.assertEqual(inspected['data']['history'], [ideas[0]])
            self.assertEqual(inspected['checkpoint']['sequence'], 3)
            with self.assertRaises(ToolError) as error:
                read(root, session=ideas[0]['id'])
            self.assertEqual(error.exception.code, 4)

    def test_incomplete_review_is_disclosed_and_missing_record_not_empty(self):
        with repository() as root:
            bootstrap = envelope(root)
            storage.save(root, bootstrap)
            exchange = envelope(root, previous=bootstrap)
            exchange['continuity_review'].update(coverage='incomplete', canon_hold_refs=['*'])
            storage.save(root, seal(exchange))
            result = read(root)
            self.assertEqual(result['data']['coverage'], 'incomplete')
            self.assertEqual(result['data']['canon_hold_refs'], ['*'])
            self.assertFalse(result['data']['narrative_consistency_verified'])
            with self.assertRaises(ToolError):
                read(root, operation='inspect', identifier='missing')
