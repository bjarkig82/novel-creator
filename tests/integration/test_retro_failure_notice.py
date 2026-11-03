import argparse
import unittest
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import selected
from novel_creator.cli import ToolError
from tests.contract.test_retro_review import begin_input


class FailureNotice(unittest.TestCase):
    def test_host_command_failure_queues_local_notice_without_leaking_error(self):
        from novel_creator.retro import Retro,dispatch,load,write
        from pathlib import Path
        from tests.helpers import uid
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=selected(service,root,initial);fake.allowed=False
            args=argparse.Namespace(novel=str(root),action='prepare',run=run)
            with patch('novel_creator.retro.Retro',return_value=service):
                with self.assertRaises(ToolError):dispatch(args)
            notes=service.notices_pending()['notices']
            self.assertEqual(len(notes),1)
            self.assertNotIn(str(root),notes[0]['text'])
            self.assertNotIn('push',fake.calls)
            before=service.run(run)
            fake.allowed=True
            restarted=Retro(root,github=fake,registry=registry)
            owner_path=Path(service.grant()['git_common_dir'])/'novel-creator-retro/owner.json'
            owner=load(owner_path,'owner')
            write(owner_path,dict(owner,run_id=uid()),'owner')
            with self.assertRaises(ToolError):restarted.resume(run)
            self.assertEqual(restarted.run(run),before)
            write(owner_path,owner,'owner')
            restarted.disable();fake.calls.clear()
            with patch('novel_creator.retro.contribution_git',side_effect=AssertionError('disabled framework access')):
                with self.assertRaises(ToolError):restarted.resume(run)
            self.assertEqual(fake.calls,[])
            restarted.enable(checkout,authorize=True)
            self.assertEqual(restarted.resume(run)['next_operation'],'prepare')
            from tests.retro_contribution_helpers import ready_prepare
            self.assertEqual(ready_prepare(restarted,run)['status'],'prepared')
            self.assertEqual(restarted.run(run)['finding'],before['finding'])
            self.assertFalse(restarted.begin(begin_input(root,initial))['review_required'])
