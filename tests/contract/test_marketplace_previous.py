"""Release CI keeps both frozen notebook sources and installed artifact paths."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from tests import verify_marketplace_previous as previous
from tests.verify_plugin_install import temporary_environment, run


class MarketplacePreviousTests(unittest.TestCase):
    def test_both_public_sources_fail_closed_on_a_corrupt_local_wheel(self):
        self.assertEqual(set(previous.PUBLIC_WHEELS), {'0.7.2', '0.8.0', '0.9.0', '0.10.0'})
        self.assertEqual(previous.PUBLIC_WHEELS['0.8.0'][1],
                         '390c6e208fe71a803783cd2cf979bada3e20988518a0032572fcf9a1b8711c5b')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / 'corrupt.whl'
            wheel.write_bytes(b'Untrusted rebuilt historical product')
            for version in previous.PUBLIC_WHEELS:
                with self.subTest(version=version), self.assertRaisesRegex(AssertionError, 'SHA-256 mismatch'):
                    previous.previous_wheel(root, wheel, version=version)

    def test_ci_probe_runs_both_sources_against_both_candidate_artifacts(self):
        with (patch('sys.argv', ['probe', '--wheel', 'candidate.whl', '--sdist', 'candidate.tar.gz',
                                 '--report', 'report.json']),
              patch.object(previous, 'verify', return_value={'ok': True}) as verify,
              patch.object(previous, 'write_report') as report):
            previous.main()
        self.assertEqual([(call.kwargs['source_version'], call.kwargs['sdist'] is not None)
                          for call in verify.call_args_list],
                         [('0.7.2', False), ('0.7.2', True), ('0.8.0', False), ('0.8.0', True),
                          ('0.9.0', False), ('0.9.0', True), ('0.10.0', False), ('0.10.0', True)])
        self.assertEqual(len(report.call_args.args[1]['checks']), 8)
        workflow = (Path(__file__).resolve().parents[2] / '.github/workflows/package-release.yml').read_text()
        self.assertIn('tests/verify_marketplace_previous.py --wheel candidate/*.whl --sdist candidate/*.tar.gz', workflow)

    def test_new_legacy_fixture_owns_identity_despite_valid_ambient_identity(self):
        with tempfile.TemporaryDirectory(prefix='previous-legacy-identity-') as temporary:
            scratch = Path(temporary).resolve()
            env = temporary_environment(scratch)
            # This ambient identity is valid but intentionally differs from the
            # repository identity required by the production initializer.
            env.update(GIT_AUTHOR_NAME='Ambient Test Author', GIT_AUTHOR_EMAIL='ambient@example.invalid',
                       GIT_COMMITTER_NAME='Ambient Test Committer', GIT_COMMITTER_EMAIL='ambient@example.invalid')
            for language in ('en', 'is'):
                with self.subTest(language=language):
                    book = scratch / ('New legacy ' + language)
                    previous.initialize_legacy_fixture(sys.executable, book, language, scratch, env)
                    # --local cannot be satisfied by developer/global config,
                    # even when that ambient identity would hide missing setup.
                    for key, expected in (('user.name', 'Previous Release Qualification'),
                                          ('user.email', 'test@example.invalid')):
                        value = run(['git', '-C', book, 'config', '--local', '--get', key],
                                    env=env, cwd=scratch).strip()
                        self.assertEqual(value, expected)
                    identity = run(['git', '-C', book, 'log', '-1', '--format=%an%n%ae%n%cn%n%ce'],
                                   env=env, cwd=scratch).splitlines()
                    self.assertEqual(identity, ['Previous Release Qualification', 'test@example.invalid',
                                                'Previous Release Qualification', 'test@example.invalid'])
                    self.assertTrue((book / '.novel-creator/manifest.json').is_file())
