"""Structural examples only: no host conversation or automatic save is executed."""
from collections import Counter
from pathlib import Path
import re
import unittest

from tests.notebook_contract_helpers import validate_notebook


FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures' / 'notebook-grouped'


def current_blocks(text):
    """Read this fixture's current item blocks, excluding its revision archive."""
    current = text.split('\n## Revisions', 1)[0]
    blocks = re.findall(r'^### [^\n]+\n(.*?)(?=^#{2,3} |\Z)', current, re.M | re.S)
    return {re.search(r'^Item-ID: (.+)$', block, re.M)[1]: block.strip()
            for block in blocks}


class GroupedNotebookExamples(unittest.TestCase):
    def snapshot(self, stage):
        root = (FIXTURES / stage).resolve()
        documents = validate_notebook(root)
        topic = documents[root / 'topics/keeper.md']
        summary = documents[root / 'working-summary.md'][2]
        return topic, summary

    def assert_summary_counts(self, items, summary):
        counts = Counter((item['Type'], item['State']) for item in items.values())
        expected = [counts[key] for key in (
            ('statement', 'accepted'), ('statement', 'proposed'),
            ('statement', 'rejected'), ('question', 'open'), ('question', 'resolved'))]
        row = re.search(r'^\| keeper \[Alex\]\(topics/keeper.md\) \| (.+) \|$', summary, re.M)
        self.assertIsNotNone(row)
        actual = [int(value.strip()) for value in row[1].split('|')]
        self.assertEqual(actual, expected)
        # The focus keeps its semantic identity as well as its valid file link.
        focus = re.search(r'Recent focus: keeper#([a-z-]+) ', summary)
        self.assertIsNotNone(focus)
        self.assertIn(focus[1], items)

    def test_grouped_snapshots_keep_independent_fields_and_derived_counts(self):
        for stage, accepted in (('before', 4), ('after', 5)):
            with self.subTest(stage=stage):
                (metadata, items, text), summary = self.snapshot(stage)
                self.assertEqual(metadata['id'], 'keeper')
                self.assertEqual(len(items), accepted + 3)  # proposal plus two questions
                self.assertEqual(set(current_blocks(text)), set(items))
                self.assertEqual(items['relief']['State'], 'proposed')
                self.assertEqual(items['sender']['State'], 'open')
                self.assertEqual(items['naming']['State'], 'resolved')
                self.assertEqual(items['belief']['Perspective'], 'character:keeper')
                self.assertEqual(items['motive']['Perspective'], 'objective')
                self.assertEqual(items['belief']['Links'],
                                 'keeper#motive [Reason to stay](keeper.md)')
                self.assert_summary_counts(items, summary)
                # Historical accepted copies share the ID, but are not current items.
                self.assertGreater(text.count('Item-ID: occupation'), 1)
                history = text.split('\n## Revisions', 1)[1]
                self.assertIn('State: accepted', history)
                self.assertIn('Alex was an archivist.', history)

    def test_selected_addition_and_revision_preserve_other_items_and_history(self):
        (before_meta, before, before_text), _ = self.snapshot('before')
        (after_meta, after, after_text), _ = self.snapshot('after')
        self.assertEqual(before_meta, after_meta)
        self.assertEqual(set(after) - set(before), {'care'})
        self.assertEqual(set(before) - set(after), set())
        before_blocks, after_blocks = current_blocks(before_text), current_blocks(after_text)
        for item_id in set(before) - {'occupation'}:
            with self.subTest(item_id=item_id):
                self.assertEqual(before[item_id], after[item_id])
                self.assertEqual(before_blocks[item_id], after_blocks[item_id])
        self.assertEqual(after['care']['State'], 'accepted')
        self.assertEqual(after['relief']['State'], 'proposed')
        self.assertIn('detail alone', after['care']['Origin'])
        self.assertIn('lighthouse keeping', after['occupation']['Origin'])
        self.assertIn('Alex keeps the lighthouse.', after_blocks['occupation'])
        history = after_text.split('\n## Revisions', 1)[1]
        self.assertIn(before_blocks['occupation'], history)
        self.assertIn(before_text.split('\n## Revisions', 1)[1].strip(), history)

    def test_stale_count_and_history_inflation_are_detectable(self):
        (_, items, _), summary = self.snapshot('after')
        for wrong in (4, 7):  # stale before count; count including two historical copies
            with self.subTest(wrong=wrong), self.assertRaises(AssertionError):
                self.assert_summary_counts(items, summary.replace('| 5 | 1 |', f'| {wrong} | 1 |'))


if __name__ == '__main__':
    unittest.main()
