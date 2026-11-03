"""Optional GitHub transport. No authentication setup, implicit forks or shell input."""
import json
import os
from pathlib import Path
import subprocess

from .cli import ToolError

REPOSITORY = 'bjarkig82/novel-creator'
ORIGIN = 'https://github.com/' + REPOSITORY + '.git'


def canonical_origin(value):
    if value not in (ORIGIN, ORIGIN.removesuffix('.git'),
                     'git@github.com:' + REPOSITORY + '.git',
                     'ssh://git@github.com/' + REPOSITORY + '.git'):
        raise ToolError(3, 'Configured checkout is not the designated upstream')
    return ORIGIN


def environment():
    # Keep credential discovery, not caller-controlled repository/host overrides.
    names = ('PATH', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT', 'HOME',
             'USERPROFILE', 'APPDATA', 'LOCALAPPDATA', 'XDG_CONFIG_HOME',
             'TEMP', 'TMP', 'SSH_AUTH_SOCK', 'GH_TOKEN', 'GITHUB_TOKEN')
    result = {k: os.environ[k] for k in names if k in os.environ}
    result.update(GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1',
                  GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
    return result


def command(argv, *, cwd=None, input=None):
    try:
        result = subprocess.run(argv, cwd=cwd, env=environment(), input=input,
                                capture_output=True, timeout=120)
    except FileNotFoundError as error:
        raise ToolError(4, 'Required contribution executable is unavailable') from error
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ToolError(5, 'Contribution operation outcome is unavailable; inspect local receipt') from error
    if result.returncode:
        raise ToolError(5, 'Contribution operation failed; inspect local receipt')
    return result.stdout


def git(root, *args, input=None, guard=None):
    if 'fetch' in args or 'push' in args:
        verify_transport(root, guard=guard)
    if guard is not None:
        guard()
    return command(['git', '-C', str(root), '-c', 'core.hooksPath=/dev/null',
                    '-c', 'core.fsmonitor=false', '-c', 'commit.gpgsign=false', *args], input=input)


def verify_transport(root, *, guard=None):
    canonical_origin(git(root, 'remote', 'get-url', 'origin', guard=guard).decode().strip())
    config = git(root, 'config', '--null', '--list', guard=guard)
    for entry in config.split(b'\0'):
        key = entry.partition(b'\n')[0].lower()
        if key.startswith(b'url.') and key.endswith((b'.insteadof', b'.pushinsteadof')):
            raise ToolError(3, 'Git URL rewrites require inspection before contribution work')
    effective = git(root, 'ls-remote', '--get-url', ORIGIN, guard=guard).decode().strip()  # No network with --get-url.
    if effective != ORIGIN:
        raise ToolError(3, 'Effective Git transport differs from the designated upstream')


class Github:
    guard = None

    def check(self):
        if self.guard is not None:
            self.guard()

    def get(self, endpoint):
        self.check()
        raw = command(['gh', 'api', '--hostname', 'github.com', '--method', 'GET', endpoint])
        try:
            return json.loads(raw)
        except (ValueError, UnicodeError) as error:
            raise ToolError(5, 'GitHub metadata is unavailable') from error

    def identity(self):
        user = self.get('user')
        repo = self.get('repos/' + REPOSITORY)
        if (repo.get('full_name') != REPOSITORY or not repo.get('permissions', {}).get('push')
                or not isinstance(user.get('login'), str) or not user['login']):
            raise ToolError(4, 'Existing upstream push access is required')
        return {'login': user['login'], 'repository': REPOSITORY}

    def base(self, checkout):
        branch = self.get('repos/' + REPOSITORY).get('default_branch')
        if not isinstance(branch, str) or branch.startswith('-'):
            raise ToolError(4, 'Upstream default branch is unavailable')
        self.check()
        git(checkout, 'check-ref-format', 'refs/heads/' + branch, guard=self.check)
        self.check()
        git(checkout, '-c', 'credential.helper=', '-c', 'credential.helper=!gh auth git-credential',
            'fetch', '--no-tags', ORIGIN, 'refs/heads/' + branch, guard=self.check)
        sha = git(checkout, 'rev-parse', 'FETCH_HEAD^{commit}', guard=self.check).decode().strip()
        return {'branch': branch, 'sha': sha}

    def pulls_for(self, branch=None):
        result = []
        page = 1
        while True:
            values = self.get(f'repos/{REPOSITORY}/pulls?state=all&per_page=100&page={page}')
            if not isinstance(values, list):
                raise ToolError(5, 'Pull request listing is unavailable')
            for value in values:
                if branch is None or value.get('head', {}).get('ref') == branch:
                    result.append(self.normalize(value))
            if len(values) < 100:
                return result
            page += 1

    @staticmethod
    def normalize(value):
        try:
            return dict(number=value['number'], url=value['html_url'], head=value['head']['ref'],
                        base=value['base']['ref'], sha=value['head']['sha'], draft=value['draft'],
                        repository=value['base']['repo']['full_name'], body=value.get('body') or '',
                        title=value['title'], state=value['state'], merged=bool(value.get('merged_at')))
        except (KeyError, TypeError) as error:
            raise ToolError(5, 'Pull request identity is unavailable') from error

    def remote_sha(self, branch):
        # Exact API ref lookup; a failed request is unavailable, never proof of absence.
        values = self.get(f'repos/{REPOSITORY}/git/matching-refs/heads/{branch}')
        if not isinstance(values, list):
            raise ToolError(5, 'Remote branch state is unavailable')
        exact = [v for v in values if v.get('ref') == 'refs/heads/' + branch]
        return exact[0]['object']['sha'] if len(exact) == 1 else None

    def pull(self, number):
        if type(number) is not int or number < 1:
            raise ToolError(3, 'Pull request number is invalid')
        return self.normalize(self.get(f'repos/{REPOSITORY}/pulls/{number}'))

    def push(self, checkout, branch, commit):
        self.check()
        git(checkout, '-c', 'credential.helper=', '-c', 'credential.helper=!gh auth git-credential',
            'push', ORIGIN, commit + ':refs/heads/' + branch, guard=self.check)

    def create(self, branch, base, title, body, observe=None):
        import tempfile
        # The body is already approved synthetic material. Never use a novel file as --body-file.
        with tempfile.TemporaryDirectory(prefix='novel-retro-public-') as folder:
            body_path = Path(folder) / 'body.md'
            body_path.write_text(body, encoding='utf-8')
            self.check()
            raw = command(['gh', 'pr', 'create', '--repo', REPOSITORY, '--base', base,
                           '--head', branch, '--draft', '--title=' + title,
                           '--body-file', str(body_path)])
        import re
        match = re.fullmatch(rb'https://github\.com/bjarkig82/novel-creator/pull/(\d+)\s*', raw)
        if not match:
            raise ToolError(5, 'Draft creation outcome is unavailable')
        number = int(match[1])
        if observe is not None:
            observe(dict(number=number, url=f'https://github.com/{REPOSITORY}/pull/{number}'))
        return self.normalize(self.get(f'repos/{REPOSITORY}/pulls/{number}'))
