import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.retro_helpers import fixtures
from novel_creator.cli import ToolError


class Authorization(unittest.TestCase):
    def test_bound_opt_in_disable_and_no_disabled_transport(self):
        from novel_creator.retro import Retro
        with fixtures() as (root, checkout, registry, fake, initial):
            service = Retro(root, github=fake, registry=registry)
            self.assertFalse(service.status()['enabled'])
            self.assertEqual(fake.calls, [])
            with self.assertRaises(ToolError):
                service.enable(checkout, authorize=False)
            service.enable(checkout, authorize=True)
            self.assertTrue(service.status()['enabled'])
            service.disable()
            fake.calls.clear()
            self.assertFalse(service.status()['enabled'])
            self.assertEqual(fake.calls, [])
            with self.assertRaises(ToolError):
                service.resume('00000000-0000-4000-8000-000000000001')
            self.assertEqual(fake.calls, [])

    def test_copied_root_does_not_enable(self):
        from novel_creator.retro import Retro
        with fixtures() as (root, checkout, registry, fake, initial), tempfile.TemporaryDirectory() as tmp:
            service = Retro(root, github=fake, registry=registry)
            service.enable(checkout, authorize=True)
            copied = Path(tmp).resolve() / 'copy'
            shutil.copytree(root, copied)
            self.assertFalse(Retro(copied, github=fake, registry=registry).status()['enabled'])

    def test_unknown_state_fails_closed(self):
        from novel_creator.retro import Retro
        with fixtures() as (root, checkout, registry, fake, initial):
            service = Retro(root, github=fake, registry=registry)
            service.enable(checkout, authorize=True)
            path = root / '.novel-creator/local/retro/authorization.json'
            path.write_text('{"retro_version":99}')
            with self.assertRaises(ToolError):
                service.status()
