"""Prevent false-positive evidence in the Phase 22 evaluation collector."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from tests.evaluations.verify_phase22 import verify_observation, verify_run, verify_input, verify_display
from novel_creator import host_input


class EvaluationObservationTests(unittest.TestCase):
    def test_recovery_preserves_original_provenance_and_checks_actual_display(self):
        original, exchange, point = self.fixture()
        recovery = copy.deepcopy(original['turns'][0])
        recovery['id'] = 'recovery-turn'
        recovery['items'] = recovery['items'][1:]
        verify_input(original, exchange, expected='Þóra?\n', thread_id='child', parent='parent')
        self.assertEqual(verify_display(recovery, exchange), point)
        with self.assertRaises(ValueError):
            verify_input({'turns': [recovery]}, exchange, expected='Þóra?\n', thread_id='child', parent='parent')
        recovery['items'][-1]['text'] += 'Changed during recovery'
        with self.assertRaisesRegex(ValueError, 'Saved/displayed response differs'):
            verify_display(recovery, exchange)

    def test_app_continuation_does_not_invent_source_turn_completion(self):
        original, exchange, point = self.fixture()
        continued = copy.deepcopy(original['turns'][0])
        continued['id'] = 'automatic-continuation'
        continued['items'] = continued['items'][1:]
        original['turns'][0]['status'] = 'inProgress'
        original['turns'][0]['items'] = original['turns'][0]['items'][:1]
        with self.assertRaises(ValueError):
            self.verify(original, exchange)
        verify_input(original, exchange, expected='Þóra?\n', thread_id='child', parent='parent')
        self.assertEqual(verify_display(continued, exchange), point)
        continued['status'] = 'inProgress'
        with self.assertRaises(ValueError):
            verify_display(continued, exchange)

    def test_empty_or_missing_submitted_observations_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            (folder / 'run.json').write_text(json.dumps({'tasks': {}, 'authorization': {}}))
            with self.assertRaisesRegex(ValueError, 'empty run cannot pass'):
                verify_run(folder)
            (folder / 'MISSING-driver.json').write_text(json.dumps({
                'case_id': 'MISSING', 'submitted': True, 'inputs': {'en': 'Input'}}))
            with self.assertRaisesRegex(ValueError, 'Missing submitted observation'):
                verify_run(folder)

    def fixture(self):
        event = {'type': 'functionCallOutput', 'id': 'input', 'name': 'send_message_to_thread',
                 'namespace': 'codex_app', 'output': {'text':
                 '<codex_delegation>\n  <source_thread_id>parent</source_thread_id>\n  <input>Þóra?\n</input>\n</codex_delegation>',
                 'truncated': False}}
        snapshot = {'thread': {'id': 'child'}, 'turns': [{'id': 'turn', 'status': 'completed', 'items': [event]}]}
        capture = host_input.capture(snapshot, thread_id='child', turn_id='turn', source='delegated',
                                     source_thread_id='parent', evaluation_only=True)
        point = {'exchange_id': 'exchange', 'git_head': 'commit', 'sequence': 2}
        snapshot['turns'][0]['items'].extend([
            {'type': 'commandExecution', 'status': 'completed', 'exitCode': 0,
             'output': {'text': '{"ok":true,"data":{"saved":true},"checkpoint":'
                        '{"exchange_id":"exchange","git_head":"commit","sequence":2}}', 'truncated': False}},
            {'type': 'agentMessage', 'phase': 'final_answer', 'text': 'Saved.\n'}])
        exchange = {'exchange_id': 'exchange', 'sequence': 2, 'messages': [
            {'role': 'user', 'text': 'Þóra?\n'}, {'role': 'assistant', 'text': 'Saved.\n'}],
            'input_artifacts': [capture['input_artifact']]}
        return snapshot, exchange, point

    def verify(self, observation, exchange):
        return verify_observation(observation, exchange, expected='Þóra?\n', thread_id='child', parent='parent')

    def test_exact_unicode_whitespace_and_order(self):
        raw, bundle, checkpoint = self.fixture()
        self.assertEqual(self.verify(raw, bundle), checkpoint)

    def test_creative_progress_before_save_cannot_pass_from_matching_final(self):
        raw, bundle, _ = self.fixture()
        text = 'The island has no bridge; this is established.'
        raw['turns'][0]['items'].insert(1, {'id': 'progress', 'type': 'agentMessage',
            'phase': 'commentary', 'text': text})
        review = [{'id': 'progress', 'text': text, 'classification': 'story',
                   'reason': 'Asserts a new creative result before its confirmed save.'}]
        with self.assertRaisesRegex(ValueError, 'Story commentary precedes'):
            verify_observation(raw, bundle, expected='Þóra?\n', thread_id='child', parent='parent',
                               commentary_review=review)

    def test_unreviewed_or_changed_commentary_cannot_receive_a_review_pass(self):
        raw, bundle, _ = self.fixture()
        raw['turns'][0]['items'].insert(1, {'id': 'progress', 'type': 'agentMessage',
            'phase': 'commentary', 'text': 'I will read the saved context.'})
        for review in ([], [{'id': 'progress', 'text': 'Different text', 'classification': 'administrative'}]):
            with self.subTest(review=review), self.assertRaises(ValueError):
                verify_observation(raw, bundle, expected='Þóra?\n', thread_id='child', parent='parent',
                                   commentary_review=review)

    def test_input_and_response_changes_are_rejected(self):
        for position in (0, 1):
            raw, bundle, _ = self.fixture()
            bundle['messages'][position]['text'] = bundle['messages'][position]['text'].rstrip()
            with self.subTest(position=position), self.assertRaises(ValueError):
                self.verify(raw, bundle)

    def test_missing_late_failed_or_wrong_save_is_rejected(self):
        for mode in ('missing', 'late', 'failed', 'wrong_exchange', 'truncated'):
            raw, bundle, _ = self.fixture()
            items = raw['turns'][0]['items']
            if mode == 'missing':
                items.pop(1)
            elif mode == 'late':
                items[1], items[2] = items[2], items[1]
            elif mode == 'failed':
                items[1]['exitCode'] = 5
            elif mode == 'wrong_exchange':
                items[1]['output']['text'] = items[1]['output']['text'].replace('exchange', 'other')
            else:
                items[1]['output']['truncated'] = True
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.verify(raw, bundle)

    def test_provenance_incomplete_turn_and_duplicate_final_are_rejected(self):
        for mode in ('provenance', 'active', 'duplicate', 'reasoning'):
            raw, bundle, _ = self.fixture()
            if mode == 'provenance':
                bundle['input_artifacts'][0]['parsed_value']['source_type'] = 'native_user'
            elif mode == 'active':
                raw['turns'][0]['status'] = 'inProgress'
            elif mode == 'duplicate':
                raw['turns'][0]['items'].append(copy.deepcopy(raw['turns'][0]['items'][-1]))
            else:
                raw['turns'][0]['items'].append({'type': 'reasoning'})
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                self.verify(raw, bundle)
