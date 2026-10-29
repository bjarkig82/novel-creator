"""Owner-thread native Git profiling in disposable full-scale saved fixtures."""
import argparse
from contextlib import ExitStack
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import git, repository
from tests.performance import benchmark_records as benchmark

BASE = Path.cwd() / '.tools/t172-git-native-20261028'
EXES = {'installed': Path(shutil.which('git')).resolve(),
        'baseline': BASE / 'baseline/git.exe',
        'profile_off': BASE / 'git-build-v2/git.exe',
        'profile_on': BASE / 'git-build-v2/git.exe'}
GIT, RUN = storage.git, subprocess.run


def run_git(exe, root, *args, env=None):
    def selected(argv, **kwargs):
        assert argv[0] == 'git'
        return RUN([str(exe), *argv[1:]], **kwargs)
    with patch.object(storage.subprocess, 'run', selected):
        return GIT(root, *args, env=env, check=False)


def parsed_profile(stderr):
    lines = [line for line in stderr.decode('utf-8').splitlines() if line.startswith('T172_PROFILE ')]
    assert len(lines) <= 1
    return json.loads(lines[0][len('T172_PROFILE '):]) if lines else None


class Memory(ctypes.Structure):
    _fields_ = [('length', wintypes.DWORD), ('load', wintypes.DWORD),
                *[(name, ctypes.c_ulonglong) for name in ('total_phys', 'avail_phys', 'total_page',
                  'avail_page', 'total_virtual', 'avail_virtual', 'avail_extended')]]


def system_times():
    values = [wintypes.FILETIME() for _ in range(3)]
    assert ctypes.windll.kernel32.GetSystemTimes(*[ctypes.byref(v) for v in values])
    return [v.dwLowDateTime + (v.dwHighDateTime << 32) for v in values]


def memory():
    state = Memory()
    state.length = ctypes.sizeof(state)
    assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state))
    return {'available_physical_bytes': state.avail_phys, 'total_physical_bytes': state.total_phys}


def load_between(first, last):
    idle, kernel, user = [b - a for a, b in zip(first, last)]
    total = kernel + user
    return max(0.0, min(100.0, 100 * (total - idle) / total)) if total else None


def quiet_gate(emit):
    previous, consecutive = system_times(), 0
    for number in range(12):
        time.sleep(5)
        current = system_times()
        observed = {'kind': 'load', 'sample': number + 1, 'cpu_percent': load_between(previous, current), **memory()}
        previous = current
        quiet = observed['cpu_percent'] is not None and observed['cpu_percent'] <= 40 and observed['available_physical_bytes'] >= 2 * 1024**3
        consecutive = consecutive + 1 if quiet else 0
        observed['consecutive_quiet'] = consecutive
        emit(observed)
        if consecutive >= 3:
            return True
    return False


def correctness():
    checks = []
    for format in ('sha1', 'sha256'):
        with repository(object_format=format) as root:
            target = root / 'Þóra.txt'
            target.write_text('Native diagnostic only.\n', encoding='utf-8')
            oid = GIT(root, 'hash-object', '-w', '--', str(target)).decode().strip()
            before = root / '.novel-creator/local/before-index'
            env = {'GIT_INDEX_FILE': str(before)}
            GIT(root, 'read-tree', 'HEAD', env=env)
            GIT(root, 'update-index', '--add', '--cacheinfo', f'100644,{oid},Þóra.txt', env=env)
            expected = None
            for variant, exe in EXES.items():
                index = root / f'.novel-creator/local/{variant}-index'
                shutil.copyfile(before, index)
                result = run_git(exe, root, 'write-tree', env={'GIT_INDEX_FILE': str(index),
                                 **({'GIT_T172_PROFILE': '1'} if variant == 'profile_on' else {})})
                assert result.returncode == 0, (variant, result.stderr.decode(errors='replace'))
                expected = expected or result.stdout.strip()
                assert result.stdout.strip() == expected
                profile = parsed_profile(result.stderr)
                assert (profile is not None) == (variant == 'profile_on')
                bad = '1' * (40 if format == 'sha1' else 64)
                GIT(root, 'update-index', '--add', '--cacheinfo', f'100644,{bad},missing', env={'GIT_INDEX_FILE': str(index)})
                failure = run_git(exe, root, 'write-tree', env={'GIT_INDEX_FILE': str(index),
                                 **({'GIT_T172_PROFILE': '1'} if variant == 'profile_on' else {})})
                assert failure.returncode != 0 and not failure.stdout
                checks.append({'format': format, 'variant': variant, 'matching_tree_oid': expected.decode(),
                               'missing_object_rejected': True, 'missing_object_returncode': failure.returncode})
    return checks


def worker(root, variant):
    guards, hashes, batches, tree = [], [], [], []
    original_guard = storage.check_managed
    def observed_git(novel, *args, **kwargs):
        if args[0] == 'hash-object' and '--stdin-paths' in args:
            assert kwargs['env'] == {'GIT_WORK_TREE': str(root)}
            hashes.append(kwargs['input'].count(b'\n'))
        if args[0] == 'cat-file':
            batches.append(kwargs['input'].count(b'\n'))
        if args[0] == 'write-tree':
            assert args == ('write-tree',) and set(kwargs['env']) == {'GIT_INDEX_FILE'}
            assert Path(kwargs['env']['GIT_INDEX_FILE']).parent.name.startswith('candidate-')
            env = {**kwargs['env'], **({'GIT_T172_PROFILE': '1'} if variant == 'profile_on' else {})}
            cooldown = []
            if not quiet_gate(cooldown.append):
                print(json.dumps({'kind': 'not_measured', 'reason': 'Pre-command quiet gate failed', 'load': cooldown}), file=sys.stderr, flush=True)
                raise storage.ToolError(5, 'Native diagnostic quiet gate did not pass')
            before = system_times()
            start = time.perf_counter()
            result = run_git(EXES[variant], novel, *args, env=env)
            seconds = time.perf_counter() - start
            cpu = load_between(before, system_times())
            assert result.returncode == 0, result.stderr.decode(errors='replace')
            profile = parsed_profile(result.stderr)
            assert (profile is not None) == (variant == 'profile_on')
            if profile:
                assert profile['result'] >= 0
                assert profile['metrics']['lookup']['calls'] >= 5000
                assert profile['metrics']['serialize']['calls'] >= 5000
                assert profile['metrics']['object_write']['calls'] == 3
                assert profile['metrics']['fsync']['calls'] == 3
                assert profile['metrics']['deflate']['calls'] > 0
                assert sum(m['exclusive_ns'] for m in profile['metrics'].values()) <= profile['total_ns']
            tree.append({'wall_seconds': seconds, 'system_cpu_percent': cpu, 'profile': profile, 'pre_tree_load': cooldown,
                         'quiet_window': cpu is not None and cpu <= 40, 'oid': result.stdout.decode().strip(), **memory()})
            return result.stdout
        return GIT(novel, *args, **kwargs)
    def observed_guard(*args, **kwargs):
        result = original_guard(*args, **kwargs)
        guards.append(len(result))
        return result
    with ExitStack() as stack:
        stack.enter_context(patch.object(storage, 'git', observed_git))
        stack.enter_context(patch.object(storage, 'check_managed', observed_guard))
        result = benchmark.worker(root, 'save')
    sequence = result['observed_count']
    assert len(guards) == 2 and sum(hashes) == sum(batches) == 2 * sequence and len(tree) == 1
    return {'kind': 'sample', 'variant': variant, 'save_seconds': result['seconds'], 'sequence': sequence,
            'guards': len(guards), 'hashed_files': sum(hashes), 'batch_objects': sum(batches), 'tree': tree[0]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', choices=EXES)
    parser.add_argument('--novel', type=Path)
    parser.add_argument('--output', type=Path, default=Path('tests/evaluations/windows-phase22-native-profile-settled-20261028.jsonl'))
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.novel, args.worker)))
        return 0
    source = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (
        'src/novel_creator/storage.py', 'src/novel_creator/context.py',
        'src/novel_creator/validation.py', 'tests/performance/benchmark_records.py')}
    binaries = {name: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'build_options': RUN([str(path), 'version', '--build-options'], capture_output=True, text=True, check=True).stdout}
                for name, path in EXES.items()}
    with args.output.open('x', encoding='utf-8') as log:
        def emit(value):
            log.write(json.dumps(value) + '\n')
            log.flush()
        emit({'kind': 'header', 'source': source, 'binaries': binaries,
              'upstream_commit': 'f8165afd89b0c190677a093f20894f5fce12f97a',
              'method': 'Four fresh-worker profile-only saves; quiet gating before fixture and each private tree command. Waiting is included in save_seconds, which is not operation latency. Only private write-tree selects diagnostic binary; '
                        'all other Git operations use installed Git. Three quiet samples <=40% CPU/>=2GiB before measurement; '
                        'all per-command load windows retained. Native profile is MSVC/zlib1.3.1 source build, not installed-distribution qualification.'})
        emit({'kind': 'correctness', 'checks': correctness()})
        if not quiet_gate(emit):
            emit({'kind': 'not_measured', 'reason': 'Preflight quiet gate did not pass in 60 seconds; no new fixture or timing samples'})
            return 2
        with benchmark.benchmark_key(True), repository(prefix='novel native profile ') as root:
            novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
            history, fixture = benchmark.generate(novel)
            for exchange in history:
                path = root / storage.bundle_path(exchange)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(benchmark.serialized(exchange))
            git(root, 'add', '--', 'story/exchanges')
            git(root, 'commit', '-m', 'Disposable native profiler fixture')
            del history, exchange
            read(root)
            fixture['fully_validated'] = True
            emit({'kind': 'fixture', **fixture, 'packing': 'none explicitly requested', 'temp': str(root.parent)})
            if not quiet_gate(emit):
                emit({'kind': 'not_measured', 'reason': 'Quiet-load gate did not pass in 60 seconds; no performance samples claimed'})
                return 2
            order = ('profile_on',) * 4
            for variant in order:
                result = RUN([sys.executable, '-B', __file__, '--worker', variant, '--novel', str(root)],
                             capture_output=True, text=True, encoding='utf-8', timeout=120)
                if result.returncode:
                    emit({'kind': 'failure', 'variant': variant, 'returncode': result.returncode, 'stderr': result.stderr})
                    return 1
                emit(json.loads(result.stdout))
            assert source == {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in source}
            assert all(hashlib.sha256(Path(info['path']).read_bytes()).hexdigest() == info['sha256'] for info in binaries.values())
            emit({'kind': 'summary', 'completed_saves': 4, 'source_and_binaries_unchanged': True})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
