import hashlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.package_release import verify_files


class PackageRelease(unittest.TestCase):
    def test_pip_selection_matches_name_version_filename_and_archive_hash(self):
        from tests.verify_package_install import selected_product
        expected = dict(distribution='novel-creator', version='0.1.0',
                        files={'novel_creator-0.1.0-py3-none-any.whl': 'a' * 64,
                               'novel_creator-0.1.0.tar.gz': 'b' * 64})
        entry = dict(metadata=dict(name='Novel_Creator', version='0.1.0'),
                     download_info=dict(url='https://files.pythonhosted.org/novel_creator-0.1.0-py3-none-any.whl',
                                        archive_info=dict(hashes=dict(sha256='a' * 64))))
        report = dict(version='1', install=[dict(metadata=dict(name='pip', version='26.2')), entry])
        self.assertEqual(selected_product(report, expected)['sha256'], 'a' * 64)
        source = copy.deepcopy(report)
        source['install'][1]['download_info']['url'] = 'https://files.pythonhosted.org/novel_creator-0.1.0.tar.gz'
        source['install'][1]['download_info']['archive_info']['hashes']['sha256'] = 'b' * 64
        self.assertEqual(selected_product(source, expected)['filename'], 'novel_creator-0.1.0.tar.gz')
        for kind in ['hash', 'platform-wheel', 'name', 'version', 'missing', 'duplicate', 'report-version']:
            altered = copy.deepcopy(report)
            if kind == 'hash':
                altered['install'][1]['download_info']['archive_info']['hashes']['sha256'] = 'c' * 64
            elif kind == 'platform-wheel':
                altered['install'][1]['download_info']['url'] = 'https://files.pythonhosted.org/novel_creator-0.1.0-cp313-win_amd64.whl'
            elif kind == 'name':
                altered['install'][1]['metadata']['name'] = 'other-package'
            elif kind == 'version':
                altered['install'][1]['metadata']['version'] = '0.2.0'
            elif kind == 'missing':
                del altered['install'][1]['download_info']['archive_info']
            elif kind == 'duplicate':
                altered['install'].append(copy.deepcopy(entry))
            else:
                altered['version'] = 'unrecognized'
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                selected_product(altered, expected)

    def test_public_install_rejects_different_pip_choice_before_novel_validation(self):
        from tests.verify_package_install import verify
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wheel = 'novel_creator-0.1.0-py3-none-any.whl'
            source = 'novel_creator-0.1.0.tar.gz'
            expected_hash = hashlib.sha256(b'approved').hexdigest()
            expected = dict(distribution='novel-creator', version='0.1.0',
                            files={wheel: expected_hash, source: expected_hash})
            manifest = root / 'manifest.json'
            manifest.write_text(json.dumps(expected))
            metadata = dict(urls=[dict(filename=name, digests=dict(sha256=expected_hash),
                                      url='https://files.pythonhosted.org/' + name) for name in [wheel, source]])
            responses = [io.BytesIO(json.dumps(metadata).encode()), io.BytesIO(b'approved'), io.BytesIO(b'approved')]
            calls = []
            def fake_run(argv, **kwargs):
                calls.append(argv)
                self.assertIn('--report', argv, 'The named pip install must record its actual selection')
                report_path = Path(argv[argv.index('--report') + 1])
                report_path.write_text(json.dumps(dict(version='1', install=[dict(
                    metadata=dict(name='novel-creator', version='0.1.0'), download_info=dict(
                        url='https://files.pythonhosted.org/novel_creator-0.1.0-cp313-win_amd64.whl',
                        archive_info=dict(hashes=dict(sha256='c' * 64))))])))
                return ''
            with patch('tests.verify_package_install.urllib.request.urlopen', side_effect=responses), \
                 patch('tests.verify_package_install.venv.EnvBuilder') as builder, \
                 patch('tests.verify_package_install.run', side_effect=fake_run):
                with self.assertRaises(ValueError):
                    verify(package='novel-creator==0.1.0', manifest=manifest)
            self.assertEqual(len(calls), 1)

    def test_remote_candidate_rejects_identity_and_evidence_mismatches(self):
        from tests.package_release import verify_remote
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ['novel_creator-0.1.0.whl', 'novel_creator-0.1.0.tar.gz']:
                (root / name).write_bytes(name.encode())
            files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
            manifest = dict(repository='o/r', run_id='12', run_attempt='1', source_commit='a' * 40,
                            distribution='novel-creator', version='0.1.0', files=files)
            (root / 'manifest.json').write_text(json.dumps(manifest))
            run = dict(id=12, run_attempt=1, conclusion='success', head_sha='a' * 40,
                       event='workflow_dispatch', path='.github/workflows/package-release.yml')
            artifact = dict(id=34, expired=False, name='candidate-12-1',
                            workflow_run=dict(id=12, head_sha='a' * 40))
            evidence = dict(candidate_run='12', candidate_attempt='1', artifact_id='34', source_commit='a' * 40,
                            files=files, windows_guide=True, linux_guide=True, windows_host=True,
                            linux_host=False, linux_cli=True, evidence_urls=['https://example.com/evidence'])
            env = dict(GITHUB_REPOSITORY='o/r', CANDIDATE_RUN='12', CANDIDATE_ATTEMPT='1',
                       CANDIDATE_ARTIFACT='34', CANDIDATE_COMMIT='a' * 40)
            scenarios = [('run', key, value) for key, value in [('run_attempt', 2), ('head_sha', 'b' * 40),
                ('conclusion', 'failure'), ('path', 'other.yml'), ('event', 'push')]]
            scenarios += [('artifact', 'expired', True), ('artifact', 'id', 35),
                          ('evidence', 'artifact_id', '35'), ('evidence', 'linux_cli', False),
                          ('evidence', 'linux_host', True),
                          ('evidence', 'evidence_urls', [None])]
            for area, key, value in [('valid', '', '')] + scenarios:
                current = dict(run=copy.deepcopy(run), artifact=copy.deepcopy(artifact), evidence=copy.deepcopy(evidence))
                if area != 'valid':
                    current[area][key] = value
                def fake_api(path):
                    return current['run'] if '/runs/' in path else current['artifact']
                with self.subTest(area=area, key=key), patch.dict('os.environ', dict(env, HOST_EVIDENCE=json.dumps(current['evidence']))), \
                     patch('tests.package_release.api', side_effect=fake_api):
                    if area == 'valid':
                        self.assertEqual(verify_remote(root)['version'], '0.1.0')
                    else:
                        with self.assertRaises(ValueError):
                            verify_remote(root)

    def test_public_hash_mismatch_is_rejected_before_installation(self):
        from tests.verify_package_install import verify
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / 'manifest.json'
            expected_hash = hashlib.sha256(b'original').hexdigest()
            manifest.write_text(json.dumps(dict(distribution='novel-creator', version='0.1.0',
                files={'novel_creator-0.1.0.whl': expected_hash, 'novel_creator-0.1.0.tar.gz': expected_hash})))
            for metadata_hash in ['0' * 64, expected_hash]:
                metadata = dict(urls=[dict(filename='novel_creator-0.1.0.whl',
                    digests=dict(sha256=metadata_hash), url='https://files.pythonhosted.org/candidate.whl')])
                responses = [io.BytesIO(json.dumps(metadata).encode()), io.BytesIO(b'changed')]
                with self.subTest(metadata_hash=metadata_hash), \
                     patch('tests.verify_package_install.urllib.request.urlopen', side_effect=responses), \
                     patch('tests.verify_package_install.venv.EnvBuilder', side_effect=AssertionError('must not install')):
                    with self.assertRaises(ValueError):
                        verify(package='novel-creator==0.1.0', manifest=manifest)

    def test_public_empty_manifest_cannot_bypass_hash_checks(self):
        from tests.verify_package_install import verify
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / 'manifest.json'
            manifest.write_text(json.dumps(dict(distribution='novel-creator', version='0.1.0', files={})))
            with patch('tests.verify_package_install.urllib.request.urlopen', side_effect=AssertionError('must validate first')):
                with self.assertRaises(ValueError):
                    verify(package='novel-creator==0.1.0', manifest=manifest)

    def test_public_install_requires_expected_candidate_before_environment_creation(self):
        from tests.verify_package_install import verify
        with patch('tests.verify_package_install.venv.EnvBuilder', side_effect=AssertionError('must validate first')):
            with self.assertRaises(ValueError):
                verify(package='novel-creator==0.1.0')

    def test_candidate_hash_and_identity_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wheel = root / 'novel_creator-0.1.0-py3-none-any.whl'
            wheel.write_bytes(b'candidate wheel')
            source = root / 'novel_creator-0.1.0.tar.gz'
            source.write_bytes(b'candidate source')
            manifest = dict(repository='owner/repo', run_id='12', run_attempt='1',
                            source_commit='a' * 40, distribution='novel-creator', version='0.1.0',
                            files={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [wheel, source]})
            (root / 'manifest.json').write_text(json.dumps(manifest))
            self.assertEqual(verify_files(root, repository='owner/repo', run_id='12',
                run_attempt='1', source_commit='a' * 40)['version'], '0.1.0')
            with self.assertRaises(ValueError):
                verify_files(root, repository='other/repo', run_id='12', run_attempt='1', source_commit='a' * 40)
            wheel.write_bytes(b'changed')
            with self.assertRaises(ValueError):
                verify_files(root, repository='owner/repo', run_id='12', run_attempt='1', source_commit='a' * 40)

    def test_unexpected_files_and_traversal_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = dict(repository='o/r', run_id='1', run_attempt='1', source_commit='b' * 40,
                            distribution='novel-creator', version='0.1.0', files={'../escape.whl': 'a' * 64})
            (root / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                verify_files(root, repository='o/r', run_id='1', run_attempt='1', source_commit='b' * 40)
