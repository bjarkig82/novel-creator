"""Verify final local support checks and pin their actual source/archive hashes."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
base = root / 'tests/evaluations'
expected = {
    'src/novel_creator/host_input.py': '01b1922cb27e50ce884c477f2aed158f066991eed0d63e394e15bdc19b3afb67',
    'src/novel_creator/validation.py': 'cbbae36120accdebc4e499f4331b212ccf806fc0e7b020e9349c31878b3a9aee',
    'src/novel_creator/cli.py': 'fda87c4155b0ffb94a995e384c2671db771306e569cf12ec6e2dc5ab1a87b0e9',
}
for path, digest in expected.items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest, path
results = {}
for platform, skips in [('windows', 2), ('linux', 3)]:
    raw = (base / f'{platform}-delegated-provenance-full-20261023.txt').read_text(encoding='utf-8-sig')
    match = re.search(r'Ran (\d+) tests in ([0-9.]+)s\s+OK \(skipped=(\d+)\)\s*$', raw)
    assert match and int(match[1]) == 165 and int(match[3]) == skips, platform
    wheel = json.loads((base / f'{platform}-delegated-provenance-wheel-20261023.json').read_bytes())
    assert wheel['ok'] and wheel['verified_source_files'] == 26
    archive = root / 'dist/delegated-provenance-20261023' / wheel['wheel']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == wheel['wheel_sha256']
    results[platform] = {'tests': 165, 'passed': 165 - skips, 'skipped': skips,
                         'seconds': float(match[2]), 'wheel_sha256': wheel['wheel_sha256']}
paths = set(expected)
paths.update(p.relative_to(root).as_posix() for p in (root / 'src').rglob('*')
             if p.is_file() and '__pycache__' not in p.parts)
paths.update(p.relative_to(root).as_posix() for p in base.glob('*delegated*20261023*')
             if p.is_file() and p.name != 'delegated-input-support-manifest-20261023.json')
manifest = {'task': 'T162', 'source_sha256': expected, 'results': results,
            'native_input_requirement_retained': True, 'novice_requirement_retained': True,
            'host_cases_reported_separately': True,
            'performance_remeasured': (base / 'windows-delegated-provenance-default-30-20261023.json').exists(),
            'performance_report': 'windows-delegated-provenance-performance-20261023.md',
            'files': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(paths)}}
(base / 'delegated-input-support-manifest-20261023.json').write_text(
    json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'ok': True, 'results': results}, indent=2))
