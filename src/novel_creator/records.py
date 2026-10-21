"""Strict JSON, canonical digests and immutable full-revision folding."""
import copy
import hashlib
import json
import math
import re
import uuid
from datetime import datetime, timezone


BRIEF_FIELDS = ('genre', 'subgenres', 'audience', 'tone', 'style', 'perspective', 'complexity')


def preference(value=None, source=None, *, default=None):
    """Preserve supplied text and interpretation separately; never infer an answer."""
    if value is None or (isinstance(value, dict) and value.get('state') == 'unknown'):
        if isinstance(value, dict) and any(value.get(k) is not None for k in ('original_text', 'interpretation')):
            raise ValueError('An unknown preference cannot contain invented text')
        return {'state': 'default' if default is not None else 'unknown',
                'original_text': default, 'interpretation': None,
                'origin': 'system_default', 'source_refs': []}
    interpretation = None
    if isinstance(value, dict):
        if set(value) - {'state', 'original_text', 'interpretation'} or value.get('state') not in ('supplied', 'interpreted'):
            raise ValueError('Invalid preference input')
        interpretation = value.get('interpretation')
        value = value.get('original_text')
    if not isinstance(value, str) or (interpretation is not None and not isinstance(interpretation, str)):
        raise ValueError('Preferences require text or explicit unknown')
    return {'state': 'supplied', 'original_text': value, 'interpretation': interpretation,
            'origin': 'supplied', 'source_refs': [source] if source else []}


def project_from_brief(brief, exchange, artifact_id):
    if not isinstance(brief, dict) or set(brief) - {'title', 'original_concept', 'creative_brief',
            'manuscript_language', 'workflow_preferences', 'review_preferences', 'creative_directions'}:
        raise ValueError('Unknown brief field or non-object brief')
    creative = brief.get('creative_brief', {})
    workflow = brief.get('workflow_preferences', {})
    review = brief.get('review_preferences', {})
    if (not isinstance(creative, dict) or set(creative) - set(BRIEF_FIELDS) or
        not isinstance(workflow, dict) or not isinstance(review, dict) or
        set(review) - {'routine_checkpoint'}):
        raise ValueError('Invalid brief preferences')
    def source(path):
        return {'type': 'bootstrap_artifact', 'exchange_id': exchange['exchange_id'],
                'artifact_id': artifact_id, 'pointer': path}
    def pref(value, path, **kwargs):
        # Object input sources identify the original text, not an interpretation.
        pointer = path + '/original_text' if isinstance(value, dict) and value.get('state') != 'unknown' else path
        return preference(value, source(pointer), **kwargs)
    language = brief.get('manuscript_language', 'en')
    if not isinstance(language, str) or not re.fullmatch(r'[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8})*', language):
        raise ValueError('Manuscript language must be a BCP-47 language tag')
    checkpoint = review.get('routine_checkpoint', 'on_request')
    if checkpoint not in ('on_request', 'session_close', 'every_exchange'):
        raise ValueError('Invalid routine checkpoint')
    directions = brief.get('creative_directions', [])
    if not isinstance(directions, list) or not all(isinstance(d, str) for d in directions):
        raise ValueError('Creative directions must be text entries')
    return {'id': exchange['novel_id'], 'kind': 'novel_project', 'revision': 1,
            'previous_revision': None, 'created_exchange_id': exchange['exchange_id'],
            'source_refs': [source('')] if brief else [], 'origin': 'supplied' if brief else 'system_default',
            'title': pref(brief.get('title'), '/title', default='Untitled novel'),
            'original_concept': pref(brief.get('original_concept'), '/original_concept'),
            'creative_brief': {key: pref(creative.get(key), '/creative_brief/' + key) for key in BRIEF_FIELDS},
            'manuscript_language': language,
            'workflow_preferences': {key: pref(value, '/workflow_preferences/' + key.replace('~', '~0').replace('/', '~1'))
                                     for key, value in workflow.items()},
            'review_preferences': {'routine_checkpoint': checkpoint},
            'creative_directions': [{'text': value, 'source_refs': [source('/creative_directions/' + str(i))]}
                                    for i, value in enumerate(directions)]}


def revise_project(project, changes, exchange):
    """Prepare a settings revision; saving still validates the whole transition."""
    if not isinstance(changes, dict) or set(changes) - {'title', 'creative_brief', 'manuscript_language',
            'workflow_preferences', 'review_preferences', 'creative_directions'}:
        raise ValueError('Unknown setting; original concept and identity are immutable')
    users = [m for m in exchange['messages'] if m['role'] == 'user']
    if len(users) != 1:
        raise ValueError('Settings revision needs the current user message')
    source = {'type': 'message', 'exchange_id': exchange['exchange_id'], 'message_id': users[0]['message_id']}
    result = copy.deepcopy(project)
    result.update(revision=project['revision'] + 1, previous_revision=project['revision'],
                  source_refs=[source], origin='supplied')
    for key, value in changes.items():
        if key == 'title':
            result[key] = preference(value, source, default='Untitled novel')
        elif key in ('creative_brief', 'workflow_preferences'):
            if not isinstance(value, dict) or (key == 'creative_brief' and set(value) - set(BRIEF_FIELDS)):
                raise ValueError('Invalid preference changes')
            result[key].update({field: preference(answer, source) for field, answer in value.items()})
        elif key == 'creative_directions':
            if not isinstance(value, list) or not all(isinstance(d, str) for d in value):
                raise ValueError('Creative directions require text')
            result[key] = [{'text': text, 'source_refs': [source]} for text in value]
        else:
            result[key] = copy.deepcopy(value)
    return result


def new_exchange(novel_id, *, previous=None, expected_head=None, messages=None, session_id=None):
    result = {'schema_version': '1.0', 'novel_id': novel_id, 'exchange_id': str(uuid.uuid4()),
              'sequence': previous['sequence'] + 1 if previous else 1,
              'previous_exchange_id': previous['exchange_id'] if previous else None,
              'previous_digest': previous['payload_digest'] if previous else None,
              'session_id': session_id, 'expected_git_head': expected_head,
              'recorded_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
              'operation': 'conversation' if previous else 'bootstrap',
              'messages': messages or [], 'input_artifacts': [], 'record_versions': [],
              'continuity_review': {'coverage': 'not_applicable', 'reviewed_record_refs': [],
                  'unavailable_refs': [], 'canon_hold_refs': [], 'finding_ids': [],
                  'summary': 'Project settings only; no narrative consistency verdict'}}
    return result


def current_user_source(exchange):
    users = [m for m in exchange['messages'] if m['role'] == 'user']
    if exchange['operation'] != 'conversation' or len(users) != 1:
        raise ValueError('A current user conversation is required')
    return {'type': 'message', 'exchange_id': exchange['exchange_id'], 'message_id': users[0]['message_id']}


def checkpoint_summary(project, state, *, requested=False, session_closed=False):
    mode = project.get('review_preferences', {}).get('routine_checkpoint', 'on_request')
    if mode not in ('on_request', 'session_close', 'every_exchange'):
        raise ValueError('Invalid routine checkpoint')
    required = requested or mode == 'every_exchange' or (mode == 'session_close' and session_closed)
    return {'derived': True, 'required': required, 'pause_agent_exploration': required,
            'proposals': copy.deepcopy([r for r in state.values() if r.get('status') in ('proposed', 'unresolved')]),
            'decisions': copy.deepcopy([r for r in state.values() if r['kind'] == 'decision']),
            'open_questions': copy.deepcopy([r for r in state.values() if r['kind'] == 'question' and r['state'] == 'open'])}


def start_session(exchange, *, topic, mode='guided'):
    if not isinstance(topic, str) or mode not in ('guided', 'open'):
        raise ValueError('Invalid session topic or mode')
    return {'id': str(uuid.uuid4()), 'kind': 'session', 'revision': 1, 'previous_revision': None,
            'created_exchange_id': exchange['exchange_id'], 'origin': 'supplied',
            'source_refs': [current_user_source(exchange)], 'topic': topic, 'mode': mode,
            'state': 'open', 'started_exchange_id': exchange['exchange_id'],
            'last_exchange_id': exchange['exchange_id'], 'related_record_ids': [],
            'unresolved_question_ids': [], 'derived_context_ref': None}


def revise_session(session, exchange, *, reopen_requested=False, **changes):
    if set(changes) - {'topic', 'mode', 'state', 'related_record_ids', 'unresolved_question_ids'}:
        raise ValueError('Unknown session setting')
    if changes.get('mode', session['mode']) not in ('guided', 'open') or changes.get('state', session['state']) not in ('open', 'closed'):
        raise ValueError('Invalid session mode or state')
    if session['state'] == 'closed' and changes.get('state', 'closed') == 'open' and not reopen_requested:
        raise ValueError('Reopening requires explicit user direction')
    result = copy.deepcopy(session)
    result.update(changes)
    result.update(revision=session['revision'] + 1, previous_revision=session['revision'],
                  last_exchange_id=exchange['exchange_id'], origin='supplied',
                  source_refs=[current_user_source(exchange)])
    return result


def loads(raw):
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="strict")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result
    def constant(value):
        raise ValueError("Non-finite JSON number")
    def number(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError("Non-finite JSON number")
        return parsed
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def canonical_bytes(payload):
    return json.dumps({k: v for k, v in payload.items() if k != "payload_digest"},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(payload):
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def fold(history):
    """Return a detached current-state mapping; reject skipped predecessors."""
    state = {}
    for exchange in history:
        state.update(revision_updates(exchange, state))
    return state


def revision_updates(exchange, before, *, detach=True):
    """Validate and detach only this bundle's revisions; never mutate the prefix."""
    updates = {}
    for record in exchange['record_versions']:
        key = record['id']
        if key in updates:
            raise ValueError('Duplicate record ID in exchange')
        previous = before.get(key)
        if previous:
            if (record['revision'] != previous['revision'] + 1 or
                record['previous_revision'] != previous['revision'] or
                record['kind'] != previous['kind'] or
                record['created_exchange_id'] != previous['created_exchange_id']):
                raise ValueError('Invalid record predecessor or identity')
        elif (record['revision'] != 1 or record['previous_revision'] is not None or
              record['created_exchange_id'] != exchange['exchange_id']):
            raise ValueError('Invalid record creation')
        updates[key] = copy.deepcopy(record) if detach else record
    return updates
