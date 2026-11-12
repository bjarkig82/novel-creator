"""Verify a published immutable candidate, then optionally attach GitHub assets.

The selection JSON is reviewed release evidence, not workflow dispatch input.
The default performs read-only remote checks and writes disposable local outputs.
Only --publish may create a release; existing releases must match every asset.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.error
import urllib.parse
import urllib.request


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, **kwargs):
    return subprocess.check_output(argv, text=True, **kwargs).strip()


def api(repository, path, *, missing_ok=False):
    request = urllib.request.Request('https://api.github.com/repos/' + repository + path,
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if missing_ok and error.code == 404:
            return None
        raise


def download(url, *, hostname):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != hostname or parsed.username or parsed.password:
        raise ValueError('Unexpected download origin: ' + url)
    # Public byte downloads never carry the GitHub credential across redirects.
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def verify_selection(selection):
    for key in ['candidate_run', 'candidate_attempt', 'artifact_id', 'publish_run', 'publish_attempt']:
        if not re.fullmatch(r'[1-9][0-9]*', selection[key]):
            raise ValueError('Invalid selected identifier: ' + key)
    for key in ['source_commit', 'tag_object']:
        if not re.fullmatch(r'[0-9a-f]{40}', selection[key]):
            raise ValueError('Invalid selected Git object: ' + key)
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', selection['repository']):
        raise ValueError('Invalid repository')
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', selection['version']):
        raise ValueError('Expected a stable package version')
    if os.environ.get('GITHUB_REPOSITORY', selection['repository']) != selection['repository']:
        raise ValueError('Selected repository differs from workflow repository')


def verify_candidate(selection, source, candidate):
    if run(['git', '-C', str(source), 'rev-parse', 'HEAD']) != selection['source_commit']:
        raise ValueError('Verifier must run from the exact qualified source checkout')
    env = dict(os.environ, GITHUB_REPOSITORY=selection['repository'],
               CANDIDATE_RUN=selection['candidate_run'], CANDIDATE_ATTEMPT=selection['candidate_attempt'],
               CANDIDATE_ARTIFACT=selection['artifact_id'], CANDIDATE_COMMIT=selection['source_commit'],
               HOST_EVIDENCE=json.dumps(selection['host_evidence']))
    # The qualified source supplies its unchanged source-bound release gates.
    data = json.loads(run([sys.executable, 'tests/package_release.py', 'verify-remote', str(candidate)],
                          cwd=source, env=env))
    if (data['version'] != selection['version'] or data['distribution'] != 'novel-creator'
            or data['files'] != selection['host_evidence']['files']):
        raise ValueError('Candidate package differs from selected release')
    return data


def verify_publish(selection):
    repository = selection['repository']
    path = '/actions/runs/' + selection['publish_run'] + '/attempts/' + selection['publish_attempt']
    release_run = api(repository, path)
    if (release_run.get('id') != int(selection['publish_run'])
            or release_run.get('run_attempt') != int(selection['publish_attempt'])
            or release_run.get('head_sha') != selection['source_commit']
            or release_run.get('path') != '.github/workflows/package-release.yml'
            or release_run.get('event') != 'workflow_dispatch'
            or release_run.get('status') != 'completed' or release_run.get('conclusion') != 'success'):
        raise ValueError('Selected publish run is unsuccessful or source mismatched')
    result = api(repository, path + '/jobs?per_page=100')
    jobs = result.get('jobs', [])
    if result.get('total_count') != len(jobs):
        raise ValueError('Incomplete publish job response')
    requirements = {
        'publish': {'Run python tests/package_release.py verify-remote candidate',
                    'Run pypa/gh-action-pypi-publish@2442bad8f54b06a326f3030ef5e6a7a674118557'},
        'public-checks (windows-latest)': {'Check named production install and selected archive hash'},
        'public-checks (ubuntu-latest)': {'Check named production install and selected archive hash'},
    }
    for name, steps in requirements.items():
        matches = [job for job in jobs if job.get('name') == name]
        if len(matches) != 1:
            raise ValueError('Missing or ambiguous publish job: ' + name)
        job = matches[0]
        if (job.get('run_id') != int(selection['publish_run'])
                or job.get('head_sha') != selection['source_commit']
                or job.get('status') != 'completed' or job.get('conclusion') != 'success'):
            raise ValueError('Unsuccessful or mismatched publish job: ' + name)
        for step_name in steps:
            matches = [step for step in job.get('steps', []) if step.get('name') == step_name]
            if (len(matches) != 1 or matches[0].get('status') != 'completed'
                    or matches[0].get('conclusion') != 'success'):
                raise ValueError('Required publish check did not pass: ' + step_name)


def verify_tag(selection):
    repository = selection['repository']
    ref = api(repository, '/git/ref/tags/v' + selection['version'])
    if ref.get('object') != {'sha': selection['tag_object'], 'type': 'tag',
                            'url': 'https://api.github.com/repos/' + repository + '/git/tags/' + selection['tag_object']}:
        raise ValueError('Remote tag is not the selected annotated tag')
    tag = api(repository, '/git/tags/' + selection['tag_object'])
    if (tag.get('tag') != 'v' + selection['version'] or tag.get('object', {}).get('type') != 'commit'
            or tag.get('object', {}).get('sha') != selection['source_commit']):
        raise ValueError('Annotated tag does not target the qualified source')


def verify_pypi(manifest):
    url = 'https://pypi.org/pypi/' + manifest['distribution'] + '/' + manifest['version'] + '/json'
    metadata = json.loads(download(url, hostname='pypi.org'))
    if (metadata.get('info', {}).get('name') != manifest['distribution']
            or metadata.get('info', {}).get('version') != manifest['version']):
        raise ValueError('Public package identity differs')
    entries = metadata.get('urls', [])
    if len(entries) != 2 or {entry.get('filename') for entry in entries} != set(manifest['files']):
        raise ValueError('Public package file inventory differs')
    for entry in entries:
        expected = manifest['files'][entry['filename']]
        if entry.get('yanked') is not False or entry.get('digests', {}).get('sha256') != expected:
            raise ValueError('Public package metadata differs: ' + entry['filename'])
        data = download(entry['url'], hostname='files.pythonhosted.org')
        if len(data) != entry.get('size') or sha256(data) != expected:
            raise ValueError('Public package bytes differ: ' + entry['filename'])


def extract_source(archive_path, destination):
    """Extract only regular files/directories below a single root, never links."""
    with tarfile.open(archive_path, 'r:gz') as archive:
        members = archive.getmembers()
        names = set()
        roots = set()
        for member in members:
            path = PurePosixPath(member.name)
            if (not member.name or not path.parts or path.is_absolute() or '..' in path.parts
                    or '\\' in member.name or member.name in names
                    or not (member.isfile() or member.isdir())):
                raise ValueError('Unsafe source archive member: ' + member.name)
            names.add(member.name)
            roots.add(path.parts[0])
        if len(roots) != 1:
            raise ValueError('Source archive must contain exactly one root')
        archive.extractall(destination, members=members, filter='data')
    return destination / roots.pop()


def build_assets(selection, manifest, candidate, output):
    output.mkdir(parents=True, exist_ok=False)
    extracted = extract_source(candidate / next(n for n in manifest['files'] if n.endswith('.tar.gz')),
                               output / 'source')
    assets = output / 'assets'
    assets.mkdir()
    run([sys.executable, str(extracted / 'scripts/build_plugins.py'), '--check'])
    run([sys.executable, str(extracted / 'scripts/build_plugins.py'), '--output', str(assets)])
    expected_plugins = {'novel-creator-' + kind + '-' + manifest['version'] + '.zip'
                        for kind in ['plugin', 'marketplace']}
    if set(selection['plugin_archives']) != expected_plugins:
        raise ValueError('Expected exactly the plugin and marketplace ZIPs')
    actual = {path.name: sha256(path.read_bytes()) for path in assets.iterdir()}
    if actual != selection['plugin_archives']:
        raise ValueError('Reproduced plugin ZIPs differ from selected hashes')
    for name in manifest['files']:
        shutil.copyfile(candidate / name, assets / name)
    return assets


def verify_release(selection, release, assets):
    if (release.get('tag_name') != 'v' + selection['version']
            or release.get('draft') is not False or release.get('prerelease') is not False):
        raise ValueError('Existing release metadata differs')
    inventory = api(selection['repository'], '/releases/' + str(release['id']) + '/assets?per_page=100')
    expected = {path.name: path for path in assets.iterdir()}
    if len(inventory) != 4 or {entry.get('name') for entry in inventory} != set(expected):
        raise ValueError('Existing release asset inventory differs; refusing to overwrite')
    for entry in inventory:
        local = expected[entry['name']].read_bytes()
        if entry.get('state') != 'uploaded' or entry.get('size') != len(local):
            raise ValueError('Existing release asset size/state differs')
        remote = download(entry['browser_download_url'], hostname='github.com')
        if sha256(remote) != sha256(local):
            raise ValueError('Existing release asset bytes differ: ' + entry['name'])


def complete_release(selection, assets, output, *, publish=False):
    repository = selection['repository']
    tag = 'v' + selection['version']
    path = '/releases/tags/' + tag
    existing = api(repository, path, missing_ok=True)
    if existing is not None:
        verify_release(selection, existing, assets)
        return existing['html_url']
    if not publish:
        return 'Verified assets prepared; GitHub release is absent (--publish was not selected).'
    base = 'https://github.com/' + repository
    source = selection['source_commit']
    notes = output / 'notes.md'
    notes.write_text(
        f"Novel Creator {selection['version']} adds installable Codex and Claude Code plugins, "
        "with guided English/Icelandic notebook setup and fifteen shared writing skills.\n\n"
        f"- [Release notes]({base}/blob/main/docs/releases/{selection['version']}.md)\n"
        f"- [Marketplace installation guide]({base}/blob/main/docs/plugin-marketplaces.md)\n"
        f"- [Qualified source]({base}/commit/{source})\n"
        f"- [Candidate qualification]({base}/actions/runs/{selection['candidate_run']}) and "
        f"[published Windows/Linux checks]({base}/actions/runs/{selection['publish_run']})\n\n"
        "Qualification is automated-only. Native Codex Desktop integration on Windows and Linux, "
        "GUI skill discovery, native conversation behavior and writing quality remain unverified.\n",
        encoding='utf-8')
    run(['gh', 'release', 'create', tag, '--repo', repository, '--verify-tag', '--title', tag,
         '--notes-file', str(notes), *[str(path) for path in sorted(assets.iterdir())]])
    created = api(repository, path)
    verify_release(selection, created, assets)
    return created['html_url']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['selection', 'source', 'candidate', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    selection = json.loads(args.selection.read_text(encoding='utf-8'))
    verify_selection(selection)
    source, candidate, output = [path.resolve() for path in [args.source, args.candidate, args.output]]
    manifest = verify_candidate(selection, source, candidate)
    verify_publish(selection)
    verify_tag(selection)
    verify_pypi(manifest)
    assets = build_assets(selection, manifest, candidate, output)
    result = complete_release(selection, assets, output, publish=args.publish)
    print(result)


if __name__ == '__main__':
    main()
