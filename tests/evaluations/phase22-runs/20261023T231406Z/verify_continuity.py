"""Check continuity records behind separately reviewed actual host replies."""
import json
from pathlib import Path
import sys

p = Path(__file__).resolve().parent
sys.path.insert(0, str(p.parents[3] / 'src'))
from novel_creator import records, storage

run = json.loads((p / 'run.json').read_bytes())
names = ('CONT_SETUP', 'CONT_CONFLICTS', 'CONT_DISPOSITIONS', 'CONT_DEFERRED',
         'CONT_UNAVAILABLE', 'CONT_REVALIDATE', 'CONT_RESOLVE')
expected = dict(motivation='rejected_idea', chronology='revised_idea', knowledge='revised_canon',
                plot_dependency='revised_idea', world_rule='intentional', relationship='deferred')
results = []
for lang, task in run['tasks'].items():
    history = storage.read_history(task['novel_path'])
    cases = {name: json.loads((p / f'exchanges/{name}-{lang}.json').read_bytes()) for name in names}
    for case in cases.values():
        assert sum(e == case for e in history) == 1
    def state_at(name):
        position = next(n for n, e in enumerate(history) if e['exchange_id'] == cases[name]['exchange_id'])
        return records.fold(history[:position + 1])
    initial = state_at('CONT_SETUP')
    conflict = state_at('CONT_CONFLICTS')
    for rid, r in initial.items():
        if r.get('status') == 'accepted':
            assert conflict[rid] == r, 'Conflict response silently changed prior canon'
    findings = {r['category']: r for r in cases['CONT_CONFLICTS']['record_versions'] if r['kind'] == 'finding'}
    assert set(findings) == set(expected) and len(findings) == 6
    for r in findings.values():
        assert r['assessment'] == 'conflict' and r['severity'] == 'significant' and r['disposition'] == 'open'
        assert r['explanation'] and r['consequences'] and r['resolution_options'] and r['affected_refs']
        assert any(s.get('exchange_id') == cases['CONT_CONFLICTS']['exchange_id'] for s in r['source_refs'])
        assert any(s.get('exchange_id') != cases['CONT_CONFLICTS']['exchange_id'] for s in r['source_refs'])
    resolved = state_at('CONT_DISPOSITIONS')
    dispositions = []
    for category, original in findings.items():
        current = resolved[original['id']]
        assert current['disposition'] == expected[category] and current['revision'] == original['revision'] + 1
        assert current['decision_ids'] and current['source_refs']
        if category == 'relationship':
            assert current['affected_refs'] == original['affected_refs'], 'Deferral lost original hold scope'
        if category == 'world_rule':
            assert current['narrative_explanation'], 'Intentional discrepancy lacks a technique'
        dispositions.append(dict(category=category, original=original, disposition=current))
    opportunity = [r for r in cases['CONT_DISPOSITIONS']['record_versions'] if r['kind'] == 'finding'
                   and r['assessment'] == 'opportunity']
    assert opportunity and all(r['severity'] == 'advisory' and r['source_refs'] for r in opportunity)
    assertions = [r for r in cases['CONT_DISPOSITIONS']['record_versions'] if r['kind'] == 'assertion']
    unknown = [r for r in assertions if r['perspective'] == 'character_knowledge' and r['truth_state'] == 'unknown']
    assert unknown and all(r['time_ref']['chronology']['start'] is None and
                           r['time_ref']['chronology']['end'] is None for r in unknown)
    assert any(r['perspective'] == 'reader_revelation' and r['status'] == 'proposed' for r in assertions)
    relation = findings['relationship']['id']
    deferred = state_at('CONT_DEFERRED')
    assert deferred[relation] == resolved[relation], 'Unrelated proposal changed the deferred finding'
    assert any(r['kind'] == 'idea' and r['status'] == 'proposed'
               for r in cases['CONT_DEFERRED']['record_versions'])
    unavailable = cases['CONT_UNAVAILABLE']
    assert unavailable['continuity_review']['coverage'] == 'incomplete'
    assert unavailable['continuity_review']['unavailable_refs']
    assert unavailable['continuity_review']['canon_hold_refs']
    assert not any(r.get('status') == 'accepted' for r in unavailable['record_versions'])
    restored = cases['CONT_REVALIDATE']
    assert not restored['continuity_review']['unavailable_refs']
    assert '*' not in restored['continuity_review']['canon_hold_refs']
    evidence = Path(task['novel_path']) / '.novel-creator/local/evidence'
    pre_context = json.loads((evidence / 'CONT_REVALIDATE-context.json').read_bytes())
    pre_validation = json.loads((evidence / 'CONT_REVALIDATE-validation.json').read_bytes())
    assert pre_context['ok'] and pre_context['data']['selected_session']['id'] == cases['CONT_SETUP']['session_id']
    assert pre_context['checkpoint']['git_head'] == pre_validation['checkpoint']['git_head'] == restored['expected_git_head']
    assert pre_validation['ok'] and pre_validation['data']['valid']
    prefix = history[:next(n for n, e in enumerate(history) if e['exchange_id'] == restored['exchange_id'])]
    assert pre_context['data']['exchanges'] == prefix
    prior_state = records.fold(prefix)
    assert all(prior_state[r['id']] == r for r in pre_context['data']['records'])
    public = json.loads((p / f'CONT_REVALIDATE-{lang}-public.json').read_bytes())
    observed = []
    for index, item in enumerate(public['turns'][0]['items']):
        if item['type'] != 'commandExecution' or item.get('exitCode') != 0 or item.get('output', {}).get('truncated'):
            continue
        for line in item.get('output', {}).get('text', '').splitlines():
            try:
                value = json.loads(line)
            except ValueError:
                continue
            if isinstance(value, dict):
                observed.append((index, value))
    saved_at = min(n for n, v in observed if v.get('data', {}).get('saved') is True
                   and v.get('checkpoint', {}).get('exchange_id') == restored['exchange_id'])
    assert any(n < saved_at and v == pre_validation for n, v in observed), 'Validation not observed before hold-clearing save'
    archive = p / 'revalidation-evidence'
    archive.mkdir(exist_ok=True)
    for name in ('context', 'validation'):
        (archive / f'{lang}-{name}.json').write_bytes((evidence / f'CONT_REVALIDATE-{name}.json').read_bytes())
    # Icelandic conservatively retains incomplete coverage for other open
    # findings. The corrected lookup must release only its wildcard hold.
    restored_state = state_at('CONT_REVALIDATE')
    remaining_holds = {ref['id'] for r in restored_state.values() if r['kind'] == 'finding'
                       and r['assessment'] == 'conflict' and r['severity'] == 'significant'
                       and r['disposition'] in ('open', 'deferred') for ref in r['affected_refs']}
    assert set(restored['continuity_review']['canon_hold_refs']) <= remaining_holds
    assert state_at('CONT_REVALIDATE')[relation]['disposition'] == 'deferred'
    final = state_at('CONT_RESOLVE')[relation]
    assert final['disposition'] == 'intentional' and final['narrative_explanation'] and final['decision_ids']
    # A general resolution disposition closes an actual recorded advisory finding.
    assert any(r['kind'] == 'finding' and r['disposition'] == 'resolved'
               for r in cases['CONT_RESOLVE']['record_versions'])
    results.append(dict(language=lang, six_categories=dispositions, advisory_opportunities=opportunity,
                        unknown_knowledge=unknown, deferred_scope_persisted=True,
                        unavailable_context_held=True, corrected_session_revalidated=True,
                        final_intentional_resolution=final,
                        unavailable_scope='Actual missing session lookup; damaged-history faults remain separate structural evidence'))
result = dict(ok=True, source_type='delegated', native_user_input=False, novice_evidence=False,
              meaning_assessment='Scoped parent-agent judgments of these actual replies; no human literary qualification',
              results=results)
(p / 'continuity-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(ok=True, languages=len(results), significant_categories_per_language=6,
                     user_dispositions=['rejected_idea', 'revised_idea', 'revised_canon', 'intentional', 'deferred', 'resolved'])))
