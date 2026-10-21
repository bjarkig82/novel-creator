import unittest
from novel_creator import records, validation
from novel_creator.context import direct_impact
from tests.helpers import envelope, record, idea, seal


class AuthorityTests(unittest.TestCase):
    def test_replacement_assertion_cannot_leave_replaced_fact_current(self):
        bootstrap = envelope()
        element = record(bootstrap, 'story_element', element_type='character', display_name='Keeper', aliases=[],
            status='proposed', assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
        bootstrap = seal(dict(bootstrap, record_versions=[element]))
        first = envelope(previous=bootstrap)
        source = records.current_user_source(first)
        axis = {'precision': 'unknown', 'event_anchor': None, 'start': None, 'end': None, 'before_refs': [], 'after_refs': []}
        assertion = record(first, 'assertion', subject_element_id=element['id'], predicate='is sender', value=True,
            perspective='author_truth', holder_id=None, reader_audience=None, time_ref={'chronology': axis, 'narrative': axis},
            truth_state='affirmed', status='accepted', decision_ids=[], supersedes=None)
        def decision(exchange, targets, action='accept'):
            src = records.current_user_source(exchange)
            return record(exchange, 'decision', action=action, user_message_ref=src, span={'start': 0, 'end': 7},
                target_refs=targets, selected_parts=[], prior_refs=[], result_refs=targets,
                reason='Explicit fixture selection', affected_refs=[], review_required_refs=[])
        accepted = decision(first, [{'id': assertion['id'], 'revision': 1}])
        assertion['decision_ids'] = [accepted['id']]
        first = seal(dict(first, record_versions=[assertion, accepted]))
        validation.validate_exchange(first, [bootstrap])
        second = envelope(previous=first)
        replacement = dict(assertion, id=__import__('uuid').uuid4().__str__(), created_exchange_id=second['exchange_id'],
                           value=False, supersedes={'id': assertion['id'], 'revision': 1})
        changed = decision(second, [{'id': replacement['id'], 'revision': 1}], action='revise')
        replacement['decision_ids'] = [changed['id']]
        with self.assertRaises(ValueError):
            validation.validate_exchange(seal(dict(second, record_versions=[replacement, changed])), [bootstrap, first])
        retired = dict(assertion, revision=2, previous_revision=1, status='superseded', decision_ids=[changed['id']])
        changed['target_refs'].append({'id': retired['id'], 'revision': 2})
        changed['prior_refs'] = [{'id': assertion['id'], 'revision': 1}]
        state = validation.validate_exchange(seal(dict(second, record_versions=[retired, replacement, changed])), [bootstrap, first])
        self.assertEqual(state[retired['id']]['status'], 'superseded')
        self.assertEqual(state[replacement['id']]['status'], 'accepted')
    def test_routine_checkpoint_triggers_summary_without_mutating_records(self):
        exchange = envelope()
        proposal = idea(exchange)
        question = record(exchange, 'question', text='Why?', related_refs=[], alternative_ids=[], state='open', resolution_decision_id=None)
        decision = {'id': 'decision', 'kind': 'decision'}
        state = {r['id']: r for r in [proposal, question, decision]}
        for mode, requested, closed, expected in [('on_request', False, False, False),
                ('on_request', True, False, True), ('session_close', False, True, True),
                ('session_close', False, False, False), ('every_exchange', False, False, True)]:
            with self.subTest(mode=mode, requested=requested, closed=closed):
                summary = records.checkpoint_summary({'review_preferences': {'routine_checkpoint': mode}}, state,
                    requested=requested, session_closed=closed)
                self.assertEqual(summary['required'], expected)
                self.assertEqual(summary['pause_agent_exploration'], expected)
                self.assertEqual(summary['proposals'], [proposal])
                self.assertEqual(summary['open_questions'], [question])
                self.assertEqual(summary['decisions'], [decision])
                self.assertTrue(summary['derived'])
        self.assertEqual(proposal['status'], 'proposed')

    def test_partial_selection_cannot_promote_whole_compound_idea(self):
        bootstrap = envelope()
        first = envelope(previous=bootstrap)
        proposal = idea(first)
        proposal.update(statement='Keeper is sender and murderer', selected_parts=['sender', 'murderer'])
        first = seal(dict(first, record_versions=[proposal]))
        exchange = envelope(previous=first)
        source = records.current_user_source(exchange)
        revised = dict(proposal, revision=2, previous_revision=1, status='accepted', source_refs=[source], origin='supplied')
        decision = record(exchange, 'decision', action='accept', user_message_ref=source, span={'start': 0, 'end': 7},
            source_refs=[source], origin='supplied', target_refs=[{'id': proposal['id'], 'revision': 1}],
            selected_parts=['sender'], prior_refs=[], result_refs=[], reason='Only sender selected',
            affected_refs=[], review_required_refs=[])
        revised['decision_ids'] = [decision['id']]
        with self.assertRaises(ValueError):
            validation.validate_exchange(seal(dict(exchange, record_versions=[revised, decision])), [bootstrap, first])

    def test_direct_impact_is_sourced_not_transitive_guessing(self):
        state = {'a': {'id': 'a', 'kind': 'idea'},
                 'b': {'id': 'b', 'kind': 'story_element', 'dependency_refs': [{'id': 'a', 'revision': 1}]},
                 'c': {'id': 'c', 'kind': 'story_element', 'dependency_refs': [{'id': 'b'}]},
                 'd': {'id': 'd', 'kind': 'idea', 'statement': 'a'}}
        impact = direct_impact(state, ['a'])
        self.assertEqual([r['id'] for r in impact], ['b'])
