"""Exercise the guide's six diagnostic/recovery categories against an installed runtime."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


def verify(python, console, workspace):
    python, console, root = [Path(p).absolute() for p in (python, console, workspace)]
    root.mkdir(parents=True, exist_ok=False)
    home = root / 'home'
    home.mkdir()
    identity = home / '.gitconfig'
    identity.write_text('[user]\nname = Disposable Guide Test\nemail = guide@example.invalid\n')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PYTHON', 'GIT_', 'PIP_'))}
    env.update(HOME=str(home), USERPROFILE=str(home), GIT_CONFIG_GLOBAL=str(identity),
               XDG_CONFIG_HOME=str(home / 'config'), GIT_CONFIG_NOSYSTEM='1', PYTHONUTF8='1')

    def run(args, code=0, override=None):
        result = subprocess.run([str(a) for a in args], cwd=root, env=env | (override or {}),
                                capture_output=True, text=True, encoding='utf-8', timeout=180)
        if result.returncode != code:
            raise RuntimeError(f'Expected {code}, got {result.returncode}: {result.stderr}')
        return result.stdout

    cases = []
    try:
        run(['novel-creator', '--version'], override={'PATH': ''})
        raise AssertionError('Command unexpectedly found without PATH')
    except FileNotFoundError:
        pass
    assert run([console, '--version']).startswith('novel-creator ')
    cases.append({'category': 'command unavailable', 'recovery': 'explicit executable path', 'passed': True})

    missing = json.loads(run([console, 'init', 'MissingGit', '--json'], code=5, override={'PATH': ''}))
    assert not missing['ok'] and 'git' in missing['error']['message'].lower()
    assert not (root / 'MissingGit').exists()
    cases.append({'category': 'prerequisite unavailable', 'diagnostic': missing['error']['message'], 'passed': True})

    empty = root / 'empty-home'
    empty.mkdir()
    missing = json.loads(run([console, 'init', 'MissingIdentity', '--json'], code=5,
                            override={'HOME': str(empty), 'USERPROFILE': str(empty),
                                      'XDG_CONFIG_HOME': str(empty / 'config')}))
    assert not missing['ok'] and 'identity' in missing['error']['message'].lower()
    assert not (root / 'MissingIdentity').exists()
    cases.append({'category': 'Git identity missing', 'diagnostic': missing['error']['message'], 'passed': True})

    occupied = root / 'Occupied'
    occupied.mkdir()
    marker = occupied / 'keep.txt'
    marker.write_bytes(b'Preserve unrelated content\r\n')
    before = hashlib.sha256(marker.read_bytes()).hexdigest()
    refused = json.loads(run([console, 'init', 'Occupied', '--json'], code=3))
    assert not refused['ok'] and hashlib.sha256(marker.read_bytes()).hexdigest() == before
    assert sorted(p.name for p in occupied.iterdir()) == ['keep.txt']
    fresh = json.loads(run([console, 'init', 'SafeAlternative', '--json']))
    assert fresh['data']['ready']
    cases.append({'category': 'unsafe destination', 'recovery': 'separate fresh destination', 'passed': True})

    permission_code = """
from unittest.mock import patch
from novel_creator.cli import main
with patch('pathlib.Path.mkdir', side_effect=PermissionError('Injected disposable permission failure')):
    raise SystemExit(main(['init', 'PermissionFailure', '--json']))
"""
    denied = json.loads(run([python, '-I', '-c', permission_code], code=5))
    assert not denied['ok'] and 'permissions' in denied['error']['message'].lower()
    assert not (root / 'PermissionFailure').exists()
    cases.append({'category': 'permission failure', 'injection': 'installed CLI filesystem boundary',
                  'diagnostic': denied['error']['message'], 'passed': True})

    interrupted_code = """
import json
from novel_creator.cli import parser, _init_request, ToolError
from novel_creator.install import initialize
args=parser().parse_args(['init','Interrupted','--json'])
request=_init_request(args)
def fault(point):
    if point == 'after_file':
        raise OSError('Injected disposable interruption')
try:
    initialize(request['resolved_destination'], '{"title":"Interrupted"}', request=request, fault=fault)
except ToolError as error:
    assert error.code == 5
else:
    raise AssertionError('Expected interrupted initial save')
"""
    run([python, '-I', '-c', interrupted_code])
    novel = root / 'Interrupted'
    state = json.loads((novel / '.novel-creator/local/setup/state.json').read_text(encoding='utf-8'))
    recovered = json.loads(run([console, 'init', 'Interrupted', '--json']))
    history = list((novel / 'story/exchanges').glob('*.json'))
    assert recovered['data']['ready'] and len(history) == 1
    assert json.loads(history[0].read_text(encoding='utf-8')) == state['bundle']
    assert recovered['checkpoint']['exchange_id'] == state['bundle']['exchange_id']
    cases.append({'category': 'interrupted initialization', 'recovery': 'unchanged original command',
                  'same_saved_bundle': True, 'passed': True})
    return {'runtime_python': str(python), 'workspace': str(root), 'cases': cases,
            'all_six_passed': True, 'host_evidence': False, 'permission_failure_is_injected': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--python', required=True)
    p.add_argument('--console', required=True)
    p.add_argument('--workspace', required=True)
    args = p.parse_args()
    print(json.dumps(verify(args.python, args.console, args.workspace), ensure_ascii=False, indent=2))
