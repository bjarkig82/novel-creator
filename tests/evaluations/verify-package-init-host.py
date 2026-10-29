"""Bind the disposable host novel to the immutable candidate's installed resources."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import novel_creator
from novel_creator.install import bundle_files

root = Path(sys.argv[1])
wheel = Path(sys.argv[2])
assert hashlib.sha256(wheel.read_bytes()).hexdigest() == 'cc8645556f74190dee9ac7527c3e66c0bc71574913b5bbae5ddff7516b8817a8'
site = Path(novel_creator.__file__).parent.parent
with zipfile.ZipFile(wheel) as archive:
    product = [name for name in archive.namelist() if name.startswith('novel_creator/') and not name.endswith('/')]
    for name in product:
        assert (site / name).read_bytes() == archive.read(name), name
expected = bundle_files()
for name, raw in expected.items():
    assert (root / name).read_bytes() == raw, name
with zipfile.ZipFile(wheel) as archive:
    assert (root / 'AGENTS.md').read_bytes() == archive.read('novel_creator/codex/AGENTS.production.md').replace(b'\r\n', b'\n')
print(json.dumps({'verified': True, 'runtime': sys.executable, 'product_module': novel_creator.__file__, 'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(), 'installed_files': len(product), 'pinned_resources': len(expected), 'agents_exact': True}, indent=2))
