import json
import os
import sys
import unittest
from unittest.mock import patch
from novel_creator.cli import ToolError
from novel_creator.retro_github import Github, command


class GithubTransport(unittest.TestCase):
    def child_environment(self, settings, names=None):
        names = list(settings if names is None else names)
        script = ('import json, os; print(json.dumps('
                  '{name: os.environ.get(name) for name in ' + repr(names) + '}))')
        # Keep only platform executable support; no real credentials or network
        # settings enter the fixture process.
        platform = {key: os.environ[key] for key in ('SYSTEMROOT', 'WINDIR')
                    if key in os.environ}
        with patch.dict('os.environ', {**platform, **settings}, clear=True):
            return json.loads(command([sys.executable, '-c', script]))

    def test_transport_subprocess_preserves_host_proxy_settings(self):
        uppercase = {
            'HTTP_PROXY': 'proxy.example.test:8080',
            'HTTPS_PROXY': 'proxy.example.test:8443',
            'ALL_PROXY': 'proxy.example.test:1080',
            'NO_PROXY': 'localhost,example.test',
        }
        lowercase = {
            'http_proxy': 'lowercase.example.test:8080',
            'https_proxy': 'lowercase.example.test:8443',
            'all_proxy': 'lowercase.example.test:1080',
            'no_proxy': 'localhost,lowercase.example.test',
        }
        cases = [uppercase, lowercase]
        if os.name != 'nt':
            cases.append({**uppercase, **lowercase})
        for settings in cases:
            with self.subTest(settings=settings):
                self.assertEqual(self.child_environment(settings), settings)

    def test_transport_subprocess_preserves_host_certificate_settings(self):
        settings = {
            'SSL_CERT_FILE': 'synthetic-ca.pem',
            'SSL_CERT_DIR': 'synthetic-certificates',
            'REQUESTS_CA_BUNDLE': 'synthetic-requests-ca.pem',
            'CURL_CA_BUNDLE': 'synthetic-curl-ca.pem',
            'GIT_SSL_CAINFO': 'synthetic-git-ca.pem',
            'GIT_SSL_CAPATH': 'synthetic-git-certificates',
        }
        self.assertEqual(self.child_environment(settings), settings)

    def test_missing_network_settings_are_not_invented(self):
        names = ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
                 'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy',
                 'SSL_CERT_FILE', 'SSL_CERT_DIR', 'REQUESTS_CA_BUNDLE',
                 'CURL_CA_BUNDLE', 'GIT_SSL_CAINFO', 'GIT_SSL_CAPATH']
        self.assertEqual(self.child_environment({}, names), dict.fromkeys(names))

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
        settings = {
            'GH_REPO': 'synthetic/other', 'GH_HOST': 'synthetic.invalid',
            'GH_CONFIG_DIR': 'synthetic-config',
            'GH_ENTERPRISE_TOKEN': 'synthetic-enterprise-token',
            'GITHUB_ENTERPRISE_TOKEN': 'synthetic-enterprise-token',
            'GIT_DIR': 'synthetic.git', 'GIT_WORK_TREE': 'synthetic-worktree',
            'GIT_COMMON_DIR': 'synthetic-common', 'GIT_INDEX_FILE': 'synthetic-index',
            'GIT_OBJECT_DIRECTORY': 'synthetic-objects',
            'GIT_ALTERNATE_OBJECT_DIRECTORIES': 'synthetic-alternate',
            'GIT_SSH': 'synthetic-ssh', 'GIT_SSH_COMMAND': 'synthetic-ssh-command',
            'GIT_PROXY_COMMAND': 'synthetic-proxy-command',
            'GIT_CONFIG': 'synthetic-config', 'GIT_CONFIG_SYSTEM': 'synthetic-system',
            'GIT_CONFIG_PARAMETERS': "'http.sslVerify=false'",
            'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'http.sslVerify',
            'GIT_CONFIG_VALUE_0': 'false', 'GIT_SSL_NO_VERIFY': '1',
            'GIT_ASKPASS': 'synthetic-askpass', 'SSH_ASKPASS': 'synthetic-askpass',
            'UNRELATED_SECRET': 'synthetic-private-value',
        }
        self.assertEqual(self.child_environment(settings), dict.fromkeys(settings))

    def test_transport_pins_noninteractive_and_isolated_git_config(self):
        settings = {'GIT_TERMINAL_PROMPT': '1', 'GH_PROMPT_DISABLED': '0',
                    'GIT_CONFIG_NOSYSTEM': '0', 'GIT_CONFIG_GLOBAL': 'synthetic-global'}
        self.assertEqual(self.child_environment(settings), {
            'GIT_TERMINAL_PROMPT': '0', 'GH_PROMPT_DISABLED': '1',
            'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
        })

    def test_push_denied_and_wrong_repo_cannot_enable(self):
        with patch.object(Github,'get',side_effect=[{'login':'writer'},
                  {'full_name':'attacker/repo','permissions':{'push':True}}]):
            with self.assertRaises(ToolError): Github().identity()
