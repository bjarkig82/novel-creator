"""Managed paths and Git metadata must not escape through Windows junctions."""
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from novel_creator import storage
from novel_creator.cli import ToolError
from tests.helpers import envelope, repository


class PathRedirectionTests(unittest.TestCase):
    def test_managed_components_reject_directory_and_file_reparse_points(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            path = storage.bundle_path(envelope())
            for redirected, mode in ((root / 'story', stat.S_IFDIR),
                                     (root / path, stat.S_IFREG)):
                original = os.lstat

                def redirected_stat(target, *args, **kwargs):
                    if Path(target) == redirected:
                        return SimpleNamespace(st_mode=mode,
                            st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
                    return original(target, *args, **kwargs)

                for native in (False, True):
                    with self.subTest(path=str(redirected), native=native), \
                            patch.object(os, 'lstat', side_effect=redirected_stat), \
                            patch.object(storage, '_WINDOWS_BUNDLE_TYPES', native), \
                            patch.object(storage, '_windows_file_attributes', return_value=lambda p: 0x400):
                        with self.assertRaises(ToolError) as caught:
                            storage.safe_path(root, path, _regular_leaf=True)
                        self.assertEqual(caught.exception.code, 2)

    @staticmethod
    def junction(link, target):
        result = subprocess.run(['cmd.exe', '/d', '/c', 'mklink', '/J', str(link), str(target)],
                                capture_output=True)
        if result.returncode:
            raise AssertionError(f'Junction fixture creation failed: {result.stderr!r}')

    @unittest.skipUnless(os.name == 'nt', 'Windows directory junction regression')
    def test_real_junction_cannot_redirect_exchange_publication(self):
        with tempfile.TemporaryDirectory(prefix='novel junction boundary ') as directory:
            parent = Path(directory).resolve()
            outside = parent / 'outside'
            outside.mkdir()
            with repository(parent=parent) as root:
                link = root / 'story'
                self.junction(link, outside)
                try:
                    with self.assertRaises(ToolError) as caught:
                        storage.save(root, envelope(root))
                    self.assertEqual(caught.exception.code, 2)
                    self.assertEqual(list(outside.iterdir()), [])
                finally:
                    # Remove only the junction, never recurse into its target.
                    link.rmdir()

    @unittest.skipUnless(os.name == 'nt', 'Windows directory junction regression')
    def test_real_junction_cannot_redirect_git_directory(self):
        with tempfile.TemporaryDirectory(prefix='novel Git junction boundary ') as directory:
            parent = Path(directory).resolve()
            with repository(parent=parent) as root:
                gitdir = root / '.git'
                outside = parent / 'external-git'
                # Both exact paths belong to this disposable fixture.
                self.assertTrue(gitdir.resolve().is_relative_to(parent))
                self.assertTrue(outside.absolute().is_relative_to(parent))
                gitdir.rename(outside)
                try:
                    self.junction(gitdir, outside)
                    try:
                        with self.assertRaises(ToolError) as caught:
                            storage.root_path(root)
                        self.assertEqual(caught.exception.code, 3)
                    finally:
                        gitdir.rmdir()
                finally:
                    outside.rename(gitdir)

    @unittest.skipUnless(os.name == 'nt', 'Windows directory junction regression')
    def test_final_guard_rejects_junction_inserted_after_candidate(self):
        with tempfile.TemporaryDirectory(prefix='novel late junction boundary ') as directory:
            parent = Path(directory).resolve()
            with repository(parent=parent) as root:
                first = envelope(root)
                storage.save(root, first)
                initial = storage.head(root)
                pending = envelope(root, previous=first)
                exchanges = root / 'story/exchanges'
                outside = parent / 'external-exchanges'
                self.assertTrue(exchanges.resolve().is_relative_to(parent))
                self.assertTrue(outside.absolute().is_relative_to(parent))

                def redirect(point):
                    if point == 'before_ref':
                        exchanges.rename(outside)
                        self.junction(exchanges, outside)

                try:
                    with self.assertRaises(ToolError) as caught:
                        storage.save(root, pending, fault=redirect)
                    self.assertEqual(caught.exception.code, 2)
                    self.assertEqual(storage.head(root), initial)
                    self.assertEqual(storage.read_history(root), [first])
                    self.assertTrue((root / '.novel-creator/local' /
                                     (pending['exchange_id'] + '.json')).is_file())
                finally:
                    if outside.exists():
                        if exchanges.exists():
                            exchanges.rmdir()
                        outside.rename(exchanges)
