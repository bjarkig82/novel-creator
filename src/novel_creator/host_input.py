"""Explicit public host-input parsing; source labels are evidence, not authority."""
import hashlib
import json
import re
import uuid


DELEGATION = re.compile(
    r'\A<codex_delegation>\r?\n  <source_thread_id>([^<>\r\n]+)</source_thread_id>'
    r'\r?\n  <input>(.*)</input>\r?\n</codex_delegation>\Z', re.DOTALL)
TOOLS = ('create_thread', 'send_message_to_thread')


def validate_provenance(value, user_text):
    """Check an evidence artifact without making it a creative source authority."""
    try:
        if not isinstance(value, dict) or value.get('kind') != 'host_input':
            raise ValueError('Only host-input evidence is allowed in a conversation artifact')
        rebuilt = capture({'thread': {'id': value['thread_id']}, 'turns': [
            {'id': value['turn_id'], 'items': [value['public_event']]}]},
            thread_id=value['thread_id'], turn_id=value['turn_id'], source=value['source_type'],
            source_thread_id=value['source_thread_id'], evaluation_only=value['evaluation_only'])
        if rebuilt['input_artifact']['parsed_value'] != value or rebuilt['text'] != user_text:
            raise ValueError('Host-input provenance differs from the current message or source')
    except (KeyError, TypeError) as error:
        raise ValueError('Unreadable host-input provenance') from error


def capture(snapshot, *, thread_id, turn_id, source, source_thread_id=None, evaluation_only=False):
    """Parse only the explicitly named newest public turn; never infer a fallback."""
    try:
        if (source not in ('native_user', 'delegated') or not thread_id or not turn_id or
                not isinstance(snapshot, dict) or snapshot.get('truncated', False) or
                snapshot['thread']['id'] != thread_id):
            raise ValueError('Input source or current thread mismatch')
        turns = snapshot['turns']
        if (not isinstance(turns, list) or len(turns) != 1 or turns[0]['id'] != turn_id or
                turns[0].get('truncated', False)):
            raise ValueError('Current turn unavailable; older turns cannot substitute')
        items = turns[0]['items']
        if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
            raise ValueError('Unreadable public items')
        candidates = [i for i in items if i.get('type') == 'userMessage' or
                      (i.get('type') == 'functionCallOutput' and i.get('name') in TOOLS)]
        if len(candidates) != 1:
            raise ValueError('Expected exactly one unambiguous current input event')
        event = candidates[0]
        if (not isinstance(event.get('id'), str) or not event['id'] or
                event.get('truncated', False)):
            raise ValueError('Input event ID unavailable or event truncated')
        if source == 'native_user':
            content = event.get('content')
            if (event['type'] != 'userMessage' or not isinstance(content, list) or len(content) != 1 or
                    not isinstance(content[0], dict) or content[0].get('type') != 'text' or
                    content[0].get('truncated', False) or not isinstance(content[0].get('text'), str)):
                raise ValueError('Expected one complete native user text input')
            text = content[0]['text']
            public = {'type': 'userMessage', 'id': event['id'], 'content': [{'type': 'text', 'text': text}]}
        else:
            if not evaluation_only or not isinstance(source_thread_id, str) or not source_thread_id:
                raise ValueError('Delegation requires evaluation-only opt-in and expected source thread')
            output = event.get('output')
            if (event['type'] != 'functionCallOutput' or event.get('namespace') != 'codex_app' or
                    event.get('name') not in TOOLS or not isinstance(output, dict) or
                    output.get('truncated', False) or not isinstance(output.get('text'), str)):
                raise ValueError('Expected complete supported delegation output')
            raw = output['text']
            match = DELEGATION.fullmatch(raw)
            if (not match or match[1] != source_thread_id or
                    any(raw.count(tag) != 1 for tag in ('<input>', '</input>',
                        '<source_thread_id>', '</source_thread_id>',
                        '<codex_delegation>', '</codex_delegation>'))):
                raise ValueError('Malformed, ambiguous or unexpected delegation wrapper')
            text = match[2]
            public = {'type': event['type'], 'id': event['id'], 'namespace': 'codex_app',
                      'name': event['name'], 'output': {'text': raw, 'truncated': False}}
        provenance = {'kind': 'host_input', 'source_type': source, 'thread_id': thread_id,
                      'turn_id': turn_id, 'event_id': event['id'], 'event_type': event['type'],
                      'source_thread_id': source_thread_id if source == 'delegated' else None,
                      'native_user_input': source == 'native_user', 'novice_evidence': False,
                      'evaluation_only': source == 'delegated', 'text': text, 'public_event': public}
        original = json.dumps(provenance, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
        artifact = {'artifact_id': str(uuid.uuid4()), 'original_text': original,
                    'parsed_value': provenance, 'digest': hashlib.sha256(original.encode('utf-8')).hexdigest()}
        return {'text': text, 'source_type': source, 'input_artifact': artifact}
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError('Unreadable current public host input') from error
