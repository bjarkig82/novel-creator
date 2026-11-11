"""Candidate notebook failures cannot masquerade as historical compatibility."""
import io
import os
import unittest
import zipfile
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from tests import verify_package_install


class NotebookPackageVerifierTest(unittest.TestCase):
    def test_previous_release_probe_is_gated_to_newer_stable_versions(self):
        from tests.verify_previous_release import applies, verify

        for version in ('0.7.0', 'novel-creator 0.7.1', '0.7.2rc1', 'invalid'):
            with self.subTest(version=version):
                self.assertFalse(applies(version))
                with patch('tests.verify_previous_release._source') as source:
                    with self.assertRaisesRegex(ValueError, 'newer stable'):
                        verify(None, None, None, None, version, None)
                    source.assert_not_called()
        self.assertTrue(applies('novel-creator 0.7.2'))

    def test_previous_release_source_requires_the_frozen_public_wheel_digest(self):
        from tests.verify_previous_release import checked_source

        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            checked_source(b'A rebuilt or corrupted historical archive')

    def test_prior_probe_rejects_same_version_wheel_with_different_product_resources(self):
        import hashlib
        import json
        from tests.verify_previous_release import check_target_inventory

        product = {'novel_creator/__init__.py': b'__version__ = "0.7.2"\n',
                   'novel_creator/notebook_resources/workflows/clarify.md': b'Installed custom answer guidance\n'}
        installed = {name: hashlib.sha256(raw).hexdigest() for name, raw in product.items()}
        with tempfile.TemporaryDirectory() as directory:
            wheel = Path(directory) / 'novel_creator-0.7.2-py3-none-any.whl'
            for mismatch in (False, True):
                with self.subTest(mismatch=mismatch):
                    with zipfile.ZipFile(wheel, 'w') as archive:
                        archive.writestr('novel_creator-0.7.2.dist-info/METADATA',
                                         'Name: novel-creator\nVersion: 0.7.2\n')
                        for name, raw in product.items():
                            archive.writestr(name, b'Divergent same-version guidance\n'
                                             if mismatch and name.endswith('clarify.md') else raw)
                    with patch('tests.verify_previous_release._run', return_value=json.dumps(installed)) as probe:
                        if mismatch:
                            with self.assertRaisesRegex(ValueError, 'inventory differs'):
                                check_target_inventory('installed-python', wheel, '0.7.2', cwd=directory, env={})
                        else:
                            self.assertEqual(check_target_inventory('installed-python', wheel, '0.7.2',
                                                                    cwd=directory, env={}), 2)
                        self.assertEqual(probe.call_args.args[0][:4], ['installed-python', '-I', '-B', '-c'])

    def test_public_050_uses_approved_wheel_resources_and_current_stays_source_strict(self):
        from novel_creator.notebook import initialize
        from tests.notebook_resource_checks import resource_paths, verify_writing_resources

        checkout = Path(__file__).resolve().parents[2]
        paths = resource_paths(checkout)
        current = {relative: source.read_bytes() for relative, (source, _) in paths.items()}
        # Explicit historical layout, not a copy of the expanding current set.
        historical_paths = {'AGENTS.md'}
        historical_paths.update(f'.codex/agents/{name}.toml' for name in (
            'novel_orchestrator', 'novel_brainstormer', 'novel_researcher',
            'novel_scene_writer', 'novel_chapter_writer', 'novel_reviewer'))
        historical_paths.update(f'.agents/skills/novel-{name}/SKILL.md' for name in (
            'outline', 'book-idea', 'premise', 'character', 'plot', 'setting',
            'agent', 'research', 'scene', 'chapter', 'review'))
        historical_paths.update(f'.novel-notebook/workflows/{name}.md' for name in (
            'conversation', 'format', 'outline', 'brainstorming', 'agents',
            'manuscript', 'research', 'review'))
        self.assertEqual(len(historical_paths), 26)
        historical = {relative: current[relative] for relative in historical_paths}
        # Minimal historical guidance fixtures cannot link to future workflows.
        # The approved fixture bytes must still be checked exactly on install.
        for relative in ('AGENTS.md', '.novel-notebook/workflows/conversation.md',
                         '.novel-notebook/workflows/agents.md', '.novel-notebook/workflows/review.md'):
            historical[relative] = b'# Historical 0.5.0 guidance fixture.\n'
        archive_bytes = io.BytesIO()
        with zipfile.ZipFile(archive_bytes, 'w') as archive:
            for relative, raw in historical.items():
                archive.writestr(paths[relative][1], raw)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'historical'
            with patch.dict(os.environ, GIT_AUTHOR_NAME='Package verifier test',
                            GIT_AUTHOR_EMAIL='test@example.invalid', GIT_COMMITTER_NAME='Package verifier test',
                            GIT_COMMITTER_EMAIL='test@example.invalid'):
                initialize(root, title='Historical resource fixture', language='en')
            for relative in current.keys() - historical.keys():
                (root / relative).unlink()
            for relative, raw in historical.items():
                (root / relative).write_bytes(raw)

            def resource_check(console, scratch, env, language, expected_resources=None):
                return verify_writing_resources(root, current if expected_resources is None else expected_resources)

            with patch('tests.verify_wheel.verify_notebook', side_effect=resource_check) as probe:
                verified = verify_package_install.verify_notebook_install(
                    'console', root.parent, {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0',
                    verified_wheel=archive_bytes.getvalue())
                self.assertEqual(verified, [26, 26])
                self.assertEqual(probe.call_count, 2)
                for package, version in ((None, '0.5.0'), (None, '0.6.0'),
                                         ('novel-creator==0.6.0', '0.6.0')):
                    with self.subTest(package=package, version=version), self.assertRaisesRegex(AssertionError, 'AGENTS.md'):
                        verify_package_install.verify_notebook_install(
                            'console', root.parent, {}, package, 'novel-creator ' + version,
                            verified_wheel=archive_bytes.getvalue())
                for relative, raw in current.items():
                    (root / relative).write_bytes(raw)
                for package in (None, 'novel-creator==0.6.0'):
                    self.assertEqual([len(current), len(current)], verify_package_install.verify_notebook_install(
                        'console', root.parent, {}, package, 'novel-creator 0.6.0',
                        verified_wheel=archive_bytes.getvalue()))
                # Historical checks still require the exact approved bytes.
                with self.assertRaisesRegex(AssertionError, 'AGENTS.md'):
                    verify_package_install.verify_notebook_install(
                        'console', root.parent, {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0',
                        verified_wheel=archive_bytes.getvalue())

    def test_public_050_missing_required_archive_resource_fails_closed(self):
        archive_bytes = io.BytesIO()
        with zipfile.ZipFile(archive_bytes, 'w') as archive:
            archive.writestr('unrelated.txt', b'Not a notebook resource')
        with patch('tests.verify_wheel.verify_notebook') as probe:
            with self.assertRaises(KeyError):
                verify_package_install.verify_notebook_install(
                    'console', 'scratch', {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0',
                    verified_wheel=archive_bytes.getvalue())
            probe.assert_not_called()

    def test_public_050_missing_approved_wheel_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'hash-verified wheel'):
            verify_package_install.verify_notebook_install(
                'console', 'scratch', {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0')

    def test_memory_candidates_cannot_skip_as_historical_versions(self):
        with patch('tests.verify_wheel.verify_context_views', side_effect=RuntimeError('missing memory')) as probe:
            for version, package in [('0.5.0', None), ('0.6.0', None),
                                     ('0.6.0', 'novel-creator==0.6.0')]:
                with self.subTest(version=version, package=package), self.assertRaisesRegex(RuntimeError, 'missing memory'):
                    verify_package_install.verify_memory_install(
                        'python', 'launcher', 'novel', 'scratch', {}, package, version)
            self.assertEqual(probe.call_count, 3)

    def test_memory_only_known_matching_public_releases_skip(self):
        with patch('tests.verify_wheel.verify_context_views', return_value={'working': True}) as probe:
            for version in ('0.1.0', '0.2.0', '0.3.0', '0.4.0', '0.4.1', '0.5.0'):
                self.assertFalse(verify_package_install.verify_memory_install(
                    'python', 'launcher', 'novel', 'scratch', {},
                    'novel-creator==' + version, 'novel-creator ' + version)['working_views_available'])
            probe.assert_not_called()
            for package, version in [('novel-creator==0.5.0', '0.6.0'), ('other==0.5.0', '0.5.0')]:
                self.assertEqual({'working': True}, verify_package_install.verify_memory_install(
                    'python', 'launcher', 'novel', 'scratch', {}, package, version))
            self.assertEqual(probe.call_count, 2)

    def test_notebook_resources_keep_lf_in_autocrlf_checkout(self):
        checkout = Path(__file__).resolve().parents[2]
        resources = [path.relative_to(checkout) for path in (checkout / 'notebook').rglob('*')
                     if path.is_file() and path.suffix in ('.md', '.py')]
        self.assertTrue(resources)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'config', 'core.autocrlf', 'true'], check=True)
            (root / '.gitattributes').write_bytes((checkout / '.gitattributes').read_bytes())
            for relative in resources:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'first line\nsecond line\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True, capture_output=True)
            for relative in resources:
                (root / relative).unlink()
            subprocess.run(['git', '-C', str(root), 'checkout-index', '--all', '--force'], check=True)
            for relative in resources:
                with self.subTest(resource=relative):
                    self.assertEqual((root / relative).read_bytes(), b'first line\nsecond line\n')

    def test_candidate_requires_notebook_even_at_historical_version(self):
        with patch('tests.verify_wheel.verify_notebook', side_effect=RuntimeError('missing route')) as probe:
            with self.assertRaisesRegex(RuntimeError, 'missing route'):
                verify_package_install.verify_notebook_install('console', 'scratch', {}, None, 'novel-creator 0.3.0')
            probe.assert_called_once()

    def test_nonhistorical_public_failure_is_not_skipped(self):
        with patch('tests.verify_wheel.verify_notebook', side_effect=RuntimeError('broken route')) as probe:
            with self.assertRaisesRegex(RuntimeError, 'broken route'):
                verify_package_install.verify_notebook_install('console', 'scratch', {}, 'novel-creator==0.4.0', 'novel-creator 0.4.0')
            probe.assert_called_once()

    def test_only_known_public_releases_skip(self):
        with patch('tests.verify_wheel.verify_notebook') as probe:
            for version in ('0.1.0', '0.2.0', '0.3.0'):
                self.assertEqual([], verify_package_install.verify_notebook_install(
                    'console', 'scratch', {}, 'novel-creator==' + version, 'novel-creator ' + version))
            probe.assert_not_called()

    def test_supported_candidate_checks_both_languages(self):
        with patch('tests.verify_wheel.verify_notebook', side_effect=lambda *args: args[-1]) as probe:
            self.assertEqual(['en', 'is'], verify_package_install.verify_notebook_install(
                'console', 'scratch', {}, None, 'novel-creator 0.3.0'))
            self.assertEqual(2, probe.call_count)
