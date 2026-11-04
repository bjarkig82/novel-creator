import copy
import json
from pathlib import Path
import sys
import os
import urllib.request
import tempfile
import unittest
from unittest.mock import patch

from novel_creator import update_release
from novel_creator.cli import ToolError
from tests.update_release_helpers import product_wheel, release_listing, archive, PRIVATE_SEEDS
from tests.helpers import envelope


RUNTIME = {'version': [3, 13, 13], 'tags': ['py3-none-any'], 'marker_environment': {}}


class ReleaseTests(unittest.TestCase):
    def test_malformed_dependency_specifier_returns_a_supported_error(self):
        with self.assertRaises(ToolError) as caught:
            update_release._check_dependencies({'novel_creator-0.3.0.dist-info/METADATA':
                b'Requires-Python: definitely-not-a-specifier\n'}, {}, RUNTIME)
        self.assertEqual(caught.exception.code, 4)

    def test_missing_instruction_template_is_refused_before_private_installation(self):
        raw, _ = product_wheel(exclude=['novel_creator/codex/AGENTS.production.md'])
        transport = release_listing({'0.3.0': raw})
        selected = update_release.select_release(transport.get(update_release.INDEX_URL), runtime=RUNTIME)
        with tempfile.TemporaryDirectory() as cache, patch('novel_creator.update_release.cache_home', return_value=Path(cache)), patch('novel_creator.update_release.create_environment', side_effect=AssertionError('unneeded installation')):
            with self.assertRaises(ToolError) as caught:
                update_release.prepare(selected, transport=transport)
        self.assertEqual(caught.exception.code, 4)

    def test_latest_and_explicit_stable_selection_never_fall_back(self):
        raw, _ = product_wheel()
        transport = release_listing({'0.2.0': raw, '0.3.0': raw, '0.4.0rc1': raw})
        metadata = transport.get(update_release.INDEX_URL)
        self.assertEqual(update_release.select_release(metadata, version=None, runtime=RUNTIME)['version'], '0.3.0')
        self.assertEqual(update_release.select_release(metadata, version='0.2.0', runtime=RUNTIME)['version'], '0.2.0')
        newest = copy.deepcopy(metadata)
        newest['releases']['0.3.0'][0]['requires_python'] = '>=9'
        with self.assertRaises(ToolError) as caught:
            update_release.select_release(newest, runtime=RUNTIME)
        self.assertEqual(caught.exception.code, 4)
        for version in ('0.4.0rc1', '0.3.0+local', 'not-a-version'):
            with self.assertRaises(ToolError):
                update_release.select_release(metadata, version=version, runtime=RUNTIME)
        newest = copy.deepcopy(metadata)
        newest['releases']['0.3.0'][0]['yanked'] = True
        self.assertEqual(update_release.select_release(newest, runtime=RUNTIME)['version'], '0.2.0')

    def test_bad_archive_identity_and_paths_fail_before_installation(self):
        raw, _ = product_wheel()
        transport = release_listing({'0.3.0': raw})
        selected = update_release.select_release(transport.get(update_release.INDEX_URL), runtime=RUNTIME)
        self.assertIn('novel_creator/update-release.json', update_release.wheel_inventory(raw, selected))
        with self.assertRaises(ToolError):
            update_release.wheel_inventory(raw + b'changed', selected)
        hostile, digest = archive([('../escape.py', b'bad')])
        wrong = dict(selected, sha256=digest, size=len(hostile))
        with self.assertRaises(ToolError):
            update_release.wheel_inventory(hostile, wrong)
        with self.assertRaises(ToolError):
            update_release.require_public_url('https://user:secret@files.pythonhosted.org/a.whl')
        with self.assertRaises(ToolError):
            update_release.require_public_url('https://files.pythonhosted.org.evil.invalid/a.whl')

    def test_same_version_inherited_product_cannot_satisfy_private_preparation(self):
        raw, _ = product_wheel()
        transport = release_listing({'0.3.0': raw})
        selected = update_release.select_release(transport.get(update_release.INDEX_URL), runtime=RUNTIME)
        with tempfile.TemporaryDirectory(prefix='update-private-') as directory:
            root = Path(directory).resolve()
            source_python = update_release.create_environment(root / 'configured', sys.executable)
            runtime = update_release.runtime_info(source_python)
            site = Path(runtime['site_paths'][0])
            fake = site / 'novel_creator'
            fake.mkdir()
            (fake / '__init__.py').write_bytes(b'__version__ = "0.3.0"\nINHERITED_UNVERIFIED = True\n')
            info = site / 'novel_creator-0.3.0.dist-info'
            info.mkdir()
            (info / 'METADATA').write_text('Metadata-Version: 2.1\nName: novel-creator\nVersion: 0.3.0\n')
            original = (fake / '__init__.py').read_bytes()
            with patch('novel_creator.update_release.cache_home', return_value=root / 'cache'):
                prepared = update_release.prepare(selected, python=source_python, transport=transport)
            self.assertEqual((fake / '__init__.py').read_bytes(), original)
            self.assertEqual(prepared['version'], '0.3.0')
            self.assertTrue(Path(prepared['package_root']).is_relative_to(root / 'cache'))
            self.assertNotEqual(Path(prepared['package_root']), fake)
            self.assertNotIn(b'INHERITED_UNVERIFIED', (Path(prepared['package_root']) / '__init__.py').read_bytes())
            self.assertEqual(prepared['artifact']['sha256'], selected['sha256'])
            self.assertTrue(prepared['files'])
            immutable = {'history': [envelope()], 'retro_documents': []}
            self.assertEqual(update_release.probe_prepared(prepared, immutable)['exchange_count'], 1)
            product = Path(prepared['package_root']) / '__init__.py'
            product.write_bytes(product.read_bytes() + b'\nCHANGED = True\n')
            with self.assertRaises(ToolError):
                update_release.probe_prepared(prepared, immutable)

    def test_unknown_release_metadata_is_not_already_current(self):
        for value in ({}, {'releases': {}}, {'releases': []}):
            with self.assertRaises(ToolError):
                update_release.select_release(value, runtime=RUNTIME)

    def test_invalid_prerequisites_protocol_network_and_archive_forms_fail_closed(self):
        raw, _ = product_wheel()
        transport = release_listing({'0.3.0': raw})
        selected = update_release.select_release(transport.get(update_release.INDEX_URL), runtime=RUNTIME)
        for name in ('../escape.py', '/absolute', 'novel_creator/CON.py', 'novel_creator/a:b', 'novel_creator/space. '):
            hostile, digest = archive([(name, b'x')])
            with self.subTest(name=name), self.assertRaises(ToolError):
                update_release.wheel_inventory(hostile, dict(selected, sha256=digest, size=len(hostile)))
        for entries in ([('novel_creator/duplicate.py', b'1'), ('novel_creator/duplicate.py', b'2')],
                        [('novel_creator/File.py', b'1'), ('novel_creator/file.py', b'2')]):
            hostile, digest = archive(entries)
            with self.assertRaises(ToolError):
                update_release.wheel_inventory(hostile, dict(selected, sha256=digest, size=len(hostile)))
        with self.assertRaises(ToolError) as caught:
            update_release.runtime_info('relative-python')
        self.assertEqual(caught.exception.code, 2)
        with self.assertRaises(ToolError):
            update_release.validate_document('release', {'kind': 'release', 'protocol_version': 999})
        transport.responses[selected['url']] = OSError('offline')
        with self.assertRaises(ToolError) as caught:
            update_release.prepare(selected, transport=transport)
        self.assertEqual(caught.exception.code, 5)
        with self.assertRaises(ToolError):
            update_release._check_dependencies({'novel_creator-0.3.0.dist-info/METADATA':
                b'Requires-Python: >=9\n'}, selected, RUNTIME)

    def test_export_cannot_omit_a_verified_package_resource(self):
        raw, _ = product_wheel()
        transport = release_listing({'0.3.0': raw})
        selected = update_release.select_release(transport.get(update_release.INDEX_URL), runtime=RUNTIME)
        original = update_release._run
        def tampered(argv, **kwargs):
            output = original(argv, **kwargs)
            if any('result=export_bundle()' in str(value) for value in argv):
                value = json.loads(output)
                value['files'].pop(next(iter(value['files'])))
                return json.dumps(value).encode()
            return output
        with tempfile.TemporaryDirectory() as cache, patch('novel_creator.update_release.cache_home', return_value=Path(cache)), patch('novel_creator.update_release._run', side_effect=tampered):
            with self.assertRaises(ToolError):
                update_release.prepare(selected, transport=transport)

    def test_inherited_pip_python_and_git_injection_cannot_redirect_private_installation(self):
        raw, _ = product_wheel()
        transport = release_listing({'0.3.0': raw})
        selected = update_release.select_release(transport.get(update_release.INDEX_URL), runtime=RUNTIME)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            injected = root / 'injected'
            injected.mkdir()
            marker = root / 'executed-sitecustomize'
            (injected / 'sitecustomize.py').write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n')
            config = root / 'private-pip.ini'
            config.write_text('[global]\nextra-index-url = https://private-credential-value@example.invalid/private\n')
            target = root / 'unrequested-install-target'
            before = config.read_bytes()
            environment = {'PYTHONPATH': str(injected), 'PYTHONSTARTUP': str(injected / 'sitecustomize.py'),
                'PIP_CONFIG_FILE': str(config), 'PIP_TARGET': str(target), 'PIP_USER': '1',
                'PIP_EXTRA_INDEX_URL': 'https://private-credential-value@example.invalid',
                'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.worktree', 'GIT_CONFIG_VALUE_0': PRIVATE_SEEDS[-1],
                'UNRELATED_PRIVATE_STORY': PRIVATE_SEEDS[0], 'PRIVATE_TRANSCRIPT': PRIVATE_SEEDS[1],
                'AUTH_TOKEN': PRIVATE_SEEDS[2]}
            with patch.dict(os.environ, environment), patch('novel_creator.update_release.cache_home', return_value=root / 'cache'):
                prepared = update_release.prepare(selected, transport=transport)
                self.assertTrue(Path(prepared['package_root']).is_relative_to(root / 'cache'))
                clean = update_release.clean_environment()
                self.assertEqual(clean['PIP_CONFIG_FILE'], os.devnull)
                for name in environment:
                    if name != 'PIP_CONFIG_FILE':
                        self.assertNotIn(name, clean)
            self.assertFalse(marker.exists())
            self.assertFalse(target.exists())
            self.assertEqual(config.read_bytes(), before)
            for url in transport.requests:
                self.assertTrue(url.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')))
                self.assertFalse(any(seed in url for seed in PRIVATE_SEEDS))

    def test_redirects_remain_within_fixed_public_https_hosts(self):
        request = urllib.request.Request(update_release.INDEX_URL)
        for url in ('http://pypi.org/file.whl', 'https://evil.invalid/file.whl',
                    'https://files.pythonhosted.org/file.whl?private=secret',
                    'file:///private/credentials', 'https://files.pythonhosted.org:8443/file.whl'):
            with self.subTest(url=url), self.assertRaises(ToolError):
                update_release._PublicRedirect().redirect_request(request, None, 302, 'redirect', {}, url)
