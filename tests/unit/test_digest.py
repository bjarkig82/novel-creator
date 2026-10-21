import hashlib
import unittest
from novel_creator import records


class DigestTests(unittest.TestCase):
    def test_canonical_unicode_sorted_keys_and_array_order(self):
        data = {"z": [2, 1], "á": "Þóra", "payload_digest": "ignored"}
        expected = '{"z":[2,1],"á":"Þóra"}'.encode()
        self.assertEqual(records.canonical_bytes(data), expected)
        self.assertEqual(records.digest(data), hashlib.sha256(expected).hexdigest())
        self.assertNotEqual(records.digest(data), records.digest({"z": [1, 2], "á": "Þóra"}))

    def test_strict_input(self):
        for raw in (b'\xff', b'{', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1,"x":2}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                records.loads(raw)

    def test_nonfinite_serialization_rejected(self):
        with self.assertRaises(ValueError):
            records.canonical_bytes({"x": float("inf")})

    def test_overflow_number_is_not_finite_json(self):
        with self.assertRaises(ValueError):
            records.loads('{"value":1e999}')
