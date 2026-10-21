"""Structural checks, source resolution and authority boundaries, not literary judgments."""
import hashlib
import re
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


def validate_exchange(bundle, history):
    """Validate an entire transition before returning its detached resulting state.

    History must itself have been validated in order by the committed reader.
    Canon acceptance meaning is a host judgment, never inferred by this validator.
    """
    errors = sorted(validator().iter_errors(bundle), key=lambda e: str(list(e.path)))
    if errors:
        raise ValueError("Exchange schema violation at " + "/".join(map(str, errors[0].path)))
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
    exchanges = {e["exchange_id"]: e for e in history}
    if bundle["exchange_id"] in exchanges:
        raise ValueError("Duplicate exchange ID")
    exchanges[bundle["exchange_id"]] = bundle
    messages, artifacts = {}, {}
    all_ids = set(exchanges)
    for exchange in exchanges.values():
        for message in exchange["messages"]:
            if message["message_id"] in all_ids:
                raise ValueError("Duplicate message ID")
            all_ids.add(message["message_id"])
            messages[(exchange["exchange_id"], message["message_id"])] = message
        for artifact in exchange["input_artifacts"]:
            if artifact["artifact_id"] in all_ids:
                raise ValueError("Duplicate artifact ID")
            all_ids.add(artifact["artifact_id"])
            if (hashlib.sha256(artifact["original_text"].encode()).hexdigest() != artifact["digest"] or
                records.loads(artifact["original_text"]) != artifact["parsed_value"]):
                raise ValueError("Bootstrap artifact content/digest mismatch")
            if exchange["operation"] != "bootstrap":
                raise ValueError("Input artifacts belong to bootstrap")
            artifacts[(exchange["exchange_id"], artifact["artifact_id"])] = artifact
    state = records.fold([*history, bundle])
    before = records.fold(history)
    versions = {(r["id"], r["revision"]): r for e in [*history, bundle] for r in e["record_versions"]}
    if all_ids.intersection(state):
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
            if message["role"] != "user":
                raise ValueError("Decision requires an actual user message")
            span(message["text"], record["span"])
            if record["user_message_ref"].get("range", record["span"]) != record["span"]:
                raise ValueError("Decision source and accepting span disagree")
        prior = before.get(record["id"])
        if prior and record == prior:
            raise ValueError("Revision must retain exact predecessor")
        canon_change = (record.get("status") == "accepted" or (prior and prior.get("status") == "accepted"))
        if not canon_change:
            continue
        if bundle["operation"] != "conversation":
            raise ValueError("Only conversations authorize canon")
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
                if prior and prior.get("status") == "accepted" and decision["action"] == "accept":
                    continue
                authorized = True
        if not authorized:
            raise ValueError("Canon transition requires a sourced current user decision")
    return state
