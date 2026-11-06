"""Conservative Windows release coverage policy and explicit compatibility runner."""
import argparse
import re
import json
from pathlib import Path
import subprocess
import unittest

# Full Windows qualification: tests/evaluations/release-0.6.0.md.
# Refresh manually only after full qualification at the exact replacement source.
WINDOWS_BASELINE = '8df4ca09e58f71d800211a4dad794dd6c1f0c610'
BASELINE_RUN = '42277353584'
BASELINE_ATTEMPT = '1'
COMPATIBILITY_TESTS = (
    'tests.integration.test_path_redirection',
    'tests.contract.test_cli_encoding',
    'tests.integration.test_languages',
    'tests.integration.test_storage.StorageTests.test_clean_save_continuation_and_retry_leave_managed_index_synchronized',
    'tests.integration.test_recovery.RecoveryTests.test_pending_inspection_and_unchanged_retry',
)
# Only known derived runtime modules and non-sensitive tests are routine.
ROUTINE_TESTS = {
    'tests/contract/test_context.py', 'tests/contract/test_working_context.py',
    'tests/contract/test_release_checks.py', 'tests/contract/test_package_release.py',
    'tests/release_checks.py', 'tests/package_release.py',
}


NOTEBOOK_AGENTS = {
    'adapters/codex/notebook/agents/' + name + '.toml' for name in
    ('novel_scene_writer', 'novel_reviewer', 'novel_researcher',
     'novel_orchestrator', 'novel_chapter_writer', 'novel_brainstormer')
}


def routine_path(path):
    return (path in {'README.md', 'AGENTS.md', 'src/novel_creator/context.py',
                     'src/novel_creator/memory.py', '.github/workflows/package-release.yml'}
            or path.startswith(('docs/', 'tests/evaluations/'))
            or (path.startswith(('resources/', 'src/novel_creator/resources/', 'workflows/', 'languages/', 'notebook/', 'adapters/codex/'))
                and path.endswith('.md'))
            or path in NOTEBOOK_AGENTS or path in ROUTINE_TESTS)


def select_windows_suite(root=None, *, baseline=WINDOWS_BASELINE, full=False):
    root = Path(root) if root is not None else Path.cwd()
    def result(profile, reason):
        return dict(profile=profile, baseline=baseline, reason=reason)
    if full:
        return result('full', 'Manual full qualification requested')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)
    try:
        if git('rev-parse', '--is-shallow-repository').strip() != b'false':
            return result('full', 'Complete Git history is required')
        git('merge-base', '--is-ancestor', baseline, 'HEAD')
        paths = git('diff', '--no-renames', '--name-only', '-z', baseline, 'HEAD').decode('utf-8').split('\0')
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        return result('full', 'Baseline history is missing, invalid or not an ancestor')
    def version_only(path):
        if path != 'src/novel_creator/__init__.py':
            return False
        try:
            before = git('show', baseline + ':' + path).decode('utf-8')
            after = git('show', 'HEAD:' + path).decode('utf-8')
        except (subprocess.CalledProcessError, UnicodeError):
            return False
        # Require one plain literal assignment; every other byte must be unchanged.
        pattern = r'(?m)^__version__ = ([\"\'])([0-9]+\.[0-9]+\.[0-9]+)\1$'
        if len(re.findall(pattern, before)) != 1 or len(re.findall(pattern, after)) != 1:
            return False
        return re.sub(pattern, '__version__ = VERSION', before) == re.sub(pattern, '__version__ = VERSION', after)
    sensitive = sorted(path for path in paths if path and not routine_path(path) and not version_only(path))
    if sensitive:
        return result('full', 'Changes require full qualification: ' + ', '.join(sensitive))
    return result('compatibility', 'Cumulative changes are within the routine allowlist')


def validate_windows_suite(data):
    profile = data.get('windows_suite', 'full')  # Historical manifests require full.
    if profile not in ('full', 'compatibility'):
        raise ValueError('Unsupported Windows suite')
    if 'windows_suite' in data:
        if (data.get('windows_baseline') != WINDOWS_BASELINE
                or not isinstance(data.get('windows_reason'), str) or not data['windows_reason']):
            raise ValueError('Invalid Windows qualification policy metadata')
    if profile == 'compatibility':
        try:
            head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, stderr=subprocess.PIPE).strip()
        except (OSError, subprocess.CalledProcessError) as error:
            raise ValueError('Cannot verify candidate source checkout') from error
        if data.get('source_commit') != head:
            raise ValueError('Candidate source checkout does not match manifest')
        if select_windows_suite()['profile'] != 'compatibility':
            raise ValueError('Source changes require full Windows qualification')
    return profile


def load_compatibility_suite(names=COMPATIBILITY_TESTS):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromNames(names)
    if loader.errors or not suite.countTestCases():
        raise ValueError('Compatibility suite is empty or contains missing test IDs: ' + '\n'.join(loader.errors))
    return suite


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--full', action='store_true', help='Request full Windows qualification')
    mode.add_argument('--run', action='store_true', help='Run the explicit compatibility suite')
    mode.add_argument('--list', action='store_true', help='List explicit compatibility test selections')
    args = parser.parse_args()
    if args.list:
        load_compatibility_suite()
        print('\n'.join(COMPATIBILITY_TESTS))
    elif args.run:
        raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(load_compatibility_suite()).wasSuccessful())
    else:
        print(json.dumps(select_windows_suite(full=args.full), indent=2))


if __name__ == '__main__':
    main()
