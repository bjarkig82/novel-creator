"""Verify saved/displayed delegated cases; semantic judgments remain separate."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(root / 'src'))
from novel_creator import host_input, storage

folder = Path(__file__).resolve().parent
run = json.loads((folder / 'run.json').read_bytes())
results = []
for driver in sorted(folder.glob('*-driver.json')):
    case = json.loads(driver.read_bytes())
    if 'case_id' not in case:
        continue
    for language, expected in case['inputs'].items():
        path = folder / f"{case['case_id']}-{language}-native.json"
        if not path.exists():
            continue
        native = json.loads(path.read_bytes())
        task = dict(run['tasks'][language])
        task['thread_id'] = case.get('thread_ids', {}).get(language, task['thread_id'])
        turn = native['turns'][0]
        assert turn['status'] == 'completed'
        assert all(i['type'] != 'reasoning' for i in turn['items'])
        observed = host_input.capture(native, thread_id=task['thread_id'], turn_id=turn['id'],
            source='delegated', source_thread_id=run['authorization']['parent_thread_id'], evaluation_only=True)
        assert observed['text'] == expected
        history = storage.read_history(task['novel_path'])
        matches = [e for e in history if e['operation'] == 'conversation' and
                   e['input_artifacts'] and e['input_artifacts'][0]['parsed_value']['turn_id'] == turn['id']]
        assert len(matches) == 1
        exchange = matches[0]
        assert exchange['messages'][0]['text'] == expected
        assert exchange['input_artifacts'][0]['parsed_value'] == observed['input_artifact']['parsed_value']
        finals = [(n, i) for n, i in enumerate(turn['items']) if i['type'] == 'agentMessage'
                  and i.get('phase') == 'final_answer']
        assert len(finals) == 1
        response = finals[0][1]['text']
        assert exchange['messages'][1]['text'] == response
        saves = []
        for index, item in enumerate(turn['items']):
            if item['type'] != 'commandExecution' or item.get('status') != 'completed':
                continue
            for line in item.get('output', {}).get('text', '').splitlines():
                try:
                    value = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(value, dict):
                    continue
                saved = (value.get('saved') is True or
                         (value.get('ok') is True and value.get('data', {}).get('saved') is True))
                if saved and value.get('checkpoint', {}).get('exchange_id') == exchange['exchange_id']:
                    saves.append((index, value['checkpoint']))
        assert saves and any(index < finals[0][0] for index, _ in saves)
        relative = storage.bundle_path(exchange)
        committed = json.loads(storage.git(task['novel_path'], 'show', saves[-1][1]['git_head'] + ':' + relative))
        assert committed == exchange
        archives = folder / 'case-bundles'
        archives.mkdir(exist_ok=True)
        (archives / f"{case['case_id']}-{language}.json").write_text(
            json.dumps(exchange, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        results.append({'case_id': case['case_id'], 'language': language, 'thread_id': task['thread_id'],
            'turn_id': turn['id'], 'exchange_id': exchange['exchange_id'], 'checkpoint': saves[-1][1],
            'exact_input_saved': True, 'exact_response_saved_and_displayed': True,
            'save_precedes_display': True, 'source_type': 'delegated', 'novice_evidence': False,
            'response': response, 'record_kinds': [r['kind'] for r in exchange['record_versions']],
            'session_changes': [{k: r.get(k) for k in ('id', 'mode', 'topic', 'status')}
                                for r in exchange['record_versions'] if r['kind'] == 'session']})
output = {'ok': True, 'scope': 'delegated case persistence and display only',
          'semantic_assessment': 'separately recorded agent judgment; no human ratings', 'cases': results}
(folder / 'case-verification.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, ensure_ascii=False, indent=2))
