import unittest
from novel_creator.cli import ToolError
from tests.helpers import git, uid
from tests.retro_helpers import fixtures


def begin_input(root, exchange, turn='task-1'):
    return {'host_kind':'codex', 'thread_id':'synthetic-thread', 'initiating_turn_id':turn,
            'completion_exchange_id':exchange['exchange_id'], 'checkpoint':git(root, 'rev-parse','HEAD')}


class Review(unittest.TestCase):
    def test_claim_once_and_no_action(self):
        from novel_creator.retro import Retro
        with fixtures() as (root, checkout, registry, fake, initial):
            service = Retro(root, github=fake, registry=registry)
            self.assertFalse(service.begin(begin_input(root, initial))['eligible'])
            service.enable(checkout, authorize=True)
            first = service.begin(begin_input(root, initial))
            self.assertTrue(first['review_required'])
            duplicate = service.begin(begin_input(root, initial))
            self.assertFalse(duplicate['review_required'])
            self.assertEqual(first['run_id'], duplicate['run_id'])
            service.review(first['run_id'], {'outcome':'no_action'})
            self.assertEqual(service.run(first['run_id'])['status'], 'no_action')
            with self.assertRaises(ToolError):
                service.review(first['run_id'], {'outcome':'selected','category':'runtime','problem':'x','reproduction':'x','evidence_refs':[initial['exchange_id']]})

    def test_reject_unknown_evidence_and_missing_identity(self):
        from novel_creator.retro import Retro
        with fixtures() as (root, checkout, registry, fake, initial):
            service = Retro(root, github=fake, registry=registry)
            service.enable(checkout, authorize=True)
            data = begin_input(root, initial)
            data['initiating_turn_id'] = ''
            with self.assertRaises(ToolError): service.begin(data)
            run = service.begin(begin_input(root, initial))['run_id']
            with self.assertRaises(ToolError):
                service.review(run, {'outcome':'selected','category':'runtime','problem':'synthetic failure','reproduction':'synthetic fixture','evidence_refs':[uid()]})
