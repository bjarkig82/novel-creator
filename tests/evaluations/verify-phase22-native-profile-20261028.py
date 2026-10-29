"""Verify source-build identity, guarded runs and native timing arithmetic."""
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

root = Path.cwd()
base = root / 'tests/evaluations'
native = root / '.tools/t172-git-native-20261028'
raw = base / 'windows-phase22-native-profile-20261028.jsonl'
rows = [json.loads(line) for line in raw.read_text(encoding='utf-8-sig').splitlines()]
header = rows[0]
assert header['kind'] == 'header'
assert header['upstream_commit'] == 'f8165afd89b0c190677a093f20894f5fce12f97a'
assert subprocess.check_output(['git', '-C', str(native / 'source'), 'rev-parse', 'HEAD'], text=True).strip() == header['upstream_commit']
for file, digest in header['source'].items():
    assert hashlib.sha256((root / file).read_bytes()).hexdigest() == digest
for info in header['binaries'].values():
    assert hashlib.sha256(Path(info['path']).read_bytes()).hexdigest() == info['sha256']
assert header['binaries']['profile_on']['sha256'] == header['binaries']['profile_off']['sha256']
assert header['binaries']['baseline']['sha256'] != header['binaries']['profile_on']['sha256']
fixture = next(row for row in rows if row['kind'] == 'fixture')
assert all(fixture[k] == v for k, v in dict(sessions=100, exchanges=5000, active_assertions=10000,
    json_bytes=26215716, synthetic=True, fully_validated=True, packing='none explicitly requested').items())
checks = next(row['checks'] for row in rows if row['kind'] == 'correctness')
assert len(checks) == 8
assert {(c['format'], c['variant']) for c in checks} == {
    (f, v) for f in ('sha1', 'sha256') for v in header['binaries']}
for format in ('sha1', 'sha256'):
    selected = [c for c in checks if c['format'] == format]
    assert len({c['matching_tree_oid'] for c in selected}) == 1
    assert all(c['missing_object_rejected'] and c['missing_object_returncode'] == 128 for c in selected)
load = [row for row in rows if row['kind'] == 'load']
assert len(load) >= 3 and load[-1]['consecutive_quiet'] == 3
assert all(row['cpu_percent'] <= 40 and row['available_physical_bytes'] >= 2 * 1024**3 for row in load[-3:])
samples = [row for row in rows if row['kind'] == 'sample']
order = ('installed', 'baseline', 'profile_off', 'profile_on', 'profile_on', 'profile_off', 'baseline', 'installed') * 2
assert len(samples) == 16
profiles = []
for number, (sample, variant) in enumerate(zip(samples, order), 5001):
    assert sample['sequence'] == number and sample['variant'] == variant
    assert sample['guards'] == 2 and sample['hashed_files'] == sample['batch_objects'] == 2 * number
    assert sample['save_seconds'] > sample['tree']['wall_seconds'] > 0
    profile = sample['tree']['profile']
    assert (profile is not None) == (variant == 'profile_on')
    if profile:
        assert profile['result'] == number + 2
        assert 0 < profile['total_ns'] < sample['tree']['wall_seconds'] * 10**9
        metrics = profile['metrics']
        assert metrics['lookup']['calls'] == number + 5
        assert metrics['serialize']['calls'] == number + 4
        assert metrics['object_write']['calls'] == metrics['fsync']['calls'] == 3
        assert metrics['deflate']['calls'] > 0
        assert all(0 <= m['exclusive_ns'] <= m['inclusive_ns'] for m in metrics.values())
        assert sum(m['exclusive_ns'] for m in metrics.values()) <= profile['total_ns']
        assert metrics['object_write']['inclusive_ns'] == metrics['object_write']['exclusive_ns'] + metrics['deflate']['inclusive_ns'] + metrics['fsync']['inclusive_ns']
        profiles.append(sample)
assert rows[-1] == {'kind': 'summary', 'completed_saves': 16, 'source_and_binaries_unchanged': True}
manifest_path = base / 'windows-phase22-native-git-instrumentation-20261028.json'
manifest = json.loads(manifest_path.read_text())
for file, digest in manifest['before_sha256'].items():
    original = subprocess.check_output(['git', '-C', str(native / 'source'), 'show', header['upstream_commit'] + ':' + file])
    assert hashlib.sha256(original).hexdigest() == digest
for file, digest in manifest['after_sha256'].items():
    assert hashlib.sha256((native / 'source' / file).read_bytes()).hexdigest() == digest
assert hashlib.sha256((base / 'windows-phase22-native-git-header-20261028.txt').read_bytes()).hexdigest() == manifest['after_sha256']['t172-profile.h']
portable = json.loads((base / 'windows-phase22-native-git-portable-tools-20261028.json').read_text(encoding='utf-8-sig'))
assert portable['CMakeVersion'] == '4.4.4'
assert hashlib.sha256((native / 'cmake.zip').read_bytes()).hexdigest() == portable['SHA256']
assert hashlib.sha256((native / 'zlib.zip').read_bytes()).hexdigest() == '50b24b47bf19e1f35d2a21ff36d2a366638cdf958219a66f30ce0861201760e6'
def stats(values):
    values = list(values)
    return {'median': statistics.median(values), 'minimum': min(values), 'maximum': max(values), 'samples': values}
report = {
    'completed_guarded_full_scale_saves': 16,
    'sha1_sha256_tree_and_missing_object_checks': 8,
    'source_and_installed_binary_unchanged': True,
    'native_profile_count': len(profiles),
    'initial_quiet_gate_passed': True,
    'quiet_native_profile_windows': sum(s['tree']['quiet_window'] and s['tree']['available_physical_bytes'] >= 2 * 1024**3 for s in profiles),
    'native_total_milliseconds': stats(s['tree']['profile']['total_ns'] / 10**6 for s in profiles),
    'native_exclusive_milliseconds': {name: stats(s['tree']['profile']['metrics'][name]['exclusive_ns'] / 10**6 for s in profiles)
                                      for name in ('lookup', 'serialize', 'object_write', 'deflate', 'fsync')},
    'variant_tree_wall_seconds': {v: stats(s['tree']['wall_seconds'] for s in samples if s['variant'] == v) for v in header['binaries']},
    'variant_save_seconds': {v: stats(s['save_seconds'] for s in samples if s['variant'] == v) for v in header['binaries']},
    'scope': 'Owner-thread MSVC/zlib1.3.1 native source-build diagnostics with explicit load/clock/compiler limits. '
             'No production optimization or installed-distribution p95/low-load claim.',
}
settled_path = base / 'windows-phase22-native-profile-settled-20261028.jsonl'
settled = [json.loads(line) for line in settled_path.read_text().splitlines()]
assert settled[0]['kind'] == 'header'
for file, digest in settled[0]['source'].items():
    assert hashlib.sha256((root / file).read_bytes()).hexdigest() == digest
if settled[-1]['kind'] == 'not_measured':
    assert not [r for r in settled if r['kind'] == 'sample']
    report['stricter_followup'] = {'status': 'not_measured', 'reason': settled[-1]['reason'],
        'load_samples': len([r for r in settled if r['kind'] == 'load'])}
elif settled[-1]['kind'] == 'summary':
    later = [r for r in settled if r['kind'] == 'sample']
    assert len(later) == 4 and settled[-1]['completed_saves'] == 4
    for sample in later:
        assert sample['variant'] == 'profile_on' and sample['guards'] == 2
        assert sample['hashed_files'] == sample['batch_objects'] == 2 * sample['sequence']
        assert sample['tree']['pre_tree_load'][-1]['consecutive_quiet'] == 3
    report['stricter_followup'] = {'status': 'completed', 'profile_count': len(later),
        'quiet_windows': sum(s['tree']['quiet_window'] for s in later)}
else:
    raise AssertionError('Follow-up has not completed successfully or reached a recorded quiet-gate stop')
artifacts = [raw, settled_path, manifest_path, Path(__file__),
    base / 'prepare-phase22-native-profile-20261028.py', base / 'phase22-native-profile-20261028.py',
    base / 'phase22-native-profile-settled-20261028.py', base / 'windows-phase22-native-git-instrumentation-20261028.patch',
    base / 'windows-phase22-native-git-baseline-build-20261028.txt',
    base / 'windows-phase22-native-git-baseline-build-v2-20261028.txt',
    base / 'windows-phase22-native-git-profile-build-20261028.txt']
artifacts += [base / 'windows-phase22-native-git-configure-source-20261028.txt',
              base / 'windows-phase22-native-git-rebuild-source-20261028.txt',
              base / 'windows-phase22-native-git-portable-tools-20261028.json',
              base / 'windows-phase22-native-git-header-20261028.txt']
report['artifact_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts}
print(json.dumps(report, indent=2))
