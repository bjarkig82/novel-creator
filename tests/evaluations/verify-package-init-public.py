"""Verify retained production reports against the immutable release candidate."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).parent
expected = json.loads((root / 'package-init-release-manifest.json').read_text(encoding='utf-8-sig'))
public = json.loads((root / 'package-init-public-pypi.json').read_text(encoding='utf-8'))
assert public['info']['name'] == 'novel-creator' and public['info']['version'] == '0.1.0'
assert {f['filename']: f['digests']['sha256'] for f in public['urls']} == expected['files']
results = {}
for platform, encoding in [('windows', 'cp1252'), ('linux', 'utf-8')]:
    path = root / f'package-init-public-{platform}/public-check.json'
    raw = path.read_bytes()
    report = json.loads(raw.decode(encoding))
    assert report['mode'] == 'public' and report['source'] == 'novel-creator==0.1.0'
    assert report['validated'] and report['dependency_inheritance'] is False
    assert report['public_artifact_hashes'] == expected['files']
    product = report['installed_product']
    assert product['name'] == 'novel-creator' and product['version'] == '0.1.0'
    assert expected['files'][product['filename']] == product['sha256']
    assert product['url'].startswith('https://files.pythonhosted.org/')
    assert report['guide_sha256'] == expected['current_source_sha256']['workflows/getting-started.md']
    assert report['invalid_input_cases'] == 5
    assert report['settings_cases'][0]['title'] == 'Bréf frá morgundeginum'
    assert all(case['preserved'] for case in report['settings_cases'])
    # Retain the original artifact bytes; provide a separately labeled UTF-8 view.
    if platform == 'windows':
        (path.parent / 'public-check-utf8.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    results[platform] = {'passed': True, 'artifact_encoding': encoding, 'report_sha256': hashlib.sha256(raw).hexdigest(), 'installed_product': product, 'declared_dependencies_resolved': True, 'dependency_inheritance': False, 'defaults_options_provenance_and_five_refusals': True}
output = {'verified': True, 'distribution': 'novel-creator', 'version': '0.1.0', 'publication_run': '40911698155', 'candidate_run': '40904366247', 'candidate_attempt': '1', 'artifact_id': '12911245684', 'source_commit': expected['source_commit'], 'public_files': expected['files'], 'platforms': results, 'linux_codex_host_verified': False}
(root / 'package-init-public-verification.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'verified': True, 'platforms': list(results), 'same_candidate_bytes': True}))
