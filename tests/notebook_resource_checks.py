"""Focused artifact and installed-resource checks for the setup-only notebook."""
import re
import subprocess
import tomllib


AGENT_NAMES = ('novel_orchestrator', 'novel_brainstormer', 'novel_researcher',
               'novel_scene_writer', 'novel_chapter_writer', 'novel_reviewer')
SKILL_NAMES = ('novel-outline', 'novel-book-idea', 'novel-premise', 'novel-character',
               'novel-plot', 'novel-setting', 'novel-agent', 'novel-research',
               'novel-scene', 'novel-chapter', 'novel-review', 'novel-clarify',
               'novel-analyze', 'novel-help')
WORKFLOW_NAMES = ('conversation', 'format', 'outline', 'brainstorming',
                  'agents', 'manuscript', 'research', 'review', 'clarify', 'analyze',
                  'help')

# Frozen published layout: future notebook additions must not become requirements
# when verifying the already approved public 0.5.0 artifact.
PUBLIC_050_AGENT_NAMES = ('novel_orchestrator', 'novel_brainstormer', 'novel_researcher',
                         'novel_scene_writer', 'novel_chapter_writer', 'novel_reviewer')
PUBLIC_050_SKILL_NAMES = ('novel-outline', 'novel-book-idea', 'novel-premise', 'novel-character',
                         'novel-plot', 'novel-setting', 'novel-agent', 'novel-research',
                         'novel-scene', 'novel-chapter', 'novel-review')
PUBLIC_050_WORKFLOW_NAMES = ('conversation', 'format', 'outline', 'brainstorming',
                            'agents', 'manuscript', 'research', 'review')


def resource_paths(checkout, *, public_version=None):
    """Map current or explicitly supported published notebook resource paths."""
    if public_version is None:
        agents, skills, workflows = AGENT_NAMES, SKILL_NAMES, WORKFLOW_NAMES
    elif public_version == '0.5.0':
        agents, skills, workflows = (PUBLIC_050_AGENT_NAMES, PUBLIC_050_SKILL_NAMES,
                                    PUBLIC_050_WORKFLOW_NAMES)
    else:
        raise ValueError('Unsupported published notebook layout: ' + public_version)
    codex = 'novel_creator/codex/notebook/'
    shared = 'novel_creator/notebook_resources/workflows/'
    paths = {'AGENTS.md': (checkout / 'adapters/codex/notebook/AGENTS.md', codex + 'AGENTS.md')}
    for name in agents:
        relative = f'agents/{name}.toml'
        paths['.codex/' + relative] = (checkout / 'adapters/codex/notebook' / relative, codex + relative)
    for name in skills:
        relative = f'skills/{name}/SKILL.md'
        paths['.agents/' + relative] = (checkout / 'adapters/codex/notebook' / relative, codex + relative)
    for name in workflows:
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
        if path.name == 'SKILL.md':
            metadata = re.match(r'---\nname: ([a-z][a-z0-9-]*)\ndescription: (.+)\n---\n',
                                path.read_text(encoding='utf-8'))
            assert metadata and metadata[1] == path.parent.name, path
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
