"""Feature-only maintenance against actual public notebook initializers."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from novel_creator.cli import ToolError
from novel_creator import notebook_side_character as maintenance
from tests.release_fixtures import published_wheel
from tests.verify_plugin_install import temporary_environment

WORKFLOW = '.novel-notebook/workflows/side-character.md'
SKILL = '.agents/skills/novel-side-character/SKILL.md'


def snapshot(root):
    return {path.relative_to(root).as_posix() + ('/' if path.is_dir() else ''):
            b'' if path.is_dir() else path.read_bytes() for path in root.rglob('*')}


class NewFileWriteGuard(unittest.TestCase):
    def test_post_callback_opened_identity_and_link_count_are_rechecked(self):
        with tempfile.TemporaryDirectory(prefix='side-write-guard-') as directory:
            for attack in ('identity', 'hardlink'):
                path = Path(directory).resolve() / (attack + '.md')
                changed = False
                original = os.fstat
                def fstat(descriptor):
                    info = original(descriptor)
                    if changed:
                        return SimpleNamespace(st_mode=info.st_mode, st_dev=info.st_dev,
                                               st_ino=info.st_ino + (attack == 'identity'),
                                               st_nlink=2 if attack == 'hardlink' else info.st_nlink)
                    return info
                def callback(skip=False):
                    nonlocal changed
                    changed = skip
                with self.subTest(attack=attack), patch.object(maintenance.os, 'fstat', fstat):
                    with self.assertRaises(ToolError):
                        maintenance._write(path, b'Never write after the simulated race', None, callback)
                    self.assertEqual(path.read_bytes(), b'')


class NotebookSideCharacter(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='notebook-side-')
        self.addCleanup(temporary.cleanup)
        self.area = Path(temporary.name).resolve()
        environment = patch.dict(os.environ, temporary_environment(self.area), clear=True)
        environment.start()
        self.addCleanup(environment.stop)
        self.serial = 0

    def book(self, host='codex', source='project', language='en', version='0.10.1'):
        self.serial += 1
        root = self.area / f'book-{self.serial}'
        code = ('import sys;sys.path.insert(0,sys.argv[1]);'
                'from novel_creator.notebook import initialize;'
                'initialize(sys.argv[2],host=sys.argv[3],skill_source=sys.argv[4],language=sys.argv[5])')
        subprocess.run([sys.executable, '-I', '-B', '-c', code, str(published_wheel(version)),
                        str(root), host, source, language], cwd=self.area, check=True, capture_output=True)
        return root

    def preview(self, root):
        return maintenance.update(root)['data']

    def apply(self, root, preview=None):
        preview = preview or self.preview(root)
        return maintenance.update(root, apply=True, preview_id=preview['preview_id'],
                                  expected_head=preview['reviewed_head'])['data']

    def test_public_host_source_language_matrix_narrow_and_repeatable(self):
        for version in ('0.10.0', '0.10.1'):
            for host in ('codex', 'claude', 'both'):
                for source in ('project', 'plugin'):
                    for language in ('en', 'is'):
                        if version == '0.10.0' and (host, source, language) not in (
                                ('codex', 'project', 'en'), ('both', 'plugin', 'is')):
                            continue  # Earlier public compatibility representatives.
                        with self.subTest(version=version, host=host, source=source, language=language):
                            root = self.book(host, source, language, version)
                            roots = ['AGENTS.md', 'CLAUDE.md'] if host == 'both' else [
                                'AGENTS.md' if host == 'codex' else 'CLAUDE.md']
                            for name in roots:
                                raw = (root / name).read_bytes().replace(b'\r\n', b'\n')
                                (root / name).write_bytes(raw.replace(b'\n', b'\r\n') + b'\r\nCustom writer direction.\r\n')
                            (root / 'writer.txt').write_bytes(b'staged')
                            subprocess.run(['git', '-C', str(root), 'add', 'writer.txt'], check=True, capture_output=True)
                            (root / 'writer.txt').write_bytes(b'unstaged')
                            before = snapshot(root)
                            preview = self.preview(root)
                            self.assertEqual(snapshot(root), before, 'Preview wrote files/directories')
                            expected = set(roots) | {WORKFLOW}
                            if source == 'project':
                                expected |= {('.agents' if r == 'AGENTS.md' else '.claude') +
                                             '/skills/novel-side-character/SKILL.md' for r in roots}
                            self.assertEqual(set(preview['changes']), expected)
                            result = self.apply(root, preview)
                            self.assertTrue(result['ready'])
                            self.assertTrue(result['applied'])
                            self.assertEqual(set(result['written_paths']), expected)
                            after = snapshot(root)
                            for name, raw in before.items():
                                self.assertTrue(after[name].startswith(raw) if name in roots else after[name] == raw, name)
                            for name in roots:
                                added = after[name][len(before[name]):]
                                self.assertNotIn(b'\n', added.replace(b'\r\n', b''))
                            self.assertTrue(self.preview(root)['already_current'])
                            self.assertEqual(self.apply(root)['written_paths'], [])
                            if source == 'plugin':
                                self.assertFalse((root / SKILL).exists())
                                self.assertFalse((root / '.claude/skills/novel-side-character/SKILL.md').exists())

    def test_missing_prerequisite_selected_second_root_and_malformed_formats_refuse(self):
        mutations = [lambda r: (r / '.novel-notebook/workflows/conversation.md').unlink(),
                     lambda r: (r / 'CLAUDE.md').unlink(),
                     lambda r: (r / '.novel-creator').mkdir(),
                     lambda r: (r / '.novel-notebook/integration.json').write_text('{'),
                     lambda r: (r / '.novel-notebook/integration.json').write_text(json.dumps(
                         dict(version=1, host='both', skill_source='project', extra=True))),
                     lambda r: (r / 'notebook/project.md').write_text('not metadata')]
        for mutate in mutations:
            root = self.book('both')
            mutate(root)
            before = snapshot(root)
            with self.assertRaises(ToolError):
                self.preview(root)
            self.assertEqual(snapshot(root), before)

    def test_custom_feature_duplicate_section_and_conflicting_writer_rule_refuse(self):
        for kind in ('workflow', 'skill', 'section', 'duplicate', 'instruction'):
            root = self.book()
            if kind in ('workflow', 'skill'):
                path = root / (WORKFLOW if kind == 'workflow' else SKILL)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'Custom feature')
            elif kind == 'instruction':
                with (root / 'AGENTS.md').open('ab') as stream:
                    stream.write(b'\nAlways save side-character drafts immediately.\n')
            else:
                self.apply(root)
                path = root / 'AGENTS.md'
                raw = path.read_bytes()
                path.write_bytes(raw.replace(b'## Side-character profiles', b'## Side-character profiles\ncustom')
                                 if kind == 'section' else raw + b'\n ## Side-character profiles ##\n')
            before = snapshot(root)
            with self.assertRaises(ToolError):
                self.preview(root)
            self.assertEqual(snapshot(root), before)

    def test_custom_feature_labels_any_word_order_language_and_line_break_refuse(self):
        root = self.book(language='is')
        instructions = root / 'AGENTS.md'
        original = instructions.read_bytes()
        policies = ('Always save drafts for side characters immediately.',
                    'Always save drafts for\nside characters immediately.',
                    'Save all drafts for supporting-character work.',
                    'Save all drafts for minor characters.',
                    'Ask me about side-character creation first.',
                    'Supporting\ncharacters have separate writer rules.',
                    'minor‐characters', 'SIDE-CHARACTERS',
                    'Vistaðu drög að aukapersónum strax.',
                    'AUKAPERSÓNUR\nFylgdu fyrri fyrirmælum mínum.',
                    'Drög að aukapersónu verða alltaf vistuð.')
        for policy in policies:
            with self.subTest(policy=policy):
                instructions.write_bytes(original + ('\n## Writer directions\n' + policy + '\n').encode())
                before = snapshot(root)
                with self.assertRaisesRegex(ToolError, 'manual reconciliation'):
                    self.preview(root)
                self.assertEqual(snapshot(root), before)
        generic = original + b'\n## Writer directions\nKeep generic character facts and custom prose intact.\n'
        instructions.write_bytes(generic)
        self.assertTrue(self.apply(root)['ready'])
        self.assertTrue(instructions.read_bytes().startswith(generic))

    def test_plugin_duplicate_local_skill_and_unselected_host_skill_refuse(self):
        for host, source, relative in [('both', 'plugin', SKILL),
                                       ('codex', 'project', '.claude/skills/novel-side-character/SKILL.md')]:
            root = self.book(host, source)
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Duplicate local skill')
            with self.assertRaisesRegex(ToolError, 'Duplicate'):
                self.preview(root)

    def test_stale_head_index_project_marker_resource_and_absence_refuse(self):
        for kind in ('head', 'index', 'project', 'marker', 'feature', 'absence', 'identity'):
            root = self.book()
            preview = self.preview(root)
            if kind == 'head':
                subprocess.run(['git', '-C', str(root), 'commit', '--allow-empty', '-qm', 'Changed'], check=True)
            elif kind == 'index':
                (root / 'writer').write_text('writer')
                subprocess.run(['git', '-C', str(root), 'add', 'writer'], check=True)
            elif kind == 'identity':
                path = root / 'AGENTS.md'
                old = path.with_suffix('.old')
                path.rename(old)
                path.write_bytes(old.read_bytes())
            else:
                name = {'project': 'notebook/project.md', 'marker': '.novel-notebook/integration.json',
                        'feature': WORKFLOW, 'absence': SKILL}[kind]
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((path.read_bytes() if path.exists() else b'') + b'changed')
            before = snapshot(root)
            with self.assertRaises(ToolError):
                self.apply(root, preview)
            self.assertEqual(snapshot(root), before)

    def test_stale_parent_and_same_byte_package_resource_identity_refuse(self):
        root = self.book()
        preview = self.preview(root)
        parent = root / '.agents/skills'
        previous = parent.with_name('previous-skills')
        parent.rename(previous)
        parent.mkdir()
        for child in previous.iterdir():
            child.rename(parent / child.name)
        previous.rmdir()
        before = snapshot(root)
        with self.assertRaisesRegex(ToolError, 'stale'):
            self.apply(root, preview)
        self.assertEqual(snapshot(root), before)
        preview = self.preview(root)
        original = maintenance.files
        alternate = self.area / 'same-byte-package'
        shutil.copytree(Path(str(original('novel_creator.codex'))), alternate)
        with patch.object(maintenance, 'files', lambda package: alternate if package == 'novel_creator.codex' else original(package)):
            with self.assertRaisesRegex(ToolError, 'stale'):
                self.apply(root, preview)
        self.assertEqual(snapshot(root), before)

    def test_documented_snippet_previews_applies_and_reports_json_errors(self):
        root = self.book('claude')
        guide = Path(__file__).resolve().parents[2] / 'docs/side-characters.md'
        snippet = guide.read_text(encoding='utf-8').split('```python\n', 1)[1].split('```', 1)[0]
        before = snapshot(root)
        def invoke(*args):
            return subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', '-c', snippet, str(root), *args],
                                  cwd=self.area, capture_output=True, text=True, encoding='utf-8')
        response = invoke('preview')
        self.assertEqual(response.returncode, 0, response.stderr)
        preview = json.loads(response.stdout)['data']
        self.assertEqual(snapshot(root), before)
        response = invoke('apply', preview['preview_id'], preview['reviewed_head'])
        self.assertEqual(response.returncode, 0, response.stderr)
        self.assertTrue(json.loads(response.stdout)['data']['ready'])
        response = invoke('apply', preview['preview_id'], preview['reviewed_head'])
        self.assertEqual(response.returncode, 3)
        self.assertFalse(json.loads(response.stdout)['ok'])

    def test_hardlinks_and_redirected_files_parents_and_git_refuse(self):
        for relative in ('AGENTS.md', '.novel-notebook/workflows/conversation.md', '.git/index'):
            root = self.book()
            os.link(root / relative, self.area / ('linked-' + str(self.serial)))
            with self.assertRaises(ToolError):
                self.preview(root)
        for relative in ('.git/commondir', '.git/objects/info/alternates'):
            root = self.book()
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(self.area))
            with self.assertRaises(ToolError):
                self.preview(root)

    @unittest.skipUnless(os.name == 'nt', 'Windows junction check')
    def test_windows_junction_destination_parent_refuses(self):
        root = self.book()
        destination = self.area / 'outside'
        destination.mkdir()
        parent = root / '.agents/skills/novel-side-character'
        subprocess.run(['cmd', '/c', 'mklink', '/J', str(parent), str(destination)], check=True, capture_output=True)
        self.addCleanup(lambda: os.rmdir(parent) if parent.exists() else None)
        with self.assertRaises(ToolError):
            self.preview(root)
        self.assertEqual(list(destination.iterdir()), [])

    def test_partial_failure_reports_attempted_path_and_fresh_preview_resumes(self):
        root = self.book()
        before_index = (root / '.git/index').read_bytes()
        original = maintenance._write
        count = 0
        def fail_second(*args, **kwargs):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError('Synthetic disk failure')
            return original(*args, **kwargs)
        with patch.object(maintenance, '_write', fail_second):
            with self.assertRaises(ToolError) as caught:
                self.apply(root)
        self.assertTrue(caught.exception.data['partial'])
        self.assertEqual(len(caught.exception.data['written_paths']), 1)
        preview = self.preview(root)
        self.assertEqual(len(preview['changes']), 2)
        self.assertTrue(self.apply(root, preview)['ready'])
        self.assertEqual((root / '.git/index').read_bytes(), before_index)

    def test_same_bytes_identity_swap_immediately_before_append_refuses(self):
        root = self.book()
        original = maintenance._write
        def race(path, *args, **kwargs):
            if path.name == 'AGENTS.md':
                prior = path.with_suffix('.prior')
                path.rename(prior)
                path.write_bytes(prior.read_bytes())
            return original(path, *args, **kwargs)
        with patch.object(maintenance, '_write', race):
            with self.assertRaises(ToolError):
                self.apply(root)
        self.assertNotIn(b'side-character:start', (root / 'AGENTS.md').read_bytes())

    def test_changes_during_git_probe_recheck_every_inspected_input(self):
        for name in ('notebook/project.md', '.git/index', '.novel-notebook/workflows/conversation.md'):
            root = self.book()
            preview = self.preview(root)
            original = subprocess.run
            probes = 0
            def race(command, *args, **kwargs):
                nonlocal probes
                result = original(command, *args, **kwargs)
                if command[-3:] == ['rev-parse', '--verify', 'HEAD']:
                    probes += 1
                    if probes == 2:
                        with (root / name).open('ab') as stream:
                            stream.write(b'changed')
                return result
            with patch.object(subprocess, 'run', race), self.assertRaises(ToolError) as caught:
                self.apply(root, preview)
            self.assertEqual(caught.exception.data['written_paths'], [])
            self.assertFalse((root / WORKFLOW).exists())

    def test_default_updater_rejects_same_bytes_identity_swap_at_open(self):
        from novel_creator import notebook
        original_open = Path.open
        for action in ('replace', 'append'):
            with self.subTest(action=action):
                root = self.book()
                instructions = root / 'AGENTS.md'
                if action == 'append':
                    instructions.write_bytes(b'# Writer instructions\n')
                original = instructions.read_bytes()
                preview = notebook.update(root)['data']
                self.assertIn({'path': 'AGENTS.md', 'action': action}, preview['changes'])
                swapped = False

                def race(path, *args, **kwargs):
                    nonlocal swapped
                    # Once the earlier side workflow is installed, the next root
                    # open is the identity check immediately before its write.
                    if path == instructions and not swapped and (root / WORKFLOW).exists():
                        swapped = True
                        prior = path.with_suffix('.prior')
                        path.rename(prior)
                        path.write_bytes(prior.read_bytes())
                    return original_open(path, *args, **kwargs)

                with patch.object(Path, 'open', race), self.assertRaises(ToolError) as caught:
                    notebook.update(root, apply=True, preview_id=preview['preview_id'],
                                    expected_head=preview['reviewed_head'])
                self.assertTrue(swapped)
                self.assertNotIn('AGENTS.md', caught.exception.data['written_paths'])
                self.assertEqual(instructions.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
