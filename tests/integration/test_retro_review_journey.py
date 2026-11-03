import unittest
from tests.retro_helpers import fixtures
from tests.contract.test_retro_review import begin_input


class ReviewJourney(unittest.TestCase):
    def test_unicode_findings_and_orphan_claim_recovery(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            first=service.begin(begin_input(root,initial))
            service.path('index.json').unlink() # Simulate run saved before index publication.
            second=service.begin(begin_input(root,initial))
            self.assertEqual(first['run_id'],second['run_id'])
            self.assertFalse(second['review_required'])
            service.review(first['run_id'],{'outcome':'selected','category':'documentation',
                'problem':'Leiðbeiningar vantar fyrir tilbúið dæmi.',
                'reproduction':'Búðu til tómt safn í tilbúnu prófi.',
                'evidence_refs':[initial['exchange_id']]})
            self.assertEqual(service.run(first['run_id'])['status'],'selected')
            self.assertEqual(fake.calls,['identity'])
