import unittest
from unittest.mock import patch
from tests.helpers import git
from tests.retro_helpers import fixtures
from tests.contract.test_retro_review import begin_input
from novel_creator.cli import ToolError


class Preservation(unittest.TestCase):
    def test_preparation_revocation_preserves_allocation_and_blocks_the_next_git_process(self):
        from novel_creator import retro
        from tests.retro_contribution_helpers import selected,ready_prepare
        for boundary in ('for-each-ref','worktree-add'):
            with self.subTest(boundary=boundary),fixtures() as (root,checkout,registry,fake,initial):
                service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run=selected(service,root,initial)
                if boundary=='for-each-ref':
                    original=retro.contribution_git
                    def fail(path,*args,**kwargs):
                        if args[:2]==('worktree','add'):raise OSError('before allocation mutation')
                        return original(path,*args,**kwargs)
                    with patch.object(retro,'contribution_git',side_effect=fail):
                        with self.assertRaises(OSError):ready_prepare(service,run)
                original=retro.contribution_git;later=[];revoked=False
                def revoke(path,*args,**kwargs):
                    nonlocal revoked
                    if revoked:later.append(args)
                    result=original(path,*args,**kwargs)
                    if (boundary=='for-each-ref' and args[0]=='for-each-ref') or (boundary=='worktree-add' and args[:2]==('worktree','add')):
                        service.disable();revoked=True
                    return result
                with patch.object(retro,'contribution_git',side_effect=revoke):
                    with self.assertRaises(ToolError):ready_prepare(service,run)
                before=service.run(run)
                self.assertTrue(revoked);self.assertEqual(later,[])
                service.enable(checkout,authorize=True);service.resume(run)
                self.assertEqual(service.prepare(run)['status'],'prepared')
                self.assertEqual(service.run(run)['contribution'],before['contribution'])

    def test_commit_result_is_retained_when_revocation_fences_the_next_process(self):
        from novel_creator import retro
        from tests.retro_contribution_helpers import prepared
        for boundary in ('commit-tree','update-ref'):
            with self.subTest(boundary=boundary),fixtures() as (root,checkout,registry,fake,initial):
                service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                original=retro.contribution_git;later=[];revoked=False;commit=[]
                def revoke(path,*args,**kwargs):
                    nonlocal revoked
                    if revoked:later.append(args)
                    result=original(path,*args,**kwargs)
                    if 'commit-tree' in args:commit.append(result.decode().strip())
                    if boundary in args:service.disable();revoked=True
                    return result
                fake.calls.clear()
                with patch.object(retro,'contribution_git',side_effect=revoke):
                    with self.assertRaises(ToolError):service.publish(run)
                self.assertTrue(revoked);self.assertEqual(later,[])
                self.assertEqual(service.run(run)['contribution']['commit'],commit[0])
                self.assertNotIn('push',fake.calls);self.assertNotIn('create',fake.calls)
                service.enable(checkout,authorize=True);service.resume(run)
                self.assertEqual(service.publish(run)['status'],'published')
                self.assertEqual(service.run(run)['contribution']['commit'],commit[0])
                self.assertEqual(fake.calls.count('push'),1);self.assertEqual(fake.calls.count('create'),1)

    def test_revocation_after_durable_check_intent_prevents_process_start(self):
        from novel_creator import retro
        from tests.retro_contribution_helpers import prepared
        with fixtures() as (root,checkout,registry,fake,initial):
            service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            original=service.save_run;revoked=False
            def revoke(item):
                nonlocal revoked
                original(item)
                if item['contribution'].get('diagnostics') and item['contribution']['diagnostics'][-1]['checks'] and not revoked:
                    service.disable();revoked=True
            original_process=retro.subprocess.run;launched=[]
            def process(argv,**kwargs):
                if argv==data['checks'][0]:launched.append(argv)
                return original_process(argv,**kwargs)
            with patch.object(service,'save_run',side_effect=revoke),patch.object(retro.subprocess,'run',side_effect=process):
                with self.assertRaises(ToolError):service.validate_contribution(run,data)
            self.assertTrue(revoked);self.assertEqual(launched,[])
            attempt=service.run(run)['contribution']['diagnostics'][-1]
            self.assertNotEqual(attempt['state'],'passed')
            self.assertIsNone(attempt['checks'][0]['exit_code'])
            service.enable(checkout,authorize=True);service.resume(run)
            self.assertEqual(service.validate_contribution(run,data)['status'],'validated')

    def test_revocation_after_add_fences_validate_publish_and_push_reassessment(self):
        from novel_creator import retro
        from tests.retro_contribution_helpers import prepared
        for action in ('validate','publish','compare'):
            with self.subTest(action=action),fixtures() as (root,checkout,registry,fake,initial):
                service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial)
                if action!='validate':service.validate_contribution(run,data)
                if action=='compare':
                    def interrupted(*args):raise OSError('push interrupted')
                    with patch.object(fake,'push',side_effect=interrupted):
                        with self.assertRaises(ToolError):service.publish(run)
                original=retro.contribution_git;seen=[];revoked=False
                head=git(root,'rev-parse','HEAD');index=git(checkout,'ls-files','--stage')
                before=service.run(run)
                def revoke_after_add(path,*args,**kwargs):
                    nonlocal revoked
                    seen.append(args)
                    result=original(path,*args,**kwargs)
                    if args[:2]==('add','--all'):
                        service.disable();revoked=True
                    return result
                fake.calls.clear()
                with patch.object(retro,'contribution_git',side_effect=revoke_after_add):
                    with self.assertRaises(ToolError):
                        if action=='validate':service.validate_contribution(run,data)
                        elif action=='publish':service.publish(run)
                        else:service.compare(run,{'snapshot':'0'*64,'equivalent_pr':None,
                                                  'upstream_fix_present':False,'public_scope_reviewed':True})
                self.assertTrue(revoked)
                self.assertFalse(any(args[0]=='write-tree' for args in seen))
                self.assertNotIn('push',fake.calls);self.assertNotIn('create',fake.calls)
                self.assertEqual(service.run(run)['contribution'],before['contribution'])
                self.assertEqual(git(root,'rev-parse','HEAD'),head)
                self.assertEqual(git(checkout,'ls-files','--stage'),index)
                service.enable(checkout,authorize=True);service.resume(run)
                if action=='validate':self.assertEqual(service.validate_contribution(run,data)['status'],'validated')
                else:self.assertEqual(service.publish(run)['status'],'published')

    def test_persisted_overlapping_binding_blocks_all_contribution_recovery(self):
        from novel_creator.retro import Retro,write
        from tests.retro_contribution_helpers import prepared
        for common_kind in ('inside','ancestor'):
            with self.subTest(common_kind=common_kind), fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial)
                item=service.run(run); head=git(root,'rev-parse','HEAD');index=git(checkout,'ls-files','--stage')
                common=root/'.novel-creator/local/invalid-framework' if common_kind=='inside' else root.parent
                grant=service.grant();grant['git_common_dir']=str(common)
                write(service.path('authorization.json'),grant,'authorization')
                write(registry/(grant['grant_id']+'.json'),grant,'authorization')
                item['bindings']['git_common_dir']=str(common);service.save_run(item)
                fake.calls.clear()
                with patch('novel_creator.retro.contribution_git',side_effect=AssertionError('framework Git accessed')):
                    for action in (lambda:service.prepare(run),lambda:service.worktree(item),
                                   lambda:service.resume(run),lambda:service.release(run),
                                   lambda:service.inspect_dead_lock(item,grant)):
                        with self.assertRaises(ToolError):action()
                self.assertEqual(fake.calls,[])
                self.assertFalse((common/'novel-creator-retro').exists())
                self.assertEqual(git(root,'rev-parse','HEAD'),head)
                self.assertEqual(git(checkout,'ls-files','--stage'),index)
                service.disable();self.assertFalse(service.status()['enabled'])

    def test_retro_does_not_touch_staged_user_changes(self):
        from novel_creator.retro import Retro
        with fixtures() as (root, checkout, registry, fake, initial):
            (checkout / 'unrelated.txt').write_text('untouched')
            git(checkout,'add','unrelated.txt')
            index = git(checkout,'ls-files','--stage')
            head = git(root,'rev-parse','HEAD')
            service=Retro(root,github=fake,registry=registry)
            service.enable(checkout,authorize=True)
            service.begin(begin_input(root, initial))
            self.assertEqual(git(checkout,'ls-files','--stage'),index)
            self.assertEqual(git(root,'rev-parse','HEAD'),head)

    def test_pending_save_blocks_review(self):
        from novel_creator.retro import Retro
        from novel_creator import storage
        from tests.helpers import envelope, FailAt
        with fixtures() as (root, checkout, registry, fake, initial):
            service=Retro(root,github=fake,registry=registry)
            service.enable(checkout,authorize=True)
            payload=envelope(root,previous=initial)
            # A genuine pending receipt, not forged state.
            with self.assertRaises(ToolError):
                storage.save(root,payload,fault=FailAt('before_file'))
            with self.assertRaises(ToolError): service.begin(begin_input(root, initial))
