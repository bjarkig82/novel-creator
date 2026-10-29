"""Compare observed public events, committed exchanges and display ordering."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(root / 'src'))
from novel_creator import host_input, storage
from novel_creator.install import bundle_files

folder = Path(__file__).resolve().parent
run = json.loads((folder / 'run.json').read_bytes())
results = []
for language, task in run['tasks'].items():
    native = json.loads((folder / f'{language}-gate-native.json').read_bytes())
    turn = native['turns'][0]
    assert turn['status'] == 'completed'
    assert all(i['type'] != 'reasoning' for i in turn['items'])
    observed = host_input.capture(native, thread_id=task['thread_id'], turn_id=turn['id'],
        source='delegated', source_thread_id=run['authorization']['parent_thread_id'], evaluation_only=True)
    expected = task['gate_prompt']
    if language == 'is':
        expected = json.loads((folder / 'is-gate-retry-driver.json').read_bytes())['prompt']
    assert observed['text'] == expected
    novel = Path(task['novel_path'])
    history = storage.read_history(novel)
    exchange = next(e for e in history if e['operation'] == 'conversation' and
                    e['input_artifacts'][0]['parsed_value']['turn_id'] == turn['id'])
    assert exchange['messages'][0]['text'] == observed['text']
    assert exchange['input_artifacts'][0]['parsed_value'] == observed['input_artifact']['parsed_value']
    assert exchange['messages'][1]['text'] == task['expected_response']
    finals = [(n, i) for n, i in enumerate(turn['items']) if i['type'] == 'agentMessage'
              and i.get('phase') == 'final_answer']
    assert len(finals) == 1 and finals[0][1]['text'] == task['expected_response']
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
            if (value.get('ok') is True and value.get('data', {}).get('saved') is True and
                    value.get('checkpoint', {}).get('exchange_id') == exchange['exchange_id']):
                saves.append((index, value))
    assert saves and any(index < finals[0][0] for index, _ in saves)
    for relative, raw in bundle_files().items():
        assert (novel / relative).read_bytes() == raw, relative
    manifest = json.loads((novel / '.novel-creator/manifest.json').read_bytes())
    for relative, digest in manifest['checksums'].items():
        assert hashlib.sha256((novel / relative).read_bytes()).hexdigest() == digest
    reopened = subprocess.run([sys.executable, '-I', '-B', str(novel / '.novel-creator/run.py'),
        'context', '--novel', str(novel), '--json'], capture_output=True, encoding='utf-8')
    assert reopened.returncode == 0, reopened.stderr
    context = json.loads(reopened.stdout)
    assert context['checkpoint']['exchange_id'] == history[-1]['exchange_id']
    exposed = next(e for e in context['data']['exchanges'] if e['exchange_id'] == exchange['exchange_id'])
    assert exposed['input_artifacts'] == exchange['input_artifacts']
    archives = folder / 'gate-bundles'
    archives.mkdir(exist_ok=True)
    raw = storage.git(novel, 'show', saves[-1][1]['checkpoint']['git_head'] + ':' + storage.bundle_path(exchange))
    (archives / f'{language}-exchange.json').write_bytes(raw)
    (archives / f'{language}-manifest.json').write_bytes((novel / '.novel-creator/manifest.json').read_bytes())
    (archives / f'{language}-gate.json').write_bytes((novel / '.novel-creator/local/evidence/delegated-gate.json').read_bytes())
    results.append({'language': language, 'thread_id': task['thread_id'], 'turn_id': turn['id'],
        'exchange_id': exchange['exchange_id'], 'checkpoint': saves[-1][1]['checkpoint'],
        'exact_observed_input_saved': True, 'exact_response_saved_and_displayed': True,
        'save_precedes_display': True, 'installed_bundle_matches_source': True,
        'fresh_cli_context_reopened': True, 'source_type': 'delegated',
        'native_user_input': False, 'novice_evidence': False})
output = {'ok': True, 'scope': 'observed delegated capture gates only', 'results': results}
(folder / 'gate-verification.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, indent=2))
