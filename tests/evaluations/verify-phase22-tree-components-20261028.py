"""Recompute tree-component diagnostics without treating probes as save stages."""
import hashlib
import json
from pathlib import Path
import statistics

base = Path(__file__).resolve().parent
root = base.parent.parent
raw = base / 'windows-phase22-tree-components-20261028.jsonl'
rows = [json.loads(line) for line in raw.read_text(encoding='utf-8-sig').splitlines()]
header, samples, footer = rows[0], rows[1:-1], rows[-1]
assert header['fixture'] == dict(sessions=100, exchanges=5000, active_assertions=10000,
    json_bytes=26215716, synthetic=True, fully_validated=True)
assert header['packing'] == 'none explicitly requested'
assert len(samples) == footer['completed_actual_saves'] == 4 and footer['source_unchanged']
for path, digest in header['source'].items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
traces = []
for number, sample in enumerate(samples, 1):
    sequence = 5000 + number
    assert sample['sequence'] == sequence and sample['guards'] == 2
    assert sample['hashed_files'] == sample['batch_objects_during_save'] == 2 * sequence
    assert sample['lookup_probe']['objects'] == sequence + 2
    assert sample['confirmed_head_and_live_index_unchanged_by_probes']
    assert sample['serialization_probe']['trees'] == 4
    assert len(sample['serialization_probe']['hash_and_zlib1_seconds']) == 4
    assert len(sample['scratch_durability_probe']['fsync_seconds']) == 4
    assert len(sample['lookup_probe']['python_loose_access_seconds']) == 4
    assert len(sample['same_index_existing_tree_replays']) == 2
    for item, expected_flushes in [(sample['fresh'], 3), *[(r, 0) for r in sample['same_index_existing_tree_replays']]]:
        trace = base / item['trace']
        traces.append(trace)
        parts = [line.split('|') for line in trace.read_text(encoding='utf-8').splitlines()]
        updates = [float(p[6]) for p in parts if len(p) >= 9 and p[3].strip() == 'region_leave'
                   and p[7].strip() == 'cache_tree' and p[8].strip() == 'label:update']
        flushes = [int(p[8].split('value:')[1]) for p in parts if len(p) >= 9
                   and p[3].strip() == 'counter' and 'name:hardware-flush value:' in p[8]]
        assert updates == [item['cache_tree_update_seconds']]
        assert sum(flushes) == item['hardware_flushes'] == expected_flushes
        assert item['seconds'] > item['cache_tree_update_seconds'] > 0
def spread(values):
    values = list(values)
    return {'samples': values, 'median': statistics.median(values), 'minimum': min(values), 'maximum': max(values)}
report = {
    'fresh_cache_tree_update_seconds': spread(s['fresh']['cache_tree_update_seconds'] for s in samples),
    'existing_cache_tree_update_seconds': spread(r['cache_tree_update_seconds'] for s in samples
                                                for r in s['same_index_existing_tree_replays']),
    'native_batch_check_wall_seconds': spread(s['lookup_probe']['native_batch_check_wall_seconds'] for s in samples),
    'python_loose_access_seconds': spread(v for s in samples for v in s['lookup_probe']['python_loose_access_seconds']),
    'verified_tree_hash_and_zlib1_seconds': spread(v for s in samples for v in s['serialization_probe']['hash_and_zlib1_seconds']),
    'scratch_fsync_seconds': spread(v for s in samples for v in s['scratch_durability_probe']['fsync_seconds']),
    'four_actual_saves_completed': True, 'source_unchanged': True,
    'scope': 'Actual fresh/existing native tree-region timings plus independent component probes. '
             'Do not add/subtract probe times to claim an exact decomposition, a speedup or p95 qualification.',
}
artifacts = [raw, Path(__file__), base / 'phase22-tree-components-20261028.py',
             base / 'windows-phase22-components-load-20261028.json', *traces]
report['artifact_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts}
print(json.dumps(report, indent=2))
