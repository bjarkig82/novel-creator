import copy
import unittest

from novel_creator import validation
from tests.performance.benchmark_records import generate
from tests.helpers import uid, record as make_record, idea


class SchemaBackendParity(unittest.TestCase):
    def test_compiled_backend_matches_reference_for_valid_and_mutated_records(self):
        history, _ = generate(uid(), exchanges=6, sessions=2, assertions=12, minimum_bytes=0)
        extra = history[-1]
        axis = {'precision': 'unknown', 'event_anchor': None, 'start': None, 'end': None,
                'before_refs': [], 'after_refs': []}
        other_kinds = [idea(extra),
            make_record(extra, 'question', text='Why?', related_refs=[], alternative_ids=[], state='open', resolution_decision_id=None),
            make_record(extra, 'finding', category='knowledge', assessment='conflict', severity='significant',
                affected_refs=[], explanation='Fixture conflict', consequences=[], resolution_options=[],
                disposition='deferred', decision_ids=[], narrative_explanation=None),
            make_record(extra, 'relationship', from_element_id=uid(), to_element_id=uid(), meaning='knows',
                perspective='author_truth', holder_id=None, reader_audience=None,
                time_ref={'chronology': axis, 'narrative': axis}, status='proposed', decision_ids=[])]
        history.append(dict(extra, record_versions=other_kinds))
        reference = validation.validator()
        compiled = validation.compiled_validator()
        cases = list(history)
        for bundle in history:
            for index, record in enumerate(bundle['record_versions']):
                for field in record:
                    invalid = copy.deepcopy(bundle)
                    del invalid['record_versions'][index][field]
                    cases.append(invalid)
                invalid = copy.deepcopy(bundle)
                invalid['record_versions'][index]['kind'] = 'unknown'
                cases.append(invalid)
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(compiled.is_valid(case), reference.is_valid(case))

    def test_uuid_dates_bool_integer_and_unicode_boundaries_match(self):
        history, _ = generate(uid(), exchanges=2, sessions=1, assertions=2, minimum_bytes=0)
        for field, value in [('novel_id', 'not-a-uuid'), ('novel_id', '{' + uid() + '}'),
                             ('sequence', True), ('sequence', 1.5),
                             ('recorded_at', '2026-02-30T00:00:00Z'),
                             ('recorded_at', '2026-10-21T00:00:00Z')]:
            with self.subTest(field=field, value=value):
                case = dict(history[0], **{field: value})
                self.assertEqual(validation.compiled_validator().is_valid(case), validation.validator().is_valid(case))
