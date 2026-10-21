"""Independent committed-record consumer. No production reducer or prose extraction."""
import hashlib
import json
from pathlib import Path
import subprocess


def _git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise ValueError('Committed snapshot is unavailable')
    return result.stdout


def _loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError('Nonfinite JSON')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=nonfinite)


def reconstruct(root):
    root = Path(root)
    commit = _git(root, 'rev-parse', '--verify', 'HEAD').decode().strip()
    names = _git(root, 'ls-tree', '-r', '--name-only', '-z', commit, '--', 'story/exchanges').split(b'\0')
    records, versions, history = {}, {}, []
    novel = None
    previous = None
    messages, artifacts, exchange_ids = {}, {}, set()
    for raw_name in sorted(name for name in names if name):
        name = raw_name.decode('utf-8')
        value = _loads(_git(root, 'show', commit + ':' + name))
        if not isinstance(value, dict) or value.get('schema_version') != '1.0':
            raise ValueError('Unsupported or malformed envelope')
        digest = hashlib.sha256(json.dumps({k: v for k, v in value.items() if k != 'payload_digest'},
            sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()
        if digest != value['payload_digest']:
            raise ValueError('Invalid digest')
        if value['sequence'] != len(history) + 1:
            raise ValueError('Broken sequence')
        if (not history and value['operation'] != 'bootstrap') or (history and value['operation'] == 'bootstrap'):
            raise ValueError('Invalid bootstrap boundary')
        if value['previous_exchange_id'] != (previous['exchange_id'] if previous else None):
            raise ValueError('Broken predecessor')
        if value['previous_digest'] != (previous['payload_digest'] if previous else None):
            raise ValueError('Broken digest chain')
        if novel is None:
            novel = value['novel_id']
        if value['novel_id'] != novel:
            raise ValueError('Cross-novel envelope')
        expected = f"story/exchanges/{value['sequence']:06d}-{value['exchange_id']}.json"
        if name != expected:
            raise ValueError('Exchange filename mismatch')
        pending = {}
        exchange_ids.add(value['exchange_id'])
        for message in value['messages']:
            messages[(value['exchange_id'], message['message_id'])] = message
        for artifact in value['input_artifacts']:
            if hashlib.sha256(artifact['original_text'].encode('utf-8')).hexdigest() != artifact['digest']:
                raise ValueError('Invalid artifact digest')
            if _loads(artifact['original_text'].encode('utf-8')) != artifact['parsed_value']:
                raise ValueError('Invalid artifact value')
            artifacts[(value['exchange_id'], artifact['artifact_id'])] = artifact
        for record in value['record_versions']:
            identifier = record['id']
            if identifier in pending:
                raise ValueError('Duplicate record revision')
            prior = records.get(identifier)
            if record['revision'] != (prior['revision'] + 1 if prior else 1):
                raise ValueError('Invalid revision')
            if record['previous_revision'] != (prior['revision'] if prior else None):
                raise ValueError('Invalid prior revision')
            if prior and (record['kind'] != prior['kind'] or record['created_exchange_id'] != prior['created_exchange_id']):
                raise ValueError('Changed record identity')
            if not prior and record['created_exchange_id'] != value['exchange_id']:
                raise ValueError('Invalid creation exchange')
            pending[identifier] = record
        available = {**records, **pending}

        def check_refs(item):
            if isinstance(item, list):
                for child in item:
                    check_refs(child)
            elif isinstance(item, dict):
                if item.get('type') == 'message':
                    message = messages.get((item['exchange_id'], item['message_id']))
                    if message is None:
                        raise ValueError('Missing source message')
                    if 'range' in item and not 0 <= item['range']['start'] < item['range']['end'] <= len(message['text']):
                        raise ValueError('Invalid source span')
                elif item.get('type') == 'bootstrap_artifact':
                    artifact = artifacts.get((item['exchange_id'], item['artifact_id']))
                    if artifact is None:
                        raise ValueError('Missing source artifact')
                    target = artifact['parsed_value']
                    path = item['pointer']
                    if path and not path.startswith('/'):
                        raise ValueError('Invalid artifact pointer')
                    try:
                        for token in path.split('/')[1:]:
                            token = token.replace('~1', '/').replace('~0', '~')
                            target = target[int(token)] if isinstance(target, list) else target[token]
                    except (KeyError, IndexError, ValueError, TypeError) as error:
                        raise ValueError('Missing artifact pointer') from error
                elif 'id' in item and set(item).issubset({'id', 'revision'}):
                    identifier = item['id']
                    candidates = versions.get(identifier, []) + ([pending[identifier]] if identifier in pending else [])
                    if identifier not in available or ('revision' in item and not any(
                            r['revision'] == item['revision'] for r in candidates)):
                        raise ValueError('Missing record revision')
                for key, child in item.items():
                    if key.endswith('_ids') and key != 'alternative_group_ids':
                        if any(identifier not in available for identifier in child):
                            raise ValueError('Missing record ID')
                    elif key in ('from_element_id', 'to_element_id', 'subject_element_id', 'holder_id', 'resolution_decision_id'):
                        if child is not None and child not in available:
                            raise ValueError('Missing record ID')
                    elif key in ('created_exchange_id', 'started_exchange_id', 'last_exchange_id'):
                        if child not in exchange_ids:
                            raise ValueError('Missing exchange ID')
                    check_refs(child)

        # Same-bundle forward references are valid, but no partial state escapes
        # if any record in the bundle has an unavailable origin or dependency.
        for record in pending.values():
            check_refs(record)
        records.update(pending)
        for identifier, record in pending.items():
            versions.setdefault(identifier, []).append(record)
        history.append(value)
        previous = value
    if not history:
        raise ValueError('No confirmed exchange history')
    return {'checkpoint': {'git_head': commit, 'sequence': len(history), 'exchange_id': previous['exchange_id']},
            'novel_id': novel, 'records': records, 'versions': versions, 'exchanges': history,
            'current_canon': [r for r in records.values() if r.get('status') == 'accepted']}
