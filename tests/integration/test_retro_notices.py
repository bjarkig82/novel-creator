import unittest
from tests.helpers import envelope,seal,uid,git
from tests.retro_helpers import fixtures
from tests.contract.test_retro_review import begin_input
from novel_creator import storage
from novel_creator.cli import ToolError


class Notices(unittest.TestCase):
    def test_save_success_before_ack_is_reconciled_once(self):
        from novel_creator.retro import Retro,digest
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry); service.enable(checkout,authorize=True)
            run=service.begin(begin_input(root,initial))['run_id']
            service.review(run,{'outcome':'insufficient_evidence'})
            notice=service.notices_pending()['notices'][0]
            service.disable() # Existing notices remain local and usable.
            exchange=envelope(root,previous=initial)
            response='Þetta er svar. '+notice['text']
            exchange['messages'][1]['text']=response
            exchange=seal(exchange)
            start=len('Þetta er svar. '.encode())
            data={'retro_version':1,'reservation_id':uid(),'exchange_id':exchange['exchange_id'],
                  'message_id':exchange['messages'][1]['message_id'],'expected_head':exchange['expected_git_head'],
                  'payload_digest':exchange['payload_digest'],'assistant_text_digest':digest(response.encode()),
                  'notices':[{'notice_id':notice['notice_id'],'start_byte':start,'end_byte':len(response.encode()),
                              'text_digest':notice['text_digest']}]}
            service.notices_reserve(data)
            self.assertEqual(service.notices_pending()['notices'],[])
            storage.save(root,exchange)
            result=service.notices_reconcile(data['reservation_id'])
            self.assertEqual(result['state'],'included')
            self.assertEqual(service.notices_pending()['notices'],[])
            self.assertEqual(service.notices_confirm(data['reservation_id'])['state'],'included')
            self.assertEqual(storage.read_history(root)[-1]['messages'][1]['text'],response)

    def test_unsaved_reservation_releases_without_consuming_notice(self):
        from novel_creator.retro import Retro,digest
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry); service.enable(checkout,authorize=True)
            run=service.begin(begin_input(root,initial))['run_id']; service.review(run,{'outcome':'insufficient_evidence'})
            notice=service.notices_pending()['notices'][0]
            data={'retro_version':1,'reservation_id':uid(),'exchange_id':uid(),'message_id':uid(),
                  'expected_head':git(root,'rev-parse','HEAD'),'payload_digest':'a'*64,
                  'assistant_text_digest':digest(notice['text'].encode()),'notices':[{'notice_id':notice['notice_id'],
                  'start_byte':0,'end_byte':len(notice['text'].encode()),'text_digest':notice['text_digest']}]}
            service.notices_reserve(data)
            with self.assertRaises(ToolError): service.notices_confirm(data['reservation_id'])
            self.assertEqual(service.notices_reconcile(data['reservation_id'])['state'],'released')
            self.assertEqual(len(service.notices_pending()['notices']),1)
