import unittest
from pathlib import Path
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared,selected,ready_prepare
from novel_creator.cli import ToolError
from tests.helpers import git


class Journey(unittest.TestCase):
    def test_failed_check_blocks_publication_and_queues_problem(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            data['checks'][0][-1]='raise SystemExit(1)'
            with self.assertRaises(ToolError): service.validate_contribution(run,data)
            with self.assertRaises(ToolError): service.publish(run)
            self.assertNotIn('push',fake.calls)
            self.assertEqual(len(service.notices_pending()['notices']),1)

    def test_repository_owner_blocks_second_run_and_release_preserves_worktree(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            first,data=prepared(service,root,initial)
            worktree=service.run(first)['contribution']['worktree']
            second=selected(service,root,initial,turn='task-2')
            with self.assertRaises(ToolError):service.prepare(second)
            service.release(first)
            self.assertTrue(Path(worktree).exists())
            self.assertEqual(ready_prepare(service,second)['status'],'prepared')

    def test_existing_generalized_finding_prevents_duplicate_contribution(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data);service.publish(run)
            second=selected(service,root,initial,turn='task-2')
            target=service.prepare(second)
            self.assertEqual(target['status'],'comparison_required')
            from tests.integration.test_retro_comparison import assessment
            self.assertEqual(service.compare(second,assessment(target,1))['status'],'duplicate')
            self.assertEqual(fake.calls.count('create'),1)
