"""Preview-bound, addition-only side-character maintenance for format-1 notebooks.

This external-package helper never adopts integrations, replaces snapshots,
stages files or runs notebook-controlled code. Normal writing needs no Python.
"""
import hashlib
from importlib.resources import files
import json
import os
from pathlib import Path
import re
import stat
import subprocess

from . import __version__
from .cli import ToolError
from .notebook import _append_side_character, _host_text, _instructions


def _identity(info):
    return info.st_dev, info.st_ino


def _safe(path):
    if '..' in path.parts or path.resolve() != path:
        raise ToolError(3, 'Side-character maintenance refuses redirected paths and parent segments')
    for part in (*reversed(path.parents), path):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
                or not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode))):
            raise ToolError(3, 'Side-character maintenance refuses redirected or special paths')
        if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
            raise ToolError(3, 'Side-character maintenance refuses hard-linked files')
    return path


def _write(path, raw, previous, recheck):
    """Exclusive additions or checked append, retaining the original inode/bytes."""
    _safe(path)
    # Directory creation is application-only. Recheck identities again afterwards.
    path.parent.mkdir(parents=True, exist_ok=True)
    _safe(path)
    recheck()
    if previous is None:
        with path.open('xb') as stream:
            _safe(path)
            opened = os.fstat(stream.fileno())
            if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1 or _identity(path.stat()) != _identity(opened):
                raise ToolError(3, 'New notebook resource changed identity before writing')
            recheck(True)  # The exclusive new file is the sole changed input.
            _safe(path)
            current = path.stat()
            checked = os.fstat(stream.fileno())
            if (not stat.S_ISREG(checked.st_mode) or checked.st_nlink != 1 or current.st_nlink != 1
                    or _identity(checked) != _identity(opened) or _identity(current) != _identity(opened)):
                raise ToolError(3, 'New notebook resource changed identity or links during final recheck')
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    else:
        with path.open('r+b') as stream:
            _safe(path)
            opened = os.fstat(stream.fileno())
            if (not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1
                    or _identity(opened) != previous[1] or _identity(path.stat()) != previous[1]
                    or stream.read() != previous[0]):
                raise ToolError(3, 'Notebook instructions changed bytes or original identity before append')
            # All other inspected inputs are checked with this handle already open.
            recheck()
            if _identity(path.stat()) != previous[1]:
                raise ToolError(3, 'Notebook instructions changed identity before append')
            stream.write(raw[len(previous[0]):])
            stream.flush()
            os.fsync(stream.fileno())


def update(target, *, apply=False, preview_id=None, expected_head=None):
    """Return an immutable review binding, or explicitly apply that exact plan.

    Every existing feature resource must match the selected rendered defaults.
    Other resources/roles are read-only prerequisites. Incomplete applications
    report actual written/attempted paths; a fresh preview resumes missing work.
    """
    if apply != (preview_id is not None and expected_head is not None) or (
            not apply and (preview_id is not None or expected_head is not None)):
        raise ToolError(2, 'Side-character apply requires apply, preview_id and expected_head together')
    root = _safe(Path(target).absolute())
    if not root.is_dir() or not _safe(root / '.git').is_dir():
        raise ToolError(3, 'Side-character maintenance requires an independent local notebook Git root')
    if _safe(root / '.novel-creator').exists():
        raise ToolError(3, 'Legacy, retained-legacy and mixed formats use their separate framework update')
    inputs, parents, resources = {}, {}, {}

    def inspect(relative, required=False):
        path = _safe(root / relative)
        # Bind all destination parents, including absent directories. Reading
        # preview must never create a missing skill directory or cache.
        parents['.'] = _identity(root.stat())
        parent = path.parent
        while parent != root:
            key = parent.relative_to(root).as_posix()
            if parent.exists() and not parent.is_dir():
                raise ToolError(3, 'Invalid notebook resource parent: ' + key)
            parents[key] = _identity(parent.stat()) if parent.exists() else None
            parent = parent.parent
        if path.exists():
            info = path.stat()
            if not stat.S_ISREG(info.st_mode) or not info.st_mode & 0o444:
                raise ToolError(3, 'Notebook resource is not a readable regular file: ' + relative)
            with path.open('rb') as stream:
                opened = os.fstat(stream.fileno())
                raw = stream.read()
                _safe(path)
                if (_identity(opened) != _identity(info) or _identity(path.stat()) != _identity(info)
                        or not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1):
                    raise ToolError(3, 'Notebook input changed identity while reading: ' + relative)
                value = raw, _identity(opened)
        else:
            if required:
                raise ToolError(3, 'Required notebook prerequisite is missing: ' + relative)
            value = None
        inputs[relative] = value
        return None if value is None else value[0]

    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')

    def git(*args):
        result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=' + os.devnull,
                                 '-C', str(root), *args], env=env, capture_output=True)
        if result.returncode:
            raise ToolError(3, 'Cannot inspect local notebook Git state')
        return os.fsdecode(result.stdout).strip()

    for name in ('.git/HEAD', '.git/index', '.git/config'):
        inspect(name, True)
    for name in ('.git/commondir', '.git/objects/info/alternates', '.git/objects/info/http-alternates'):
        if inspect(name) is not None:
            raise ToolError(3, 'Redirected/shared Git storage is unsupported: ' + name)
    if (Path(git('rev-parse', '--show-toplevel')).resolve() != root
            or Path(git('rev-parse', '--absolute-git-dir')).resolve() != root / '.git'
            or Path(git('rev-parse', '--path-format=absolute', '--git-common-dir')).resolve() != root / '.git'
            or Path(git('rev-parse', '--path-format=absolute', '--git-path', 'index')).absolute() != root / '.git/index'
            or Path(git('rev-parse', '--path-format=absolute', '--git-path', 'objects')).absolute() != root / '.git/objects'
            or git('rev-parse', '--shared-index-path')):
        raise ToolError(3, 'Notebook requires local independent Git worktree, index and objects')
    _safe(root / '.git/objects')
    head = git('rev-parse', '--verify', 'HEAD')
    ref = git('rev-parse', '--symbolic-full-name', 'HEAD')
    if ref != 'HEAD':
        if not ref.startswith('refs/') or '..' in Path(ref).parts:
            raise ToolError(3, 'Unsupported notebook HEAD reference')
        inspect('.git/' + ref)
    inspect('.git/packed-refs')
    project = inspect('notebook/project.md', True)
    try:
        match = re.match(rb'\A(```|~~~)json\r?\n(.*?)\r?\n\1(?:\r?\n|\Z)', project, re.S)
        metadata = json.loads(match[2]) if match else None
        if (not isinstance(metadata, dict) or type(metadata.get('version')) is not int
                or (metadata.get('format'), metadata.get('version'), metadata.get('kind'), metadata.get('id')) !=
                ('novel-notebook', 1, 'project', 'project') or metadata.get('language') not in ('en', 'is')):
            raise ValueError()
    except (ValueError, TypeError, UnicodeError):
        raise ToolError(3, 'Side-character maintenance requires valid format-1 en/is notebook metadata') from None
    language = metadata['language']
    host, source = 'codex', 'project'
    marker = inspect('.novel-notebook/integration.json')
    if marker is not None:
        try:
            integration = json.loads(marker)
            if (not isinstance(integration, dict) or set(integration) != {'version', 'host', 'skill_source'}
                    or type(integration['version']) is not int or integration['version'] != 1
                    or integration['host'] not in ('codex', 'claude', 'both')
                    or integration['skill_source'] not in ('project', 'plugin')):
                raise ValueError()
            host, source = integration['host'], integration['skill_source']
        except (ValueError, TypeError, UnicodeError):
            raise ToolError(3, 'Invalid or unsupported notebook integration marker') from None
    selected_hosts = ('codex', 'claude') if host == 'both' else (host,)
    for selected in ('codex', 'claude'):
        relative = ('.agents' if selected == 'codex' else '.claude') + '/skills/novel-side-character/SKILL.md'
        existing = inspect(relative)
        if existing is not None and (source == 'plugin' or selected not in selected_hosts):
            raise ToolError(3, 'Duplicate/unselected local side-character skill requires manual reconciliation: ' + relative)
    inspect('notebook/working-summary.md', True)
    inspect('.novel-notebook/languages/' + language + '.md', True)
    for name in ('conversation', 'format', 'agents'):
        inspect('.novel-notebook/workflows/' + name + '.md', True)
    codex = files('novel_creator.codex').joinpath('notebook')
    shared = files('novel_creator.notebook_resources').joinpath('workflows')
    desired = {}
    links = {}
    for name in ('__init__.py', 'notebook.py', 'notebook_side_character.py'):
        location = _safe(Path(str(files('novel_creator').joinpath(name))).absolute())
        resources[str(location)] = [hashlib.sha256(location.read_bytes()).hexdigest(), _identity(location.stat())]

    def resource(relative, resource, rendered):
        # Bind package-resource physical identity and bytes as well as the output.
        location = Path(str(resource)).absolute()
        _safe(location)
        info = location.stat()
        resources[str(location)] = [hashlib.sha256(location.read_bytes()).hexdigest(), _identity(info)]
        raw = rendered.replace(b'\r\n', b'\n')
        original = inspect(relative)
        if original is not None and original.replace(b'\r\n', b'\n') != raw:
            raise ToolError(3, 'Customized side-character feature resource must be reconciled manually: ' + relative)
        desired[relative] = original if original is not None else raw
        links[relative] = raw

    workflow = shared.joinpath('side-character.md')
    resource('.novel-notebook/workflows/side-character.md', workflow,
             _host_text(workflow.read_text(encoding='utf-8'), host, source).encode())
    for selected in selected_hosts:
        relative = 'AGENTS.md' if selected == 'codex' else 'CLAUDE.md'
        original = inspect(relative, True)
        try:
            text = original.decode('utf-8')
        except UnicodeError:
            raise ToolError(3, 'Notebook instructions must be UTF-8') from None
        template = _instructions(codex, selected, source)
        # Bind actual root/Claude fragment resources used by _instructions.
        for location in (codex.joinpath('AGENTS.md'), *(
                (files('novel_creator.claude').joinpath('notebook/CLAUDE.fragment.md'),) if selected == 'claude' else ())):
            path = _safe(Path(str(location)).absolute())
            resources[str(path)] = [hashlib.sha256(path.read_bytes()).hexdigest(), _identity(path.stat())]
        updated = _append_side_character(original, template)
        # Conservative label preflight, not semantic policy interpretation:
        # feature-specific text outside the managed block needs human review,
        # regardless of word order, action verbs, line breaks or language.
        # Older generic enrichment/save guidance is superseded by the block.
        outside = re.sub(r'<!-- novel-creator:side-character:start -->.*?<!-- novel-creator:side-character:end -->', '', text, flags=re.S)
        if re.search(r'\b(?:side|supporting|minor)[\s\-\u2010\u2011]+characters?\b|\baukapersón\w*', outside, re.I):
            raise ToolError(3, 'Custom side-character writer instructions require manual reconciliation: ' + relative)
        newline = b'\r\n' if b'\r\n' in original else b'\n'
        desired[relative] = original + updated[len(original):].replace(b'\n', newline)
        links[relative] = updated[len(original):] if updated != original else re.search(
            rb'<!-- novel-creator:side-character:start -->.*?<!-- novel-creator:side-character:end -->', original, re.S).group()
        if source == 'project':
            skill = codex.joinpath('skills/novel-side-character/SKILL.md')
            resource(('.agents' if selected == 'codex' else '.claude') + '/skills/novel-side-character/SKILL.md',
                     skill, _host_text(skill.read_text(encoding='utf-8'), selected, source).encode())
    # Validate only the feature section's root links; unrelated custom root text
    # stays byte-identical and is not claimed as feature-owned.
    for relative, raw in links.items():
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', raw.decode('utf-8')):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                continue
            destination = Path(os.path.abspath((root / relative).parent / link))
            if not destination.is_relative_to(root):
                raise ToolError(3, 'Feature link leaves notebook: ' + relative)
            linked = destination.relative_to(root).as_posix()
            if linked not in desired:
                inspect(linked, True)
    binding = dict(root=str(root), version=__version__, head=head, host=host, source=source, language=language,
                   inputs={p: None if v is None else [hashlib.sha256(v[0]).hexdigest(), v[1]] for p, v in sorted(inputs.items())},
                   parents=parents, resources=resources,
                   outputs={p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(desired.items())})
    preview = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    changes = [p for p, raw in desired.items() if inputs[p] is None or inputs[p][0] != raw]
    result = dict(ready=not changes, already_current=not changes, applied=False, written_paths=[],
                  changes=changes, preview_id=preview, reviewed_head=head, novel_path=str(root),
                  host=host, skill_source=source, language=language, target_version=__version__,
                  next_action='Review additions and existing writer instructions, then apply this exact preview/HEAD. Plugin books require the matching plugin enabled first.')
    if not apply:
        return {'ok': True, 'data': result}
    if preview_id != preview or expected_head != head:
        raise ToolError(3, 'Side-character preview is stale; review a fresh preview')
    expected = dict(inputs)
    expected_parents = dict(parents)

    def recheck(skip=None):
        # Git probes are read-only; inspect inputs after probes to close their race.
        if git('rev-parse', '--verify', 'HEAD') != head:
            raise ToolError(3, 'Notebook HEAD changed during side-character maintenance')
        if (root / '.novel-creator').exists():
            raise ToolError(3, 'Notebook became a mixed/retained-legacy format')
        for relative, value in expected.items():
            if relative == skip:
                continue
            inspect(relative)
            if inputs[relative] != value:
                raise ToolError(3, 'Inspected notebook bytes/absence/identity changed: ' + relative)
        for relative, identity in expected_parents.items():
            path = _safe(root / relative)
            current = _identity(path.stat()) if path.exists() else None
            if current != identity:
                raise ToolError(3, 'Notebook parent identity changed: ' + relative)
        for name, value in resources.items():
            path = _safe(Path(name))
            if [hashlib.sha256(path.read_bytes()).hexdigest(), _identity(path.stat())] != value:
                raise ToolError(3, 'Installed package resource changed during maintenance')

    written, attempted = [], None
    try:
        for relative in changes:
            recheck()
            path = root / relative
            # Create absent parents exclusively in order and incorporate only
            # our own new identities into subsequent rechecks.
            for parent in reversed(path.parent.parents):
                if parent.is_relative_to(root) and not parent.exists():
                    _safe(parent).mkdir()
                    expected_parents[parent.relative_to(root).as_posix()] = _identity(parent.stat())
            if not path.parent.exists():
                _safe(path.parent).mkdir()
                expected_parents[path.parent.relative_to(root).as_posix()] = _identity(path.parent.stat())
            attempted = relative
            _write(path, desired[relative], expected[relative],
                   lambda skip=False: recheck(relative if skip else None))
            inspect(relative, True)
            if inputs[relative][0] != desired[relative]:
                raise ToolError(3, 'Written side-character resource changed unexpectedly')
            expected[relative] = inputs[relative]
            written.append(relative)
            attempted = None
        recheck()
    except (OSError, ToolError) as error:
        raise ToolError(5, 'Side-character maintenance is partial; inspect completed/attempted files and review a fresh preview to resume',
                        data=dict(ready=False, partial=True, written_paths=written,
                                  attempted_path=attempted, novel_path=str(root))) from error
    result.update(ready=True, applied=bool(changes), written_paths=written,
                  next_action='Review uncommitted additions, then reread/reload root instructions, actual skills and workflow in the host. No story save, staging or commit was made.')
    return {'ok': True, 'data': result}
