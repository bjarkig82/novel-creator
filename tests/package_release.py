"""Build manifest and verify an immutable release candidate. Does not publish."""
import argparse
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlparse
import zipfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_files(root, *, repository, run_id, run_attempt, source_commit):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    for key, expected in dict(repository=repository, run_id=str(run_id), run_attempt=str(run_attempt),
                              source_commit=source_commit).items():
        if manifest.get(key) != expected:
            raise ValueError('Candidate identity mismatch: ' + key)
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


def manifest(root):
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
    data = dict(repository=os.environ['GITHUB_REPOSITORY'], run_id=os.environ['GITHUB_RUN_ID'],
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
            or run.get('conclusion') != 'success' or run.get('head_sha') != commit
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
        raise ValueError('Host/guide evidence is not bound to this candidate')
    if not all(evidence.get(key) is True for key in ['windows_guide', 'linux_guide', 'windows_host', 'linux_host']):
        raise ValueError('Required guide and actual-host checks are not confirmed')
    if not isinstance(evidence.get('evidence_urls'), list) or not evidence['evidence_urls']:
        raise ValueError('Traceable guide/host evidence URLs are required')
    if any(not isinstance(url, str) or urlparse(url).scheme != 'https' or not urlparse(url).netloc
           for url in evidence['evidence_urls']):
        raise ValueError('Evidence URLs must be nonempty HTTPS URLs')
    # This checks binding and declarations, not literary quality or independent human approval.
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['manifest', 'verify', 'verify-remote'])
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    if args.operation == 'manifest':
        result = manifest(args.directory)
    elif args.operation == 'verify-remote':
        result = verify_remote(args.directory)
    else:
        data = json.loads((args.directory / 'manifest.json').read_text(encoding='utf-8'))
        # Local verification checks bytes; remote mode additionally checks externally selected identity.
        result = verify_files(args.directory, **{key: data[key] for key in ['repository', 'run_id', 'run_attempt', 'source_commit']})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
