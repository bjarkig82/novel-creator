"""Host layouts remain independent notebooks with resolvable project resources."""
import json
from pathlib import Path
import re
import subprocess
import unittest

from novel_creator.cli import ToolError
from novel_creator.notebook import initialize, update
from tests.integration import test_notebook_init


class NotebookHosts(unittest.TestCase):
    setUp = test_notebook_init.NotebookInitialization.setUp

    def test_host_and_delivery_matrix_preserves_language_history_and_links(self):
        for language in ('en', 'is'):
            for host in ('codex', 'claude', 'both'):
                for source in ('project', 'plugin'):
                    with self.subTest(language=language, host=host, source=source):
                        target = self.parent / f'Bréf Þóru {language} {host} {source}'
                        result = initialize(target, language=language, host=host, skill_source=source)
                        self.assertEqual((result['data']['host'], result['data']['skill_source']), (host, source))
                        self.assertEqual((target / 'AGENTS.md').exists(), host in ('codex', 'both'))
                        self.assertEqual((target / 'CLAUDE.md').exists(), host in ('claude', 'both'))
                        self.assertEqual(len(list((target / '.codex/agents').glob('*.toml'))),
                                         6 if host in ('codex', 'both') else 0)
                        agents = list((target / '.claude/agents').glob('*.md'))
                        self.assertEqual(len(agents), 6 if host in ('claude', 'both') else 0)
                        for agent in agents:
                            self.assertIn(f'name: {agent.stem}\n', agent.read_text())
                            self.assertIn('disclose unavailable capabilities', agent.read_text())
                            self.assertIn('You are ' + agent.stem, agent.read_text())
                        for directory, selected in (('.agents', host in ('codex', 'both')),
                                                    ('.claude', host in ('claude', 'both'))):
                            skills = list((target / directory / 'skills').glob('*/SKILL.md'))
                            self.assertEqual(len(skills), 14 if source == 'project' and selected else 0)
                        for path in target.rglob('*'):
                            if path.is_file() and path.suffix in ('.md', '.toml'):
                                for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text()):
                                    if not re.match(r'[a-z]+:', link):
                                        self.assertTrue((path.parent / link).is_file(), (path, link))
                        roles = (target / '.novel-notebook/workflows/agents.md').read_text()
                        if host in ('claude', 'both'):
                            self.assertIn('`novel-scene-writer`', roles)
                        help_text = (target / '.novel-notebook/workflows/help.md').read_text()
                        self.assertIn('Help is strictly read-only', help_text)
                        if host in ('claude', 'both'):
                            expected = '/novel-creator:novel-clarify' if source == 'plugin' else '/novel-clarify'
                            self.assertIn(expected, help_text)
                        if source == 'plugin':
                            self.assertNotIn('`.agents/skills/`', help_text)
                            self.assertIn('actually enabled `novel-creator` plugin skills', help_text)
                        if host == 'both' and source == 'plugin':
                            self.assertIn('$novel-creator:novel-clarify', help_text)
                        project = (target / 'notebook/project.md').read_text()
                        self.assertEqual(json.loads(project.split('```json\n')[1].split('```')[0])['language'], language)
                        self.assertEqual(subprocess.check_output(['git', '-C', str(target), 'status', '--porcelain']), b'')

    def test_update_refuses_nondefault_integrations_without_changes(self):
        for host, source in (('both', 'plugin'), ('claude', 'project'), ('codex', 'plugin')):
            with self.subTest(host=host, source=source):
                target = self.parent / f'{host}-{source}'
                initialize(target, host=host, skill_source=source)
                # Unknown or damaged marker content is still protected.
                (target / '.novel-notebook/integration.json').write_text('{unexpected')
                before = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
                with self.assertRaisesRegex(ToolError, 'does not support host/plugin'):
                    update(target)
                after = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
                self.assertEqual(before, after)

    def test_invalid_host_options_do_not_claim_destination(self):
        for kwargs in ({'host': 'other'}, {'skill_source': 'other'}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ToolError):
                    initialize(self.target, **kwargs)
                self.assertFalse(self.target.exists())
