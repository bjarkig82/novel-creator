"""Verify original delegated source and separate public recovery display."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from tests.evaluations.verify_phase22 import verify_input, verify_display, require
from novel_creator import storage

p = Path(__file__).resolve().parent
run = json.loads((p / 'run.json').read_bytes())
task = run['tasks']['is']
history = storage.read_history(task['novel_path'])
exchange = next(e for e in history if e['exchange_id'] == 'f785cc17-4d49-438c-878c-118229fddc0d')
pending = json.loads((p / 'authority-interruption/is/pending-receipt.json').read_bytes())
require(exchange['sequence'] == 8, 'Recovery added or changed sequence')
require(exchange == pending['bundle'], 'Recovery changed the preserved pending bundle')
original = json.loads((p / 'AUTH_PARTIAL-is-public.json').read_bytes())
recovery = json.loads((p / 'AUTH_PARTIAL-is-recovery-public.json').read_bytes())
expected = json.loads((p / 'AUTH_PARTIAL-driver.json').read_bytes())['inputs']['is']
verify_input(original, exchange, expected=expected, thread_id=task['thread_id'],
             parent=run['authorization']['parent_thread_id'])
review = [dict(id=i['id'], text=i['text'], classification='administrative',
               reason='Operational comparisons, diagnosis correction and recovery status only; no story content.')
          for i in recovery['turns'][0]['items']
          if i['type'] == 'agentMessage' and i.get('phase') == 'commentary']
point = verify_display(recovery['turns'][0], exchange, commentary_review=review)
blob = storage.git(task['novel_path'], 'show', point['git_head'] + ':' + storage.bundle_path(exchange))
require(json.loads(blob) == exchange, 'Recovery checkpoint differs from committed exchange')
require(len([e for e in history if e['exchange_id'] == exchange['exchange_id']]) == 1,
        'Pending exchange committed more than once')
payload = json.loads((p / 'authority-interruption/is/AUTH_PARTIAL-payload.json').read_bytes())
# Compare the preserved original prepared response, not a new recovery response.
require(payload['messages'] == exchange['messages'], 'Recovery changed original prepared conversation')
require(payload['input_artifacts'] == exchange['input_artifacts'], 'Recovery replaced original provenance')
manifest = json.loads((Path(task['novel_path']) / '.novel-creator/manifest.json').read_bytes())
for relative, digest in manifest['checksums'].items():
    require(hashlib.sha256((Path(task['novel_path']) / relative).read_bytes()).hexdigest() == digest,
            'Installed manifest mismatch: ' + relative)
for relative, digest in run['bundle_source_sha256'].items():
    require(hashlib.sha256((Path(task['novel_path']) / relative).read_bytes()).hexdigest() == digest,
            'Pinned bundle mismatch: ' + relative)
(p / 'AUTH_PARTIAL-is-recovery-commentary-review.json').write_text(
    json.dumps(review, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(p / 'exchanges/AUTH_PARTIAL-is.json').write_bytes(blob)
result = dict(ok=True, source_type='delegated', native_user_input=False, novice_evidence=False,
              original_turn=original['turns'][0]['id'], recovery_turn=recovery['turns'][0]['id'],
              checkpoint=point, original_input_and_provenance_preserved=True,
              original_prepared_response_unchanged=True, exact_recovered_display=True,
              original_failed_display_retained=True, single_original_exchange=True,
              installed_bundle_verified=True)
(p / 'recovery-verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result))
