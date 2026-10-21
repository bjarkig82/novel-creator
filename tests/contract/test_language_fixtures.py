"""Check authored evaluation inputs, without claiming semantic host outcomes."""
import json
from pathlib import Path
import unittest


FIXTURES = Path(__file__).resolve().parents[1] / 'fixtures'


class LanguageFixtureContract(unittest.TestCase):
    def paired(self, name, section='cases'):
        documents = [json.loads((FIXTURES / language / name).read_text(encoding='utf-8'))
                     for language in ('en', 'is')]
        self.assertEqual([d['language'] for d in documents], ['en', 'is'])
        indexed = []
        for document in documents:
            cases = document[section]
            mapping = {case['id']: case for case in cases}
            self.assertEqual(len(mapping), len(cases), 'Duplicate evaluation case ID')
            indexed.append(mapping)
        self.assertEqual(indexed[0].keys(), indexed[1].keys())
        return [(indexed[0][key], indexed[1][key]) for key in indexed[0]]

    def test_acceptance_pairs_retain_outcomes_and_valid_source_spans(self):
        pairs = self.paired('acceptance.json')
        self.assertGreaterEqual(sum(a['expected_action'] == 'accept' for a, _ in pairs), 12)
        self.assertGreaterEqual(sum(a['id'].startswith('N') for a, _ in pairs), 12)
        for english, icelandic in pairs:
            with self.subTest(case=english['id']):
                for field in ('expected_action', 'selected_propositions'):
                    self.assertEqual(english[field], icelandic[field])
                for case in (english, icelandic):
                    span = case.get('source_span')
                    if span:
                        self.assertGreaterEqual(span['start'], 0)
                        self.assertLess(span['start'], span['end'])
                        self.assertLessEqual(span['end'], len(case['user_text']))
                    if case['expected_action'] == 'accept':
                        self.assertTrue(span)
                        self.assertTrue(case['selected_propositions'])
                    else:
                        self.assertEqual(case['selected_propositions'], [])
        for english, icelandic in self.paired('acceptance.json', 'revisions'):
            for field in ('prior_version', 'result_version', 'expected_action',
                          'preserve_history', 'review_direct_dependencies', 'edit_manuscript'):
                self.assertEqual(english[field], icelandic[field])

    def test_continuity_pairs_retain_categories_and_intervention_boundaries(self):
        pairs = self.paired('continuity.json')
        self.assertEqual({a['category'] for a, _ in pairs if a.get('category')},
                         {'motivation', 'chronology', 'knowledge', 'plot_dependency',
                          'world_rule', 'relationship'})
        for english, icelandic in pairs:
            with self.subTest(case=english['id']):
                for field in ('category', 'expected_assessment', 'severity',
                              'interrupt_next_response', 'may_establish_canon', 'resolutions'):
                    self.assertEqual(english.get(field), icelandic.get(field))
                if english['expected_assessment'] != 'conflict':
                    self.assertFalse(english['may_establish_canon'])

    def test_pitfall_pairs_cover_each_workflow_and_exact_quoted_source(self):
        pairs = self.paired('language-pitfalls.json')
        self.assertEqual({a['stage'] for a, _ in pairs},
                         {'setup', 'guidance', 'capture', 'acceptance', 'continuity'})
        self.assertTrue({'false_friend', 'mixed_language', 'diacritics', 'negation',
                         'partial_selection', 'quoted_dialogue'}.issubset(
                             {tag for a, _ in pairs for tag in a['challenges']}))
        for english, icelandic in pairs:
            with self.subTest(case=english['id']):
                for field in ('stage', 'challenges', 'expected_action',
                              'selected_propositions', 'expected_values'):
                    self.assertEqual(english[field], icelandic[field])
                for case in (english, icelandic):
                    span = case['source_span']
                    self.assertGreaterEqual(span['start'], 0)
                    self.assertLessEqual(span['end'], len(case['user_text']))
                    self.assertEqual(case['user_text'][span['start']:span['end']], case['source_quote'])
                    self.assertTrue(case['source_quote'])
                    if case['expected_action'] != 'accept':
                        self.assertEqual(case['selected_propositions'], [])
