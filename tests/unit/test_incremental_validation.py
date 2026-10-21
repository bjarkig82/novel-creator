import copy
import unittest

from novel_creator import validation
from tests.helpers import envelope, idea, seal, held_conflict_transition


class IncrementalValidationTests(unittest.TestCase):
    def test_failed_append_does_not_change_state_or_predecessor(self):
        chain = validation.ExchangeValidator()
        first, acceptance, finding = held_conflict_transition()
        chain.append(first)
        initial = chain.snapshot()
        changed = dict(finding, revision=2, previous_revision=1, severity='advisory')
        with self.assertRaises(ValueError):
            chain.append(seal(dict(acceptance, record_versions=[*acceptance['record_versions'], changed])))
        self.assertEqual(chain.snapshot(), initial)
        safe = envelope(previous=first)
        safe['record_versions'] = [idea(safe)]
        safe = seal(safe)
        chain.append(safe)
        self.assertEqual(chain.snapshot(), validation.validate_exchange(safe, [first]))

    def test_input_and_result_mutation_cannot_change_indexed_history(self):
        chain = validation.ExchangeValidator()
        first = envelope()
        first['record_versions'] = [idea(first)]
        first = seal(first)
        original = copy.deepcopy(first)
        chain.append(first)
        first['record_versions'][0]['statement'] = 'Mutated outside validator'
        result = chain.snapshot()
        result[original['record_versions'][0]['id']]['statement'] = 'Mutated returned snapshot'
        exchange = envelope(previous=original)
        chain.append(exchange)
        self.assertEqual(chain.snapshot()[original['record_versions'][0]['id']]['statement'], 'Possibility')

    def test_stream_checks_schema_digest_identity_and_cross_bundle_references(self):
        from tests.performance.benchmark_records import generate
        from tests.helpers import uid
        history, _ = generate(uid(), exchanges=8, sessions=3, assertions=16, minimum_bytes=0)
        for index in (0, 3, 7):
            for corruption in ('digest', 'version', 'reference', 'revision'):
                with self.subTest(index=index, corruption=corruption):
                    chain = validation.ExchangeValidator()
                    for previous in history[:index]:
                        chain.append(previous)
                    bad = copy.deepcopy(history[index])
                    if corruption == 'digest':
                        bad['payload_digest'] = '0' * 64
                    elif corruption == 'version':
                        bad['schema_version'] = '2.0'
                    elif corruption == 'reference':
                        bad['continuity_review']['reviewed_record_refs'] = [{'id': uid()}]
                    else:
                        bad['record_versions'][0]['revision'] += 1
                    if corruption != 'digest':
                        bad = seal(bad)
                    with self.assertRaises(ValueError):
                        chain.append(bad)
                    chain.append(history[index])
