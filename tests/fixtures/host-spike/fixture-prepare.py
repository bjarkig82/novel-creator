"""Fixture-only input preparation. Does not run a model or display conversation."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import sys
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parent))
from novel_creator import records, storage
p = argparse.ArgumentParser()
p.add_argument('--user-file', required=True)
p.add_argument('--response-file', required=True)
args = p.parse_args()
root = Path(__file__).resolve().parents[2]
history = storage.read_history(root)
previous = history[-1]
identifier = str(uuid.uuid4())
bundle = {'schema_version': '1.0', 'novel_id': previous['novel_id'], 'exchange_id': identifier,
          'sequence': previous['sequence'] + 1, 'previous_exchange_id': previous['exchange_id'],
          'previous_digest': previous['payload_digest'], 'session_id': None,
          'expected_git_head': storage.head(root), 'recorded_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
          'operation': 'conversation', 'messages': [
           {'message_id': str(uuid.uuid4()), 'role': role, 'text': Path(path).read_bytes().decode('utf-8')}
           for role, path in [('user', args.user_file), ('assistant', args.response_file)]],
          'input_artifacts': [], 'record_versions': [], 'continuity_review': {'coverage': 'not_applicable',
          'reviewed_record_refs': [], 'unavailable_refs': [], 'canon_hold_refs': [], 'finding_ids': [],
          'summary': 'Host protocol fixture only; no canon or narrative judgment'}}
bundle['payload_digest'] = records.digest(bundle)
payload = root / '.novel-creator/local' / (identifier + '.payload')
payload.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'fixture_only': True, 'payload_file': str(payload)}))
