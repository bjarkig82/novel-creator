"""Offline release transport and acknowledged hard-stop test support."""
import copy
import hashlib
import io
import os
import zipfile
from pathlib import Path
import base64
import csv
import re


PRIVATE_SEEDS = ('PRIVATE-STORY-ÞÓRA', 'PRIVATE-TRANSCRIPT-ANSWER',
                 'private-credential-value', r'C:\Private\Book')


class FakeReleaseTransport:
    def __init__(self, responses=None):
        self.responses = dict(responses or {})
        self.requests = []

    def get(self, url):
        self.requests.append(url)
        if any(seed in url for seed in PRIVATE_SEEDS):
            raise AssertionError('Private value sent to release transport')
        if url not in self.responses:
            raise OSError('Offline fixture has no response for this request')
        value = self.responses[url]
        if isinstance(value, Exception):
            raise value
        return copy.deepcopy(value)


def archive(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as wheel:
        for path, raw in entries:
            wheel.writestr(path, raw)
    raw = output.getvalue()
    return raw, hashlib.sha256(raw).hexdigest()


def hard_stop(point, *, selected, acknowledgement):
    """Terminate only the calling test child after a flushed acknowledgement."""
    if point == selected:
        acknowledgement.write(point + '\n')
        acknowledgement.flush()
        os.fsync(acknowledgement.fileno())
        os._exit(91)


def product_wheel(version='0.3.0', *, exclude=()):
    """Controlled unpublished target from current code, never a release claim."""
    root = Path(__file__).resolve().parents[1]
    entries = {}
    for source, target, suffixes in (
        ('src/novel_creator', 'novel_creator', ('.py', '.json')),
        ('schemas', 'novel_creator/schemas', ('.py', '.json')),
        ('workflows', 'novel_creator/workflows', ('.py', '.md')),
        ('languages', 'novel_creator/languages', ('.py', '.md')),
        ('adapters/codex', 'novel_creator/codex', ('.py', '.md')),
    ):
        folder = root / source
        for path in folder.rglob('*'):
            if path.is_file() and path.suffix in suffixes and '__pycache__' not in path.parts:
                entries[target + '/' + path.relative_to(folder).as_posix()] = path.read_bytes()
    initializer = entries['novel_creator/__init__.py'].decode('utf-8')
    entries['novel_creator/__init__.py'] = re.sub(
        r'__version__\s*=\s*"[^"]+"', '__version__ = "' + version + '"', initializer).encode('utf-8')
    for package in ('schemas', 'schemas/v1', 'workflows', 'languages', 'codex'):
        entries.setdefault('novel_creator/' + package + '/__init__.py', b'')
    for name in exclude:
        entries.pop(name)
    info = 'novel_creator-' + version + '.dist-info/'
    entries[info + 'METADATA'] = (
        'Metadata-Version: 2.1\nName: novel-creator\nVersion: ' + version +
        '\nRequires-Python: >=3.11\nRequires-Dist: jsonschema>=4.23,<5\n'
        'Requires-Dist: jsonschema-rs>=0.59,<0.60\nRequires-Dist: packaging>=24\n\n').encode()
    entries[info + 'WHEEL'] = b'Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n'
    record = io.StringIO(newline='')
    writer = csv.writer(record)
    for name, raw in sorted(entries.items()):
        encoded = base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b'=').decode()
        writer.writerow([name, 'sha256=' + encoded, len(raw)])
    writer.writerow([info + 'RECORD', '', ''])
    entries[info + 'RECORD'] = record.getvalue().encode()
    return archive(sorted(entries.items()))


def release_listing(versions):
    """Map exact versions to synthetic, public-shaped immutable wheel responses."""
    metadata = {'releases': {}}
    responses = {}
    for version, raw in versions.items():
        name = 'novel_creator-' + version + '-py3-none-any.whl'
        url = 'https://files.pythonhosted.org/synthetic/' + name
        metadata['releases'][version] = [{'filename': name, 'url': url,
            'digests': {'sha256': hashlib.sha256(raw).hexdigest()},
            'size': len(raw), 'yanked': False, 'requires_python': '>=3.11', 'packagetype': 'bdist_wheel'}]
        responses[url] = raw
    responses['https://pypi.org/pypi/novel-creator/json'] = metadata
    return FakeReleaseTransport(responses)
