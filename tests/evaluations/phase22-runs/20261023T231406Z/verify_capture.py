"""Compare actual automatic capture and fresh resumption with independent baselines.

The proposition mapping is an explicitly labeled parent-agent meaning judgment;
this script verifies its record references, states, source presence and recovery.
It does not turn those judgments into human approval or a literary-quality score.
"""
import json
from pathlib import Path
import sys

folder = Path(__file__).resolve().parent
root = folder.parents[3]
sys.path.insert(0, str(root / 'src'))
from novel_creator import records, storage

assessment = json.loads((folder / 'capture-proposition-assessment.json').read_bytes())
run = json.loads((folder / 'run.json').read_bytes())
results = []
for language, task in run['tasks'].items():
    fresh_case = run.get('fresh_cases', {}).get(language, 'FRESH_RESUME')
    driver = json.loads((folder / f'{fresh_case}-driver.json').read_bytes())
    baseline = json.loads((folder / f'pre-fresh-{language}.json').read_bytes())
    observed_context = json.loads((Path(task['novel_path']) /
        f'.novel-creator/local/evidence/{fresh_case}-pre-context.json').read_bytes())
    assert observed_context == baseline, 'Fresh host context differs from independent baseline'
    state = {r['id']: r for r in baseline['data']['records']}
    history = baseline['data']['exchanges']
    versions = {(r['id'], r['revision']): r for e in history for r in e['record_versions']}
    selected = assessment['languages'][language]
    assert len(selected['designated_proposition_groups']) == 20
    for group in selected['designated_proposition_groups']:
        for reference, statement in zip(group['record_refs'], group['observed_statements'], strict=True):
            original = versions[reference['id'], reference['revision']]
            assert original['statement'] == statement and original['source_refs']
            assert state[reference['id']]['status'] == group['expected_status']
    assert len(selected['observed_decision_refs']) >= 10
    for reference in selected['observed_decision_refs']:
        decision = state[reference['id']]
        assert decision['action'] == 'accept' and decision['source_refs']
        assert decision['user_message_ref']['type'] == 'message'
    assert len(selected['question_refs']) == 5
    session_map = {s['id']: s for s in baseline['data']['sessions']}
    assert len(session_map) == 3
    for reference in selected['session_refs']:
        session = session_map[reference['id']]
        assert session['topic'] == reference['topic'] and session['mode'] == reference['mode']
    for reference in selected['question_refs']:
        question = state[reference['id']]
        assert question['text'] == reference['text'] and question['state'] == 'open' and question['source_refs']
        assert any(question['id'] in session['unresolved_question_ids'] for session in session_map.values())
    alternatives = [r for r in state.values() if r['kind'] == 'idea' and r['status'] == 'unresolved']
    assert len(alternatives) >= 2 and len({r['alternative_group_id'] for r in alternatives}) == 1
    corrected_ref = selected['designated_proposition_groups'][4]['record_refs'][0]
    corrected = state[corrected_ref['id']]
    assert corrected['revision'] == 2 and corrected['previous_revision'] == 1
    assert corrected['statement'] != versions[corrected['id'], 1]['statement']
    assert corrected['status'] == 'proposed'
    correction = json.loads((folder / f'exchanges/CORRECTION-{language}.json').read_bytes())
    assert any(r['kind'] == 'decision' and r['action'] == 'correct' for r in correction['record_versions'])
    assert {'idea', 'assertion', 'story_element', 'relationship', 'decision', 'question', 'session'} <= {
        r['kind'] for r in state.values()}
    assert {'character', 'location', 'event', 'plot_thread'} <= {
        r.get('element_type') for r in state.values() if r['kind'] == 'story_element'}
    resumed = json.loads((folder / f'exchanges/{fresh_case}-{language}.json').read_bytes())
    assert resumed['record_versions'] == []
    assert resumed['expected_git_head'] == baseline['checkpoint']['git_head']
    assert resumed['input_artifacts'][0]['parsed_value']['thread_id'] == driver['task_overrides'][language]['thread_id']
    points = [case['checkpoint'] for report in folder.glob('observation-verification*.json')
              for case in json.loads(report.read_bytes()).get('cases', [])
              if case['case_id'] == fresh_case and case['language'] == language
              and case['exchange_id'] == resumed['exchange_id']]
    assert points and all(point == points[0] for point in points)
    # Later authorized scenarios may advance this disposable novel. Judge this
    # resumption at its observed immutable save checkpoint, not a later HEAD.
    current = records.fold(storage.read_history(task['novel_path'], points[0]['git_head']))
    assert current == state, 'Fresh resumption changed creative records'
    reply = resumed['messages'][1]['text']
    for reference in selected['question_refs']:
        assert reference['id'][:8] in reply, 'Open question lacks a visible source citation'
    for group in selected['designated_proposition_groups']:
        assert all(r['id'][:8] in reply for r in group['record_refs']), 'Designated idea lacks a visible citation'
    results.append({'language': language, 'designated_proposition_groups': 20,
        'observed_accept_decision_records': len(selected['observed_decision_refs']), 'open_questions': 5,
        'sessions': 3, 'pre_save_context_exactly_matches_independent_baseline': True,
        'no_creative_record_changes_on_fresh_resume': True, 'correction_history_retained': True,
        'all_capture_record_kinds_observed': True, 'source_type': 'delegated',
        'native_user_input': False, 'novice_evidence': False})
output = {'ok': True, 'scope': 'Designated automated capture and actual fresh resumption only',
    'semantic_proposition_mapping': 'Separate parent-agent judgment; no human or arbitrary-extraction guarantee',
    'results': results}
(folder / 'capture-verification.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, indent=2))
