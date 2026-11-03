import unittest
from tests.helpers import git
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import selected
from novel_creator.cli import ToolError


class TransportMutation(unittest.TestCase):
    def test_changed_rewrite_after_enable_blocks_before_any_remote_probe(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=selected(service,root,initial)
            git(checkout,'config','url.https://attacker.invalid/.insteadOf','https://github.com/')
            fake.calls.clear()
            with self.assertRaises(ToolError):service.prepare(run)
            self.assertEqual(fake.calls,[])
