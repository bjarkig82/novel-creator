import hashlib,json,subprocess,unittest
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared
from tests.helpers import git
from novel_creator.cli import ToolError


class Diagnostics(unittest.TestCase):
    def test_unicode_failed_checks_retain_tree_bound_private_logs(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            raw='Þóra private diagnostic token=synthetic-secret\n'.encode()
            data['checks'][0][-1]=f'import sys;sys.stdout.buffer.write({raw!r});sys.stderr.buffer.write(b"check failed");sys.exit(1)'
            with self.assertRaises(ToolError):service.validate_contribution(run,data)
            attempt=service.run(run)['contribution']['diagnostics'][-1]
            self.assertEqual(attempt['state'],'failed');self.assertTrue(attempt['tree'])
            result=attempt['checks'][0];log=service.path(result['stdout']['path'])
            self.assertEqual(log.read_bytes(),raw)
            self.assertEqual(result['stdout']['digest'],hashlib.sha256(raw).hexdigest())
            self.assertEqual(result['exit_code'],1)
            self.assertTrue(git(root,'check-ignore',str(log)))
            summary=json.dumps(service.status(run))
            self.assertNotIn('synthetic-secret',summary);self.assertNotIn(str(root),summary)
            # A later passing attempt retains the failure, and no logs enter the PR.
            data['checks'][0][-1]=f'import sys;sys.stdout.buffer.write({raw!r})'
            service.validate_contribution(run,data);service.publish(run)
            self.assertEqual(len(service.run(run)['contribution']['diagnostics']),2)
            public=json.dumps(fake.pulls)
            self.assertNotIn('synthetic-secret',public);self.assertNotIn(str(log),public)

    def test_unavailable_timeout_and_interruption_preserve_diagnostics(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            original=subprocess.run
            for error,state in [(OSError('synthetic missing executable'),'unavailable'),
                                (subprocess.TimeoutExpired(data['checks'][0],300),'interrupted'),
                                (KeyboardInterrupt(),'interrupted')]:
                def fail(argv,**kwargs):
                    if argv==data['checks'][0]:
                        kwargs['stdout'].write(b'partial private output');kwargs['stdout'].flush()
                        raise error
                    return original(argv,**kwargs)
                with self.subTest(state=state),patch('novel_creator.retro.subprocess.run',side_effect=fail):
                    with self.assertRaises((ToolError,KeyboardInterrupt)):service.validate_contribution(run,data)
                attempt=service.run(run)['contribution']['diagnostics'][-1]
                self.assertEqual(attempt['state'],state)
                result=attempt['checks'][0]
                self.assertIsNone(result['exit_code'])
                self.assertEqual(service.path(result['stdout']['path']).read_bytes(),b'partial private output')
            self.assertNotIn('push',fake.calls)
