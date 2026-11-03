import unittest
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared


class ValidationResume(unittest.TestCase):
    def test_interrupted_local_validation_can_resume_same_prepared_finding(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            original=__import__('subprocess').run
            def interrupt_checks(argv,**kwargs):
                if '-c' in argv and argv[-1]=='print("synthetic check passed")':
                    raise KeyboardInterrupt('synthetic interrupted check')
                return original(argv,**kwargs)
            with patch('novel_creator.retro.subprocess.run',side_effect=interrupt_checks):
                with self.assertRaises(KeyboardInterrupt):service.validate_contribution(run,data)
            self.assertEqual(service.run(run)['status'],'validating')
            self.assertEqual(service.validate_contribution(run,data)['status'],'validated')
            self.assertNotIn('push',fake.calls)
