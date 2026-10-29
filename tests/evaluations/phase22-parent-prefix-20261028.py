"""Unretained lexical-prefix prototype, preserving per-guard metadata checks."""
import argparse
from contextlib import ExitStack
import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time
import types
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import git, repository
from tests.performance import benchmark_records as benchmark


def prototype():
    source = Path(storage.__file__).read_text(encoding='utf-8')
    old = '    current = os.fspath(root)\n    for index, part in enumerate(parts):'
    new = '''    current = os.fspath(root)
    if bundle and _directories is not None:
        story = current + os.sep + 'story'
        parent_directory = story + os.sep + 'exchanges'
        if story in _directories and parent_directory in _directories:
            current = parent_directory
            parts = parts[2:]
    for index, part in enumerate(parts):'''
    assert source.count(old) == 1
    candidate = types.ModuleType('novel_creator.parent_prefix_diagnostic')
    candidate.__package__ = 'novel_creator'
    exec(compile(source.replace(old, new), '<unretained-parent-prefix>', 'exec'), candidate.__dict__)
    # Use exactly the same fresh metadata implementations as the runtime.
    candidate._path_mode = storage._path_mode
    candidate._bundle_leaf_mode = storage._bundle_leaf_mode
    return candidate._checked_path


def worker(root, enabled):
    checked = prototype() if enabled else storage._checked_path
    original_git, original_guard = storage.git, storage.check_managed
    guards, hashes, batches, leaf_queries = [], [], [], []
    candidate_globals = checked.__globals__
    original_leaf = storage._bundle_leaf_mode
    def counted_leaf(path):
        leaf_queries.append(path)
        return original_leaf(path)
    def counted_git(root, *args, **kwargs):
        if args[0] == 'hash-object' and '--stdin-paths' in args:
            assert kwargs['env'] == {'GIT_WORK_TREE': str(root)}
            hashes.append(kwargs['input'].count(b'\n'))
        if args[0] == 'cat-file':
            batches.append(kwargs['input'].count(b'\n'))
        return original_git(root, *args, **kwargs)
    def counted_guard(*args, **kwargs):
        result = original_guard(*args, **kwargs)
        guards.append(len(result))
        return result
    with ExitStack() as stack:
        stack.enter_context(patch.object(storage, '_checked_path', checked))
        stack.enter_context(patch.dict(candidate_globals, {'_bundle_leaf_mode': counted_leaf}))
        stack.enter_context(patch.object(storage, 'git', counted_git))
        stack.enter_context(patch.object(storage, 'check_managed', counted_guard))
        result = benchmark.worker(root, 'save')
    sequence = result['observed_count']
    assert len(guards) == 2 and sum(hashes) == sum(batches) == 2 * sequence
    assert len(leaf_queries) == 2 * (sequence - 1)
    result.update(candidate=enabled, guards=len(guards), hashed_files=sum(hashes),
                  batch_objects=sum(batches), fresh_bundle_leaf_queries=len(leaf_queries))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--novel', type=Path)
    parser.add_argument('--candidate', action='store_true')
    args = parser.parse_args()
    if args.novel:
        print(json.dumps(worker(args.novel, args.candidate)))
        return
    source = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (
        'src/novel_creator/storage.py', 'src/novel_creator/context.py',
        'src/novel_creator/validation.py', 'tests/performance/benchmark_records.py')}
    with benchmark.benchmark_key(True), repository(prefix='novel parent prefix ') as root:
        novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, fixture = benchmark.generate(novel)
        for exchange in history:
            path = root / storage.bundle_path(exchange)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(benchmark.serialized(exchange))
        git(root, 'add', '--', 'story/exchanges')
        git(root, 'commit', '-m', 'Disposable lexical prefix comparison')
        del history, exchange
        read(root)
        fixture['fully_validated'] = True
        print(json.dumps({'fixture': fixture, 'source': source, 'git': shutil.which('git'),
            'python': sys.version, 'temp': str(root.parent), 'packing': 'none explicitly requested',
            'method': 'Unretained source copy changes lexical assembly only after both parents are in '
                      'the existing per-guard checked-directory set; fresh-worker ABBA/ABBA; not p95'}), flush=True)
        samples = []
        for enabled in (False, True, True, False, False, True, True, False):
            result = subprocess.run([sys.executable, '-B', __file__, '--novel', str(root),
                *(['--candidate'] if enabled else [])], capture_output=True, text=True,
                encoding='utf-8', timeout=30)
            if result.returncode:
                print(json.dumps({'failure': result.returncode, 'stderr': result.stderr}), flush=True)
                raise RuntimeError('Diagnostic worker failed')
            observed = json.loads(result.stdout)
            samples.append(observed)
            print(json.dumps(observed), flush=True)
        assert source == {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in source}
        print(json.dumps({'medians': {str(enabled): statistics.median(s['seconds'] for s in samples
            if s['candidate'] == enabled) for enabled in (False, True)}, 'source_unchanged': True}), flush=True)


if __name__ == '__main__':
    main()
