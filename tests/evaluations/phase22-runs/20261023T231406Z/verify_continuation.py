"""Verify public source and display across an automatic app continuation.

Do not synthesize a completed original turn or combine turns into a fake turn.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

p = Path(__file__).resolve().parent
sys.path.insert(0, str(p.parents[3]))
from tests.evaluations.verify_phase22 import verify_input, verify_display, require
from novel_creator import storage

parser = argparse.ArgumentParser()
parser.add_argument('--case', required=True)
args = parser.parse_args()
run = json.loads((p / 'run.json').read_bytes())
driver = json.loads((p / f'{args.case}-driver.json').read_bytes())
results = []
for lang, task in run['tasks'].items():
    source = json.loads((p / f'{args.case}-{lang}-source-public.json').read_bytes())
    displayed = json.loads((p / f'{args.case}-{lang}-continued-public.json').read_bytes())
    require(source['thread']['id'] == displayed['thread']['id'] == task['thread_id'], 'Thread differs')
    require(len(source['turns']) == len(displayed['turns']) == 1, 'Expected two distinct actual turns')
    origin, continuation = source['turns'][0], displayed['turns'][0]
    require(origin['id'] != continuation['id'], 'Not a separate continuation turn')
    require(not any(i['type'] in ('userMessage', 'functionCallOutput') for i in continuation['items']),
            'Continuation contains a separate input; requires a different source assessment')
    require(not any(i['type'] == 'agentMessage' and i.get('phase') == 'final_answer'
                    for i in origin['items']), 'Original turn already displayed a final')
    history = storage.read_history(task['novel_path'])
    matches = [e for e in history if e['input_artifacts'] and
               e['input_artifacts'][0]['parsed_value'].get('turn_id') == origin['id'] and
               e['input_artifacts'][0]['parsed_value'].get('thread_id') == task['thread_id']]
    require(len(matches) == 1, 'Expected exactly one committed original exchange')
    exchange = matches[0]
    verify_input(source, exchange, expected=driver['inputs'][lang], thread_id=task['thread_id'],
                 parent=run['authorization']['parent_thread_id'])
    # Both sets of commentary are reviewed explicitly; original progress contains no story.
    source_review = json.loads((p / f'{args.case}-{lang}-source-commentary-review.json').read_bytes())
    comments = [i for i in origin['items'] if i['type'] == 'agentMessage' and i.get('phase') == 'commentary']
    require([(i['id'], i['text']) for i in comments] == [(i['id'], i['text']) for i in source_review],
            'Original progress review differs')
    require(all(i['classification'] in ('administrative', 'failure_disclosure') and i['reason']
                for i in source_review), 'Original unfinished turn contains creative disclosure')
    review = json.loads((p / f'{args.case}-{lang}-continued-commentary-review.json').read_bytes())
    point = verify_display(continuation, exchange, commentary_review=review)
    blob = storage.git(task['novel_path'], 'show', point['git_head'] + ':' + storage.bundle_path(exchange))
    require(json.loads(blob) == exchange, 'Observed checkpoint differs from committed exchange')
    for relative, digest in run['bundle_source_sha256'].items():
        require(hashlib.sha256((Path(task['novel_path']) / relative).read_bytes()).hexdigest() == digest,
                'Pinned bundle mismatch: ' + relative)
    (p / f'exchanges/{args.case}-{lang}.json').write_bytes(blob)
    results.append(dict(language=lang, source_turn=origin['id'], source_turn_observed_status=origin['status'],
                        completed_display_turn=continuation['id'], checkpoint=point,
                        original_source_preserved=True, exact_saved_display=True,
                        one_original_exchange=True, separate_continuation_has_no_new_input=True,
                        source_type='delegated', native_user_input=False, novice_evidence=False))
result = dict(ok=True, scope='Actual original input and separate completed continuation display only', results=results)
(p / f'continuation-verification-{args.case}.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result))
