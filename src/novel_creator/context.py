"""Read one committed snapshot; context is derived and never a second authority."""
from . import records, storage
from .cli import ToolError


def direct_impact(state, identifiers):
    """Return only recorded direct dependencies; never guess unrecorded links."""
    targets = set(identifiers)
    def mentions(value):
        if isinstance(value, dict):
            if set(value).issubset({'id', 'revision'}) and value.get('id') in targets:
                return True
            for key, child in value.items():
                if key == 'source_refs':
                    continue
                if key.endswith('_id') and key != 'created_exchange_id' and isinstance(child, str) and child in targets:
                    return True
                if key.endswith('_ids') and isinstance(child, list) and targets.intersection(child):
                    return True
                if mentions(child):
                    return True
            return False
        if isinstance(value, list):
            return any(mentions(child) for child in value)
        return False
    return [r for r in state.values() if r['id'] not in targets and
            any(mentions(value) for key, value in r.items() if key not in ('id', 'source_refs', 'created_exchange_id'))]


def read(novel, *, operation='context', session=None, kind=None, identifier=None, revision=None):
    root = storage.root_path(novel)
    commit = storage.head(root)
    history, chain = storage.read_snapshot(root, commit)
    if not history:
        raise ToolError(4, 'No confirmed novel checkpoint')
    point = storage.checkpoint(root, history, commit)
    try:
        manifest = records.loads(storage.git(root, 'show', commit + ':.novel-creator/manifest.json'))
        if not isinstance(manifest, dict) or manifest.get('schema_version') != '1.0':
            raise ValueError()
    except (ValueError, TypeError) as error:
        raise ToolError(4, 'Committed installation metadata is unavailable', checkpoint=point) from error
    if manifest.get('novel_id') != history[0]['novel_id']:
        raise ToolError(4, 'Manifest identity differs from committed novel', checkpoint=point)
    state = chain.snapshot()
    projects = [r for r in state.values() if r['kind'] == 'novel_project']
    sessions = [r for r in state.values() if r['kind'] == 'session']
    if session and (session not in state or state[session]['kind'] != 'session'):
        raise ToolError(4, 'Requested session unavailable', checkpoint=point, affected_refs=[session])
    selected = [r for r in state.values() if (not kind or r['kind'] == kind) and (not identifier or r['id'] == identifier)]
    if identifier and not selected:
        raise ToolError(4, 'Requested record unavailable', checkpoint=point, affected_refs=[identifier])
    versions = [r for e in history for r in e['record_versions'] if (not kind or r['kind'] == kind)
                and (not identifier or r['id'] == identifier) and (revision is None or r['revision'] == revision)]
    if revision is not None and not versions:
        raise ToolError(4, 'Requested revision unavailable', checkpoint=point)
    review = history[-1]['continuity_review']
    data = {'coverage': 'incomplete' if review['coverage'] == 'incomplete' else 'complete',
            'unavailable_refs': review['unavailable_refs'], 'canon_hold_refs': review['canon_hold_refs'],
            'derived': True, 'narrative_consistency_verified': False}
    language = projects[0]['manuscript_language'] if projects else 'en'
    primary = language.split('-')[0].lower()
    data.update(manuscript_language=language,
                language_resource=f'.novel-creator/languages/{primary}.md' if primary in ('en', 'is') else None,
                language_semantics_verified=False)
    if operation == 'validate':
        data.update(valid=True, exchange_count=len(history), record_count=len(state))
    elif operation == 'session':
        data['sessions'] = sessions
    elif operation == 'inspect':
        data.update(records=versions if revision is not None else selected, history=versions,
                    exchanges=history, directly_affected=direct_impact(state, [r['id'] for r in selected]),
                    impact_scope='recorded direct links only')
    else:
        visible = set(state)
        if session:
            chosen = state[session]
            visible = {session, *chosen['related_record_ids'], *chosen['unresolved_question_ids']}
            visible.update(r['id'] for r in state.values() if r['kind'] == 'novel_project' or
                           r.get('status') == 'accepted' or
                           (r['kind'] == 'finding' and r['disposition'] in ('open', 'deferred')))
            def references(value):
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key == 'id' and isinstance(child, str) and child in state:
                            yield child
                        elif key.endswith('_ids') and isinstance(child, list):
                            yield from (identifier for identifier in child if identifier in state)
                        else:
                            yield from references(child)
                elif isinstance(value, list):
                    for child in value:
                        yield from references(child)
            while True:
                expanded = visible | {i for key in visible for i in references(state[key])}
                if expanded == visible:
                    break
                visible = expanded
        session_history = [e for e in history if not session or e['session_id'] == session]
        last = session_history[-1] if session_history else None
        data.update(project=projects[0] if projects else None, sessions=sessions,
                    selected_session=state.get(session), records=[r for key, r in state.items() if key in visible], exchanges=history,
                    current_canon=[r for r in state.values() if r.get('status') == 'accepted'],
                    active_findings=[r for r in state.values() if r['kind'] == 'finding' and r['disposition'] in ('open', 'deferred')],
                    saved_response_display='unconfirmed',
                    last_saved_response=next((m['text'] for m in reversed(last['messages']) if m['role'] == 'assistant'), None) if last else None)
    return {'ok': True, 'operation': 'session.list' if operation == 'session' else operation, 'novel_id': history[0]['novel_id'],
            'data': data, 'warnings': [], 'checkpoint': point}
