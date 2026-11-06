"""Context projections read disposable committed journals, never local summaries."""
import json
import subprocess
import sys
import unittest

from novel_creator import records, storage
from novel_creator.cli import ToolError
from novel_creator.context import read
from tests.helpers import envelope, git, idea, record, repository, seal


class WorkingContextContract(unittest.TestCase):
    def fixture(self, root, count=24):
        first = envelope(root)
        project = records.project_from_brief({}, first, 'unused')
        element = record(first, 'story_element', element_type='character', display_name='Þóra',
            aliases=[], status='proposed', assertion_ids=[], relationship_ids=[],
            dependency_refs=[], time_ref=None, decision_ids=[])
        assertion = record(first, 'assertion', subject_element_id=element['id'], predicate='knows',
            value='A\u0301lfheimar', perspective='author_truth', holder_id=None, reader_audience=None,
            time_ref={axis: {'precision': 'unknown', 'event_anchor': None, 'start': None, 'end': None,
                'before_refs': [], 'after_refs': []} for axis in ('chronology', 'narrative')}, truth_state='affirmed', status='proposed',
            decision_ids=[], supersedes=None)
        unrelated = [dict(idea(first), statement='Unrelated possibility ' + str(i)) for i in range(count)]
        first = seal(dict(first, record_versions=[project, element, assertion, *unrelated]))
        storage.save(root, first)
        return first, project, element, assertion, unrelated

    def test_default_full_and_current_preserve_existing_fields(self):
        with repository() as root:
            first = envelope(root)
            storage.save(root, first)
            second = envelope(root, previous=first)
            storage.save(root, second)
            full = read(root)
            self.assertEqual(full, read(root, view='full'))
            current = read(root, view='current')
            self.assertNotIn('exchanges', current['data'])
            for key, value in full['data'].items():
                if key != 'exchanges':
                    self.assertEqual(current['data'][key], value, key)
            self.assertEqual(current['checkpoint'], full['checkpoint'])
            self.assertEqual(current['data']['omitted']['exchange_count'], 2)
            self.assertEqual(current['data']['view'], 'current')

    def test_focus_includes_incoming_assertion_complete_and_bounded(self):
        with repository() as root:
            first, project, element, assertion, unrelated = self.fixture(root)
            result = read(root, view='working', focus=[element['id']], limit=3)
            self.assertEqual(result, read(root, view='working', focus=[element['id']], limit=3))
            data = result['data']
            self.assertEqual(data['project'], project)
            self.assertEqual({r['id'] for r in data['records']}, {element['id'], assertion['id']})
            self.assertIn(assertion, data['records'])
            self.assertEqual(data['retrieval']['selection_reasons'][assertion['id']], 'incoming_record_link')
            self.assertFalse(data['retrieval']['exhaustive'])
            self.assertEqual(data['omitted']['record_count'], len(unrelated))
            self.assertEqual(data['omitted']['exchange_count'], 1)
            self.assertLess(len(json.dumps(result)), len(json.dumps(read(root))) * .7)
            limited = read(root, view='working', focus=[element['id']], limit=1)['data']
            self.assertEqual(limited['retrieval']['outstanding_record_ids'], [assertion['id']])
            self.assertNotIn('current_canon', data)
            self.assertNotIn('exchanges', data)

    def test_unicode_query_and_no_hits_are_distinct_from_no_records(self):
        with repository() as root:
            self.fixture(root)
            hit = read(root, view='working', query='ÁLFHEIMAR')['data']
            self.assertEqual(hit['retrieval']['query_match_count'], 1)
            self.assertEqual(len(hit['records']), 2)
            miss = read(root, view='working', query='absent word')['data']
            self.assertEqual(miss['retrieval']['result'], 'no_query_matches')
            self.assertEqual(miss['records'], [])
        with repository() as root:
            storage.save(root, envelope(root))
            self.assertEqual(read(root, view='working', query='absent')['data']['retrieval']['result'], 'no_saved_records')

    def test_fresh_revision_and_local_summary_is_never_authority(self):
        with repository() as root:
            first = envelope(root)
            proposal = dict(idea(first), statement='Before')
            first = seal(dict(first, record_versions=[proposal]))
            storage.save(root, first)
            before = read(root, view='working', focus=[proposal['id']])
            (root / '.novel-creator/local/working-summary.md').write_text('Fake accepted truth')
            second = envelope(root, previous=first)
            revised = dict(proposal, revision=2, previous_revision=1, statement='After')
            second = seal(dict(second, record_versions=[revised]))
            storage.save(root, second)
            after = read(root, view='working', focus=[proposal['id']])
            self.assertEqual(after['data']['records'], [revised])
            self.assertNotEqual(before['checkpoint'], after['checkpoint'])
            self.assertNotIn('Fake accepted truth', json.dumps(after))
            self.assertEqual(read(root, operation='inspect', identifier=proposal['id'])['data']['history'], [proposal, revised])

    def test_global_findings_holds_and_language_survive_focus(self):
        with repository() as root:
            first = envelope(root)
            proposal, other = idea(first), idea(first)
            finding = record(first, 'finding', category='knowledge', assessment='conflict',
                severity='significant', affected_refs=[{'id': other['id']}],
                explanation='Knowledge arrives late', consequences=[], resolution_options=[],
                disposition='deferred', decision_ids=[], narrative_explanation=None)
            first = seal(dict(first, record_versions=[proposal, other, finding]))
            storage.save(root, first)
            second = envelope(root, previous=first)
            second['continuity_review'].update(coverage='incomplete', canon_hold_refs=['*'])
            storage.save(root, seal(second))
            full = read(root)['data']
            working = read(root, view='working', focus=[proposal['id']], limit=1)['data']
            self.assertIn(finding, working['records'])
            self.assertIn(finding['id'], working['active_finding_ids'])
            self.assertIn(other['id'], working['retrieval']['outstanding_record_ids'])
            for key in ('coverage', 'unavailable_refs', 'canon_hold_refs', 'derived',
                        'narrative_consistency_verified', 'manuscript_language', 'language_resource',
                        'language_semantics_verified', 'saved_response_display'):
                self.assertEqual(working[key], full[key], key)
            self.assertEqual(working['unresolved_holds'][0]['affected_refs'], finding['affected_refs'])

    def test_explicit_global_finding_seeds_bounded_links_but_automatic_guard_does_not(self):
        with repository() as root:
            first = envelope(root)
            affected, unrelated = idea(first), idea(first)
            first = seal(dict(first, record_versions=[affected, unrelated]))
            storage.save(root, first)
            second = envelope(root, previous=first)
            second['messages'][0]['text'] = 'Defer the proposal.'
            source = {'type': 'message', 'exchange_id': second['exchange_id'],
                'message_id': second['messages'][0]['message_id']}
            decision = record(second, 'decision', action='defer', user_message_ref=source,
                span={'start': 0, 'end': 19}, target_refs=[{'id': affected['id']}],
                selected_parts=[], prior_refs=[], result_refs=[], reason='Defer proposal',
                affected_refs=[], review_required_refs=[], source_refs=[source], origin='supplied')
            finding = record(second, 'finding', category='knowledge', assessment='conflict',
                severity='significant', affected_refs=[{'id': affected['id']}],
                explanation='Unresolved timing', consequences=[], resolution_options=[],
                disposition='deferred', decision_ids=[decision['id']], narrative_explanation=None)
            storage.save(root, seal(dict(second, record_versions=[decision, finding])))
            for options in ({'focus': [finding['id']]}, {'query': 'Unresolved timing'}):
                with self.subTest(options=options):
                    data = read(root, view='working', limit=2, **options)['data']
                    self.assertCountEqual(data['records'], [finding, affected, decision])
                    self.assertEqual(data['retrieval']['outstanding_record_ids'], [])
                    self.assertEqual(data['omitted']['record_count'], 1)
                    limited = read(root, view='working', limit=1, **options)['data']
                    self.assertIn(finding, limited['records'])
                    retrieved = {r['id'] for r in limited['records']} - {finding['id']}
                    self.assertEqual(len(retrieved), 1)
                    self.assertEqual(set(limited['retrieval']['outstanding_record_ids']),
                        {affected['id'], decision['id']} - retrieved)
            automatic = read(root, view='working', focus=[unrelated['id']], limit=3)['data']
            self.assertCountEqual(automatic['records'], [unrelated, finding])
            self.assertEqual(set(automatic['retrieval']['outstanding_record_ids']),
                {affected['id'], decision['id']})

    def test_project_directions_and_exact_sourced_accepted_state(self):
        from novel_creator.install import bootstrap
        with repository() as root:
            novel_id = json.loads((root / '.novel-creator/manifest.json').read_text())['novel_id']
            first = bootstrap(json.dumps({'title': 'Bréf', 'manuscript_language': 'is',
                'creative_directions': ['Keep the ending uncertain.'],
                'workflow_preferences': {'questions': 'One at a time'}}), novel_id=novel_id)
            first['expected_git_head'] = storage.head(root)
            proposal = idea(first)
            first = seal(dict(first, record_versions=[*first['record_versions'], proposal]))
            storage.save(root, first)
            second = envelope(root, previous=first)
            second['messages'][0]['text'] = 'Accept the proposal.'
            source = {'type': 'message', 'exchange_id': second['exchange_id'],
                'message_id': second['messages'][0]['message_id']}
            decision = record(second, 'decision', action='accept', user_message_ref=source,
                span={'start': 0, 'end': 19}, target_refs=[{'id': proposal['id'], 'revision': 2}],
                selected_parts=[], prior_refs=[], result_refs=[], reason='Accept proposal',
                affected_refs=[], review_required_refs=[], source_refs=[source], origin='supplied')
            accepted = dict(proposal, revision=2, previous_revision=1, status='accepted',
                decision_ids=[decision['id']], source_refs=[source], origin='supplied')
            second = seal(dict(second, record_versions=[accepted, decision]))
            storage.save(root, second)
            data = read(root, view='working', focus=[accepted['id']], limit=2)['data']
            self.assertIn(accepted, data['records'])
            self.assertIn(decision, data['records'])
            self.assertEqual(data['project'], first['record_versions'][0])
            self.assertEqual(data['manuscript_language'], 'is')
            self.assertEqual(data['language_resource'], '.novel-creator/languages/is.md')
            self.assertEqual(data['retrieval']['outstanding_record_ids'], [])
            self.assertNotIn(second['exchange_id'], data['retrieval']['outstanding_record_ids'])
            self.assertNotIn(source['message_id'], data['retrieval']['outstanding_record_ids'])

    def test_session_navigation_is_compact_and_does_not_expand_all_related_records(self):
        with repository() as root:
            first, project, element, assertion, unrelated = self.fixture(root)
            second = envelope(root, previous=first)
            session = record(second, 'session', topic='Þóra', mode='guided', state='open',
                started_exchange_id=second['exchange_id'], last_exchange_id=second['exchange_id'],
                related_record_ids=[element['id'], *[r['id'] for r in unrelated]],
                unresolved_question_ids=[], derived_context_ref='local/old-summary.md')
            second = seal(dict(second, session_id=session['id'], record_versions=[session]))
            storage.save(root, second)
            focused = read(root, view='working', focus=[element['id']], limit=3)['data']
            self.assertEqual({r['id'] for r in focused['records']}, {element['id'], assertion['id']})
            self.assertNotIn('related_record_ids', focused['session_summary'])
            selected_session = read(root, view='working', focus=[session['id']], limit=3)['data']
            self.assertEqual(selected_session['records'], [session])
            self.assertEqual(set(selected_session['retrieval']['outstanding_record_ids']), set(session['related_record_ids']))
            fallback = read(root, view='working', session=session['id'], limit=3)['data']
            self.assertEqual(len(fallback['records']), 3)
            self.assertTrue(all(reason == 'latest_session_link' for identifier, reason in
                fallback['retrieval']['selection_reasons'].items() if identifier != project['id']))
            self.assertEqual(fallback['session_summary']['id'], session['id'])
            full = read(root, session=session['id'])['data']
            current = read(root, view='current', session=session['id'])['data']
            self.assertEqual(current['records'], full['records'])
            self.assertEqual(current['selected_session'], full['selected_session'])

    def test_cli_options_and_missing_focus_fail_clearly(self):
        with repository() as root:
            first = envelope(root)
            proposal = idea(first)
            storage.save(root, seal(dict(first, record_versions=[proposal])))
            for args in (['--focus', proposal['id']], ['--view', 'current', '--query', 'x'],
                         ['--view', 'working', '--limit', '0'], ['--view', 'working', '--limit', '101'],
                         ['--view', 'working', '--query', '  '], ['--view', 'working', '--focus', 'missing']):
                with self.subTest(args=args):
                    result = subprocess.run([sys.executable, '-m', 'novel_creator', 'context',
                        '--novel', str(root), '--json', *args], capture_output=True, text=True)
                    self.assertIn(result.returncode, (2, 4), result.stdout)
                    self.assertFalse(json.loads(result.stdout)['ok'])
            ok = subprocess.run([sys.executable, '-m', 'novel_creator', 'context', '--novel', str(root),
                '--view', 'working', '--focus', proposal['id'], '--limit', '1', '--json'], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertEqual(json.loads(ok.stdout)['data']['records'], [proposal])
            with self.assertRaises(ToolError) as caught:
                read(root, view='working', focus=['missing'])
            self.assertEqual(caught.exception.affected_refs, ['missing'])
            for options in ({'view': 'invalid'}, {'view': 'working', 'limit': True},
                            {'view': 'working', 'focus': proposal['id']}, {'limit': 2},
                            {'operation': 'inspect', 'view': 'working'},
                            {'view': 'working', 'focus': [proposal['id'], 'missing'], 'limit': 1},
                            {'view': 'working', 'identifier': proposal['id']}):
                with self.subTest(options=options), self.assertRaises(ToolError):
                    read(root, **options)

    def test_all_views_validate_damaged_history(self):
        with repository() as root:
            first = envelope(root)
            receipt = storage.save(root, first)
            broken = envelope(root, previous=first)
            relative = storage.bundle_path(broken)
            (root / relative).write_text('{}')
            git(root, 'add', relative)
            git(root, 'commit', '-m', 'Damaged successor fixture')
            for view in ('full', 'current', 'working'):
                with self.subTest(view=view), self.assertRaises(ToolError) as caught:
                    read(root, view=view)
                self.assertEqual(caught.exception.code, 4)
                self.assertEqual(caught.exception.checkpoint, receipt['checkpoint'])
