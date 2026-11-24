"""Offline immutable published wheels used by focused resource delivery tests."""
import hashlib
import re
from pathlib import Path

SHA256 = {'0.10.0': '097e9d093424a04fdf0d50fcfbc47c3ed7fd0e6d4d081167b3a78cda497ce4d6', '0.10.1': '6721c5a527f1b7e567743f2760ec5e13aec2d0394f520913e98589ac54b8b11a'}


def published_wheel(version):
    path = Path(__file__).resolve().parent / 'fixtures/releases' / f'novel_creator-{version}-py3-none-any.whl'
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHA256[version]:
        raise AssertionError(f'Historical wheel hash differs: {path}')
    return path


def refreshed_character_root(original, fresh):
    """Expected original bytes with only the Character section body refreshed."""
    section = rb'^## Character development\r?\n.*?(?=^## |^<!-- novel-creator:|\Z)'
    old, = re.finditer(section, original, re.M | re.S)
    current, = re.finditer(section, fresh, re.M | re.S)
    old_body = old.group().rstrip(b'\r\n')
    newline = b'\r\n' if old_body.startswith(b'## Character development\r\n') else b'\n'
    new_body = current.group().rstrip(b'\r\n').replace(b'\r\n', b'\n').replace(b'\n', newline)
    return original[:old.start()] + new_body + original[old.start() + len(old_body):]
