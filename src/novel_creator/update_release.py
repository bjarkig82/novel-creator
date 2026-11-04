"""Versioned bundle export and read-only compatibility checks.

Release acquisition and private preparation are separate from book mutations.
No provider or contribution service is constructed by these protocol helpers.
"""
import base64
from functools import lru_cache, wraps
import hashlib
from importlib.resources import files
import json
import io
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
from email.parser import BytesParser
import urllib.request
from urllib.parse import urlsplit
import zipfile

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version, InvalidVersion

from jsonschema import Draft202012Validator, FormatChecker

from . import records, validation
from .cli import ToolError


INDEX_URL = 'https://pypi.org/pypi/novel-creator/json'
MAX_DOWNLOAD = 50 * 1024 * 1024
MAX_EXPANDED = 128 * 1024 * 1024


def require_public_url(url):
    try:
        parsed = urlsplit(url)
        if (parsed.scheme != 'https' or parsed.hostname not in ('pypi.org', 'files.pythonhosted.org')
                or parsed.username is not None or parsed.password is not None
                or parsed.port not in (None, 443) or parsed.query or parsed.fragment):
            raise ValueError()
    except (ValueError, TypeError, AttributeError) as error:
        raise ToolError(4, 'Release URL is outside the fixed public source boundary') from error
    return url


class _PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, newurl):
        require_public_url(newurl)
        return super().redirect_request(request, file, code, message, headers, newurl)


class PublicReleaseTransport:
    def get(self, url):
        require_public_url(url)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _PublicRedirect())
        try:
            with opener.open(urllib.request.Request(url, headers={'User-Agent': 'novel-creator-update/1'}), timeout=30) as response:
                require_public_url(response.geturl())
                raw = response.read(MAX_DOWNLOAD + 1)
                if len(raw) > MAX_DOWNLOAD:
                    raise ValueError()
                return raw
        except (OSError, ValueError) as error:
            raise ToolError(5, 'Public release lookup/download failed; installed book is unchanged') from error


def release_index(transport=None):
    try:
        value = (transport or PublicReleaseTransport()).get(INDEX_URL)
        value = records.loads(value) if isinstance(value, (str, bytes)) else value
        if not isinstance(value, dict) or not isinstance(value.get('releases'), dict):
            raise ValueError()
        return value
    except (OSError, ValueError, TypeError) as error:
        raise ToolError(5, 'Release availability is unknown; retry the explicit check later') from error


def stable_version(value):
    try:
        version = Version(value)
        if version.is_prerelease or version.is_devrelease or version.local:
            raise InvalidVersion(value)
        return version
    except (InvalidVersion, TypeError) as error:
        raise ToolError(2, 'Choose a published stable version without local or prerelease suffixes') from error


def select_release(metadata, *, version=None, runtime=None):
    runtime = runtime or runtime_info()
    if not isinstance(metadata, dict) or not isinstance(metadata.get('releases'), dict):
        raise ToolError(5, 'Release availability is unknown')
    choices = {}
    for key, items in metadata['releases'].items():
        try:
            parsed = stable_version(key)
        except ToolError:
            continue
        entries = [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []
        if any(not item.get('yanked') for item in entries):
            choices[parsed] = entries
    if not choices:
        raise ToolError(5, 'No published stable release could be established')
    chosen = stable_version(version) if version is not None else max(choices)
    if chosen not in choices:
        raise ToolError(4, 'Selected stable release is unavailable or yanked')
    python_version = '.'.join(map(str, runtime['version'][:3]))
    for item in sorted(choices[chosen], key=lambda value: str(value.get('filename', ''))):
        try:
            if item.get('yanked') or item.get('packagetype') != 'bdist_wheel':
                continue
            name, wheel_version, _, tags = parse_wheel_filename(item['filename'])
            if canonicalize_name(name) != 'novel-creator' or wheel_version != chosen:
                continue
            if not {str(tag) for tag in tags}.intersection(runtime['tags']):
                continue
            if not SpecifierSet(item.get('requires_python') or '').contains(python_version):
                continue
            result = {'project': 'novel-creator', 'version': str(chosen),
                      'filename': item['filename'], 'sha256': item['digests']['sha256'],
                      'size': item['size'], 'url': require_public_url(item['url'])}
            schema = records.loads(files('novel_creator.schemas.v1').joinpath('update.schema.json').read_bytes())
            if not Draft202012Validator({'$defs': schema['$defs'], '$ref': '#/$defs/artifact'}).is_valid(result):
                continue
            if type(result['size']) is not int or result['size'] > MAX_DOWNLOAD:
                continue
            return result
        except (ValueError, TypeError, KeyError, ToolError):
            continue
    raise ToolError(4, 'Selected release has no supported verified wheel for this configured runtime; no older release was substituted')


def validate_artifact(value):
    schema = records.loads(files('novel_creator.schemas.v1').joinpath('update.schema.json').read_bytes())
    if not Draft202012Validator({'$defs': schema['$defs'], '$ref': '#/$defs/artifact'}).is_valid(value):
        raise ToolError(4, 'Invalid release artifact identity')
    require_public_url(value['url'])
    stable_version(value['version'])
    if value['size'] > MAX_DOWNLOAD:
        raise ToolError(4, 'Release archive exceeds the supported size')
    return value


def _relative(name):
    path = PurePosixPath(name)
    if (not name or not path.parts or path.is_absolute() or str(path) != name
            or '..' in path.parts or any(ord(character) < 32 or character in '\\:<>"|?*' for character in name)
            or any(part.endswith((' ', '.')) or re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I)
                   for part in path.parts)):
        raise ToolError(4, 'Release archive contains an unsafe path')
    return path


def wheel_inventory(raw, artifact):
    if not isinstance(raw, bytes) or len(raw) != artifact['size'] or digest(raw) != artifact['sha256']:
        raise ToolError(4, 'Release archive does not match the reviewed public identity')
    result = {}
    seen = set()
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            infos = archive.infolist()
            if len(infos) > 4096 or sum(info.file_size for info in infos) > MAX_EXPANDED:
                raise ValueError()
            for info in infos:
                name = info.filename.rstrip('/') if info.is_dir() else info.filename
                path = _relative(name)
                if name.casefold() in seen or stat.S_ISLNK(info.external_attr >> 16):
                    raise ValueError()
                seen.add(name.casefold())
                if info.is_dir():
                    continue
                mode = stat.S_IFMT(info.external_attr >> 16)
                if mode not in (0, stat.S_IFREG):
                    raise ValueError()
                if path.parts[0] != 'novel_creator' and not (
                        len(path.parts) == 2 and path.parts[0].startswith('novel_creator-')
                        and path.parts[0].endswith('.dist-info')):
                    raise ValueError()
                result[name] = archive.read(info)
        metadata_names = [name for name in result if name.endswith('.dist-info/METADATA')]
        if (len(metadata_names) != 1 or metadata_names[0].split('/')[0] != 'novel_creator-' + artifact['version'] + '.dist-info'
                or any(name.split('/')[0].endswith('.dist-info') and name.split('/')[0] != metadata_names[0].split('/')[0]
                       for name in result)):
            raise ValueError()
        metadata = BytesParser().parsebytes(result[metadata_names[0]])
        if (len(metadata.get_all('Name', [])) != 1 or len(metadata.get_all('Version', [])) != 1
                or canonicalize_name(metadata['Name']) != 'novel-creator'
                or Version(metadata['Version']) != Version(artifact['version'])):
            raise ValueError()
    except (ValueError, TypeError, KeyError, RuntimeError, NotImplementedError, EOFError, zipfile.BadZipFile, OSError) as error:
        raise ToolError(4, 'Release wheel has invalid paths, modes, or distribution metadata') from error
    return result


def clean_environment():
    names = ('PATH', 'SYSTEMROOT', 'SystemRoot', 'WINDIR', 'COMSPEC', 'PATHEXT',
             'TEMP', 'TMP', 'LANG', 'LC_ALL')
    environment = {name: os.environ[name] for name in names if name in os.environ}
    environment.update(PIP_CONFIG_FILE=os.devnull, PIP_DISABLE_PIP_VERSION_CHECK='1',
                       PYTHONDONTWRITEBYTECODE='1')
    return environment


def _run(argv, *, cwd=None, payload=None):
    try:
        result = subprocess.run(list(map(str, argv)), cwd=cwd, env=clean_environment(),
                                input=payload, capture_output=True, timeout=300)
        if result.returncode:
            raise ValueError()
        return result.stdout
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        raise ToolError(4, 'Isolated release preparation/probe failed; check the configured runtime prerequisites') from error


_RUNTIME_SCRIPT = '''
import sys,sysconfig,json,importlib.metadata as metadata
from pathlib import Path
from packaging.tags import sys_tags
from packaging.markers import default_environment
names=sorted({d.metadata['Name'] for d in metadata.distributions() if d.metadata['Name']})
print(json.dumps({'python':str(Path(sys.executable).absolute()),'version':list(sys.version_info[:3]),
 'site_paths':list(dict.fromkeys(str(Path(p).absolute()) for p in sys.path if Path(p).name in ('site-packages','dist-packages'))),
 'distributions':{name:metadata.version(name) for name in names},
 'tags':[str(tag) for tag in sys_tags()],'marker_environment':default_environment()}))
'''


def runtime_info(python=None):
    if python is not None and not Path(python).is_absolute():
        raise ToolError(2, '--python requires an absolute configured interpreter path')
    selected = str(Path(python or sys.executable).absolute())
    try:
        result = records.loads(_run([selected, '-I', '-B', '-X', 'utf8', '-c', _RUNTIME_SCRIPT]))
        if (result['version'][:2] < [3, 11] or not result['site_paths']
                or 'pip' not in result['distributions']):
            raise ValueError()
        result['fingerprint'] = digest(canonical(result))
        return result
    except (ValueError, KeyError, TypeError) as error:
        raise ToolError(4, 'Configured Python needs Python >=3.11, pip, packaging and the selected release dependencies') from error


def create_environment(destination, python=None):
    destination = Path(destination).absolute()
    if destination.exists():
        raise ToolError(3, 'Private preparation environment already exists')
    runtime = runtime_info(python)
    _run([runtime['python'], '-I', '-B', '-X', 'utf8', '-c',
          'import sys,venv; venv.EnvBuilder(with_pip=False).create(sys.argv[1])', destination])
    selected = destination / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    site = Path(_run([selected, '-I', '-B', '-c',
                     "import sysconfig; print(sysconfig.get_path('purelib'))"]).decode().strip())
    if not site.is_relative_to(destination):
        raise ToolError(4, 'Private interpreter does not own its installation directory')
    (site / 'update-dependencies.pth').write_text(
        ''.join(path + '\n' for path in runtime['site_paths']), encoding='utf-8')
    return str(selected)


def cache_home():
    base = (Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local')) / 'NovelCreator'
            if os.name == 'nt' else Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')) / 'novel-creator')
    return base / 'updates'


def _check_dependencies(inventory, artifact, runtime):
    metadata = BytesParser().parsebytes(next(raw for name, raw in inventory.items()
                                           if name.endswith('.dist-info/METADATA')))
    try:
        if not SpecifierSet(metadata.get('Requires-Python', '')).contains('.'.join(map(str, runtime['version']))):
            raise ToolError(4, 'Selected release requires a different configured Python')
        installed = {canonicalize_name(name): value for name, value in runtime['distributions'].items()}
        for value in metadata.get_all('Requires-Dist', []):
            requirement = Requirement(value)
            if requirement.url:
                raise ValueError()
            if requirement.marker and not requirement.marker.evaluate(dict(runtime['marker_environment'], extra='')):
                continue
            existing = installed.get(canonicalize_name(requirement.name))
            if existing is None or existing not in requirement.specifier:
                raise ValueError()
    except (ValueError, TypeError) as error:
        raise ToolError(4, 'Selected release dependencies are unavailable; repair the configured interpreter explicitly') from error


def _installed_inventory(package_root, expected):
    actual = {}
    for path in package_root.rglob('*'):
        if path.is_symlink():
            raise ToolError(4, 'Private product installation contains a redirected path')
        if path.is_file():
            actual['novel_creator/' + path.relative_to(package_root).as_posix()] = path.read_bytes()
    wanted = {name: raw for name, raw in expected.items() if name.startswith('novel_creator/')}
    if actual != wanted:
        raise ToolError(4, 'Private product module/resource inventory differs from the verified wheel')


def bundle_inventory(inventory, *, legacy=False):
    """Derive the complete installed inventory without trusting an exporter."""
    result = {}
    for name, raw in inventory.items():
        relative = name.removeprefix('novel_creator/')
        if relative == name:
            continue
        destination = None
        if '/' not in relative and (relative.endswith('.py') or relative == 'update-release.json'):
            destination = '.novel-creator/src/novel_creator/' + relative
        for prefix, target in (('schemas/', '.novel-creator/src/novel_creator/schemas/'),
                               ('workflows/', '.novel-creator/workflows/'),
                               ('languages/', '.novel-creator/languages/'),
                               ('codex/skills/', '.agents/skills/')):
            if relative.startswith(prefix) and not any(part.startswith('__') for part in relative[len(prefix):].split('/')):
                destination = target + relative[len(prefix):]
        if destination:
            result[destination] = raw.replace(b'\r\n', b'\n')
    for name in ('schemas/__init__.py', 'schemas/v1/__init__.py'):
        result['.novel-creator/src/novel_creator/' + name] = b''
    if legacy:
        launcher = ('from pathlib import Path\nimport sys\n'
                    "sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))\n"
                    'from novel_creator.cli import main\nraise SystemExit(main())\n').encode()
    else:
        from .install import bundle_files
        launcher = bundle_files()['.novel-creator/run.py']
    result['.novel-creator/run.py'] = launcher
    return result


def _metadata_boundary(function):
    @wraps(function)
    def checked(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (ValueError, TypeError, KeyError, AttributeError, RecursionError) as error:
            raise ToolError(4, 'Selected release metadata/export is invalid; preserve the book and inspect the selected artifact') from error
    return checked


@_metadata_boundary
def prepare(artifact, *, python=None, transport=None):
    validate_artifact(artifact)
    runtime = runtime_info(python)
    try:
        raw = (transport or PublicReleaseTransport()).get(require_public_url(artifact['url']))
    except OSError as error:
        raise ToolError(5, 'Selected release download failed; book remains unchanged') from error
    inventory = wheel_inventory(raw, artifact)
    _check_dependencies(inventory, artifact, runtime)
    if 'novel_creator/codex/AGENTS.production.md' not in inventory:
        raise ToolError(4, 'Selected release lacks its supported default instruction template')
    try:
        release_protocol = records.loads(inventory['novel_creator/update-release.json'])
        validate_document('release', release_protocol)
    except (KeyError, ValueError) as error:
        raise ToolError(4, 'Selected release does not support update protocol 1') from error
    home = cache_home().resolve()
    home.mkdir(parents=True, mode=0o700, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='prepared-', dir=home))
    wheel = folder / artifact['filename']
    wheel.write_bytes(raw)
    env_python = create_environment(folder / 'environment', runtime['python'])
    _run([env_python, '-I', '-B', '-X', 'utf8', '-m', 'pip', '--isolated',
          '--disable-pip-version-check', 'install', '--ignore-installed', '--no-index',
          '--no-deps', '--no-compile', '--no-cache-dir', wheel], cwd=folder)
    site = Path(_run([env_python, '-I', '-B', '-c',
                     "import sysconfig; print(sysconfig.get_path('purelib'))"]).decode().strip())
    package_root = site / 'novel_creator'
    _installed_inventory(package_root, inventory)
    program = '''
import sys,json,importlib.util
from pathlib import Path
root=Path(sys.argv[1]); expected=sys.argv[2]
spec=importlib.util.find_spec('novel_creator')
if spec is None or Path(spec.origin).parent != root: raise ValueError('Product origin mismatch')
import novel_creator
from packaging.version import Version
if Version(novel_creator.__version__) != Version(expected): raise ValueError('Product version mismatch')
from novel_creator.update_release import export_bundle
result=export_bundle()
for name,module in list(sys.modules.items()):
 if name.startswith('novel_creator') and getattr(module,'__file__',None):
  if not Path(module.__file__).resolve().is_relative_to(root): raise ValueError('Product module origin mismatch')
print(json.dumps(result,ensure_ascii=False))
'''
    exported = records.loads(_run([env_python, '-I', '-B', '-X', 'utf8', '-c',
                                  program, package_root, artifact['version']], cwd=folder))
    _installed_inventory(package_root, inventory)
    validate_document('release', exported['protocol'])
    if exported['protocol'] != release_protocol:
        raise ToolError(4, 'Target export protocol differs from its packaged declaration')
    decoded = {}
    from .install import bundle_files
    current_launcher = bundle_files()['.novel-creator/run.py']
    for path, encoded in exported['files'].items():
        _relative(path)
        content = base64.b64decode(encoded, validate=True)
        if path == '.novel-creator/run.py':
            expected = current_launcher
        else:
            source = None
            for prefix, target in (
                ('.novel-creator/src/novel_creator/', 'novel_creator/'),
                ('.novel-creator/workflows/', 'novel_creator/workflows/'),
                ('.novel-creator/languages/', 'novel_creator/languages/'),
                ('.agents/skills/', 'novel_creator/codex/skills/')):
                if path.startswith(prefix):
                    source = target + path[len(prefix):]
                    break
            if source not in inventory:
                raise ToolError(4, 'Target bundle contains a path outside the verified package')
            expected = inventory[source].replace(b'\r\n', b'\n')
            if path in ('.novel-creator/src/novel_creator/schemas/__init__.py',
                        '.novel-creator/src/novel_creator/schemas/v1/__init__.py'):
                expected = b''
        if content != expected or exported['checksums'].get(path) != digest(content) or exported['modes'].get(path) != '100644':
            raise ToolError(4, 'Target bundle does not match its verified wheel inventory')
        decoded[path] = content
    if decoded != bundle_inventory(inventory):
        raise ToolError(4, 'Target export omits or adds verified package resources')
    hashes = {path: {'sha256': digest(content), 'mode': '100644'} for path, content in sorted(decoded.items())}
    if digest(canonical(hashes)) != exported['bundle_digest']:
        raise ToolError(4, 'Target bundle digest is invalid')
    return {'version': artifact['version'], 'artifact': artifact, 'protocol': release_protocol,
            'files': decoded, 'checksums': exported['checksums'], 'modes': exported['modes'],
            'bundle_digest': exported['bundle_digest'], 'runtime': runtime,
            'env_python': env_python, 'package_root': str(package_root), 'wheel_path': str(wheel),
            'agents_default': inventory.get('novel_creator/codex/AGENTS.production.md')}


def probe_prepared(prepared, snapshot):
    """Validate immutable JSON via the verified product, with no book path."""
    inventory = wheel_inventory(Path(prepared['wheel_path']).read_bytes(), prepared['artifact'])
    if snapshot.get('retro_documents') and 1 not in prepared['protocol']['retro_versions']:
        raise ToolError(4, 'Selected release does not declare support for retained retrospective records')
    root = Path(prepared['package_root'])
    _installed_inventory(root, inventory)
    program = '''
import sys,json,importlib.util
from pathlib import Path
root=Path(sys.argv[1]); expected=sys.argv[2]
spec=importlib.util.find_spec('novel_creator')
if spec is None or Path(spec.origin).parent != root: raise ValueError('Product origin mismatch')
import novel_creator
from packaging.version import Version
if Version(novel_creator.__version__) != Version(expected): raise ValueError('Product version mismatch')
from novel_creator.update_release import validate_snapshot
result=validate_snapshot(json.load(sys.stdin))
for name,module in list(sys.modules.items()):
 if name.startswith('novel_creator') and getattr(module,'__file__',None):
  if not Path(module.__file__).resolve().is_relative_to(root): raise ValueError('Product module origin mismatch')
print(json.dumps(result))
'''
    result = records.loads(_run([prepared['env_python'], '-I', '-B', '-X', 'utf8', '-c',
                                program, root, prepared['version']],
                               cwd=Path(prepared['wheel_path']).parent, payload=canonical(snapshot)))
    _installed_inventory(root, inventory)
    if result.get('valid') is not True:
        raise ToolError(4, 'Selected release cannot read the existing immutable records')
    return result


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


@lru_cache(maxsize=None)
def document_validator(kind):
    schema = records.loads(files('novel_creator.schemas.v1').joinpath('update.schema.json').read_bytes())
    if kind not in ('release', 'active', 'preview', 'operation'):
        raise ToolError(4, 'Unsupported update document kind')
    return Draft202012Validator({'$defs': schema['$defs'], '$ref': '#/$defs/' + kind},
                                 format_checker=FormatChecker())


def validate_document(kind, value):
    if not document_validator(kind).is_valid(value):
        raise ToolError(4, 'Invalid or unsupported update metadata')
    return value


def protocol():
    value = records.loads(files('novel_creator').joinpath('update-release.json').read_bytes())
    return validate_document('release', value)


def export_bundle():
    from .install import bundle_files
    inventory = bundle_files()
    hashes = {name: digest(raw) for name, raw in sorted(inventory.items())}
    modes = {name: '100644' for name in hashes}
    return {'protocol': protocol(), 'files': {
                name: base64.b64encode(raw).decode('ascii') for name, raw in sorted(inventory.items())},
            'checksums': hashes, 'modes': modes,
            'bundle_digest': digest(canonical({name: {'sha256': hashes[name], 'mode': modes[name]}
                                                for name in hashes}))}


def validate_snapshot(snapshot):
    """Consume local immutable values; never a path, cache, or service instance."""
    if (not isinstance(snapshot, dict) or set(snapshot) != {'history', 'retro_documents'}
            or not isinstance(snapshot['history'], list) or not snapshot['history']
            or not isinstance(snapshot['retro_documents'], list)):
        raise ToolError(2, 'Invalid update compatibility snapshot')
    try:
        chain = validation.ExchangeValidator()
        for exchange in snapshot['history']:
            chain.append(exchange)
        # Import only the schema validation function, never a Retro instance.
        from .retro import validate as validate_retro
        kinds = records.loads(files('novel_creator.schemas.v1').joinpath('retro.schema.json').read_bytes())['$defs']
        for document in snapshot['retro_documents']:
            if not isinstance(document, dict) or set(document) != {'kind', 'value'}:
                raise ValueError('Invalid operational document wrapper')
            if document['kind'] not in kinds:
                raise ValueError('Unsupported operational document kind')
            validate_retro(document['value'], document['kind'])
    except (ValueError, TypeError, KeyError, ToolError) as error:
        raise ToolError(4, 'Selected release cannot validate existing book records or operational state') from error
    return {'valid': True, 'exchange_count': len(snapshot['history'])}
