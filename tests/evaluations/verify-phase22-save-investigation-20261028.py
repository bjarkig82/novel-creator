"""Recompute diagnostic comparisons and retain the independent 30-run gate."""
import hashlib
import json
import math
from pathlib import Path
import statistics

base = Path(__file__).resolve().parent
root = base.parent.parent
artifacts = []
comparisons = {}
for name, count, expected_order in (
    ('balance-normal', 12, [(4, 2, False), (1, 2, False), (4, 1, False),
                          (4, 1, False), (1, 2, False), (4, 2, False)] * 2),
    ('schedule', 8, [(4, 2, False), (4, 2, True), (4, 2, True), (4, 2, False)] * 2),
):
    path = base / f'windows-phase22-save-{name}-20261028.jsonl'
    artifacts.append(path)
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines()]
    first, samples, last = rows[0], rows[1:-1], rows[-1]
    assert first['fixture'] == dict(sessions=100, exchanges=5000, active_assertions=10000,
        json_bytes=26215716, synthetic=True, fully_validated=True)
    assert first['packing'] == 'none explicitly requested'
    assert len(samples) == count and last['source_unchanged']
    for file, digest in first['source'].items():
        assert hashlib.sha256((root / file).read_bytes()).hexdigest() == digest, file
    grouped = {}
    for i, (sample, policy) in enumerate(zip(samples, expected_order), 5001):
        actual = (sample['history_workers'], sample['initial_hash_workers'], sample.get('defer_guard', False))
        assert actual == policy and sample['observed_count'] == i
        assert sample['guards'] == 2
        assert sample['hashed_files'] == sample['batch_objects'] == 2 * i
        assert sample['seconds'] > 0
        grouped.setdefault(str(policy), []).append(sample['seconds'])
    comparisons[name] = {policy: {'samples': values, 'median': statistics.median(values)}
                         for policy, values in grouped.items()}
    assert sorted(last['medians'].values()) == sorted(x['median'] for x in comparisons[name].values())

path = base / 'windows-phase22-ordinary-30-20261028.json'
artifacts.append(path)
gate = json.loads(path.read_text(encoding='utf-8-sig'))
qualification = {}
assert gate['fixture']['fully_validated'] and gate['cold_read']['status'] == 'ok'
for operation, target in [('read', 2.0), ('save', 1.0)]:
    observed = gate[operation]
    samples = observed['samples_seconds']
    assert observed['completed_runs'] == len(samples) == 30 and observed['failure'] is None
    assert observed['target_seconds'] == target
    p95 = sorted(samples)[math.ceil(len(samples) * .95) - 1]
    assert p95 == observed['p95_seconds'] and (p95 <= target) == observed['passes']
    qualification[operation] = {'p95_seconds': p95, 'target_seconds': target, 'passes': p95 <= target}
artifacts += [Path(__file__).resolve(), base / 'phase22-save-balance-20261028.py']
report = {'diagnostic_comparisons': comparisons, 'unchanged_30_run_qualification': qualification,
    'T172_complete': False, 'T173_prerequisite_satisfied': False,
    'artifact_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts},
    'scope': 'Evidence arithmetic and unchanged production/harness identity; not new runtime tests or release approval'}
print(json.dumps(report, indent=2))
