"""Historical v1 receipts are seeded directly; no retired producer is invoked."""
from pathlib import Path
import argparse
import os
import unittest
from unittest.mock import patch
from novel_creator import retro
from novel_creator.cli import ToolError
from novel_creator.retro_github import Github, REPOSITORY
from tests.helpers import git
from tests.retro_helpers import fixtures, historical




class Retirement(unittest.TestCase):
    def test_service_and_transport_reject_before_effects(self):
        with fixtures() as (root, checkout, registry, fake, initial):
            service=retro.Retro(root,github=fake,registry=registry)
            item,grant,base=historical(service,checkout,initial)
            before=service.path('runs/'+item['run_id']+'.json').read_bytes()
            for name,args in [('begin',({},)),('review',(item['run_id'],{})),
                              ('compare',(item['run_id'],{})),('prepare',(item['run_id'],)),
                              ('validate_contribution',(item['run_id'],{})),('publish',(item['run_id'],))]:
                with self.subTest(name=name),self.assertRaises(ToolError): getattr(service,name)(*args)
            with self.assertRaises(ToolError):service.enable(checkout,authorize=True)
            self.assertEqual(fake.calls,[])
            self.assertEqual(before,service.path('runs/'+item['run_id']+'.json').read_bytes())
            with patch('novel_creator.retro_github.command') as command:
                with self.assertRaises(ToolError):Github().push(checkout,'branch','sha')
                with self.assertRaises(ToolError):Github().create('branch','main','title','body')
                command.assert_not_called()
            args=argparse.Namespace(novel=str(root),action='prepare',run=item['run_id'])
            with patch.object(retro,'Retro',return_value=service),self.assertRaises(ToolError):retro.dispatch(args)
            self.assertEqual(before,service.path('runs/'+item['run_id']+'.json').read_bytes())

    def test_recovery_enable_preserves_identity_and_requires_matching_binding(self):
        with fixtures() as (root,checkout,registry,fake,initial):
            service=retro.Retro(root,github=fake,registry=registry)
            with self.assertRaises(ToolError):service.enable(checkout,recovery_only=True)
            item,grant,base=historical(service,checkout,initial)
            service.disable(); fake.calls.clear()
            self.assertFalse(service.status()['enabled'])
            with self.assertRaises(ToolError):service.resume(item['run_id'])
            self.assertEqual(fake.calls,[])
            fake.login='other'
            with self.assertRaises(ToolError):service.enable(checkout,recovery_only=True)
            fake.login=grant['github_login']
            service.enable(checkout,recovery_only=True)
            self.assertEqual(service.grant()['grant_id'],grant['grant_id'])
            self.assertEqual(service.grant()['generation'],3)
            self.assertEqual(service.run(item['run_id'])['authorization_generation'],1)
            self.assertEqual(service.resume(item['run_id'])['next_operation'],'release')
            self.assertEqual(service.run(item['run_id'])['authorization_generation'],3)
            self.assertEqual(service.release(item['run_id'])['status'],'abandoned')
            self.assertFalse((base/'owner.json').exists())

    def test_seeded_stages_preserve_work_and_never_publish(self):
        for stage in ('not_started','pushed','publication_unknown','create_intent'):
            with self.subTest(stage=stage),fixtures() as (root,checkout,registry,fake,initial):
                service=retro.Retro(root,github=fake,registry=registry)
                item,grant,base=historical(service,checkout,initial,stage,'prepared')
                part=item['contribution']; work=Path(part['worktree'])/'fix.txt'
                if stage=='pushed':fake.refs[part['branch']]=part['commit']
                if stage in ('publication_unknown','create_intent'):
                    with self.assertRaises(ToolError):service.resume(item['run_id'])
                    with self.assertRaises(ToolError):service.release(item['run_id'])
                    self.assertTrue((base/'owner.json').exists())
                else:
                    result=service.resume(item['run_id'])
                    self.assertNotEqual(result.get('next_operation'),'prepare')
                    self.assertEqual(service.release(item['run_id'])['status'],'abandoned')
                    self.assertFalse((base/'owner.json').exists())
                self.assertEqual(work.read_text(),'retained historical fix')
                self.assertFalse({'base','push','create'} & set(fake.calls))

    def test_known_closed_pr_release_and_terminal_owner(self):
        with fixtures() as (root,checkout,registry,fake,initial):
            service=retro.Retro(root,github=fake,registry=registry)
            item,grant,base=historical(service,checkout,initial,'remote_observed','blocked')
            part=item['contribution']
            pr=dict(number=7,url=f'https://github.com/{REPOSITORY}/pull/7',head=part['branch'],
                base='main',sha=part['commit'],draft=False,state='closed',repository=REPOSITORY,
                title='Historical fix',body='novel-retro-contribution:'+part['public_id'])
            fake.pulls=[pr];item['remote_outcome']=dict(kind='observed',pr=pr);service.save_run(item)
            with self.assertRaises(ToolError):service.resume(item['run_id'])
            self.assertEqual(service.release(item['run_id'])['status'],'abandoned')
            self.assertEqual(service.run(item['run_id'])['remote_outcome']['pr'],pr)
            self.assertFalse((base/'owner.json').exists())
            # Terminal cleanup can be retried without a new remote operation.
            retro.write(base/'owner.json',retro.document('owner',run_id=item['run_id'],
                grant_id=grant['grant_id'],novel_root=str(root)),'owner')
            fake.calls.clear();service.resume(item['run_id']);self.assertEqual(fake.calls,[])
            self.assertFalse((base/'owner.json').exists())

    def test_live_and_unknown_locks_are_never_removed(self):
        with fixtures() as (root,checkout,registry,fake,initial):
            service=retro.Retro(root,github=fake,registry=registry)
            item,grant,base=historical(service,checkout,initial)
            path=base/'operation.lock';path.mkdir()
            for raw in (b'{}', __import__('json').dumps(dict(retro_version=1,document='lock',
                           pid=os.getpid(),token=retro.uid())).encode()):
                (path/'holder.json').write_bytes(raw)
                with self.assertRaises(ToolError):service.release(item['run_id'])
                self.assertTrue(path.exists())

    def test_read_identity_without_push_permission(self):
        with patch.object(Github,'get',side_effect=[{'login':'reader'},
                {'full_name':REPOSITORY,'permissions':{'push':False}}]):
            self.assertEqual(Github().identity()['login'],'reader')

    def test_ambiguous_create_reconciles_known_pr_and_notice_once(self):
        with fixtures() as (root,checkout,registry,fake,initial):
            service=retro.Retro(root,github=fake,registry=registry)
            item,grant,base=historical(service,checkout,initial,'publication_unknown','blocked')
            part=item['contribution']
            pr=dict(number=8,url=f'https://github.com/{REPOSITORY}/pull/8',head=part['branch'],
                base='main',sha=part['commit'],draft=True,state='open',repository=REPOSITORY,
                title='Historical fix',body='novel-retro-contribution:'+part['public_id'])
            fake.pulls=[pr]
            original=service.save_run
            def fail_terminal(value):
                if value['status']=='published':raise OSError('Interrupted terminal receipt')
                return original(value)
            with patch.object(service,'save_run',side_effect=fail_terminal),self.assertRaises(OSError):
                service.resume(item['run_id'])
            self.assertEqual(service.run(item['run_id'])['remote_outcome']['pr'],pr)
            self.assertEqual(len(service.notice_items()),1)
            self.assertEqual(service.resume(item['run_id'])['status'],'published')
            self.assertEqual(len(service.notice_items()),1)
            self.assertFalse((base/'owner.json').exists())
            self.assertFalse({'create','push','base'} & set(fake.calls))
