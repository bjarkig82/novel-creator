import unittest
import os
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared
from tests.helpers import git
from novel_creator.cli import ToolError


class AuthorPrivacy(unittest.TestCase):
    def test_existing_global_author_identity_is_preserved_with_per_read_revocation(self):
        from novel_creator import retro
        from pathlib import Path
        for mode in ('global','local_precedence','revoke'):
            with self.subTest(mode=mode),fixtures() as (root,checkout,registry,fake,initial):
                revoke=mode=='revoke'
                service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                if mode!='local_precedence':
                    git(checkout,'config','--unset','user.name');git(checkout,'config','--unset','user.email')
                home=registry/'synthetic-home';home.mkdir()
                (home/'.gitconfig').write_text('[user]\n name = Configured Contributor\n email = configured@example.invalid\n',encoding='utf-8')
                global_before=(home/'.gitconfig').read_bytes();local_before=(checkout/'.git/config').read_bytes()
                original=retro.storage.git;reads=[]
                def inspect(path,*args,**kwargs):
                    result=original(path,*args,**kwargs)
                    if path==str(checkout) and args[:1]==('config',):
                        reads.append(args)
                        if revoke and args==('config','user.name'):service.disable()
                    return result
                with patch.dict(os.environ,{'HOME':str(home),'USERPROFILE':str(home),'XDG_CONFIG_HOME':str(home/'config')}),patch.object(retro.storage,'git',side_effect=inspect):
                    if revoke:
                        with self.assertRaises(ToolError):service.publish(run)
                    else:self.assertEqual(service.publish(run)['status'],'published')
                self.assertEqual(reads,[('config','user.name')] if revoke else [('config','user.name'),('config','user.email')])
                if revoke:
                    self.assertIsNone(service.run(run)['contribution']['commit'])
                    self.assertNotIn('push',fake.calls);self.assertNotIn('create',fake.calls)
                else:
                    part=service.run(run)['contribution']
                    identity=git(Path(part['worktree']),'show','-s','--format=%an <%ae>',part['commit'])
                    self.assertEqual(identity,'Disposable Test <test@example.invalid>' if mode=='local_precedence' else 'Configured Contributor <configured@example.invalid>')
                self.assertEqual((home/'.gitconfig').read_bytes(),global_before)
                self.assertEqual((checkout/'.git/config').read_bytes(),local_before)

    def test_private_author_metadata_blocks_before_commit_or_push(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            git(checkout,'config','user.name','password=synthetic_private_identity')
            with self.assertRaises(ToolError):service.publish(run)
            self.assertNotIn('push',fake.calls)
