"""Verify write-tree diagnostic measurements, tracing and unchanged source."""
import hashlib
import json
from pathlib import Path
import statistics

base = Path(__file__).resolve().parent
root = base.parent.parent
raw = base / 'windows-phase22-write-tree-20261028.jsonl'
rows = [json.loads(line) for line in raw.read_text(encoding='utf-8-sig').splitlines()]
header, samples, summary = rows[0], rows[1:-1], rows[-1]
assert header['fixture'] == dict(sessions=100, exchanges=5000, active_assertions=10000,
    json_bytes=26215716, synthetic=True, fully_validated=True)
assert header['packing'] == 'none explicitly requested'
assert header['default_fscache'] == '' and header['default_fscache_query_returncode'] == 1
assert len(samples) == 8 and summary['source_unchanged']
for path, digest in header['source'].items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
assert len(header['missing_object_checks']) == 4
assert {(c['format'], c['fscache']) for c in header['missing_object_checks']} == {
    (f, enabled) for f in ('sha1', 'sha256') for enabled in (False, True)}
assert all(c['missing_object_rejected'] and c['returncode'] == 128 for c in header['missing_object_checks'])
traces = []
for number, (sample, enabled) in enumerate(zip(samples, (False, True, True, False) * 2), 1):
    assert sample['fscache'] == enabled and sample['observed_count'] == 5000 + number
    assert sample['guards'] == 2
    assert sample['hashed_files'] == sample['batch_objects'] == 2 * sample['observed_count']
    assert sample['seconds'] > sample['write_tree']['seconds'] > 0
    trace = base / sample['trace']
    lines = [line.split('|') for line in trace.read_text(encoding='utf-8-sig').splitlines()]
    def duration(category, label):
        matching = [parts for parts in lines if len(parts) >= 9 and parts[3].strip() == 'region_leave'
                    and parts[7].strip() == category and parts[8].strip() == label]
        assert len(matching) == 1, (category, label)
        return float(matching[0][6])
    updates = duration('cache_tree', 'label:update')
    assert any('name:hardware-flush value:3' in '|'.join(parts) for parts in lines)
    assert any(parts[3].strip() == 'exit' and 'code:0' in '|'.join(parts) for parts in lines if len(parts) >= 9)
    traces.append({'file': trace.name, 'fscache': enabled, 'cache_tree_update_seconds': updates,
                   'hardware_flushes': 3})
medians = {str(enabled): {
    'save': statistics.median(s['seconds'] for s in samples if s['fscache'] == enabled),
    'write_tree': statistics.median(s['write_tree']['seconds'] for s in samples if s['fscache'] == enabled)}
    for enabled in (False, True)}
assert medians == summary['medians']
activation_path = base / 'windows-phase22-fscache-activation-20261028.json'
activation = json.loads(activation_path.read_text(encoding='utf-8-sig'))
assert [item['command'] for item in activation] == ['write-tree', 'status']
assert [item['cache_activation_observed'] for item in activation] == [False, True]
artifacts = [raw, activation_path, Path(__file__), base / 'phase22-write-tree-20261028.py',
             base / 'phase22-tree-cache-activation-20261028.py',
             *(base / item['file'] for item in traces)]
report = {'medians': medians, 'trace_measurements': traces,
    'cache_tree_update_medians': {str(enabled): statistics.median(
        t['cache_tree_update_seconds'] for t in traces if t['fscache'] == enabled) for enabled in (False, True)},
    'missing_object_checks': header['missing_object_checks'],
    'cache_activation_observed': {item['command']: item['cache_activation_observed'] for item in activation},
    'production_source_unchanged': True, 'candidate_retained': False,
    'T172_complete': False, 'T173_prerequisite_satisfied': False,
    'artifact_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts},
    'scope': 'Full-scale diagnostics and arithmetic; traced comparisons are not a qualification p95 or a causal slowdown claim'}
print(json.dumps(report, indent=2))
