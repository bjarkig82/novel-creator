"""Read-only verification of the stderr-pipe diagnostic and qualification arithmetic."""
import hashlib
import json
import math
from pathlib import Path
import statistics

base = Path('tests/evaluations')


def rows(name):
    return [json.loads(line) for line in (base / name).read_text(encoding='utf-8-sig').splitlines()]


outputs = {}
for name, kind, repetitions in (
    ('windows-phase23-stderr-component-20261028.jsonl', 'component', 4),
    ('windows-phase23-stderr-save-normal-20261028.jsonl', 'save', 2),
):
    data = rows(name)
    header = data[0]
    assert header['kind'] == 'header'
    for file, digest in header['source'].items():
        assert hashlib.sha256(Path(file).read_bytes()).hexdigest() == digest, file
    assert data[-1] == dict(kind='complete', source_unchanged=True)
    checks = next(r['checks'] for r in data if r['kind'] == 'correctness')
    assert {r['format'] for r in checks} == {'sha1', 'sha256'}
    assert all(all(r[k] for k in ('stdout_equal', 'binary_stdin_equal',
        'checked_failure_sanitized', 'unchecked_stderr_retained')) for r in checks)
    samples = [r for r in data if r['kind'] == kind]
    assert [r['candidate'] for r in samples] == [False, True, True, False] * repetitions
    if kind == 'component':
        assert all(r['commands'] == 8 and r['reader_threads'] == (0 if r['candidate'] else 16) for r in samples)
    else:
        fixture = next(r for r in data if r['kind'] == 'fixture')
        for key, value in dict(sessions=100, exchanges=5000, active_assertions=10000,
            json_bytes=26215716, fully_validated=True, packing='none explicitly requested').items():
            assert fixture[key] == value
        assert [r['observed_count'] for r in samples] == list(range(5001, 5009))
        assert all(r['guards'] == 2 and r['hashed_files'] == r['batch_objects'] == 2*r['observed_count'] for r in samples)
    outputs[kind] = {}
    for selected in (False, True):
        chosen = [r for r in samples if r['candidate'] == selected]
        times = [r['seconds'] for r in chosen]
        outputs[kind][str(selected)] = dict(samples=len(chosen), median_seconds=statistics.median(times),
            range_seconds=[min(times), max(times)], cpu_percent_range=[min(r['cpu_percent'] for r in chosen),
            max(r['cpu_percent'] for r in chosen)])

# The original sandbox failure and mistaken reader-count assumption remain visible.
assert 'WinError 5' in (base/'windows-phase23-stderr-save-stderr-20261028.txt').read_text()
assert 'AssertionError' in (base/'windows-phase23-stderr-component-assumption-stderr-20261028.txt').read_text()
for name in ('windows-phase23-stderr-component-stderr-20261028.txt',
             'windows-phase23-stderr-save-normal-stderr-20261028.txt'):
    assert (base/name).read_bytes() == b''
retained = json.loads((base/'windows-phase22-ordinary-30-20261028.json').read_bytes())
for kind in ('read', 'save'):
    result = retained[kind]
    assert len(result['samples_seconds']) == result['completed_runs'] == 30
    assert result['failure'] is None
    assert sorted(result['samples_seconds'])[math.ceil(30*.95)-1] == result['p95_seconds']
outputs['retained_qualification'] = {k: retained[k]['p95_seconds'] for k in ('read', 'save')}
artifacts = [Path(__file__), base/'phase23-stderr-pipe-20261028.py',
    *base.glob('windows-phase23-stderr-*.jsonl'), *base.glob('windows-phase23-stderr-*.txt')]
print(json.dumps(dict(ok=True, observations=outputs, qualification_rerun=False,
    artifacts={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)}), indent=2))
