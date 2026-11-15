"""Historical fixture lookup is offline and independent of local release tooling."""
from pathlib import Path
import unittest
from unittest.mock import patch
from tests.release_fixtures import SHA256, published_wheel


class ReleaseFixtureTests(unittest.TestCase):
    def test_lookup_never_reads_local_tools_artifacts(self):
        original = Path.read_bytes
        def read(path):
            self.assertNotIn('.tools', path.parts)
            return original(path)
        with patch.object(Path, 'read_bytes', read):
            for version in SHA256:
                self.assertEqual(published_wheel(version).parent,
                                 Path(__file__).resolve().parents[1] / 'fixtures/releases')

    def test_changed_fixture_is_rejected(self):
        with patch.object(Path, 'read_bytes', return_value=b'changed'):
            with self.assertRaisesRegex(AssertionError, 'hash differs'):
                published_wheel('0.10.1')
