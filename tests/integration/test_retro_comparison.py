"""Public comparison judgments are explicit, snapshot-bound host input."""
import unittest
import argparse
import json
from contextlib import contextmanager
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import selected,prepared
from novel_creator.cli import ToolError


def public_pr(**overrides):
    return dict(number=8,url='https://github.com/bjarkig82/novel-creator/pull/8',
                head='public-fix',base='main',sha='a'*40,draft=True,
                repository='bjarkig82/novel-creator',body='Handle an empty parser input.',
                title='Accept zero elements',state='open',merged=False,**overrides)


def assessment(target, equivalent=None, upstream=False):
    return dict(snapshot=target['snapshot'],equivalent_pr=equivalent,
                upstream_fix_present=upstream,public_scope_reviewed=True)


class Comparison(unittest.TestCase):
    def test_delayed_comparison_preserves_new_publication_receipts(self):
        from novel_creator.retro import Retro,dispatch
        from tests.helpers import git
        for effect in ('published', 'create_intent', 'observed'):
            with self.subTest(effect=effect), fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                upstream,candidates,snapshot=service.comparison_scope(service.run(run),service.require())
                judgment=dict(snapshot=snapshot,equivalent_pr=None,upstream_fix_present=False,public_scope_reviewed=True)
                input_path=service.path('inputs/comparison.json');input_path.write_text(json.dumps(judgment))
                args=argparse.Namespace(novel=str(root),run=run,action='compare',input=str(input_path))
                (checkout/'unrelated.txt').write_text('preserve staged user work')
                git(checkout,'add','unrelated.txt')
                before=(git(root,'rev-parse','HEAD'),git(checkout,'ls-files','--stage'))
                original=service.repository_operation;latest=[];calls=[]
                def create(branch,base,title,body,observe):
                    if effect=='observed':
                        pr=original_create(branch,base,title,body,observe)
                    raise KeyboardInterrupt('synthetic interruption after durable effect')
                original_create=fake.create
                @contextmanager
                def delayed(item,**kwargs):
                    with patch.object(service,'repository_operation',original):
                        if effect=='published':service.publish(run)
                        else:
                            with patch.object(fake,'create',side_effect=create):
                                with self.assertRaises(KeyboardInterrupt):service.publish(run)
                        latest.append(service.run(run))
                        calls.extend(fake.calls)
                    with original(item,**kwargs) as operation:yield operation
                with patch.object(service,'repository_operation',delayed),patch('novel_creator.retro.Retro',return_value=service):
                    with self.assertRaisesRegex(ToolError,'Retrospective state changed'):dispatch(args)
                restarted=Retro(root,github=fake,registry=registry)
                self.assertEqual(restarted.run(run),latest[0])
                self.assertEqual(fake.calls,calls)
                self.assertIsNotNone(latest[0]['contribution']['commit'])
                if effect=='create_intent':
                    self.assertEqual(latest[0]['contribution']['stage'],'create_intent')
                    with self.assertRaises(ToolError):restarted.resume(run)
                    self.assertNotIn('create',fake.calls)
                else:
                    self.assertEqual(restarted.resume(run)['status'],'published')
                    self.assertEqual(restarted.status(run)['latest_run']['pr']['number'],1)
                    self.assertEqual(fake.calls.count('create'),1)
                self.assertEqual(fake.calls.count('push'),1)
                self.assertEqual((git(root,'rev-parse','HEAD'),git(checkout,'ls-files','--stage')),before)

    def test_reassess_after_interrupted_push_preserves_intent_and_avoids_second_push(self):
        from novel_creator.retro import Retro
        for equivalent in (None,8):
            for after_push in (False,True):
                with self.subTest(equivalent=equivalent,after_push=after_push),fixtures() as (root,checkout,registry,fake,initial):
                    service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                    run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                    push=fake.push
                    def interrupted(*args):
                        if after_push:push(*args)
                        raise KeyboardInterrupt('synthetic push interruption')
                    with patch.object(fake,'push',side_effect=interrupted):
                        with self.assertRaises(KeyboardInterrupt):service.publish(run)
                    before=service.run(run)['contribution']
                    fake.pulls=[public_pr()]
                    target=service.publish(run)
                    self.assertEqual(target['status'],'comparison_required')
                    result=service.compare(run,assessment(target,equivalent))
                    after=service.run(run)['contribution']
                    for key in ('commit','validation','branch','worktree','base'):
                        self.assertEqual(after[key],before[key])
                    if equivalent:
                        self.assertEqual(result['status'],'duplicate')
                        self.assertEqual(Retro(root,github=fake,registry=registry).status(run)['latest_run']['pr']['number'],8)
                        self.assertNotIn('create',fake.calls)
                    else:
                        self.assertEqual(service.publish(run)['status'],'published')
                        self.assertEqual(fake.calls.count('push'),1)
                        self.assertEqual(fake.calls.count('create'),1)
                        self.assertEqual(service.resume(run)['status'],'published')

    def test_public_comparison_output_is_bounded_and_marks_missing_scope(self):
        from novel_creator.retro import Retro
        service=Retro.__new__(Retro)
        candidates=[dict(public_pr(),number=n,title='T'*1100,body='B'*9000) for n in range(1,52)]
        result=service.comparison_request({'run_id':'synthetic'},dict(branch='main',sha='a'*40),candidates,'b'*64)
        self.assertEqual(result['candidate_count'],51);self.assertTrue(result['has_more'])
        self.assertEqual(len(result['candidates']),50)
        self.assertEqual(len(result['candidates'][0]['body']),8192)
        self.assertEqual(len(result['candidates'][0]['title']),1024)
        self.assertTrue(result['candidates'][0]['text_truncated'])

    def test_public_equivalence_and_upstream_review_are_required(self):
        from novel_creator.retro import Retro
        for state,merged,equivalent in [('open',False,8),('closed',True,8),('closed',False,None)]:
            with self.subTest(state=state,merged=merged),fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                fake.pulls=[dict(public_pr(),state=state,merged=merged)]
                run=selected(service,root,initial)
                target=service.prepare(run)
                self.assertEqual(target['status'],'comparison_required')
                self.assertEqual(len(target['candidates']),0 if state=='closed' and not merged else 1)
                result=service.compare(run,assessment(target,equivalent))
                if equivalent:
                    self.assertEqual(result['status'],'duplicate')
                    restarted=Retro(root,github=fake,registry=registry)
                    self.assertEqual(restarted.status(run)['latest_run']['pr']['url'],fake.pulls[0]['url'])
                else:self.assertEqual(service.prepare(run)['status'],'prepared')
                self.assertNotIn('create',fake.calls)

    def test_stale_judgment_and_irrelevant_marker_do_not_suppress_fix(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            fake.pulls=[public_pr()];run=selected(service,root,initial)
            target=service.prepare(run)
            fake.pulls[0]['body']='Unrelated public issue with novel-retro-finding:irrelevant'
            with self.assertRaises(ToolError):service.compare(run,assessment(target,8))
            target=service.prepare(run);service.compare(run,assessment(target))
            self.assertEqual(service.prepare(run)['status'],'prepared')
            self.assertEqual(service.run(run)['status'],'prepared')

    def test_current_upstream_fix_ends_without_a_pr(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=selected(service,root,initial);target=service.prepare(run)
            self.assertEqual(service.compare(run,assessment(target,upstream=True))['status'],'duplicate')
            self.assertEqual(service.status(run)['latest_run']['reason_code'],'upstream_already_fixed')
            self.assertNotIn('create',fake.calls)

    def test_new_public_candidate_blocks_publication_until_reassessed(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            fake.pulls=[public_pr()]
            target=service.publish(run)
            self.assertEqual(target['status'],'comparison_required')
            self.assertNotIn('push',fake.calls)
            service.compare(run,assessment(target,8))
            self.assertEqual(service.status(run)['latest_run']['pr']['number'],8)
