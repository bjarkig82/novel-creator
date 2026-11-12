"""Focused fail-closed checks for GitHub release completion (no publication)."""
import copy
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from scripts import github_release_assets as release


ROOT = Path(__file__).resolve().parents[2]
SELECTION = json.loads((ROOT / '.github/release-assets-0.8.0.json').read_text())


class GithubReleaseAssets(unittest.TestCase):
    def test_pinned_workflow_selection_is_consistent(self):
        workflow = (ROOT / '.github/workflows/github-release-assets.yml').read_text()
        release.verify_selection(SELECTION)
        for name in ['candidate_run', 'artifact_id', 'source_commit']:
            self.assertIn(SELECTION[name], workflow)
        self.assertIn('contents: write', workflow)
        self.assertNotIn('id-token:', workflow)

    def test_publish_requires_both_public_checks_and_real_publish_steps(self):
        run = dict(id=int(SELECTION['publish_run']), run_attempt=2, head_sha=SELECTION['source_commit'],
                   path='.github/workflows/package-release.yml', event='workflow_dispatch',
                   status='completed', conclusion='success')
        steps = {'publish': ['Run python tests/package_release.py verify-remote candidate',
                            'Run pypa/gh-action-pypi-publish@2442bad8f54b06a326f3030ef5e6a7a674118557'],
                 'public-checks (windows-latest)': ['Check named production install and selected archive hash'],
                 'public-checks (ubuntu-latest)': ['Check named production install and selected archive hash']}
        jobs = [dict(name=name, run_id=run['id'], head_sha=run['head_sha'], status='completed',
                     conclusion='success', steps=[dict(name=step, status='completed', conclusion='success')
                                                  for step in names]) for name, names in steps.items()]
        for change in ['valid', 'run-source', 'run-failed', 'incomplete', 'missing-linux',
                       'windows-skipped', 'publish-step-skipped', 'job-source', 'duplicate']:
            selected_run, selected_jobs = copy.deepcopy(run), copy.deepcopy(jobs)
            total = 3
            if change == 'run-source': selected_run['head_sha'] = 'a' * 40
            elif change == 'run-failed': selected_run['conclusion'] = 'failure'
            elif change == 'incomplete': total = 101
            elif change == 'missing-linux': selected_jobs.pop(); total = 2
            elif change == 'windows-skipped': selected_jobs[1]['steps'][0]['conclusion'] = 'skipped'
            elif change == 'publish-step-skipped': selected_jobs[0]['steps'][0]['conclusion'] = 'skipped'
            elif change == 'job-source': selected_jobs[2]['head_sha'] = 'a' * 40
            elif change == 'duplicate': selected_jobs.append(selected_jobs[1]); total = 4
            def api(repository, path):
                return dict(jobs=selected_jobs, total_count=total) if '/jobs?' in path else selected_run
            with self.subTest(change=change), patch.object(release, 'api', side_effect=api):
                if change == 'valid': release.verify_publish(SELECTION)
                else:
                    with self.assertRaises(ValueError): release.verify_publish(SELECTION)

    def test_remote_tag_requires_annotation_and_exact_source(self):
        repository = SELECTION['repository']
        obj = dict(sha=SELECTION['tag_object'], type='tag',
                   url='https://api.github.com/repos/' + repository + '/git/tags/' + SELECTION['tag_object'])
        tag = dict(tag='v0.8.0', object=dict(type='commit', sha=SELECTION['source_commit']))
        for change in ['valid', 'lightweight', 'wrong-object', 'wrong-source']:
            altered_obj, altered_tag = copy.deepcopy(obj), copy.deepcopy(tag)
            if change == 'lightweight': altered_obj['type'] = 'commit'
            elif change == 'wrong-object': altered_obj['sha'] = 'a' * 40
            elif change == 'wrong-source': altered_tag['object']['sha'] = 'a' * 40
            with self.subTest(change=change), patch.object(release, 'api', side_effect=[dict(object=altered_obj), altered_tag]):
                if change == 'valid': release.verify_tag(SELECTION)
                else:
                    with self.assertRaises(ValueError): release.verify_tag(SELECTION)

    def test_public_package_requires_exact_inventory_metadata_and_bytes(self):
        files = {'x.whl': release.sha256(b'wheel'), 'x.tar.gz': release.sha256(b'sdist')}
        manifest = dict(distribution='novel-creator', version='0.8.0', files=files)
        metadata = dict(info=dict(name='novel-creator', version='0.8.0'), urls=[
            dict(filename=name, digests=dict(sha256=digest), size=len(data), yanked=False,
                 url='https://files.pythonhosted.org/' + name)
            for (name, digest), data in zip(files.items(), [b'wheel', b'sdist'])])
        for change in ['valid', 'extra', 'hash', 'bytes', 'yanked', 'version']:
            altered = copy.deepcopy(metadata)
            if change == 'extra': altered['urls'].append(altered['urls'][0])
            elif change == 'hash': altered['urls'][0]['digests']['sha256'] = '0' * 64
            elif change == 'yanked': altered['urls'][0]['yanked'] = True
            elif change == 'version': altered['info']['version'] = '0.7.2'
            downloads = [json.dumps(altered).encode(), b'wrong' if change == 'bytes' else b'wheel', b'sdist']
            with self.subTest(change=change), patch.object(release, 'download', side_effect=downloads):
                if change == 'valid': release.verify_pypi(manifest)
                else:
                    with self.assertRaises(ValueError): release.verify_pypi(manifest)

    def test_source_extraction_rejects_escape_links_and_special_files(self):
        for name, kind in [('root/file', tarfile.REGTYPE), ('../escape', tarfile.REGTYPE),
                           ('/absolute', tarfile.REGTYPE), ('root/link', tarfile.SYMTYPE),
                           ('root/hard', tarfile.LNKTYPE), ('root/fifo', tarfile.FIFOTYPE),
                           ('root/../escape', tarfile.REGTYPE), ('.', tarfile.DIRTYPE)]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                archive = root / 'source.tar.gz'
                with tarfile.open(archive, 'w:gz') as bundle:
                    info = tarfile.TarInfo(name); info.type = kind
                    info.size = 1 if kind == tarfile.REGTYPE else 0
                    info.linkname = '../../outside'
                    bundle.addfile(info, io.BytesIO(b'x') if info.size else None)
                if name == 'root/file':
                    extracted = release.extract_source(archive, root / 'out')
                    self.assertEqual((extracted / 'file').read_bytes(), b'x')
                else:
                    with self.assertRaises(ValueError): release.extract_source(archive, root / 'out')

    def test_existing_release_requires_exact_assets_and_never_mutates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); assets = root / 'assets'; assets.mkdir()
            names = ['a.whl', 'a.tar.gz', 'plugin.zip', 'marketplace.zip']
            for name in names: (assets / name).write_bytes(name.encode())
            existing = dict(id=1, tag_name='v0.8.0', draft=False, prerelease=False, html_url='https://example.test/release')
            inventory = [dict(name=name, state='uploaded', size=len(name),
                              browser_download_url='https://github.com/' + name) for name in names]
            for change in ['valid', 'missing', 'extra', 'bytes', 'draft']:
                altered, entries = copy.deepcopy(existing), copy.deepcopy(inventory)
                if change == 'missing': entries.pop()
                elif change == 'extra': entries.append(entries[0])
                elif change == 'draft': altered['draft'] = True
                with self.subTest(change=change), patch.object(release, 'api', side_effect=[altered, entries]), \
                     patch.object(release, 'download', side_effect=lambda url, **kw: b'wrong' if change == 'bytes' else url.rsplit('/', 1)[1].encode()), \
                     patch.object(release, 'run', side_effect=AssertionError('existing release must never be changed')):
                    if change == 'valid':
                        self.assertEqual(release.complete_release(SELECTION, assets, root, publish=True), existing['html_url'])
                    else:
                        with self.assertRaises(ValueError): release.complete_release(SELECTION, assets, root, publish=True)

    def test_absent_release_is_read_only_without_publish(self):
        with patch.object(release, 'api', return_value=None), \
             patch.object(release, 'run', side_effect=AssertionError('no publication allowed')):
            self.assertIn('--publish was not selected', release.complete_release(SELECTION, Path('/unused'), Path('/unused')))

    def test_create_uses_verified_tag_and_exact_four_assets_then_verifies_remote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); assets = root / 'assets'; assets.mkdir()
            names = ['a.whl', 'a.tar.gz', 'plugin.zip', 'marketplace.zip']
            for name in names: (assets / name).write_bytes(name.encode())
            created = dict(id=1, tag_name='v0.8.0', draft=False, prerelease=False,
                           html_url='https://example.test/release')
            with patch.object(release, 'api', side_effect=[None, created]), \
                 patch.object(release, 'run') as command, patch.object(release, 'verify_release') as verify:
                self.assertEqual(release.complete_release(SELECTION, assets, root, publish=True), created['html_url'])
            argv = command.call_args.args[0]
            self.assertEqual(argv[:4], ['gh', 'release', 'create', 'v0.8.0'])
            self.assertIn('--verify-tag', argv)
            self.assertNotIn('--clobber', argv)
            self.assertEqual(set(argv[-4:]), {str(assets / name) for name in names})
            verify.assert_called_once_with(SELECTION, created, assets)
            notes = (root / 'notes.md').read_text()
            self.assertIn(SELECTION['source_commit'], notes)
            self.assertIn('remain unverified', notes)
