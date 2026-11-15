"""Side-character setup and reviewed default updates from immutable public wheels."""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
import zipfile

from novel_creator import notebook
from novel_creator.cli import ToolError
from novel_creator.install import initialize as initialize_legacy
from novel_creator.update_release import export_bundle
from tests.integration import test_notebook_update as update_tests
from tests.release_fixtures import published_wheel


SKILL = '.agents/skills/novel-side-character/SKILL.md'
WORKFLOW = '.novel-notebook/workflows/side-character.md'
HELP = '.novel-notebook/workflows/help.md'
START = b'<!-- novel-creator:side-character:start -->'
END = b'<!-- novel-creator:side-character:end -->'


class SideCharacterRootSection(unittest.TestCase):
    template = (b'# Writer instructions\n\n' + START +
                b'\n## Side-character profiles\n\nProtected routing.\n' + END + b'\n')
    equivalent_headings = (b'## Side-character profiles ', b'## Side-character profiles\t',
                           b'## Side-character profiles ##', b'## Side-character profiles ### \t',
                           b' ## Side-character profiles', b'   ## Side-character profiles ',
                           b'  ##\tSide-character profiles\t##', b'##   Side-character profiles')

    def test_equivalent_duplicate_h2_headings_refuse(self):
        for heading in self.equivalent_headings:
            for newline in (b'\n', b'\r\n'):
                with self.subTest(heading=heading, newline=newline):
                    current = self.template + b'\n' + heading + b'\nCustom routing.\n'
                    current = current.replace(b'\n', newline)
                    with self.assertRaisesRegex(ToolError, 'side-character'):
                        notebook._append_side_character(current, self.template)

    def test_equivalent_unmanaged_or_customized_managed_h2_refuses(self):
        for heading in self.equivalent_headings:
            for managed in (False, True):
                with self.subTest(heading=heading, managed=managed):
                    current = heading + b'\nCustom routing.\n'
                    if managed:
                        current = START + b'\n' + current + END + b'\n'
                    with self.assertRaisesRegex(ToolError, 'side-character'):
                        notebook._append_side_character(current, self.template)

    def test_current_lf_crlf_and_other_heading_levels_keep_exact_bytes(self):
        for newline in (b'\n', b'\r\n'):
            for heading in (b'# Side-character profiles', b'### Side-character profiles',
                            b'    ## Side-character profiles', b'## Side-character profiles###'):
                with self.subTest(newline=newline, heading=heading):
                    current = (self.template + b'\n' + heading + b'\nWriter text.\n').replace(b'\n', newline)
                    self.assertEqual(notebook._append_side_character(current, self.template), current)


class SideCharacterInstall(unittest.TestCase):
    setUp = update_tests.NotebookUpdate.setUp
    initialize = update_tests.NotebookUpdate.initialize
    snapshot = update_tests.NotebookUpdate.snapshot
    git = update_tests.NotebookUpdate.git
    apply = update_tests.NotebookUpdate.apply

    def old(self, version='0.10.1'):
        # Run the previous public initializer, rather than synthesizing its layout
        # by deleting a feature from the current initializer.
        program = ('import sys;sys.path.insert(0,sys.argv[1]);'
                   'from novel_creator.notebook import initialize;initialize(sys.argv[2])')
        result = subprocess.run([sys.executable, '-I', '-B', '-c', program,
                                 str(published_wheel(version)), str(self.target)],
                                cwd=self.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_previous_public_updates_preserve_story_root_history_and_raw_index(self):
        for version in ('0.10.0', '0.10.1'):
            for newline in (b'\n', b'\r\n'):
                with self.subTest(version=version, newline=newline):
                    self.target = self.parent / (version + str(len(list(self.parent.iterdir()))))
                    self.old(version)
                    agents = self.target / 'AGENTS.md'
                    original = agents.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', newline)
                    original += newline + b'## Writer directions' + newline + b'Keep these exact bytes.'
                    agents.write_bytes(original)
                    staged = self.target / 'writer.txt'
                    staged.write_bytes(b'staged writer text')
                    self.git('add', 'writer.txt')
                    staged.write_bytes(b'unstaged writer text')
                    head = self.git('rev-parse', 'HEAD')
                    index = (self.target / '.git/index').read_bytes()
                    before = self.snapshot()
                    preview = notebook.update(self.target)
                    self.assertEqual(self.snapshot(), before)
                    expected = {SKILL, WORKFLOW, HELP, 'AGENTS.md',
                                '.novel-notebook/workflows/retrospective.md'}
                    if version == '0.10.0':
                        expected.add('.novel-notebook/workflows/character-development.md')
                    self.assertEqual({c['path'] for c in preview['data']['changes']}, expected)
                    self.apply(preview)
                    self.assertTrue(agents.read_bytes().startswith(original))
                    self.assertIn(START, agents.read_bytes())
                    self.assertIn(b'novel-side-character', (self.target / HELP).read_bytes())
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    self.assertEqual(self.git('rev-parse', 'HEAD'), head)
                    for relative, raw in before.items():
                        if relative not in expected:
                            self.assertEqual((self.target / relative).read_bytes(), raw, relative)
                    self.assertTrue(notebook.update(self.target)['data']['already_current'])

    def test_current_setup_and_legacy_bundle_have_feature_and_resolvable_links(self):
        self.initialize()
        self.assertTrue((self.target / SKILL).is_file())
        self.assertTrue((self.target / WORKFLOW).is_file())
        self.assertTrue(notebook.update(self.target)['data']['already_current'])
        exported = export_bundle()
        bundle = {name: base64.b64decode(raw) for name, raw in exported['files'].items()}
        self.assertIn(SKILL, bundle)
        self.assertIn('.novel-creator/workflows/side-character.md', bundle)
        for relative in (SKILL, '.novel-creator/workflows/side-character.md'):
            self.assertEqual(hashlib.sha256(bundle[relative]).hexdigest(), exported['checksums'][relative])
            for link in re.findall(rb'\]\(([^)#]+)(?:#[^)]*)?\)', bundle[relative]):
                resolved = os.path.normpath(str(Path(relative).parent / link.decode())).replace('\\', '/')
                self.assertIn(resolved, bundle, (relative, link))

    def test_new_legacy_setup_pins_feature_and_root_routing(self):
        result = initialize_legacy(self.target, json.dumps({'title': 'Disposable profile book',
                                                          'manuscript_language': 'en'}))
        self.assertTrue(result['data']['saved'])
        self.assertTrue((self.target / SKILL).is_file())
        self.assertTrue((self.target / '.novel-creator/workflows/side-character.md').is_file())
        self.assertIn(b'.novel-creator/workflows/side-character.md', (self.target / 'AGENTS.md').read_bytes())
        manifest = json.loads((self.target / '.novel-creator/manifest.json').read_bytes())
        for relative in (SKILL, '.novel-creator/workflows/side-character.md'):
            self.assertEqual(manifest['checksums'][relative],
                             hashlib.sha256((self.target / relative).read_bytes()).hexdigest())

    def test_custom_duplicate_incomplete_and_unmarked_routing_refuse_before_writes(self):
        self.initialize()
        path = self.target / 'AGENTS.md'
        raw = path.read_bytes()
        section = raw[raw.index(START):raw.index(END) + len(END)]
        for changed in (raw.replace(b'## Side-character profiles', b'## Side-character profiles\nCustom'),
                        raw + b'\n' + section, raw.replace(END, b''),
                        raw.replace(START, b'').replace(END, b'')):
            with self.subTest(changed=hashlib.sha256(changed).hexdigest()):
                path.write_bytes(changed)
                before = self.snapshot()
                with self.assertRaisesRegex(ToolError, 'side-character'):
                    notebook.update(self.target)
                self.assertEqual(self.snapshot(), before)
        path.write_bytes(raw)
        for relative in (SKILL, WORKFLOW):
            feature = self.target / relative
            original = feature.read_bytes()
            feature.write_bytes(original + b'\nWriter customization.\n')
            before = self.snapshot()
            with self.assertRaisesRegex(ToolError, 'Customized notebook resource'):
                notebook.update(self.target)
            self.assertEqual(self.snapshot(), before)
            feature.write_bytes(original)

    def test_character_section_ends_before_appended_independent_managed_blocks(self):
        self.initialize()
        agents = self.target / 'AGENTS.md'
        raw = agents.read_bytes().replace(b'\r\n', b'\n')
        section = raw[raw.index(START):raw.index(END) + len(END)]
        raw = raw.replace(section + b'\n\n', b'')
        raw += b'\n' + section + b'\n' + notebook._ROUTING + b'\n'
        raw += b'<!-- novel-creator:session-guidance:start -->\nSession guidance\n<!-- novel-creator:session-guidance:end -->\n'
        raw += b'<!-- novel-creator:retrospective:start -->\nRetrospective guidance\n<!-- novel-creator:retrospective:end -->\n'
        agents.write_bytes(raw.replace(b'\n', b'\r\n'))
        before = self.snapshot()
        self.assertTrue(notebook.update(self.target)['data']['already_current'])
        self.apply()
        self.assertEqual(self.snapshot(), before)

    def test_changed_index_bytes_invalidate_preview_before_writes(self):
        for change in ('staging', 'index-format'):
            with self.subTest(change=change):
                self.target = self.parent / change
                self.old()
                preview = notebook.update(self.target)
                original_index = (self.target / '.git/index').read_bytes()
                entries = self.git('ls-files', '--stage', '-z')
                if change == 'staging':
                    (self.target / 'writer.txt').write_bytes(b'writer staging')
                    self.git('add', 'writer.txt')
                else:
                    # Same semantic entries, different valid Git index encoding.
                    self.git('update-index', '--index-version=4')
                    self.assertEqual(self.git('ls-files', '--stage', '-z'), entries)
                self.assertNotEqual((self.target / '.git/index').read_bytes(), original_index)
                before = self.snapshot()
                with self.assertRaisesRegex(ToolError, 'stale'):
                    self.apply(preview)
                self.assertEqual(self.snapshot(), before)

    def test_equal_feature_hardlink_and_changed_identity_are_refused(self):
        self.initialize()
        path = self.target / SKILL
        raw = path.read_bytes()
        outside = self.parent / 'outside-skill'
        path.rename(outside)
        os.link(outside, path)
        with self.assertRaisesRegex(ToolError, 'hard-linked'):
            notebook.update(self.target)
        path.unlink()
        path.write_bytes(raw)
        preview = notebook.update(self.target)
        path.rename(self.parent / 'previous-identity')
        path.write_bytes(raw)
        with self.assertRaisesRegex(ToolError, 'stale'):
            self.apply(preview)

    def test_index_change_during_final_probe_stops_before_first_write(self):
        self.old()
        preview = notebook.update(self.target)
        original = subprocess.run
        probes = 0
        def change_index(command, *args, **kwargs):
            nonlocal probes
            result = original(command, *args, **kwargs)
            if command[-3:] == ['rev-parse', '--verify', 'HEAD']:
                probes += 1
                if probes == 2:
                    (self.target / 'writer.txt').write_bytes(b'new staging')
                    self.git('add', 'writer.txt')
            return result
        with patch.object(subprocess, 'run', change_index), self.assertRaises(ToolError) as caught:
            self.apply(preview)
        self.assertEqual(caught.exception.data['written_paths'], [])
        self.assertFalse((self.target / SKILL).exists())
        self.assertFalse((self.target / WORKFLOW).exists())
        self.assertIn(b'writer.txt', self.git('ls-files', '--stage'))

    def test_partial_feature_addition_resumes_without_rewriting_completed_skill(self):
        self.old()
        preview = notebook.update(self.target)
        original_open = Path.open
        def interrupted(path, *args, **kwargs):
            if path == self.target / WORKFLOW and args and args[0] == 'xb':
                raise OSError('Controlled interruption before workflow addition')
            return original_open(path, *args, **kwargs)
        with patch.object(Path, 'open', interrupted), self.assertRaises(ToolError) as caught:
            self.apply(preview)
        self.assertTrue(caught.exception.data['partial'])
        self.assertIn(SKILL, caught.exception.data['written_paths'])
        skill = (self.target / SKILL).read_bytes()
        self.apply()
        self.assertEqual((self.target / SKILL).read_bytes(), skill)
        self.assertTrue(notebook.update(self.target)['data']['already_current'])
