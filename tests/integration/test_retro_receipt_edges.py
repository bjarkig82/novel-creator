"""Additional receipt-boundary regressions, using only synthetic repositories."""
import unittest
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.helpers import envelope,seal,uid,git,FailAt
from tests.contract.test_retro_review import begin_input
from tests.retro_contribution_helpers import prepared
from novel_creator import storage
from novel_creator.cli import ToolError


def notice_payload(service,root,previous,notes):
    from novel_creator.retro import digest
    exchange=envelope(root,previous=previous)
    response='Synthetic reply.\n';spans=[]
    for note in notes:
        start=len(response.encode());response+=note['text']
        spans.append({'notice_id':note['notice_id'],'start_byte':start,'end_byte':len(response.encode()),'text_digest':note['text_digest']})
        response+='\n'
    exchange['messages'][1]['text']=response;exchange=seal(exchange)
    data={'retro_version':1,'reservation_id':uid(),'exchange_id':exchange['exchange_id'],
          'message_id':exchange['messages'][1]['message_id'],'expected_head':exchange['expected_git_head'],
          'payload_digest':exchange['payload_digest'],'assistant_text_digest':digest(response.encode()),'notices':spans}
    return exchange,data


class ReceiptEdges(unittest.TestCase):
    def test_publication_notice_is_idempotent_across_terminal_save_interruption(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            original=service.save_run
            def fail_terminal(item):
                if item['status']=='published':raise OSError('synthetic death before terminal receipt')
                return original(item)
            with patch.object(service,'save_run',side_effect=fail_terminal):
                with self.assertRaises(OSError):service.publish(run)
            notes=service.notices_pending()['notices'];self.assertEqual(len(notes),1)
            exchange,reservation=notice_payload(service,root,initial,notes)
            service.notices_reserve(reservation);storage.save(root,exchange)
            service.notices_confirm(reservation['reservation_id'])
            service.resume(run)
            self.assertEqual(service.notices_pending()['notices'],[])
            self.assertEqual(len(service.notice_items()),1)
            self.assertEqual(fake.calls.count('create'),1)

    def test_confirmed_inclusion_cannot_be_released_when_history_is_missing(self):
        from novel_creator.retro import Retro,load
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=service.begin(begin_input(root,initial))['run_id'];service.review(run,{'outcome':'insufficient_evidence'})
            exchange,data=notice_payload(service,root,initial,service.notices_pending()['notices'])
            service.notices_reserve(data);storage.save(root,exchange)
            service.notices_confirm(data['reservation_id'])
            (root/'.novel-creator/local'/ (exchange['exchange_id']+'.json')).unlink(missing_ok=True)
            with patch.object(service,'history',return_value=[initial]):
                for _ in range(2):
                    with self.assertRaises(ToolError):service.notices_reconcile(data['reservation_id'])
            receipt=load(service.path('reservations/'+data['reservation_id']+'.json'),'reservation')
            self.assertEqual(receipt['state'],'included')
            self.assertEqual(service.notices_pending()['notices'],[])
            self.assertEqual(service.notices_confirm(data['reservation_id'])['state'],'included')

    def test_pending_story_save_retains_reservation_until_original_recovery(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=service.begin(begin_input(root,initial))['run_id'];service.review(run,{'outcome':'insufficient_evidence'})
            exchange,data=notice_payload(service,root,initial,service.notices_pending()['notices'])
            service.notices_reserve(data)
            with self.assertRaises(ToolError):storage.save(root,exchange,fault=FailAt('before_ref'))
            with self.assertRaises(ToolError):service.notices_reconcile(data['reservation_id'])
            self.assertEqual(service.notices_pending()['notices'],[])
            storage.recover(root,exchange['exchange_id'],retry=True,expected_head=git(root,'rev-parse','HEAD'))
            self.assertEqual(service.notices_confirm(data['reservation_id'])['state'],'included')

    def test_partial_batch_cannot_be_reserved_twice_and_reconciles(self):
        from novel_creator import retro
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            for turn in ('one','two'):
                run=service.begin(begin_input(root,initial,turn))['run_id'];service.review(run,{'outcome':'insufficient_evidence'})
            exchange,data=notice_payload(service,root,initial,service.notices_pending()['notices'])
            original=retro.write;count=0
            def interrupt(path,value,kind):
                nonlocal count
                if kind=='notice':
                    count+=1
                    if count==2:raise OSError('synthetic interrupted notice batch')
                return original(path,value,kind)
            with patch('novel_creator.retro.write',side_effect=interrupt):
                with self.assertRaises(OSError):service.notices_reserve(data)
            self.assertEqual(service.notices_pending()['notices'],[])
            other=dict(data,reservation_id=uid())
            with self.assertRaises(ToolError):service.notices_reserve(other)
            storage.save(root,exchange)
            self.assertEqual(service.notices_reconcile(data['reservation_id'])['state'],'included')
            self.assertEqual(service.notices_pending()['notices'],[])

    def test_mismatched_saved_notice_is_a_conflict_not_consumption(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run=service.begin(begin_input(root,initial))['run_id'];service.review(run,{'outcome':'insufficient_evidence'})
            exchange,data=notice_payload(service,root,initial,service.notices_pending()['notices'])
            service.notices_reserve(data)
            exchange['messages'][1]['text']='Different saved response';exchange=seal(exchange)
            storage.save(root,exchange)
            with self.assertRaises(ToolError):service.notices_reconcile(data['reservation_id'])
            self.assertEqual(service.notices_pending()['notices'],[])

    def test_missing_check_wrong_draft_and_uncertain_absence_block(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial)
            with self.assertRaises(ToolError):service.validate_contribution(run,dict(data,checks=[]))
            service.validate_contribution(run,data)
            original=fake.create
            def wrong(*args):
                pr=original(*args);pr['draft']=False;return pr
            with patch.object(fake,'create',side_effect=wrong):
                with self.assertRaises(ToolError):service.publish(run)
            with self.assertRaises(ToolError):service.resume(run)
            self.assertNotEqual(service.run(run)['status'],'published')
            self.assertEqual(fake.calls.count('create'),1)

    def test_unknown_create_without_listing_result_is_never_retried(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            with patch.object(fake,'create',side_effect=OSError('ambiguous request')) as request:
                with self.assertRaises(ToolError):service.publish(run)
                with self.assertRaises(ToolError):service.publish(run)
                self.assertEqual(request.call_count,1)

    def test_checked_draft_notice_is_saved_in_next_reply(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data);service.publish(run)
            exchange,reservation=notice_payload(service,root,initial,service.notices_pending(language='is')['notices'])
            service.notices_reserve(reservation);storage.save(root,exchange)
            self.assertEqual(service.notices_confirm(reservation['reservation_id'])['state'],'included')
            self.assertIn('https://github.com/bjarkig82/novel-creator/pull/1',storage.read_history(root)[-1]['messages'][1]['text'])
            self.assertEqual(service.notices_pending()['notices'],[])
            self.assertEqual(fake.calls.count('create'),1)
