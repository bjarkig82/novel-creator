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

from novel_creator.notebook import initialize
from tests.notebook_contract_helpers import validate_notebook


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

    def older_notebook(self, language):
        root = self.area / language
        initialize(root, language=language)
        if language == 'is':
            project = root / 'notebook/project.md'
            project.write_bytes(project.read_bytes().replace(b'```', b'~~~'))
        for relative in self.resources:
            (root / relative).unlink()
        agents = root / 'AGENTS.md'
        old = agents.read_text(encoding='utf-8').replace(self.section, '')
        agents.write_text(old + '\n## Writer custom guidance\n\n'
                          'Use restrained language. Preserve my spelling: Elín.\n', encoding='utf-8')
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
        for language in ('en', 'is'):
            with self.subTest(language=language):
                root = self.older_notebook(language)
                before = self.snapshot(root)
                index = self.git(root, 'ls-files', '--stage', '-z')
                head = self.git(root, 'rev-parse', 'HEAD')
                self.run_procedure(root)
                after = self.snapshot(root)
                self.assertEqual(set(after) - set(before), set(self.resources))
                self.assertEqual({p for p in before if before[p] != after[p]}, {'AGENTS.md'})
                self.assertTrue(after['AGENTS.md'].startswith(before['AGENTS.md']))
                self.assertEqual(after['AGENTS.md'].decode().count(self.section), 1)
                for relative, raw in self.resources.items():
                    self.assertEqual(after[relative], raw)
                    path = root / relative
                    for link in re.findall(r'\]\(([^)]+)\)', raw.decode()):
                        self.assertTrue((path.parent / link).is_file(), link)
                self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)
                self.assertEqual(self.git(root, 'rev-parse', 'HEAD'), head)
                self.run_procedure(root)
                self.assertEqual(self.snapshot(root), after)
                self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)

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

    def test_crlf_divergent_root_section_stops_before_any_writes(self):
        root = self.older_notebook('en')
        agents = root / 'AGENTS.md'
        guidance = agents.read_bytes() + (
            b'\n## Character development\n\nCustom rule: save suggestions automatically.\n')
        agents.write_bytes(guidance.replace(b'\n', b'\r\n'))
        before = self.snapshot(root)
        index = self.git(root, 'ls-files', '--stage', '-z')
        result = self.run_procedure(root, success=False)
        self.assertIn('Divergent root feature section', result.stderr)
        self.assertEqual(self.snapshot(root), before)
        self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)

    def test_crlf_identical_root_section_reinstallation_preserves_exact_bytes(self):
        root = self.older_notebook('en')
        agents = root / 'AGENTS.md'
        guidance = agents.read_bytes() + b'\n' + self.section.encode('utf-8')
        agents.write_bytes(guidance.replace(b'\n', b'\r\n'))
        for relative, raw in self.resources.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        before = self.snapshot(root)
        index = self.git(root, 'ls-files', '--stage', '-z')
        self.run_procedure(root)
        self.assertEqual(self.snapshot(root), before)
        self.assertEqual(self.git(root, 'ls-files', '--stage', '-z'), index)


if __name__ == '__main__':
    unittest.main()
