"""Exercise development fixtures, including deliberately damaged copies."""
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.notebook_contract_helpers import validate_notebook

FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures' / 'notebook'


class NotebookContractTests(unittest.TestCase):
    def test_scenarios(self):
        for language in ('en', 'is'):
            with self.subTest(language=language):
                documents = validate_notebook(FIXTURES / language)
                self.assertEqual(len(documents), 5)
                self.assertEqual(sum(len(items) for _, items, _ in documents.values()), 7)

    def test_multiline_metadata(self):
        project = FIXTURES / "en" / "project.md"
        self.assertIn('```json\n{\n', project.read_text(encoding="utf-8"))
        documents = validate_notebook(FIXTURES / "en")
        self.assertEqual(documents[project.resolve()][0]["language"], "en")

    def test_mutations_are_rejected(self):
        mutations = (
            ('duplicate topic', 'visitor.md', '"id": "visitor"', '"id": "keeper"'),
            ('duplicate item', 'keeper.md', 'Item-ID: hope', 'Item-ID: occupation'),
            ('invalid state', 'keeper.md', 'State: accepted', 'State: open'),
            ('invalid type', 'keeper.md', 'Type: statement', 'Type: rumor'),
            ('missing origin', 'keeper.md', 'Origin: The writer chose the occupation.', ''),
            ('broken file', 'keeper.md', '(letters.md)', '(missing.md)'),
            ('wrong item', 'keeper.md', 'letters#sender', 'letters#absent'),
            ('wrong topic', 'keeper.md', 'letters#sender', 'visitor#sender'),
            ('fragment', 'keeper.md', '(letters.md)', '(letters.md#sender)'),
            ('traversal', 'keeper.md', '(letters.md)', '(../../outside.md)'),
            ('unpaired key', 'keeper.md', 'letters#sender [Letters](letters.md)', 'letters#sender'),
            ('unknown perspective', 'keeper.md', 'character:keeper', 'character:missing'),
            ('version', 'keeper.md', '"version": 1', '"version": 2'),
        )
        for label, filename, before, after in mutations:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / 'notebook'
                shutil.copytree(FIXTURES / 'en', root)
                path = root / 'topics' / filename
                original = path.read_text(encoding='utf-8')
                self.assertIn(before, original)
                path.write_text(original.replace(before, after, 1), encoding='utf-8')
                with self.assertRaises(ValueError):
                    validate_notebook(root)


if __name__ == '__main__':
    unittest.main()
