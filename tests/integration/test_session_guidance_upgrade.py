"""Offline documented session-guidance upgrade with frozen public resources."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from novel_creator.notebook import initialize, _host_text, update
from novel_creator.notebook_side_character import update as side_update
from novel_creator.retro_issue_setup import setup as issue_setup, SESSION_BLOCKS
from tests.release_fixtures import published_wheel
from types import SimpleNamespace
from tests import session_guidance_checks as checks
from tests.integration import test_path_redirection
from tests.verify_plugin_install import temporary_environment, snapshot


class SessionGuidanceUpgrade(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='session-guidance-')
        self.addCleanup(temporary.cleanup)
        self.area = Path(temporary.name).resolve()
        self.env = temporary_environment(self.area)
        environment = patch.dict(os.environ, self.env, clear=True)
        environment.start()
        self.addCleanup(environment.stop)

    def book(self, host='codex', source='project', language='en', version='0.10.0'):
        root = self.area / f'{version}-{host}-{source}-{language}'
        initialize(root, host=host, skill_source=source, language=language)
        for name in checks.GUIDES:
            public = checks.ROOT / f'tests/fixtures/session-guidance-{version}' / name
            raw = _host_text(public.read_text(encoding='utf-8'), host, source).encode()
            (root / '.novel-notebook/workflows' / name).write_bytes(raw)
        return root

    def run_script(self, root, *args):
        return subprocess.run([sys.executable, '-I', '-B', '-c', checks.procedure(), *args],
                              cwd=root, env=self.env, capture_output=True, text=True)

    def test_public_resources_all_host_source_language_combinations(self):
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                for language in ('en', 'is'):
                    with self.subTest(host=host, source=source, language=language):
                        root = self.book(host, source, language)
                        expected = self.area / ('New ' + root.name)
                        initialize(expected, host=host, skill_source=source, language=language)
                        checks.exercise(sys.executable, root, expected, self.env, host=host, source=source)

    def test_public_0102_guides_and_existing_exact_session_routing(self):
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                for language in ('en', 'is'):
                    with self.subTest(host=host, source=source, language=language):
                        root = self.book(host, source, language, version='0.10.2')
                        for name in (('AGENTS.md', 'CLAUDE.md') if host == 'both' else
                                     ('CLAUDE.md',) if host == 'claude' else ('AGENTS.md',)):
                            path = root / name
                            path.write_bytes(path.read_bytes() + b'\n## Session guidance\n\n' +
                                             SESSION_BLOCKS[1].encode() + b'\n')
                        expected = self.area / ('New ' + root.name)
                        initialize(expected, host=host, skill_source=source, language=language)
                        checks.exercise(sys.executable, root, expected, self.env, host=host, source=source)

    def test_true_public_0100_requires_explicit_feature_then_issue_setup(self):
        root = self.area / 'actual-public-0100'
        code = ('import sys;sys.path.insert(0,sys.argv[1]);'
                'from novel_creator.notebook import initialize;initialize(sys.argv[2])')
        subprocess.run([sys.executable, '-I', '-B', '-c', code,
                        str(published_wheel('0.10.0')), str(root)], cwd=self.area,
                       env=self.env, check=True, capture_output=True)
        self.assertFalse((root / '.novel-notebook/workflows/side-character.md').exists())
        before = snapshot(root)
        self.assertNotEqual(self.run_script(root, 'preview').returncode, 0)
        self.assertEqual(snapshot(root), before)
        preview = side_update(root)['data']
        side_update(root, apply=True, preview_id=preview['preview_id'],
                    expected_head=preview['reviewed_head'])
        args = SimpleNamespace(novel=root, apply=False, preview=None, expected_head=None)
        preview = issue_setup(args)
        args.apply, args.preview, args.expected_head = True, preview['preview_id'], preview['reviewed_head']
        issue_setup(args)
        expected = self.area / 'New actual-public-0100'
        initialize(expected)
        checks.exercise(sys.executable, root, expected, self.env, host='codex', source='project')

    def test_missing_side_character_prerequisite_refuses_before_writes(self):
        root = self.book(version='0.10.2')
        (root / '.novel-notebook/workflows/side-character.md').unlink()
        before = snapshot(root)
        result = self.run_script(root, 'preview')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Missing prerequisite: .novel-notebook/workflows/side-character.md', result.stderr)
        self.assertEqual(snapshot(root), before)

    def test_custom_session_routing_refuses(self):
        root = self.book(version='0.10.2')
        path = root / 'AGENTS.md'
        path.write_bytes(path.read_bytes() + b'\n' + SESSION_BLOCKS[1].encode().replace(
            b'Keep character-development', b'Custom character-development') + b'\n')
        before = snapshot(root)
        self.assertNotEqual(self.run_script(root, 'preview').returncode, 0)
        self.assertEqual(snapshot(root), before)

    def test_manual_routing_preserves_later_focused_update_character_boundary(self):
        root = self.book()
        review = json.loads(self.run_script(root, 'preview').stdout)
        result = self.run_script(root, 'apply', review['preview_id'], review['reviewed_head'])
        self.assertEqual(result.returncode, 0, result.stderr)
        preview = update(root)['data']
        update(root, apply=True, preview_id=preview['preview_id'], expected_head=preview['reviewed_head'])
        # The appended manual block does not become part of the protected old
        # Character development section when the older updater extracts it.
        self.assertIn(b'novel-creator:issue-retro:start', (root / 'AGENTS.md').read_bytes())

    def test_changed_head_and_malformed_marker_refuse_without_writes(self):
        root = self.book()
        preview = json.loads(self.run_script(root, 'preview').stdout)
        subprocess.check_call(['git', '-C', str(root), 'commit', '--allow-empty', '-qm', 'New HEAD'])
        before = snapshot(root)
        result = self.run_script(root, 'apply', preview['preview_id'], preview['reviewed_head'])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(root), before)
        marker = root / '.novel-notebook/integration.json'
        marker.write_text('{"version":true,"host":"codex","skill_source":"project"}')
        before = snapshot(root)
        self.assertNotEqual(self.run_script(root, 'preview').returncode, 0)
        self.assertEqual(snapshot(root), before)

    def test_redirected_paths_refuse_before_writes(self):
        root = self.book()
        path = root / '.novel-notebook/workflows'
        outside = self.area / 'external-workflows'
        path.rename(outside)  # Both resolved targets are inside this disposable fixture.
        if os.name == 'nt':
            test_path_redirection.PathRedirectionTests.junction(path, outside)
        else:
            path.symlink_to(outside, target_is_directory=True)
        try:
            before = snapshot(root)
            external = snapshot(outside)
            self.assertNotEqual(self.run_script(root, 'preview').returncode, 0)
            self.assertEqual(snapshot(root), before)
            self.assertEqual(snapshot(outside), external)
        finally:
            if os.name == 'nt':
                path.rmdir()
            else:
                path.unlink()
            outside.rename(path)

    def test_generic_focused_updater_accepts_only_public_old_character_workflow(self):
        root = self.book()
        public_root = checks.ROOT / 'tests/fixtures/session-guidance-0.10.0/root-AGENTS.md'
        (root / 'AGENTS.md').write_bytes(public_root.read_bytes().replace(
            b'## Character development\n', b'Custom writer direction.\n\n## Character development\n'))
        # Existing focused updater does not refresh conversation/debugging/roles.
        before = snapshot(root)
        preview = update(root)['data']
        update(root, apply=True, preview_id=preview['preview_id'], expected_head=preview['reviewed_head'])
        after = snapshot(root)
        self.assertTrue(update(root)['data']['already_current'])
        for name in ('conversation.md', 'debugging.md', 'agents.md'):
            relative = '.novel-notebook/workflows/' + name
            self.assertEqual(before[relative], after[relative])
        path = root / '.novel-notebook/workflows/character-development.md'
        path.write_bytes(path.read_bytes() + b'Custom guidance.\n')
        from novel_creator.cli import ToolError
        with self.assertRaises(ToolError):
            update(root)
