import unittest
from novel_creator import records, storage
from novel_creator.context import read
from novel_creator.install import bootstrap
from tests.helpers import repository


class LanguageTests(unittest.TestCase):
    def test_language_resource_selection_preserves_names_and_unknowns(self):
        for language, title in [('en', 'Þóra and the letters'), ('is', 'Þóra og bréfin'), ('is-IS', 'Bréf frá morgundeginum')]:
            with self.subTest(language=language), repository() as root:
                import json
                b = bootstrap(json.dumps({'title': title, 'manuscript_language': language}, ensure_ascii=False),
                              records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id'])
                b['expected_git_head'] = storage.head(root)
                b['payload_digest'] = records.digest(b)
                storage.save(root, b)
                context = read(root)['data']
                self.assertEqual(context['project']['title']['original_text'], title)
                self.assertEqual(context['project']['manuscript_language'], language)
                self.assertEqual(context['language_resource'], '.novel-creator/languages/' + language.split('-')[0] + '.md')
                self.assertFalse(context['language_semantics_verified'])
