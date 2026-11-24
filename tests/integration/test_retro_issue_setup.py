"""Disposable explicit setup/update delivery, without GitHub operations."""
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

from novel_creator.cli import ToolError
from novel_creator.notebook import initialize, _host_text
from novel_creator.retro_issue_setup import setup, OLD_ROOT, ROUTING
from tests.release_fixtures import published_wheel
from tests.integration import test_notebook_init


class IssueSetup(unittest.TestCase):
    setUp = test_notebook_init.NotebookInitialization.setUp

    def test_new_notebook_keeps_legacy_notice_protocol_out_of_ordinary_turns(self):
        root = self.parent / 'native-protocol'
        initialize(root)
        notebook = (root / '.novel-notebook/workflows/retrospective.md').read_text(encoding='utf-8')
        for legacy_instruction in ('retro notices pending', 'retro notices reserve',
                                   'retro notices confirm', 'retro notices reconcile',
                                   'exchange/message UUIDs', 'schemas/v1/retro.schema.json'):
            self.assertNotIn(legacy_instruction, notebook)
        self.assertIn('Ordinary notebook turns do not run legacy notice or exchange routines', notebook)
        self.assertIn('retained legacy markers', notebook)
        self.assertIn('explicitly selects genuine legacy historical recovery', notebook)
        self.assertIn('(https://github.com/bjarkig82/novel-creator/blob/main/workflows/retrospective.md)', notebook)
        legacy = (Path(__file__).resolve().parents[2] / 'workflows/retrospective.md').read_text(encoding='utf-8')
        for recovery_instruction in ('--recovery-only', 'retro notices pending',
                                     'retro notices reserve', 'retro notices confirm',
                                     'retro notices reconcile', 'normal legacy saves'):
            self.assertIn(recovery_instruction, legacy)

    def test_retrospective_handoff_and_exact_previous_snapshots(self):
        from tests.verify_plugin_install import snapshot
        fixtures = Path(__file__).resolve().parents[1] / 'fixtures'
        for fixture in (fixtures / 'session-guidance-0.10.2/retrospective.md',
                        fixtures / 'session-guidance-0.10.5/retrospective.md'):
            for host in ('codex', 'claude', 'both'):
                for source in ('project', 'plugin'):
                    with self.subTest(fixture=fixture.name, host=host, source=source):
                        root = self.parent / (fixture.parent.name + fixture.stem + host + source)
                        initialize(root, host=host, skill_source=source)
                        path = root / '.novel-notebook/workflows/retrospective.md'
                        raw = _host_text(fixture.read_text(encoding='utf-8'), host, source).encode()
                        path.write_bytes(raw + b'Writer customized guidance')
                        before = snapshot(root)
                        preview = self.call(root)
                        self.assertEqual([entry['path'] for entry in preview['conflicts']],
                                         [path.relative_to(root).as_posix()])
                        self.assertEqual(snapshot(root), before)
                        path.write_bytes(raw)
                        (root / 'unrelated.txt').write_bytes(b'staged')
                        subprocess.run(['git', '-C', str(root), 'add', '--', 'unrelated.txt'], check=True)
                        index = (root / '.git/index').read_bytes()
                        story = (root / 'notebook/project.md').read_bytes()
                        preview = self.call(root)
                        path.write_bytes(raw + b'Changed after preview')
                        with self.assertRaises(ToolError):
                            self.call(root, preview)
                        path.write_bytes(raw)
                        self.call(root, self.call(root))
                        self.assertEqual((root / '.git/index').read_bytes(), index)
                        self.assertEqual((root / 'notebook/project.md').read_bytes(), story)
                        self.assertTrue(self.call(root)['already_current'])
                        self.assertIn('First review response and completion status', path.read_text(encoding='utf-8'))
        legacy = (Path(__file__).resolve().parents[2] / 'workflows/retrospective.md').read_text(encoding='utf-8')
        notebook = path.read_text(encoding='utf-8')
        for text in (legacy, notebook):
            for requirement in ('complete exact preview', 'without repeating approval',
                                'No action or declined', 'Equivalent issue', 'Blocked/manual',
                                'Uncertain creation/upload', 'observed receipts', 'connector_create', 'connector_receipt',
                                'Semantically compare', 'Never retry unknown creation blindly'):
                self.assertIn(requirement, text)
            evidence_review = text.split('## Local evidence and review', 1)[1]
            local_route = evidence_review.split('For the formal issue workflow', 1)[0]
            local_route = ' '.join(local_route.split())
            for requirement in ('writer requests local-only review', 'issue commands are unavailable',
                                'evidence the writer has selected', 'requested debugging state',
                                'Skip `retro issue begin` and `retro issue draft`'):
                self.assertIn(requirement, local_route)
            first_response = text.split('## First review response and completion status', 1)[1]
            first_response = first_response.split('## Exact sharing approval', 1)[0]
            first_response = ' '.join(first_response.split())
            for requirement in ('potential filing rationale', 'no evidenced problems', 'debugging state',
                                'exact outgoing approval'):
                self.assertIn(requirement, first_response)

    def test_duplicate_check_precedes_issue_suggestions(self):
        root = self.parent / 'early-duplicate-check'
        initialize(root)
        legacy = Path(__file__).resolve().parents[2] / 'workflows/retrospective.md'
        notebook = root / '.novel-notebook/workflows/retrospective.md'
        for path in (legacy, notebook):
            with self.subTest(path=path):
                workflow = path.read_text(encoding='utf-8')
                _, check = workflow.split('## Check existing GitHub issues', 1)
                check, draft = check.split('## Formal issue drafts', 1)
                draft, response = draft.split('## First review response and completion status', 1)
                response, _ = response.split('## Exact sharing approval', 1)
                for requirement in (
                    'once per retrospective', 'before drafting or suggesting',
                    'gh issue list --repo github.com/bjarkig82/novel-creator --state all --limit 100'
                    ' --json number,title,body,url',
                    'repo:bjarkig82/novel-creator is:issue', 'complete Markdown body',
                    'without sending private search terms', 'including paraphrases',
                    'skip all GitHub reads', 'permission to read public GitHub issues',
                ):
                    self.assertIn(requirement, check)
                self.assertIn('Only create new issue drafts for findings with no equivalent in the reviewed listing',
                              ' '.join(draft.split()))
                for requirement in ('existing issue URL', 'duplicate comparison pending',
                                    'do not recommend creating', 'no equivalent in the reviewed listing'):
                    self.assertIn(requirement, ' '.join(response.split()))

    def call(self, root, preview=None):
        return setup(SimpleNamespace(novel=root, apply=preview is not None,
                                     preview=None if preview is None else preview['preview_id'],
                                     expected_head=None if preview is None else preview['reviewed_head']))

    def old(self, name='old', host='codex', source='project', language='en', version='0.10.0'):
        root = self.parent / name
        initialize(root, host=host, skill_source=source, language=language)
        wheel = published_wheel(version)
        with zipfile.ZipFile(wheel) as archive:
            for name in ('conversation', 'debugging', 'help'):
                raw = archive.read('novel_creator/notebook_resources/workflows/' + name + '.md').decode()
                (root / '.novel-notebook/workflows' / (name + '.md')).write_text(_host_text(raw, host, source), encoding='utf-8')
        (root / '.novel-notebook/workflows/retrospective.md').unlink()
        for selected in (('codex', 'claude') if host == 'both' else (host,)):
            path = root / ('AGENTS.md' if selected == 'codex' else 'CLAUDE.md')
            text = path.read_text(encoding='utf-8').replace(_host_text(ROUTING, selected, source), OLD_ROOT)
            path.write_text(text, encoding='utf-8')
            skill = root / ('.agents' if selected == 'codex' else '.claude') / 'skills/novel-retro/SKILL.md'
            if skill.exists():
                skill.unlink()
        return root

    def test_previous_resources_all_host_source_language_combinations(self):
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                for language in ('en', 'is'):
                    with self.subTest(host=host, source=source, language=language):
                        root = self.old(host+'-'+source+'-'+language, host, source, language)
                        custom = b'\r\n## Writer custom bytes\r\nKeep this exact prose.\r\n'
                        names = ('AGENTS.md', 'CLAUDE.md') if host == 'both' else ('AGENTS.md' if host == 'codex' else 'CLAUDE.md',)
                        for name in names:
                            with (root/name).open('ab') as stream: stream.write(custom)
                        story = (root/'notebook/project.md').read_bytes()
                        index = (root/'.git/index').read_bytes()
                        preview = self.call(root)
                        self.assertTrue(preview['changes'])
                        self.assertTrue(self.call(root, preview)['applied'])
                        self.assertEqual((root/'notebook/project.md').read_bytes(), story)
                        self.assertEqual((root/'.git/index').read_bytes(), index)
                        for name in names:
                            self.assertIn(custom, (root/name).read_bytes())
                        if source == 'project':
                            self.assertTrue((root/('.claude' if host == 'claude' else '.agents')/'skills/novel-retro/SKILL.md').is_file())
                        else:
                            self.assertFalse((root/'.agents/skills').exists())
                        self.assertTrue(self.call(root)['already_current'])

    def test_released_0102_shared_guides_refresh_without_weakening_custom_protection(self):
        from tests.verify_plugin_install import snapshot
        frozen = Path(__file__).resolve().parents[1] / 'fixtures/session-guidance-0.10.2'
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                with self.subTest(host=host, source=source):
                    root = self.parent / ('released-' + host + '-' + source)
                    initialize(root, host=host, skill_source=source)
                    for name in ('conversation.md', 'debugging.md'):
                        path = root / '.novel-notebook/workflows' / name
                        path.write_text(_host_text((frozen / name).read_text(encoding='utf-8'), host, source), encoding='utf-8')
                    path = root / '.novel-notebook/workflows/debugging.md'
                    raw = path.read_bytes()
                    path.write_bytes(raw + b'Custom instructions.\n')
                    before = snapshot(root)
                    preview = self.call(root)
                    self.assertEqual([entry['path'] for entry in preview['conflicts']],
                                     [path.relative_to(root).as_posix()])
                    self.assertEqual(snapshot(root), before)
                    path.write_bytes(raw)
                    index = (root / '.git/index').read_bytes()
                    self.assertTrue(self.call(root, self.call(root))['applied'])
                    self.assertTrue(self.call(root)['already_current'])
                    self.assertEqual((root / '.git/index').read_bytes(), index)

    def test_released_0103_conversation_guide_can_be_explicitly_refreshed(self):
        self.assert_conversation_guide_refresh('0.10.3')

    def test_released_0105_conversation_guide_can_be_explicitly_refreshed(self):
        self.assert_conversation_guide_refresh('0.10.5')

    def assert_conversation_guide_refresh(self, version):
        from tests.verify_plugin_install import snapshot
        frozen = Path(__file__).resolve().parents[1] / f'fixtures/session-guidance-{version}/conversation.md'
        released = frozen.read_text(encoding='utf-8')
        relative = '.novel-notebook/workflows/conversation.md'
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                with self.subTest(host=host, source=source):
                    root = self.parent / f'continuation-{host}-{source}'
                    initialize(root, host=host, skill_source=source)
                    path = root / relative
                    expected = path.read_bytes()
                    original = _host_text(released, host, source).encode('utf-8')
                    path.write_bytes(original + b'\nWriter custom instruction.\n')
                    (root / 'notebook/project.md').write_bytes(
                        (root / 'notebook/project.md').read_bytes() + b'\nWriter project note.\n')
                    subprocess.run(['git', '-C', str(root), 'add', '--', 'notebook/project.md'], check=True)
                    before = snapshot(root, include_git=True)
                    preview = self.call(root)
                    self.assertEqual([entry['path'] for entry in preview['conflicts']], [relative])
                    self.assertEqual(preview['changes'], [])
                    self.assertFalse(preview['ready'])
                    self.assertFalse(preview['already_current'])
                    self.assertEqual(snapshot(root, include_git=True), before)

                    path.write_bytes(original)
                    before = snapshot(root, include_git=True)
                    preview = self.call(root)
                    self.assertEqual(preview['changes'], [relative])
                    self.assertEqual(snapshot(root, include_git=True), before)
                    self.assertTrue(self.call(root, preview)['applied'])
                    self.assertEqual(path.read_bytes(), expected)
                    after = snapshot(root, include_git=True)
                    self.assertEqual({name for name in before.keys() | after.keys()
                                      if before.get(name) != after.get(name)}, {relative})
                    self.assertTrue(self.call(root)['already_current'])

    def test_released_0104_resources_upgrade_to_live_snapshot_routing(self):
        from tests.verify_plugin_install import snapshot
        frozen = Path(__file__).resolve().parents[1] / 'fixtures/session-guidance-0.10.4'
        workflows = ('retrospective.md', 'conversation.md', 'debugging.md', 'help.md')
        for host in ('codex', 'claude', 'both'):
            for source in ('project', 'plugin'):
                with self.subTest(host=host, source=source):
                    root = self.parent / f'live-snapshot-{host}-{source}'
                    initialize(root, host=host, skill_source=source, language='is')
                    expected = {}

                    def previous(path, fixture, selected):
                        expected[path] = path.read_bytes()
                        return _host_text((frozen / fixture).read_text(encoding='utf-8'),
                                          selected, source).encode()

                    for name in workflows:
                        path = root / '.novel-notebook/workflows' / name
                        path.write_bytes(previous(path, name, host))
                    skills = []
                    for selected in (('codex', 'claude') if host == 'both' else (host,)):
                        path = root / ('AGENTS.md' if selected == 'codex' else 'CLAUDE.md')
                        old = previous(path, 'root-issue-retro.md', selected)
                        current = _host_text(ROUTING, selected, source).encode()
                        custom = b'\r\n## Writer custom bytes\r\nKeep this exact prose.\r\n'
                        original = expected[path]
                        self.assertIn(current, original)
                        # Keep a CRLF block between otherwise unchanged surrounding bytes.
                        path.write_bytes(original.replace(current, old.replace(b'\n', b'\r\n'), 1) + custom)
                        expected[path] = original.replace(current, current.replace(b'\n', b'\r\n'), 1) + custom
                        if source == 'project':
                            skill = root / ('.agents' if selected == 'codex' else '.claude') / 'skills/novel-retro/SKILL.md'
                            skill.write_bytes(previous(skill, 'novel-retro.skill.md', selected))
                            skills.append(skill)

                    staged = root / 'unrelated.txt'
                    staged.write_bytes(b'staged before setup')
                    subprocess.run(['git', '-C', str(root), 'add', '--', staged.name], check=True)
                    # Workflow conflicts are previewable. Customized root blocks and skills still raise.
                    retro = root / '.novel-notebook/workflows/retrospective.md'
                    raw = retro.read_bytes()
                    retro.write_bytes(raw + b'\nWriter customized instructions.\n')
                    before = snapshot(root, include_git=True)
                    preview = self.call(root)
                    self.assertEqual([entry['path'] for entry in preview['conflicts']],
                                     [retro.relative_to(root).as_posix()])
                    self.assertEqual(snapshot(root, include_git=True), before)
                    retro.write_bytes(raw)
                    for path in skills:
                        raw = path.read_bytes()
                        path.write_bytes(raw + b'\nWriter customized instructions.\n')
                        before = snapshot(root, include_git=True)
                        with self.assertRaisesRegex(ToolError, 'Customized'):
                            self.call(root)
                        self.assertEqual(snapshot(root, include_git=True), before)
                        path.write_bytes(raw)
                    path = root / ('CLAUDE.md' if host == 'claude' else 'AGENTS.md')
                    raw = path.read_bytes()
                    path.write_bytes(raw.replace(b'debugging before review', b'debugging before Writer review', 1))
                    before = snapshot(root, include_git=True)
                    with self.assertRaisesRegex(ToolError, 'Customized'):
                        self.call(root)
                    self.assertEqual(snapshot(root, include_git=True), before)
                    path.write_bytes(raw)

                    before = snapshot(root, include_git=True)
                    preview = self.call(root)
                    self.assertEqual(set(preview['changes']), {path.relative_to(root).as_posix() for path in expected})
                    self.assertEqual(snapshot(root, include_git=True), before)
                    self.assertTrue(self.call(root, preview)['applied'])
                    for path, data in expected.items():
                        self.assertEqual(path.read_bytes(), data)
                    after = snapshot(root, include_git=True)
                    self.assertEqual({name for name in before.keys() | after.keys()
                                      if before.get(name) != after.get(name)}, set(preview['changes']))
                    self.assertIn(b'--keep-debugging', retro.read_bytes())
                    self.assertTrue(self.call(root)['already_current'])

    def test_cli_previews_all_workflow_conflicts_without_applying_pending_changes(self):
        from tests.verify_plugin_install import snapshot
        frozen = Path(__file__).resolve().parents[1] / 'fixtures/session-guidance-0.10.4'
        root = self.parent / 'customized-guides'
        initialize(root, host='both', skill_source='plugin')
        workflow_dir = '.novel-notebook/workflows/'
        debug, help_guide, conversation = [workflow_dir + name + '.md'
                                           for name in ('debugging', 'help', 'conversation')]
        expected = {name: (root / name).read_bytes() for name in (debug, help_guide, conversation)}
        custom = b'\nWriter customized instructions.\n'
        for name in expected:
            old = _host_text((frozen / Path(name).name).read_text(encoding='utf-8'),
                             'both', 'plugin').encode()
            (root / name).write_bytes(old + custom if name != conversation else old)
        staged = root / 'unrelated.txt'
        staged.write_bytes(b'staged writer material')
        subprocess.run(['git', '-C', str(root), 'add', '--', help_guide, staged.name], check=True)
        staged.write_bytes(b'unstaged writer edit')

        def cli(*options):
            return subprocess.run([sys.executable, '-m', 'novel_creator', 'retro', 'issue',
                                   'setup', '--novel', str(root), '--json', *options],
                                  capture_output=True, text=True, encoding='utf-8')

        before = snapshot(root, include_git=True)
        result = cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        preview = json.loads(result.stdout)['data']
        self.assertFalse(preview['ready'])
        self.assertFalse(preview['already_current'])
        self.assertFalse(preview['applied'])
        self.assertEqual(preview['changes'], [conversation])
        self.assertEqual(preview['conflicts'], [
            {'path': name, 'replacement': expected[name].decode()} for name in (debug, help_guide)
        ])
        self.assertIn('`/novel-creator:novel-help`', preview['conflicts'][1]['replacement'])
        self.assertEqual(snapshot(root, include_git=True), before)

        options = ('--apply', '--preview', preview['preview_id'],
                   '--expected-head', preview['reviewed_head'])
        result = cli(*options)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(json.loads(result.stdout)['error']['affected_refs'], [debug, help_guide])
        self.assertEqual(snapshot(root, include_git=True), before)

        with (root / debug).open('ab') as stream:
            stream.write(b'A later customized instruction.\n')
        before = snapshot(root, include_git=True)
        result = cli(*options)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn('stale', json.loads(result.stdout)['error']['message'])
        self.assertEqual(snapshot(root, include_git=True), before)

        for conflict in preview['conflicts']:
            (root / conflict['path']).write_bytes(conflict['replacement'].encode())
        before = snapshot(root, include_git=True)
        fresh = json.loads(cli().stdout)['data']
        self.assertEqual(fresh['conflicts'], [])
        result = cli('--apply', '--preview', fresh['preview_id'],
                     '--expected-head', fresh['reviewed_head'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['data']['applied'])
        self.assertEqual((root / conversation).read_bytes(), expected[conversation])
        after = snapshot(root, include_git=True)
        self.assertEqual({name for name in before.keys() | after.keys()
                          if before.get(name) != after.get(name)}, {conversation})

    def test_published_0101_and_unrelated_staging_preserved(self):
        root = self.old(version='0.10.1')
        (root/'unrelated.txt').write_bytes(b'staged')
        subprocess.run(['git','-C',str(root),'add','--','unrelated.txt'],check=True)
        (root/'unrelated.txt').write_bytes(b'unstaged')
        index = (root/'.git/index').read_bytes()
        self.call(root, self.call(root))
        self.assertEqual((root/'.git/index').read_bytes(), index)
        self.assertEqual((root/'unrelated.txt').read_bytes(), b'unstaged')

    def test_custom_resources_root_blocks_stale_input_and_head_refuse(self):
        root = self.old()
        preview = self.call(root)
        path = root/'.novel-notebook/workflows/help.md'
        raw = path.read_bytes(); path.write_bytes(raw+b'Custom instruction')
        with self.assertRaises(ToolError): self.call(root, preview)
        self.assertEqual(path.read_bytes(), raw+b'Custom instruction')
        path.write_bytes(raw)
        (root/'AGENTS.md').write_bytes((root/'AGENTS.md').read_bytes()+b'\nLate custom bytes\n')
        with self.assertRaisesRegex(ToolError, 'stale'): self.call(root, preview)
        preview = self.call(root)
        subprocess.run(['git','-C',str(root),'commit','--allow-empty','-qm','later'],check=True)
        with self.assertRaisesRegex(ToolError, 'stale'): self.call(root, preview)
        text = (root/'AGENTS.md').read_text(encoding='utf-8')
        (root/'AGENTS.md').write_text(text+'\n<!-- novel-creator:issue-retro:start -->Custom\n',encoding='utf-8')
        with self.assertRaisesRegex(ToolError, 'conflicting'): self.call(root)

    def test_bad_markers_and_observed_hardlink_metadata_refuse(self):
        root = self.old()
        marker = root/'.novel-notebook/integration.json'
        marker.write_text(json.dumps(dict(version=True,host='codex',skill_source='project')))
        with self.assertRaisesRegex(ToolError, 'marker'): self.call(root)
        marker.unlink()
        original = Path.lstat
        def linked(path):
            value = original(path)
            if path == root/'AGENTS.md':
                return SimpleNamespace(st_mode=value.st_mode,st_nlink=2,st_file_attributes=0)
            return value
        with patch.object(Path,'lstat',linked):
            with self.assertRaisesRegex(ToolError, 'hard-linked'): self.call(root)

    def test_interruption_preserves_completed_resources_and_fresh_preview_resumes(self):
        root = self.old()
        preview = self.call(root)
        replace = __import__('os').replace
        def fail(source, target):
            raise OSError('synthetic interruption')
        with patch('novel_creator.retro_issue_setup.os.replace', fail):
            with self.assertRaises(ToolError) as raised: self.call(root, preview)
        self.assertTrue(raised.exception.data['partial'])
        self.assertTrue((root/'.novel-notebook/workflows/retrospective.md').is_file())
        self.call(root, self.call(root))
        self.assertTrue(self.call(root)['already_current'])

    def test_redirected_link_target_inside_root_is_not_resolved_away(self):
        root = self.old()
        target = root/'.novel-notebook/workflows/format.md'
        original = Path.lstat
        def redirected(path):
            value = original(path)
            if path == target:
                return SimpleNamespace(st_mode=value.st_mode,st_nlink=1,st_file_attributes=0x400)
            return value
        with patch.object(Path,'lstat',redirected):
            with self.assertRaisesRegex(ToolError, 'redirected'): self.call(root)

    def test_arbitrary_ignore_bytes_and_mixed_marker_debug_location_preserved(self):
        root = self.old()
        (root/'.gitignore').write_bytes(b'custom\xff\n')
        (root/'.novel-creator').mkdir()
        (root/'.novel-creator/manifest.json').write_bytes(b'legacy marker retained')
        self.call(root, self.call(root))
        self.assertTrue((root/'.gitignore').read_bytes().startswith(b'custom\xff\n'))
        self.assertEqual((root/'.novel-creator/manifest.json').read_bytes(),b'legacy marker retained')


    def test_current_crlf_root_block_is_preserved_and_idempotent(self):
        root = self.parent / 'crlf-current'
        initialize(root)
        path = root / 'AGENTS.md'
        raw = path.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n') + b'\r\nWriter exact custom bytes.\r\n'
        path.write_bytes(raw)
        preview = self.call(root)
        self.assertNotIn('AGENTS.md', preview['changes'])
        self.call(root, preview)
        self.assertEqual(path.read_bytes(), raw)
        self.assertTrue(self.call(root)['already_current'])

    def test_post_write_content_change_reports_partial_state(self):
        root = self.old()
        preview = self.call(root)
        import os
        replace = os.replace
        def changed(source, target):
            replace(source, target)
            Path(target).write_bytes(b'Unexpected concurrent bytes')
        with patch('novel_creator.retro_issue_setup.os.replace', changed):
            with self.assertRaises(ToolError) as raised:
                self.call(root, preview)
        self.assertTrue(raised.exception.data['partial'])

    def test_focused_update_and_issue_setup_supply_absent_passive_prerequisites(self):
        from novel_creator.notebook import update
        focused = self.old('focused-missing')
        review = update(focused)['data']
        update(focused, apply=True, preview_id=review['preview_id'], expected_head=review['reviewed_head'])
        self.assertTrue((focused / '.novel-notebook/workflows/retrospective.md').is_file())
        old = self.old('older-minimal')
        custom = old / '.novel-notebook/workflows/research.md'
        custom.write_bytes(b'Writer custom research guide')
        for name in ('agents','character-development','analyze','clarify','manuscript','review','format'):
            (old / '.novel-notebook/workflows' / (name + '.md')).unlink(missing_ok=True)
        self.call(old, self.call(old))
        self.assertTrue(self.call(old)['already_current'])
        self.assertEqual(custom.read_bytes(), b'Writer custom research guide')
        self.assertTrue((old / '.novel-notebook/workflows/agents.md').is_file())

    def test_debug_setup_adds_only_missing_passive_retro_snapshot(self):
        from novel_creator import debug
        root = self.old('pre-debug')
        (root / '.novel-notebook/workflows/debugging.md').unlink()
        result = debug.setup(root)
        self.assertTrue(result['ready'])
        retrospective = root / '.novel-notebook/workflows/retrospective.md'
        self.assertTrue(retrospective.is_file())
        self.assertFalse((root / '.agents/skills/novel-retro/SKILL.md').exists())
        retrospective.write_bytes(b'Writer custom retrospective guide')
        debug.setup(root)
        self.assertEqual(retrospective.read_bytes(), b'Writer custom retrospective guide')

    def test_known_manual_session_routing_refreshes_and_custom_block_refuses(self):
        from novel_creator.retro_issue_setup import SESSION_BLOCKS, SESSION_ROUTING
        root = self.old('manual-routing')
        path = root / 'AGENTS.md'
        with path.open('ab') as stream:
            stream.write(b'\n' + SESSION_BLOCKS[0].encode() + b'\n')
        self.call(root, self.call(root))
        self.assertIn(SESSION_ROUTING.encode(), path.read_bytes())
        self.assertNotIn(SESSION_BLOCKS[0].encode(), path.read_bytes())
        # Actual custom changes inside a product block must refuse before writes.
        raw = path.read_bytes().replace(b'Exact outgoing', b'Custom outgoing')
        path.write_bytes(raw)
        with self.assertRaisesRegex(ToolError, 'conflicting session'):
            self.call(root)
