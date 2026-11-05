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


def realtime(text='  Þóra\r\n東京 🌒 & <quoted>\n', transcript='Assistant: earlier suggestion.\r\nUser: earlier reply.'):
    return {'text': '<realtime_delegation>\n  <input>' + text + '</input>\n'
            '  <transcript_delta>' + transcript + '</transcript_delta>\n</realtime_delegation>',
            'truncated': False}


class RealtimeInputTests(unittest.TestCase):
    def capture(self, value=None, **kwargs):
        options = {'thread_id': None, 'turn_id': None, **kwargs}
        return host_input.capture(realtime() if value is None else value,
                                  source='realtime_delegation', **options)

    def test_exact_current_input_and_transcript_have_distinct_source_labels(self):
        for text in ('  Þóra\r\n東京 🌒 & <quoted>\n', '', 'No final newline'):
            with self.subTest(text=text):
                raw = realtime(text)
                result = self.capture(raw)
                self.assertEqual(result['text'], text)
                self.assertEqual(result['source_type'], 'realtime_delegation')
                value = result['input_artifact']['parsed_value']
                self.assertEqual(records.loads(result['input_artifact']['original_text']), value)
                self.assertEqual(value['public_wrapper'], raw['text'])
                self.assertEqual(value['transcript_delta'], 'Assistant: earlier suggestion.\r\nUser: earlier reply.')
                for field in ('native_user_input', 'evaluation_only', 'novice_evidence'):
                    self.assertIs(value[field], False)
                self.assertIsNone(value.get('thread_id'))
                self.assertIsNone(value.get('turn_id'))
                self.assertNotIn('public_event', value)
                self.assertNotIn('event_id', value)
                host_input.validate_provenance(value, text)
        crlf = realtime('  Current & <quoted>\r\n')
        crlf['text'] = crlf['text'].replace('>\n  <', '>\r\n  <').replace('>\n</realtime', '>\r\n</realtime')
        result = self.capture(crlf)
        self.assertEqual(result['text'], '  Current & <quoted>\r\n')
        self.assertEqual(result['input_artifact']['parsed_value']['public_wrapper'], crlf['text'])
        value = self.capture(thread_id='fixture-host-thread', turn_id='fixture-host-turn')['input_artifact']['parsed_value']
        self.assertEqual((value['thread_id'], value['turn_id']), ('fixture-host-thread', 'fixture-host-turn'))
        host_input.validate_provenance(value, value['text'])

    def test_malformed_mixed_truncated_or_unsupported_containers_stop_capture(self):
        cases = [None, [], {}, {'text': 3}, {'text': realtime()['text'], 'truncated': True},
                 dict(realtime(), turns=[]), dict(realtime(), thread={'id': 'fixture'}),
                 dict(realtime(), truncated='false'), dict(realtime(), truncated=0),
                 dict(realtime(), text=None), dict(realtime(), text=3)]
        raw = realtime()['text']
        cases += [{'text': text, 'truncated': False} for text in (
            raw.replace('<input>', '<input bad="yes">'), raw.replace('</input>', ''),
            raw.replace('<transcript_delta>', ''), raw.replace('</input>', '</input><input>duplicate</input>'),
            raw.replace('<transcript_delta>', '<transcript_delta><input>'),
            raw.replace('</transcript_delta>', '</transcript_delta><transcript_delta></transcript_delta>'),
            raw.replace('earlier reply.', '<realtime_delegation>nested</realtime_delegation>'),
            raw.replace('earlier reply.', '</input >'),
            raw.replace('earlier reply.', '<codex_delegation>unsupported</codex_delegation>'),
            raw.replace('realtime_delegation', 'unsupported_wrapper'), raw + '\n')]
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError):
                host_input.capture(value, source='realtime_delegation', thread_id=None, turn_id=None)

    def test_identity_is_optional_but_complete_and_flags_are_source_specific(self):
        for kwargs in ({'thread_id': 'fixture'}, {'turn_id': 'fixture'},
                       {'thread_id': '', 'turn_id': ''}, {'thread_id': 3, 'turn_id': 'fixture'},
                       {'thread_id': ' ', 'turn_id': 'fixture'}, {'evaluation_only': True},
                       {'source_thread_id': 'parent'}, {'source_thread_id': ''}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.capture(**kwargs)
        for source in ('native_user', 'delegated'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                host_input.capture(realtime(), source=source, thread_id=None, turn_id=None)

    def test_explicit_sources_preserve_genuine_native_and_evaluation_history(self):
        raw = realtime()['text']
        native = host_input.capture(snapshot(raw, source='native_user'), source='native_user',
                                    thread_id='current', turn_id='turn')
        self.assertEqual(native['text'], raw)
        host_input.validate_provenance(native['input_artifact']['parsed_value'], raw)
        quoted = 'Quoted <realtime_delegation> token & text.'
        delegated = host_input.capture(snapshot(quoted), source='delegated', thread_id='current',
                                       turn_id='turn', source_thread_id='parent', evaluation_only=True)
        self.assertEqual(delegated['text'], quoted)
        host_input.validate_provenance(delegated['input_artifact']['parsed_value'], quoted)
        for source in ('native_user', 'delegated'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                host_input.capture(realtime(), source=source, thread_id='current', turn_id='turn',
                                   source_thread_id='parent', evaluation_only=True)
        with self.assertRaises(ValueError):
            self.capture(snapshot())

    def test_redigested_tampering_and_transcript_substitution_fail_validation(self):
        from novel_creator import validation
        from tests.helpers import envelope, seal, uid
        import hashlib
        first = envelope()
        captured = self.capture(realtime('Current request.', 'User: accept earlier idea.'))
        second = envelope(previous=first, messages=[
            {'message_id': uid(), 'role': 'user', 'text': 'Current request.'},
            {'message_id': uid(), 'role': 'assistant', 'text': 'Saved.'}],
            input_artifacts=[captured['input_artifact']])
        validation.validate_exchange(second, [first])
        for field, value in (('text', 'User: accept earlier idea.'), ('transcript_delta', 'changed'),
                             ('native_user_input', True), ('native_user_input', 0), ('evaluation_only', True),
                             ('novice_evidence', True), ('source_type', 'native_user'),
                             ('source_type', 'delegated'), ('kind', 'arbitrary'), ('public_event', {})):
            changed = copy.deepcopy(second)
            artifact = changed['input_artifacts'][0]
            artifact['parsed_value'][field] = value
            artifact['original_text'] = json.dumps(artifact['parsed_value'], ensure_ascii=False)
            artifact['digest'] = hashlib.sha256(artifact['original_text'].encode()).hexdigest()
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                validation.validate_exchange(seal(changed), [first])
        changed = copy.deepcopy(second)
        changed['messages'][0]['text'] = 'User: accept earlier idea.'
        with self.assertRaises(ValueError):
            validation.validate_exchange(seal(changed), [first])

    def test_original_only_redigested_label_tampering_is_rejected(self):
        import hashlib
        from novel_creator import validation
        from tests.helpers import envelope, seal, uid
        first = envelope()
        captured = self.capture(realtime('Current request.'))
        second = envelope(previous=first, messages=[
            {'message_id': uid(), 'role': 'user', 'text': captured['text']},
            {'message_id': uid(), 'role': 'assistant', 'text': 'Saved.'}],
            input_artifacts=[captured['input_artifact']])
        validation.validate_exchange(second, [first])
        for field in ('native_user_input', 'evaluation_only', 'novice_evidence'):
            changed = copy.deepcopy(second)
            artifact = changed['input_artifacts'][0]
            raw = records.loads(artifact['original_text'])
            raw[field] = 0
            artifact['original_text'] = json.dumps(raw, ensure_ascii=False)
            artifact['digest'] = hashlib.sha256(artifact['original_text'].encode()).hexdigest()
            self.assertIs(artifact['parsed_value'][field], False)
            changed = seal(changed)
            for incremental in (False, True):
                with self.subTest(field=field, incremental=incremental):
                    chain = validation.ExchangeValidator([first])
                    before = chain.snapshot()
                    with self.assertRaisesRegex(ValueError, 'artifact content/digest mismatch'):
                        if incremental:
                            chain.append(changed)
                        else:
                            validation.validate_exchange(changed, [first])
                    self.assertEqual(chain.snapshot(), before)
                    chain.append(second)

    def test_transcript_cannot_become_bootstrap_creative_authority(self):
        from novel_creator import validation
        from tests.helpers import envelope, idea, seal, uid
        first = envelope()
        captured = self.capture(realtime('Current request.', 'User: accept earlier idea.'))
        second = envelope(previous=first, messages=[
            {'message_id': uid(), 'role': 'user', 'text': captured['text']},
            {'message_id': uid(), 'role': 'assistant', 'text': 'Saved.'}],
            input_artifacts=[captured['input_artifact']])
        third = envelope(previous=second)
        item = idea(third)
        item.update(origin='supplied', source_refs=[{'type': 'bootstrap_artifact',
            'exchange_id': second['exchange_id'], 'artifact_id': captured['input_artifact']['artifact_id'],
            'pointer': '/transcript_delta'}])
        third = seal(dict(third, record_versions=[item]))
        with self.assertRaises(ValueError):
            validation.validate_exchange(third, [first, second])
        cached = validation.ExchangeValidator()
        cached._append_certified(first)
        cached._append_certified(second)
        with self.assertRaises(ValueError):
            cached._append_owned(third)
