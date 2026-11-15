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


def historical(service, checkout, initial, stage=None, status='selected'):
    from novel_creator import retro
    grant = retro.document('authorization', enabled=True, grant_id=retro.uid(), generation=1,
        novel_id=service.novel_id, novel_root=str(service.root), checkout_root=str(checkout),
        git_common_dir=str(Path(git(checkout, 'rev-parse', '--path-format=absolute', '--git-common-dir'))),
        repository=retro.REPOSITORY, github_login='test-contributor', authorization_source='direct_cli')
    retro.write(service.path('authorization.json'), grant, 'authorization')
    retro.write(service.registry / (grant['grant_id']+'.json'), grant, 'authorization')
    part = None
    if stage:
        worktree=checkout.parent / ('retained-'+retro.uid()); worktree.mkdir()
        (worktree/'fix.txt').write_text('retained historical fix')
        part=dict(base=dict(branch='main',sha=git(checkout,'rev-parse','HEAD')),
            worktree=str(worktree),branch='novel-retro/'+retro.uid(),stage=stage,
            commit=git(checkout,'rev-parse','HEAD') if stage != 'not_started' else None,
            validation=None,pr=None,fingerprint='a'*64,public_id=retro.uid())
    item=retro.document('run',run_id=retro.uid(),task_key='b'*64,
        completion_exchange_id=initial['exchange_id'],checkpoint=git(service.root,'rev-parse','HEAD'),
        grant_id=grant['grant_id'],authorization_generation=1,
        bindings={k:grant[k] for k in ('checkout_root','git_common_dir','github_login')},
        status=status,reason_code='',evidence_refs=[initial['exchange_id']],
        finding=dict(category='runtime',problem='Synthetic parser issue',reproduction='Empty fixture'),
        contribution=part,notice=None)
    service.save_run(item)
    base=Path(grant['git_common_dir'])/'novel-creator-retro'
    retro.write(base/'owner.json',retro.document('owner',run_id=item['run_id'],
        grant_id=grant['grant_id'],novel_root=str(service.root)),'owner')
    return item,grant,base


def historical_notice(service, checkout, initial):
    """Seed an already-recorded old insufficient-evidence notice."""
    from novel_creator import retro
    item,grant,base=historical(service,checkout,initial,status='insufficient_evidence')
    # This is an authentic historical local result, not new review work.
    service.notice(item, 'Retrospective needs more evidence.')
    service.save_run(item)
    service.release_owner(item,base)
    return item['run_id']
