import unittest
from unittest.mock import patch
from tests.retro_helpers import fixtures
from novel_creator.cli import ToolError


class Controls(unittest.TestCase):
    def test_real_common_directory_containing_novel_is_rejected(self):
        from tests.helpers import git,repository,envelope
        from novel_creator import storage
        from novel_creator.retro import Retro
        with fixtures() as (_,checkout,registry,fake,initial):
            common=checkout/'.git'
            linked=registry/'linked-checkout'
            git(checkout,'worktree','add','-b','linked-fixture',str(linked))
            with repository(parent=common) as root:
                storage.save(root,envelope(root))
                head=git(root,'rev-parse','HEAD');index=git(root,'ls-files','--stage')
                service=Retro(root,github=fake,registry=registry)
                with self.assertRaises(ToolError):service.enable(linked,authorize=True)
                self.assertEqual(fake.calls,[])
                self.assertIsNone(service.grant())
                self.assertFalse((common/'novel-creator-retro').exists())
                self.assertEqual(git(root,'rev-parse','HEAD'),head)
                self.assertEqual(git(root,'ls-files','--stage'),index)

    def test_linked_checkout_common_directory_cannot_overlap_novel(self):
        from tests.helpers import git
        from novel_creator.retro import Retro
        for contains_novel in (False, True):
            with self.subTest(contains_novel=contains_novel), fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry)
                head=git(root,'rev-parse','HEAD'); index=git(root,'ls-files','--stage')
                common=root.parent if contains_novel else root/'.novel-creator/local/framework.git'
                if not contains_novel:
                    git(checkout,'init','--separate-git-dir',str(common))
                original=__import__('novel_creator.storage',fromlist=['git']).git
                def resolve_common(path,*args,**kwargs):
                    if contains_novel and args==('rev-parse','--path-format=absolute','--git-common-dir'):
                        return str(common).encode()
                    return original(path,*args,**kwargs)
                with patch('novel_creator.retro.storage.git',side_effect=resolve_common):
                    with self.assertRaises(ToolError):service.enable(checkout,authorize=True)
                self.assertEqual(fake.calls,[])
                self.assertIsNone(service.grant())
                self.assertFalse((common/'novel-creator-retro').exists())
                self.assertEqual(git(root,'rev-parse','HEAD'),head)
                self.assertEqual(git(root,'ls-files','--stage'),index)

    def test_missing_machine_grant_is_disabled(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            for path in registry.glob('*.json'): path.unlink()
            fake.calls.clear()
            self.assertFalse(service.status()['enabled'])
            self.assertEqual(fake.calls,[])

    def test_partial_enable_stays_disabled(self):
        from novel_creator.retro import Retro
        from novel_creator import retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry)
            original=retro.write
            def fail_local(path,value,kind):
                if path.name=='authorization.json': raise OSError('synthetic interrupted local publication')
                return original(path,value,kind)
            with patch('novel_creator.retro.write',side_effect=fail_local):
                with self.assertRaises(OSError): service.enable(checkout,authorize=True)
            self.assertFalse(service.status()['enabled'])

    def test_unknown_fields_and_overlap_are_rejected(self):
        from novel_creator.retro import Retro,validate
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry)
            with self.assertRaises(ToolError): service.enable(root,authorize=True)
            with self.assertRaises(ToolError): validate({'outcome':'no_action','hidden_reasoning':'x'},'review')
