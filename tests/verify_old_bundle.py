"""Verify current package continuation preserves an actual historical wheel's novel."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import venv

from verify_package_install import run


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


def verify(old_wheel, new_wheel):
    old_wheel, new_wheel = Path(old_wheel).resolve(strict=True), Path(new_wheel).resolve(strict=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON', 'PIP_'))}
    env.update(PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='novel-old-bundle-') as folder:
        root = Path(folder).resolve()
        home = root / 'home'
        home.mkdir()
        (home / '.gitconfig').write_text('[user]\nname = Old Bundle Test\nemail = old@example.invalid\n')
        env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / 'config'))
        runtime = root / 'runtime'
        venv.EnvBuilder(with_pip=False).create(runtime)
        scripts = runtime / ('Scripts' if os.name == 'nt' else 'bin')
        python = scripts / ('python.exe' if os.name == 'nt' else 'python')
        console = scripts / ('novel-creator.exe' if os.name == 'nt' else 'novel-creator')
        run([sys.executable, '-I', '-m', 'pip', '--isolated', '--python', python,
             'install', 'pip', old_wheel], cwd=root, env=env)
        brief = root / 'brief.json'
        brief.write_text('{}')
        novel = root / 'Novel'
        original = json.loads(run([console, 'init', '--path', novel, '--brief-file', brief, '--json'], cwd=root, env=env))
        if (novel / '.novel-creator/workflows/getting-started.md').exists():
            raise ValueError('Historical fixture must predate the new guide')
        before = snapshot(novel)
        run([python, '-I', '-m', 'pip', '--isolated', 'install', '--force-reinstall', '--no-deps', new_wheel], cwd=root, env=env)
        current = json.loads(run([console, 'init', 'Novel', '--json'], cwd=root, env=env))
        if (snapshot(novel) != before or current['checkpoint'] != original['checkpoint']
                or not current['data']['ready'] or not Path(current['data']['getting_started_path']).is_file()
                or 'Package-guide fallback' not in ' '.join(current['warnings'])):
            raise ValueError('Historical novel was changed or continuation/guide fallback failed')
        return dict(old_wheel_sha256=hashlib.sha256(old_wheel.read_bytes()).hexdigest(),
                    new_wheel_sha256=hashlib.sha256(new_wheel.read_bytes()).hexdigest(),
                    files_preserved=len(before), checkpoint_preserved=True,
                    guide_fallback=True, novel_mutations=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old_wheel')
    parser.add_argument('new_wheel')
    args = parser.parse_args()
    print(json.dumps(verify(args.old_wheel, args.new_wheel), indent=2))
