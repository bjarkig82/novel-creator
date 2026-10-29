"""Structural checks, source resolution and authority boundaries, not literary judgments."""
import hashlib
import re
import copy
from collections import ChainMap
from importlib.resources import files
from functools import lru_cache

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from . import records


@lru_cache(maxsize=1)
def validator():
    root = files("novel_creator.schemas.v1")
    schemas = [records.loads(root.joinpath(name).read_bytes()) for name in
               ("records.schema.json", "exchange.schema.json")]
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas)
    return Draft202012Validator(schemas[1], registry=registry, format_checker=FormatChecker())


@lru_cache(maxsize=1)
def compiled_validator():
    """Compile the same pinned schemas locally; retain the reference format rules."""
    from jsonschema_rs import Draft202012Validator as CompiledValidator, Registry as CompiledRegistry
    root = files('novel_creator.schemas.v1')
    schemas = [records.loads(root.joinpath(name).read_bytes()) for name in
               ('records.schema.json', 'exchange.schema.json')]
    checker = FormatChecker()
    registry = CompiledRegistry([(schema['$id'], schema) for schema in schemas])
    return CompiledValidator(schemas[1], registry=registry, offline=True, validate_formats=True,
        formats={name: (lambda value, name=name: checker.conforms(value, name))
                 for name in ('uuid', 'date-time')})


def pointer(value, path):
    if path == "":
        return value
    if not path.startswith("/"):
        raise ValueError("Invalid JSON Pointer")
    for token in path[1:].split("/"):
        if re.search(r"~(?![01])", token):
            raise ValueError("Invalid JSON Pointer escape")
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError("Invalid array pointer")
            try:
                value = value[int(token)]
            except IndexError as error:
                raise ValueError("Missing JSON Pointer value") from error
        elif isinstance(value, dict) and token in value:
            value = value[token]
        else:
            raise ValueError("Missing JSON Pointer value")
    return value


def span(text, bounds):
    if not 0 <= bounds["start"] < bounds["end"] <= len(text):
        raise ValueError("Source range outside message")
    return text[bounds["start"]:bounds["end"]]


class ExchangeValidator:
    """One owned, incrementally validated read. No persisted cache or authority."""

    def __init__(self, history=()):
        # The standalone API accepts an already-validated prefix, as before.
        self._history = list(history)
        self.cache_hit = False
        self._state = records.fold(history)
        self._exchanges = {e['exchange_id']: e for e in history}
        self._ids = set(self._exchanges)
        self._messages, self._artifacts, self._versions = {}, {}, {}
        self._projects = {r['id'] for r in self._state.values() if r['kind'] == 'novel_project'}
        self._findings = {r['id']: r for r in self._state.values() if r['kind'] == 'finding'}
        for exchange in history:
            messages, artifacts, identifiers = _sources(exchange, self._ids, include_exchange=False)
            self._messages.update(messages)
            self._artifacts.update(artifacts)
            self._ids.update(identifiers)
            self._versions.update({(r['id'], r['revision']): r for r in exchange['record_versions']})
        if self._ids.intersection(self._state):
            raise ValueError('Message/artifact ID collides with record')

    def append(self, bundle):
        self._append_owned(copy.deepcopy(bundle))

    def _append_owned(self, owned):
        # The committed reader passes fresh JSON values with no outside aliases.
        state, messages, artifacts, identifiers = _validate_exchange(owned, self)
        updates = state.maps[0]
        self._remember(owned, updates, messages, artifacts, identifiers)

    def _append_certified(self, owned):
        """Only the committed reader may use this after authenticating exact blobs."""
        messages = {(owned['exchange_id'], m['message_id']): m for m in owned['messages']}
        artifacts = ({(owned['exchange_id'], a['artifact_id']): a for a in owned['input_artifacts']}
                     if owned['operation'] == 'bootstrap' else {})
        identifiers = {owned['exchange_id'], *(m['message_id'] for m in owned['messages']),
                       *(a['artifact_id'] for a in owned['input_artifacts'])}
        self._remember(owned, {r['id']: r for r in owned['record_versions']}, messages, artifacts, identifiers)

    def _remember(self, owned, updates, messages, artifacts, identifiers):
        # Commit indexes only after every structural/authority check succeeds.
        self._state.update(updates)
        self._messages.update(messages)
        self._artifacts.update(artifacts)
        self._ids.update(identifiers)
        self._versions.update({(r['id'], r['revision']): r for r in owned['record_versions']})
        self._projects.update(r['id'] for r in updates.values() if r['kind'] == 'novel_project')
        self._findings.update({r['id']: r for r in updates.values() if r['kind'] == 'finding'})
        self._exchanges[owned['exchange_id']] = owned
        self._history.append(owned)

    def snapshot(self):
        return copy.deepcopy(self._state)


def _sources(exchange, occupied, *, include_exchange=True):
    identifiers = {exchange['exchange_id']} if include_exchange else set()
    if include_exchange and exchange['exchange_id'] in occupied:
        raise ValueError('Duplicate exchange ID')
    messages, artifacts = {}, {}
    for message in exchange['messages']:
        if message['message_id'] in occupied or message['message_id'] in identifiers:
            raise ValueError('Duplicate message ID')
        identifiers.add(message['message_id'])
        messages[(exchange['exchange_id'], message['message_id'])] = message
    for artifact in exchange['input_artifacts']:
        if artifact['artifact_id'] in occupied or artifact['artifact_id'] in identifiers:
            raise ValueError('Duplicate artifact ID')
        identifiers.add(artifact['artifact_id'])
        if (hashlib.sha256(artifact['original_text'].encode()).hexdigest() != artifact['digest'] or
            records.loads(artifact['original_text']) != artifact['parsed_value']):
            raise ValueError('Bootstrap artifact content/digest mismatch')
        if exchange['operation'] != 'bootstrap':
            from .host_input import validate_provenance
            if len(exchange['input_artifacts']) != 1:
                raise ValueError('Conversation accepts only one host-input evidence artifact')
            users = [m for m in exchange['messages'] if m['role'] == 'user']
            if len(users) != 1:
                raise ValueError('Host-input evidence requires exactly one current user message')
            validate_provenance(artifact['parsed_value'], users[0]['text'])
            # Evidence is retained, but never registered as a bootstrap source.
            continue
        artifacts[(exchange['exchange_id'], artifact['artifact_id'])] = artifact
    return messages, artifacts, identifiers


def validate_exchange(bundle, history):
    """Validate an entire transition before returning its detached resulting state.

    History must itself have been validated in order by the committed reader.
    Canon acceptance meaning is a host judgment, never inferred by this validator.
    """
    state, _, _, _ = _validate_exchange(bundle, ExchangeValidator(history))
    return copy.deepcopy(dict(state))


def _validate_exchange(bundle, context):
    history = context._history
    if not compiled_validator().is_valid(bundle):
        errors = sorted(validator().iter_errors(bundle), key=lambda e: str(list(e.path)))
        location = '/'.join(map(str, errors[0].path)) if errors else 'compiled-schema-check'
        raise ValueError('Exchange schema violation at ' + location)
    if records.digest(bundle) != bundle["payload_digest"]:
        raise ValueError("Payload digest mismatch")
    if history:
        previous = history[-1]
        if (bundle["novel_id"] != previous["novel_id"] or
            bundle["sequence"] != previous["sequence"] + 1 or
            bundle["previous_exchange_id"] != previous["exchange_id"] or
            bundle["previous_digest"] != previous["payload_digest"] or
            bundle["operation"] == "bootstrap"):
            raise ValueError("Exchange chain mismatch")
    elif (bundle["sequence"] != 1 or bundle["operation"] != "bootstrap" or
          bundle["previous_exchange_id"] is not None or bundle["previous_digest"] is not None):
        raise ValueError("Missing bootstrap predecessor")
    local_messages, local_artifacts, identifiers = _sources(bundle, context._ids)
    exchanges = ChainMap({bundle['exchange_id']: bundle}, context._exchanges)
    messages = ChainMap(local_messages, context._messages)
    artifacts = ChainMap(local_artifacts, context._artifacts)
    before = context._state
    updates = records.revision_updates(bundle, before, detach=False)
    state = ChainMap(updates, before)
    projects = context._projects | {r['id'] for r in updates.values() if r['kind'] == 'novel_project'}
    if len(projects) > 1:
        raise ValueError('A novel has one stable project record')
    versions = ChainMap({(r['id'], r['revision']): r for r in bundle['record_versions']}, context._versions)
    if any(i in state for i in identifiers) or any(i in context._ids for i in updates):
        raise ValueError("Message/artifact ID collides with record")

    def record_ref(reference, kind=None):
        identifier = reference["id"] if isinstance(reference, dict) else reference
        value = (versions.get((identifier, reference["revision"]))
                 if isinstance(reference, dict) and "revision" in reference else state.get(identifier))
        if value is None or (kind and value["kind"] != kind):
            raise ValueError("Missing or incorrectly typed record reference")
        return value

    def source(reference):
        if reference["type"] == "message":
            message = messages.get((reference["exchange_id"], reference["message_id"]))
            if message is None:
                raise ValueError("Missing source message")
            if "range" in reference:
                span(message["text"], reference["range"])
            return message
        artifact = artifacts.get((reference["exchange_id"], reference["artifact_id"]))
        if artifact is None:
            raise ValueError("Missing bootstrap artifact")
        pointer(artifact["parsed_value"], reference["pointer"])
        return artifact

    # Traverse source and record-reference shapes, including nested preferences/timing.
    def walk(value):
        if isinstance(value, dict):
            if value.get("type") in ("message", "bootstrap_artifact"):
                source(value)
            elif "id" in value and set(value).issubset({"id", "revision"}):
                record_ref(value)
            for key, child in value.items():
                if key.endswith("_ids") and key not in ("alternative_group_ids",):
                    kinds = {'related_element_ids': 'story_element', 'assertion_ids': 'assertion',
                             'resulting_assertion_ids': 'assertion', 'relationship_ids': 'relationship',
                             'decision_ids': 'decision', 'unresolved_question_ids': 'question',
                             'alternative_ids': 'idea'}
                    for identifier in child:
                        record_ref(identifier, kinds.get(key))
                elif key in ("from_element_id", "to_element_id", "subject_element_id", "holder_id") and child:
                    record_ref(child, "story_element")
                elif key == "resolution_decision_id" and child:
                    record_ref(child, "decision")
                elif key in ("started_exchange_id", "last_exchange_id"):
                    if child not in exchanges:
                        raise ValueError("Missing session exchange")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    review = bundle["continuity_review"]
    finding_holds = set()

    def held_scope(finding):
        if (finding['kind'] == 'finding' and finding['assessment'] == 'conflict' and
            finding['severity'] == 'significant' and finding['disposition'] in ('open', 'deferred')):
            return {r['id'] for r in finding['affected_refs']} or {'*'}
        return set()

    findings = ChainMap({r['id']: r for r in updates.values() if r['kind'] == 'finding'}, context._findings)
    for finding in findings.values():
        scope = held_scope(finding)
        prior = before.get(finding['id'])
        # A still-unresolved finding cannot discard its committed protection,
        # even in a proposal-only exchange that could enable later promotion.
        # Terminal dispositions are authorized below by a current user decision.
        if prior and finding['kind'] == 'finding' and finding['disposition'] in ('open', 'deferred'):
            previous_scope = held_scope(prior)
            if previous_scope and '*' not in scope and not previous_scope.issubset(scope):
                raise ValueError('Conflict hold cannot be weakened without a user-directed resolution')
        finding_holds.update(scope)
    if review["coverage"] == "complete" and (review["unavailable_refs"] or review["canon_hold_refs"]):
        raise ValueError("Complete review cannot conceal unavailable scope")
    for reference in review["reviewed_record_refs"]:
        record_ref(reference)
    for identifier in review["finding_ids"]:
        record_ref(identifier, "finding")
    if bundle["session_id"] is not None:
        record_ref(bundle["session_id"], "session")
    for record in bundle["record_versions"]:
        walk(record)
        if record["origin"] == "system_default" and record["source_refs"]:
            raise ValueError("System defaults cannot fabricate sources")
        if record["origin"] != "system_default" and not record["source_refs"]:
            raise ValueError("Supplied/derived record needs provenance")
        for key in ("decision_ids",):
            for identifier in record.get(key, []):
                record_ref(identifier, "decision")
        if record["kind"] == "decision":
            message = source(record["user_message_ref"])
            if (message["role"] != "user" or
                record["user_message_ref"]["exchange_id"] != bundle["exchange_id"]):
                raise ValueError("Decision requires the current exchange's actual user message")
            span(message["text"], record["span"])
            if record["user_message_ref"].get("range", record["span"]) != record["span"]:
                raise ValueError("Decision source and accepting span disagree")
        prior = before.get(record["id"])
        if record['kind'] == 'finding' and prior and record['disposition'] != prior['disposition']:
            allowed = {'deferred': {'defer'}, 'rejected_idea': {'reject'}, 'revised_idea': {'revise', 'correct'},
                       'revised_canon': {'revise', 'reverse', 'correct'}, 'intentional': {'resolve'},
                       'resolved': {'resolve', 'revise', 'reverse', 'correct'}, 'open': {'revise', 'correct'}}
            decisions = [record_ref(i, 'decision') for i in record['decision_ids']]
            if not any(d in bundle['record_versions'] and d['action'] in allowed[record['disposition']] and
                       any(r['id'] == record['id'] for r in d['target_refs'] + d['result_refs']) for d in decisions):
                raise ValueError('Finding disposition change requires a sourced current decision')
            if record['disposition'] == 'intentional' and not record['narrative_explanation']:
                raise ValueError('Intentional technique needs its narrative explanation')
        timing = record.get('time_ref')
        if timing:
            for axis in timing.values():
                if axis['precision'] == 'unknown' and (axis['start'] is not None or axis['end'] is not None):
                    raise ValueError('Unknown timing must retain null bounds')
        if record['kind'] == 'novel_project':
            if prior and record['original_concept'] != prior['original_concept']:
                raise ValueError('Original concept provenance is immutable')
            for preference in [record['title'], record['original_concept'],
                               *record['creative_brief'].values(), *record['workflow_preferences'].values()]:
                if preference['state'] == 'unknown' and (preference['original_text'] is not None or preference['interpretation'] is not None):
                    raise ValueError('Unknown preference cannot invent text')
                if preference['origin'] == 'system_default' and preference['source_refs']:
                    raise ValueError('Default preference cannot fabricate sources')
                if preference['origin'] != 'system_default' and not preference['source_refs']:
                    raise ValueError('Supplied preference needs a source')
            if prior and not any(s.get('type') == 'message' and s.get('exchange_id') == bundle['exchange_id']
                                 and source(s).get('role') == 'user' for s in record['source_refs']):
                raise ValueError('Project revision requires the current user message')
        if record['kind'] == 'assertion' and record['status'] == 'accepted' and record['supersedes']:
            superseded = record['supersedes']
            if 'revision' not in superseded:
                raise ValueError('Supersession must identify the precise prior revision')
            record_ref(superseded, 'assertion')
            if superseded['id'] == record['id']:
                if not prior or superseded['revision'] != prior['revision']:
                    raise ValueError('Supersession must name the exact predecessor')
            elif state[superseded['id']]['status'] != 'superseded':
                raise ValueError('Replacement cannot leave the old assertion current')
        if prior and record == prior:
            raise ValueError("Revision must retain exact predecessor")
        canon_change = (record.get("status") == "accepted" or (prior and prior.get("status") == "accepted"))
        if not canon_change:
            continue
        if bundle["operation"] != "conversation":
            raise ValueError("Only conversations authorize canon")
        if '*' in finding_holds or record['id'] in finding_holds:
            raise ValueError('Open or deferred significant conflict holds this canon change')
        holds = review["canon_hold_refs"]
        if ("*" in holds or record["id"] in holds or
            any(r["id"] == record["id"] for r in review["unavailable_refs"])):
            raise ValueError("Unavailable canon scope holds this change")
        if review["coverage"] == "incomplete" and not (holds or review["unavailable_refs"]):
            raise ValueError("Unbounded incomplete scope holds all canon changes")
        authorized = False
        for identifier in record.get("decision_ids", []):
            decision = record_ref(identifier, "decision")
            references = decision["target_refs"] + decision["result_refs"]
            targets = [r["id"] for r in references
                       if r.get("revision", record["revision"]) == record["revision"]]
            # Accepting a prior proposal can promote that unchanged proposition.
            # It cannot authorize different content under the same stable ID.
            if decision["action"] == "accept" and prior and prior.get("status") in ("proposed", "unresolved"):
                metadata = {"revision", "previous_revision", "status", "decision_ids", "source_refs", "origin"}
                content = lambda value: {k: v for k, v in value.items() if k not in metadata}
                if content(prior) == content(record):
                    targets += [r["id"] for r in decision["target_refs"]
                                if r["id"] == record["id"] and r.get("revision") == prior["revision"]]
            if (decision in bundle["record_versions"] and record["id"] in targets and
                decision["action"] in ("accept", "revise", "reverse", "correct")):
                if (decision['action'] == 'accept' and decision['selected_parts'] and
                    record['kind'] == 'idea' and set(record['selected_parts']) != set(decision['selected_parts'])):
                    raise ValueError('Partial selection cannot promote an entire compound idea')
                if prior and prior.get("status") == "accepted" and decision["action"] == "accept":
                    continue
                authorized = True
        if not authorized:
            raise ValueError("Canon transition requires a sourced current user decision")
    return state, local_messages, local_artifacts, identifiers
