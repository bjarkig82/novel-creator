import json
import unittest
from unittest.mock import patch
from novel_creator.cli import ToolError
from novel_creator.retro_github import Github, environment


class GithubTransport(unittest.TestCase):
    def test_transport_verification_revocation_prevents_fetch_and_push_launch(self):
        from novel_creator import retro_github
        for mutation in ('fetch','push'):
            with self.subTest(mutation=mutation):
                allowed=True;seen=[]
                def guard():
                    if not allowed:raise ToolError(3,'revoked')
                def command(argv,**kwargs):
                    nonlocal allowed
                    seen.append(argv)
                    if 'remote' in argv:return (retro_github.ORIGIN+'\n').encode()
                    if 'config' in argv:return b''
                    if 'ls-remote' in argv:
                        allowed=False
                        return (retro_github.ORIGIN+'\n').encode()
                    raise AssertionError('Network mutation launched')
                with patch.object(retro_github,'command',side_effect=command):
                    with self.assertRaises(ToolError):retro_github.git('synthetic-checkout',mutation,retro_github.ORIGIN,guard=guard)
                self.assertEqual(len(seen),3)
                self.assertFalse(any(mutation in argv for argv in seen))

    def test_create_persists_known_reference_before_metadata_read(self):
        observed=[]
        with patch('novel_creator.retro_github.command',return_value=b'https://github.com/bjarkig82/novel-creator/pull/12\n'),patch.object(Github,'get',side_effect=ToolError(5,'metadata unavailable')):
            with self.assertRaises(ToolError):Github().create('branch','main','Synthetic fix','Synthetic body',observed.append)
        self.assertEqual(observed,[{'number':12,'url':'https://github.com/bjarkig82/novel-creator/pull/12'}])

    def test_revoked_base_probe_does_not_fetch(self):
        allowed=True
        def guard():
            if not allowed:raise ToolError(3,'revoked')
        def response(endpoint):
            nonlocal allowed
            allowed=False
            return {'default_branch':'main'}
        github=Github();github.guard=guard
        with patch.object(github,'get',side_effect=response),patch('novel_creator.retro_github.git') as fetch:
            with self.assertRaises(ToolError):github.base('synthetic-checkout')
            self.assertFalse(any('fetch' in call.args for call in fetch.call_args_list))

    def test_readonly_identity_uses_fixed_get_endpoints(self):
        seen=[]
        def response(argv,**kwargs):
            seen.append(argv)
            return json.dumps({'login':'writer'} if argv[-1]=='user' else
                {'full_name':'bjarkig82/novel-creator','permissions':{'push':True}}).encode()
        with patch('novel_creator.retro_github.command',side_effect=response):
            self.assertEqual(Github().identity()['login'],'writer')
        self.assertTrue(all(a[:7]==['gh','api','--hostname','github.com','--method','GET',a[-1]] for a in seen))

    def test_repository_overrides_and_secret_propagation_are_limited(self):
        with patch.dict('os.environ',{'GH_REPO':'attacker/repo','GH_HOST':'attacker.invalid',
                        'GIT_SSH_COMMAND':'steal','GIT_CONFIG_COUNT':'1'}):
            env=environment()
        for key in ('GH_REPO','GH_HOST','GIT_SSH_COMMAND','GIT_CONFIG_COUNT'):
            self.assertNotIn(key,env)

    def test_push_denied_and_wrong_repo_cannot_enable(self):
        with patch.object(Github,'get',side_effect=[{'login':'writer'},
                  {'full_name':'attacker/repo','permissions':{'push':True}}]):
            with self.assertRaises(ToolError): Github().identity()
