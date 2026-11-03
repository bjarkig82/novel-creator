import unittest
import argparse
from contextlib import contextmanager
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared
from novel_creator.cli import ToolError


class Recovery(unittest.TestCase):
    def test_terminal_replace_failure_retains_observation_and_dispatch_recovery(self):
        """Deny exactly the terminal replace, not a high-level save or PR request."""
        import ctypes
        import json
        import os
        from pathlib import Path
        from novel_creator import retro, storage
        from tests.helpers import envelope, git
        Retro=retro.Retro

        with fixtures() as (root,checkout,registry,fake,initial):
            writing=envelope(root,previous=initial)
            storage.save(root,writing)
            (checkout/'unrelated.txt').write_bytes(b'staged unrelated work\n')
            git(checkout,'add','unrelated.txt')
            (checkout/'unrelated.txt').write_bytes(b'unstaged unrelated work\n')
            service=Retro(root,github=fake,registry=registry)
            service.enable(checkout,authorize=True)
            run,data=prepared(service,root,writing)
            receipt=service.path('runs/'+run+'.json')
            owner=Path(service.grant()['git_common_dir'])/'novel-creator-retro/owner.json'
            owner_before=owner.read_bytes()
            worktree=Path(service.run(run)['contribution']['worktree'])
            fix_before=(worktree/'synthetic_fix.txt').read_bytes()

            def preserved():
                return (git(root,'rev-parse','HEAD'),git(root,'ls-files','--stage'),
                        {name:(root/name).read_bytes() for name in git(root,'ls-files').splitlines()},
                        storage.read_history(root),git(checkout,'rev-parse','HEAD'),
                        git(checkout,'ls-files','--stage'),(checkout/'unrelated.txt').read_bytes())

            before=preserved()
            replace=storage.os.replace
            failed=[];replaced=[];latest=[];calls=[]
            original=service.repository_operation
            published_notice=[]

            def deny_terminal(source,target):
                if Path(target)!=receipt:
                    return replace(source,target)
                candidate=json.loads(Path(source).read_bytes())
                if candidate['status']!='published' or failed:
                    result=replace(source,target);replaced.append(candidate['status']);return result
                durable=service.run(run)
                self.assertEqual(durable['contribution']['stage'],'remote_observed')
                self.assertEqual(durable['remote_outcome'],{'kind':'observed','pr':fake.pulls[0]})
                self.assertEqual(owner.read_bytes(),owner_before)
                note=candidate['notice']
                note_path=service.path('notices/'+note['notice_id']+'.json')
                self.assertEqual(json.loads(note_path.read_bytes()),note)
                published_notice.append((note_path,note_path.read_bytes()))
                failed.append(Path(source))
                if os.name!='nt':
                    raise PermissionError(13,'Synthetic terminal replacement denial')
                # A known deny-delete handle is an injected control, not a claim
                # about which process caused the unexplained cycle3 WinError5.
                kernel=ctypes.WinDLL('kernel32',use_last_error=True)
                create=kernel.CreateFileW
                create.argtypes=[ctypes.c_wchar_p,ctypes.c_uint32,ctypes.c_uint32,
                                 ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_void_p]
                create.restype=ctypes.c_void_p
                close=kernel.CloseHandle
                close.argtypes=[ctypes.c_void_p];close.restype=ctypes.c_int
                # Exclusive access to the prepared file proves its writer has
                # closed before os.replace. Release this probe before replacement.
                probe=create(str(source),0x80000000,0,None,3,0x80,None)
                self.assertNotEqual(probe,ctypes.c_void_p(-1).value)
                self.assertTrue(close(probe))
                held=create(str(target),0x80000000,3,None,3,0x80,None)
                self.assertNotEqual(held,ctypes.c_void_p(-1).value)
                try:
                    with self.assertRaises(PermissionError) as denied:
                        replace(source,target)
                    self.assertIn(denied.exception.winerror,(5,32))
                    print('Injected deny-delete handle: WinError'+str(denied.exception.winerror),flush=True)
                    raise denied.exception
                finally:
                    self.assertTrue(close(held))

            @contextmanager
            def delayed(item,**kwargs):
                with patch.object(service,'repository_operation',original):
                    service.validate_contribution(run,data)
                    args=argparse.Namespace(novel=str(root),action='publish',run=run)
                    with patch.object(storage.os,'replace',side_effect=deny_terminal):
                        with patch.object(retro,'Retro',return_value=service):
                            with self.assertRaises(PermissionError):retro.dispatch(args)
                    self.assertEqual(len(failed),1)
                    self.assertFalse(failed[0].exists())
                    self.assertEqual(list(receipt.parent.glob('prepare-*')),[])
                    self.assertIn('blocked',replaced)  # Actual dispatch journal replaced the receipt.
                    durable=service.run(run)
                    self.assertEqual(durable['status'],'blocked')
                    self.assertEqual(durable['reason_code'],'operation_unavailable')
                    self.assertEqual(durable['remote_outcome'],{'kind':'observed','pr':fake.pulls[0]})
                    self.assertEqual(durable['contribution']['stage'],'remote_observed')
                    self.assertEqual(durable['contribution']['commit'],fake.refs[durable['contribution']['branch']])
                    self.assertEqual(owner.read_bytes(),owner_before)
                    self.assertEqual(preserved(),before)
                    restarted=Retro(root,github=fake,registry=registry)
                    self.assertEqual(restarted.status(run)['latest_run']['pr']['number'],1)
                    self.assertEqual(restarted.resume(run)['status'],'published')
                    latest.append(restarted.run(run));calls.extend(fake.calls)
                    self.assertFalse(owner.exists())
                    self.assertEqual(latest[0]['remote_outcome'],{'kind':'verified','pr':fake.pulls[0]})
                    self.assertEqual(latest[0]['notice']['notice_id'],json.loads(published_notice[0][1])['notice_id'])
                    self.assertEqual(published_notice[0][0].read_bytes(),published_notice[0][1])
                    self.assertEqual(len(restarted.notice_items()),2)  # Published plus sanitized problem.
                with original(item,**kwargs) as operation:yield operation

            args=argparse.Namespace(novel=str(root),action='prepare',run=run)
            with patch.object(service,'repository_operation',delayed):
                with patch.object(retro,'Retro',return_value=service):
                    with self.assertRaisesRegex(retro.StaleRunError,'Retrospective state changed'):
                        retro.dispatch(args)
            restarted=Retro(root,github=fake,registry=registry)
            self.assertEqual(restarted.run(run),latest[0])
            self.assertEqual(fake.calls,calls)
            self.assertEqual(preserved(),before)
            self.assertEqual((worktree/'synthetic_fix.txt').read_bytes(),fix_before)
            self.assertEqual(restarted.resume(run)['status'],'published')
            self.assertEqual(fake.calls.count('push'),1);self.assertEqual(fake.calls.count('create'),1)

    def test_completed_push_survives_revocation_without_following_request(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            original=fake.push;after=[]
            def revoke(*args):
                result=original(*args);service.disable();after.extend(fake.calls);return result
            with patch.object(fake,'push',side_effect=revoke):
                with self.assertRaises(ToolError):service.publish(run)
            item=service.run(run);part=item['contribution']
            self.assertEqual(fake.calls,after);self.assertEqual(fake.refs[part['branch']],part['commit'])
            self.assertEqual(part['stage'],'push_intent');self.assertNotIn('create',fake.calls)
            with self.assertRaises(ToolError):service.resume(run)
            self.assertEqual(fake.calls,after)
            service.enable(checkout,authorize=True);service.resume(run)
            self.assertEqual(service.publish(run)['status'],'published')
            self.assertEqual(fake.calls.count('push'),1);self.assertEqual(fake.calls.count('create'),1)

    def test_known_created_result_survives_revocation_without_recreation(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            original=fake.create
            def revoke(*args):
                result=original(*args);service.disable();return result
            with patch.object(fake,'create',side_effect=revoke):
                with self.assertRaises(ToolError):service.publish(run)
            item=service.run(run)
            self.assertEqual(item['remote_outcome']['pr']['number'],1)
            self.assertEqual(item['status'],'published')
            before=list(fake.calls)
            with self.assertRaises(ToolError):service.resume(run)
            self.assertEqual(fake.calls,before)
            service.enable(checkout,authorize=True);self.assertEqual(service.resume(run)['status'],'published')
            self.assertEqual(fake.calls.count('create'),1)

    def test_delayed_generation_adoption_does_not_replace_completed_publication(self):
        from novel_creator import retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            service.disable();service.enable(checkout,authorize=True)
            original=retro.lock;latest=[]
            @contextmanager
            def delayed(path,**kwargs):
                if path.name in (run+'.lock','operation.lock') and not latest:
                    with patch.object(retro,'lock',original):
                        service.resume(run);service.publish(run)
                        latest.append(service.run(run))
                with original(path,**kwargs):yield
            with patch.object(retro,'lock',delayed):
                with self.assertRaisesRegex(ToolError,'Retrospective state changed'):service.resume(run)
            self.assertEqual(retro.Retro(root,github=fake,registry=registry).run(run),latest[0])
            self.assertEqual(service.resume(run)['status'],'published')
            self.assertEqual(fake.calls.count('push'),1);self.assertEqual(fake.calls.count('create'),1)

    def test_delayed_contribution_commands_reject_changed_receipt_before_effects(self):
        from novel_creator.retro import Retro
        for command in ('prepare','validate','publish','resume','release'):
            with self.subTest(command=command),fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial)
                if command!='prepare':service.validate_contribution(run,data)
                original=service.repository_operation;latest=[];calls=[]
                @contextmanager
                def delayed(item,**kwargs):
                    with patch.object(service,'repository_operation',original):
                        if command=='prepare':service.validate_contribution(run,data)
                        service.publish(run)
                        latest.append(service.run(run))
                        calls.extend(fake.calls)
                    with original(item,**kwargs) as operation:yield operation
                action=(lambda:service.validate_contribution(run,data)) if command=='validate' else (lambda:getattr(service,command)(run))
                with patch.object(service,'repository_operation',delayed):
                    with self.assertRaisesRegex(ToolError,'Retrospective state changed'):action()
                restarted=Retro(root,github=fake,registry=registry)
                self.assertEqual(restarted.run(run),latest[0])
                self.assertEqual(fake.calls,calls)
                self.assertEqual(restarted.resume(run)['status'],'published')
                self.assertEqual(fake.calls.count('push'),1)
                self.assertEqual(fake.calls.count('create'),1)

    def test_failure_journal_does_not_write_during_a_repository_operation(self):
        from novel_creator.retro import Retro,dispatch
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            original=fake.create;observed=[]
            def create(branch,base,title,body,observe):
                result=original(branch,base,title,body,observe)
                before=service.run(run)
                args=argparse.Namespace(novel=str(root),action='publish',run=run)
                with patch('novel_creator.retro.Retro',return_value=service),patch('novel_creator.retro._dispatch',side_effect=ToolError(6,'synthetic competing failure')):
                    with self.assertRaises(ToolError):dispatch(args)
                observed.append((before,service.run(run)))
                return result
            with patch.object(fake,'create',side_effect=create):
                self.assertEqual(service.publish(run)['status'],'published')
            self.assertEqual(observed[0][0],observed[0][1])
            self.assertEqual(len(service.notice_items()),1)
            self.assertEqual(service.resume(run)['status'],'published')
            self.assertEqual(fake.calls.count('push'),1);self.assertEqual(fake.calls.count('create'),1)

    def test_comparison_recovery_keeps_uncertain_create_blocked(self):
        from novel_creator.retro import Retro
        from tests.integration.test_retro_comparison import public_pr,assessment
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            with patch.object(fake,'create',side_effect=OSError('synthetic uncertain creation')):
                with self.assertRaises(ToolError):service.publish(run)
            fake.pulls=[public_pr()]
            item=service.run(run)
            upstream,candidates,snapshot=service.comparison_scope(item,service.require(item))
            target=service.comparison_request(item,upstream,candidates,snapshot)
            for action in (lambda:service.compare(run,assessment(target,8)),lambda:service.resume(run)):
                with self.assertRaises(ToolError):action()
            self.assertEqual(service.run(run)['contribution']['stage'],'publication_unknown')
            self.assertEqual(len(fake.pulls),1)

    def test_push_comparison_recovery_rejects_changed_remote_base_and_revocation(self):
        from novel_creator.retro import Retro
        from tests.integration.test_retro_comparison import public_pr,assessment
        for changed in ('remote','base','authorization'):
            with self.subTest(changed=changed),fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                original=fake.push
                def interrupted(*args):
                    original(*args);raise KeyboardInterrupt('synthetic interruption')
                with patch.object(fake,'push',side_effect=interrupted):
                    with self.assertRaises(KeyboardInterrupt):service.publish(run)
                fake.pulls=[public_pr()];target=service.publish(run)
                intent=service.run(run)['contribution'];fake.calls.clear()
                if changed=='remote':fake.refs[intent['branch']]='b'*40
                if changed=='authorization':service.disable()
                base=fake.base
                def current(checkout):
                    result=base(checkout)
                    return dict(result,sha='c'*40) if changed=='base' else result
                with patch.object(fake,'base',side_effect=current):
                    with self.assertRaises(ToolError):service.compare(run,assessment(target,8))
                self.assertNotIn('push',fake.calls);self.assertNotIn('create',fake.calls)
                if changed=='authorization':self.assertEqual(fake.calls,[])
                self.assertNotEqual(service.run(run)['status'],'duplicate')
                for key in ('commit','validation','branch','worktree','base'):
                    self.assertEqual(service.run(run)['contribution'][key],intent[key])

    def test_known_creation_reference_survives_failed_metadata_lookup(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            original=fake.create
            def unavailable(branch,base,title,body,observe):
                pr=original(branch,base,title,body)
                observe({'number':pr['number'],'url':pr['url']})
                raise ToolError(5,'synthetic metadata lookup unavailable')
            with patch.object(fake,'create',side_effect=unavailable):
                with self.assertRaises(ToolError):service.publish(run)
            self.assertEqual(service.status(run)['latest_run']['remote_outcome'],'observed')
            self.assertEqual(service.status(run)['latest_run']['pr']['number'],1)
            self.assertEqual(service.resume(run)['status'],'published')
            self.assertEqual(fake.calls.count('create'),1)

    def test_revocation_during_identity_stops_following_requests(self):
        from novel_creator.retro import Retro
        from tests.retro_contribution_helpers import selected
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=selected(service,root,initial);fake.calls.clear();original=fake.identity
            def revoke():
                result=original();service.disable();return result
            with patch.object(fake,'identity',side_effect=revoke):
                with self.assertRaises(ToolError):service.prepare(run)
            self.assertEqual(fake.calls,['identity'])

    def test_uncertain_create_reconciles_without_second_request(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry); service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial); service.validate_contribution(run,data)
            fake.unknown_create=True
            with self.assertRaises(ToolError): service.publish(run)
            service.resume(run)
            self.assertEqual(service.run(run)['status'],'published')
            self.assertEqual(fake.calls.count('create'),1)

    def test_disable_stops_resume_release_before_external_access(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry); service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            service.disable(); fake.calls.clear()
            for action in (service.resume,service.release):
                with self.assertRaises(ToolError): action(run)
            self.assertEqual(fake.calls,[])
            service.enable(checkout,authorize=True)
            service.resume(run)
            self.assertEqual(service.release(run)['status'],'abandoned')
