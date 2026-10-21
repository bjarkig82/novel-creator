import unittest
from novel_creator import records, storage
from tests.helpers import envelope, record, repository, seal, git


class IndependentConsumerTests(unittest.TestCase):
    def test_independent_reader_rejects_missing_history_unknown_version_and_dangling_sources(self):
        from tests.integration.independent_reader import reconstruct
        import copy
        import json
        for corruption in ('missing_bootstrap', 'unsupported', 'dangling_record', 'dangling_message', 'wrong_creation'):
            with self.subTest(corruption=corruption), repository() as root:
                initial = envelope(root)
                storage.save(root, initial)
                exchange = envelope(root, previous=initial)
                proposal = record(exchange, 'question', text='Hvers vegna? / Why?', related_refs=[],
                    alternative_ids=[], state='open', resolution_decision_id=None)
                exchange = seal(dict(exchange, record_versions=[proposal]))
                storage.save(root, exchange)
                changed = copy.deepcopy(exchange)
                if corruption == 'missing_bootstrap':
                    (root / storage.bundle_path(initial)).unlink()
                    git(root, 'add', '--', storage.bundle_path(initial))
                else:
                    if corruption == 'unsupported':
                        changed['schema_version'] = '2.0'
                    elif corruption == 'dangling_record':
                        changed['record_versions'][0]['related_refs'] = [{'id': __import__('uuid').uuid4().__str__()}]
                    elif corruption == 'dangling_message':
                        changed['record_versions'][0].update(origin='supplied', source_refs=[{
                            'type': 'message', 'exchange_id': initial['exchange_id'],
                            'message_id': exchange['messages'][0]['message_id']}])
                    else:
                        changed['record_versions'][0]['created_exchange_id'] = initial['exchange_id']
                    path = root / storage.bundle_path(exchange)
                    path.write_text(json.dumps(seal(changed), ensure_ascii=False), encoding='utf-8')
                    git(root, 'add', '--', storage.bundle_path(exchange))
                git(root, 'commit', '-m', 'Harness invalid consumer history')
                with self.assertRaises(ValueError):
                    reconstruct(root)

    def test_reconstructs_entities_relationship_order_perspectives_and_decisions(self):
        from tests.integration.independent_reader import reconstruct
        from novel_creator.install import bootstrap
        import uuid
        with repository() as root:
            initial = bootstrap('{"title":"Þóra og bréfin","manuscript_language":"is"}',
                                records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id'])
            initial['expected_git_head'] = storage.head(root)
            elements = [record(initial, 'story_element', element_type=kind, display_name=name, aliases=[], status='proposed',
                assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
                for kind, name in [('character', 'Þóra'), ('event', 'Arrival'), ('event', 'Revelation'),
                                   ('location', 'Island'), ('plot_thread', 'Letters'), ('character', 'Þóra')]]
            unknown = {'precision': 'unknown', 'event_anchor': None, 'start': None, 'end': None, 'before_refs': [], 'after_refs': []}
            known = {'precision': 'known', 'event_anchor': {'id': elements[1]['id']},
                     'start': 'Day 1', 'end': 'Day 2', 'before_refs': [], 'after_refs': []}
            connection = record(initial, 'relationship', from_element_id=elements[0]['id'], to_element_id=elements[3]['id'],
                meaning='lives on', perspective='author_truth', holder_id=None, reader_audience=None,
                time_ref={'chronology': known, 'narrative': unknown},
                status='proposed', decision_ids=[])
            initial = seal(dict(initial, record_versions=[*initial['record_versions'], *elements, connection]))
            storage.save(root, initial)
            exchange = envelope(root, previous=initial)
            source = records.current_user_source(exchange)
            axis = {'precision': 'partial', 'event_anchor': {'id': elements[1]['id']}, 'start': None, 'end': None,
                    'before_refs': [{'id': elements[2]['id']}], 'after_refs': []}
            assertions = [record(exchange, 'assertion', subject_element_id=elements[0]['id'], predicate='knows sender', value='Keeper',
                perspective=perspective, holder_id=elements[0]['id'] if perspective.startswith('character_') else None,
                reader_audience='reader' if perspective == 'reader_revelation' else None, time_ref={'chronology': axis, 'narrative': axis},
                truth_state={'character_belief': 'denied', 'reader_revelation': 'unknown'}.get(perspective, 'affirmed'),
                status='accepted', decision_ids=[],
                supersedes=None, source_refs=[source], origin='supplied')
                for perspective in ['author_truth', 'character_knowledge', 'character_belief', 'reader_revelation']]
            decision = record(exchange, 'decision', action='accept', user_message_ref=source, span={'start': 0, 'end': 7},
                target_refs=[{'id': r['id'], 'revision': 1} for r in assertions], selected_parts=[], prior_refs=[], result_refs=[],
                reason='Prepared explicit selection fixture', affected_refs=[], review_required_refs=[])
            for r in assertions:
                r['decision_ids'] = [decision['id']]
            session = records.start_session(exchange, topic='Knowledge / Vitneskja')
            question = record(exchange, 'question', text='Hvers vegna?', related_refs=[{'id': elements[0]['id']}],
                alternative_ids=[], state='open', resolution_decision_id=None)
            proposal = record(exchange, 'idea', statement='Kannski er bréfið falsað / perhaps forged',
                status='unresolved', related_element_ids=[elements[0]['id']], alternative_group_id=str(uuid.uuid4()),
                selected_parts=[], decision_ids=[], resulting_assertion_ids=[])
            finding = record(exchange, 'finding', category='knowledge', assessment='opportunity', severity='advisory',
                affected_refs=[{'id': elements[0]['id']}], explanation='Sourced foreshadowing opportunity',
                consequences=[], resolution_options=[], disposition='open', decision_ids=[], narrative_explanation=None)
            exchange = seal(dict(exchange, session_id=session['id'],
                record_versions=[*assertions, decision, session, question, proposal, finding]))
            storage.save(root, exchange)
            independent = reconstruct(root)
            self.assertEqual(independent['records'], records.fold([initial, exchange]))
            self.assertEqual({r['perspective'] for r in independent['current_canon']},
                             {'author_truth', 'character_knowledge', 'character_belief', 'reader_revelation'})
            self.assertEqual(independent['records'][connection['id']]['to_element_id'], elements[3]['id'])
            self.assertEqual(independent['records'][connection['id']]['time_ref']['chronology']['precision'], 'known')
            self.assertEqual(independent['records'][connection['id']]['time_ref']['narrative']['start'], None)
            self.assertEqual({r['perspective']: r['truth_state'] for r in independent['current_canon']},
                {'author_truth': 'affirmed', 'character_knowledge': 'affirmed',
                 'character_belief': 'denied', 'reader_revelation': 'unknown'})
            self.assertEqual(independent['records'][assertions[0]['id']]['time_ref']['chronology']['before_refs'][0]['id'], elements[2]['id'])
            self.assertEqual(independent['records'][decision['id']]['user_message_ref'], source)
            self.assertEqual({r['kind'] for r in independent['records'].values()},
                {'novel_project', 'session', 'idea', 'story_element', 'relationship', 'assertion', 'decision', 'question', 'finding'})
            self.assertEqual(independent['records'][initial['novel_id']]['title']['original_text'], 'Þóra og bréfin')

            revision = envelope(root, previous=exchange)
            current_source = records.current_user_source(revision)
            replacement = dict(assertions[0], id=str(uuid.uuid4()), created_exchange_id=revision['exchange_id'],
                value='Þóra', source_refs=[current_source], supersedes={'id': assertions[0]['id'], 'revision': 1})
            retired = dict(assertions[0], revision=2, previous_revision=1, status='superseded')
            change = record(revision, 'decision', action='revise', user_message_ref=current_source,
                span={'start': 0, 'end': 7}, target_refs=[{'id': retired['id'], 'revision': 2},
                    {'id': replacement['id'], 'revision': 1}], selected_parts=[],
                prior_refs=[{'id': retired['id'], 'revision': 1}], result_refs=[], reason='Fixture revision',
                affected_refs=[{'id': elements[0]['id']}], review_required_refs=[{'id': elements[0]['id']}])
            retired['decision_ids'] = replacement['decision_ids'] = [change['id']]
            renamed = dict(elements[0], revision=2, previous_revision=1, display_name='Ægir Örn', aliases=['Þóra'])
            revision = seal(dict(revision, record_versions=[retired, replacement, change, renamed]))
            storage.save(root, revision)
            independent = reconstruct(root)
            self.assertEqual(independent['records'][elements[0]['id']]['display_name'], 'Ægir Örn')
            self.assertEqual(independent['records'][elements[-1]['id']]['display_name'], 'Þóra')
            self.assertEqual([r['status'] for r in independent['versions'][retired['id']]], ['accepted', 'superseded'])
            self.assertNotIn(retired['id'], [r['id'] for r in independent['current_canon']])
            self.assertIn(replacement['id'], [r['id'] for r in independent['current_canon']])
            self.assertEqual(independent['records'][change['id']]['prior_refs'], [{'id': retired['id'], 'revision': 1}])
            self.assertEqual(independent['records'][replacement['id']]['supersedes'], {'id': retired['id'], 'revision': 1})
            cache = root / '.novel-creator/local/derived-cache.json'
            cache.write_text('{"fake_canon":"must not be read"}', encoding='utf-8')
            self.assertEqual(reconstruct(root), independent)
            cache.unlink()
            self.assertEqual(reconstruct(root), independent)
            path = root / storage.bundle_path(exchange)
            path.write_bytes(b'{broken')
            git(root, 'add', '--', path.relative_to(root).as_posix())
            git(root, 'commit', '-m', 'Harness damaged consumer context')
            with self.assertRaises(ValueError):
                reconstruct(root)
