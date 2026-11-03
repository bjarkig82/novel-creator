"""Offline synthetic retrospective fixtures. Never constructs a real publisher."""
from contextlib import contextmanager
from pathlib import Path
import tempfile
from unittest.mock import patch
from tests.helpers import repository, git, envelope
from novel_creator import storage


class FakeGithub:
    def __init__(self, checkout):
        self.checkout = checkout
        self.calls = []
        self.login = 'test-contributor'
        self.allowed = True
        self.pulls = []
        self.refs = {}
        self.unknown_create = False

    def identity(self):
        self.calls.append('identity')
        if not self.allowed:
            from novel_creator.cli import ToolError
            raise ToolError(4, 'Repository access unavailable')
        return {'login': self.login, 'repository': 'bjarkig82/novel-creator'}

    def base(self, checkout):
        self.calls.append('base')
        return {'branch': 'main', 'sha': git(checkout, 'rev-parse', 'main')}

    def pulls_for(self, branch=None):
        self.calls.append('pulls')
        return [p for p in self.pulls if branch is None or p['head'] == branch]

    def remote_sha(self, branch):
        self.calls.append('remote')
        return self.refs.get(branch)

    def pull(self, number):
        self.calls.append('pull')
        return next(p for p in self.pulls if p['number']==number)

    def push(self, checkout, branch, commit):
        self.calls.append('push')
        self.refs[branch] = commit

    def create(self, branch, base, title, body, observe=None):
        self.calls.append('create')
        number = max((p['number'] for p in self.pulls), default=0) + 1
        result = {'number': number,
                  'url': f'https://github.com/bjarkig82/novel-creator/pull/{number}',
                  'head': branch, 'base': base, 'sha': self.refs[branch],
                  'draft': True, 'body': body, 'title': title,
                  'repository': 'bjarkig82/novel-creator', 'state': 'open'}
        self.pulls.append(result)
        if self.unknown_create:
            raise OSError('Synthetic ambiguous success')
        if observe is not None:
            observe({'number':result['number'],'url':result['url']})
        return result


@contextmanager
def fixtures():
    with repository() as novel, repository() as checkout, tempfile.TemporaryDirectory() as registry:
        git(checkout, 'remote', 'add', 'origin', 'https://github.com/bjarkig82/novel-creator.git')
        initial = envelope(novel)
        storage.save(novel, initial)
        fake = FakeGithub(checkout)
        yield novel, checkout, Path(registry).resolve(), fake, initial
