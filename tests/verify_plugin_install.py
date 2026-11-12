"""Opt-in candidate plugin/runtime installation checks; may download dependencies.

Uses disposable runtime and book directories, without changing host configuration.
This verifies installed files and CLI behavior, not native host conversations.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    """Keep qualification checks active even when Python runs with -O."""
    if not condition:
        raise AssertionError(message)


def run(command, *, env, cwd, expected_exit=0):
    result = subprocess.run([str(value) for value in command], env=env, cwd=cwd,
                            capture_output=True, text=True, encoding='utf-8', timeout=180)
    if result.returncode != expected_exit:
        raise RuntimeError(f'Command returned {result.returncode}, expected {expected_exit}: '
                           f'{command}\n{result.stdout[-2500:]}\n{result.stderr[-1000:]}')
    return result.stdout


def temporary_environment(scratch):
    env = os.environ.copy()
    for name in ('PYTHONPATH', 'PYTHONHOME', 'PIP_TARGET', 'PIP_PREFIX', 'PIP_USER',
                 'PIP_ROOT', 'PIP_PYTHON', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE',
                 'GIT_COMMON_DIR', 'GIT_CONFIG', 'GIT_CONFIG_COUNT', 'GIT_CONFIG_PARAMETERS'):
        env.pop(name, None)
    # Both cache variables are scoped to this process, supporting Windows/Linux.
    env.update(XDG_CACHE_HOME=str(scratch / 'cache'), LOCALAPPDATA=str(scratch / 'local'),
               GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_AUTHOR_NAME='Plugin Qualification', GIT_AUTHOR_EMAIL='test@example.invalid',
               GIT_COMMITTER_NAME='Plugin Qualification', GIT_COMMITTER_EMAIL='test@example.invalid')
    return env


def snapshot(book, *, include_git=False):
    return {path.relative_to(book).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in book.rglob('*') if path.is_file()
            and (include_git or '.git' not in path.relative_to(book).parts)}


def bootstrap(plugin, wheel, scratch, env):
    result = json.loads(run([sys.executable, plugin / 'scripts/bootstrap.py', '--wheel', wheel,
                             '--novel', scratch / 'Book en'], env=env, cwd=scratch))
    require(result.get('ok'), f'Runtime bootstrap failed: {result}')
    return result['data']


def write_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


def verify(*, plugin, wheel):
    with tempfile.TemporaryDirectory(prefix='novel-marketplace-runtime-') as temporary:
        scratch = Path(temporary).resolve()
        env = temporary_environment(scratch)
        first = bootstrap(plugin, wheel, scratch, env)
        require(not first['reused'], 'First bootstrap unexpectedly reused a runtime')
        repeat = bootstrap(plugin, wheel, scratch, env)
        require(repeat['reused'], 'Second bootstrap did not reuse the runtime')
        require(first['runtime_python'] == repeat['runtime_python'], 'Runtime interpreter changed')
        python = first['runtime_python']
        checks = []
        for language in ('en', 'is'):
            book = scratch / f'Bréf Þóru {language}'
            created = json.loads(run([python, '-I', '-m', 'novel_creator', 'notebook', 'init',
                                      book.name, '--path', book, '--language', language,
                                      '--host', 'both', '--skill-source', 'plugin', '--json'],
                                     env=env, cwd=scratch))
            require(created.get('ok') and created['data']['ready'], f'Notebook not ready: {created}')
            for relative in ('.agents/skills', '.claude/skills'):
                require(not (book / relative).exists(), f'Unexpected local skills: {relative}')
            for relative, pattern in (('.codex/agents', '*.toml'), ('.claude/agents', '*.md')):
                require(len(list((book / relative).glob(pattern))) == 6,
                        f'Expected six native role definitions in {relative}')
            for relative in ('AGENTS.md', 'CLAUDE.md'):
                require((book / relative).is_file(), f'Missing instructions: {relative}')
            marker = json.loads((book / '.novel-notebook/integration.json').read_text(encoding='utf-8'))
            require(marker == {'version': 1, 'host': 'both', 'skill_source': 'plugin'},
                    f'Unexpected integration marker: {marker}')
            for path in book.rglob('*'):
                if path.is_file() and path.suffix in ('.md', '.toml'):
                    links = re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', path.read_text(encoding='utf-8'))
                    for link in links:
                        if not re.match(r'[a-z]+:', link):
                            require((path.parent / link).is_file(), f'Broken link: {path}: {link}')
            require(run(['git', '-C', book, 'status', '--porcelain'], env=env, cwd=scratch) == '',
                    'Initialized notebook has uncommitted changes')
            before = snapshot(book, include_git=True)
            refusal = json.loads(run([python, '-I', '-m', 'novel_creator', 'notebook', 'update',
                                      '--path', book, '--json'], env=env, cwd=scratch, expected_exit=3))
            require(not refusal['ok'], 'Updater accepted unsupported plugin layout')
            require(before == snapshot(book, include_git=True), 'Refused update changed files')
            checks.append({'language': language, 'host': 'both', 'skill_source': 'plugin',
                           'instructions': 2, 'native_agents': 12, 'local_skills': 0,
                           'links': 'resolved', 'git': 'clean', 'updater': 'refused without mutation'})
        return {'ok': True, 'version': first['version'],
                'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
                'plugin_root': str(plugin), 'runtime_created': True, 'runtime_reused': True,
                'isolated_dependency_checks': 'passed', 'notebooks': checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', type=Path, required=True, help='Exact local candidate wheel')
    parser.add_argument('--plugin', type=Path, default=ROOT / 'plugins/novel-creator',
                        help='Plugin root; select an installed cache to qualify installed bytes')
    parser.add_argument('--report', type=Path, required=True, help='Success JSON report destination')
    args = parser.parse_args()
    write_report(args.report.resolve(), verify(plugin=args.plugin.resolve(), wheel=args.wheel.resolve()))


if __name__ == '__main__':
    main()
