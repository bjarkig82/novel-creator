"""Fresh ordinary bundle types must preserve all transaction and fallback checks."""
from contextlib import contextmanager, ExitStack
import ctypes
import itertools
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from novel_creator import records, storage
from novel_creator.cli import ToolError
from tests.helpers import repository, git, envelope
from tests.performance import benchmark_records as benchmark


class BundleMetadataTests(unittest.TestCase):
    @staticmethod
    def _attributes(original, calls):
        def query(path):
            calls.append(path)
            try:
                mode = original(path).st_mode
            except OSError:
                return 0xffffffff
            if stat.S_ISLNK(mode):
                return 0x400
            if stat.S_ISDIR(mode):
                return 0x10
            return 0x20 if stat.S_ISREG(mode) else 0x40
        return query

    @contextmanager
    def _native_policy(self, query):
        with ExitStack() as stack:
            for name, value in (('_WINDOWS_BUNDLE_TYPES', True), ('_SAVE_HISTORY_WORKERS', 4),
                                ('_INITIAL_HASH_WORKERS', 2), ('_SAVE_HASH_WORKERS', 4),
                                ('_HISTORY_PARALLEL_MINIMUM', 1), ('_PARALLEL_HASH_MINIMUM', 1)):
                stack.enter_context(patch.object(storage, name, value))
            stack.enter_context(patch.object(storage, '_windows_file_attributes', return_value=query))
            yield

    def _fixture(self, root):
        novel = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, _ = benchmark.generate(novel, exchanges=8, sessions=2, assertions=16, minimum_bytes=0)
        for bundle in history:
            path = root / storage.bundle_path(bundle)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(benchmark.serialized(bundle))
        git(root, 'add', 'story/exchanges')
        git(root, 'commit', '-m', 'Native bundle metadata fixture')
        self.assertEqual(storage.read_history(root), history)
        return history, storage.head(root)

    def test_native_attribute_table_and_errors_always_preserve_full_lstat_fallback(self):
        bits = [1, 2, 4, 0x20]
        accepted = [0x80] + [sum(c) for n in range(1, 5) for c in itertools.combinations(bits, n)]
        fallback = [None, True, False, 1.0, "ordinary", 0, 0xffffffff, 0x10, 0x40, 0x400, 0x800, 0x40000000]
        fallback += [0x80 | value for value in accepted[1:]]
        for value in accepted:
            with self.subTest(accepted=value), patch.object(storage, '_windows_file_attributes', return_value=lambda path: value), patch.object(os, 'lstat', side_effect=AssertionError('Ordinary native result was discarded')):
                self.assertEqual(storage._bundle_leaf_mode('ordinary bundle'), stat.S_IFREG)
        for value in fallback:
            for mode in (stat.S_IFREG, stat.S_IFDIR, stat.S_IFLNK, stat.S_IFCHR):
                with self.subTest(fallback=value, mode=mode), patch.object(storage, '_windows_file_attributes', return_value=lambda path: value), patch.object(os, 'lstat', return_value=SimpleNamespace(st_mode=mode)) as checked:
                    self.assertEqual(storage._bundle_leaf_mode('special bundle'), mode)
                    checked.assert_called_once_with('special bundle')
        for error in (PermissionError('denied'), FileNotFoundError('missing')):
            with self.subTest(error=type(error).__name__), patch.object(storage, '_windows_file_attributes', return_value=lambda path: 0xffffffff), patch.object(os, 'lstat', side_effect=error):
                with self.assertRaises(type(error)) as seen:
                    storage._bundle_leaf_mode('unavailable bundle')
                self.assertIs(seen.exception, error)
        for error in (OSError('API unavailable'), TypeError('API input unavailable'), ValueError('API unavailable')):
            with self.subTest(api_error=type(error).__name__), patch.object(storage, '_windows_file_attributes', return_value=lambda path: (_ for _ in ()).throw(error)), patch.object(os, 'lstat', return_value=SimpleNamespace(st_mode=stat.S_IFREG)) as checked:
                self.assertEqual(storage._bundle_leaf_mode('ordinary bundle'), stat.S_IFREG)
                checked.assert_called_once()
        with patch.object(storage, '_windows_file_attributes', return_value=None), patch.object(os, 'lstat', return_value=SimpleNamespace(st_mode=stat.S_IFDIR)) as checked:
            self.assertEqual(storage._bundle_leaf_mode('fallback bundle'), stat.S_IFDIR)
            checked.assert_called_once()

    def test_native_initialization_and_wide_query_failures_remain_optional(self):
        factory = storage._windows_file_attributes.__wrapped__
        with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', False), patch.dict(sys.modules, {'ctypes': None}):
            self.assertIsNone(factory())
        with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.dict(sys.modules, {'ctypes': None}):
            self.assertIsNone(factory())
        for error in (OSError('DLL unavailable'), AttributeError('API unavailable')):
            fake = SimpleNamespace(WinDLL=lambda *args, **kwargs: (_ for _ in ()).throw(error), wintypes=SimpleNamespace(LPCWSTR=object(), DWORD=object()))
            with self.subTest(error=type(error).__name__), patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.dict(sys.modules, {'ctypes': fake}):
                self.assertIsNone(factory())
        class API:
            failure = None
            def __call__(self, path):
                if self.failure:
                    raise self.failure
                self.path = path
                return 0x20
        api = API()
        fake = SimpleNamespace(WinDLL=lambda *args, **kwargs: SimpleNamespace(GetFileAttributesW=api), ArgumentError=ctypes.ArgumentError, wintypes=SimpleNamespace(LPCWSTR=object(), DWORD=object()))
        with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.dict(sys.modules, {'ctypes': fake}):
            query = factory()
            self.assertEqual(api.argtypes, [fake.wintypes.LPCWSTR])
            self.assertIs(api.restype, fake.wintypes.DWORD)
            self.assertEqual(query('C:/Þóra/ordinary bundle.json'), 0x20)
            self.assertEqual(api.path, 'C:/Þóra/ordinary bundle.json')
            for error in (OSError('API failure'), TypeError('API failure'), ValueError('API failure'), ctypes.ArgumentError('wide input unavailable')):
                api.failure = error
                self.assertIsNone(query('ordinary bundle'))

    def test_native_queries_are_fresh_and_exclude_parents_nonbundles_and_nonwindows(self):
        self.assertEqual(storage._WINDOWS_BUNDLE_TYPES, os.name == 'nt')
        with repository(prefix='novel metadata Þóra with spaces-') as root:
            relative = 'story/exchanges/000001-' + benchmark.uid() + '.json'
            leaf = root / relative
            leaf.parent.mkdir(parents=True, exist_ok=True)
            leaf.write_bytes(b'ordinary bytes\n')
            original = os.lstat
            native, ordinary = [], []
            query = self._attributes(original, native)
            def traced(path):
                ordinary.append(os.fspath(path))
                return original(path)
            with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.object(storage, '_windows_file_attributes', return_value=query), patch.object(os, 'lstat', traced):
                for _ in range(2):
                    self.assertEqual(storage._checked_path(root, relative, _regular_leaf=True, _directories=set()), str(leaf))
                self.assertEqual(native, [str(leaf), str(leaf)])
                self.assertNotIn(str(leaf), ordinary)
                self.assertEqual(ordinary.count(str(root / 'story')), 2)
                self.assertEqual(ordinary.count(str(root / 'story/exchanges')), 2)
                self.assertEqual(storage._checked_path(root, relative), str(leaf))
                self.assertIn(str(leaf), ordinary)
                self.assertEqual(len(native), 2)
                storage._checked_path(root, '.novel-creator/manifest.json', _regular_leaf=True)
                self.assertEqual(len(native), 2)
            with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', False), patch.object(storage, '_windows_file_attributes', side_effect=AssertionError('Non-Windows initialized a native query')):
                self.assertEqual(storage._checked_path(root, relative, _regular_leaf=True), str(leaf))

    def test_native_unicode_long_and_special_paths_preserve_original_results(self):
        with tempfile.TemporaryDirectory(prefix='novel native Þóra-') as directory:
            root = Path(directory).resolve() / ('long' * 20) / ('path' * 20) / ('name' * 20)
            relative = 'story/exchanges/000001-' + benchmark.uid() + '.json'
            leaf = root / relative
            try:
                leaf.parent.mkdir(parents=True)
                leaf.write_bytes(b'ordinary bytes\n')
            except OSError as error:
                if getattr(error, 'winerror', None) in (3, 206):
                    self.skipTest('Long-path creation unsupported by this Windows runtime')
                raise
            variants = [root]
            if os.name == 'nt' and not str(root).startswith('\\\\?\\'):
                variants.append(Path('\\\\?\\' + str(root)))
            for selected_root in variants:
                with self.subTest(root=str(selected_root)), patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.object(storage, '_windows_file_attributes', return_value=lambda path: 0xffffffff):
                    self.assertEqual(storage._checked_path(selected_root, relative, _regular_leaf=True), str(selected_root / relative))
            if os.name == 'nt':
                with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True):
                    live = storage._windows_file_attributes.__wrapped__()
                if live is not None:
                    for selected_root in variants:
                        observed = []
                        def queried(path):
                            value = live(path)
                            observed.append(value)
                            return value
                        with self.subTest(native_root=str(selected_root)), patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.object(storage, '_windows_file_attributes', return_value=queried):
                            selected_leaf = selected_root / relative
                            self.assertEqual(storage._checked_path(selected_root, relative, _regular_leaf=True), str(selected_leaf))
                            self.assertEqual(len(observed), 1)
                            if str(selected_root).startswith('\\\\?\\'):
                                self.assertEqual(observed[0], os.lstat(selected_leaf).st_file_attributes)
            original = os.lstat
            query = self._attributes(original, [])
            leaf.unlink()
            leaf.mkdir()
            with self._native_policy(query), self.assertRaises(ToolError) as error:
                storage._checked_path(root, relative, _regular_leaf=True)
            self.assertEqual(error.exception.code, 3)
            leaf.rmdir()
            with self._native_policy(query), self.assertRaises(ToolError) as error:
                storage._checked_path(root, relative, _regular_leaf=True)
            self.assertEqual(error.exception.code, 3)

    def test_native_same_stat_edit_stays_pending_then_exact_retry_publishes_once(self):
        for fmt in ('sha1', 'sha256'):
            with self.subTest(fmt=fmt), benchmark.benchmark_key(True), repository(object_format=fmt) as root:
                history, commit = self._fixture(root)
                pending = envelope(root, previous=history[-1])
                target = root / storage.bundle_path(history[0])
                before = target.stat()
                original = target.read_bytes()
                changed = original[:-1] + (b' ' if original[-1:] != b' ' else b'\n')
                self.assertNotEqual(changed, original)
                index = (root / '.git/index').read_bytes()
                calls = []
                query = self._attributes(os.lstat, calls)
                def tamper(point):
                    if point == 'before_ref':
                        target.write_bytes(changed)
                        os.utime(target, ns=(before.st_atime_ns, before.st_mtime_ns))
                with self._native_policy(query):
                    with self.assertRaises(ToolError) as error:
                        storage.save(root, pending, fault=tamper)
                    self.assertEqual(error.exception.code, 3)
                    self.assertEqual(len(calls), 16)
                    self.assertEqual(storage.head(root), commit)
                    self.assertEqual((root / '.git/index').read_bytes(), index)
                    self.assertEqual(target.read_bytes(), changed)
                    self.assertFalse((root / '.novel-creator/local/write.lock').exists())
                    receipt = storage.read_receipt(root, root / '.novel-creator/local' / (pending['exchange_id'] + '.json'))
                    self.assertEqual(receipt['state'], 'pending')
                    self.assertIn('candidate', receipt)
                    target.write_bytes(original)
                    calls.clear()
                    saved = storage.save(root, pending)
                    self.assertEqual(len(calls), 16)
                    self.assertCountEqual(calls, [str(root / storage.bundle_path(bundle)) for bundle in history] * 2)
                    self.assertFalse(saved['data']['cleanup_required'])
                    again = storage.save(root, pending)
                    self.assertTrue(again['data']['already_saved'])
                    self.assertEqual(len(calls), 16)
                    self.assertEqual(saved['checkpoint'], again['checkpoint'])
                self.assertEqual(git(root, 'rev-list', '--count', commit + '..HEAD'), '1')
                self.assertEqual(storage.read_history(root), history + [pending])
                self.assertEqual(git(root, 'diff', '--cached', '--exit-code'), '')

    def test_native_staged_tampering_is_preserved_and_prevents_publication(self):
        for fmt in ('sha1', 'sha256'):
            with self.subTest(fmt=fmt), benchmark.benchmark_key(True), repository(object_format=fmt) as root:
                history, commit = self._fixture(root)
                pending = envelope(root, previous=history[-1])
                entries = storage.committed_entries(root, commit)
                first, second = [storage.bundle_path(bundle) for bundle in history[:2]]
                external = []
                def tamper(point):
                    if point == 'before_ref':
                        storage.git(root, 'update-index', '--cacheinfo', f'100644,{entries[second][1]},{first}')
                        external.append((root / '.git/index').read_bytes())
                with self._native_policy(self._attributes(os.lstat, [])), self.assertRaises(ToolError) as error:
                    storage.save(root, pending, fault=tamper)
                self.assertEqual(error.exception.code, 3)
                self.assertEqual(storage.head(root), commit)
                self.assertEqual((root / '.git/index').read_bytes(), external[0])
                self.assertFalse((root / '.novel-creator/local/write.lock').exists())
                receipt = storage.read_receipt(root, root / '.novel-creator/local' / (pending['exchange_id'] + '.json'))
                self.assertEqual(receipt['state'], 'pending')

    def test_native_bootstrap_and_identical_retry_do_not_initialize_queries(self):
        for fmt in ('sha1', 'sha256'):
            with self.subTest(fmt=fmt), repository(unborn=True, object_format=fmt) as root:
                first = envelope(root)
                with patch.object(storage, '_WINDOWS_BUNDLE_TYPES', True), patch.object(storage, '_windows_file_attributes', side_effect=AssertionError('Bootstrap/retry initialized native leaf queries')):
                    saved = storage.save(root, first)
                    again = storage.save(root, first)
                    self.assertEqual(storage.read_history(root), [first])
                self.assertTrue(again['data']['already_saved'])
                self.assertEqual(saved['checkpoint'], again['checkpoint'])