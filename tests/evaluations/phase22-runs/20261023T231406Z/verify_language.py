"""Verify actual paired fixture spans and scoped agent-assessed outcomes."""
import json
from pathlib import Path
import sys

p = Path(__file__).resolve().parent
root = p.parents[3]
sys.path.insert(0, str(root / 'src'))
from novel_creator import records, storage

mapping = {
    'en': dict(sender='cbc84f52', married='010a1c3d', quote='c05518bd', conflict='2069408e', murder='100e9a66'),
    'is': dict(sender='141e3934', married='749bdc9a', quote='1e86a4a9', conflict='c372f461', murder='e2fa965c'),
}
phases = {'LANG_SETUP': ['L05'], 'LANG_GUIDANCE': ['L06'],
          'LANG_CAPTURE': ['L01', 'L02', 'L07', 'L08'], 'LANG_CONTINUITY': ['L03', 'L04']}
results = []
for lang, selected in mapping.items():
    fixtures = {c['id']: c for c in json.loads((root / f'tests/fixtures/{lang}/language-pitfalls.json').read_bytes())['cases']}
    cases = {name: json.loads((p / f'exchanges/{name}-{lang}.json').read_bytes()) for name in phases}
    driver = json.loads((p / 'LANG_SETUP-driver.json').read_bytes())
    novel = driver['task_overrides'][lang]['novel_path']
    history = storage.read_history(novel)
    state = records.fold(history)
    def record(prefix, values):
        matches = [r for r in values if r['id'].startswith(prefix)]
        assert len(matches) == 1
        return matches[0]
    fixture_spans = []
    for phase, ids in phases.items():
        e = cases[phase]
        assert sum(old == e for old in history) == 1
        text = e['messages'][0]['text']
        for fixture_id in ids:
            f = fixtures[fixture_id]
            assert text.count(f['user_text']) == 1
            offset = text.index(f['user_text'])
            span = dict(start=offset + f['source_span']['start'], end=offset + f['source_span']['end'])
            assert text[span['start']:span['end']] == f['source_quote']
            fixture_spans.append(dict(id=fixture_id, phase=phase, source_quote=f['source_quote'], range=span,
                                      exchange_id=e['exchange_id'], message_id=e['messages'][0]['message_id']))
    capture = cases['LANG_CAPTURE']
    before = {r['id']: r for r in capture['record_versions']}
    sender_before = record(selected['sender'], before.values())
    married = record(selected['married'], state.values())
    quoted = record(selected['quote'], state.values())
    sender = state[sender_before['id']]
    finding = record(selected['conflict'], state.values())
    murder = record(selected['murder'], state.values())
    assert sender_before['status'] == 'proposed' and sender['status'] == 'accepted'
    assert married['status'] == 'accepted' and married['value'] == ('married' if lang == 'en' else 'gift')
    assert quoted['status'] == 'proposed' and murder['status'] == 'unresolved'
    assert finding['category'] == 'world_rule' and finding['assessment'] == 'conflict'
    assert finding['severity'] == 'significant' and finding['disposition'] == 'open'
    last = cases['LANG_CONTINUITY']
    assert [r for r in last['record_versions'] if r['kind'] == 'assertion' and r['status'] == 'accepted'] == [sender]
    decision = next(r for r in last['record_versions'] if r['kind'] == 'decision' and r['action'] == 'accept')
    partial = next(s for s in fixture_spans if s['id'] == 'L04')
    assert decision['span'] == partial['range'], 'Acceptance span includes unselected murder clause'
    engine = next(r for r in cases['LANG_SETUP']['record_versions'] if r['kind'] == 'assertion' and r['status'] == 'accepted')
    assert state[engine['id']] == engine, 'Fuel conflict changed the petrol-only canon'
    project = next(r for r in state.values() if r['kind'] == 'novel_project')
    assert project['manuscript_language'] == 'is'
    assert project['creative_brief']['genre']['state'] == 'unknown'
    assert project['creative_brief']['genre']['original_text'] is None
    # Judge the requested redirection in its next saved response. Later writer
    # notes about Þóra may legitimately redirect the same session again.
    assert any(r['kind'] == 'session' and r['mode'] == 'guided' and 'Æg' in r['topic']
               for r in cases['LANG_GUIDANCE']['record_versions'])
    questions = [r for r in cases['LANG_GUIDANCE']['record_versions'] if r['kind'] == 'question']
    assert questions and all(state[r['id']] == r for r in questions)
    source_quotes = []
    for e in cases.values():
        for r in e['record_versions']:
            for source in r['source_refs']:
                if source.get('exchange_id') == e['exchange_id'] and 'range' in source:
                    a, b = source['range']['start'], source['range']['end']
                    message = next(m for m in e['messages'] if m['message_id'] == source['message_id'])
                    source_quotes.append(dict(record_id=r['id'], revision=r['revision'], range=source['range'],
                                              quote=message['text'][a:b], role=message['role']))
    results.append(dict(fixture_variant=lang, fixtures=fixture_spans, source_quotes=source_quotes,
                        assessed_records=dict(sender_before=sender_before, sender_after=sender, married=married,
                                              possible_quote=quoted, fuel_conflict=finding, murder=murder),
                        actual_project=project, question_preserved=True))
result = dict(ok=True, source_type='delegated', native_user_input=False, novice_evidence=False,
              scope='Eight authored fixture inputs per language embedded in four actual saved director turns',
              meaning_assessment='Parent-agent interpretation of actual replies and records; human/subjective parity unmeasured',
              results=results)
(p / 'language-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(ok=True, fixture_variants=2, fixture_inputs_per_variant=8, actual_saved_exchanges=8)))
