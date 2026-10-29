"""Separate native fresh/existing tree work and isolated component probes.

Every actual save retains all guards. Component probes never publish refs or
change the user index. Independent probe times are not additive save stages.
"""
from contextlib import ExitStack
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import statistics
import sys
import tempfile
import time
from unittest.mock import patch
import zlib

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import git, repository
from tests.performance import benchmark_records as benchmark


def trace_metrics(path):
    rows = [line.split('|') for line in path.read_text(encoding='utf-8').splitlines()]
    updates = [float(r[6]) for r in rows if len(r) >= 9 and r[3].strip() == 'region_leave'
               and r[7].strip() == 'cache_tree' and r[8].strip() == 'label:update']
    assert len(updates) == 1
    flushes = [int(r[8].split('value:')[1]) for r in rows if len(r) >= 9
               and r[3].strip() == 'counter' and 'name:hardware-flush value:' in r[8]]
    return {'cache_tree_update_seconds': updates[0], 'hardware_flushes': sum(flushes)}


def timed(function):
    start = time.perf_counter()
    result = function()
    return result, time.perf_counter() - start


def main():
    base = Path(__file__).resolve().parent
    source = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (
        'src/novel_creator/storage.py', 'src/novel_creator/context.py',
        'src/novel_creator/validation.py', 'tests/performance/benchmark_records.py')}
    with benchmark.benchmark_key(True), repository(prefix='novel tree components ') as root, \
            tempfile.TemporaryDirectory(prefix='novel tree probes ') as scratch:
        scratch = Path(scratch).resolve()
        novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, fixture = benchmark.generate(novel)
        for exchange in history:
            path = root / storage.bundle_path(exchange)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(benchmark.serialized(exchange))
        git(root, 'add', '--', 'story/exchanges')
        git(root, 'commit', '-m', 'Disposable tree component fixture')
        del history, exchange
        read(root)
        fixture['fully_validated'] = True
        print(json.dumps({'fixture': fixture, 'source': source, 'git': shutil.which('git'),
            'python': sys.version, 'temp': str(root.parent), 'packing': 'none explicitly requested',
            'method': 'Four actual guarded saves; copy invalid private index before normal write-tree; '
                      'replay same index only after save completes, retaining object existence checks. '
                      'Separate lookup/compression/scratch-fsync probes, not additive or p95.'}), flush=True)
        for number in range(1, 5):
            original_git, original_guard = storage.git, storage.check_managed
            trees, guards, hashes, batches = [], [], [], []
            before_index = scratch / f'before-{number}'
            actual_trace = base / f'windows-phase22-components-{number}-fresh-20261028.txt'
            assert not actual_trace.exists(), 'Preserve prior evidence'
            def observed_git(novel_root, *args, **kwargs):
                if args[0] == 'hash-object' and '--stdin-paths' in args:
                    assert kwargs['env'] == {'GIT_WORK_TREE': str(root)}
                    hashes.append(kwargs['input'].count(b'\n'))
                if args[0] == 'cat-file':
                    batches.append(kwargs['input'].count(b'\n'))
                if args[0] == 'write-tree':
                    assert args == ('write-tree',) and set(kwargs['env']) == {'GIT_INDEX_FILE'}
                    candidate_index = Path(kwargs['env']['GIT_INDEX_FILE'])
                    assert candidate_index.parent.name.startswith('candidate-')
                    shutil.copyfile(candidate_index, before_index)
                    env = {**kwargs['env'], 'GIT_TRACE2_PERF': str(actual_trace)}
                    result, elapsed = timed(lambda: original_git(novel_root, *args, **{**kwargs, 'env': env}))
                    trees.append({'oid': result.decode().strip(), 'seconds': elapsed,
                                  'trace': actual_trace.name, **trace_metrics(actual_trace)})
                    return result
                return original_git(novel_root, *args, **kwargs)
            def observed_guard(*args, **kwargs):
                result = original_guard(*args, **kwargs)
                guards.append(len(result))
                return result
            with ExitStack() as stack:
                stack.enter_context(patch.object(storage, 'git', observed_git))
                stack.enter_context(patch.object(storage, 'check_managed', observed_guard))
                actual_save = benchmark.worker(root, 'save')
            sequence = actual_save['observed_count']
            assert len(trees) == 1 and len(guards) == 2
            assert sum(hashes) == sum(batches) == 2 * sequence
            confirmed = storage.head(root)
            live_index_digest = hashlib.sha256((root / '.git/index').read_bytes()).hexdigest()
            replays = []
            for repeat in range(1, 3):
                replay_index = scratch / f'replay-{number}-{repeat}'
                shutil.copyfile(before_index, replay_index)
                trace = base / f'windows-phase22-components-{number}-existing-{repeat}-20261028.txt'
                assert not trace.exists(), 'Preserve prior evidence'
                env = {'GIT_INDEX_FILE': str(replay_index), 'GIT_TRACE2_PERF': str(trace)}
                result, elapsed = timed(lambda: storage.git(root, 'write-tree', env=env))
                assert result.decode().strip() == trees[0]['oid']
                replays.append({'seconds': elapsed, 'trace': trace.name, **trace_metrics(trace)})
            indexed = storage.git(root, 'ls-files', '--stage', '-z', env={'GIT_INDEX_FILE': str(before_index)})
            oids = [item.split(b' ', 2)[1] for item in indexed.split(b'\0') if item]
            checked, lookup = timed(lambda: storage.git(root, 'cat-file', '--batch-check=%(objectname) %(objecttype)',
                                                       input=b'\n'.join(oids) + b'\n'))
            assert checked.splitlines() == [oid + b' blob' for oid in oids]
            paths = [root / '.git/objects' / oid.decode()[:2] / oid.decode()[2:] for oid in oids]
            access_samples = []
            for _ in range(4):
                available, elapsed = timed(lambda: all(os.access(path, os.F_OK) for path in paths))
                assert available
                access_samples.append(elapsed)
            recursive = storage.git(root, 'ls-tree', '-rtz', trees[0]['oid'])
            tree_oids = [trees[0]['oid']]
            tree_oids += [line.split(b'\t', 1)[0].split()[2].decode() for line in recursive.split(b'\0')
                          if line and line.split(b'\t', 1)[0].split()[1] == b'tree']
            raw = storage.git(root, 'cat-file', '--batch', input=''.join(oid + '\n' for oid in tree_oids).encode())
            stream = io.BytesIO(raw)
            payloads = []
            for oid in tree_oids:
                content = storage._read_batch_object(stream, oid, 'tree')
                payload = b'tree ' + str(len(content)).encode() + b'\0' + content
                assert hashlib.sha1(payload).hexdigest() == oid
                payloads.append(payload)
            assert not stream.read()
            compression_samples = []
            for _ in range(4):
                _, elapsed = timed(lambda: [(hashlib.sha1(p).digest(), zlib.compress(p, 1)) for p in payloads])
                compression_samples.append(elapsed)
            writes, flushes = [], []
            for i, payload in enumerate(payloads):
                target = scratch / f'flush-{number}-{i}'
                compressed = zlib.compress(payload, 1)
                with target.open('xb') as file:
                    _, elapsed = timed(lambda: (file.write(compressed), file.flush()))
                    writes.append(elapsed)
                    _, elapsed = timed(lambda: os.fsync(file.fileno()))
                    flushes.append(elapsed)
            assert storage.head(root) == confirmed
            assert hashlib.sha256((root / '.git/index').read_bytes()).hexdigest() == live_index_digest
            print(json.dumps({'sequence': sequence, 'actual_save_instrumented_seconds': actual_save['seconds'],
                'fresh': trees[0], 'same_index_existing_tree_replays': replays,
                'guards': len(guards), 'hashed_files': sum(hashes), 'batch_objects_during_save': sum(batches),
                'lookup_probe': {'objects': len(oids), 'native_batch_check_wall_seconds': lookup,
                                 'python_loose_access_seconds': access_samples},
                'serialization_probe': {'trees': len(payloads), 'bytes_with_headers': sum(map(len, payloads)),
                    'hash_and_zlib1_seconds': compression_samples,
                    'note': 'Already-serialized verified tree bytes; excludes native tree assembly'},
                'scratch_durability_probe': {'write_seconds': writes, 'fsync_seconds': flushes,
                    'note': 'Independent scratch-file flushes, not actual Git fsync subcall timings'},
                'confirmed_head_and_live_index_unchanged_by_probes': True}), flush=True)
        assert source == {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in source}
        print(json.dumps({'source_unchanged': True, 'completed_actual_saves': 4}), flush=True)


if __name__ == '__main__':
    main()
