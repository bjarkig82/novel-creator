"""Release policy exercises real cumulative Git trees, without product mutation."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from tests.release_checks import select_windows_suite, load_compatibility_suite, COMPATIBILITY_TESTS


class ReleaseChecks(unittest.TestCase):
    def test_real_cumulative_git_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
            git('init', '-q'); git('config', 'user.email', 'test@example.invalid'); git('config', 'user.name', 'Test')
            def commit(path, content):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
                git('add', '-A'); git('commit', '-qm', 'test')
                return git('rev-parse', 'HEAD')
            commit('src/novel_creator/__init__.py', '__version__ = \"0.6.0\"\n')
            baseline = commit('README.md', 'baseline')
            commit('src/novel_creator/__init__.py', '__version__ = \"0.6.1\"\n')
            self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'compatibility')
            for path in ['docs/a space.md', 'resources/a.md', 'src/novel_creator/context.py', 'src/novel_creator/memory.py', 'tests/contract/test_context.py', '.github/workflows/package-release.yml', 'tests/release_checks.py', 'tests/package_release.py', 'tests/contract/test_release_checks.py', 'tests/contract/test_package_release.py', 'AGENTS.md', 'workflows/review.md', 'languages/is.md', 'notebook/templates/project.md', 'adapters/codex/skills/novel-init/SKILL.md', 'adapters/codex/notebook/agents/novel_reviewer.toml', 'tests/contract/test_working_context.py']:
                commit(path, 'routine')
                self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'compatibility')
            self.assertEqual(select_windows_suite(root, baseline=baseline, full=True)['profile'], 'full')
            safe = git('rev-parse', 'HEAD')
            commit('src/novel_creator/__init__.py', '__version__ = \"0.6.1\"\nprint(\"side effect\")\n')
            self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'full')
            git('reset', '--hard', safe)
            risky = commit('src/novel_creator/storage.py', 'sensitive')
            commit('docs/later.md', 'later')
            self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'full')
            for path in ['src/novel_creator/new.py', 'pyproject.toml', 'tests/integration/test_path_redirection.py', 'tests/update_helpers.py', '.gitattributes', 'src/novel_creator/__init__.py', 'notebook/new.py', 'adapters/codex/notebook/agents/new.toml']:
                git('reset', '--hard', risky + '~1')
                commit(path, 'risk')
                self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'full')
            git('reset', '--hard', risky + '~1')
            git('mv', 'src/novel_creator/context.py', 'src/novel_creator/storage.py')
            git('commit', '-qm', 'rename')
            self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'full')
            git('reset', '--hard', risky)
            git('rm', 'src/novel_creator/storage.py'); git('commit', '-qm', 'delete')
            self.assertEqual(select_windows_suite(root, baseline=risky)['profile'], 'full')
            self.assertEqual(select_windows_suite(root, baseline='f' * 40)['profile'], 'full')
            git('checkout', '--orphan', 'unrelated'); git('rm', '-rf', '.')
            commit('README.md', 'orphan')
            self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'full')

    def test_shallow_history_requires_full(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'clone'
            subprocess.run(['git', 'clone', '-q', '--depth=1', Path.cwd().as_uri(), str(root)], check=True)
            baseline = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
            self.assertEqual(select_windows_suite(root, baseline=baseline)['profile'], 'full')

    def test_manifest_records_auto_and_manual_full_at_exact_source(self):
        from contextlib import chdir
        import json
        import os
        import zipfile
        from unittest.mock import patch
        from tests.package_release import manifest, verify_files
        from tests.release_checks import WINDOWS_BASELINE
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', str(Path.cwd()), str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'checkout', '-q', WINDOWS_BASELINE], check=True)
            candidate = root / 'candidate'; candidate.mkdir()
            with zipfile.ZipFile(candidate / 'a.whl', 'w') as archive:
                archive.writestr('a.dist-info/METADATA', 'Name: novel-creator\nVersion: 0.6.0\n')
            (candidate / 'a.tar.gz').write_bytes(b'source')
            env = dict(GITHUB_SHA=WINDOWS_BASELINE, GITHUB_REPOSITORY='o/r', GITHUB_RUN_ID='12', GITHUB_RUN_ATTEMPT='1')
            with chdir(root), patch.dict(os.environ, env):
                for full, expected in [(False, 'compatibility'), (True, 'full')]:
                    data = manifest(candidate, full=full)
                    self.assertEqual(data['windows_suite'], expected)
                    self.assertEqual(json.loads((candidate / 'manifest.json').read_text())['windows_suite'], expected)
                data['windows_suite'] = 'unsupported'
                (candidate / 'manifest.json').write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    verify_files(candidate, repository='o/r', run_id='12', run_attempt='1', source_commit=WINDOWS_BASELINE)
            with chdir(root), patch.dict(os.environ, dict(env, GITHUB_SHA='f' * 40)):
                with self.assertRaises(ValueError): manifest(candidate)

    def test_explicit_suite_and_missing_ids(self):
        suite = load_compatibility_suite()
        def ids(suite):
            for item in suite:
                if isinstance(item, unittest.TestSuite): yield from ids(item)
                else: yield item.id()
        names = list(ids(suite))
        self.assertTrue(any('path_redirection' in name for name in names))
        self.assertIn('tests.integration.test_storage.StorageTests.test_clean_save_continuation_and_retry_leave_managed_index_synchronized', names)
        self.assertIn('tests.integration.test_recovery.RecoveryTests.test_pending_inspection_and_unchanged_retry', names)
        self.assertFalse(any('test_update' in name for name in names))
        self.assertEqual(len(COMPATIBILITY_TESTS), 5)
        for selected in [(), ('tests.integration.test_storage.StorageTests.nonexistent',)]:
            with self.assertRaises(ValueError): load_compatibility_suite(selected)
