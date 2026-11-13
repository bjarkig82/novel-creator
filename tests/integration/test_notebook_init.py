"""Real disposable filesystem/Git setup; no author settings escape the test."""
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from novel_creator.cli import ToolError
from tests.notebook_resource_checks import resource_paths, verify_writing_resources


class NotebookInitialization(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='notebook-test-')
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name).resolve()
        self.target = self.parent / 'Bréf Þóru'
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_AUTHOR_NAME='Notebook Test', GIT_AUTHOR_EMAIL='test@example.invalid',
                   GIT_COMMITTER_NAME='Notebook Test', GIT_COMMITTER_EMAIL='test@example.invalid')
        self.environment = patch.dict(os.environ, env, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.assertIsNotNone(importlib.util.find_spec('novel_creator.notebook'),
                             'The setup-only notebook initializer is not implemented')
        self.module = importlib.import_module('novel_creator.notebook')

    def initialize(self, **kwargs):
        return self.module.initialize(self.target, title='Bréf Þóru', **kwargs)

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob('*') if p.is_file()}

    def test_new_notebook_is_committed_readable_and_runtime_free(self):
        result = self.initialize(language='is')
        self.assertTrue(result['data']['ready'])
        self.assertEqual(result['data']['format'], 'novel-notebook')
        brief = (self.target / 'notebook/project.md').read_text(encoding='utf-8')
        self.assertIn('Bréf Þóru', brief)
        metadata = json.loads(brief.split('```json\n', 1)[1].split('```', 1)[0])
        self.assertEqual(metadata['language'], 'is')
        self.assertTrue((self.target / 'AGENTS.md').is_file())
        self.assertTrue((self.target / '.novel-notebook/languages/is.md').is_file())
        self.assertFalse((self.target / '.novel-notebook/languages/en.md').exists())
        self.assertFalse((self.target / '.novel-creator').exists())
        self.assertFalse((self.target / 'notebook/topics').exists())
        self.assertFalse(list(self.target.rglob('*.py')))
        status = subprocess.check_output(['git', '-C', str(self.target), 'status', '--porcelain'])
        self.assertEqual(status, b'')
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.target), 'log', '--format=%s']).strip(),
                         b'Create story notebook')

    def test_seed_content_uses_only_selected_language(self):
        for language in ('en', 'is'):
            with self.subTest(language=language):
                self.target = self.parent / language
                self.initialize(language=language)
                project = (self.target / 'notebook/project.md').read_text(encoding='utf-8')
                summary = (self.target / 'notebook/working-summary.md').read_text(encoding='utf-8')
                project_metadata = json.loads(project.split('```json\n', 1)[1].split('```', 1)[0])
                summary_metadata = json.loads(summary.split('```json\n', 1)[1].split('```', 1)[0])
                self.assertEqual(project_metadata, {'format': 'novel-notebook', 'version': 1,
                                                   'kind': 'project', 'id': 'project', 'language': language})
                self.assertEqual(summary_metadata, {'format': 'novel-notebook', 'version': 1,
                                                   'kind': 'summary', 'id': 'working-summary'})
                self.assertIn('# Bréf Þóru', project)
                if language == 'en':
                    self.assertIn('## Concept\n\nUnknown.', project)
                    self.assertIn('Guided conversation is the default', project)
                    self.assertIn('# Working summary\n', summary)
                    self.assertIn('Derived navigation, not canon. Do not display automatically', summary)
                    self.assertNotIn('Hugmynd', project)
                    self.assertNotIn('Vinnuyfirlit', summary)
                else:
                    self.assertIn('## Hugmynd\n\nÓþekkt.', project)
                    self.assertIn('Sjálfgefið er leiðbeinandi samtal', project)
                    self.assertIn('# Vinnuyfirlit\n', summary)
                    self.assertIn('Leiðarvísir, ekki sjálfstæðar sögustaðreyndir. Ekki birta sjálfkrafa', summary)
                    self.assertNotIn('Concept', project)
                    self.assertNotIn('Working summary', summary)

    def test_debug_guidance_is_installed_without_enabling_capture_and_logs_are_ignored(self):
        self.initialize()
        workflow = self.target / '.novel-notebook/workflows/debugging.md'
        self.assertTrue(workflow.is_file())
        self.assertIn('.novel-notebook/workflows/debugging.md',
                      (self.target / 'AGENTS.md').read_text(encoding='utf-8'))
        local = self.target / '.novel-notebook/local'
        self.assertFalse(local.exists(), 'Notebook initialization must not activate debugging')
        debug = local / 'debug'
        debug.mkdir(parents=True)
        (debug / 'events.jsonl').write_text('{"private":"writing"}\n', encoding='utf-8')
        self.assertEqual(subprocess.check_output(
            ['git', '-C', str(self.target), 'status', '--porcelain']), b'')
        ignored = subprocess.check_output(
            ['git', '-C', str(self.target), 'check-ignore', '--',
             '.novel-notebook/local/debug/events.jsonl'], text=True)
        self.assertIn('.novel-notebook/local/debug/events.jsonl', ignored)

    def test_writing_agents_and_guidance_are_installed_unchanged_and_tracked(self):
        checkout = Path(__file__).resolve().parents[2]
        expected = {relative: source.read_bytes()
                    for relative, (source, _) in resource_paths(checkout).items()}
        for language in ('en', 'is'):
            with self.subTest(language=language):
                self.target = self.parent / language
                self.initialize(language=language)
                self.assertEqual(verify_writing_resources(self.target, expected), len(expected))

    def test_project_instructions_and_handoff_are_installed_for_continuation(self):
        from importlib.resources import files

        result = self.initialize()
        instructions = (self.target / 'AGENTS.md').read_bytes()
        self.assertEqual(instructions, files('novel_creator.codex').joinpath(
            'notebook/AGENTS.md').read_bytes().replace(b'\r\n', b'\n'))
        self.assertIn(b'Use Novel Creator for ongoing story work in this project.', instructions)
        self.assertIn(b'no Python\nlauncher or per-turn skill invocation is required', instructions)
        handoff = result['data']['next_action']
        for relative in ('AGENTS.md', 'notebook/project.md', 'notebook/working-summary.md'):
            self.assertIn(relative, handoff)
            self.assertTrue((self.target / relative).is_file())
        for relative in ('.novel-notebook/workflows/conversation.md',
                         '.novel-notebook/workflows/format.md', '.novel-notebook/languages/en.md'):
            self.assertTrue((self.target / relative).is_file())
        self.assertIn('Continue in this notebook folder', handoff)
        self.assertIn('do not initialize it again', handoff)

    def test_focused_guidance_resources_are_required_before_creation(self):
        from importlib.resources import files

        for name in ('clarify', 'analyze', 'help'):
            for kind in ('workflow', 'skill'):
                with self.subTest(name=name, kind=kind):
                    self.target = self.parent / f'{name}-{kind}-notebook'
                    package = ('novel_creator.notebook_resources' if kind == 'workflow'
                               else 'novel_creator.codex')
                    replacement = self.parent / f'{name}-{kind}-resources'
                    shutil.copytree(files(package), replacement)
                    relative = (f'workflows/{name}.md' if kind == 'workflow'
                                else f'notebook/skills/novel-{name}/SKILL.md')
                    (replacement / relative).unlink()

                    def resources(requested):
                        return replacement if requested == package else files(requested)

                    with patch.object(self.module, 'files', side_effect=resources):
                        with self.assertRaises(FileNotFoundError):
                            self.initialize()
                    self.assertFalse(self.target.exists(), 'Incomplete resources must not create a notebook')

    def test_outline_skill_is_installed_with_resolvable_shared_guidance(self):
        import re
        for language in ('en', 'is'):
            with self.subTest(language=language):
                self.target = self.parent / language
                self.initialize(language=language)
                skill = self.target / '.agents/skills/novel-outline/SKILL.md'
                workflow = self.target / '.novel-notebook/workflows/outline.md'
                self.assertTrue(skill.is_file(), 'New notebooks need the explicit outline skill')
                self.assertTrue(workflow.is_file())
                links = re.findall(r'\]\(([^)]+)\)', skill.read_text(encoding='utf-8'))
                self.assertTrue(links)
                self.assertIn(workflow.resolve(), [(skill.parent / link).resolve() for link in links])
                for link in links:
                    self.assertTrue((skill.parent / link).is_file(), link)
                tracked = subprocess.check_output(['git', '-C', str(self.target), 'ls-files'], text=True)
                self.assertIn('.agents/skills/novel-outline/SKILL.md', tracked)
                self.assertIn('.novel-notebook/workflows/outline.md', tracked)
                self.assertFalse((self.target / 'notebook/topics').exists())
                self.assertFalse((self.target / 'chapters').exists())
                self.assertFalse((self.target / 'scenes').exists())

    def test_brainstorming_resources_are_installed_linked_and_committed(self):
        import re
        stages = ('book-idea', 'premise', 'character', 'plot', 'setting')
        for language in ('en', 'is'):
            with self.subTest(language=language):
                self.target = self.parent / language
                self.initialize(language=language)
                tracked = subprocess.check_output(
                    ['git', '-C', str(self.target), 'ls-files'], text=True).splitlines()
                workflow = self.target / '.novel-notebook/workflows/brainstorming.md'
                self.assertTrue(workflow.is_file())
                self.assertIn(workflow.relative_to(self.target).as_posix(), tracked)
                for stage in stages:
                    skill = self.target / f'.agents/skills/novel-{stage}/SKILL.md'
                    self.assertTrue(skill.is_file(), stage)
                    self.assertIn(skill.relative_to(self.target).as_posix(), tracked)
                    links = re.findall(r'\]\(([^)]+)\)', skill.read_text(encoding='utf-8'))
                    self.assertIn(workflow.resolve(), [(skill.parent / link).resolve() for link in links])
                    for link in links:
                        self.assertTrue((skill.parent / link).is_file(), link)
                for path in (self.target / '.novel-notebook/workflows').glob('*.md'):
                    for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                        self.assertTrue((path.parent / link).is_file(), (path, link))
                self.assertFalse((self.target / 'notebook/topics').exists())

    def test_character_development_skill_links_to_installed_workflow(self):
        import re

        checkout = Path(__file__).resolve().parents[2]
        for language in ('en', 'is'):
            with self.subTest(language=language):
                self.target = self.parent / language
                self.initialize(language=language)
                relatives = ('.agents/skills/novel-character-develop/SKILL.md',
                             '.novel-notebook/workflows/character-development.md')
                resources = resource_paths(checkout)
                for relative in relatives:
                    source, _ = resources[relative]
                    self.assertEqual((self.target / relative).read_bytes(), source.read_bytes())
                    tracked = subprocess.check_output(
                        ['git', '-C', str(self.target), 'ls-files', '--', relative], text=True)
                    self.assertEqual(tracked.strip(), relative)
                skill, workflow = (self.target / relative for relative in relatives)
                destinations = {(skill.parent / link).resolve() for link in re.findall(
                    r'\]\(([^)]+)\)', skill.read_text(encoding='utf-8'))}
                self.assertIn(workflow.resolve(), destinations)
                self.assertFalse((self.target / 'notebook/topics').exists())
                self.assertEqual(subprocess.check_output(
                    ['git', '-C', str(self.target), 'status', '--porcelain']), b'')

    def test_existing_empty_directory_is_preserved(self):
        self.target.mkdir()
        with self.assertRaises(ToolError):
            self.initialize()
        self.assertEqual(list(self.target.iterdir()), [])

    def test_existing_legacy_and_unrelated_content_is_preserved(self):
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                self.target = self.parent / str(legacy)
                self.target.mkdir()
                (self.target / 'author.txt').write_text('Keep me', encoding='utf-8')
                if legacy:
                    (self.target / '.novel-creator').mkdir()
                    (self.target / '.novel-creator/manifest.json').write_text('{}')
                before = self.snapshot()
                with self.assertRaises(ToolError):
                    self.initialize()
                self.assertEqual(self.snapshot(), before)

    def test_completed_notebook_and_staged_edits_are_not_reinitialized(self):
        self.initialize()
        (self.target / 'notebook/project.md').write_text('Author edit', encoding='utf-8')
        subprocess.check_call(['git', '-C', str(self.target), 'add', 'notebook/project.md'])
        before = self.snapshot()
        with self.assertRaises(ToolError):
            self.initialize()
        self.assertEqual(self.snapshot(), before)

    def test_nested_repository_is_refused_before_creation(self):
        subprocess.check_call(['git', 'init', '-q', str(self.parent)])
        with self.assertRaises(ToolError):
            self.initialize()
        self.assertFalse(self.target.exists())

    def test_bare_repository_is_refused_without_changes(self):
        subprocess.check_call(['git', 'init', '--bare', '-q', str(self.parent)])
        before = {p.relative_to(self.parent): p.read_bytes()
                  for p in self.parent.rglob('*') if p.is_file()}
        with self.assertRaises(ToolError):
            self.initialize()
        self.assertFalse(self.target.exists())
        self.assertEqual({p.relative_to(self.parent): p.read_bytes()
                          for p in self.parent.rglob('*') if p.is_file()}, before)

    def test_discovery_ceiling_cannot_hide_enclosing_repository(self):
        subprocess.check_call(['git', 'init', '-q', str(self.parent)])
        nested = self.parent / 'nested'
        nested.mkdir()
        child = nested / 'child'
        child.mkdir()
        self.target = child / 'Novel'
        before = {p.relative_to(self.parent): p.read_bytes()
                  for p in self.parent.rglob('*') if p.is_file()}
        with patch.dict(os.environ, {'GIT_CEILING_DIRECTORIES': str(nested),
                                     'GIT_DISCOVERY_ACROSS_FILESYSTEM': '0'}):
            with self.assertRaises(ToolError):
                self.initialize()
        self.assertFalse(self.target.exists())
        self.assertEqual({p.relative_to(self.parent): p.read_bytes()
                          for p in self.parent.rglob('*') if p.is_file()}, before)

    def test_symlink_component_is_refused(self):
        link = self.parent / 'link'
        actual = self.parent / 'actual'
        actual.mkdir()
        try:
            link.symlink_to(actual, target_is_directory=True)
        except OSError:
            self.skipTest('Symlink creation unavailable')
        self.target = link / 'Novel'
        with self.assertRaises(ToolError):
            self.initialize()
        self.assertEqual(list(actual.iterdir()), [])

    def test_missing_identity_does_not_create_destination(self):
        for key in ('GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_NAME', 'GIT_COMMITTER_EMAIL'):
            os.environ.pop(key, None)
        os.environ['GIT_CONFIG_COUNT'] = '1'
        os.environ['GIT_CONFIG_KEY_0'] = 'user.useConfigOnly'
        os.environ['GIT_CONFIG_VALUE_0'] = 'true'
        with self.assertRaisesRegex(ToolError, 'identity'):
            self.initialize()
        self.assertFalse(self.target.exists())

    def test_invalid_language_and_title_do_not_create_destination(self):
        for kwargs in ({'language': 'fr'}, {'title': ''}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ToolError):
                self.module.initialize(self.target, **kwargs)
            self.assertFalse(self.target.exists())

    def test_failed_initial_commit_preserves_partial_notebook(self):
        real_run = subprocess.run
        def fail_commit(argv, **kwargs):
            if 'commit' in argv:
                return subprocess.CompletedProcess(argv, 1, stdout=b'', stderr=b'commit denied')
            return real_run(argv, **kwargs)
        with patch.object(self.module.subprocess, 'run', side_effect=fail_commit):
            with self.assertRaisesRegex(ToolError, 'partial'):
                self.initialize()
        self.assertTrue((self.target / 'notebook/project.md').exists())
        before = self.snapshot()
        with self.assertRaises(ToolError):
            self.initialize()
        self.assertEqual(self.snapshot(), before)

    def test_competing_creator_is_preserved(self):
        real_mkdir = Path.mkdir
        def compete(path, *args, **kwargs):
            if path == self.target:
                real_mkdir(path)
                (path / 'winner.txt').write_text('Other creator', encoding='utf-8')
            return real_mkdir(path, *args, **kwargs)
        with patch.object(Path, 'mkdir', compete), self.assertRaises(ToolError):
            self.initialize()
        self.assertEqual(list(self.target.iterdir()), [self.target / 'winner.txt'])


class LegacyNotebookBoundary(unittest.TestCase):
    def test_legacy_bundle_excludes_notebook_setup_and_rejects_its_command(self):
        import sys
        from novel_creator.install import initialize
        from novel_creator.update_release import export_bundle

        with tempfile.TemporaryDirectory(prefix='legacy-notebook-boundary-') as directory:
            home = Path(directory).resolve() / 'home'
            home.mkdir()
            (home / '.gitconfig').write_text('[user]\n\tuseConfigOnly = true\n', encoding='utf-8')
            root = Path(directory).resolve() / 'legacy'
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / 'xdg'),
                       GIT_CONFIG_NOSYSTEM='1',
                       GIT_AUTHOR_NAME='Test', GIT_AUTHOR_EMAIL='test@example.invalid',
                       GIT_COMMITTER_NAME='Test', GIT_COMMITTER_EMAIL='test@example.invalid')
            with patch.dict(os.environ, env, clear=True):
                root.mkdir()
                subprocess.check_call(['git', '-C', str(root), 'init', '-q', '-b', 'main'])
                subprocess.check_call(['git', '-C', str(root), 'config', 'user.name', 'Disposable Test'])
                subprocess.check_call(['git', '-C', str(root), 'config', 'user.email', 'test@example.invalid'])
                initialize(root, json.dumps({'title': 'Legacy'}))
            exported = export_bundle()['files']
            setup_module = '.novel-creator/src/novel_creator/notebook.py'
            launcher = root / '.novel-creator/run.py'
            help_result = subprocess.run([sys.executable, '-I', str(launcher), '--help'],
                                         capture_output=True, text=True, env=env)
            target = Path(directory) / 'unwanted-notebook'
            result = subprocess.run([sys.executable, '-I', str(launcher), 'notebook', 'init',
                                     'Unwanted', '--path', str(target), '--json'],
                                    capture_output=True, text=True, env=env)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(json.loads(result.stdout)['error']['code'], 2)
            self.assertNotIn('Traceback', result.stderr)
            self.assertFalse(target.exists())
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertNotIn('notebook', help_result.stdout)
            self.assertNotIn(setup_module, exported)
            self.assertFalse((root / setup_module).exists())
            self.assertNotIn('.agents/skills/novel-outline/SKILL.md', exported)
            self.assertFalse((root / '.agents/skills/novel-outline').exists())
            self.assertFalse((root / '.novel-notebook/workflows/outline.md').exists())
            for stage in ('book-idea', 'premise', 'character', 'character-develop', 'plot', 'setting',
                          'agent', 'research', 'scene', 'chapter', 'review'):
                skill = f'.agents/skills/novel-{stage}/SKILL.md'
                self.assertNotIn(skill, exported)
                self.assertFalse((root / skill).exists())
            for method in ('clarify', 'analyze', 'help'):
                self.assertIn(f'.agents/skills/novel-{method}/SKILL.md', exported)
                self.assertTrue((root / f'.agents/skills/novel-{method}/SKILL.md').is_file())
                self.assertTrue((root / f'.novel-creator/workflows/{method}.md').is_file())
            self.assertFalse((root / '.novel-notebook/workflows/brainstorming.md').exists())
            self.assertFalse((root / '.codex/agents').exists())
            self.assertFalse(any(path.startswith('.codex/agents/') for path in exported))
            for workflow in ('agents', 'manuscript', 'research', 'review', 'clarify', 'analyze', 'help'):
                self.assertFalse((root / f'.novel-notebook/workflows/{workflow}.md').exists())
