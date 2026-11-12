"""Create a private, pinned Novel Creator runtime. Standard library only."""
import sys
import json

# Keep this before imports/syntax that require the supported Python version.
if sys.version_info < (3, 11):
    print(json.dumps({'ok': False, 'error': {'message': 'Python 3.11 or newer is required; run this script with a compatible interpreter.'}}))
    sys.exit(2)

import argparse
import ast
from email.parser import Parser
import hashlib
import os
from pathlib import Path
import re
import stat
import subprocess
import venv
import zipfile


PLUGIN = Path(__file__).resolve().parents[1]
VERSION = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))['version']
STATE = '.novel-creator-runtime.json'


class SetupError(Exception):
    """Safe setup refusal or recoverable setup failure."""


def reject_redirects(path):
    """Reject existing symlinks and Windows reparse points in every component."""
    for item in (path, *path.parents):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise SetupError('Path contains a symlink/junction redirect: ' + str(item))


def absolute_path(value):
    path = Path(value).expanduser().absolute()
    if '..' in path.parts:
        raise SetupError('Paths must not contain parent traversal segments')
    reject_redirects(path)
    return path


def runtime_directory(novel=None):
    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA')
        if not base:
            raise SetupError('LOCALAPPDATA is required on Windows')
        runtime = absolute_path(base) / 'NovelCreator/runtimes' / VERSION
    elif sys.platform.startswith('linux'):
        runtime = absolute_path(os.environ.get('XDG_CACHE_HOME') or '~/.cache') / 'novel-creator/runtimes' / VERSION
    else:
        raise SetupError('Setup supports Windows and Linux only')
    reject_redirects(runtime)
    if runtime == PLUGIN or PLUGIN in runtime.parents or runtime in PLUGIN.parents:
        raise SetupError('Runtime cache must be outside the plugin directory')
    if novel is not None:
        novel = absolute_path(novel)
        if runtime == novel or novel in runtime.parents or runtime in novel.parents:
            raise SetupError('Runtime cache must be outside the intended novel directory')
    return runtime


def runtime_python(runtime):
    return runtime / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')


def check_prerequisites():
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SetupError('Install Git 2.39 or newer, then retry setup; Git was not usable') from exc
    match = re.search(r'(\d+)\.(\d+)', result.stdout)
    if not match or tuple(map(int, match.groups())) < (2, 39):
        raise SetupError('Git 2.39 or newer is required; install a compatible Git and retry')


def wheel_source(wheel):
    if wheel is None:
        return {'kind': 'pypi', 'requirement': 'novel-creator==' + VERSION}, 'novel-creator==' + VERSION
    path = absolute_path(wheel)
    if not path.is_file() or path.suffix.lower() != '.whl':
        raise SetupError('Candidate wheel must be an existing .whl file')
    try:
        with zipfile.ZipFile(path) as archive:
            members = [name for name in archive.namelist() if name.endswith('.dist-info/METADATA')]
            if len(members) != 1:
                raise SetupError('Candidate wheel must contain exactly one product METADATA record')
            metadata = Parser().parsestr(archive.read(members[0]).decode('utf-8'))
        product = re.sub(r'[-_.]+', '-', metadata.get('Name', '')).lower()
        if product != 'novel-creator' or metadata.get('Version') != VERSION:
            raise SetupError('Candidate wheel must be novel-creator version ' + VERSION)
    except (OSError, ValueError, zipfile.BadZipFile, UnicodeError) as exc:
        raise SetupError('Candidate wheel metadata could not be read') from exc
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {'kind': 'wheel', 'sha256': digest}, str(path)


def install_environment(python=None):
    env = os.environ.copy()
    # Remove destination overrides before even the read-only config probe.
    for name in ('PIP_TARGET', 'PIP_PREFIX', 'PIP_USER', 'PIP_ROOT', 'PIP_PYTHON', 'PYTHONPATH', 'PYTHONHOME'):
        env.pop(name, None)
    if python is not None:
        # Let pip resolve system/user/site/explicit config precedence itself.
        # Pin --python so configured global.python cannot redirect the probe;
        # override logging so reading configuration cannot write a configured log.
        try:
            result = subprocess.run([str(python), '-I', '-m', 'pip', '--python', str(python),
                                     '--log', os.devnull, 'config', 'list'], env=env.copy(),
                                    capture_output=True, text=True)
        except OSError as exc:
            raise SetupError('Could not read pip configuration. Check the private runtime and pip configuration files, then retry setup.') from exc
        if result.returncode:
            raise SetupError('Could not read pip configuration. Check pip.ini/pip.conf or PIP_CONFIG_FILE, then retry setup; configuration output is withheld to protect credentials.')
        allowed = ('proxy', 'cert', 'client-cert', 'index-url', 'extra-index-url')
        values = {}
        for line in result.stdout.splitlines():
            key, separator, raw = line.partition('=')
            if separator and key in {scope + '.' + option for scope in ('global', 'install') for option in allowed}:
                try:
                    value = ast.literal_eval(raw)
                except (ValueError, SyntaxError) as exc:
                    raise SetupError('Could not interpret pip configuration network settings; check pip configuration syntax and retry.') from exc
                if not isinstance(value, str):
                    raise SetupError('Pip configuration network settings must be strings; check pip configuration and retry.')
                # Pip ignores empty options rather than clearing lower scopes.
                if value:
                    values[key] = value
        # Install-specific options override global config; inherited PIP_* options
        # retain their existing higher precedence over either configuration scope.
        for option in allowed:
            value = values.get('install.' + option, values.get('global.' + option))
            if value is not None:
                variable = 'PIP_' + option.upper().replace('-', '_')
                if not env.get(variable):
                    env[variable] = value
    # Install sees only the permitted network options, never target/prefix/user
    # or another option from config that could redirect its writes.
    env['PIP_CONFIG_FILE'] = os.devnull
    return env


def create_venv(runtime):
    try:
        venv.EnvBuilder(with_pip=True).create(str(runtime))
    except Exception as exc:
        raise SetupError('Virtual environment creation failed. Install Python venv/ensurepip support and retry the same setup; the partial runtime was preserved.') from exc


def install_package(python, requirement):
    try:
        subprocess.run([str(python), '-I', '-m', 'pip', 'install', '--disable-pip-version-check',
                        '--no-input', '--no-user', requirement], env=install_environment(python),
                       capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SetupError('Package installation failed. Check network/index access, proxy and CA settings and availability of novel-creator==' + VERSION + '; for an unpublished candidate supply --wheel PATH. Retry the same setup; the partial runtime was preserved.') from exc


def healthy_runtime(python):
    probe = (
        'import importlib.metadata as m, pathlib, sys, novel_creator, jsonschema, jsonschema_rs, packaging; '
        'root=pathlib.Path(sys.prefix).resolve(); '
        'assert sys.prefix != sys.base_prefix; '
        'assert m.version("novel-creator") == ' + repr(VERSION) + '; '
        'assert novel_creator.__version__ == ' + repr(VERSION) + '; '
        'assert pathlib.Path(novel_creator.__file__).resolve().is_relative_to(root); '
        'assert pathlib.Path(m.distribution("novel-creator").locate_file("")).resolve().is_relative_to(root)'
    )
    try:
        for args in (['-c', probe], ['-m', 'pip', 'check']):
            result = subprocess.run([str(python), '-I', *args], env=install_environment(),
                                    capture_output=True, text=True)
            if result.returncode:
                return False
        return True
    except OSError:
        return False


def read_state(runtime, source):
    reject_redirects(runtime)
    state_path = runtime / STATE
    reject_redirects(state_path)
    try:
        state = json.loads(state_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise SetupError('Refusing occupied unknown runtime directory: ' + str(runtime) + '. Choose another cache location or inspect and move this directory yourself.') from exc
    if (not isinstance(state, dict) or state.get('owner') != 'novel-creator-plugin'
            or state.get('version') != VERSION or state.get('format') != 1
            or state.get('phase') not in ('creating', 'installing', 'ready')):
        raise SetupError('Refusing unrecognized runtime ownership marker: ' + str(runtime))
    if state.get('source') != source:
        raise SetupError('Runtime provenance differs: a different candidate or package source already owns ' + str(runtime) + '. Use a separate XDG_CACHE_HOME/LOCALAPPDATA to qualify this candidate.')
    return state


def write_state(runtime, source, phase):
    state_path = runtime / STATE
    reject_redirects(state_path)
    state_path.write_text(json.dumps({'owner': 'novel-creator-plugin', 'format': 1,
                                     'version': VERSION, 'source': source, 'phase': phase}, indent=2) + '\n', encoding='utf-8')


def bootstrap(*, wheel=None, novel=None):
    runtime = runtime_directory(novel)
    source, requirement = wheel_source(wheel)
    check_prerequisites()
    if runtime.exists():
        read_state(runtime, source)
    runtime.parent.mkdir(parents=True, exist_ok=True)
    reject_redirects(runtime.parent)
    lock = runtime.parent / (VERSION + '.lock')
    try:
        descriptor = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise SetupError('Concurrent setup lock exists: ' + str(lock) + '. Wait for that setup. If it crashed, verify that no setup process is running before manually removing only this lock.') from exc
    try:
        os.write(descriptor, ('pid=' + str(os.getpid()) + '\n').encode('ascii'))
        if runtime.exists():
            state = read_state(runtime, source)
        else:
            runtime.mkdir()
            write_state(runtime, source, 'creating')
            state = {'phase': 'creating'}
        python = runtime_python(runtime)
        # venv's interpreter is normally a symlink to the selected base Python;
        # reject redirects in directories, not this expected interpreter link.
        reject_redirects(python.parent)
        if state['phase'] == 'ready' and healthy_runtime(python):
            return {'runtime_python': str(python), 'version': VERSION, 'reused': True}
        if state['phase'] == 'creating' or not python.is_file():
            write_state(runtime, source, 'creating')
            create_venv(runtime)
        write_state(runtime, source, 'installing')
        install_package(python, requirement)
        if not healthy_runtime(python):
            raise SetupError('Installed runtime failed isolated version/dependency checks. The partial runtime is preserved; inspect its environment and retry setup.')
        write_state(runtime, source, 'ready')
        return {'runtime_python': str(python), 'version': VERSION, 'reused': False}
    finally:
        # Windows CRT file handles must be closed before unlinking. Capture the
        # identity first so a replacement lock remains protected after close.
        try:
            identity = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        try:
            current = os.stat(lock, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino):
                lock.unlink()


def main(argv=None):
    class JsonParser(argparse.ArgumentParser):
        def error(self, message):
            raise SetupError(message)
    try:
        parser = JsonParser(description=__doc__)
        parser.add_argument('--wheel', help='Local exact-version candidate wheel; otherwise install the pinned PyPI release')
        parser.add_argument('--novel', help='Intended new novel path, to validate cache separation')
        args = parser.parse_args(argv)
        data = bootstrap(wheel=args.wheel, novel=args.novel)
        print(json.dumps({'ok': True, 'data': data}))
        return 0
    except (SetupError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({'ok': False, 'error': {'message': str(exc), 'recovery': 'Preserve partial files. Resolve the reported cause, then retry this same setup; never rerun a successful notebook initialization.'}}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
