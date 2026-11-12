"""Execute the documentation's one-off procedure, not a second installer."""
from importlib.resources import files
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from novel_creator.notebook import initialize, _host_text, _instructions
from tests.notebook_contract_helpers import validate_notebook
from tests.integration import test_path_redirection


class CharacterDevelopmentManualInstall(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='character-manual-')
        self.addCleanup(temporary.cleanup)
        self.area = Path(temporary.name).resolve()
        checkout = Path(__file__).resolve().parents[2]
        doc = (checkout / 'docs/character-development.md').read_text(encoding='utf-8')
        snippets = re.findall(r'```python\n(.*?)\n```', doc, re.S)
        self.assertEqual(len(snippets), 1, 'Run the actual documented manual procedure')
        self.procedure = snippets[0]
        shared = files('novel_creator.notebook_resources')
        codex = files('novel_creator.codex').joinpath('notebook')
        self.resources = {
            '.novel-notebook/workflows/character-development.md':
                shared.joinpath('workflows/character-development.md').read_bytes(),
            '.agents/skills/novel-character-develop/SKILL.md':
                codex.joinpath('skills/novel-character-develop/SKILL.md').read_bytes(),
        }
        supplied = codex.joinpath('AGENTS.md').read_text(encoding='utf-8')
        self.section = re.search(r'^## Character development\n.*?(?=^## |\Z)',
                                 supplied, re.M | re.S).group().rstrip() + '\n'
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_AUTHOR_NAME='Manual Test', GIT_AUTHOR_EMAIL='test@example.invalid',
                   GIT_COMMITTER_NAME='Manual Test', GIT_COMMITTER_EMAIL='test@example.invalid',
                   PYTHONDONTWRITEBYTECODE='1')
        environment = patch.dict(os.environ, env, clear=True)
        environment.start()
        self.addCleanup(environment.stop)

    def git(self, root, *arguments):
        return subprocess.check_output(['git', '-C', str(root), *arguments])

    def older_notebook(self, language, host='codex', source='project'):
        root = self.area / f'{language}-{host}-{source}'
        initialize(root, language=language, host=host, skill_source=source)
        hosts = ('codex', 'claude') if host == 'both' else (host,)
        codex = files('novel_creator.codex').joinpath('notebook')
        self.resources = {'.novel-notebook/workflows/character-development.md':
                          _host_text(files('novel_creator.notebook_resources').joinpath(
                              'workflows/character-development.md').read_text(encoding='utf-8'),
                              host, source).encode()}
        self.sections = {}
        for selected in hosts:
            name = 'AGENTS.md' if selected == 'codex' else 'CLAUDE.md'
            text = _instructions(codex, selected, source).decode()
            section = re.search(r'^## Character development\n.*?(?=^## |\Z)',
                                text, re.M | re.S).group().rstrip() + '\n'
            self.sections[name] = section
            if source == 'project':
                directory = '.agents' if selected == 'codex' else '.claude'
                self.resources[f'{directory}/skills/novel-character-develop/SKILL.md'] = (
                    _host_text(codex.joinpath('skills/novel-character-develop/SKILL.md').read_text(
                        encoding='utf-8'), selected, source).encode())
        if language == 'is':
            project = root / 'notebook/project.md'
            project.write_bytes(project.read_bytes().replace(b'```', b'~~~'))
        for relative in self.resources:
            (root / relative).unlink()
        for name, section in self.sections.items():
            instructions = root / name
            old = instructions.read_text(encoding='utf-8').replace(section, '')
            instructions.write_text(old + '\n## Writer custom guidance\n\n'
                                    'Use restrained language. Preserve my spelling: Elín.\n'
                                    '[Custom unrelated reference](outside-custom.md)\n', encoding='utf-8')
        topic = root / 'notebook/topics/elin.md'
        topic.parent.mkdir()
        topic.write_text('```json\n{"format":"novel-notebook","version":1,'
                         '"kind":"topic","id":"elin","category":"character"}\n```\n'
                         '# Elín\n\n## Items\n\n### Home\nItem-ID: elin-home\n'
                         'Type: statement\nState: accepted\nPerspective: objective\n'
                         'Origin: Writer established before installation.\nLinks: none\n\n'
                         'She lives near the harbour.\n',
                         encoding='utf-8')
        self.git(root, 'add', '--all')
        self.git(root, 'commit', '-qm', 'Older notebook fixture with custom guidance')
        topic.write_bytes(topic.read_bytes() + '\nWriter edit: Þóra is her sister.\n'.encode())
        self.git(root, 'add', '--', 'notebook/topics/elin.md')
        topic.write_bytes(topic.read_bytes() + b'Unstaged writer line.\n')
        summary = root / 'notebook/working-summary.md'
        summary.write_bytes(summary.read_bytes() + b'\nUnstaged navigation edit.\n')
        self.assertEqual(len(validate_notebook(root / 'notebook')), 3)
        return root

    def snapshot(self, root):
        return {p.relative_to(root).as_posix(): p.read_bytes()
                for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}

    def run_procedure(self, root, success=True):
        result = subprocess.run([sys.executable, '-I', '-c', self.procedure], cwd=root,
                                capture_output=True, text=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_documented_install_and_identical_retry_preserve_story_and_index(self):
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                for language in ('en', 'is'):
                    with self.subTest(host=host, source=source, language=language):
                        root = self.older_notebook(language, host, source)
                        before = self.snapshot(root)
                        index = self.git(root, 'ls-files', '--stage', '-z')
                        head = self.git(root, 'rev-parse', 'HEAD')
                        self.run_procedure(root)
                        after = self.snapshot(root)
                        self.assertEqual(set(after) - set(before), set(self.resources))
                        self.assertEqual({p for p in before if before[p] != after[p]}, set(self.sections))
                        for name, section in self.sections.items():
                            self.assertTrue(after[name].startswith(before[name]))
                            self.assertEqual(after[name].decode().count(section), 1)
                        for relative, raw in self.resources.items():
                            self.assertEqual(after[relative], raw)
                        self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)
                        self.assertEqual(self.git(root, 'rev-parse', 'HEAD'), head)
                        self.run_procedure(root)
                        self.assertEqual(self.snapshot(root), after)
                        self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)
                        if source == 'plugin':
                            self.assertFalse((root / '.agents/skills').exists())
                            self.assertFalse((root / '.claude/skills').exists())

    def test_divergent_destinations_stop_before_any_writes(self):
        for number, relative in enumerate((*self.resources, 'AGENTS.md')):
            with self.subTest(destination=relative):
                root = self.older_notebook('en')
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if relative == 'AGENTS.md':
                    destination.write_bytes(destination.read_bytes() +
                                            b'\n## Character development\n\nCustom older version.\n')
                else:
                    destination.write_bytes(b'Writer-owned divergent guidance.\n')
                before = self.snapshot(root)
                index = self.git(root, 'ls-files', '--stage', '-z')
                result = self.run_procedure(root, success=False)
                self.assertIn('Divergent', result.stderr)
                self.assertEqual(self.snapshot(root), before)
                self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)
                # Give the next case a distinct disposable destination.
                root.rename(self.area / f'checked-{number}')

    def test_missing_prerequisites_and_unsupported_format_leave_bytes_intact(self):
        cases = ('conversation.md', 'format.md', 'agents.md', 'brainstorming.md',
                 'language', 'format-version')
        for number, missing in enumerate(cases):
            with self.subTest(case=missing):
                root = self.older_notebook('is')
                if missing == 'format-version':
                    project = root / 'notebook/project.md'
                    project.write_bytes(project.read_bytes().replace(b'"version": 1', b'"version": 2'))
                elif missing == 'language':
                    (root / '.novel-notebook/languages/is.md').unlink()
                else:
                    (root / '.novel-notebook/workflows' / missing).unlink()
                before = self.snapshot(root)
                self.run_procedure(root, success=False)
                self.assertEqual(self.snapshot(root), before)
                root.rename(self.area / f'missing-{number}')

    def test_both_crlf_roots_identical_or_divergent_preflight(self):
        for conflict in (None, 'AGENTS.md', 'CLAUDE.md'):
            with self.subTest(conflict=conflict):
                root = self.older_notebook('en', 'both')
                for name, section in self.sections.items():
                    raw = (root / name).read_bytes() + b'\n' + section.encode()
                    if name == conflict:
                        raw += b'Writer divergent addition.\n'
                    (root / name).write_bytes(raw.replace(b'\n', b'\r\n'))
                if conflict is None:
                    for relative, raw in self.resources.items():
                        path = root / relative
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(raw.replace(b'\n', b'\r\n'))
                before = self.snapshot(root)
                index = self.git(root, 'ls-files', '--stage', '-z')
                self.run_procedure(root, success=conflict is None)
                self.assertEqual(self.snapshot(root), before)
                self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)
                root.rename(self.area / f'crlf-{conflict}')

    def test_invalid_and_unreadable_markers_stop_before_writes(self):
        markers = (b'{', b'[]', b'{"version":true,"host":"both","skill_source":"plugin"}',
                   b'{"version":2,"host":"both","skill_source":"plugin"}',
                   b'{"version":1,"host":"other","skill_source":"plugin"}',
                   b'{"version":1,"host":"codex","skill_source":"other"}', None)
        for number, marker in enumerate(markers):
            with self.subTest(marker=marker):
                root = self.older_notebook('en', 'both', 'plugin')
                path = root / '.novel-notebook/integration.json'
                if marker is None:
                    path.chmod(0)
                    if path.stat().st_mode & 0o444:
                        # Windows chmod does not remove read permission.
                        path.chmod(0o644)
                        root.rename(self.area / f'marker-{number}')
                        continue
                else:
                    path.write_bytes(marker)
                before = self.snapshot(root) if marker is not None else None
                try:
                    self.run_procedure(root, success=False)
                finally:
                    if marker is None:
                        path.chmod(0o644)
                if marker is None:
                    self.assertFalse((root / '.novel-notebook/workflows/character-development.md').exists())
                else:
                    self.assertEqual(self.snapshot(root), before)
                root.rename(self.area / f'marker-{number}')

    def test_partial_install_retry_preserves_completed_resources(self):
        root = self.older_notebook('is', 'both', 'project')
        workflow = '.novel-notebook/workflows/character-development.md'
        (root / workflow).write_bytes(self.resources[workflow].replace(b'\n', b'\r\n'))
        root_name = 'AGENTS.md'
        path = root / root_name
        path.write_bytes(path.read_bytes() + b'\n' + self.sections[root_name].encode())
        before_workflow, before_root = (root / workflow).read_bytes(), path.read_bytes()
        index = self.git(root, 'ls-files', '--stage', '-z')
        self.run_procedure(root)
        self.assertEqual((root / workflow).read_bytes(), before_workflow)
        self.assertEqual(path.read_bytes(), before_root)
        self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)
        after = self.snapshot(root)
        self.run_procedure(root)
        self.assertEqual(self.snapshot(root), after)

    def test_marker_read_denial_preserves_all_files(self):
        root = self.older_notebook('en', 'both', 'plugin')
        prefix = ("from pathlib import Path\n"
                  "read_original = Path.read_bytes\n"
                  "def denied(path):\n"
                  "    if path.name == 'integration.json': raise PermissionError('marker denied')\n"
                  "    return read_original(path)\n"
                  "Path.read_bytes = denied\n")
        before = self.snapshot(root)
        result = subprocess.run([sys.executable, '-I', '-c', prefix + self.procedure],
                                cwd=root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('marker denied', result.stderr)
        self.assertEqual(self.snapshot(root), before)

    @unittest.skipUnless(os.name == 'nt', 'Windows junction guard')
    def test_windows_junction_preflight(self):
        root = self.older_notebook('en', 'both')
        parent = root / '.claude/skills/novel-character-develop'
        parent.rmdir()
        for outside in (self.area / 'junction-target', root / 'writer-owned-dir'):
            outside.mkdir()
            test_path_redirection.PathRedirectionTests.junction(parent, outside)
            try:
                before = self.snapshot(root)
                self.run_procedure(root, success=False)
                self.assertEqual(self.snapshot(root), before)
                self.assertEqual(list(outside.iterdir()), [])
            finally:
                os.rmdir(parent)

    def test_missing_second_root_and_redirected_destination_preflight(self):
        for case in ('missing-root', 'hardlink', 'symlink', 'parent-file'):
            with self.subTest(case=case):
                root = self.older_notebook('en', 'both')
                if case == 'missing-root':
                    (root / 'CLAUDE.md').unlink()
                elif case == 'parent-file':
                    parent = root / '.claude/skills/novel-character-develop'
                    parent.rmdir()
                    parent.write_bytes(b'Writer file')
                else:
                    target = self.area / ('outside-' + case)
                    target.write_bytes(b'Outside writer bytes')
                    destination = root / '.novel-notebook/workflows/character-development.md'
                    if case == 'hardlink':
                        os.link(target, destination)
                    else:
                        try:
                            destination.symlink_to(target)
                        except OSError:
                            root.rename(self.area / f'preflight-{case}')
                            continue  # Windows may not permit unprivileged symlinks.
                before = self.snapshot(root)
                self.run_procedure(root, success=False)
                self.assertEqual(self.snapshot(root), before)
                root.rename(self.area / f'preflight-{case}')


if __name__ == '__main__':
    unittest.main()
