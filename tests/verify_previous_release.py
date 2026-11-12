"""Installed-candidate upgrades from an immutable public release, in disposable books."""
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import urllib.request
from urllib.parse import urlparse
import zipfile


SOURCE_VERSION = '0.7.1'
SOURCE_FILENAME = 'novel_creator-0.7.1-py3-none-any.whl'
SOURCE_SHA256 = 'cbbd487cee102003160f1966b5748efac73ac9733532744b015abb1f9e6393ba'
CLARIFY_PATHS = ('.agents/skills/novel-clarify/SKILL.md',
                 '.novel-notebook/workflows/clarify.md')


def applies(version):
    """Historical public checks must not be silently tested as newer candidates."""
    match = re.fullmatch(r'(\d+)\.(\d+)\.(\d+)', version.removeprefix('novel-creator '))
    return bool(match and tuple(map(int, match.groups())) >= (0, 7, 2))


def checked_source(raw):
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Previous public release wheel hash mismatch')
    return raw


def _run(args, *, cwd, env):
    result = subprocess.run(list(map(str, args)), cwd=cwd, env=env,
                            capture_output=True, text=True, encoding='utf-8', timeout=300)
    if result.returncode:
        raise RuntimeError(f'Previous-release probe failed: {args!r}\n{result.stdout}\n{result.stderr}')
    return result.stdout


def _source(scratch, source_wheel=None):
    if source_wheel is not None:
        raw = checked_source(Path(source_wheel).read_bytes())
    else:
        with urllib.request.urlopen('https://pypi.org/pypi/novel-creator/0.7.1/json', timeout=30) as response:
            metadata = json.load(response)
        matches = [entry for entry in metadata['urls'] if entry['filename'] == SOURCE_FILENAME]
        if len(matches) != 1 or matches[0]['digests']['sha256'] != SOURCE_SHA256:
            raise ValueError('Previous public release metadata does not match frozen archive')
        url = matches[0]['url']
        parsed = urlparse(url)
        if parsed.scheme != 'https' or parsed.hostname != 'files.pythonhosted.org':
            raise ValueError('Unexpected previous release archive origin')
        with urllib.request.urlopen(url, timeout=60) as response:
            raw = checked_source(response.read())
    path = scratch / SOURCE_FILENAME
    path.write_bytes(raw)
    return path


def _snapshot(root):
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob('*')
            if path.is_file() and '.git' not in path.relative_to(root).parts}


def check_target_inventory(python, target_wheel, version, *, cwd, env):
    """Bind every shipped product file to the actual installed controller."""
    probe = '''
import hashlib,json,sys
from pathlib import Path
import novel_creator
root = Path(novel_creator.__file__).resolve().parent
assert root.is_relative_to(Path(sys.prefix))
assert novel_creator.__version__ == sys.argv[1]
inventory = {}
for path in root.rglob('*'):
 if path.is_symlink():
  raise ValueError('Installed product has a redirected path')
 if path.is_file() and '__pycache__' not in path.relative_to(root).parts and path.suffix not in ('.pyc', '.pyo'):
  inventory['novel_creator/' + path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
print(json.dumps(inventory))
'''
    installed = json.loads(_run([python, '-I', '-B', '-c', probe, version], cwd=cwd, env=env))
    target = {}
    with zipfile.ZipFile(target_wheel) as archive:
        for info in archive.infolist():
            if info.is_dir() or not info.filename.startswith('novel_creator/'):
                continue
            name = info.filename
            parts = PurePosixPath(name)
            if '..' in parts.parts or '\\' in name or name in target:
                raise ValueError('Invalid target product resource path')
            target[name] = hashlib.sha256(archive.read(info)).hexdigest()
    if not target or installed != target:
        raise ValueError('Upgrade target product inventory differs from the installed candidate')
    return len(target)


def verify(python, console, scratch, env, version, target_wheel, *, source_wheel=None):
    """The controller is the installed wheel/sdist/public product, never checkout code."""
    if not applies(version):
        raise ValueError('Previous-release probe requires a supported newer stable version')
    scratch = Path(scratch) / 'previous-release'
    scratch.mkdir()
    current_version = version.removeprefix('novel-creator ')
    target_file_count = check_target_inventory(python, target_wheel, current_version, cwd=scratch, env=env)
    source = _source(scratch, source_wheel)
    old = scratch / 'source-package'
    with zipfile.ZipFile(source) as archive:
        for name in archive.namelist():
            parts = PurePosixPath(name)
            if parts.is_absolute() or '..' in parts.parts or '\\' in name:
                raise ValueError('Unsafe previous release archive path')
        archive.extractall(old)
    probe = '''
import base64,json,sys
from pathlib import Path
from importlib.resources import files
import novel_creator
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))
assert novel_creator.__version__ == sys.argv[1]
resources = files('novel_creator.notebook_resources')
codex = files('novel_creator.codex')
expected = {
 '.agents/skills/novel-clarify/SKILL.md': base64.b64encode(codex.joinpath('notebook/skills/novel-clarify/SKILL.md').read_bytes()).decode(),
 '.novel-notebook/workflows/clarify.md': base64.b64encode(resources.joinpath('workflows/clarify.md').read_bytes()).decode()}
feature = codex.joinpath('notebook/skills/novel-character-develop/SKILL.md')
if feature.is_file():
 expected['.agents/skills/novel-character-develop/SKILL.md'] = base64.b64encode(feature.read_bytes()).decode()
 for name in ('character-development', 'help'):
  expected['.novel-notebook/workflows/' + name + '.md'] = base64.b64encode(resources.joinpath('workflows/' + name + '.md').read_bytes()).decode()
print(json.dumps(expected))
'''
    expected = {path: base64.b64decode(raw).replace(b'\r\n', b'\n') for path, raw in json.loads(
        _run([python, '-I', '-B', '-c', probe, current_version], cwd=scratch, env=env)).items()}
    cases = []
    for language in ('en', 'is'):
        root = scratch / ('Published notebook ' + language)
        initialize = '''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import novel_creator
from novel_creator.notebook import initialize
assert novel_creator.__version__ == '0.7.1'
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.argv[1]))
assert initialize(sys.argv[2], title='Published notebook', language=sys.argv[3])['data']['ready']
'''
        _run([python, '-I', '-B', '-c', initialize, old, root, language], cwd=scratch, env=env)

        def git(*args):
            return _run(['git', '-C', root, *args], cwd=scratch, env=env)

        original_instructions = (root / 'AGENTS.md').read_bytes()
        custom = original_instructions + b'\nKeep the writer custom direction.\n'
        (root / 'AGENTS.md').write_bytes(custom)
        accepted = root / 'notebook/accepted-verifier.md'
        accepted.write_bytes(b'Accepted story content must remain unchanged.\n')
        git('add', '.')
        git('commit', '-m', 'Synthetic writer work on published notebook')
        writer = root / 'writer-verifier.txt'
        writer.write_bytes(b'Staged writer work\n')
        git('add', 'writer-verifier.txt')
        writer.write_bytes(b'Unstaged writer work\n')
        before, head, index = _snapshot(root), git('rev-parse', 'HEAD'), git('ls-files', '--stage', '-z')
        assert all(before[path].replace(b'\r\n', b'\n') != expected[path] for path in CLARIFY_PATHS)
        preview = json.loads(_run([console, 'notebook', 'update', '--path', root, '--json'],
                                  cwd=scratch, env=env))['data']
        assert _snapshot(root) == before
        replacements = {item['path'] for item in preview['changes'] if item['action'] == 'replace'}
        expected_replacements = set(CLARIFY_PATHS)
        if '.novel-notebook/workflows/help.md' in expected:
            expected_replacements.add('.novel-notebook/workflows/help.md')
        assert replacements == expected_replacements, preview
        result = json.loads(_run([console, 'notebook', 'update', '--path', root, '--apply',
                                 '--preview', preview['preview_id'], '--expected-head', preview['reviewed_head'],
                                 '--json'], cwd=scratch, env=env))['data']
        assert result['ready'] and result['applied']
        assert git('rev-parse', 'HEAD') == head and git('ls-files', '--stage', '-z') == index
        after = _snapshot(root)
        assert {name for name in before.keys() | after.keys() if before.get(name) != after.get(name)} <= set(expected) | {'AGENTS.md'}
        assert after['AGENTS.md'].startswith(custom)
        for name in expected:
            assert after[name] == expected[name], name
            text = after[name].decode()
            for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
                assert (root / name).parent.joinpath(link).is_file(), (name, link)
        workflow = after[CLARIFY_PATHS[1]].decode()
        assert '2–4' in workflow and '**Custom — type your own answer**' in workflow
        assert '.novel-notebook/workflows/clarify.md' in after['AGENTS.md'].decode()
        assert json.loads(_run([console, 'notebook', 'update', '--path', root, '--json'],
                               cwd=scratch, env=env))['data']['already_current']
        cases.append({'language': language, 'source_version': SOURCE_VERSION,
                      'two_clarify_resources_refreshed': True, 'links_and_suggestions': True,
                      'story_history_custom_instructions_staging_preserved': True})

    checkout = Path(__file__).resolve().parents[1]
    legacy_probe = '''
import json,sys
from pathlib import Path
import novel_creator
assert Path(novel_creator.__file__).resolve().is_relative_to(Path(sys.prefix))
assert novel_creator.__version__ == sys.argv[4]
sys.path.append(sys.argv[1])
from tests.update_helpers import SOURCE_WHEELS
from tests import update_helpers
from tests.verify_update import installed_matrix
from contextlib import contextmanager
from novel_creator.install import bundle_files
SOURCE_WHEELS['0.7.1'] = (sys.argv[2], sys.argv[5])
historical_book = update_helpers.historical_book
@contextmanager
def checked_book(*args, **kwargs):
 with historical_book(*args, **kwargs) as book:
  yield book
  expected = bundle_files()
  for relative in ('.agents/skills/novel-clarify/SKILL.md', '.novel-creator/workflows/clarify.md'):
   assert (book.root / relative).read_bytes().replace(b'\\r\\n', b'\\n') == expected[relative].replace(b'\\r\\n', b'\\n')
  assert b'Custom' in (book.root / '.novel-creator/workflows/clarify.md').read_bytes()
update_helpers.historical_book = checked_book
result = installed_matrix([sys.argv[2]], sys.argv[3])
assert all(Path(module.__file__).resolve().is_relative_to(Path(sys.prefix))
 for name,module in sys.modules.items() if name.startswith('novel_creator') and getattr(module,'__file__',None))
print(json.dumps(result))
'''
    legacy = json.loads(_run([python, '-I', '-B', '-X', 'utf8', '-c', legacy_probe,
                             checkout, source, target_wheel, current_version, SOURCE_SHA256],
                            cwd=scratch, env=env))
    return {'source_version': SOURCE_VERSION, 'source_sha256': SOURCE_SHA256,
            'target_version': current_version,
            'legacy_target_matches_installed_product_files': target_file_count,
            'legacy_target_wheel_sha256': hashlib.sha256(Path(target_wheel).read_bytes()).hexdigest(),
            'notebooks': cases, 'legacy': legacy, 'native_host_evidence': False}
