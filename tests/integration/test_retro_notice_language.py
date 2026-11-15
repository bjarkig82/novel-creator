import unittest
from tests.retro_helpers import fixtures, historical_notice


class NoticeLanguage(unittest.TestCase):
    def test_interaction_language_renders_before_digest_reservation(self):
        from novel_creator.retro import Retro,digest
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry)
            run=historical_notice(service,checkout,initial)
            english=service.notices_pending(language='en')['notices'][0]
            icelandic=service.notices_pending(language='is')['notices'][0]
            self.assertNotEqual(english['text'],icelandic['text'])
            self.assertIn('Endurskoðun',icelandic['text'])
            self.assertEqual(icelandic['text_digest'],digest(icelandic['text'].encode()))
            self.assertEqual(service.notices_pending()['notices'][0]['text'],icelandic['text'])
