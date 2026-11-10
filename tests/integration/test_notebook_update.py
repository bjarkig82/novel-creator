"""Explicit additive notebook retrofit, including old and customized projects."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from novel_creator import notebook
from novel_creator.cli import ToolError, main
from tests.integration import test_notebook_init as notebook_init_tests


class NotebookUpdate(unittest.TestCase):
    setUp = notebook_init_tests.NotebookInitialization.setUp
    initialize = notebook_init_tests.NotebookInitialization.initialize
    snapshot = notebook_init_tests.NotebookInitialization.snapshot
    def old_notebook(self, language='en', *, old_roles=False):
        self.initialize(language=language)
        for name in ('clarify', 'analyze', 'help'):
            (self.target / f'.agents/skills/novel-{name}/SKILL.md').unlink()
            (self.target / f'.novel-notebook/workflows/{name}.md').unlink()
        if old_roles:
            for name in ('agents', 'manuscript', 'research', 'review'):
                (self.target / f'.novel-notebook/workflows/{name}.md').unlink()
        (self.target / 'AGENTS.md').write_text('# My story instructions\n\nKeep my custom directions.\n', encoding='utf-8')
        (self.target / 'notebook/accepted.md').write_text('Accepted writer content.\n', encoding='utf-8')
        self.git('add', '.')
        self.git('commit', '-m', 'Existing notebook before focused methods')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.target), *args])

    def apply(self, preview=None):
        data = (preview or notebook.update(self.target))['data']
        return notebook.update(self.target, apply=True, preview_id=data['preview_id'],
                               expected_head=data['reviewed_head'])

    def test_upgrade_existing_notebooks_in_both_languages_preserves_history_and_staging(self):
        for language in ('en', 'is'):
            with self.subTest(language=language):
                self.target = self.parent / language
                self.old_notebook(language, old_roles=True)
                staged = self.target / 'writer-draft.txt'
                staged.write_bytes(b'staged writer version\n')
                self.git('add', 'writer-draft.txt')
                staged.write_bytes(b'unstaged writer version\n')
                index = self.git('ls-files', '--stage', '-z')
                head = self.git('rev-parse', 'HEAD')
                accepted = (self.target / 'notebook/accepted.md').read_bytes()
                agents = (self.target / 'AGENTS.md').read_bytes()
                before = self.snapshot()
                preview = notebook.update(self.target)
                self.assertEqual(self.snapshot(), before, 'Preview must not mutate any files')
                self.assertFalse(preview['data']['ready'])
                result = self.apply(preview)
                self.assertTrue(result['data']['ready'])
                self.assertEqual(self.git('rev-parse', 'HEAD'), head)
                self.assertEqual(self.git('ls-files', '--stage', '-z'), index)
                self.assertEqual(staged.read_bytes(), b'unstaged writer version\n')
                self.assertEqual((self.target / 'notebook/accepted.md').read_bytes(), accepted)
                self.assertTrue((self.target / 'AGENTS.md').read_bytes().startswith(agents))
                for name in ('clarify', 'analyze', 'help'):
                    self.assertTrue((self.target / f'.agents/skills/novel-{name}/SKILL.md').is_file())
                    self.assertTrue((self.target / f'.novel-notebook/workflows/{name}.md').is_file())
                self.assertTrue(notebook.update(self.target)['data']['already_current'])
                after = self.snapshot()
                self.assertTrue(self.apply()['data']['ready'])
                self.assertEqual(self.snapshot(), after)

    def test_valid_project_metadata_fences_and_line_endings_preserve_bytes(self):
        for fence, newline in (('```', b'\n'), ('```', b'\r\n'),
                               ('~~~', b'\n'), ('~~~', b'\r\n')):
            with self.subTest(fence=fence, newline=newline):
                self.target = self.parent / ('fence-' + str(len(list(self.parent.iterdir()))))
                self.old_notebook()
                project = self.target / 'notebook/project.md'
                original = project.read_bytes().replace(b'```', fence.encode()).replace(b'\n', newline)
                project.write_bytes(original)
                before = self.snapshot()
                preview = notebook.update(self.target)
                self.assertEqual(self.snapshot(), before)
                self.assertTrue(self.apply(preview)['data']['ready'])
                self.assertEqual(project.read_bytes(), original)

    def test_mismatched_or_noninitial_project_metadata_fence_is_refused(self):
        self.old_notebook()
        project = self.target / 'notebook/project.md'
        original = project.read_bytes()
        invalid = (original.replace(b'\n```\n', b'\n~~~\n', 1),
                   original.replace(b'```json', b'~~~json', 1),
                   b'# Unidentified document\n' + original,
                   original.replace(b'\n```\n', b'\n````\n', 1))
        for raw in invalid:
            with self.subTest(raw=raw[:40]):
                project.write_bytes(raw)
                before = self.snapshot()
                with self.assertRaisesRegex(ToolError, 'format-1'):
                    notebook.update(self.target)
                self.assertEqual(self.snapshot(), before)

    def test_crlf_routing_block_is_an_idempotent_noop_without_normalizing_files(self):
        self.old_notebook()
        self.assertTrue(self.apply()['data']['ready'])
        agents = self.target / 'AGENTS.md'
        original = agents.read_bytes().replace(b'\n', b'\r\n')
        agents.write_bytes(original)
        before = self.snapshot()
        preview = notebook.update(self.target)
        self.assertTrue(preview['data']['already_current'])
        self.assertTrue(self.apply(preview)['data']['ready'])
        self.assertEqual(agents.read_bytes(), original)
        self.assertEqual(self.snapshot(), before)

    def test_current_notebook_is_an_idempotent_noop(self):
        self.initialize()
        before = self.snapshot()
        self.assertTrue(notebook.update(self.target)['data']['already_current'])
        self.assertTrue(self.apply()['data']['ready'])
        self.assertEqual(self.snapshot(), before)

    def test_custom_resource_conflicts_stop_before_any_write(self):
        self.old_notebook()
        custom = self.target / '.novel-notebook/workflows/analyze.md'
        custom.write_bytes(b'Customized writer analysis instructions\n')
        before = self.snapshot()
        with self.assertRaisesRegex(ToolError, 'Customized notebook resource'):
            notebook.update(self.target)
        self.assertEqual(self.snapshot(), before)

    def test_stale_content_or_head_preview_is_refused_without_resource_writes(self):
        self.old_notebook()
        preview = notebook.update(self.target)
        agents = self.target / 'AGENTS.md'
        agents.write_bytes(agents.read_bytes() + b'New custom direction\n')
        before = self.snapshot()
        with self.assertRaisesRegex(ToolError, 'stale'):
            self.apply(preview)
        self.assertEqual(self.snapshot(), before)
        preview = notebook.update(self.target)
        self.git('add', 'AGENTS.md')
        self.git('commit', '-m', 'Writer changed instructions')
        before = self.snapshot()
        with self.assertRaisesRegex(ToolError, 'stale'):
            self.apply(preview)
        self.assertEqual(self.snapshot(), before)

    def test_partial_complete_additions_can_be_resumed_with_fresh_review(self):
        self.old_notebook()
        preview = notebook.update(self.target)
        original = Path.open
        def fail_on_second(path, *args, **kwargs):
            if str(path).endswith('/workflows/clarify.md') and args and args[0] == 'xb':
                raise OSError('Simulated interruption after one complete resource')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', fail_on_second):
            with self.assertRaises(ToolError) as caught:
                self.apply(preview)
        self.assertTrue(caught.exception.data['partial'])
        self.assertIn('.agents/skills/novel-clarify/SKILL.md', caught.exception.data['written_paths'])
        self.assertTrue(self.apply()['data']['ready'])
        self.assertTrue(notebook.update(self.target)['data']['already_current'])

    def test_symlink_destinations_and_git_redirects_are_refused(self):
        self.old_notebook()
        link = self.parent / 'redirect'
        try:
            link.symlink_to(self.target, target_is_directory=True)
        except OSError:
            self.skipTest('Directory symlinks unavailable on this host')
        before = self.snapshot()
        with self.assertRaises(ToolError):
            notebook.update(link)
        workflows = self.target / '.novel-notebook/workflows'
        moved = self.parent / 'outside-workflows'
        workflows.rename(moved)
        workflows.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(ToolError):
            notebook.update(self.target)
        workflows.unlink()
        moved.rename(workflows)
        self.assertEqual(self.snapshot(), before)
        dotgit = self.target / '.git'
        outside = self.parent / 'redirected-git'
        dotgit.rename(outside)
        dotgit.write_text('gitdir: ' + str(outside) + '\n', encoding='utf-8')
        with self.assertRaises(ToolError):
            notebook.update(self.target)

    def test_invalid_format_parent_segments_and_nested_roots_are_refused(self):
        self.old_notebook()
        for path in (self.target / 'notebook', self.target / '..' / self.target.name):
            with self.subTest(path=str(path)), self.assertRaises(ToolError):
                notebook.update(path)
        project = self.target / 'notebook/project.md'
        project.write_text('Other software, not a story notebook.\n', encoding='utf-8')
        before = self.snapshot()
        with self.assertRaisesRegex(ToolError, 'format-1'):
            notebook.update(self.target)
        self.assertEqual(self.snapshot(), before)

    def test_cli_preview_and_explicit_apply_use_bound_plan(self):
        self.old_notebook()
        def call(*args):
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(['notebook', 'update', '--path', str(self.target), *args, '--json'])
            return code, json.loads(out.getvalue())
        code, preview = call()
        self.assertEqual(code, 0)
        code, _ = call('--apply')
        self.assertEqual(code, 2)
        data = preview['data']
        code, result = call('--apply', '--preview', data['preview_id'], '--expected-head', data['reviewed_head'])
        self.assertEqual(code, 0)
        self.assertTrue(result['data']['ready'])

