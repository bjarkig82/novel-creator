"""Offline immutable published wheels used by focused resource delivery tests."""
import hashlib
from pathlib import Path

SHA256 = {'0.10.0': '097e9d093424a04fdf0d50fcfbc47c3ed7fd0e6d4d081167b3a78cda497ce4d6', '0.10.1': '6721c5a527f1b7e567743f2760ec5e13aec2d0394f520913e98589ac54b8b11a'}


def published_wheel(version):
    path = Path(__file__).resolve().parent / 'fixtures/releases' / f'novel_creator-{version}-py3-none-any.whl'
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256[version]:
        raise AssertionError(f'Historical wheel hash differs: {path}')
    return path
