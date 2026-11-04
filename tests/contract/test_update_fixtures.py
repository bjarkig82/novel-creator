import json
import tempfile
import unittest
from pathlib import Path

from tests.update_helpers import artifact, historical_book, add_writer_work, snapshot
from tests.update_release_helpers import FakeReleaseTransport, PRIVATE_SEEDS, archive


class UpdateFixtureTests(unittest.TestCase):
    def test_historical_wheels_have_exact_approved_bytes_and_independent_books(self):
        for version in ('0.1.0', '0.2.0'):
            with self.subTest(version=version), historical_book(version, language='is') as book:
                result = json.loads(book.run(
                    "import json, novel_creator; print(json.dumps({'origin':novel_creator.__file__}))"))
                self.assertTrue(Path(result['origin']).is_relative_to(book.vendor))
                before = add_writer_work(book.root)
                self.assertEqual(before, snapshot(book.root))
                self.assertNotEqual((book.root / 'notes.txt').read_bytes(), b'staged\n')
                self.assertIn('notes.txt', before['index'])

    def test_rebuilt_or_changed_wheel_cannot_claim_release_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            wrong = Path(directory) / 'wrong.whl'
            wrong.write_bytes(b'not the approved release')
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                artifact('0.1.0', wrong)

    def test_transport_is_explicit_offline_and_checks_private_values(self):
        transport = FakeReleaseTransport({'https://pypi.org/public': b'fixture'})
        self.assertEqual(transport.get('https://pypi.org/public'), b'fixture')
        with self.assertRaises(OSError):
            transport.get('https://pypi.org/missing')
        for seed in PRIVATE_SEEDS:
            with self.assertRaises(AssertionError):
                transport.get('https://pypi.org/' + seed)
        raw, digest = archive([('../bad.py', b'hostile fixture')])
        self.assertTrue(raw)
        self.assertEqual(len(digest), 64)
