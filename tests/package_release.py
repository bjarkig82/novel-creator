"""Build manifest and verify an immutable release candidate. Does not publish."""
import argparse
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request
import zipfile

try:
    from tests.release_checks import select_windows_suite, validate_windows_suite
except ModuleNotFoundError:  # Direct invocation: python tests/package_release.py
    from release_checks import select_windows_suite, validate_windows_suite


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_files(root, *, repository, run_id, run_attempt, source_commit):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    for key, expected in dict(repository=repository, run_id=str(run_id), run_attempt=str(run_attempt),
                              source_commit=source_commit).items():
        if manifest.get(key) != expected:
            raise ValueError('Candidate identity mismatch: ' + key)
    validate_windows_suite(manifest)
    names = manifest.get('files', {})
    if (len(names) != 2 or sum(n.endswith('.whl') for n in names) != 1
            or sum(n.endswith('.tar.gz') for n in names) != 1):
        raise ValueError('Candidate must contain exactly one wheel and one sdist')
    if {p.name for p in root.iterdir()} != set(names) | {'manifest.json'}:
        raise ValueError('Candidate has missing or unexpected files')
    for name, expected in names.items():
        if (Path(name).name != name or '/' in name or '\\' in name or name in ('.', '..')
                or not re.fullmatch(r'[0-9a-f]{64}', expected)):
            raise ValueError('Invalid candidate file or checksum')
        path = root / name
        if path.is_symlink() or not path.is_file() or digest(path) != expected:
            raise ValueError('Candidate bytes changed: ' + name)
    return manifest


def manifest(root, *, full=False):
    root = Path(root)
    wheels = list(root.glob('*.whl'))
    sources = list(root.glob('*.tar.gz'))
    if len(wheels) != 1 or len(sources) != 1:
        raise ValueError('Use a fresh directory containing one wheel and one sdist')
    with zipfile.ZipFile(wheels[0]) as archive:
        metadata = [name for name in archive.namelist() if name.endswith('.dist-info/METADATA')]
        info = BytesParser().parsebytes(archive.read(metadata[0]))
    commit = os.environ['GITHUB_SHA']
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Candidate requires an immutable source commit')
    policy = select_windows_suite(full=full)
    if subprocess_head() != commit:
        raise ValueError('Candidate source checkout does not match GITHUB_SHA')
    data = dict(windows_suite=policy['profile'], windows_baseline=policy['baseline'],
                windows_reason=policy['reason'], repository=os.environ['GITHUB_REPOSITORY'], run_id=os.environ['GITHUB_RUN_ID'],
                run_attempt=os.environ['GITHUB_RUN_ATTEMPT'], source_commit=commit,
                distribution=info['Name'], version=info['Version'],
                files={p.name: digest(p) for p in [wheels[0], sources[0]]})
    (root / 'manifest.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    verify_files(root, **{key: data[key] for key in ['repository', 'run_id', 'run_attempt', 'source_commit']})
    return data


def api(path):
    request = urllib.request.Request('https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'] + path,
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def verify_remote(root):
    run_id, attempt, artifact_id = [os.environ[name] for name in ['CANDIDATE_RUN', 'CANDIDATE_ATTEMPT', 'CANDIDATE_ARTIFACT']]
    if not all(re.fullmatch(r'[1-9][0-9]*', value) for value in [run_id, attempt, artifact_id]):
        raise ValueError('Candidate run/attempt/artifact must be positive numeric identifiers')
    commit = os.environ['CANDIDATE_COMMIT']
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Full candidate source commit is required')
    run = api(f'/actions/runs/{run_id}/attempts/{attempt}')
    artifact = api(f'/actions/artifacts/{artifact_id}')
    if (run.get('id') != int(run_id) or run.get('run_attempt') != int(attempt)
            or run.get('status') != 'completed' or run.get('conclusion') != 'success'
            or run.get('head_sha') != commit
            or run.get('event') != 'workflow_dispatch'
            or run.get('path') != '.github/workflows/package-release.yml'
            or artifact.get('id') != int(artifact_id) or artifact.get('expired') is not False
            or artifact.get('workflow_run', {}).get('id') != int(run_id)
            or artifact.get('workflow_run', {}).get('head_sha') != commit
            or artifact.get('name') != f'candidate-{run_id}-{attempt}'):
        raise ValueError('Candidate workflow/artifact is missing, expired, unsuccessful or mismatched')
    data = verify_files(root, repository=os.environ['GITHUB_REPOSITORY'], run_id=run_id,
                        run_attempt=attempt, source_commit=commit)
    evidence = json.loads(os.environ.get('HOST_EVIDENCE', '{}'))
    expected = dict(candidate_run=run_id, candidate_attempt=attempt, artifact_id=artifact_id,
                    source_commit=commit, files=data['files'])
    if any(evidence.get(key) != value for key, value in expected.items()):
        raise ValueError('Qualification evidence is not bound to this candidate')
    if evidence.get('qualification') != 'automated-only':
        raise ValueError('This release requires automated-only qualification')
    if any(evidence.get(key) is not False for key in ['windows_host', 'linux_host']):
        raise ValueError('Both native Codex Desktop integrations must remain explicitly unverified')
    jobs = api(f'/actions/runs/{run_id}/attempts/{attempt}/jobs?per_page=100')
    if jobs.get('total_count') != len(jobs.get('jobs', [])):
        raise ValueError('Candidate job response is incomplete')
    profile = validate_windows_suite(data)
    common_steps = {'Verify candidate manifest',
                    'Verify plugin runtime installation',
                    'Verify previous published notebook compatibility',
                    'Verify wheel bytes and legacy journeys', 'Verify clean wheel installation',
                    'Verify clean installation from the candidate sdist'}
    for platform in ['windows-latest', 'ubuntu-latest']:
        matches = [job for job in jobs['jobs'] if job.get('name') == f'candidate-checks ({platform})']
        if len(matches) != 1:
            raise ValueError('Candidate platform qualification is missing or ambiguous: ' + platform)
        job = matches[0]
        if (job.get('run_id') != int(run_id) or job.get('head_sha') != commit
                or job.get('status') != 'completed' or job.get('conclusion') != 'success'):
            raise ValueError('Candidate platform qualification is unsuccessful or mismatched: ' + platform)
        suite_name = ('Run Windows compatibility suite' if platform == 'windows-latest'
                      and profile == 'compatibility' else 'Run full unit suite')
        # Extra full coverage is acceptable, but a failed alternate suite is never ignored.
        suite_steps = [step for step in job.get('steps', []) if step.get('name') in
                       {'Run full unit suite', 'Run Windows compatibility suite'}]
        if any(step.get('status') != 'completed' or step.get('conclusion') not in ('success', 'skipped')
               for step in suite_steps):
            raise ValueError('Candidate suite failed or is unfinished')
        if platform == 'windows-latest' and profile == 'compatibility':
            if any(step.get('name') == 'Run full unit suite' and step.get('status') == 'completed'
                   and step.get('conclusion') == 'success' for step in suite_steps):
                suite_name = 'Run full unit suite'
        required = common_steps | {suite_name} | ({'Follow the literal Bash getting-started guide'}
                                   if platform == 'ubuntu-latest' else set())
        for name in required:
            steps = [step for step in job.get('steps', []) if step.get('name') == name]
            if (len(steps) != 1 or steps[0].get('status') != 'completed'
                    or steps[0].get('conclusion') != 'success'):
                raise ValueError('Required automated candidate check did not pass: ' + name)
    # These are verified runner results, not native conversation or literary acceptance.
    return data


def subprocess_head():
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['manifest', 'verify', 'verify-remote'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('--full', action='store_true', help='Request full Windows qualification at build time')
    args = parser.parse_args()
    if args.operation == 'manifest':
        result = manifest(args.directory, full=args.full)
    elif args.operation == 'verify-remote':
        result = verify_remote(args.directory)
    else:
        data = json.loads((args.directory / 'manifest.json').read_text(encoding='utf-8'))
        # Local verification checks bytes; remote mode additionally checks externally selected identity.
        result = verify_files(args.directory, **{key: data[key] for key in ['repository', 'run_id', 'run_attempt', 'source_commit']})
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write('windows_suite=' + result.get('windows_suite', 'full') + '\n')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as stream:
            stream.write('Windows suite: ' + result.get('windows_suite', 'full') + '\n\n'
                         + 'Baseline: ' + result.get('windows_baseline', 'legacy full') + '\n\n'
                         + result.get('windows_reason', 'Historical full qualification') + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
