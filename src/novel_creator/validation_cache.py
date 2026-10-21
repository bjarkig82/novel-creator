"""Optional authenticated proof of a validated Git snapshot; stores no story state.

An explicitly configured private key outside the novel authenticates proofs
produced by this runtime. The CLI only reads that key. Novel-supplied keys are
never trusted; absent configuration uses full validation. Changed runtime/HEAD,
tracked or malformed proofs are cache misses. Readers verify actual Git blobs.
"""
from functools import lru_cache
import hashlib
import hmac
from importlib import metadata
from importlib.resources import files
import json
import os
import stat
import sys
from pathlib import Path

from . import records
from .cli import ToolError


PREFIX = '.novel-creator/local/cache/'
KEY_ENV = 'NOVEL_CREATOR_VALIDATION_KEY_FILE'


@lru_cache(maxsize=1)
def validator_digest():
    digest = hashlib.sha256()
    package = files('novel_creator')
    resources = [(child.name, child.read_bytes()) for child in package.iterdir()
                 if child.name.endswith('.py')]
    schemas = files('novel_creator.schemas.v1')
    resources.extend((name, schemas.joinpath(name).read_bytes()) for name in
                     ('exchange.schema.json', 'records.schema.json'))
    for name, raw in sorted(resources):
        digest.update(name.encode() + b'\0' + str(len(raw)).encode() + b'\0' + raw)
    versions = {}
    for name in ('jsonschema', 'jsonschema-rs', 'rfc3339-validator'):
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = None
    from jsonschema import FormatChecker
    digest.update(_bytes({'python': list(sys.version_info[:3]), 'platform': sys.platform,
                          'versions': versions, 'formats': sorted(FormatChecker.checkers)}))
    return digest.hexdigest()


def _bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode('utf-8')


def _body(commit, entries):
    journal = [(path, mode, oid) for path, (mode, oid) in sorted(entries.items())
               if path.startswith('story/exchanges/')]
    return {'derived': True, 'cache_version': 1, 'schema_version': '1.0',
            'git_head': commit, 'journal_digest': hashlib.sha256(_bytes(journal)).hexdigest(),
            'validator_digest': validator_digest()}


def _key(root):
    configured = os.environ.get(KEY_ENV)
    if not configured:
        return None
    if not Path(configured).is_absolute():
        return None
    path = Path(configured).absolute()
    # Explicit runtime configuration is the trust boundary. A repository cannot
    # authenticate itself using a key supplied alongside its untrusted data.
    if path.resolve() != path or path.is_relative_to(Path(root).resolve()):
        return None
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size != 32:
        return None
    if os.name != 'nt' and stat.S_IMODE(info.st_mode) & 0o077:
        return None
    return path.read_bytes()


def trusted(root, commit, entries):
    from .storage import safe_path
    if not commit or not os.environ.get(KEY_ENV) or any(path.startswith(PREFIX) for path in entries):
        return False
    try:
        key = _key(root)
        path = safe_path(root, PREFIX + 'validation.json')
        if key is None or path.stat().st_size > 4096:
            return False
        proof = records.loads(path.read_bytes())
        expected = _body(commit, entries)
        if not isinstance(proof, dict) or set(proof) != {*expected, 'signature'}:
            return False
        signature = proof.pop('signature')
        return proof == expected and isinstance(signature, str) and hmac.compare_digest(
            signature, hmac.new(key, _bytes(expected), hashlib.sha256).hexdigest())
    except (OSError, ValueError, TypeError, ToolError):
        return False


def remember(root, commit, entries):
    """Best effort; cache failures never change the outcome of a read or save."""
    from .storage import safe_path, atomic_json
    if not commit or not os.environ.get(KEY_ENV) or any(path.startswith(PREFIX) for path in entries):
        return
    try:
        key = _key(root)
        if key is None:
            return
        body = _body(commit, entries)
        proof = {**body, 'signature': hmac.new(key, _bytes(body), hashlib.sha256).hexdigest()}
        atomic_json(safe_path(root, PREFIX + 'validation.json'), proof)
    except (OSError, ValueError, TypeError, ToolError):
        pass
