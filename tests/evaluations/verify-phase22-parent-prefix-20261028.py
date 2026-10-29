"""Check the unretained lexical-prefix comparison and safeguard counts."""
import hashlib
import json
from pathlib import Path
import statistics

base = Path(__file__).resolve().parent
root = base.parent.parent
path = base / 'windows-phase22-parent-prefix-20261028.jsonl'
rows = [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines()]
header, samples, footer = rows[0], rows[1:-1], rows[-1]
assert header['fixture'] == dict(sessions=100, exchanges=5000, active_assertions=10000,
    json_bytes=26215716, synthetic=True, fully_validated=True)
assert header['packing'] == 'none explicitly requested'
assert len(samples) == 8 and footer['source_unchanged']
for file, digest in header['source'].items():
    assert hashlib.sha256((root / file).read_bytes()).hexdigest() == digest
for number, (sample, candidate) in enumerate(zip(samples, (False, True, True, False) * 2), 1):
    assert sample['candidate'] == candidate and sample['observed_count'] == 5000 + number
    assert sample['guards'] == 2
    assert sample['hashed_files'] == sample['batch_objects'] == 2 * sample['observed_count']
    assert sample['fresh_bundle_leaf_queries'] == 2 * (sample['observed_count'] - 1)
    assert sample['seconds'] > 0
medians = {str(enabled): statistics.median(s['seconds'] for s in samples if s['candidate'] == enabled)
           for enabled in (False, True)}
assert medians == footer['medians']
report = {'medians': medians,
    'ranges': {str(enabled): [min(s['seconds'] for s in samples if s['candidate'] == enabled),
                             max(s['seconds'] for s in samples if s['candidate'] == enabled)]
               for enabled in (False, True)},
    'eight_full_scale_saves_verified': True, 'source_unchanged': True,
    'scope': 'Matched diagnostic with identical guard/hash/leaf counts; not a qualification p95 or sufficient alone for production adoption',
    'artifact_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (
        path, Path(__file__), base / 'phase22-parent-prefix-20261028.py')}}
print(json.dumps(report, indent=2))
