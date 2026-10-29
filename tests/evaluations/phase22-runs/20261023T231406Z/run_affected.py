"""Run current affected installed checks; create only temporary test repositories."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[4]
folder = Path(__file__).resolve().parent
environment = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
modules = ['tests.unit.test_evaluation_observation', 'tests.integration.test_install',
    'tests.integration.test_initialize_journey', 'tests.integration.test_guidance_journey',
    'tests.integration.test_resume_journey', 'tests.integration.test_portable_install',
    'tests.integration.test_languages', 'tests.integration.test_host_input']
command = [sys.executable, '-B', '-m', 'unittest', *modules]
started = time.monotonic()
result = subprocess.run(command, cwd=root, env=environment, capture_output=True,
                        encoding='utf-8', timeout=600)
platform = 'windows' if os.name == 'nt' else 'linux'
(folder / f'{platform}-affected-tests.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
report = {'command': command, 'exit_code': result.returncode,
          'elapsed_seconds': time.monotonic() - started, 'scope': 'Affected automated installed checks only'}
(folder / f'{platform}-affected-tests.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report))
sys.exit(result.returncode)
