"""Explicit, preview-bound notebook installation of issue retrospective resources."""
import hashlib
from importlib.resources import files
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

from .cli import ToolError
from .retro_issue_provenance import KNOWN, SESSION_BLOCKS

START = '<!-- novel-creator:issue-retro:start -->'
END = '<!-- novel-creator:issue-retro:end -->'
ROUTING = START + '''
## Optional session retrospective

For `$novel-retro` or an explicit session retrospective, follow the
[retrospective workflow](.novel-notebook/workflows/retrospective.md).
Automatic retro is off; an explicit opt-in applies only to this active writing
session and runs only at explicit session closure, after any authorized pending
normal save. Never save an unsaved draft to enable retro. Stop known current
debugging before review and keep it off. No story exchange, story file, commit,
code fix or PR is created for retro administration. Publication and attachments
require current approval of the entire actual outgoing material to the fixed
repository bjarkig82/novel-creator. Saved records never enable participation.
''' + END + '\n'
OLD_ROOT = '''For an explicitly requested local notebook retrospective, follow the read-only
[notebook retrospective guidance](.novel-notebook/workflows/debugging.md#local-notebook-retrospective)
on a debug archive or other public evidence the writer supplies or explicitly
selects. Keep the review in chat; it enables no capture, story writes, commits,
uploads or publication and adds no retrospective CLI.
'''


def setup(args):
    """Return a read-only preview or apply its exact inspected resource changes."""
    apply = bool(args.apply)
    if apply != bool(args.preview and args.expected_head) or (not apply and (args.preview or args.expected_head)):
        raise ToolError(2, 'Setup apply requires --apply, --preview and --expected-head together')
    root = Path(args.novel).absolute()
    inputs = {}

    def safe(path):
        if '..' in path.parts or path.resolve() != path:
            raise ToolError(3, 'Issue setup refuses redirected paths and parent segments')
        for part in (*reversed(path.parents), path):
            try:
                info = part.lstat()
            except FileNotFoundError:
                continue
            if (stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
                    or not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode))):
                raise ToolError(3, 'Issue setup refuses redirected or special paths')
            if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
                raise ToolError(3, 'Issue setup refuses hard-linked files')
        return path

    def inspect(relative, required=False):
        path = safe(root / relative)
        if not path.exists():
            if required:
                raise ToolError(3, 'Required notebook resource is missing: ' + relative)
            value = None
        else:
            if not path.is_file():
                raise ToolError(3, 'Notebook resource must be a regular file: ' + relative)
            info = path.stat()
            value = (path.read_bytes(), (info.st_dev, info.st_ino))
        inputs[relative] = value
        return None if value is None else value[0]

    safe(root)
    safe(root / '.git')
    if not root.is_dir() or not (root / '.git').is_dir():
        raise ToolError(3, 'Issue setup requires an independent format-1 notebook Git root; legacy novels use framework update')
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')

    def git(*argv):
        result = subprocess.run(['git', '-c', 'core.fsmonitor=false', '-C', str(root), *argv], env=env, capture_output=True)
        if result.returncode:
            raise ToolError(3, 'Cannot inspect notebook Git identity')
        return result.stdout.decode('utf-8').strip()

    if (Path(git('rev-parse', '--show-toplevel')).resolve() != root
            or Path(git('rev-parse', '--absolute-git-dir')).resolve() != root / '.git'
            or Path(git('rev-parse', '--path-format=absolute', '--git-common-dir')).resolve() != root / '.git'):
        raise ToolError(3, 'Notebook Git routing must be independent and local')
    head = git('rev-parse', '--verify', 'HEAD')
    if not safe(root / 'notebook/project.md').is_file():
        raise ToolError(3, 'Issue setup requires a format-1 notebook; legacy novels use the normal framework update')
    project = inspect('notebook/project.md', True)
    try:
        match = re.match(rb'\A(```|~~~)json\r?\n(.*?)\r?\n\1(?:\r?\n|\Z)', project, re.S)
        metadata = json.loads(match[2])
        if (metadata.get('format'), metadata.get('version'), metadata.get('kind'), metadata.get('id')) != ('novel-notebook', 1, 'project', 'project') or type(metadata.get('version')) is not int or metadata.get('language') not in ('en', 'is'):
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ToolError(3, 'Issue setup requires valid supported format-1 notebook metadata') from None
    inspect('notebook/working-summary.md', True)
    inspect('.novel-notebook/languages/' + metadata['language'] + '.md', True)
    try:
        from .notebook import _host_text
    except ModuleNotFoundError as error:
        if error.name != __package__ + '.notebook':
            raise
        raise ToolError(3, 'Notebook issue setup requires an external current runtime; pinned legacy runtime cannot install notebook resources') from error
    marker = inspect('.novel-notebook/integration.json')
    host, source = 'codex', 'project'
    if marker is not None:
        try:
            integration = json.loads(marker)
            host, source = integration['host'], integration['skill_source']
            if type(integration.get('version')) is not int or integration.get('version') != 1 or host not in ('codex', 'claude', 'both') or source not in ('project', 'plugin'):
                raise ValueError()
        except (ValueError, KeyError, TypeError):
            raise ToolError(3, 'Unrecognized notebook integration marker') from None
    desired = {}
    workflows = files('novel_creator.notebook_resources').joinpath('workflows')
    for name in ('retrospective', 'debugging', 'help', 'conversation'):
        relative = '.novel-notebook/workflows/' + name + '.md'
        raw = _host_text(workflows.joinpath(name + '.md').read_text(encoding='utf-8'), host, source).encode()
        original = inspect(relative)
        if original is not None and original.replace(b'\r\n', b'\n') != raw and hashlib.sha256(original.replace(b'\r\n', b'\n')).hexdigest() not in KNOWN.get(name + '.md', ()):
            raise ToolError(3, 'Customized notebook resource would be overwritten: ' + relative)
        desired[relative] = raw
    # Older supported notebooks may predate these linked writing guides.
    # Add missing trusted snapshots; existing custom prerequisite bytes stay put.
    for name in ('agents', 'format', 'outline', 'brainstorming', 'manuscript',
                 'research', 'review', 'clarify', 'analyze', 'character-development'):
        relative = '.novel-notebook/workflows/' + name + '.md'
        if inspect(relative) is None:
            desired[relative] = _host_text(workflows.joinpath(name + '.md').read_text(encoding='utf-8'), host, source).encode()
    for selected in (('codex', 'claude') if host == 'both' else (host,)):
        relative = 'AGENTS.md' if selected == 'codex' else 'CLAUDE.md'
        original = inspect(relative, True)
        try:
            text = original.decode('utf-8')
        except UnicodeError:
            raise ToolError(3, 'Notebook instructions must be UTF-8') from None
        session_start = '<!-- novel-creator:session-guidance:start -->'
        session_end = '<!-- novel-creator:session-guidance:end -->'
        if session_start in text or session_end in text:
            if text.count(session_start) != 1 or text.count(session_end) != 1:
                raise ToolError(3, 'Customized conflicting session routing block')
            block = text[text.index(session_start):text.index(session_end) + len(session_end)]
            normalized_block = block.replace('\r\n', '\n')
            if normalized_block not in SESSION_BLOCKS:
                raise ToolError(3, 'Customized conflicting session routing block')
            if normalized_block == SESSION_BLOCKS[0]:
                actual = block.encode()
                replacement = SESSION_BLOCKS[1].replace('\n', '\r\n') if '\r\n' in block else SESSION_BLOCKS[1]
                original = original.replace(actual, replacement.encode(), 1)
                text = original.decode('utf-8')
        route = _host_text(ROUTING, selected, source)
        if START in text or END in text:
            if text.count(START) != 1 or text.count(END) != 1:
                raise ToolError(3, 'Customized conflicting retrospective routing block')
            block = text[text.index(START):text.index(END) + len(END)]
            if block.replace('\r\n', '\n') != route.rstrip('\n'):
                raise ToolError(3, 'Customized conflicting retrospective routing block')
            new = original
        else:
            # Remove only the exact shipped obsolete paragraph; preserve all other bytes.
            old = OLD_ROOT.encode()
            normalized = original.replace(b'\r\n', b'\n')
            if old in normalized:
                old_actual = old.replace(b'\n', b'\r\n') if old.replace(b'\n', b'\r\n') in original else old
                original_without_old = original.replace(old_actual, b'', 1)
            else:
                if re.search(r'(?im)^.*(?:retrospective|retro issue|novel-retro).*$', text):
                    raise ToolError(3, 'Unrecognized conflicting retrospective instruction; preserve and review custom guidance')
                original_without_old = original
            new = original_without_old + (b'\n' if original_without_old.endswith(b'\n') else b'\n\n') + route.encode()
        desired[relative] = new
        if source == 'project':
            relative = ('.agents' if selected == 'codex' else '.claude') + '/skills/novel-retro/SKILL.md'
            raw = files('novel_creator.codex').joinpath('notebook/skills/novel-retro/SKILL.md').read_text(encoding='utf-8')
            raw = _host_text(raw, selected, source).encode()
            original_skill = inspect(relative)
            if original_skill is not None and original_skill.replace(b'\r\n', b'\n') != raw:
                raise ToolError(3, 'Customized notebook retro skill would be overwritten')
            desired[relative] = raw
    ignore = inspect('.gitignore') or b''
    if not ignore.splitlines() or ignore.splitlines()[-1] != b'.novel-notebook/local/':
        desired['.gitignore'] = ignore + (b'\n' if ignore and not ignore.endswith(b'\n') else b'') + b'.novel-notebook/local/\n'
    # Bind every local link target inspected by the desired resources as well.
    for relative, raw in list(desired.items()):
        if not relative.endswith('.md'):
            continue
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', raw.decode('utf-8')):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                continue
            destination = Path(os.path.abspath((root / relative).parent.joinpath(link)))
            if not destination.is_relative_to(root):
                raise ToolError(3, 'Resource link leaves notebook: ' + relative)
            linked = destination.relative_to(root).as_posix()
            if linked not in desired:
                inspect(linked, True)
    root_info = root.stat()
    git_info = (root / '.git').stat()
    binding = dict(root=str(root), root_identity=(root_info.st_dev, root_info.st_ino), git_identity=(git_info.st_dev, git_info.st_ino), head=head,
                   inputs={p: None if value is None else [hashlib.sha256(value[0]).hexdigest(), value[1]] for p, value in sorted(inputs.items())},
                   outputs={p: hashlib.sha256(raw).hexdigest() for p, raw in sorted(desired.items())})
    preview = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    changes = [p for p, raw in desired.items() if inputs[p] is None or inputs[p][0] != raw]
    result = dict(ready=not changes, applied=False, preview_id=preview, reviewed_head=head, changes=changes,
                  host=host, skill_source=source, novel_path=str(root), already_current=not changes,
                  next_action='Review this preview, then explicitly apply with its ID and HEAD. No story files, staging or commits are changed.')
    if not apply:
        return result
    if args.preview != preview or args.expected_head != head:
        raise ToolError(3, 'Issue setup preview is stale; take a fresh preview')
    written = []
    def unchanged(relative, expected):
        current = inspect(relative)
        if inputs[relative] != expected:
            raise ToolError(3, 'Notebook input bytes or identity changed: ' + relative)
        return current
    inspected = dict(inputs)
    try:
        for relative in changes:
            for name, expected in inspected.items():
                unchanged(name, expected)
            if git('rev-parse', '--verify', 'HEAD') != head or root.stat().st_ino != root_info.st_ino or (root / '.git').stat().st_ino != git_info.st_ino:
                raise ToolError(3, 'Notebook identity or HEAD changed during setup')
            path = safe(root / relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            safe(path)
            if inspected[relative] is None:
                with path.open('xb') as stream:
                    stream.write(desired[relative])
            else:
                fd, temporary = tempfile.mkstemp(prefix='.retro-setup-', dir=path.parent)
                temporary = Path(temporary)
                try:
                    with os.fdopen(fd, 'wb') as stream:
                        stream.write(desired[relative]); stream.flush(); os.fsync(stream.fileno())
                    unchanged(relative, inspected[relative])
                    temporary.chmod(stat.S_IMODE(path.stat().st_mode))
                    os.replace(temporary, path)
                finally:
                    temporary.unlink(missing_ok=True)
            if inspect(relative) != desired[relative]:
                raise ToolError(3, 'Written resource changed unexpectedly: ' + relative)
            inspected[relative] = inputs[relative]
            written.append(relative)
    except (OSError, ToolError) as error:
        raise ToolError(5, 'Issue setup is partial; preserve completed files and take a fresh preview to resume safely', data=dict(partial=True, written_paths=written)) from error
    for name, expected in inspected.items():
        unchanged(name, expected)
    if git('rev-parse', '--verify', 'HEAD') != head:
        raise ToolError(5, 'Issue setup is partial; HEAD changed, take a fresh preview', data=dict(partial=True, written_paths=written))
    result.update(ready=True, applied=True, next_action='Review uncommitted resources and actual skill links, then reread/reload project instructions and skills in the host. No novel save or commit was made.')
    return result
