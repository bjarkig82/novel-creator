"""Deterministic navigation over validated current records, never a fact store."""
import re
import unicodedata

from .cli import ToolError


def _normalize(text):
    return unicodedata.normalize('NFKC', text).casefold()


def validate_options(operation, view, focus, query, limit):
    if view not in ('full', 'current', 'working'):
        raise ToolError(2, 'Context view must be full, current or working')
    if operation != 'context' and (view != 'full' or focus is not None or query is not None or limit is not None):
        raise ToolError(2, 'Context view and retrieval options require context')
    if view != 'working' and (focus is not None or query is not None or limit is not None):
        raise ToolError(2, '--focus, --query and --limit require --view working')
    if focus is not None and (not isinstance(focus, (list, tuple)) or
            not all(isinstance(value, str) and value.strip() for value in focus)):
        raise ToolError(2, 'Focus must be a list of nonempty stable record IDs')
    if query is not None and (not isinstance(query, str) or not re.findall(r'\w+', _normalize(query))):
        raise ToolError(2, 'Query must contain searchable text')
    if limit is not None and (type(limit) is not int or not 1 <= limit <= 100):
        raise ToolError(2, 'Working retrieval limit must be an integer from 1 to 100')
    focus = list(dict.fromkeys(focus or []))
    limit = 12 if limit is None else limit
    if len(focus) > limit:
        raise ToolError(2, 'Explicit focus count exceeds retrieval limit; increase --limit or request fewer IDs',
                        affected_refs=focus)
    return focus, limit


# These are record relationships, not provenance or arbitrary UUID-looking text.
_SINGLE_LINKS = {'from_element_id', 'to_element_id', 'subject_element_id', 'holder_id',
                 'resolution_decision_id'}
_MULTI_LINKS = {'related_element_ids', 'assertion_ids', 'resulting_assertion_ids',
                'relationship_ids', 'decision_ids', 'unresolved_question_ids',
                'alternative_ids', 'related_record_ids'}
_PROVENANCE = {'source_refs', 'user_message_ref', 'created_exchange_id',
               'started_exchange_id', 'last_exchange_id'}


def _links(value):
    if isinstance(value, dict):
        if 'id' in value and set(value).issubset({'id', 'revision'}):
            yield value
            return
        for key, child in value.items():
            if key in _PROVENANCE:
                continue
            if key in _SINGLE_LINKS and child:
                yield {'id': child}
            elif key in _MULTI_LINKS:
                yield from ({'id': identifier} for identifier in child)
            else:
                yield from _links(child)
    elif isinstance(value, list):
        for child in value:
            yield from _links(child)


def _text(value):
    """Search saved field values, excluding IDs, provenance and schema metadata."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key in _PROVENANCE or key in ('id', 'kind', 'origin') or key.endswith(('_id', '_ids')):
                continue
            yield from _text(child)
    elif isinstance(value, list):
        for child in value:
            yield from _text(child)
    elif isinstance(value, str):
        yield _normalize(value)


def working(state, history, point, *, session, focus, query, limit):
    """Project complete current versions with bounded retrieval and explicit gaps.

    The project and active findings are global context outside the retrieval
    budget. Sessions are navigation: their broad related-record lists never
    participate in recursive expansion, even when a full session is requested.
    """
    missing = [identifier for identifier in focus if identifier not in state]
    if missing:
        raise ToolError(4, 'Requested focus record unavailable', checkpoint=point, affected_refs=missing)
    project = next((r for r in state.values() if r['kind'] == 'novel_project'), None)
    findings = [r for r in state.values() if r['kind'] == 'finding' and r['disposition'] in ('open', 'deferred')]
    global_ids = {r['id'] for r in findings}
    if project:
        global_ids.add(project['id'])
    # Recent revision order is obtained from the saved journal, not timestamps
    # or local summary files. Stable IDs break ties within the same exchange.
    changed = {r['id']: e['sequence'] for e in history for r in e['record_versions']}
    ordered = sorted(state, key=lambda identifier: (-changed[identifier], identifier))
    sessions = [state[identifier] for identifier in ordered if state[identifier]['kind'] == 'session']
    active_session = state[session] if session else next((state[e['session_id']] for e in reversed(history)
        if e['session_id'] is not None), sessions[0] if sessions else None)
    links = {identifier: list(_links(record)) if record['kind'] != 'session' else []
             for identifier, record in state.items()}
    outgoing = {identifier: {ref['id'] for ref in refs} for identifier, refs in links.items()}
    incoming = {identifier: set() for identifier in state}
    for identifier, targets in outgoing.items():
        for target in targets:
            if target in incoming:
                incoming[target].add(identifier)

    matches = []
    if query is not None:
        terms = re.findall(r'\w+', _normalize(query))
        matches = [identifier for identifier in ordered
                   if all(any(term in text for text in _text(state[identifier])) for term in terms)]
    reasons = {identifier: 'explicit_focus' for identifier in focus}
    seeds = list(focus)
    for identifier in matches:
        if identifier not in seeds:
            seeds.append(identifier)
            reasons[identifier] = 'unicode_lexical_query'
    if not focus and query is None:
        recent_session_ids = set(active_session['related_record_ids'] + active_session['unresolved_question_ids']) if active_session else set()
        for identifier in ordered:
            if identifier in recent_session_ids and identifier not in global_ids and state[identifier]['kind'] != 'session':
                seeds.append(identifier)
                reasons[identifier] = 'latest_session_link'
        for identifier in ordered:
            if identifier not in seeds and identifier not in global_ids and state[identifier]['kind'] != 'session':
                seeds.append(identifier)
                reasons[identifier] = 'recent_change'

    selected = []
    for identifier in seeds:
        if identifier not in global_ids and len(selected) < limit:
            selected.append(identifier)
    # Explicit/query-selected globals seed navigation without consuming the
    # retrieval budget. Automatically included guards remain nonexpanding.
    frontier = [identifier for identifier in seeds if identifier in global_ids or identifier in selected]
    # Expand both directions breadth first. Session navigation does not bridge
    # unrelated topics; omitted session links remain disclosed separately.
    index = 0
    while index < len(frontier) and len(selected) < limit:
        identifier = frontier[index]
        for relation, candidates in (('outgoing_record_link', outgoing[identifier]),
                                     ('incoming_record_link', incoming[identifier])):
            for candidate in sorted(candidates):
                if candidate in state and candidate not in global_ids and candidate not in selected and len(selected) < limit:
                    selected.append(candidate)
                    frontier.append(candidate)
                    reasons[candidate] = relation
        index += 1
    included = global_ids | set(selected)
    for identifier in global_ids:
        reasons[identifier] = 'global_project' if project and identifier == project['id'] else 'global_active_finding'
    outstanding = {target for identifier in included for target in outgoing[identifier] | incoming[identifier]
                   if target not in included}
    # Full session records preserve their navigation fields without recursively
    # expanding them. Report those omitted IDs for further explicit retrieval.
    for identifier in selected:
        if state[identifier]['kind'] == 'session':
            outstanding.update(set(state[identifier]['related_record_ids'] + state[identifier]['unresolved_question_ids']) - included)
    historical_refs = {(ref['id'], ref['revision']) for identifier in included for ref in links[identifier]
                       if 'revision' in ref and ref['id'] in state and ref['revision'] != state[ref['id']]['revision']}
    last = next((e for e in reversed(history) if not session or e['session_id'] == session), None)
    if not state:
        result = 'no_saved_records'
    elif query is not None and not matches:
        result = 'no_query_matches'
    else:
        result = 'selected'
    return {'view': 'working', 'authority': 'Derived navigation only; saved records retain their original authority and status',
        'project': project,
        'session_summary': ({key: active_session[key] for key in ('id', 'revision', 'topic', 'mode', 'state')} |
            {'related_record_count': len(active_session['related_record_ids']),
             'unresolved_question_count': len(active_session['unresolved_question_ids'])}) if active_session else None,
        'session_count': len(sessions),
        'records': [state[identifier] for identifier in selected] + sorted(findings, key=lambda r: r['id']),
        'active_finding_ids': sorted(r['id'] for r in findings),
        'unresolved_holds': [{'finding_id': r['id'], 'affected_refs': r['affected_refs'],
            'disposition': r['disposition'], 'explanation': r['explanation']} for r in findings
            if r['assessment'] == 'conflict' and r['severity'] == 'significant'],
        'saved_response_display': 'unconfirmed',
        'last_saved_response': next((m['text'] for m in reversed(last['messages']) if m['role'] == 'assistant'), None) if last else None,
        'omitted': {'exchange_count': len(history),
            'record_version_count': sum(len(e['record_versions']) for e in history),
            'record_count': len(state) - len(included)},
        'retrieval': {'source_novel_id': history[0]['novel_id'], 'source_checkpoint': point,
            'method': 'explicit IDs, Unicode NFKC casefold lexical terms, bounded bidirectional record links',
            'exhaustive': False, 'notice': 'Lexical/navigation retrieval is not exhaustive continuity review; retrieve outstanding records and inspect historical sources before relying on them',
            'focus': focus, 'query': query, 'query_match_count': len(matches), 'result': result,
            'limit': limit, 'limit_scope': 'retrieved records; global project and active findings are additional',
            'selection_reasons': {identifier: reasons[identifier] for identifier in sorted(included)},
            'omitted_seed_ids': [identifier for identifier in seeds if identifier not in included][:limit],
            'omitted_seed_count': sum(identifier not in included for identifier in seeds),
            'outstanding_record_ids': sorted(outstanding),
            'historical_reference_versions': [{'id': identifier, 'revision': revision,
                'current_revision': state[identifier]['revision']} for identifier, revision in sorted(historical_refs)],
            'record_versions': 'Complete current versions; inspect for exact historical wording and source artifacts'}}
