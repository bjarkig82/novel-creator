"""Diagnostic only: compare complete saves with buffered Git history output."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import repository, git
from tests.performance import benchmark_records as benchmark

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path)
parser.add_argument('--buffered', action='store_true')
args = parser.parse_args()

if args.root:
    history = storage.read_history(args.root)
    bundle = records.new_exchange(history[0]['novel_id'], previous=history[-1],
        expected_head=storage.head(args.root), messages=[
            {'message_id': benchmark.uid(), 'role': 'user', 'text': 'Continue the benchmark.'},
            {'message_id': benchmark.uid(), 'role': 'assistant', 'text': 'Benchmark continuation.'}])
    bundle['payload_digest'] = records.digest(bundle)
    original = storage.git
    counts = {'history_requests': 0, 'hash_files': 0}
    def buffered_git(root, *command, **kwargs):
        if command[:2] == ('cat-file', '--batch') and kwargs.get('check') is False:
            counts['history_requests'] += 1
            if args.buffered:
                command = (*command, '--buffer')
        if command[0] == 'hash-object' and '--stdin-paths' in command:
            assert kwargs['env'] == {'GIT_WORK_TREE': str(root)}
            counts['hash_files'] += kwargs['input'].count(b'\n')
        return original(root, *command, **kwargs)
    with patch.object(storage, 'git', buffered_git):
        start = time.perf_counter()
        result = storage.save(args.root, bundle)
        elapsed = time.perf_counter() - start
    assert result['ok'] and not result['data']['cleanup_required'], result
    assert counts['history_requests'] == 4, counts
    assert counts['hash_files'] == 2 * (len(history) + 1), counts
    print(json.dumps({'buffered': args.buffered, 'seconds': elapsed,
        'sequence': result['checkpoint']['sequence'], **counts}), flush=True)
else:
    source = hashlib.sha256(Path(storage.__file__).read_bytes()).hexdigest()
    with benchmark.benchmark_key(True), repository(prefix='novel buffered history-') as root:
        novel_id = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, fixture = benchmark.generate(novel_id)
        for bundle in history:
            path = root / storage.bundle_path(bundle)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(benchmark.serialized(bundle))
        git(root, 'add', 'story/exchanges')
        git(root, 'commit', '-m', 'Disposable buffered-history fixture')
        del history, bundle
        read(root)
        fixture['fully_validated'] = True
        print(json.dumps({'fixture': fixture, 'storage_sha256': source,
            'method': 'ABBA/ABBA complete saves in fresh workers; ordinary unpacked fixture; diagnostic only'}), flush=True)
        samples = {False: [], True: []}
        for buffered in [False, True, True, False] * 2:
            command = [sys.executable, '-B', __file__, '--root', str(root)]
            if buffered:
                command.append('--buffered')
            result = subprocess.run(command, capture_output=True, text=True,
                encoding='utf-8', timeout=60)
            if result.returncode:
                raise RuntimeError(result.stderr[-3000:])
            row = json.loads(result.stdout)
            samples[buffered].append(row['seconds'])
            print(json.dumps(row), flush=True)
        assert source == hashlib.sha256(Path(storage.__file__).read_bytes()).hexdigest()
        print(json.dumps({'medians': {str(k): statistics.median(v) for k, v in samples.items()},
            'storage_unchanged': True}), flush=True)
