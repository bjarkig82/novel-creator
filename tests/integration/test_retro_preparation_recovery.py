import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import selected,prepared,ready_prepare
from tests.helpers import uid


class PreparationRecovery(unittest.TestCase):
    def test_dispatch_recovers_each_preparation_boundary_without_reallocation(self):
        import argparse
        from novel_creator import retro
        for boundary in ('before_allocation_save','allocation_save','before_add','after_add','prepared_save'):
            with self.subTest(boundary=boundary),fixtures() as (root,checkout,registry,fake,initial):
                service=retro.Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run=selected(service,root,initial)
                scope=service.prepare(run)
                service.compare(run,{'snapshot':scope['snapshot'],'equivalent_pr':None,
                                     'upstream_fix_present':False,'public_scope_reviewed':True})
                original_git=retro.contribution_git;original_save=service.save_run
                allocated=[]
                def fail_git(path,*args,**kwargs):
                    if args[:2]==('worktree','add') and boundary=='before_add':raise OSError('before add')
                    result=original_git(path,*args,**kwargs)
                    if args[:2]==('worktree','add') and boundary=='after_add':raise OSError('after add')
                    return result
                def fail_save(item):
                    if item['contribution']:allocated.append(dict(item['contribution']))
                    if boundary=='before_allocation_save' and item['status']=='preparing':raise OSError('before allocation save')
                    if boundary=='allocation_save' and item['status']=='preparing':
                        original_save(item);raise OSError('after allocation save')
                    if boundary=='prepared_save' and item['status']=='prepared':raise OSError('before result save')
                    return original_save(item)
                args=argparse.Namespace(novel=str(root),action='prepare',run=run)
                with patch.object(retro,'Retro',return_value=service),patch.object(retro,'contribution_git',side_effect=fail_git),patch.object(service,'save_run',side_effect=fail_save):
                    with self.assertRaises(OSError):retro.dispatch(args)
                failed=service.run(run)
                self.assertEqual(failed['status'],'blocked')
                restarted=retro.Retro(root,github=fake,registry=registry)
                self.assertEqual(restarted.resume(run)['next_operation'],'prepare')
                result=ready_prepare(restarted,run)
                self.assertEqual(result['status'],'prepared')
                current=restarted.run(run)
                if failed['contribution']:
                    for field in ('worktree','branch','base','public_id'):
                        self.assertEqual(current['contribution'][field],allocated[0][field])
                self.assertEqual(current['finding'],failed['finding'])
                self.assertTrue(restarted.notices_pending()['notices'])

    def test_preparation_intent_without_worktree_is_resumable(self):
        from novel_creator.retro import Retro
        from novel_creator import retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=selected(service,root,initial)
            original=retro.contribution_git
            def fail_add(path,*args,**kwargs):
                if args[:2]==('worktree','add'):raise OSError('synthetic process death before add')
                return original(path,*args,**kwargs)
            with patch('novel_creator.retro.contribution_git',side_effect=fail_add):
                with self.assertRaises(OSError):ready_prepare(service,run)
            self.assertEqual(service.prepare(run)['status'],'prepared')

    def test_worktree_created_before_receipt_status_save_is_resumable(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=selected(service,root,initial)
            original=service.save_run
            def fail_status(item):
                if item['status']=='prepared':raise OSError('synthetic process death after add')
                return original(item)
            with patch.object(service,'save_run',side_effect=fail_status):
                with self.assertRaises(OSError):ready_prepare(service,run)
            self.assertEqual(service.prepare(run)['status'],'prepared')

    def test_explicit_release_can_inspect_proven_dead_operation_holder(self):
        from novel_creator.retro import Retro
        from pathlib import Path
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            base=Path(service.grant()['git_common_dir'])/'novel-creator-retro'
            dead=subprocess.run([sys.executable,'-c','import os;print(os.getpid())'],capture_output=True,check=True,text=True)
            (base/'operation.lock').mkdir()
            (base/'operation.lock/holder.json').write_text(json.dumps({'retro_version':1,'document':'lock','pid':int(dead.stdout),'token':uid()}))
            self.assertEqual(service.release(run)['status'],'abandoned')
