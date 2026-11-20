"""Release CI keeps both frozen notebook sources and installed artifact paths."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from importlib.resources import files
import re

from tests import verify_marketplace_previous as previous
from tests.verify_plugin_install import temporary_environment, run
from tests import feature_upgrade_checks as features


class MarketplacePreviousTests(unittest.TestCase):
    def test_legacy_routing_rejects_corrupted_root_entry_and_missing_target(self):
        with tempfile.TemporaryDirectory(prefix='previous-legacy-routing-') as temporary:
            root = Path(temporary).resolve()
            resources = {'AGENTS.md': files('novel_creator.codex').joinpath('AGENTS.production.md').read_bytes(),
                         '.novel-creator/workflows/entry.md': files('novel_creator.workflows').joinpath('entry.md').read_bytes().replace(b'\r\n', b'\n')}
            for name, raw in resources.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', raw.decode()):
                    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link):
                        target = path.parent / link
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.touch(exist_ok=True)
            features.check_legacy_routing(root, fresh_root=True)
            for name, raw in resources.items():
                with self.subTest(resource=name):
                    (root / name).write_bytes(raw + b'Corrupt routing\n')
                    with self.assertRaisesRegex(AssertionError, 'routing bytes'):
                        features.check_legacy_routing(root, fresh_root=True)
                    (root / name).write_bytes(raw)
            # A preserved custom root is valid on explicit updates; its managed
            # entry still has to match the installed artifact and resolve links.
            (root / 'AGENTS.md').write_bytes(b'Writer-owned instructions\n')
            features.check_legacy_routing(root)
            target = root / '.novel-creator/workflows/side-character.md'
            target.unlink()
            with self.assertRaisesRegex(AssertionError, 'routing link'):
                features.check_legacy_routing(root)

    def test_both_public_sources_fail_closed_on_a_corrupt_local_wheel(self):
        self.assertEqual(set(previous.PUBLIC_WHEELS), {'0.7.2', '0.8.0', '0.9.0', '0.10.0', '0.10.1', '0.10.2', '0.10.3', '0.10.4'})
        self.assertEqual(previous.PUBLIC_WHEELS['0.10.4'][1],
                         'dc5988f53929ae2783169408fcab35e21305123434b305735a6ea6e38bf2bad3')
        self.assertEqual(previous.PUBLIC_WHEELS['0.10.3'][1],
                         'c29f36dad95f8289a9a2b19d0d0fe3246d8a6c2c2d2860bd736c2b981c6629f9')
        self.assertEqual(previous.PUBLIC_WHEELS['0.10.1'][1],
                         '6721c5a527f1b7e567743f2760ec5e13aec2d0394f520913e98589ac54b8b11a')
        self.assertEqual(previous.PUBLIC_WHEELS['0.8.0'][1],
                         '390c6e208fe71a803783cd2cf979bada3e20988518a0032572fcf9a1b8711c5b')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / 'corrupt.whl'
            wheel.write_bytes(b'Untrusted rebuilt historical product')
            for version in previous.PUBLIC_WHEELS:
                with self.subTest(version=version), self.assertRaisesRegex(AssertionError, 'SHA-256 mismatch'):
                    previous.previous_wheel(root, wheel, version=version)

    def test_ci_probe_runs_both_sources_against_both_candidate_artifacts(self):
        with (patch('sys.argv', ['probe', '--wheel', 'candidate.whl', '--sdist', 'candidate.tar.gz',
                                 '--report', 'report.json']),
              patch.object(previous, 'verify', return_value={'ok': True}) as verify,
              patch.object(previous, 'write_report') as report):
            previous.main()
        self.assertEqual([(call.kwargs['source_version'], call.kwargs['sdist'] is not None)
                          for call in verify.call_args_list],
                         [('0.7.2', False), ('0.7.2', True), ('0.8.0', False), ('0.8.0', True),
                          ('0.9.0', False), ('0.9.0', True), ('0.10.0', False), ('0.10.0', True),
                          ('0.10.1', False), ('0.10.1', True), ('0.10.2', False), ('0.10.2', True),
                          ('0.10.3', False), ('0.10.3', True),
                          ('0.10.4', False), ('0.10.4', True)])
        self.assertEqual(len(report.call_args.args[1]['checks']), 16)
        workflow = (Path(__file__).resolve().parents[2] / '.github/workflows/package-release.yml').read_text()
        self.assertIn('tests/verify_marketplace_previous.py --wheel candidate/*.whl --sdist candidate/*.tar.gz', workflow)

    def test_default_inventory_is_exact_and_bound_to_target_and_source(self):
        original = {'AGENTS.md', '.agents/skills/novel-character-develop/SKILL.md',
                    '.novel-notebook/workflows/character-development.md',
                    '.novel-notebook/workflows/help.md'}
        side = {'.agents/skills/novel-side-character/SKILL.md',
                '.novel-notebook/workflows/side-character.md'}
        retro = '.novel-notebook/workflows/retrospective.md'
        self.assertEqual(previous.default_update_inventory('0.10.1', '0.8.0', {}), original)
        self.assertEqual(previous.default_update_inventory('0.10.2', '0.8.0', {}), original | side | {retro})
        self.assertEqual(previous.default_update_inventory('0.10.2', '0.10.0', {retro: 'old'}),
                         {'AGENTS.md', '.novel-notebook/workflows/character-development.md',
                          '.novel-notebook/workflows/help.md'} | side)
        self.assertEqual(previous.default_update_inventory('0.10.2', '0.10.1', {retro: 'old'}),
                         {'AGENTS.md', '.novel-notebook/workflows/help.md'} | side)
        self.assertNotIn('.novel-notebook/workflows/arbitrary.md',
                         previous.default_update_inventory('0.10.2', '0.8.0', {}))

    def test_local_latest_public_fixture_flag_is_forwarded_for_both_artifacts(self):
        with (patch('sys.argv', ['probe', '--wheel', 'candidate.whl', '--sdist', 'candidate.tar.gz',
                                 '--previous-0104-wheel', 'frozen.whl', '--report', 'report.json']),
              patch.object(previous, 'verify', return_value={'ok': True}) as verify,
              patch.object(previous, 'write_report')):
            previous.main()
        latest = [call for call in verify.call_args_list if call.kwargs['source_version'] == '0.10.4']
        self.assertEqual(len(latest), 2)
        self.assertTrue(all(call.kwargs['previous'] == Path('frozen.whl') for call in latest))

    def test_0102_dispatch_uses_session_procedure_and_actual_legacy_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            wheel = Path(temporary) / 'candidate.whl'
            wheel.write_bytes(b'candidate')
            runtime = {'runtime_python': 'private-python', 'version': '0.10.3',
                       'verified_product_files': 42}
            with (patch.object(previous, 'candidate_runtime', return_value=runtime),
                  patch.object(previous, 'install_previous', return_value=('old-product', 'old-cli')),
                  patch.object(previous, 'previous_wheel', return_value=wheel),
                  patch.object(previous, 'verify_session_upgrade', return_value=['sessions']) as session,
                  patch.object(previous, 'verify_feature_upgrade') as feature,
                  patch.object(previous, 'verify_debug_legacy', return_value={'ok': True}) as legacy):
                report = previous.verify(plugin=Path('plugin'), wheel=wheel, previous=wheel,
                                         source_version='0.10.2')
            self.assertEqual(session.call_args.kwargs, {'source_version': '0.10.2'})
            self.assertEqual(legacy.call_args.kwargs, {'source_version': '0.10.2'})
            self.assertEqual(report['notebooks'], ['sessions'])
            self.assertEqual(report['source_sha256'],
                             '24117c4c17c7a56a981edbf1852440bbca94f668ea4f4fdf9aef4b940a000659')
            feature.assert_not_called()

    def test_new_legacy_fixture_owns_identity_despite_valid_ambient_identity(self):
        with tempfile.TemporaryDirectory(prefix='previous-legacy-identity-') as temporary:
            scratch = Path(temporary).resolve()
            env = temporary_environment(scratch)
            # This ambient identity is valid but intentionally differs from the
            # repository identity required by the production initializer.
            env.update(GIT_AUTHOR_NAME='Ambient Test Author', GIT_AUTHOR_EMAIL='ambient@example.invalid',
                       GIT_COMMITTER_NAME='Ambient Test Committer', GIT_COMMITTER_EMAIL='ambient@example.invalid')
            for language in ('en', 'is'):
                with self.subTest(language=language):
                    book = scratch / ('New legacy ' + language)
                    previous.initialize_legacy_fixture(sys.executable, book, language, scratch, env)
                    # --local cannot be satisfied by developer/global config,
                    # even when that ambient identity would hide missing setup.
                    for key, expected in (('user.name', 'Previous Release Qualification'),
                                          ('user.email', 'test@example.invalid')):
                        value = run(['git', '-C', book, 'config', '--local', '--get', key],
                                    env=env, cwd=scratch).strip()
                        self.assertEqual(value, expected)
                    identity = run(['git', '-C', book, 'log', '-1', '--format=%an%n%ae%n%cn%n%ce'],
                                   env=env, cwd=scratch).splitlines()
                    self.assertEqual(identity, ['Previous Release Qualification', 'test@example.invalid',
                                                'Previous Release Qualification', 'test@example.invalid'])
                    self.assertTrue((book / '.novel-creator/manifest.json').is_file())
