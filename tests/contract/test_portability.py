"""Portable identity and version boundaries, without literary-quality claims."""
import unittest

from novel_creator import records, validation
from tests.helpers import envelope, record, seal


class PortabilityContract(unittest.TestCase):
    def test_duplicate_unicode_names_remain_distinct_after_rename(self):
        first = envelope()
        elements = [record(first, 'story_element', element_type='character',
            display_name='Þóra / The keeper — Ðð Áá', aliases=[], status='proposed',
            assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
            for _ in range(2)]
        first = seal(dict(first, record_versions=elements))
        validation.validate_exchange(first, [])
        exchange = envelope(previous=first)
        renamed = dict(elements[0], revision=2, previous_revision=1, display_name='Ægir Örn',
                       aliases=[elements[0]['display_name']])
        state = validation.validate_exchange(seal(dict(exchange, record_versions=[renamed])), [first])
        self.assertEqual(len(state), 2)
        self.assertEqual(state[elements[0]['id']]['display_name'], 'Ægir Örn')
        self.assertEqual(state[elements[1]['id']]['display_name'], 'Þóra / The keeper — Ðð Áá')
        self.assertEqual(state[elements[0]['id']]['aliases'], ['Þóra / The keeper — Ðð Áá'])

    def test_unknown_schema_cannot_be_silently_coerced(self):
        for version in ('0.9', '1.1', '2.0'):
            with self.subTest(version=version), self.assertRaises(ValueError):
                validation.validate_exchange(seal(dict(envelope(), schema_version=version)), [])

    def test_additional_manuscript_language_preserves_text_without_claimed_resources(self):
        from novel_creator.install import bootstrap
        first = bootstrap('{"manuscript_language":"fr","title":"Þóra et le secret",'
                          '"creative_brief":{"genre":"Óákveðið / undecided"}}')
        state = validation.validate_exchange(first, [])
        project = state[first['novel_id']]
        self.assertEqual(project['manuscript_language'], 'fr')
        self.assertEqual(project['creative_brief']['genre']['original_text'], 'Óákveðið / undecided')
        self.assertEqual(project['creative_brief']['style']['state'], 'unknown')
