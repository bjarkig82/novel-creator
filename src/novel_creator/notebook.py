"""One-time creation of a new story notebook. No conversation or save runtime."""
import json
import os
from pathlib import Path
import re
import subprocess
from importlib.resources import files

from .cli import ToolError


def initialize(target, *, title=None, language='en'):
    """Create only a nonexistent destination; preserve all partial failures."""
    root = Path(target).absolute()
    title = root.name if title is None else title
    if language not in ('en', 'is') or not isinstance(title, str) or not title.strip():
        raise ToolError(2, 'Notebook requires a nonempty title and language en or is')
    if '..' in root.parts or root.resolve() != root or any(p.is_symlink() for p in (root, *root.parents)):
        raise ToolError(2, 'Notebook destination must not traverse symlinks or parent segments')
    if root.exists():
        raise ToolError(3, 'Notebook setup requires a new destination; existing novels are not converted')
    if not root.parent.is_dir():
        raise ToolError(2, 'Notebook destination needs an existing parent directory')

    env = os.environ.copy()
    # Never let inherited repository redirects send writes to another checkout.
    for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR',
                 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES',
                 'GIT_CEILING_DIRECTORIES'):
        env.pop(name, None)
    # Safety discovery must include repositories above inherited search boundaries.
    env['GIT_DISCOVERY_ACROSS_FILESYSTEM'] = '1'

    def git(at, *args, check=True):
        result = subprocess.run(['git', '-C', str(at), *args], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and result.returncode:
            raise ToolError(5, 'Local notebook Git operation failed; preserve files and inspect Git configuration')
        return result

    version = git(root.parent, '--version').stdout.decode('utf-8', errors='replace')
    match = re.search(r'(\d+)\.(\d+)', version)
    if not match or tuple(map(int, match.groups())) < (2, 39):
        raise ToolError(4, 'Notebook setup requires Git >=2.39')
    if git(root.parent, 'rev-parse', '--absolute-git-dir', check=False).returncode == 0:
        raise ToolError(3, 'Notebook must be outside the framework and every other Git repository')
    for identity in ('GIT_AUTHOR_IDENT', 'GIT_COMMITTER_IDENT'):
        if git(root.parent, 'var', identity, check=False).returncode:
            raise ToolError(5, 'Git identity is unavailable; configure your intended author/committer before setup')

    # Read and render the entire small resource set before creating anything.
    shared = files('novel_creator.notebook_resources')
    codex = files('novel_creator.codex').joinpath('notebook', 'AGENTS.md')
    planned = {'AGENTS.md': codex.read_bytes(),
               '.gitignore': b'.env\n.env.*\n*.key\n*.pem\n',
               '.gitattributes': b'*.md text eol=lf\n'}
    for name in ('conversation.md', 'format.md'):
        planned['.novel-notebook/workflows/' + name] = shared.joinpath('workflows', name).read_bytes()
    planned['.novel-notebook/languages/' + language + '.md'] = shared.joinpath('languages', language + '.md').read_bytes()
    for kind, filename, identifier in (('project', 'project.md', 'project'),
                                       ('summary', 'working-summary.md', 'working-summary')):
        metadata = dict(format='novel-notebook', version=1, kind=kind, id=identifier)
        if kind == 'project':
            metadata['language'] = language
        resource = filename if language == 'en' else filename.replace('.md', '.is.md')
        template = shared.joinpath('templates', resource).read_text(encoding='utf-8')
        planned['notebook/' + filename] = template.replace(
            '{{metadata}}', json.dumps(metadata, ensure_ascii=False)).replace('{{title}}', title).encode('utf-8')

    try:
        root.mkdir()  # Exclusive claim: never adopt a concurrent creator's folder.
    except FileExistsError as error:
        raise ToolError(3, 'Another creator occupied the notebook destination; existing files preserved') from error
    try:
        for relative, raw in planned.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(raw.replace(b'\r\n', b'\n'))
        git(root, 'init', '-b', 'main')
        git(root, 'add', '--', *planned)
        git(root, 'commit', '-m', 'Create story notebook', '--', *planned)
    except (OSError, ToolError) as error:
        raise ToolError(5, 'Notebook setup is partial; files were preserved. Inspect them or choose a new destination; do not overwrite this folder',
                        data={'ready': False, 'partial': True, 'novel_path': str(root)}) from error
    return {'ok': True, 'data': {'ready': True, 'format': 'novel-notebook', 'version': 1,
                                 'novel_path': str(root), 'language': language,
                                 'next_action': 'Open this folder in Codex and start talking about your novel. Ask for a topic brief whenever useful.'}}
