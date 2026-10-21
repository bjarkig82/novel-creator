import unittest
from novel_creator import records, validation
from tests.helpers import envelope, record, idea, seal, held_conflict_transition


class ContinuityTests(unittest.TestCase):
    def test_conflict_metadata_cannot_release_hold_now_or_in_a_later_exchange(self):
        for disposition in ('open', 'deferred'):
            for field in ('severity', 'assessment', 'affected_refs'):
                for promote in (False, True):
                    with self.subTest(disposition=disposition, field=field, promote=promote):
                        first, exchange, finding = held_conflict_transition(disposition=disposition)
                        validation.validate_exchange(first, [])
                        changes = {'severity': 'advisory', 'assessment': 'uncertainty',
                                   'affected_refs': [{'id': finding['id']}]}
                        changed = dict(finding, revision=2, previous_revision=1,
                                       **{field: changes[field]})
                        exchange['record_versions'] = ([*exchange['record_versions'], changed]
                                                       if promote else [changed])
                        with self.assertRaisesRegex(ValueError, 'hold'):
                            validation.validate_exchange(seal(exchange), [first])

    def test_user_directed_resolution_releases_prior_hold_without_extra_approval(self):
        for disposition, action in [('resolved', 'resolve'), ('intentional', 'resolve'),
                ('revised_canon', 'revise'), ('revised_idea', 'revise'), ('rejected_idea', 'reject')]:
            with self.subTest(disposition=disposition):
                first, exchange, finding = held_conflict_transition()
                exchange['messages'][0]['text'] = ('Reject or revise the idea; keep alternatives unaccepted.'
                    if disposition in ('rejected_idea', 'revised_idea') else
                    'Resolve the conflict; accept the revised proposal.')
                source = records.current_user_source(exchange)
                decision = record(exchange, 'decision', action=action, user_message_ref=source,
                    span={'start': 0, 'end': 20}, target_refs=[{'id': finding['id'], 'revision': 2}],
                    selected_parts=[], prior_refs=[{'id': finding['id'], 'revision': 1}],
                    result_refs=[], reason='Explicit conflict direction', affected_refs=[], review_required_refs=[])
                changed = dict(finding, revision=2, previous_revision=1, disposition=disposition,
                    decision_ids=[decision['id']], narrative_explanation='Intentional unreliable viewpoint'
                    if disposition == 'intentional' else None)
                proposal_id = first['record_versions'][0]['id']
                if disposition in ('rejected_idea', 'revised_idea'):
                    exchange['record_versions'] = [changed, decision]
                else:
                    exchange['record_versions'].extend([changed, decision])
                state = validation.validate_exchange(seal(exchange), [first])
                self.assertEqual(state[finding['id']]['disposition'], disposition)
                self.assertEqual(state[proposal_id]['status'],
                    'proposed' if disposition in ('rejected_idea', 'revised_idea') else 'accepted')

    def test_finding_cannot_be_silently_resolved_to_bypass_hold(self):
        first = envelope()
        proposal = idea(first)
        finding = record(first, 'finding', category='world_rule', assessment='conflict', severity='significant',
            affected_refs=[{'id': proposal['id']}], explanation='Rule conflict', consequences=[],
            resolution_options=[], disposition='open', decision_ids=[], narrative_explanation=None)
        first = seal(dict(first, record_versions=[proposal, finding]))
        exchange = envelope(previous=first)
        revised = dict(finding, revision=2, previous_revision=1, disposition='resolved')
        with self.assertRaises(ValueError):
            validation.validate_exchange(seal(dict(exchange, record_versions=[revised])), [first])

    def test_open_and_deferred_significant_findings_hold_affected_canon(self):
        for disposition in ('open', 'deferred'):
            bootstrap = envelope()
            first = envelope(previous=bootstrap)
            proposal = idea(first)
            finding = record(first, 'finding', category='knowledge', assessment='conflict', severity='significant',
                affected_refs=[{'id': proposal['id']}], explanation='Knowledge arrives too late',
                consequences=['Action lacks its prerequisite'], resolution_options=['Revise or defer'],
                disposition=disposition, decision_ids=[], narrative_explanation=None)
            first = seal(dict(first, record_versions=[proposal, finding]))
            exchange = envelope(previous=first)
            source = records.current_user_source(exchange)
            accepted = dict(proposal, revision=2, previous_revision=1, status='accepted')
            decision = record(exchange, 'decision', action='accept', user_message_ref=source,
                span={'start': 0, 'end': 7}, target_refs=[{'id': proposal['id'], 'revision': 2}],
                selected_parts=[], prior_refs=[], result_refs=[], reason='Accept', affected_refs=[], review_required_refs=[])
            accepted['decision_ids'] = [decision['id']]
            with self.subTest(disposition=disposition), self.assertRaises(ValueError):
                validation.validate_exchange(seal(dict(exchange, record_versions=[accepted, decision])), [bootstrap, first])
            # Proposal-only exchanges remain safe and do not silently clear the finding.
            safe = dict(proposal, revision=2, previous_revision=1, status='unresolved')
            state = validation.validate_exchange(seal(dict(exchange, record_versions=[safe])), [bootstrap, first])
            self.assertEqual(state[finding['id']]['disposition'], disposition)

    def test_unknown_time_bounds_cannot_look_established(self):
        exchange = envelope()
        element = record(exchange, 'story_element', element_type='character', display_name='Þóra', aliases=[],
            status='proposed', assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
        axis = {'precision': 'unknown', 'event_anchor': None, 'start': 'Chapter 1', 'end': None, 'before_refs': [], 'after_refs': []}
        assertion = record(exchange, 'assertion', subject_element_id=element['id'], predicate='knows', value='secret',
            perspective='character_belief', holder_id=element['id'], reader_audience=None,
            time_ref={'chronology': axis, 'narrative': axis}, truth_state='unknown', status='proposed', decision_ids=[], supersedes=None)
        with self.assertRaises(ValueError):
            validation.validate_exchange(seal(dict(exchange, record_versions=[element, assertion])), [])
