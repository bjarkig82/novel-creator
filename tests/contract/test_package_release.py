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

    def test_remote_candidate_requires_automated_platform_checks_and_honest_native_limits(self):
        from tests.package_release import verify_remote
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ['novel_creator-0.1.0.whl', 'novel_creator-0.1.0.tar.gz']:
                (root / name).write_bytes(name.encode())
            files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
            manifest = dict(repository='o/r', run_id='12', run_attempt='1', source_commit='a' * 40,
                            distribution='novel-creator', version='0.1.0', files=files)
            (root / 'manifest.json').write_text(json.dumps(manifest))
            run = dict(id=12, run_attempt=1, status='completed', conclusion='success', head_sha='a' * 40,
                       event='workflow_dispatch', path='.github/workflows/package-release.yml')
            artifact = dict(id=34, expired=False, name='candidate-12-1',
                            workflow_run=dict(id=12, head_sha='a' * 40))
            evidence = dict(candidate_run='12', candidate_attempt='1', artifact_id='34', source_commit='a' * 40,
                            files=files, qualification='automated-only', windows_host=False, linux_host=False)
            env = dict(GITHUB_REPOSITORY='o/r', CANDIDATE_RUN='12', CANDIDATE_ATTEMPT='1',
                       CANDIDATE_ARTIFACT='34', CANDIDATE_COMMIT='a' * 40)
            common_steps = ['Verify candidate manifest', 'Run full unit suite',
                            'Verify wheel bytes and legacy journeys', 'Verify clean wheel installation',
                            'Verify clean installation from the candidate sdist',
                            'Verify plugin runtime installation',
                            'Verify previous published notebook compatibility']
            jobs = dict(total_count=2, jobs=[dict(name='candidate-checks (' + platform + ')',
                run_id=12, head_sha='a' * 40, status='completed', conclusion='success',
                steps=[dict(name=name, status='completed', conclusion='success') for name in
                       common_steps + (['Follow the literal Bash getting-started guide']
                                       if platform == 'ubuntu-latest' else [])])
                for platform in ['windows-latest', 'ubuntu-latest']])
            scenarios = [('run', key, value) for key, value in [('run_attempt', 2), ('head_sha', 'b' * 40),
                ('conclusion', 'failure'), ('status', 'in_progress'), ('path', 'other.yml'), ('event', 'push')]]
            scenarios += [('artifact', 'expired', True), ('artifact', 'id', 35),
                          ('artifact', 'workflow_run', dict(id=13, head_sha='a' * 40)),
                          ('evidence', 'artifact_id', '35'), ('evidence', 'source_commit', 'b' * 40),
                          ('evidence', 'files', {}), ('evidence', 'windows_host', True),
                          ('evidence', 'linux_host', True), ('evidence', 'qualification', 'manual'),
                          ('evidence', 'windows_host', None),
                          ('jobs', 'jobs', []), ('jobs', 'total_count', 101)]
            for change in ['failed', 'skipped-suite', 'missing-wheel', 'wrong-source', 'wrong-run',
                           'missing-linux', 'duplicate-windows', 'missing-guide', 'unfinished']:
                altered = copy.deepcopy(jobs['jobs'])
                if change == 'failed': altered[0]['conclusion'] = 'failure'
                elif change == 'skipped-suite': altered[0]['steps'][1]['conclusion'] = 'skipped'
                elif change == 'missing-wheel': del altered[0]['steps'][2]
                elif change == 'wrong-source': altered[0]['head_sha'] = 'b' * 40
                elif change == 'wrong-run': altered[0]['run_id'] = 13
                elif change == 'missing-linux': altered.pop()
                elif change == 'duplicate-windows': altered.append(copy.deepcopy(altered[0]))
                elif change == 'missing-guide': altered[1]['steps'].pop()
                else: altered[0]['status'] = 'in_progress'
                scenarios.append(('jobs', 'jobs', altered))
            for area, key, value in [('valid', '', '')] + scenarios:
                current = dict(run=copy.deepcopy(run), artifact=copy.deepcopy(artifact),
                               evidence=copy.deepcopy(evidence), jobs=copy.deepcopy(jobs))
                if area != 'valid':
                    current[area][key] = value
                def fake_api(path):
                    if path == '/actions/runs/12/attempts/1/jobs?per_page=100':
                        return current['jobs']
                    if path == '/actions/runs/12/attempts/1':
                        return current['run']
                    if path == '/actions/artifacts/34':
                        return current['artifact']
                    raise AssertionError('Unexpected API request: ' + path)
                with self.subTest(area=area, key=key), patch.dict('os.environ', dict(env, HOST_EVIDENCE=json.dumps(current['evidence']))), \
                     patch('tests.package_release.api', side_effect=fake_api):
                    if area == 'valid':
                        self.assertEqual(verify_remote(root)['version'], '0.1.0')
                    else:
                        with self.assertRaises(ValueError):
                            verify_remote(root)

            # A successful job cannot hide omitted or unsuccessful real plugin checks.
            for platform in ['windows-latest', 'ubuntu-latest']:
                for step_name in ['Verify plugin runtime installation',
                                  'Verify previous published notebook compatibility']:
                    for conclusion in ['skipped', 'failure', 'missing']:
                        current = dict(run=copy.deepcopy(run), artifact=copy.deepcopy(artifact),
                                       evidence=copy.deepcopy(evidence), jobs=copy.deepcopy(jobs))
                        job = next(job for job in current['jobs']['jobs']
                                   if job['name'] == f'candidate-checks ({platform})')
                        if conclusion == 'missing':
                            job['steps'] = [step for step in job['steps'] if step['name'] != step_name]
                        else:
                            step = next(step for step in job['steps'] if step['name'] == step_name)
                            step['conclusion'] = conclusion
                        with self.subTest(platform=platform, step=step_name, conclusion=conclusion), \
                             patch.dict('os.environ', dict(env, HOST_EVIDENCE=json.dumps(evidence))), \
                             patch('tests.package_release.api', side_effect=fake_api):
                            with self.assertRaisesRegex(ValueError,
                                    'Required automated candidate check did not pass: ' + step_name):
                                verify_remote(root)

    def test_windows_coverage_profiles_fail_closed(self):
        from contextlib import chdir
        import subprocess
        from tests.package_release import verify_remote
        from tests.release_checks import WINDOWS_BASELINE
        # Real complete baseline history permits compatibility; only the GitHub boundary is mocked.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', str(Path.cwd()), str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'checkout', '-q', WINDOWS_BASELINE], check=True)
            commit = WINDOWS_BASELINE
            candidate = root / 'candidate'; candidate.mkdir()
            for name in ['a.whl', 'a.tar.gz']: (candidate / name).write_bytes(b'archive')
            files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in candidate.iterdir()}
            base = dict(repository='o/r', run_id='12', run_attempt='1', source_commit=commit, files=files)
            env = dict(GITHUB_REPOSITORY='o/r', CANDIDATE_RUN='12', CANDIDATE_ATTEMPT='1', CANDIDATE_ARTIFACT='34', CANDIDATE_COMMIT=commit,
                HOST_EVIDENCE=json.dumps(dict(candidate_run='12', candidate_attempt='1', artifact_id='34', source_commit=commit, files=files, qualification='automated-only', windows_host=False, linux_host=False)))
            run = dict(id=12, run_attempt=1, status='completed', conclusion='success', head_sha=commit, event='workflow_dispatch', path='.github/workflows/package-release.yml')
            artifact = dict(id=34, expired=False, name='candidate-12-1', workflow_run=dict(id=12, head_sha=commit))
            for profile in [None, 'full', 'compatibility', 'unknown']:
                data = dict(base)
                if profile is not None: data.update(windows_suite=profile, windows_baseline=WINDOWS_BASELINE, windows_reason='test')
                (candidate / 'manifest.json').write_text(json.dumps(data))
                for platform in ['windows-latest', 'ubuntu-latest']:
                    for conclusion in ['success', 'skipped', 'failure', 'missing']:
                        jobs = []
                        for os_name in ['windows-latest', 'ubuntu-latest']:
                            names = ['Verify candidate manifest', ('Run Windows compatibility suite' if profile == 'compatibility' and os_name == 'windows-latest' else 'Run full unit suite'), 'Verify wheel bytes and legacy journeys', 'Verify clean wheel installation', 'Verify clean installation from the candidate sdist']
                            names += ['Verify plugin runtime installation',
                                      'Verify previous published notebook compatibility']
                            if os_name == 'ubuntu-latest': names.append('Follow the literal Bash getting-started guide')
                            steps = [dict(name=n, status='completed', conclusion='success') for n in names]
                            if os_name == platform:
                                if conclusion == 'missing': steps.pop(1)
                                else: steps[1]['conclusion'] = conclusion
                            jobs.append(dict(name='candidate-checks (' + os_name + ')', run_id=12, head_sha=commit, status='completed', conclusion='success', steps=steps))
                        def api(path):
                            if '/jobs?' in path: return dict(total_count=2, jobs=jobs)
                            return artifact if '/artifacts/' in path else run
                        with self.subTest(profile=profile, platform=platform, conclusion=conclusion), chdir(root), patch.dict('os.environ', env), patch('tests.package_release.api', side_effect=api):
                            if profile in [None, 'full', 'compatibility'] and conclusion == 'success': verify_remote(candidate)
                            else:
                                with self.assertRaises(ValueError): verify_remote(candidate)
            # A failed alternate suite must never be hidden by successful selected coverage.
            data = dict(base, windows_suite='compatibility', windows_baseline=WINDOWS_BASELINE, windows_reason='test')
            (candidate / 'manifest.json').write_text(json.dumps(data))
            for job in jobs:
                for step in job['steps']: step['conclusion'] = 'success'
            jobs[1]['steps'].append(dict(name='Run full unit suite', status='completed', conclusion='success'))
            jobs[0]['steps'] = [step for step in jobs[0]['steps'] if step['name'] != 'Run full unit suite']
            jobs[0]['steps'].append(dict(name='Run Windows compatibility suite', status='completed', conclusion='success'))
            for alternate in ['failure', 'success', 'skipped']:
                jobs[0]['steps'].append(dict(name='Run full unit suite', status='completed', conclusion=alternate))
                with chdir(root), patch.dict('os.environ', env), patch('tests.package_release.api', side_effect=api):
                    if alternate == 'failure':
                        with self.assertRaises(ValueError): verify_remote(candidate)
                    else: verify_remote(candidate)
                jobs[0]['steps'].pop()
            # At an exact sensitive source checkout, compatibility is still rejected.
            (root / 'src/novel_creator/storage.py').write_text('# sensitive change')
            subprocess.run(['git', '-C', str(root), 'add', 'src/novel_creator/storage.py'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'sensitive'], check=True)
            commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
            data['source_commit'] = commit
            (candidate / 'manifest.json').write_text(json.dumps(data))
            env['CANDIDATE_COMMIT'] = commit
            evidence = json.loads(env['HOST_EVIDENCE']); evidence['source_commit'] = commit
            env['HOST_EVIDENCE'] = json.dumps(evidence)
            run['head_sha'] = commit; artifact['workflow_run']['head_sha'] = commit
            for job in jobs: job['head_sha'] = commit
            with chdir(root), patch.dict('os.environ', env), patch('tests.package_release.api', side_effect=api):
                with self.assertRaises(ValueError): verify_remote(candidate)
            # Missing history forces full even when a manifest asks for compatibility.
            subprocess.run(['git', '-C', str(root), 'checkout', '-q', '--orphan', 'unrelated'], check=True)
            subprocess.run(['git', '-C', str(root), 'rm', '-rfq', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'unrelated', '--allow-empty'], check=True)
            with chdir(root), patch.dict('os.environ', env), patch('tests.package_release.api', side_effect=api):
                with self.assertRaises(ValueError): verify_remote(candidate)

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
