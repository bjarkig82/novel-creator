"""Format-specific focused methods must ship in legacy updates too."""
import re
from pathlib import PurePosixPath
import unittest

from novel_creator.install import bundle_files
from novel_creator.update_release import export_bundle


class LegacyFocusedMethods(unittest.TestCase):
    def test_exported_update_inventory_contains_linked_legacy_methods(self):
        import base64
        resources = bundle_files()
        exported = {name: base64.b64decode(raw) for name, raw in export_bundle()['files'].items()}
        for method in ('clarify', 'analyze', 'help'):
            skill = f'.agents/skills/novel-{method}/SKILL.md'
            workflow = f'.novel-creator/workflows/{method}.md'
            self.assertEqual(resources[skill], exported[skill])
            self.assertEqual(resources[workflow], exported[workflow])
            self.assertNotIn(b'.novel-notebook/', resources[skill])
            self.assertNotIn(b'notebook/project.md', resources[workflow])
            for source in (skill, workflow):
                for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', resources[source].decode()):
                    parts = []
                    for part in (PurePosixPath(source).parent / link).parts:
                        if part == '..':
                            parts.pop()
                        elif part != '.':
                            parts.append(part)
                    self.assertIn('/'.join(parts), resources, (source, link))

    def test_analysis_help_exceptions_are_explicit_before_capture(self):
        resources = bundle_files()
        entry = resources['.novel-creator/workflows/entry.md'].decode()
        self.assertLess(entry.index('## Read-only analysis and help exception'),
                        entry.index('## Exact current legacy input'))
        for name in ('analyze', 'help'):
            workflow = resources[f'.novel-creator/workflows/{name}.md'].decode()
            skill = resources[f'.agents/skills/novel-{name}/SKILL.md'].decode()
            self.assertIn('strictly read-only', workflow)
            self.assertIn('strictly read-only', skill)
            self.assertIn('before capture', skill)
            self.assertIn('`-I -B`', workflow)
            self.assertIn('NOVEL_CREATOR_VALIDATION_KEY_FILE', workflow)
        clarify = resources['.novel-creator/workflows/clarify.md'].decode()
        self.assertIn('save-before-display', clarify)
        self.assertIn('No manuscript', clarify)

    def test_documented_read_only_subprocess_does_not_create_project_files_or_cache(self):
        import json
        import os
        import subprocess
        import sys
        from novel_creator import records, storage
        from tests.helpers import repository, envelope, seal
        from tests.update_helpers import snapshot
        with repository() as root:
            first = envelope(root)
            first['record_versions'] = [records.project_from_brief({}, first, 'unused')]
            storage.save(root, seal(first))
            # The pass explicitly omits optional cache configuration from its
            # child environment; a configured parent must not enable writes.
            environment = dict(os.environ, NOVEL_CREATOR_VALIDATION_KEY_FILE=str(root.parent / 'unused-cache-key'))
            environment.pop('NOVEL_CREATOR_VALIDATION_KEY_FILE')
            before = snapshot(root)
            code = 'import json,sys; from novel_creator.context import read; print(json.dumps(read(sys.argv[1], view="working")))'
            result = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(root)],
                                    env=environment, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)['ok'])
            self.assertEqual(snapshot(root), before)
            self.assertFalse((root / '.novel-creator/local/cache').exists())
