"""Explicit, hash-bound historical artifacts and disposable book snapshots.

No downloads, global Git settings, or production-book discovery. A rebuilt wheel
is never silently substituted for the approved public-release artifact.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import queue
import subprocess
import sys
import tempfile
import threading
import zipfile

from tests.helpers import git


REPOSITORY = Path(__file__).resolve().parents[1]
SOURCE_WHEELS = {
    '0.1.0': ('tests/fixtures/releases/novel_creator-0.1.0-py3-none-any.whl',
              'cc8645556f74190dee9ac7527c3e66c0bc71574913b5bbae5ddff7516b8817a8'),
    '0.2.0': ('tests/fixtures/releases/novel_creator-0.2.0-py3-none-any.whl',
              '9872b3aa9a4a1629d4b6c50a1672f5acbd376130f08f9c7edcd0492381c632fa'),
}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def artifact(version, wheel=None):
    """Resolve an explicitly selected historical release, checking exact bytes."""
    relative, digest = SOURCE_WHEELS[version]
    selected = wheel if wheel is not None else os.environ.get(
        'NOVEL_UPDATE_SOURCE_' + version.replace('.', '') + '_WHEEL', REPOSITORY / relative)
    path = Path(selected).resolve(strict=True)
    if sha256(path.read_bytes()) != digest:
        raise ValueError('Historical release archive digest mismatch')
    return path, {'version': version, 'filename': path.name, 'sha256': digest}


def snapshot(root):
    """Read bytes/modes and semantic staging, excluding .git's mutable internals."""
    root = Path(root)
    files = {}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root).as_posix()
        if relative == '.git' or relative.startswith('.git/'):
            continue
        # OS mutex bytes are derived, may be unreadable while held on Windows,
        # and never own grants/notices/history. Keep holder/journal JSON visible.
        if relative.startswith('.novel-creator/local/') and relative.endswith('.guard'):
            continue
        if path.is_symlink():
            files[relative] = {'symlink': os.readlink(path)}
        elif path.is_file():
            files[relative] = {'sha256': sha256(path.read_bytes()),
                               'mode': path.stat().st_mode & 0o777}
    return {'head': git(root, 'rev-parse', 'HEAD'),
            'index': git(root, 'ls-files', '--stage', '-z'), 'files': files}


@dataclass
class LegacyBook:
    root: Path
    vendor: Path
    identity: dict
    python: str = sys.executable

    def run(self, code, *arguments, expected=0, pinned=False):
        environment = {key: value for key, value in os.environ.items()
                       if not key.startswith(('GIT_', 'PYTHON'))}
        environment.update(PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_NOSYSTEM='1')
        program = ('import sys; sys.path.insert(0, sys.argv.pop(1)); ' + code)
        result = subprocess.run([self.python, '-I', '-B', '-X', 'utf8', '-c', program,
                                 str(self.root / '.novel-creator/src' if pinned else self.vendor),
                                 str(self.root), *map(str, arguments)],
                                cwd=self.root.parent, env=environment,
                                capture_output=True, text=True, encoding='utf-8', timeout=120)
        if result.returncode != expected:
            raise AssertionError(f'Legacy subprocess exit {result.returncode}: {result.stderr}')
        return result.stdout.strip()

    @contextmanager
    def spawn(self, code):
        """Run an acknowledged probe from the actual pinned legacy modules."""
        program = 'import sys; sys.path.insert(0, sys.argv.pop(1)); ' + code
        process = subprocess.Popen(
            [self.python, '-I', '-B', '-X', 'utf8', '-c', program,
             str(self.root / '.novel-creator/src'), str(self.root)],
            cwd=self.root.parent, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding='utf-8',
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        try:
            yield process
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=30)

    def launch(self, *arguments):
        return subprocess.run([self.python, '-I', '-B', '-X', 'utf8', str(self.root / '.novel-creator/run.py'),
                               *map(str, arguments)], cwd=self.root.parent,
                              capture_output=True, text=True, encoding='utf-8', timeout=120)


def acknowledged(process, expected):
    output = queue.Queue()
    threading.Thread(target=lambda: output.put(process.stdout.readline()), daemon=True).start()
    try:
        line = output.get(timeout=30).strip()
    except queue.Empty as error:
        raise AssertionError('Probe did not acknowledge its durable checkpoint') from error
    if line != expected:
        raise AssertionError('Unexpected probe acknowledgement: ' + repr(line))

@contextmanager
def historical_book(version, *, wheel=None, language='en'):
    path, identity = artifact(version, wheel)
    with tempfile.TemporaryDirectory(prefix='novel-update-legacy-') as directory:
        base = Path(directory).resolve()
        vendor = base / 'vendor'
        vendor.mkdir()
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                parts = PurePosixPath(name)
                if parts.is_absolute() or '..' in parts.parts or '\\' in name:
                    raise ValueError('Unsafe historical archive path')
            archive.extractall(vendor)
        root = base / 'Bók-Þóra'
        root.mkdir()
        git(root, 'init', '-b', 'main')
        git(root, 'config', 'user.name', 'Disposable Update Test')
        git(root, 'config', 'user.email', 'update@example.invalid')
        book = LegacyBook(root, vendor, identity)
        code = ("import json; from novel_creator.install import initialize; "
                "from novel_creator import __version__; "
                "value=initialize(sys.argv[1], json.dumps({'title':'Þóra',"
                "'manuscript_language':sys.argv[2]},ensure_ascii=False)); "
                "print(json.dumps({'version':__version__,'saved':value['data']['saved']}))")
        result = json.loads(book.run(code, language))
        if result != {'version': version, 'saved': True}:
            raise AssertionError('Historical initialization identity/save mismatch')
        yield book


def add_writer_work(root):
    """Seed content and partial staging without asserting any story canon."""
    root = Path(root)
    (root / 'manuscript.md').write_bytes('Ósamþykkt prófunarefni.\n'.encode())
    (root / 'notes.txt').write_bytes(b'initial\n')
    git(root, 'add', 'manuscript.md', 'notes.txt')
    git(root, 'commit', '-m', 'Synthetic writer files')
    (root / 'notes.txt').write_bytes(b'staged\n')
    git(root, 'add', 'notes.txt')
    (root / 'notes.txt').write_bytes(b'working\n')
    (root / 'untracked.txt').write_bytes(b'preserve untracked\n')
    return snapshot(root)
