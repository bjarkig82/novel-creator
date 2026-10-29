"""Verify completed integrity evidence and write a source-pinned manifest."""
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
base = root / 'tests/evaluations'
expected = {
    'src/novel_creator/storage.py': '40c7c1ef61af98e9c1e04292d2befc963bd48bbd45196ce8cbf91576f3ee771b',
    'tests/integration/test_candidate.py': 'cfceb90e269f8a9c9758372e9c42c738a3ec9ad2fee472f0aa84b7adefc02e8d',
    'tests/integration/test_cache.py': 'b7d58c6e277d53a6e9c467dee27c12aa248cd768f24e6417ccf0f28ee135a218',
}
for relative, fingerprint in expected.items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == fingerprint, relative
results = {}
for platform, skips in [('windows', 2), ('linux', 3)]:
    log = base / f'{platform}-git-blob-integrity-full-tests-20261023.txt'
    raw = log.read_text(encoding='utf-8-sig')
    match = re.search(r'Ran (\d+) tests in ([0-9.]+)s\s+OK \(skipped=(\d+)\)\s*$', raw)
    assert match and int(match[1]) == 158 and int(match[3]) == skips, log
    wheel = json.loads((base / f'{platform}-git-blob-integrity-wheel-20261023.json').read_text(encoding='utf-8-sig'))
    assert wheel['ok'] and wheel['verified_source_files'] == 25
    assert wheel['semantic_host_or_human_evidence'] is False
    fingerprint = hashlib.sha256((root / 'dist/git-blob-integrity-20261023' / wheel['wheel']).read_bytes()).hexdigest()
    assert wheel['wheel_sha256'] == fingerprint
    results[platform] = {'tests': 158, 'passed': 158 - skips, 'skipped': skips,
                         'seconds': float(match[2]), 'wheel_sha256': fingerprint,
                         'wheel_verified_source_files': 25}
paths = set(expected)
paths.update(p.relative_to(root).as_posix() for p in (root / 'src').rglob('*')
             if p.is_file() and '__pycache__' not in p.parts)
paths.update(p.relative_to(root).as_posix() for p in base.glob('*blob*20261023*')
             if p.is_file() and p.suffix != '.json')
paths.update(f'tests/evaluations/{p}-git-blob-integrity-wheel-20261023.json'
             for p in ('windows', 'linux'))
manifest = {'task': 'T161', 'results': results, 'source_sha256': expected,
            'semantic_host_or_human_evidence': False,
            'performance_remeasured': False,
            'remaining_tasks': [f'T{n}' for n in range(151, 159)],
            'files': {p: hashlib.sha256((root / p).read_bytes()).hexdigest()
                      for p in sorted(paths)}}
output = base / 'git-blob-integrity-manifest-20261023.json'
output.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'ok': True, 'results': results}, indent=2))
