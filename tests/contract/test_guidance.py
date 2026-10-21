import unittest
from novel_creator import records, validation
from tests.helpers import envelope, seal


class GuidanceContract(unittest.TestCase):
    def test_guided_default_switch_redirect_close_and_explicit_reopen(self):
        bootstrap = envelope()
        exchange = envelope(previous=bootstrap)
        session = records.start_session(exchange, topic='The lighthouse')
        exchange.update(session_id=session['id'], record_versions=[session])
        first = seal(exchange)
        validation.validate_exchange(first, [bootstrap])
        self.assertEqual(session['mode'], 'guided')
        change = envelope(previous=first)
        changed = records.revise_session(session, change, mode='open', topic='The keeper')
        change.update(session_id=session['id'], record_versions=[changed])
        second = seal(change)
        validation.validate_exchange(second, [bootstrap, first])
        self.assertEqual(changed['mode'], 'open')
        self.assertEqual(changed['topic'], 'The keeper')
        close = envelope(previous=second)
        closed = records.revise_session(changed, close, state='closed')
        close['record_versions'] = [closed]
        third = seal(close)
        validation.validate_exchange(third, [bootstrap, first, second])
        reopen = envelope(previous=third)
        with self.assertRaises(ValueError):
            records.revise_session(closed, reopen, state='open')
        resumed = records.revise_session(closed, reopen, state='open', reopen_requested=True)
        self.assertEqual(resumed['mode'], 'open')
        self.assertEqual(resumed['id'], session['id'])
        self.assertEqual(first['record_versions'][0]['topic'], 'The lighthouse')

    def test_invalid_session_changes_fail_before_save(self):
        exchange = envelope(previous=envelope())
        for mode in ('automatic', None):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                records.start_session(exchange, topic='Opening', mode=mode)
        session = records.start_session(exchange, topic='Opening')
        with self.assertRaises(ValueError):
            records.revise_session(session, exchange, mode='invalid')
