"""Independently verify the exported public native events, without hidden data."""
import hashlib
import json
from pathlib import Path


folder = Path(__file__).resolve().parent
run = json.loads((folder / 'run.json').read_text(encoding='utf-8-sig'))
rows = []
for language in ('en', 'is'):
    task = run['tasks'][language]
    inventory = json.loads((folder / f'{language}-task-inventory.json').read_text(encoding='utf-8-sig'))
    assert all(not ({'.git', '.novel-creator', 'story'} &
                   set(item['relative_path'].replace('\\', '/').split('/')))
               for item in inventory)
    for phase, tool in (('creation', 'create_thread'), ('followup', 'send_message_to_thread')):
        path = folder / f'{language}-{phase}-native.json'
        native = json.loads(path.read_text(encoding='utf-8-sig'))
        assert native['thread']['id'] == task['threadId']
        assert len(native['turns']) == 1
        turn = native['turns'][0]
        assert turn['status'] == 'completed'
        assert all(item['type'] != 'reasoning' for item in turn['items'])
        assert not [item for item in turn['items'] if item['type'] == 'userMessage']
        delegated = [item for item in turn['items'] if item['type'] == 'functionCallOutput']
        assert len(delegated) == 1 and delegated[0]['name'] == tool
        output = delegated[0]['output']
        assert not output.get('truncated', False)
        text = output['text']
        assert text.count('<input>') == text.count('</input>') == 1
        observed_input = text.split('<input>', 1)[1].split('</input>', 1)[0]
        intended = (task['initial_prompt'] if phase == 'creation' else
                    (folder / f'{language}-followup-driver-prompt.txt').read_bytes().decode('utf-8'))
        assert observed_input == intended
        assert f"<source_thread_id>{run['authorization']['parent_thread_id']}</source_thread_id>" in text
        report = json.loads((folder / f'{language}-{phase}-gate-report.json').read_text(encoding='utf-8-sig'))
        assert report['status'] == 'gate_unavailable'
        assert report['task_thread_id'] == task['threadId']
        assert report.get('current_native_turn_id', report.get('native_turn_id')) == turn['id']
        assert report.get('conversation_saved') is not True
        assert report.get('initialization_performed', report.get('novel_initialized')) is not True
        rows.append({'language': language, 'phase': phase, 'thread_id': task['threadId'],
                     'turn_id': turn['id'], 'source_type': 'functionCallOutput', 'source_tool': tool,
                     'native_user_messages': 0, 'delegated_input_matches_driver': True,
                     'capture_gate_passed': False, 'semantic_cases_executed': 0})

files = sorted(path for path in folder.iterdir() if path.is_file() and
               path.name not in ('capture-boundary-verification.json', 'manifest.json',
                                 'boundary-verifier-output.txt', 'README.md'))
result = {'verification_ok': True, 'scope': 'Observed delegated-input boundary only',
          'tasks_created': 2, 'fresh_resumption_tasks_created': 0,
          'native_capture_gate_passed': False, 'novels_initialized': 0,
          'semantic_cases_executed': 0, 'human_or_novice_evidence': False,
          'probes': rows, 'sha256': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}}
(folder / 'capture-boundary-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
