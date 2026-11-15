"""Candidate notebook failures cannot masquerade as historical compatibility."""
import io
import os
import unittest
import zipfile
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from tests import verify_package_install


class NotebookPackageVerifierTest(unittest.TestCase):
    def test_previous_notebook_inventory_is_exact_for_each_historical_target(self):
        from tests.verify_previous_release import notebook_resource_paths

        clarify = {'.agents/skills/novel-clarify/SKILL.md',
                   '.novel-notebook/workflows/clarify.md'}
        character = {'.agents/skills/novel-character-develop/SKILL.md',
                     '.novel-notebook/workflows/character-development.md',
                     '.novel-notebook/workflows/help.md'}
        side = {'.agents/skills/novel-side-character/SKILL.md',
                '.novel-notebook/workflows/side-character.md'}
        retro = '.novel-notebook/workflows/retrospective.md'
        for version in ('0.7.2', '0.8.0', '0.9.0', '0.10.1', '0.10.2'):
            expected = clarify.copy()
            if version in ('0.9.0', '0.10.1', '0.10.2'):
                expected |= character
            if version == '0.10.2':
                expected |= side | {retro}
            with self.subTest(version=version):
                paths = notebook_resource_paths(version, {})
                self.assertEqual(set(paths), expected)
                self.assertEqual(paths['.agents/skills/novel-clarify/SKILL.md'],
                                 'novel_creator/codex/notebook/skills/novel-clarify/SKILL.md')
                self.assertEqual(paths['.novel-notebook/workflows/clarify.md'],
                                 'novel_creator/notebook_resources/workflows/clarify.md')
                self.assertEqual(set(notebook_resource_paths(version, {retro: b'Writer version'})),
                                 expected - {retro})

    def test_previous_notebook_delivery_requires_exact_bytes_inventory_routing_and_local_links(self):
        from tests.verify_previous_release import check_notebook_delivery

        root_template = (b'# Current root\n## Character development\nCurrent character routing.\n'
                         b'<!-- novel-creator:side-character:start -->\n'
                         b'## Side-character profiles\n[Side](.novel-notebook/workflows/side-character.md)\n'
                         b'<!-- novel-creator:side-character:end -->\n')
        expected = {
            '.agents/skills/novel-character-develop/SKILL.md': b'[Character](../../../.novel-notebook/workflows/character-development.md)\n',
            '.novel-notebook/workflows/character-development.md': b'Current character workflow\n',
            '.novel-notebook/workflows/side-character.md': b'[Issue](https://github.com/example/issues/new#details)\n[Local](retrospective.md#review)\n',
            '.novel-notebook/workflows/retrospective.md': b'Passive retrospective guidance\n',
        }
        before = {'AGENTS.md': b'# Writer custom root\r\n',
                  'notebook/story.md': b'Accepted writer content\n',
                  '.novel-notebook/workflows/character-development.md': b'Old character workflow\n'}
        after = dict(before, **expected)
        after['AGENTS.md'] = before['AGENTS.md'] + b'\n## Character development' + root_template.split(
            b'## Character development', 1)[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()

            def write(snapshot):
                for path in root.rglob('*'):
                    if path.is_file():
                        path.unlink()
                for name, raw in snapshot.items():
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(raw)

            write(after)
            check_notebook_delivery(root, before, expected, root_template)
            mutations = {
                'unrelated write': dict(after, **{'notebook/story.md': b'Rewritten story'}),
                'extra resource': dict(after, **{'.novel-notebook/workflows/arbitrary.md': b'Extra'}),
                'wrong bytes': dict(after, **{'.novel-notebook/workflows/retrospective.md': b'Wrong'}),
                'missing local link': {name: raw for name, raw in after.items()
                                       if name != '.novel-notebook/workflows/retrospective.md'},
                'custom root lost': dict(after, **{'AGENTS.md': root_template}),
                'wrong managed routing': dict(after, **{'AGENTS.md': after['AGENTS.md'].replace(
                    b'Current character routing.', b'Wrong character routing.')}),
            }
            for label, snapshot in mutations.items():
                with self.subTest(label=label):
                    write(snapshot)
                    with self.assertRaises(AssertionError):
                        check_notebook_delivery(root, before, expected, root_template)
            # A local link must resolve even when it points to an unchanged file.
            broken = dict(expected)
            broken['.novel-notebook/workflows/side-character.md'] = b'[Local](missing.md)\n'
            write(dict(after, **broken))
            with self.assertRaises(AssertionError):
                check_notebook_delivery(root, before, broken, root_template)

    def test_previous_release_probe_is_gated_to_newer_stable_versions(self):
        from tests.verify_previous_release import applies, verify

        for version in ('0.7.0', 'novel-creator 0.7.1', '0.7.2rc1', 'invalid'):
            with self.subTest(version=version):
                self.assertFalse(applies(version))
                with patch('tests.verify_previous_release._source') as source:
                    with self.assertRaisesRegex(ValueError, 'newer stable'):
                        verify(None, None, None, None, version, None)
                    source.assert_not_called()
        self.assertTrue(applies('novel-creator 0.7.2'))

    def test_previous_release_source_requires_the_frozen_public_wheel_digest(self):
        from tests.verify_previous_release import checked_source

        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            checked_source(b'A rebuilt or corrupted historical archive')

    def test_prior_probe_rejects_same_version_wheel_with_different_product_resources(self):
        import hashlib
        import json
        from tests.verify_previous_release import check_target_inventory

        product = {'novel_creator/__init__.py': b'__version__ = "0.7.2"\n',
                   'novel_creator/notebook_resources/workflows/clarify.md': b'Installed custom answer guidance\n'}
        installed = {name: hashlib.sha256(raw).hexdigest() for name, raw in product.items()}
        with tempfile.TemporaryDirectory() as directory:
            wheel = Path(directory) / 'novel_creator-0.7.2-py3-none-any.whl'
            for mismatch in (False, True):
                with self.subTest(mismatch=mismatch):
                    with zipfile.ZipFile(wheel, 'w') as archive:
                        archive.writestr('novel_creator-0.7.2.dist-info/METADATA',
                                         'Name: novel-creator\nVersion: 0.7.2\n')
                        for name, raw in product.items():
                            archive.writestr(name, b'Divergent same-version guidance\n'
                                             if mismatch and name.endswith('clarify.md') else raw)
                    with patch('tests.verify_previous_release._run', return_value=json.dumps(installed)) as probe:
                        if mismatch:
                            with self.assertRaisesRegex(ValueError, 'inventory differs'):
                                check_target_inventory('installed-python', wheel, '0.7.2', cwd=directory, env={})
                        else:
                            self.assertEqual(check_target_inventory('installed-python', wheel, '0.7.2',
                                                                    cwd=directory, env={}), 2)
                        self.assertEqual(probe.call_args.args[0][:4], ['installed-python', '-I', '-B', '-c'])

    def test_public_050_uses_approved_wheel_resources_and_current_stays_source_strict(self):
        from novel_creator.notebook import initialize
        from tests.notebook_resource_checks import resource_paths, verify_writing_resources

        checkout = Path(__file__).resolve().parents[2]
        paths = resource_paths(checkout)
        current = {relative: source.read_bytes() for relative, (source, _) in paths.items()}
        # Explicit historical layout, not a copy of the expanding current set.
        historical_paths = {'AGENTS.md'}
        historical_paths.update(f'.codex/agents/{name}.toml' for name in (
            'novel_orchestrator', 'novel_brainstormer', 'novel_researcher',
            'novel_scene_writer', 'novel_chapter_writer', 'novel_reviewer'))
        historical_paths.update(f'.agents/skills/novel-{name}/SKILL.md' for name in (
            'outline', 'book-idea', 'premise', 'character', 'plot', 'setting',
            'agent', 'research', 'scene', 'chapter', 'review'))
        historical_paths.update(f'.novel-notebook/workflows/{name}.md' for name in (
            'conversation', 'format', 'outline', 'brainstorming', 'agents',
            'manuscript', 'research', 'review'))
        self.assertEqual(len(historical_paths), 26)
        current_paths = historical_paths | {
            f'.agents/skills/novel-{name}/SKILL.md' for name in (
                'character-develop', 'clarify', 'analyze', 'help', 'retro', 'side-character')
        } | {
            f'.novel-notebook/workflows/{name}.md' for name in (
                'character-development', 'clarify', 'analyze', 'help', 'debugging',
                'retrospective', 'side-character')
        }
        self.assertEqual(len(current), 39)
        self.assertEqual(set(current), current_paths)
        historical = {relative: current[relative] for relative in historical_paths}
        historical['.codex/agents/novel_brainstormer.toml'] = (
            b'name = "novel_brainstormer"\ndescription = "Historical fixture"\n'
            b'developer_instructions = "Read [format](../../.novel-notebook/workflows/format.md)."\n')
        historical['.agents/skills/novel-character/SKILL.md'] = (
            b'---\nname: novel-character\ndescription: Historical character fixture\n---\n'
            b'Read [brainstorming](../../../.novel-notebook/workflows/brainstorming.md).\n')
        # Minimal historical guidance fixtures cannot link to future workflows.
        # The approved fixture bytes must still be checked exactly on install.
        for relative in ('AGENTS.md', '.novel-notebook/workflows/conversation.md',
                         '.novel-notebook/workflows/agents.md', '.novel-notebook/workflows/review.md',
                         '.novel-notebook/workflows/brainstorming.md'):
            historical[relative] = b'# Historical 0.5.0 guidance fixture.\n'
        archive_bytes = io.BytesIO()
        with zipfile.ZipFile(archive_bytes, 'w') as archive:
            for relative, raw in historical.items():
                archive.writestr(paths[relative][1], raw)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / 'historical'
            with patch.dict(os.environ, GIT_AUTHOR_NAME='Package verifier test',
                            GIT_AUTHOR_EMAIL='test@example.invalid', GIT_COMMITTER_NAME='Package verifier test',
                            GIT_COMMITTER_EMAIL='test@example.invalid'):
                initialize(root, title='Historical resource fixture', language='en')
            for relative in current.keys() - historical.keys():
                (root / relative).unlink()
            for relative, raw in historical.items():
                (root / relative).write_bytes(raw)

            def resource_check(console, scratch, env, language, expected_resources=None):
                return verify_writing_resources(root, current if expected_resources is None else expected_resources)

            with patch('tests.verify_wheel.verify_notebook', side_effect=resource_check) as probe:
                verified = verify_package_install.verify_notebook_install(
                    'console', root.parent, {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0',
                    verified_wheel=archive_bytes.getvalue())
                self.assertEqual(verified, [26, 26])
                self.assertEqual(probe.call_count, 2)
                for package, version in ((None, '0.5.0'), (None, '0.6.0'),
                                         ('novel-creator==0.6.0', '0.6.0')):
                    with self.subTest(package=package, version=version), self.assertRaisesRegex(AssertionError, 'AGENTS.md'):
                        verify_package_install.verify_notebook_install(
                            'console', root.parent, {}, package, 'novel-creator ' + version,
                            verified_wheel=archive_bytes.getvalue())
                for relative, raw in current.items():
                    (root / relative).write_bytes(raw.replace(b'\r\n', b'\n'))
                for package in (None, 'novel-creator==0.6.0'):
                    self.assertEqual([len(current), len(current)], verify_package_install.verify_notebook_install(
                        'console', root.parent, {}, package, 'novel-creator 0.6.0',
                        verified_wheel=archive_bytes.getvalue()))
                # Current checks must require every newly introduced resource.
                for relative in set(current) - set(historical):
                    resource = root / relative
                    raw = resource.read_bytes()
                    resource.unlink()
                    for package in (None, 'novel-creator==0.6.0'):
                        with self.subTest(package=package, missing=relative), self.assertRaises(FileNotFoundError):
                            verify_package_install.verify_notebook_install(
                                'console', root.parent, {}, package, 'novel-creator 0.6.0',
                                verified_wheel=archive_bytes.getvalue())
                    resource.write_bytes(raw)
                # Historical checks still require the exact approved bytes.
                with self.assertRaisesRegex(AssertionError, 'AGENTS.md'):
                    verify_package_install.verify_notebook_install(
                        'console', root.parent, {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0',
                        verified_wheel=archive_bytes.getvalue())

    def test_public_050_missing_required_archive_resource_fails_closed(self):
        archive_bytes = io.BytesIO()
        with zipfile.ZipFile(archive_bytes, 'w') as archive:
            archive.writestr('unrelated.txt', b'Not a notebook resource')
        with patch('tests.verify_wheel.verify_notebook') as probe:
            with self.assertRaises(KeyError):
                verify_package_install.verify_notebook_install(
                    'console', 'scratch', {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0',
                    verified_wheel=archive_bytes.getvalue())
            probe.assert_not_called()

    def test_public_050_missing_approved_wheel_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'hash-verified wheel'):
            verify_package_install.verify_notebook_install(
                'console', 'scratch', {}, 'novel-creator==0.5.0', 'novel-creator 0.5.0')

    def test_memory_candidates_cannot_skip_as_historical_versions(self):
        with patch('tests.verify_wheel.verify_context_views', side_effect=RuntimeError('missing memory')) as probe:
            for version, package in [('0.5.0', None), ('0.6.0', None),
                                     ('0.6.0', 'novel-creator==0.6.0')]:
                with self.subTest(version=version, package=package), self.assertRaisesRegex(RuntimeError, 'missing memory'):
                    verify_package_install.verify_memory_install(
                        'python', 'launcher', 'novel', 'scratch', {}, package, version)
            self.assertEqual(probe.call_count, 3)

    def test_memory_only_known_matching_public_releases_skip(self):
        with patch('tests.verify_wheel.verify_context_views', return_value={'working': True}) as probe:
            for version in ('0.1.0', '0.2.0', '0.3.0', '0.4.0', '0.4.1', '0.5.0'):
                self.assertFalse(verify_package_install.verify_memory_install(
                    'python', 'launcher', 'novel', 'scratch', {},
                    'novel-creator==' + version, 'novel-creator ' + version)['working_views_available'])
            probe.assert_not_called()
            for package, version in [('novel-creator==0.5.0', '0.6.0'), ('other==0.5.0', '0.5.0')]:
                self.assertEqual({'working': True}, verify_package_install.verify_memory_install(
                    'python', 'launcher', 'novel', 'scratch', {}, package, version))
            self.assertEqual(probe.call_count, 2)

    def test_notebook_resources_keep_lf_in_autocrlf_checkout(self):
        checkout = Path(__file__).resolve().parents[2]
        resources = [path.relative_to(checkout) for path in (checkout / 'notebook').rglob('*')
                     if path.is_file() and path.suffix in ('.md', '.py')]
        self.assertTrue(resources)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'config', 'core.autocrlf', 'true'], check=True)
            (root / '.gitattributes').write_bytes((checkout / '.gitattributes').read_bytes())
            for relative in resources:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'first line\nsecond line\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True, capture_output=True)
            for relative in resources:
                (root / relative).unlink()
            subprocess.run(['git', '-C', str(root), 'checkout-index', '--all', '--force'], check=True)
            for relative in resources:
                with self.subTest(resource=relative):
                    self.assertEqual((root / relative).read_bytes(), b'first line\nsecond line\n')

    def test_candidate_requires_notebook_even_at_historical_version(self):
        with patch('tests.verify_wheel.verify_notebook', side_effect=RuntimeError('missing route')) as probe:
            with self.assertRaisesRegex(RuntimeError, 'missing route'):
                verify_package_install.verify_notebook_install('console', 'scratch', {}, None, 'novel-creator 0.3.0')
            probe.assert_called_once()

    def test_nonhistorical_public_failure_is_not_skipped(self):
        with patch('tests.verify_wheel.verify_notebook', side_effect=RuntimeError('broken route')) as probe:
            with self.assertRaisesRegex(RuntimeError, 'broken route'):
                verify_package_install.verify_notebook_install('console', 'scratch', {}, 'novel-creator==0.4.0', 'novel-creator 0.4.0')
            probe.assert_called_once()

    def test_only_known_public_releases_skip(self):
        with patch('tests.verify_wheel.verify_notebook') as probe:
            for version in ('0.1.0', '0.2.0', '0.3.0'):
                self.assertEqual([], verify_package_install.verify_notebook_install(
                    'console', 'scratch', {}, 'novel-creator==' + version, 'novel-creator ' + version))
            probe.assert_not_called()

    def test_supported_candidate_checks_both_languages(self):
        with patch('tests.verify_wheel.verify_notebook', side_effect=lambda *args: args[-1]) as probe:
            self.assertEqual(['en', 'is'], verify_package_install.verify_notebook_install(
                'console', 'scratch', {}, None, 'novel-creator 0.3.0'))
            self.assertEqual(2, probe.call_count)
