"""Source-free comparison of unused checked-Git stderr capture. Disposable data only."""
import argparse
from contextlib import ExitStack
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import threading
import time
import types
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
from novel_creator import records, storage
from novel_creator.cli import ToolError
from novel_creator.context import read
from tests.helpers import git, repository
from tests.performance import benchmark_records as benchmark


def prototype():
    source = Path(storage.__file__).read_text(encoding='utf-8')
    old = 'input=input, capture_output=True)'
    assert source.count(old) == 1
    module = types.ModuleType('novel_creator._stderr_diagnostic')
    exec(compile(source.replace(old, 'input=input, stdout=subprocess.PIPE, '
        'stderr=subprocess.DEVNULL if check else subprocess.PIPE)'),
        str(Path(storage.__file__).resolve()) + ':stderr-diagnostic', 'exec'), module.__dict__)
    return module.git


def system_times():
    values = [wintypes.FILETIME() for _ in range(3)]
    assert ctypes.windll.kernel32.GetSystemTimes(*[ctypes.byref(v) for v in values])
    return [v.dwLowDateTime + (v.dwHighDateTime << 32) for v in values]


def cpu_between(before, after):
    idle, kernel, user = [b - a for a, b in zip(before, after)]
    return 100 * (kernel + user - idle) / (kernel + user)


def emit(value):
    print(json.dumps(value), flush=True)


def correctness(variant):
    checks = []
    for fmt in ('sha1', 'sha256'):
        with repository(object_format=fmt) as root:
            original = storage.git(root, 'rev-parse', '--verify', 'HEAD')
            assert variant(root, 'rev-parse', '--verify', 'HEAD') == original
            raw = b'Unicode \xc3\x9e\xc3\xb3ra\x00binary\n'
            expected = storage.git(root, 'hash-object', '--stdin', input=raw)
            assert variant(root, 'hash-object', '--stdin', input=raw) == expected
            marker = 'private-diagnostic-no-such-object'
            try:
                variant(root, 'rev-parse', '--verify', marker)
            except ToolError as error:
                assert error.code == 5 and marker not in str(error)
            else:
                raise AssertionError('Checked failure not reported')
            failed = variant(root, 'rev-parse', '--verify', marker, check=False)
            assert failed.returncode != 0 and failed.stderr
            assert failed.stdout == b''
            checks.append(dict(format=fmt, stdout_equal=True, binary_stdin_equal=True,
                               checked_failure_sanitized=True, unchecked_stderr_retained=True))
    return checks


def component(candidate):
    counts = {'readers': 0}
    mutex = threading.Lock()
    reader = subprocess.Popen._readerthread
    def observed_reader(self, *args):
        with mutex:
            counts['readers'] += 1
        return reader(self, *args)
    with repository() as root:
        variants = {False: storage.git, True: candidate}
        for selected in (False, True, True, False) * 4:
            counts['readers'] = 0
            before = system_times()
            start = time.perf_counter()
            with patch.object(subprocess.Popen, '_readerthread', observed_reader):
                for _ in range(8):
                    result = variants[selected](root, 'rev-parse', '--verify', 'HEAD')
                    assert len(result.strip()) == 40
            seconds = time.perf_counter() - start
            after = system_times()
            # With stdin=None and one captured stream, communicate reads on
            # the caller thread; two captured streams require two readers.
            assert counts['readers'] == (0 if selected else 16)
            emit(dict(kind='component', candidate=selected, commands=8,
                      reader_threads=counts['readers'], seconds=seconds,
                      cpu_percent=cpu_between(before, after)))


def worker(root, selected):
    original_git, original_guard = storage.git, storage.check_managed
    chosen = prototype() if selected else original_git
    hashes, batches, guards, commands = [], [], [], []
    def observed_git(novel, *args, **kwargs):
        commands.append((args[0], kwargs.get('check', True)))
        if args[0] == 'hash-object' and '--stdin-paths' in args:
            assert kwargs['env'] == {'GIT_WORK_TREE': str(root)}
            hashes.append(kwargs['input'].count(b'\n'))
        if args[0] == 'cat-file':
            batches.append(kwargs['input'].count(b'\n'))
        return chosen(novel, *args, **kwargs)
    def observed_guard(*args, **kwargs):
        result = original_guard(*args, **kwargs)
        guards.append(len(result))
        return result
    before = system_times()
    with patch.object(storage, 'git', observed_git), patch.object(storage, 'check_managed', observed_guard):
        result = benchmark.worker(root, 'save')
    after = system_times()
    sequence = result['observed_count']
    assert len(guards) == 2 and sum(hashes) == sum(batches) == 2 * sequence
    result.update(kind='save', candidate=selected, guards=len(guards),
                  hashed_files=sum(hashes), batch_objects=sum(batches),
                  commands=len(commands), cpu_percent=cpu_between(before, after))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full-scale', action='store_true')
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--candidate', action='store_true')
    args = parser.parse_args()
    if args.worker:
        emit(worker(args.worker, args.candidate))
        return
    files = ('src/novel_creator/storage.py', 'src/novel_creator/context.py',
             'src/novel_creator/validation.py', 'tests/performance/benchmark_records.py')
    source = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files}
    emit(dict(kind='header', source=source, python=sys.version, git=storage.git(Path.cwd(), '--version').decode().strip(),
              full_scale=args.full_scale, method='ABBA repeated; diagnostic medians, not p95; no runtime file edits'))
    candidate = prototype()
    emit(dict(kind='correctness', checks=correctness(candidate)))
    if not args.full_scale:
        component(candidate)
    else:
        with benchmark.benchmark_key(True), repository(prefix='novel stderr pipe ') as root:
            novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
            history, fixture = benchmark.generate(novel)
            for exchange in history:
                path = root / storage.bundle_path(exchange)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(benchmark.serialized(exchange))
            git(root, 'add', '--', 'story/exchanges')
            git(root, 'commit', '-m', 'Disposable stderr pipe comparison')
            del history, exchange
            read(root)
            fixture['fully_validated'] = True
            emit(dict(kind='fixture', **fixture, packing='none explicitly requested'))
            for selected in (False, True, True, False) * 2:
                command = [sys.executable, '-B', __file__, '--worker', str(root)]
                if selected:
                    command.append('--candidate')
                result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=30)
                assert result.returncode == 0, result.stderr
                emit(json.loads(result.stdout))
    assert source == {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files}
    emit(dict(kind='complete', source_unchanged=True))


if __name__ == '__main__':
    main()
