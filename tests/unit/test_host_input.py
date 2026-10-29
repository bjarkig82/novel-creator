"""Source parsing is structural evidence, never human/novice evidence."""
import copy
import json
from pathlib import Path
import unittest

from novel_creator import host_input, records


def snapshot(text='  Þóra\r\n東京 🌒\n\n', source='delegated'):
    item = {'type': 'functionCallOutput', 'id': 'event', 'namespace': 'codex_app',
            'name': 'send_message_to_thread', 'output': {'truncated': False, 'text':
            '<codex_delegation>\n  <source_thread_id>parent</source_thread_id>\n  <input>'
            + text + '</input>\n</codex_delegation>'}}
    if source == 'native_user':
        item = {'type': 'userMessage', 'id': 'event', 'content': [{'type': 'text', 'text': text}]}
    return {'thread': {'id': 'current'}, 'turns': [{'id': 'turn', 'items': [item]}]}


class HostInputTests(unittest.TestCase):
    def capture(self, value, **kwargs):
        return host_input.capture(value, thread_id='current', turn_id='turn',
                                  source='delegated', source_thread_id='parent',
                                  evaluation_only=True, **kwargs)

    def test_delegated_text_and_committable_provenance_are_exact(self):
        for text in ('  Þóra\r\n東京 🌒\n\n', 'No newline', '', '<quoted> & text'):
            with self.subTest(text=text):
                result = self.capture(snapshot(text))
                self.assertEqual(result['text'], text)
                artifact = result['input_artifact']
                provenance = records.loads(artifact['original_text'])
                self.assertEqual(provenance, artifact['parsed_value'])
                self.assertEqual(provenance['source_type'], 'delegated')
                self.assertEqual(provenance['event_type'], 'functionCallOutput')
                self.assertEqual(provenance['source_thread_id'], 'parent')
                self.assertEqual(provenance['event_id'], 'event')
                self.assertEqual(provenance['text'], text)
                self.assertFalse(provenance['native_user_input'])
                self.assertFalse(provenance['novice_evidence'])
                self.assertTrue(provenance['evaluation_only'])

    def test_native_mode_remains_explicit_and_does_not_fall_back(self):
        value = snapshot(source='native_user')
        result = host_input.capture(value, thread_id='current', turn_id='turn', source='native_user')
        self.assertEqual(result['text'], value['turns'][0]['items'][0]['content'][0]['text'])
        self.assertTrue(result['input_artifact']['parsed_value']['native_user_input'])
        with self.assertRaises(ValueError):
            host_input.capture(snapshot(), thread_id='current', turn_id='turn', source='native_user')
        with self.assertRaises(ValueError):
            host_input.capture(snapshot(), thread_id='current', turn_id='turn', source='delegated',
                               source_thread_id='parent')

    def test_provenance_cannot_mismatch_current_message_or_source_labels(self):
        from novel_creator import validation
        from tests.helpers import envelope, seal, uid
        first = envelope()
        captured = self.capture(snapshot())
        exchange = envelope(previous=first, messages=[
            {'message_id': uid(), 'role': 'user', 'text': captured['text']},
            {'message_id': uid(), 'role': 'assistant', 'text': 'Saved.'}],
            input_artifacts=[captured['input_artifact']])
        validation.validate_exchange(exchange, [first])
        for field, value in [('text', 'different'), ('native_user_input', True),
                             ('novice_evidence', True), ('evaluation_only', False), ('kind', 'arbitrary')]:
            changed = copy.deepcopy(exchange)
            artifact = changed['input_artifacts'][0]
            artifact['parsed_value'][field] = value
            artifact['original_text'] = json.dumps(artifact['parsed_value'], ensure_ascii=False)
            import hashlib
            artifact['digest'] = hashlib.sha256(artifact['original_text'].encode()).hexdigest()
            with self.subTest(field=field), self.assertRaises(ValueError):
                validation.validate_exchange(seal(changed), [first])

    def test_host_provenance_never_becomes_a_bootstrap_creative_source(self):
        from novel_creator import validation
        from tests.helpers import envelope, idea, seal
        first = envelope()
        captured = self.capture(snapshot('Explore Þóra.'))
        second = envelope(previous=first, input_artifacts=[captured['input_artifact']])
        third = envelope(previous=second)
        item = idea(third)
        item.update(origin='supplied', source_refs=[{'type': 'bootstrap_artifact',
            'exchange_id': second['exchange_id'], 'artifact_id': captured['input_artifact']['artifact_id'],
            'pointer': '/text'}])
        third = seal(dict(third, record_versions=[item]))
        with self.assertRaises(ValueError):
            validation.validate_exchange(third, [first, second])
        cached = validation.ExchangeValidator()
        cached._append_certified(first)
        cached._append_certified(second)
        with self.assertRaises(ValueError):
            cached._append_owned(third)

    def test_rejects_wrong_stale_ambiguous_truncated_and_malformed_sources(self):
        cases = []
        value = snapshot(); value['thread']['id'] = 'other'; cases.append(value)
        value = snapshot(); value['turns'].insert(0, {'id': 'newer', 'items': []}); cases.append(value)
        value = snapshot(); value['turns'].append({'id': 'newer', 'items': []}); cases.append(value)
        value = snapshot(); value['truncated'] = True; cases.append(value)
        value = snapshot(); value['turns'][0]['truncated'] = True; cases.append(value)
        value = snapshot(); value['turns'][0]['items'] *= 2; cases.append(value)
        value = snapshot(); value['turns'][0]['items'] += snapshot(source='native_user')['turns'][0]['items']; cases.append(value)
        for key, invalid in [('truncated', True), ('text', '<input>preview</input>')]:
            value = snapshot(); value['turns'][0]['items'][0]['output'][key] = invalid; cases.append(value)
        for key, invalid in [('namespace', 'other'), ('name', 'arbitrary_tool'), ('id', '')]:
            value = snapshot(); value['turns'][0]['items'][0][key] = invalid; cases.append(value)
        value = snapshot(); value['turns'][0]['items'][0]['output']['text'] = value['turns'][0]['items'][0]['output']['text'].replace('parent', 'wrong'); cases.append(value)
        cases += [snapshot('</input><input>ambiguous'), None, {}, {'thread': [], 'turns': []}]
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.capture(value)

    def test_replays_four_observed_public_events_without_reclassifying_them(self):
        folder = Path(__file__).resolve().parents[1] / 'evaluations/product-host-runs/20261023T095949Z'
        run = json.loads((folder / 'run.json').read_bytes())
        for language in ('en', 'is'):
            for phase in ('creation', 'followup'):
                data = json.loads((folder / f'{language}-{phase}-native.json').read_bytes())
                result = host_input.capture(data, thread_id=data['thread']['id'],
                    turn_id=data['turns'][0]['id'], source='delegated', evaluation_only=True,
                    source_thread_id=run['authorization']['parent_thread_id'])
                intended = (run['tasks'][language]['initial_prompt'] if phase == 'creation' else
                            (folder / f'{language}-followup-driver-prompt.txt').read_bytes().decode('utf-8'))
                self.assertEqual(result['text'], intended)
                self.assertFalse(result['input_artifact']['parsed_value']['native_user_input'])
