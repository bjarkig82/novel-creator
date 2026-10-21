import unittest

from novel_creator import records, validation
from tests.helpers import uid


class BenchmarkFixtureTests(unittest.TestCase):
    def test_scaled_fixture_is_a_valid_chain_with_requested_active_population_and_size(self):
        from tests.performance.benchmark_records import generate
        history, metadata = generate(uid(), exchanges=4, sessions=2, assertions=8, minimum_bytes=64000)
        self.assertEqual(len(history), 4)
        state = {}
        for index, bundle in enumerate(history):
            state = validation.validate_exchange(bundle, history[:index])
        self.assertEqual(sum(r['kind'] == 'session' for r in state.values()), 2)
        self.assertEqual(sum(r['kind'] == 'assertion' and r['status'] == 'accepted' for r in state.values()), 8)
        self.assertGreaterEqual(metadata['json_bytes'], 64000)
        self.assertEqual(metadata['json_bytes'], sum(len(records.canonical_bytes(e)) +
            len(',"payload_digest":""') + 64 for e in history))
