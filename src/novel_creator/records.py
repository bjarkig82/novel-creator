"""Strict JSON, canonical digests and immutable full-revision folding."""
import copy
import hashlib
import json
import math


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
        seen = set()
        for record in exchange["record_versions"]:
            key = record["id"]
            if key in seen:
                raise ValueError("Duplicate record ID in exchange")
            seen.add(key)
            previous = state.get(key)
            if previous:
                if (record["revision"] != previous["revision"] + 1 or
                    record["previous_revision"] != previous["revision"] or
                    record["kind"] != previous["kind"] or
                    record["created_exchange_id"] != previous["created_exchange_id"]):
                    raise ValueError("Invalid record predecessor or identity")
            elif (record["revision"] != 1 or record["previous_revision"] is not None or
                  record["created_exchange_id"] != exchange["exchange_id"]):
                raise ValueError("Invalid record creation")
            state[key] = copy.deepcopy(record)
    return state
