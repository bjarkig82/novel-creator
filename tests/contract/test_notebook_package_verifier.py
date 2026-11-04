"""Candidate notebook failures cannot masquerade as historical compatibility."""
import unittest
from unittest.mock import patch

from tests import verify_package_install


class NotebookPackageVerifierTest(unittest.TestCase):
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
