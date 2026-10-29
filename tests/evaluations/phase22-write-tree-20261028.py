"""Full-scale private-candidate write-tree cache diagnostic; no runtime edits."""
import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import git, repository
from tests.performance import benchmark_records as benchmark


def fingerprint():
    return {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (
        'src/novel_creator/storage.py', 'src/novel_creator/context.py',
        'src/novel_creator/validation.py', 'tests/performance/benchmark_records.py')}


def worker(root, enabled, trace):
    original_git, original_guard = storage.git, storage.check_managed
    trees, guards, hashes, batches = [], [], [], []
    def observed_git(root, *args, **kwargs):
        command = args[0]
        if command == 'hash-object' and '--stdin-paths' in args:
            assert kwargs['env'] == {'GIT_WORK_TREE': str(root)}
            hashes.append(kwargs['input'].count(b'\n'))
        if command == 'cat-file':
            batches.append(kwargs['input'].count(b'\n'))
        if command == 'write-tree':
            assert args == ('write-tree',)  # Retain normal object-existence checks.
            assert set(kwargs['env']) == {'GIT_INDEX_FILE'}
            assert Path(kwargs['env']['GIT_INDEX_FILE']).parent.name.startswith('candidate-')
            kwargs['env'] = {**kwargs['env'], 'GIT_TRACE2_PERF': str(trace.resolve())}
            if enabled:
                args = ('-c', 'core.fscache=true', *args)
            start = time.perf_counter()
            result = original_git(root, *args, **kwargs)
            trees.append({'seconds': time.perf_counter() - start, 'oid': result.decode().strip()})
            return result
        return original_git(root, *args, **kwargs)
    def observed_guard(*args, **kwargs):
        result = original_guard(*args, **kwargs)
        guards.append(len(result))
        return result
    with ExitStack() as stack:
        stack.enter_context(patch.object(storage, 'git', observed_git))
        stack.enter_context(patch.object(storage, 'check_managed', observed_guard))
        result = benchmark.worker(root, 'save')
    sequence = result['observed_count']
    assert len(trees) == 1 and len(guards) == 2
    assert sum(hashes) == sum(batches) == 2 * sequence
    result.update(fscache=enabled, write_tree=trees[0], guards=len(guards),
                  hashed_files=sum(hashes), batch_objects=sum(batches), trace=trace.name)
    return result


def missing_object_checks():
    results = []
    for format in ('sha1', 'sha256'):
        with repository(object_format=format) as root:
            index = root / '.novel-creator/local/missing-index'
            env = {'GIT_INDEX_FILE': str(index)}
            storage.git(root, 'read-tree', 'HEAD', env=env)
            oid = '1' * (40 if format == 'sha1' else 64)
            storage.git(root, 'update-index', '--add', '--cacheinfo', f'100644,{oid},missing', env=env)
            for enabled in (False, True):
                args = ('-c', 'core.fscache=true', 'write-tree') if enabled else ('write-tree',)
                observed = storage.git(root, *args, env=env, check=False)
                assert observed.returncode != 0
                results.append({'format': format, 'fscache': enabled,
                                'missing_object_rejected': True, 'returncode': observed.returncode})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--novel', type=Path)
    parser.add_argument('--fscache', action='store_true')
    parser.add_argument('--trace', type=Path)
    args = parser.parse_args()
    if args.novel:
        print(json.dumps(worker(args.novel, args.fscache, args.trace)))
        return
    frozen = fingerprint()
    checks = missing_object_checks()
    with benchmark.benchmark_key(True), repository(prefix='novel write-tree ') as root:
        novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, fixture = benchmark.generate(novel)
        for exchange in history:
            path = root / storage.bundle_path(exchange)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(benchmark.serialized(exchange))
        git(root, 'add', '--', 'story/exchanges')
        git(root, 'commit', '-m', 'Disposable tree construction fixture')
        del history, exchange
        read(root)
        fixture['fully_validated'] = True
        # The runtime intentionally excludes system Git config. Measure the
        # effective setting under that same environment, not the shell default.
        config = storage.git(root, 'config', '--get', 'core.fscache', check=False)
        print(json.dumps({'fixture': fixture, 'source': frozen, 'missing_object_checks': checks,
            'git': shutil.which('git'), 'python': sys.version, 'temp': str(root.parent),
            'packing': 'none explicitly requested', 'default_fscache': config.stdout.decode().strip(),
            'default_fscache_query_returncode': config.returncode,
            'method': 'ABBA/ABBA fresh workers; write-tree-only command-local fscache; tracing both variants; not p95'}), flush=True)
        samples = []
        for number, enabled in enumerate((False, True, True, False, False, True, True, False), 1):
            trace = Path(__file__).parent / f'windows-phase22-write-tree-trace-{number}-20261028.txt'
            assert not trace.exists(), 'Preserve previous evidence; choose a fresh run name'
            result = subprocess.run([sys.executable, '-B', __file__, '--novel', str(root),
                '--trace', str(trace), *(['--fscache'] if enabled else [])],
                capture_output=True, text=True, encoding='utf-8', timeout=30)
            if result.returncode:
                print(json.dumps({'failure': result.returncode, 'stderr': result.stderr}), flush=True)
                raise RuntimeError('Diagnostic worker failed')
            data = json.loads(result.stdout)
            samples.append(data)
            print(json.dumps(data), flush=True)
        assert frozen == fingerprint()
        print(json.dumps({'medians': {str(enabled): {
            'save': statistics.median(s['seconds'] for s in samples if s['fscache'] == enabled),
            'write_tree': statistics.median(s['write_tree']['seconds'] for s in samples if s['fscache'] == enabled)}
            for enabled in (False, True)}, 'source_unchanged': True}), flush=True)


if __name__ == '__main__':
    main()
