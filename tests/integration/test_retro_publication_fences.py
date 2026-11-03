import sys
import unittest
from unittest.mock import patch
from pathlib import Path
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared
from novel_creator.cli import ToolError


class PublicationFences(unittest.TestCase):
    def test_abandoned_validation_cannot_be_published(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            service.release(run)
            with self.assertRaises(ToolError):service.publish(run)
            self.assertNotIn('push',fake.calls)

    def test_network_intent_freezes_validation_and_intended_commit(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            with patch.object(fake,'push',side_effect=OSError('uncertain push')):
                with self.assertRaises((OSError,ToolError)):service.publish(run)
            service.block(service.run(run),'push_outcome_unknown')
            old=service.run(run)['contribution']['commit']
            (Path(service.run(run)['contribution']['worktree'])/'synthetic_fix.txt').write_text('new correction after push intent')
            with self.assertRaises(ToolError):service.validate_contribution(run,data)
            self.assertEqual(service.run(run)['contribution']['commit'],old)
            self.assertNotIn('create',fake.calls)
