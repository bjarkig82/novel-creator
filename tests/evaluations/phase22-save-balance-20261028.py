"""Source-free, fresh-worker full-scale save concurrency experiment.

No production or benchmark edits. Every policy retains complete guards and reads.
"""
import argparse
from contextlib import ExitStack
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import git, repository
from tests.performance import benchmark_records as benchmark


def fingerprint():
    return {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in (
        'src/novel_creator/storage.py', 'src/novel_creator/context.py',
        'src/novel_creator/validation.py', 'tests/performance/benchmark_records.py')}


class DeferredPreparation:
    """Diagnostic history-first schedule; complete queued work before lock exit."""
    def __enter__(self):
        self.work = None
        return self

    def submit(self, function, *args, **kwargs):
        self.work = (function, args, kwargs)
        return self

    def result(self):
        if self.work is not None:
            function, args, kwargs = self.work
            self.work = None
            try:
                self.value = function(*args, **kwargs)
                self.error = None
            except BaseException as error:
                self.error = error
        if self.error is not None:
            raise self.error
        return self.value

    def __exit__(self, *exception):
        if self.work is not None:
            try:
                self.result()
            except BaseException:
                pass  # Like executor shutdown: join, don't raise an unread future.


def worker(root, history_workers, initial_workers, defer_guard=False):
    original_git = storage.git
    original_guard = storage.check_managed
    guards, hashes, batches = [], [], []

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
        if defer_guard:
            original_executor = storage.ThreadPoolExecutor
            def executor(*args, **kwargs):
                return (DeferredPreparation() if kwargs.get('max_workers') == 1
                        else original_executor(*args, **kwargs))
            stack.enter_context(patch.object(storage, 'ThreadPoolExecutor', executor))
        stack.enter_context(patch.object(storage, '_SAVE_HISTORY_WORKERS', history_workers))
        stack.enter_context(patch.object(storage, '_INITIAL_HASH_WORKERS', initial_workers))
        stack.enter_context(patch.object(storage, 'git', counted_git))
        stack.enter_context(patch.object(storage, 'check_managed', counted_guard))
        observed = benchmark.worker(root, 'save')
    prior = observed['observed_count'] - 1
    assert len(guards) == 2
    assert sum(hashes) == 2 * (prior + 1), hashes
    # Payload preparation reads all history too; candidate verifies two objects.
    assert sum(batches) == 2 * prior + 2, batches
    observed.update(history_workers=history_workers, initial_hash_workers=initial_workers,
                    defer_guard=defer_guard, guards=len(guards), hashed_files=sum(hashes), batch_objects=sum(batches))
    return observed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--novel', type=Path)
    parser.add_argument('--history-workers', type=int)
    parser.add_argument('--initial-workers', type=int)
    parser.add_argument('--defer-guard', action='store_true')
    parser.add_argument('--schedule-diagnostic', action='store_true')
    args = parser.parse_args()
    if args.novel:
        print(json.dumps(worker(args.novel, args.history_workers, args.initial_workers, args.defer_guard)))
        return
    frozen = fingerprint()
    with benchmark.benchmark_key(True), repository(prefix='novel balance ') as root:
        novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, fixture = benchmark.generate(novel)
        for exchange in history:
            path = root / storage.bundle_path(exchange)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(benchmark.serialized(exchange))
        git(root, 'add', '--', 'story/exchanges')
        git(root, 'commit', '-m', 'Disposable full-scale concurrency fixture')
        del history, exchange
        read(root)
        fixture['fully_validated'] = True
        policies = [(4, 2, False), (1, 2, False), (4, 1, False)]
        order = (0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0)
        if args.schedule_diagnostic:
            policies = [(4, 2, False), (4, 2, True)]
            order = (0, 1, 1, 0, 0, 1, 1, 0)
        print(json.dumps({'fixture': fixture, 'source': frozen,
            'git': benchmark.shutil.which('git'), 'python': sys.version,
            'temp': str(root.parent), 'packing': 'none explicitly requested',
            'order': order, 'policies': policies,
            'method': 'Balanced fresh-worker saves; default final guard; diagnostic not p95'}), flush=True)
        samples = {str(policy): [] for policy in policies}
        for index in order:
            h, g, deferred = policies[index]
            result = subprocess.run([sys.executable, '-B', __file__, '--novel', str(root),
                '--history-workers', str(h), '--initial-workers', str(g),
                *(['--defer-guard'] if deferred else [])],
                capture_output=True, text=True, encoding='utf-8', timeout=30)
            if result.returncode:
                print(json.dumps({'failure': result.returncode, 'stderr': result.stderr}), flush=True)
                raise RuntimeError('Diagnostic worker failed')
            data = json.loads(result.stdout)
            samples[str((h, g, deferred))].append(data['seconds'])
            print(json.dumps(data), flush=True)
        assert frozen == fingerprint()
        print(json.dumps({'medians': {key: statistics.median(value) for key, value in samples.items()},
                          'source_unchanged': True}), flush=True)


if __name__ == '__main__':
    main()
