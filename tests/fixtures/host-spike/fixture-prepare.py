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
user_input = p.add_mutually_exclusive_group(required=True)
user_input.add_argument('--user-file')
user_input.add_argument('--user-message-file')
p.add_argument('--response-file', required=True)
args = p.parse_args()
try:
    if args.user_message_file:
        message = records.loads(Path(args.user_message_file).read_bytes())
        if (not isinstance(message, dict) or message.get('type') != 'userMessage' or
            not isinstance(message.get('id'), str) or not message['id'] or
            not isinstance(message.get('content'), list) or len(message['content']) != 1 or
            not isinstance(message['content'][0], dict) or
            message['content'][0].get('type') != 'text' or
            not isinstance(message['content'][0].get('text'), str)):
            raise ValueError('Not a single native user text message')
        # Preserve the native text verbatim. The JSON file's own final newline
        # is outside this string and must not be added to the story message.
        user_text = message['content'][0]['text']
    else:
        user_text = Path(args.user_file).read_bytes().decode('utf-8')
except (OSError, ValueError, TypeError) as error:
    p.error('User input must be readable UTF-8 text or one native userMessage with one text input')
root = Path(__file__).resolve().parents[2]
history = storage.read_history(root)
previous = history[-1]
identifier = str(uuid.uuid4())
bundle = {'schema_version': '1.0', 'novel_id': previous['novel_id'], 'exchange_id': identifier,
          'sequence': previous['sequence'] + 1, 'previous_exchange_id': previous['exchange_id'],
          'previous_digest': previous['payload_digest'], 'session_id': None,
          'expected_git_head': storage.head(root), 'recorded_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
          'operation': 'conversation', 'messages': [
           {'message_id': str(uuid.uuid4()), 'role': 'user', 'text': user_text},
           {'message_id': str(uuid.uuid4()), 'role': 'assistant',
            'text': Path(args.response_file).read_bytes().decode('utf-8')}],
          'input_artifacts': [], 'record_versions': [], 'continuity_review': {'coverage': 'not_applicable',
          'reviewed_record_refs': [], 'unavailable_refs': [], 'canon_hold_refs': [], 'finding_ids': [],
          'summary': 'Host protocol fixture only; no canon or narrative judgment'}}
bundle['payload_digest'] = records.digest(bundle)
payload = root / '.novel-creator/local' / (identifier + '.payload')
payload.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'fixture_only': True, 'payload_file': str(payload)}))
