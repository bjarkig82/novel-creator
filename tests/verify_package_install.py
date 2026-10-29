"""Clean candidate/public installation checks. Never publishes or inherits dependencies."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import venv
import urllib.request
from urllib.parse import unquote, urlparse


def selected_product(report, expected):
    """Bind the installed product to an approved archive, not just its version."""
    if report.get('version') != '1' or not isinstance(report.get('install'), list):
        raise ValueError('Unsupported or malformed pip installation report')
    normalize = lambda name: re.sub(r'[-_.]+', '-', name).lower()
    products = [entry for entry in report['install']
                if isinstance(entry, dict) and isinstance(entry.get('metadata'), dict)
                and isinstance(entry['metadata'].get('name'), str)
                and normalize(entry['metadata']['name']) == normalize(expected['distribution'])]
    if len(products) != 1:
        raise ValueError('Pip report must contain exactly one selected product')
    product = products[0]
    if product['metadata'].get('version') != expected['version']:
        raise ValueError('Pip selected a different product version')
    download = product.get('download_info') or {}
    url = download.get('url', '')
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname != 'files.pythonhosted.org':
        raise ValueError('Unexpected selected public distribution origin')
    filename = unquote(parsed.path.rsplit('/', 1)[-1])
    archive = download.get('archive_info') or {}
    digest = (archive.get('hashes') or {}).get('sha256')
    if filename not in expected['files'] or digest != expected['files'][filename]:
        raise ValueError('Pip selected an archive outside the approved candidate')
    return {'name': product['metadata']['name'], 'version': product['metadata']['version'],
            'filename': filename, 'sha256': digest, 'url': url}


def run(argv, *, cwd, env, expected_exit=0):
    result = subprocess.run([str(a) for a in argv], cwd=cwd, env=env,
                            capture_output=True, text=True, encoding='utf-8', timeout=180)
    if result.returncode != expected_exit:
        raise RuntimeError(f'Command failed ({result.returncode}): {argv[1:]}\n{result.stderr}')
    return result.stdout


def verify(*, wheel=None, package=None, manifest=None):
    expected = json.loads(Path(manifest).read_text(encoding='utf-8')) if manifest else None
    if package:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*==[A-Za-z0-9][A-Za-z0-9_.+-]*', package):
            raise ValueError('Public mode requires an exact NAME==VERSION')
        if expected is None or package != expected.get('distribution', '') + '==' + expected.get('version', ''):
            raise ValueError('Public mode requires a matching verified candidate manifest')
        expected_files = expected.get('files')
        if (not isinstance(expected_files, dict) or len(expected_files) != 2
                or sum(name.endswith('.whl') for name in expected_files) != 1
                or sum(name.endswith('.tar.gz') for name in expected_files) != 1
                or any(not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{64}', value)
                       for value in expected_files.values())):
            raise ValueError('Public mode requires candidate wheel and sdist SHA-256 hashes')
    public_hashes = {}
    if package:
        name, version = package.split('==')
        with urllib.request.urlopen(f'https://pypi.org/pypi/{name}/{version}/json', timeout=30) as response:
            metadata = json.load(response)
        available = {entry['filename']: entry for entry in metadata['urls']}
        for filename, expected_hash in expected['files'].items():
            entry = available.get(filename)
            if entry is None or entry['digests']['sha256'] != expected_hash:
                raise ValueError('Public distribution does not match candidate: ' + filename)
            url = urlparse(entry['url'])
            if url.scheme != 'https' or url.hostname != 'files.pythonhosted.org':
                raise ValueError('Unexpected public distribution origin')
            with urllib.request.urlopen(entry['url'], timeout=60) as response:
                actual = hashlib.sha256(response.read()).hexdigest()
            if actual != expected_hash:
                raise ValueError('Downloaded public distribution hash mismatch')
            public_hashes[filename] = actual
    env = os.environ.copy()
    for key in list(env):
        if key.startswith(('PIP_', 'PYTHON', 'GIT_')):
            env.pop(key)
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1', PIP_DISABLE_PIP_VERSION_CHECK='1')
    with tempfile.TemporaryDirectory(prefix='novel-clean-install-') as folder:
        root = Path(folder).resolve()
        home = root / 'home'
        home.mkdir()
        (home / '.gitconfig').write_text('[user]\nname = Disposable Package Test\nemail = package@example.invalid\n', encoding='utf-8')
        env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / 'config'))
        runtime = root / 'runtime'
        # Use the caller's pip only as the installer, never its dependency sites.
        # --python also works on Linux installations without bundled ensurepip.
        venv.EnvBuilder(with_pip=False).create(runtime)
        scripts = runtime / ('Scripts' if os.name == 'nt' else 'bin')
        python = scripts / ('python.exe' if os.name == 'nt' else 'python')
        console = scripts / ('novel-creator.exe' if os.name == 'nt' else 'novel-creator')
        source = str(Path(wheel).resolve(strict=True)) if wheel else package
        report_path = root / 'install-report.json'
        run([sys.executable, '-I', '-m', 'pip', '--isolated', '--python', python,
             'install', '--no-cache-dir', '--index-url', 'https://pypi.org/simple',
             '--report', report_path,
             'pip', source], cwd=root, env=env)
        installed_product = selected_product(json.loads(report_path.read_text(encoding='utf-8')), expected) if package else None
        run([python, '-I', '-m', 'pip', 'check'], cwd=root, env=env)
        version = run([console, '--version'], cwd=root, env=env).strip()
        if expected and version != 'novel-creator ' + expected['version']:
            raise ValueError('Installed version does not match candidate')
        initialized = json.loads(run([console, 'init', 'Bréf', '--json'], cwd=root, env=env))
        novel = root / 'Bréf'
        launcher = novel / '.novel-creator/run.py'
        reported_python = initialized['data']['runtime_python']
        validated = json.loads(run([reported_python, '-I', launcher, 'validate', '--novel', novel, '--json'], cwd=root, env=env))
        guide = Path(initialized['data']['getting_started_path'])
        if not initialized['data']['ready'] or not guide.is_file() or not validated['ok']:
            raise RuntimeError('Installed novel is not ready/valid or guide is missing')
        settings_cases = []
        for name, title, language, explicit in [('Folder', 'Bréf frá morgundeginum', 'is', True),
                                                 ('English', 'A working title', 'en', True),
                                                 ('A Novel', 'A Novel', 'en', False)]:
            target = root / (name + '-destination' if explicit else name)
            args = [console, 'init', name, '--json']
            if explicit:
                args += ['--path', target, '--title', title, '--language', language]
            result = json.loads(run(args, cwd=root, env=env))
            context = json.loads(run([result['data']['runtime_python'], '-I', target / '.novel-creator/run.py',
                                      'context', '--novel', target, '--json'], cwd=root, env=env))
            project = context['data']['project']
            if project['title']['original_text'] != title or project['manuscript_language'] != language:
                raise RuntimeError('Installed optional settings changed supplied text/defaults')
            if not all(value['state'] == 'unknown' for value in project['creative_brief'].values()):
                raise RuntimeError('Initialization invented creative choices')
            bootstrap = json.loads(next((target / 'story/exchanges').glob('*.json')).read_text(encoding='utf-8'))
            request = bootstrap['input_artifacts'][1]['parsed_value']
            if request['name'] != name or request['language_argument'] != (language if explicit else None):
                raise RuntimeError('Setup request provenance changed')
            settings_cases.append(dict(name=name, title=title, language=language, preserved=True))
        for invalid in [('init', '../escape'), ('init', 'Invalid', '--language', 'fr'),
                        ('init', 'Invalid', '--title', ''), ('init', 'Invalid', '--unknown'),
                        ('init', 'Invalid', '--path', '')]:
            outcome = json.loads(run([console, *invalid, '--json'], cwd=root, env=env, expected_exit=2))
            if outcome['ok'] or (root / 'Invalid').exists():
                raise RuntimeError('Invalid input changed a novel or reported success')
        dependencies = json.loads(run([python, '-I', '-m', 'pip', 'list', '--format=json'], cwd=root, env=env))
        return {'mode': 'candidate' if wheel else 'public', 'source': Path(source).name if wheel else source,
                'version': version, 'dependencies': dependencies, 'validated': True,
                'guide_sha256': hashlib.sha256(guide.read_bytes()).hexdigest(),
                'wheel_sha256': hashlib.sha256(Path(wheel).read_bytes()).hexdigest() if wheel else None,
                'public_artifact_hashes': public_hashes,
                'installed_product': installed_product,
                'settings_cases': settings_cases, 'invalid_input_cases': 5,
                'host_walkthrough': 'not performed', 'dependency_inheritance': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--wheel', type=Path)
    mode.add_argument('--package', help='Verified production NAME==VERSION')
    parser.add_argument('--manifest', type=Path, help='Required expected candidate manifest for public mode')
    args = parser.parse_args()
    print(json.dumps(verify(wheel=args.wheel, package=args.package, manifest=args.manifest), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
