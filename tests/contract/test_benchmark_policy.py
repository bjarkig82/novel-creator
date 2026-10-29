"""Benchmark exit status respects the owner's latency-policy scope."""
from contextlib import redirect_stdout
import io
import json
import unittest
from unittest.mock import patch

from tests.performance import benchmark_records as benchmark


class BenchmarkPolicyTests(unittest.TestCase):
    def run_benchmark(self, warm_read=0.5, save=None):
        observations = [dict(status='ok', seconds=0.8, observed_count=3),
                        dict(status='ok', seconds=warm_read, observed_count=3),
                        save or dict(status='ok', seconds=5.0, observed_count=3)]
        output = io.StringIO()
        args = ['benchmark', '--exchanges', '2', '--sessions', '1',
                '--assertions', '1', '--mib', '0', '--runs', '1']
        # Real disposable fixture creation; controlled measurements isolate
        # qualification policy from machine load and wall-clock timing.
        with patch('sys.argv', args), patch.object(benchmark, 'measure', side_effect=observations), redirect_stdout(output):
            code = benchmark.main()
        return code, json.loads(output.getvalue())

    def test_successful_slow_saves_are_measured_without_a_latency_pass_claim(self):
        code, result = self.run_benchmark()
        self.assertEqual(code, 0)
        self.assertEqual(result['save']['p95_seconds'], 5.0)
        self.assertIsNone(result['save']['target_seconds'])
        self.assertIsNone(result['save']['passes'])
        self.assertTrue(result['save']['completed_successfully'])

    def test_successful_slow_reads_are_measured_without_a_latency_pass_claim(self):
        code, result = self.run_benchmark(warm_read=2.5)
        self.assertEqual(code, 0)
        self.assertEqual(result['read']['p95_seconds'], 2.5)
        self.assertIsNone(result['read']['target_seconds'])
        self.assertIsNone(result['read']['passes'])
        self.assertTrue(result['read']['completed_successfully'])

    def test_save_timeout_cannot_become_success(self):
        code, result = self.run_benchmark(save=dict(status='timeout', elapsed_lower_bound_seconds=30))
        self.assertEqual(code, 1)
        self.assertEqual(result['save']['failure']['status'], 'timeout')
        self.assertIsNone(result['save']['p95_seconds'])

    def test_save_operation_failure_cannot_become_success(self):
        code, result = self.run_benchmark(save=dict(status='error', returncode=5))
        self.assertEqual(code, 1)
        self.assertEqual(result['save']['failure']['returncode'], 5)
        self.assertIsNone(result['save']['p95_seconds'])
