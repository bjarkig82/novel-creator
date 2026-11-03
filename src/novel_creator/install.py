"""Explicit, pinned independent installation. No provider calls or global Git edits."""
import base64
import hashlib
import json
import os
from importlib.resources import files
from pathlib import Path
import re
import sys
import uuid

from . import records, storage, validation
from . import __version__
from .cli import ToolError


def bootstrap(original_text, novel_id=None, *, request=None):
    try:
        brief = records.loads(original_text)
        result = records.new_exchange(novel_id or str(uuid.uuid4()))
        artifact_id = str(uuid.uuid4())
        result['input_artifacts'] = [{'artifact_id': artifact_id, 'original_text': original_text,
            'parsed_value': brief, 'digest': hashlib.sha256(original_text.encode('utf-8')).hexdigest()}]
        result['record_versions'] = [records.project_from_brief(brief, result, artifact_id)]
        if request is not None:
            text = json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
            result['input_artifacts'].append({'artifact_id': str(uuid.uuid4()), 'original_text': text,
                'parsed_value': request, 'digest': hashlib.sha256(text.encode('utf-8')).hexdigest()})
        result['payload_digest'] = records.digest(result)
        validation.validate_exchange(result, [])
        return result
    except (ValueError, TypeError, KeyError) as error:
        raise ToolError(2, 'Invalid initialization brief: ' + str(error)) from error


def _resources(node, destination):
    result = {}
    for child in node.iterdir():
        if child.name.startswith('__') or child.name.endswith('.pyc'):
            continue
        target = destination + '/' + child.name
        if child.is_dir():
            result.update(_resources(child, target))
        else:
            result[target] = child.read_bytes()
    return result


def bundle_files():
    result = {'.novel-creator/src/novel_creator/' + p.name: p.read_bytes()
              for p in files('novel_creator').iterdir() if p.is_file() and p.name.endswith('.py')}
    result.update(_resources(files('novel_creator.schemas'), '.novel-creator/src/novel_creator/schemas'))
    # Explicit package markers also work without namespace-package assumptions.
    result['.novel-creator/src/novel_creator/schemas/__init__.py'] = b''
    result['.novel-creator/src/novel_creator/schemas/v1/__init__.py'] = b''
    for package, target in [('workflows', '.novel-creator/workflows'), ('languages', '.novel-creator/languages')]:
        result.update(_resources(files('novel_creator.' + package), target))
    codex = files('novel_creator.codex')
    result.update(_resources(codex.joinpath('skills'), '.agents/skills'))
    result['.novel-creator/run.py'] = (
        'from pathlib import Path\nimport sys\n'
        "sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))\n"
        'from novel_creator.cli import main\nraise SystemExit(main())\n').encode()
    # Framework resources are text governed by the installed LF attributes.
    # Brief artifacts and conversation text never pass through this conversion.
    return {name: raw.replace(b'\r\n', b'\n') for name, raw in result.items()}


def _append(original, addition):
    return original + (b'\n' if original and not original.endswith(b'\n') else b'') + addition


def _reserve_setup(path, state):
    """Publish one immutable setup plan; competing installers never replace it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.parent / 'install.lock'
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise ToolError(6, 'Setup lock held; inspect ownership before retry') from error
    try:
        if path.exists():
            raise ToolError(3, 'Another initialization owns this target; inspect and retry unchanged')
        storage.atomic_json(path, state)
    finally:
        lock.rmdir()


def _preflight(root):
    if sys.version_info < (3, 11):
        raise ToolError(4, 'Python >=3.11 is required')
    version = storage.git(root, '--version').decode()
    match = re.search(r'(\d+)\.(\d+)', version)
    if not match or tuple(map(int, match.groups())) < (2, 39):
        raise ToolError(4, 'Git >=2.39 is required')
    try:
        storage.git(root, 'var', 'GIT_AUTHOR_IDENT')
        storage.git(root, 'var', 'GIT_COMMITTER_IDENT')
    except ToolError as error:
        raise ToolError(error.code, 'Git identity is unavailable; configure your intended author/committer identity before retrying') from error


def _result(root, saved, *, already=False):
    result = dict(saved, operation='init')
    result['data'] = dict(saved['data'], already_initialized=already,
        brainstorming_optional=True, next_action='Open this novel folder in Codex and invoke $novel-init; brainstorming is optional.')
    if saved['data']['cleanup_required']:
        result['data']['next_action'] = 'Run recover inspection and explicit cleanup retry before continuing.'
    return result


def initialize(target, original_text, *, fault=None, request=None):
    candidate = bootstrap(original_text, request=request)  # Validate before any filesystem mutation.
    root = Path(target).absolute()
    if '..' in root.parts or root.resolve() != root:
        raise ToolError(2, 'Initialization requires a nonsymlink, nontraversing path')
    if root.exists() and not root.is_dir():
        raise ToolError(3, 'Target is not a directory')
    for parent in root.parents:
        if parent.exists() and storage.git(parent, 'rev-parse', '--show-toplevel', check=False).returncode == 0:
            raise ToolError(3, 'Novel must be outside the framework and every other Git repository')
    manifest_path = root / '.novel-creator/manifest.json'
    state_path = root / '.novel-creator/local/setup/state.json'
    if root.exists() and (root / '.novel-creator').exists():
        storage.root_path(root)
        storage.safe_path(root, '.novel-creator/manifest.json')
        storage.safe_path(root, '.novel-creator/local/setup/state.json')
        if manifest_path.is_symlink() or state_path.is_symlink():
            raise ToolError(2, 'Unsafe initialization metadata')
        history = storage.read_history(root)
        if history:
            manifest = records.loads(manifest_path.read_bytes())
            projects = [p for p in records.fold(history).values() if p['kind'] == 'novel_project']
            if len(projects) != 1 or projects[0]['id'] != manifest.get('novel_id'):
                raise ToolError(3, 'Existing repository is not a recognized novel project')
            for relative, digest in manifest.get('checksums', {}).items():
                if hashlib.sha256(storage.safe_path(root, relative, setup=True).read_bytes()).hexdigest() != digest:
                    raise ToolError(3, 'Installed bundle changed; explicit repair or upgrade required')
            point = storage.checkpoint(root, history)
            recovery = storage.recover(root, history[-1]['exchange_id'])
            result = _result(root, {'ok': True, 'novel_id': projects[0]['id'], 'warnings': [],
                'checkpoint': point, 'data': {'saved': True, 'cleanup_required': recovery['data']['cleanup_required']}}, already=True)
            return _command_result(root, result) if request is not None else result
        if not state_path.is_file():
            raise ToolError(3, 'Unrecognized partial installation; preserve it and choose another path')
        try:
            state = records.loads(state_path.read_bytes())
            if state['bundle']['input_artifacts'][0]['original_text'] != original_text:
                raise ToolError(3, 'Partial initialization requires the unchanged original brief')
            stored_requests = [a['parsed_value'] for a in state['bundle']['input_artifacts'][1:]
                               if isinstance(a['parsed_value'], dict)
                               and a['parsed_value'].get('request_type') == 'cli_init_v1']
            if stored_requests != ([] if request is None else [request]):
                raise ToolError(3, 'Partial initialization requires the original setup choices and input mode')
            validation.validate_exchange(state['bundle'], [])
            planned = {name: base64.b64decode(raw, validate=True) for name, raw in state['files'].items()}
        except (ValueError, TypeError, KeyError) as error:
            raise ToolError(4, 'Partial setup evidence is unreadable') from error
    else:
        allowed = {'.git', 'AGENTS.md', '.gitignore', '.gitattributes'}
        if root.exists() and any(p.name not in allowed or p.is_symlink() for p in root.iterdir()):
            raise ToolError(3, 'Existing content requires a separate novel path')
        if root.exists() and (root / '.git').exists():
            storage.root_path(root)
            if storage.head(root) is not None:
                raise ToolError(3, 'Existing repository is not an empty novel target')
        existing_parent = root if root.exists() else next(p for p in root.parents if p.exists())
        _preflight(existing_parent)
        planned = bundle_files()
        for name, addition in [('.gitignore', b'.novel-creator/local/\n__pycache__/\n*.pyc\n'),
                               ('.gitattributes', b'.novel-creator/** text eol=lf\nstory/exchanges/** text eol=lf\n.agents/skills/** text eol=lf\n')]:
            old = (root / name).read_bytes() if (root / name).exists() else b''
            planned[name] = _append(old, addition)
        planned['AGENTS.md'] = ((root / 'AGENTS.md').read_bytes() if (root / 'AGENTS.md').exists()
                                else files('novel_creator.codex').joinpath('AGENTS.production.md').read_bytes())
        manifest = {'novel_id': candidate['novel_id'], 'schema_version': '1.0', 'bundle_version': __version__,
                    'managed_paths': sorted(planned), 'checksums': {
                        name: hashlib.sha256(raw).hexdigest() for name, raw in planned.items()}}
        planned['.novel-creator/manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
        state = {'bundle': candidate, 'files': {name: base64.b64encode(raw).decode('ascii') for name, raw in planned.items()}}
        root.mkdir(parents=True, exist_ok=True)
        if not (root / '.git').exists():
            storage.git(root, 'init', '-b', 'main')
        _reserve_setup(storage.safe_path(root, '.novel-creator/local/setup/state.json'), state)
    _preflight(root)
    for name, raw in planned.items():
        path = storage.safe_path(root, name, setup=True)
        if path.exists():
            # Preserved metadata files may still have their original prefix on first setup.
            if path.read_bytes() != raw:
                if name in ('.gitignore', '.gitattributes') and raw.startswith(path.read_bytes()) and not manifest_path.exists():
                    path.write_bytes(raw)
                else:
                    raise ToolError(3, 'Partial installation file changed; preserve it before recovery', affected_refs=[name])
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
    saved = storage.save(root, state['bundle'], fault=fault)
    result = _result(root, saved)
    return _command_result(root, result) if request is not None else result


def _command_result(root, result):
    guide = root / '.novel-creator/workflows/getting-started.md'
    manifest = records.loads(storage.safe_path(root, '.novel-creator/manifest.json').read_bytes())
    if '.novel-creator/workflows/getting-started.md' in manifest.get('checksums', {}):
        guide = storage.safe_path(root, '.novel-creator/workflows/getting-started.md', setup=True)
        if hashlib.sha256(guide.read_bytes()).hexdigest() != manifest['checksums']['.novel-creator/workflows/getting-started.md']:
            raise ToolError(3, 'Pinned guide changed; preserve the novel and inspect its resources')
    else:
        guide = Path(str(files('novel_creator.workflows').joinpath('getting-started.md')))
        if not guide.is_file():
            raise ToolError(4, 'Getting-started documentation is unavailable; preserve this novel and repair the package')
        result['warnings'].append('Package-guide fallback: this older novel keeps its pinned workflows; reading the guide does not upgrade them.')
    # Linux venv interpreters are often symlinks; resolving them selects base Python.
    result['data'].update(novel_path=str(root), runtime_python=str(Path(sys.executable).absolute()),
        launcher_path=str(root / '.novel-creator/run.py'), getting_started_path=str(guide),
        ready=bool(result['data']['saved'] and not result['data']['cleanup_required']))
    if result['data']['already_initialized']:
        result['warnings'].append('Existing novel: requested replacement settings were not applied.')
    return result
