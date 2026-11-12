"""Runtime setup never touches a book or shares a global Python install."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'plugins/novel-creator/scripts/bootstrap.py'


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        platform = patch('sys.platform', 'linux')
        platform.start()
        self.addCleanup(platform.stop)
        if not SCRIPT.exists():
            self.fail('The bundled standard-library bootstrap is missing')
        spec = importlib.util.spec_from_file_location('plugin_bootstrap', SCRIPT)
        self.bootstrap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.bootstrap)
        self.env = patch.dict(os.environ, {'XDG_CACHE_HOME': str(self.root / 'cache')})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.runtime = self.root / 'cache/novel-creator/runtimes/0.8.0'
        self.installs = []
        self.healthy = False

    def wheel(self, name='novel_creator', version='0.8.0', extra=''):
        path = self.root / ('candidate' + extra + '.whl')
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr(f'{name}-{version}.dist-info/METADATA',
                             f'Name: {name}\nVersion: {version}\n\n{extra}')
        return path

    def fake_create(self, runtime):
        python = self.bootstrap.runtime_python(runtime)
        python.parent.mkdir(parents=True, exist_ok=True)
        python.write_text('test interpreter')

    def fake_install(self, python, requirement):
        self.installs.append(requirement)
        self.healthy = True

    def setup_runtime(self, wheel=None, novel=None):
        with patch.object(self.bootstrap, 'check_prerequisites'), \
                patch.object(self.bootstrap, 'create_venv', side_effect=self.fake_create), \
                patch.object(self.bootstrap, 'install_package', side_effect=self.fake_install), \
                patch.object(self.bootstrap, 'healthy_runtime', side_effect=lambda p: self.healthy):
            return self.bootstrap.bootstrap(wheel=wheel, novel=novel)

    def test_exact_install_and_healthy_reuse(self):
        first = self.setup_runtime()
        second = self.setup_runtime()
        self.assertFalse(first['reused'])
        self.assertTrue(second['reused'])
        self.assertEqual(self.installs, ['novel-creator==0.8.0'])
        self.assertEqual(first['runtime_python'], str(self.bootstrap.runtime_python(self.runtime)))

    def test_unknown_runtime_preserved(self):
        self.runtime.mkdir(parents=True)
        sentinel = self.runtime / 'valuable'
        sentinel.write_text('preserve')
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'unknown|unrecognized'):
            self.setup_runtime()
        self.assertEqual(sentinel.read_text(), 'preserve')
        self.assertEqual(list(self.runtime.iterdir()), [sentinel])

    def test_invalid_owned_marker_is_refused_without_rewriting(self):
        self.runtime.mkdir(parents=True)
        marker = self.runtime / '.novel-creator-runtime.json'
        marker.write_text(json.dumps({'owner': 'novel-creator-plugin', 'format': 1,
                                      'version': '0.8.0', 'source': {'kind': 'pypi', 'requirement': 'novel-creator==0.8.0'},
                                      'phase': 'unknown'}))
        before = marker.read_bytes()
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'unrecognized'):
            self.setup_runtime()
        self.assertEqual(marker.read_bytes(), before)
        self.assertEqual(self.installs, [])

    def test_runtime_redirect_rejected_before_mutation(self):
        outside = self.root / 'outside'
        outside.mkdir()
        try:
            (self.root / 'cache').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('This Windows account cannot create symbolic links')
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'redirect|symlink'):
            self.setup_runtime()
        self.assertEqual(list(outside.iterdir()), [])

    def test_cache_cannot_be_inside_novel_or_plugin(self):
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'novel'):
            self.setup_runtime(novel=self.root / 'cache')
        with patch.dict(os.environ, {'XDG_CACHE_HOME': str(SCRIPT.parents[1] / 'cache')}):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'plugin'):
                self.setup_runtime()
        self.assertFalse((SCRIPT.parents[1] / 'cache').exists())

    def test_wheel_product_version_and_provenance(self):
        for name, version in [('other', '0.8.0'), ('novel_creator', '0.7.2')]:
            with self.subTest(name=name, version=version):
                with self.assertRaisesRegex(self.bootstrap.SetupError, 'wheel'):
                    self.setup_runtime(wheel=self.wheel(name, version))
        first = self.wheel(extra='first')
        self.setup_runtime(wheel=first)
        self.assertEqual(self.installs, [str(first)])
        self.assertTrue(self.setup_runtime(wheel=first)['reused'])
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'provenance|different'):
            self.setup_runtime(wheel=self.wheel(extra='second'))

    def test_install_failure_retains_owned_partial_for_retry(self):
        with patch.object(self.bootstrap, 'check_prerequisites'), \
                patch.object(self.bootstrap, 'create_venv', side_effect=self.fake_create), \
                patch.object(self.bootstrap, 'healthy_runtime', return_value=False), \
                patch.object(self.bootstrap, 'install_package', side_effect=self.bootstrap.SetupError('pip failed')):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'pip failed'):
                self.bootstrap.bootstrap()
        self.assertTrue(self.runtime.is_dir())
        self.assertTrue((self.runtime / '.novel-creator-runtime.json').is_file())
        self.assertFalse((self.runtime.parent / '0.8.0.lock').exists())
        self.assertFalse(self.setup_runtime()['reused'])

    def test_venv_creation_failure_preserves_partial(self):
        with patch.object(self.bootstrap, 'check_prerequisites'), \
                patch.object(self.bootstrap, 'create_venv', side_effect=self.bootstrap.SetupError('venv failed')):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'venv failed'):
                self.bootstrap.bootstrap()
        self.assertTrue((self.runtime / '.novel-creator-runtime.json').exists())
        self.assertFalse(self.setup_runtime()['reused'])

    def test_partial_interpreter_without_pip_retries_venv_creation(self):
        def interrupted(runtime):
            self.fake_create(runtime)
            raise self.bootstrap.SetupError('ensurepip interrupted')
        with patch.object(self.bootstrap, 'check_prerequisites'), \
                patch.object(self.bootstrap, 'create_venv', side_effect=interrupted):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'ensurepip'):
                self.bootstrap.bootstrap()
        with patch.object(self.bootstrap, 'create_venv', wraps=self.fake_create) as create, \
                patch.object(self.bootstrap, 'check_prerequisites'), \
                patch.object(self.bootstrap, 'install_package', side_effect=self.fake_install), \
                patch.object(self.bootstrap, 'healthy_runtime', side_effect=lambda p: self.healthy):
            self.bootstrap.bootstrap()
        self.assertEqual(create.call_count, 1)

    def test_windows_cache_location_and_interpreter(self):
        with patch('sys.platform', 'win32'), patch.dict(os.environ, {'LOCALAPPDATA': str(self.root / 'local')}):
            runtime = self.bootstrap.runtime_directory()
            self.assertEqual(runtime, self.root / 'local/NovelCreator/runtimes/0.8.0')
            self.assertEqual(self.bootstrap.runtime_python(runtime), runtime / 'Scripts/python.exe')

    def test_windows_reparse_attributes_rejected(self):
        path = self.root / 'redirect'
        path.mkdir()
        original = Path.lstat
        def lstat(item):
            if item == path:
                class Info:
                    st_mode = stat.S_IFDIR
                    st_file_attributes = 0x400
                return Info()
            return original(item)
        with patch.object(Path, 'lstat', lstat):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'junction|redirect'):
                self.bootstrap.absolute_path(path)

    def test_unsupported_platform_refuses_before_mutation(self):
        with patch('sys.platform', 'darwin'):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'Windows and Linux'):
                self.setup_runtime()
        self.assertFalse(self.runtime.exists())

    def test_runtime_state_redirect_preserved(self):
        self.runtime.mkdir(parents=True)
        marker = self.root / 'outside.json'
        marker.write_text('{}')
        try:
            (self.runtime / '.novel-creator-runtime.json').symlink_to(marker)
        except OSError:
            self.skipTest('This Windows account cannot create symbolic links')
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'symlink|redirect'):
            self.setup_runtime()
        self.assertEqual(marker.read_text(), '{}')

    def test_lock_redirect_is_never_followed(self):
        self.runtime.parent.mkdir(parents=True)
        target = self.root / 'other-lock'
        target.write_text('preserve')
        lock = self.runtime.parent / '0.8.0.lock'
        try:
            lock.symlink_to(target)
        except OSError:
            self.skipTest('This Windows account cannot create symbolic links')
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'lock'):
            self.setup_runtime()
        self.assertTrue(lock.is_symlink())
        self.assertEqual(target.read_text(), 'preserve')

    def test_concurrent_lock_is_never_removed(self):
        self.runtime.parent.mkdir(parents=True)
        lock = self.runtime.parent / '0.8.0.lock'
        lock.write_text('another process')
        with self.assertRaisesRegex(self.bootstrap.SetupError, 'lock|concurrent'):
            self.setup_runtime()
        self.assertEqual(lock.read_text(), 'another process')
        self.assertFalse(self.runtime.exists())

    def test_lock_descriptor_closed_before_unlink(self):
        lock = self.runtime.parent / '0.8.0.lock'
        closed = False
        original_close = os.close
        original_unlink = Path.unlink
        def close(descriptor):
            nonlocal closed
            original_close(descriptor)
            closed = True
        def unlink(path, *args, **kwargs):
            if path == lock:
                self.assertTrue(closed, 'Windows requires closing the lock handle before deletion')
            return original_unlink(path, *args, **kwargs)
        with patch.object(self.bootstrap.os, 'close', side_effect=close), patch.object(Path, 'unlink', unlink):
            self.setup_runtime()
        self.assertFalse(lock.exists())

    def test_lock_replaced_after_close_is_preserved(self):
        lock = self.runtime.parent / '0.8.0.lock'
        original_close = os.close
        def close(descriptor):
            original_close(descriptor)
            lock.rename(lock.with_name('original-lock'))
            lock.write_text('replacement')
        with patch.object(self.bootstrap.os, 'close', side_effect=close):
            self.setup_runtime()
        self.assertEqual(lock.read_text(), 'replacement')

    def test_config_only_network_settings_retained_without_destination_options(self):
        output = "\n".join([
            "global.proxy='https://proxy.invalid'", "global.cert='/global-ca.pem'",
            "install.cert='/install-ca.pem'", "install.client-cert='/client.pem'",
            "global.index-url='https://index.invalid/simple'",
            "install.extra-index-url='https://extra.invalid/simple'",
            "global.target='/unsafe'", "install.prefix='/unsafe'", "install.user='true'",
            "global.python='/unsafe/python'", "global.log='/unsafe/log'",
        ])
        with patch.dict(os.environ, {}, clear=True), patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, output, '')):
            env = self.bootstrap.install_environment(Path('/runtime/bin/python'))
        self.assertEqual(env['PIP_PROXY'], 'https://proxy.invalid')
        self.assertEqual(env['PIP_CERT'], '/install-ca.pem')
        self.assertEqual(env['PIP_CLIENT_CERT'], '/client.pem')
        self.assertEqual(env['PIP_INDEX_URL'], 'https://index.invalid/simple')
        self.assertEqual(env['PIP_EXTRA_INDEX_URL'], 'https://extra.invalid/simple')
        self.assertEqual(env['PIP_CONFIG_FILE'], os.devnull)
        self.assertTrue(all(name not in env for name in ('PIP_TARGET', 'PIP_PREFIX', 'PIP_USER', 'PIP_PYTHON', 'PIP_LOG')))

    def test_config_probe_uses_original_config_and_inherited_transport_wins(self):
        supplied = {'PIP_CONFIG_FILE': str(self.root / 'corporate.ini'),
                    'PIP_PROXY': 'https://env-proxy.invalid', 'PIP_CERT': '/env-ca.pem',
                    'HTTPS_PROXY': 'https://https-env.invalid', 'PIP_TARGET': '/unsafe'}
        output = "global.proxy='https://config-proxy.invalid'\ninstall.cert='/config-ca.pem'\n"
        calls = []
        def run(command, **kwargs):
            calls.append((command, kwargs))
            return subprocess.CompletedProcess(command, 0, output, '')
        with patch.dict(os.environ, supplied, clear=True), patch.object(self.bootstrap.subprocess, 'run', side_effect=run):
            env = self.bootstrap.install_environment(Path('/runtime/bin/python'))
        self.assertEqual(env['PIP_PROXY'], supplied['PIP_PROXY'])
        self.assertEqual(env['PIP_CERT'], supplied['PIP_CERT'])
        self.assertEqual(env['HTTPS_PROXY'], supplied['HTTPS_PROXY'])
        command, kwargs = calls[0]
        self.assertEqual(command[:4], [str(Path('/runtime/bin/python')), '-I', '-m', 'pip'])
        self.assertEqual(command[-2:], ['config', 'list'])
        self.assertEqual(kwargs['env']['PIP_CONFIG_FILE'], supplied['PIP_CONFIG_FILE'])
        self.assertTrue('PIP_TARGET' not in kwargs['env'])
        self.assertTrue(kwargs['capture_output'])

    def test_empty_install_config_retains_nonempty_global_network_options(self):
        output = "global.cert='/company/ca.pem'\ninstall.cert=''\nglobal.proxy='https://company.invalid'\ninstall.proxy=''\n"
        with patch.dict(os.environ, {}, clear=True), patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, output, '')):
            env = self.bootstrap.install_environment(Path('/runtime/bin/python'))
        self.assertEqual(env['PIP_CERT'], '/company/ca.pem')
        self.assertEqual(env['PIP_PROXY'], 'https://company.invalid')

    def test_empty_inherited_transport_options_do_not_block_configuration(self):
        output = "global.cert='/company/ca.pem'\ninstall.proxy='https://company.invalid'\n"
        inherited = {'PIP_CERT': '', 'PIP_PROXY': ''}
        with patch.dict(os.environ, inherited, clear=True), patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, output, '')):
            env = self.bootstrap.install_environment(Path('/runtime/bin/python'))
        self.assertEqual(env['PIP_CERT'], '/company/ca.pem')
        self.assertEqual(env['PIP_PROXY'], 'https://company.invalid')

    def test_empty_overrides_match_actual_pip_install_parser(self):
        config = self.root / 'empty-overrides.conf'
        config.write_text('[global]\ncert = /company/ca.pem\nproxy = https://company.invalid\n'
                          '[install]\ncert =\nproxy =\n')
        original = {'PIP_CONFIG_FILE': str(config), 'PIP_CERT': '', 'PIP_PROXY': ''}
        probe = ('import json; from pip._internal.commands import create_command; '
                 'options,args=create_command("install").parse_args([]); '
                 'print(json.dumps({"PIP_CERT": options.cert, "PIP_PROXY": options.proxy}))')
        with patch.dict(os.environ, original, clear=True):
            expected = subprocess.run([os.sys.executable, '-I', '-c', probe], capture_output=True, text=True, check=True)
            env = self.bootstrap.install_environment(Path(os.sys.executable))
        effective = json.loads(expected.stdout)
        self.assertEqual(effective['PIP_CERT'], '/company/ca.pem')
        self.assertEqual(effective['PIP_PROXY'], 'https://company.invalid')
        for option, value in effective.items():
            self.assertEqual(env[option], value)

    def test_config_probe_failure_is_actionable_without_disclosing_output(self):
        result = subprocess.CompletedProcess([], 1, 'secret-token', 'secret-token')
        with patch.object(self.bootstrap.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'pip configuration') as error:
                self.bootstrap.install_environment(Path('/runtime/bin/python'))
        self.assertNotIn('secret-token', str(error.exception))

    def test_real_pip_config_network_settings_and_redirect_sanitization(self):
        config = self.root / 'pip.conf'
        log = self.root / 'configured-log'
        config.write_text('[global]\nproxy = https://configured.invalid\ncert = /global-ca.pem\n'
                          'target = /unsafe\npython = /unsafe-python\nlog = ' + str(log) + '\n'
                          '[install]\ncert = /install-ca.pem\nprefix = /unsafe-prefix\nuser = true\n')
        with patch.dict(os.environ, {'PIP_CONFIG_FILE': str(config)}, clear=True):
            env = self.bootstrap.install_environment(Path(os.sys.executable))
        self.assertEqual(env['PIP_PROXY'], 'https://configured.invalid')
        self.assertEqual(env['PIP_CERT'], '/install-ca.pem')
        self.assertTrue(all(name not in env for name in ('PIP_TARGET', 'PIP_PREFIX', 'PIP_USER', 'PIP_PYTHON')))
        self.assertFalse(log.exists(), 'The read-only probe must not write a configured log')
        self.assertEqual(env['PIP_CONFIG_FILE'], os.devnull)

    def test_config_values_are_parsed_without_executing_expressions(self):
        marker = self.root / 'must-not-exist'
        malicious = 'global.proxy=__import__("pathlib").Path(' + repr(str(marker)) + ').touch()\n'
        with patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, malicious, '')):
            with self.assertRaisesRegex(self.bootstrap.SetupError, 'configuration'):
                self.bootstrap.install_environment(Path('/runtime/bin/python'))
        self.assertFalse(marker.exists())

    def test_install_uses_network_config_environment(self):
        calls = []
        def run(command, **kwargs):
            calls.append((command, kwargs))
            output = "global.proxy='https://proxy.invalid'\n" if command[-2:] == ['config', 'list'] else ''
            return subprocess.CompletedProcess(command, 0, output, '')
        with patch.dict(os.environ, {}, clear=True), patch.object(self.bootstrap.subprocess, 'run', side_effect=run):
            self.bootstrap.install_package(Path('/runtime/bin/python'), 'novel-creator==0.8.0')
        installs = [kwargs for command, kwargs in calls if 'install' in command]
        self.assertEqual(len(installs), 1)
        self.assertEqual(installs[0]['env']['PIP_PROXY'], 'https://proxy.invalid')

    def test_pip_environment_redirects_removed_proxy_and_ca_retained(self):
        with patch.dict(os.environ, {'PIP_TARGET': '/unsafe', 'PIP_PREFIX': '/unsafe',
                                    'PIP_USER': 'yes', 'PIP_PYTHON': '/unsafe/python', 'HTTPS_PROXY': 'https://proxy.invalid',
                                    'PIP_CERT': '/trusted-ca.pem'}):
            env = self.bootstrap.install_environment()
        for key in ('PIP_TARGET', 'PIP_PREFIX', 'PIP_USER', 'PIP_PYTHON'):
            self.assertTrue(key not in env, key + ' must not redirect package installation')
        self.assertEqual(env['HTTPS_PROXY'], 'https://proxy.invalid')
        self.assertEqual(env['PIP_CERT'], '/trusted-ca.pem')
        self.assertEqual(env['PIP_CONFIG_FILE'], os.devnull)

    def test_health_checks_use_isolated_interpreter_and_dependency_check(self):
        calls = []
        def run(command, **kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command, 0, '', '')
        with patch.object(self.bootstrap.subprocess, 'run', side_effect=run):
            self.assertTrue(self.bootstrap.healthy_runtime(Path('/runtime/bin/python')))
        self.assertTrue(all(command[1] == '-I' for command in calls))
        self.assertTrue(any(command[-3:] == ['-m', 'pip', 'check'] for command in calls))

    def test_health_probe_imports_runtime_dependencies(self):
        with patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run:
            self.bootstrap.healthy_runtime(Path('/runtime/bin/python'))
        probe = run.call_args_list[0].args[0][-1]
        for dependency in ('jsonschema', 'jsonschema_rs', 'packaging'):
            self.assertIn(dependency, probe)

    def test_health_probe_failure_stops_reuse(self):
        with patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', 'ImportError: missing binary')):
            self.assertFalse(self.bootstrap.healthy_runtime(Path('/runtime/bin/python')))

    def test_old_git_rejected(self):
        with patch.object(self.bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'git version 2.38.0\n', '')):
            with self.assertRaisesRegex(self.bootstrap.SetupError, '2.39'):
                self.bootstrap.check_prerequisites()

    def test_cli_failure_is_json_without_mutating_runtime(self):
        result = subprocess.run([os.sys.executable, str(SCRIPT), '--wheel', str(self.root / 'missing.whl')],
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['ok'])
        self.assertEqual(result.stderr, '')
        self.assertFalse(self.runtime.exists())
