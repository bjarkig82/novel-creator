"""Check whether the tree command actually activates Git for Windows fscache."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
from novel_creator import storage
from tests.helpers import repository

base = Path(__file__).resolve().parent
results = []
with repository() as root:
    for command in ('write-tree', 'status'):
        trace = base / f'windows-phase22-fscache-activation-{command}-20261028.txt'
        assert not trace.exists(), 'Do not overwrite prior evidence'
        observed = storage.git(root, '-c', 'core.fscache=true', command,
                               env={'GIT_TRACE_FSCACHE': str(trace)}, check=False)
        assert observed.returncode == 0
        content = trace.read_text(encoding='utf-8') if trace.exists() else ''
        results.append({'command': command, 'returncode': observed.returncode,
                        'trace_created': trace.exists(), 'trace': content,
                        'cache_activation_observed': 'fscache: enable' in content})
assert not results[0]['cache_activation_observed']
assert results[1]['cache_activation_observed'], 'Positive tracing control must activate the cache'
print(json.dumps(results, indent=2))
