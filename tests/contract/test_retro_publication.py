import unittest
from unittest.mock import patch
from pathlib import Path
from tests.helpers import git
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared
from novel_creator.cli import ToolError


class Publication(unittest.TestCase):
    def test_observed_nonconforming_pr_is_durable_and_can_be_inspected_abandoned(self):
        from novel_creator.retro import Retro
        for changes in ({'draft':False},{'state':'closed'},{'head':'unexpected-head'},{'base':'unexpected-base'}):
            with self.subTest(changes=changes), fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                original=fake.create
                def changed(*args):
                    pr=original(*args);pr.update(changes);return pr
                with patch.object(fake,'create',side_effect=changed):
                    with self.assertRaises(ToolError):service.publish(run)
                restarted=Retro(root,github=fake,registry=registry)
                outcome=restarted.status(run)['latest_run']
                self.assertEqual(outcome['remote_outcome'],'observed')
                self.assertEqual(outcome['pr']['url'],fake.pulls[0]['url'])
                with self.assertRaises(ToolError):restarted.publish(run)
                self.assertEqual(restarted.release(run)['status'],'abandoned')
                self.assertEqual(fake.calls.count('create'),1)

    def test_prepared_checked_draft_preserves_checkout(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            before=git(checkout,'rev-parse','HEAD')
            service=Retro(root,github=fake,registry=registry); service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            service.validate_contribution(run,data)
            result=service.publish(run)
            self.assertEqual(result['status'],'published')
            self.assertTrue(fake.pulls[0]['draft'])
            self.assertEqual(fake.calls.count('create'),1)
            self.assertEqual(git(checkout,'rev-parse','HEAD'),before)
            self.assertEqual(service.publish(run)['status'],'published')
            self.assertEqual(fake.calls.count('create'),1)

    def test_tree_change_invalidates_validation(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry); service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial); service.validate_contribution(run,data)
            (Path(service.run(run)['contribution']['worktree'])/'synthetic_fix.txt').write_text('changed after check')
            with self.assertRaises(ToolError): service.publish(run)
            self.assertNotIn('push',fake.calls)
