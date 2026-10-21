import copy
import hashlib
import unittest
from novel_creator import records, validation
from tests.helpers import envelope, seal, idea, record, uid


class ExchangeContract(unittest.TestCase):
    def validate(self, data, history=()):
        return validation.validate_exchange(data, list(history))

    def test_bootstrap_and_chain_are_atomic(self):
        first = envelope()
        item = idea(first)
        first = seal(dict(first, record_versions=[item]))
        self.validate(first)
        second = envelope(previous=first)
        updated = dict(item, revision=2, previous_revision=1, statement="Revised possibility")
        second = seal(dict(second, record_versions=[updated]))
        state = self.validate(second, [first])
        self.assertEqual(state[item["id"]]["revision"], 2)
        self.assertEqual(item["revision"], 1)
        updated["previous_revision"] = None
        with self.assertRaises(ValueError):
            self.validate(seal(dict(second, record_versions=[updated])), [first])

    def test_bad_chain_and_unknown_schema(self):
        first = envelope()
        for field, value in (("schema_version", "2.0"), ("sequence", 0),
                             ("previous_digest", "0" * 64), ("previous_exchange_id", uid()),
                             ("novel_id", "not-a-uuid")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.validate(seal(dict(first, **{field: value})))
        second = envelope(previous=first)
        for field, value in (("sequence", 3), ("novel_id", uid()), ("previous_digest", "0" * 64)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.validate(seal(dict(second, **{field: value})), [first])

    def test_duplicates_and_digest(self):
        data = envelope()
        item = idea(data)
        for changed in (dict(data, record_versions=[item, item]), dict(data, payload_digest="0" * 64)):
            with self.assertRaises(ValueError):
                self.validate(seal(changed) if "record_versions" in changed and len(changed["record_versions"]) else changed)
        turn = envelope(previous=data)
        turn["messages"][1]["message_id"] = turn["messages"][0]["message_id"]
        with self.assertRaises(ValueError):
            self.validate(seal(turn), [data])

    def test_artifact_digest_pointer_and_no_canon_authorization(self):
        data = envelope()
        text = '{"concept":{"a/b~c":"Þóra"}}'
        artifact = {"artifact_id": uid(), "original_text": text,
                    "parsed_value": records.loads(text), "digest": hashlib.sha256(text.encode()).hexdigest()}
        source = {"type": "bootstrap_artifact", "exchange_id": data["exchange_id"],
                  "artifact_id": artifact["artifact_id"], "pointer": "/concept/a~1b~0c"}
        item = idea(data)
        item.update(origin="supplied", source_refs=[source])
        data = seal(dict(data, input_artifacts=[artifact], record_versions=[item]))
        self.validate(data)
        for pointer in ("/missing", "/concept/a~2b", "bad"):
            changed = copy.deepcopy(data)
            changed["record_versions"][0]["source_refs"][0]["pointer"] = pointer
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                self.validate(seal(changed))
        changed = copy.deepcopy(data)
        changed["input_artifacts"][0]["digest"] = "0" * 64
        with self.assertRaises(ValueError): self.validate(seal(changed))
        changed = copy.deepcopy(data)
        changed["record_versions"][0]["status"] = "accepted"
        with self.assertRaises(ValueError): self.validate(seal(changed))

    def test_same_bundle_forward_references_and_missing_reference(self):
        data = envelope()
        entity = record(data, "story_element", element_type="character", display_name="Þóra", aliases=[],
                        status="proposed", assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
        proposed = idea(data)
        proposed["related_element_ids"] = [entity["id"]]
        data = seal(dict(data, record_versions=[proposed, entity]))
        self.validate(data)
        proposed["related_element_ids"] = [uid()]
        with self.assertRaises(ValueError): self.validate(seal(dict(data, record_versions=[proposed, entity])))

    def test_message_sources_and_actual_user_authorization(self):
        bootstrap = envelope()
        data = envelope(previous=bootstrap)
        source = {"type": "message", "exchange_id": data["exchange_id"],
                  "message_id": data["messages"][0]["message_id"], "range": {"start": 0, "end": 7}}
        proposed = idea(data)
        proposed.update(status="accepted", origin="supplied", source_refs=[source])
        decision = record(data, "decision", origin="supplied", source_refs=[source], action="accept",
                          user_message_ref=source, span={"start": 0, "end": 7}, target_refs=[{"id": proposed["id"], "revision": 1}],
                          selected_parts=[], prior_refs=[], result_refs=[{"id": proposed["id"], "revision": 1}],
                          reason="Explicit selection", affected_refs=[], review_required_refs=[])
        proposed["decision_ids"] = [decision["id"]]
        data = seal(dict(data, record_versions=[proposed, decision]))
        self.validate(data, [bootstrap])
        changed = copy.deepcopy(data)
        changed["record_versions"][1]["user_message_ref"]["message_id"] = data["messages"][1]["message_id"]
        with self.assertRaises(ValueError): self.validate(seal(changed), [bootstrap])
        changed = copy.deepcopy(data)
        changed["record_versions"][0]["source_refs"][0]["range"]["end"] = 999
        with self.assertRaises(ValueError): self.validate(seal(changed), [bootstrap])
        changed = copy.deepcopy(data)
        changed["continuity_review"]["canon_hold_refs"] = ["*"]
        with self.assertRaises(ValueError): self.validate(seal(changed), [bootstrap])

    def test_maintenance_cannot_introduce_canon(self):
        bootstrap = envelope()
        data = envelope(previous=bootstrap, operation="maintenance", messages=[])
        proposed = idea(data)
        proposed["status"] = "accepted"
        with self.assertRaises(ValueError): self.validate(seal(dict(data, record_versions=[proposed])), [bootstrap])

    def test_schema_requires_complete_typed_records(self):
        data = envelope()
        for kind in ("novel_project", "session", "idea", "story_element", "relationship", "assertion", "decision", "question", "finding"):
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.validate(seal(dict(data, record_versions=[record(data, kind)])))

    def test_all_typed_records_have_valid_structural_examples(self):
        data = envelope()
        unknown = {"state": "unknown", "original_text": None, "interpretation": None,
                   "origin": "system_default", "source_refs": []}
        project = record(data, "novel_project", title=unknown, original_concept=unknown,
                         creative_brief={k: unknown for k in ('genre','subgenres','audience','tone','style','perspective','complexity')},
                         manuscript_language='is', workflow_preferences={},
                         review_preferences={'routine_checkpoint':'on_request'}, creative_directions=[])
        element = record(data, 'story_element', element_type='event', display_name='Arrival', aliases=[],
                         status='proposed', assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
        axis = {'precision':'unknown','event_anchor':None,'start':None,'end':None,'before_refs':[],'after_refs':[]}
        timing = {'chronology':axis,'narrative':axis}
        assertion = record(data,'assertion',subject_element_id=element['id'],predicate='is remembered',value=True,
                           perspective='reader_revelation', holder_id=None,reader_audience='reader',time_ref=timing,
                           truth_state='unknown',status='proposed',decision_ids=[],supersedes=None)
        relationship = record(data,'relationship',from_element_id=element['id'],to_element_id=element['id'],
                              meaning='echoes',perspective='author_truth',holder_id=None,reader_audience=None,
                              time_ref=timing,status='proposed',decision_ids=[])
        session = record(data,'session',topic='Opening',mode='guided',state='open',started_exchange_id=data['exchange_id'],
                         last_exchange_id=data['exchange_id'],related_record_ids=[element['id']],unresolved_question_ids=[],derived_context_ref=None)
        question = record(data,'question',text='Why?',related_refs=[{'id':element['id']}],alternative_ids=[],state='open',resolution_decision_id=None)
        finding = record(data,'finding',category='motivation',assessment='opportunity',severity='advisory',affected_refs=[],
                         explanation='Possible echo',consequences=[],resolution_options=[],disposition='open',decision_ids=[],narrative_explanation=None)
        examples = [project,session,idea(data),element,relationship,assertion,question,finding]
        value = seal(dict(data, record_versions=examples))
        self.assertEqual(len(self.validate(value)), len(examples))
        for checkpoint in ('on_request','session_close','every_exchange'):
            project['review_preferences']['routine_checkpoint'] = checkpoint
            self.validate(seal(dict(data,record_versions=examples)))
        project['review_preferences']['routine_checkpoint'] = 'never_save'
        with self.assertRaises(ValueError): self.validate(seal(dict(data,record_versions=examples)))
        project['review_preferences']['routine_checkpoint'] = 'on_request'
        assertion['reader_audience'] = None
        with self.assertRaises(ValueError): self.validate(seal(dict(data,record_versions=examples)))

    def test_duplicate_exchange_message_identity_rejected(self):
        bootstrap = envelope()
        data = envelope(previous=bootstrap)
        data['messages'][0]['message_id'] = data['exchange_id']
        with self.assertRaises(ValueError): self.validate(seal(data), [bootstrap])

    def test_typed_id_lists_cannot_reference_wrong_record_kind(self):
        data = envelope()
        for field in ('related_element_ids','resulting_assertion_ids'):
            item = idea(data)
            item[field] = [item['id']]
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.validate(seal(dict(data,record_versions=[item])))

    def test_canon_authorization_must_target_the_resulting_revision(self):
        bootstrap = envelope()
        first = envelope(previous=bootstrap)
        item = idea(first)
        first = seal(dict(first, record_versions=[item]))
        data = envelope(previous=first)
        source = {'type':'message','exchange_id':data['exchange_id'],
                  'message_id':data['messages'][0]['message_id'],'range':{'start':0,'end':7}}
        changed = dict(item,revision=2,previous_revision=1,status='accepted',statement='Changed proposition',origin='supplied',source_refs=[source])
        decision = record(data,'decision',origin='supplied',source_refs=[source],action='accept',user_message_ref=source,
                          span={'start':0,'end':7},target_refs=[{'id':item['id'],'revision':1}],selected_parts=[],prior_refs=[],
                          result_refs=[],reason='Select old proposal only',affected_refs=[],review_required_refs=[])
        changed['decision_ids'] = [decision['id']]
        with self.assertRaises(ValueError):
            self.validate(seal(dict(data,record_versions=[changed,decision])),[bootstrap,first])

    def test_acceptance_can_target_unchanged_prior_proposition(self):
        bootstrap = envelope()
        first = envelope(previous=bootstrap)
        item = idea(first)
        first = seal(dict(first,record_versions=[item]))
        data = envelope(previous=first)
        source = {'type':'message','exchange_id':data['exchange_id'],
                  'message_id':data['messages'][0]['message_id'],'range':{'start':0,'end':7}}
        changed = dict(item,revision=2,previous_revision=1,status='accepted',origin='supplied',source_refs=[source])
        decision = record(data,'decision',origin='supplied',source_refs=[source],action='accept',user_message_ref=source,
                          span={'start':0,'end':7},target_refs=[{'id':item['id'],'revision':1}],selected_parts=[],prior_refs=[],
                          result_refs=[],reason='Select unchanged proposal',affected_refs=[],review_required_refs=[])
        changed['decision_ids'] = [decision['id']]
        result = self.validate(seal(dict(data,record_versions=[changed,decision])),[bootstrap,first])
        self.assertEqual(result[item['id']]['status'],'accepted')
