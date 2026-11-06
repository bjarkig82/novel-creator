"""Focused artifact and installed-resource checks for the setup-only notebook."""
import re
import subprocess
import tomllib


AGENT_NAMES = ('novel_orchestrator', 'novel_brainstormer', 'novel_researcher',
               'novel_scene_writer', 'novel_chapter_writer', 'novel_reviewer')
SKILL_NAMES = ('novel-outline', 'novel-book-idea', 'novel-premise', 'novel-character',
               'novel-plot', 'novel-setting', 'novel-agent', 'novel-research',
               'novel-scene', 'novel-chapter', 'novel-review')
WORKFLOW_NAMES = ('conversation', 'format', 'outline', 'brainstorming',
                  'agents', 'manuscript', 'research', 'review')


def resource_paths(checkout):
    """Map initialized paths to source paths and wheel member names."""
    codex = 'novel_creator/codex/notebook/'
    shared = 'novel_creator/notebook_resources/workflows/'
    paths = {'AGENTS.md': (checkout / 'adapters/codex/notebook/AGENTS.md', codex + 'AGENTS.md')}
    for name in AGENT_NAMES:
        relative = f'agents/{name}.toml'
        paths['.codex/' + relative] = (checkout / 'adapters/codex/notebook' / relative, codex + relative)
    for name in SKILL_NAMES:
        relative = f'skills/{name}/SKILL.md'
        paths['.agents/' + relative] = (checkout / 'adapters/codex/notebook' / relative, codex + relative)
    for name in WORKFLOW_NAMES:
        relative = name + '.md'
        paths['.novel-notebook/workflows/' + relative] = (checkout / 'notebook/workflows' / relative, shared + relative)
    return paths


def verify_writing_resources(root, expected):
    """Check real initialized bytes, tracked files, parsed agents and local links."""
    definitions = sorted((root / '.codex/agents').glob('*.toml'))
    assert {path.stem for path in definitions} == set(AGENT_NAMES), definitions
    assert {path.relative_to(root).as_posix() for path in (root / '.codex').rglob('*')
            if path.is_file()} == {f'.codex/agents/{name}.toml' for name in AGENT_NAMES}
    tracked = set(subprocess.check_output(['git', '-C', str(root), 'ls-files'], text=True).splitlines())
    names = set()
    guidance = []
    for path in definitions:
        definition = tomllib.loads(path.read_text(encoding='utf-8'))
        assert set(definition) == {'name', 'description', 'developer_instructions'}, path
        assert all(isinstance(value, str) and value.strip() for value in definition.values()), path
        assert definition['name'] == path.stem, path
        names.add(definition['name'])
        guidance.append((path, definition['developer_instructions']))
    assert names == set(AGENT_NAMES)
    for relative, raw in expected.items():
        path = root / relative
        assert path.read_bytes() == raw.replace(b'\r\n', b'\n'), relative
        assert relative in tracked, relative
        if path.suffix == '.md':
            guidance.append((path, path.read_text(encoding='utf-8')))
    for path, content in guidance:
        links = re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', content)
        if path.suffix == '.toml' or path.name == 'SKILL.md':
            assert links, path
        for link in links:
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                continue
            destination = (path.parent / link).resolve()
            assert destination.is_relative_to(root.resolve()), (path, link)
            assert destination.is_file(), (path, link)
    for directory in ('manuscript', 'research', 'reviews'):
        assert not (root / directory).exists(), directory
    return len(expected)
