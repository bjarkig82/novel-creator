"""Recheck sourced authority observations; meaning labels are agent judgments."""
import json
from pathlib import Path
import sys

p = Path(__file__).resolve().parent
sys.path.insert(0, str(p.parents[3] / 'src'))
from novel_creator import records, storage

run = json.loads((p / 'run.json').read_bytes())
capture = json.loads((p / 'capture-proposition-assessment.json').read_bytes())
output = []
for lang, task in run['tasks'].items():
    history = storage.read_history(task['novel_path'])
    by_exchange = {e['exchange_id']: e for e in history}
    versions = {(r['id'], r['revision']): r for e in history for r in e['record_versions']}
    loaded = {name: json.loads((p / f'exchanges/{name}-{lang}.json').read_bytes())
              for name in ('AUTH_PARTIAL', 'AUTH_NONACCEPT', 'AUTH_REVISE', 'AUTH_PROTECTED')}
    for e in loaded.values():
        assert by_exchange[e['exchange_id']] == e
    # Ten independent designated acceptance groups plus storm and blue light.
    groups = [g for g in capture['languages'][lang]['designated_proposition_groups']
              if g['expected_status'] == 'accepted']
    assert len(groups) == 10
    accept = [dict(statements=g['observed_statements'], refs=g['record_refs']) for g in groups]
    partial = loaded['AUTH_PARTIAL']
    additions = [r for r in partial['record_versions'] if r['kind'] == 'idea'
                 and r['status'] == 'accepted' and r['revision'] == 2]
    assert len(additions) == 2
    accept += [dict(statements=[r['statement']], refs=[{'id': r['id'], 'revision': r['revision']}])
               for r in additions]
    negative = loaded['AUTH_NONACCEPT']
    assert not any(r['kind'] == 'decision' and r['action'] == 'accept' for r in negative['record_versions'])
    assert not any(r.get('status') == 'accepted' for r in negative['record_versions'])
    # An explicit reopening is a revision, not passive silence or acceptance.
    assert {r['action'] for r in negative['record_versions'] if r['kind'] == 'decision'} == {'reject', 'revise'}
    ideas = [r for r in negative['record_versions'] if r['kind'] == 'idea']
    assert len(ideas) >= 12 and len([r for r in ideas if r['status'] == 'rejected']) == 1
    revision = loaded['AUTH_REVISE']
    decisions = [r for r in revision['record_versions'] if r['kind'] == 'decision' and r['action'] == 'revise']
    assert len(decisions) == 5
    revisions = []
    for d in decisions:
        quote = revision['messages'][0]['text'][d['span']['start']:d['span']['end']]
        assert quote and d['prior_refs'] and d['result_refs'] and d['source_refs']
        prior = [versions[r['id'], r['revision']] for r in d['prior_refs']]
        result = [versions[r['id'], r['revision']] for r in d['result_refs']]
        assert any(r['kind'] == 'assertion' and r['status'] == 'accepted' for r in prior)
        assert any(r['kind'] == 'assertion' and r['status'] == 'accepted' for r in result)
        assert all(versions[r['id'], r['revision']] for r in d['affected_refs'])
        assert all(versions[r['id'], r['revision']] for r in d['review_required_refs'])
        revisions.append(dict(decision_id=d['id'], source_quote=quote, prior=prior, result=result,
                              directly_affected=d['affected_refs'], review_required=d['review_required_refs']))
    protected = loaded['AUTH_PROTECTED']
    assert not any(r['kind'] == 'decision' and r['action'] == 'accept' for r in protected['record_versions'])
    assert not any(r.get('status') == 'accepted' for r in protected['record_versions'])
    assert any(r['kind'] == 'finding' and r['disposition'] == 'open' for r in protected['record_versions'])
    assert any(r['kind'] == 'finding' and r['assessment'] == 'conflict'
               and r['severity'] == 'significant' and r['disposition'] == 'open'
               and r['affected_refs'] for r in protected['record_versions'])
    assert any(r['kind'] == 'question' and r['state'] == 'open' for r in protected['record_versions'])
    for name in ('AUTH_PARTIAL', 'AUTH_NONACCEPT', 'AUTH_REVISE', 'AUTH_PROTECTED'):
        e = loaded[name]
        # Verify the actual Git save touched only this exchange's managed bundle.
        report_case = 'AUTH_PARTIAL-recovery' if lang == 'is' and name == 'AUTH_PARTIAL' else name
        report = json.loads((Path(task['novel_path']) / f'.novel-creator/local/evidence/{report_case}-report.json').read_bytes())
        point = report['save_result']['checkpoint']
        paths = storage.git(task['novel_path'], 'diff-tree', '--no-commit-id', '--name-only', '-r', point['git_head']).decode().splitlines()
        assert paths == [storage.bundle_path(e)], paths
    settings = [r for r in revision['record_versions'] if r['kind'] == 'novel_project']
    assert settings[0]['review_preferences']['routine_checkpoint'] == 'session_close'
    assert any(r['kind'] == 'session' and r['state'] == 'closed' for r in revision['record_versions'])
    partial_settings = [r for r in partial['record_versions'] if r['kind'] == 'novel_project']
    assert partial_settings[0]['review_preferences']['routine_checkpoint'] == 'every_exchange'
    output.append(dict(language=lang, acceptance_groups=accept, nonacceptance_examples=12,
                       nonacceptance_ideas=ideas, deliberate_revisions=revisions,
                       protected_conflict_preserved=True, only_exchange_bundle_committed=True,
                       checkpoints=['on_request: CORRECTION', 'every_exchange: AUTH_PARTIAL',
                                    'session_close: AUTH_REVISE']))
result = dict(ok=True, source_type='delegated', native_user_input=False, novice_evidence=False,
              meaning_assessment='Parent agent judgment scoped to these supplied examples; no human literary score',
              results=output)
(p / 'authority-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(ok=True, languages=len(output), acceptance_groups_per_language=12,
                     nonacceptance_examples_per_language=12, deliberate_revisions_per_language=5)))
