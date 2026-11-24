"""Focused real-local issue state tests with no network transport."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

from novel_creator import debug, retro_issues as issues
from novel_creator.cli import ToolError, parser

class Fake:
    def __init__(self):
        self.creates = 0
        self.fail = False
        self.remote = None
    def listing(self): return {'issue': [], 'pr': []}
    def preflight(self): pass
    def create(self, title, body_file):
        self.creates += 1
        self.remote = dict(title=title, body=body_file.read_text(encoding='utf-8'), url='https://github.com/bjarkig82/novel-creator/issues/1')
        if self.fail: raise ToolError(5, 'timeout')
        return self.remote['url']
    def view(self, url): return self.remote

class HostConnector:
    def __init__(self):
        self.issues = []

    def create_issue(self, repository_full_name, title, body, *, lose_response=False):
        if repository_full_name != issues.REPOSITORY:
            raise AssertionError('Unexpected repository')
        number = len(self.issues) + 1
        remote = dict(title=title, body=body, url=f'https://github.com/{repository_full_name}/issues/{number}')
        self.issues.append(remote)
        if lose_response:
            raise TimeoutError('Synthetic lost response after creation')
        return remote

    def listing(self):
        return dict(issue=[dict(number=i, **remote) for i, remote in enumerate(self.issues, 1)], pr=[])

    def fetch_issue(self, url):
        return next(remote for remote in self.issues if remote['url'] == url)


class IssueTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        (self.root/'notebook').mkdir(); (self.root/'notebook/project.md').write_text('Notebook')
        (self.root/'.novel-notebook/workflows').mkdir(parents=True)
        (self.root/'.gitignore').write_text('.novel-notebook/local/\n.novel-creator/local/\n')
        self.fake = Fake(); self.service = issues.Issues(self.root,self.fake)
        self.run = self.service.begin(dict(request_key='request',host_session='current'))
        self.fid = str(uuid.uuid4())
    def draft(self, **extra):
        data = {key:'Synthetic '+key for key in ('title','problem','environment','reproduction','expected','actual','evidence','uncertainties','acceptance_criteria')}
        data.update(extra)
        return self.service.draft(self.run,self.fid,data)
    def approve(self,f):
        return self.service.approve(self.run,f,dict(observed_author_decision=True,decision='approve',preview_digest=f['preview_digest']))
    def preflight(self,f):
        return self.service.publish(self.run,f,dict(observed_publication_direction=True,stage='preflight',observed_duplicate_read_direction=True))
    def publish(self,f):
        return self.service.publish(self.run,f,dict(observed_publication_direction=True,observed_comparison_complete=True,duplicate_snapshot_digest=f.get('duplicate_snapshot',{}).get('sha256')))
    def test_no_debug_multiple_and_no_action(self):
        self.assertEqual(self.run['capture']['state'],'absent')
        self.assertEqual(self.service.begin(dict(request_key='request',host_session='current'))['run_id'],self.run['run_id'])
        first=self.draft(); self.assertIn(first['marker'],first['body'])
        self.service.draft(self.run,str(uuid.uuid4()),dict(outcome='no_action'))
        self.assertEqual(len(self.run['findings']),2)
        self.assertEqual(self.fake.creates,0)
    def test_decline_changed_and_cross_finding(self):
        f=self.draft(); self.approve(f)
        f['title']='changed'
        with self.assertRaises(ToolError):self.preflight(f)
        f=self.draft(); self.service.approve(self.run,f,dict(observed_author_decision=True,decision='decline',preview_digest=f['preview_digest']))
        with self.assertRaises(ToolError):self.preflight(f)
        self.fid=str(uuid.uuid4()); other=self.draft()
        with self.assertRaises(ToolError):self.preflight(other)
    def test_timeout_reconcile_never_second_create(self):
        f=self.draft(); self.approve(f); self.preflight(f); self.fake.fail=True
        with self.assertRaises(ToolError):self.publish(f)
        self.assertEqual(f['creation']['state'],'unknown')
        with self.assertRaises(ToolError):self.publish(f)
        self.service.resume(self.run,f,dict(observed_reconciliation_read_direction=True,issue_url=self.fake.remote['url']))
        self.assertEqual(self.fake.creates,1)
        self.assertEqual(f['creation']['state'],'created')
    def test_listing_auth_and_no_approval(self):
        f=self.draft()
        with self.assertRaises(ToolError):self.preflight(f)
        self.approve(f)
        with self.assertRaises(ToolError):self.publish(f)
        self.preflight(f)
        with patch.object(self.fake,'preflight',side_effect=ToolError(4,'absent')):
            with self.assertRaises(ToolError):self.publish(f)
        self.assertEqual(f['creation']['state'],'draft')
    def connector_publish(self, stage, **data):
        return self.issue_command('publish', dict(stage=stage, observed_publication_direction=True, **data))

    def issue_command(self, action, data):
        src = self.root / 'host-input.json'
        src.write_text(json.dumps(dict(version=1, **data)), encoding='utf-8')
        args = parser().parse_args(['retro', 'issue', action, '--novel', str(self.root), '--run',
                                    self.run['run_id'], '--finding', self.fid, '--input', str(src), '--json'])
        return issues.dispatch(args)

    def connector_snapshot(self, listing=None):
        return self.connector_publish('connector_preflight', observed_duplicate_read_direction=True,
                                      observed_connector_listing=True,
                                      listing={'issue': [], 'pr': []} if listing is None else listing)

    def connector_intent(self, snapshot):
        return self.connector_publish('connector_create', observed_comparison_complete=True,
                                      duplicate_snapshot_digest=snapshot['duplicate_snapshot']['sha256'])

    def connector_resume(self, remote):
        return self.issue_command('resume', dict(stage='connector_receipt', observed_connector_receipt=True,
                                  observed_reconciliation_read_direction=True, issue_url=remote['url'], receipt=remote))

    def test_connector_receipt_cli_is_compact_and_keeps_full_audit_in_status(self):
        finding = self.draft()
        self.approve(finding)
        listing = {
            'issue': [dict(number=42, title='Existing issue', body='Complete issue body\n' * 1000,
                           url=f'https://github.com/{issues.REPOSITORY}/issues/42')],
            'pr': [dict(number=43, title='Existing PR', body='Complete PR body\n' * 1000,
                        url=f'https://github.com/{issues.REPOSITORY}/pull/43')],
        }
        reviewed = self.connector_snapshot(listing)
        connector = HostConnector()
        receipt = connector.create_issue(**self.connector_intent(reviewed)['connector_create'])
        src = self.root / 'connector-receipt.json'
        src.write_text(json.dumps(dict(version=1, stage='connector_receipt', observed_connector_receipt=True,
                                       observed_reconciliation_read_direction=True, issue_url=receipt['url'],
                                       receipt=receipt)), encoding='utf-8')
        cli = [sys.executable, '-m', 'novel_creator', 'retro', 'issue']
        scope = ['--novel', str(self.root), '--run', self.run['run_id'], '--json']
        args = [*cli, 'resume', *scope, '--finding', self.fid, '--input', str(src)]
        expected = {'ok': True, 'data': {'status': 'created', 'upload': {'state': 'none'}, 'creation': {
            'state': 'created', 'url': receipt['url'], 'preview_digest': finding['preview_digest'],
        }}}
        for attempt in ('first receipt', 'exact replay'):
            with self.subTest(attempt=attempt):
                response = subprocess.run(args, capture_output=True, check=True)
                self.assertEqual(expected, json.loads(response.stdout))
        response = subprocess.run([*cli, 'status', *scope], capture_output=True, check=True)
        audit = json.loads(response.stdout)['data']['findings'][self.fid]
        self.assertEqual(audit['duplicate_snapshot'], reviewed['duplicate_snapshot'])
        self.assertEqual(audit['duplicate_snapshot']['listing'], listing)
        self.assertEqual(audit['creation'], expected['data']['creation'])

    def test_connector_create_after_gh_401_and_exact_receipt(self):
        f = self.draft(sharing='excerpts', excerpt_text='private fixture')
        self.approve(f)
        self.preflight(f)
        gh = issues.Github()
        failure = subprocess.CompletedProcess([], 1, b'', b'HTTP 401: Bad credentials')
        self.service.transport = gh
        with patch.object(subprocess, 'run', return_value=failure) as auth:
            with self.assertRaises(ToolError):
                self.publish(f)
        self.assertEqual(auth.call_args.args[0], ['gh', 'auth', 'status', '--hostname', 'github.com'])
        self.assertEqual(self.service.load(self.run['run_id'])['findings'][self.fid]['creation']['state'], 'draft')
        compared = self.connector_snapshot()
        with patch.object(issues.storage, 'atomic_json', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                self.connector_intent(compared)
        response = self.connector_intent(compared)
        stored = self.service.load(self.run['run_id'])['findings'][self.fid]
        self.assertEqual(stored['creation']['state'], 'unknown')
        self.assertNotIn('connector_create', stored)
        self.assertEqual(response['connector_create'], dict(repository_full_name=issues.REPOSITORY,
                                                           title=f['title'], body=f['body']))
        connector = HostConnector()
        receipt = connector.create_issue(**response['connector_create'])
        self.assertIn(f['marker'], receipt['body'])
        with self.assertRaises(ToolError):
            self.connector_intent(compared)
        self.issue_command('cancel', dict(observed_cancel_direction=True))
        Path(f['attachments'][0]['path']).unlink()
        for bad in (dict(receipt, title='changed'), dict(receipt, body=f['body'].replace(f['marker'], '')),
                    dict(receipt, url='https://github.com/other/repo/issues/12'),
                    dict(receipt, url=receipt['url'].replace('/issues/', '/pull/'))):
            with self.subTest(receipt=bad), self.assertRaises(ToolError):
                self.connector_resume(bad)
        with self.assertRaises(ToolError):
            self.issue_command('resume', dict(stage='connector_receipt', issue_url=receipt['url'],
                               observed_reconciliation_read_direction=True, receipt=receipt))
        verified = self.connector_resume(receipt)
        self.assertEqual(verified['status'], 'cancelled')
        self.assertEqual(verified['upload']['state'], 'pending')
        self.assertEqual(verified['creation']['url'], receipt['url'])
        with self.assertRaises(ToolError):
            self.connector_resume(dict(receipt, url=receipt['url'] + '3'))
        self.assertEqual(len(connector.issues), 1)

    def test_connector_uncertain_write_reconciles_marker_then_exact_read(self):
        f = self.draft()
        self.approve(f)
        compared = self.connector_snapshot()
        payload = self.connector_intent(compared)['connector_create']
        connector = HostConnector()
        with self.assertRaises(TimeoutError):
            connector.create_issue(**payload, lose_response=True)
        search = dict(stage='connector_search', observed_connector_listing=True,
                      observed_reconciliation_read_direction=True, listing=dict(issue=[], pr=[]))
        self.assertEqual(self.issue_command('resume', search)['marker_urls'], [])
        with self.assertRaises(ToolError):
            self.connector_intent(compared)
        search['listing'] = connector.listing()
        matches = self.issue_command('resume', search)
        self.assertEqual(matches['marker_urls'], [connector.issues[0]['url']])
        remote = connector.fetch_issue(matches['marker_urls'][0])
        self.assertEqual(self.service.load(self.run['run_id'])['findings'][self.fid]['creation']['state'], 'unknown')
        self.assertEqual(self.connector_resume(remote)['creation']['url'], remote['url'])
        self.assertEqual(len(connector.issues), 1)
        with self.assertRaises(ToolError):
            self.connector_intent(compared)

    def test_connector_preflight_validates_scope_binding_and_marker(self):
        f = self.draft()
        self.approve(f)
        row = dict(number=2, url='https://github.com/bjarkig82/novel-creator/issues/2', title='issue', body='')
        for listing in (None, dict(issue=[]), dict(issue=[], pr=[], private=[]), dict(issue={}, pr=[]),
                        dict(issue=[dict(row, number=n,
                             url=f'https://github.com/{issues.REPOSITORY}/issues/{n}') for n in range(1, 102)], pr=[]), dict(issue=[row, row], pr=[]),
                        dict(issue=[dict(row, number=True)], pr=[]), dict(issue=[dict(row, body=None)], pr=[]),
                        dict(issue=[dict(row, url=row['url'] + '0')], pr=[]), dict(issue=[], pr=[row]),
                        dict(issue=[dict(row, body_text='extra')], pr=[])):
            with self.subTest(listing=listing), self.assertRaises(ToolError):
                self.connector_publish('connector_preflight', observed_duplicate_read_direction=True,
                                       observed_connector_listing=True, listing=listing)
        with self.assertRaises(ToolError):
            self.connector_publish('connector_preflight', observed_duplicate_read_direction=True, listing=dict(issue=[], pr=[]))
        first = self.connector_snapshot()
        self.fid = str(uuid.uuid4())
        other = self.draft()
        self.approve(other)
        self.connector_snapshot()
        with self.assertRaises(ToolError):
            self.connector_intent(first)
        listed = self.connector_snapshot(dict(issue=[dict(row, body=other['marker'])], pr=[]))
        with self.assertRaises(ToolError):
            self.connector_intent(listed)
        with self.assertRaises(ToolError):
            self.connector_intent(self.connector_snapshot())
        self.assertEqual(self.service.load(self.run['run_id'])['findings'][self.fid]['creation']['state'], 'draft')

    def test_connector_rejects_changed_snapshot_or_intent(self):
        f = self.draft()
        self.approve(f)
        url = f'https://github.com/{issues.REPOSITORY}/issues/1'
        remote = dict(url=url, title=f['title'], body=f['body'])
        with self.assertRaises(ToolError):
            self.connector_resume(remote)
        snapshot = self.connector_snapshot()
        run = self.service.load(self.run['run_id'])
        stored = run['findings'][self.fid]['duplicate_snapshot']
        stored['listing']['issue'].append(dict(number=1, **remote))
        self.service.save(run)
        with self.assertRaises(ToolError):
            self.connector_intent(snapshot)
        self.connector_intent(self.connector_snapshot())
        run = self.service.load(self.run['run_id'])
        finding = run['findings'][self.fid]
        finding['title'] = 'Unapproved local edit'
        self.service.save(run)
        with self.assertRaisesRegex(ToolError, 'intent differs'):
            self.connector_resume(dict(remote, title=finding['title']))

    def test_publish_cannot_switch_transports_after_comparison(self):
        f = self.draft()
        self.approve(f)
        gh_review = self.preflight(f)
        with self.assertRaises(ToolError):
            self.connector_intent(gh_review)
        connector_review = self.connector_snapshot()
        digest = connector_review['duplicate_snapshot']['sha256']
        for stage in ({}, {'stage': 'create'}):
            with self.subTest(stage=stage), patch.object(issues.Github, 'preflight') as auth, \
                    patch.object(issues.Github, 'create') as create:
                with self.assertRaises(ToolError):
                    self.issue_command('publish', dict(observed_publication_direction=True,
                                       observed_comparison_complete=True, duplicate_snapshot_digest=digest, **stage))
                auth.assert_not_called()
                create.assert_not_called()
                self.assertEqual(self.service.load(self.run['run_id'])['findings'][self.fid]['creation']['state'], 'draft')

    def test_marker_field_must_match_approved_body_before_listing_or_creation(self):
        f = self.draft()
        self.approve(f)
        reviewed = self.connector_snapshot()
        run = self.service.load(self.run['run_id'])
        finding = run['findings'][self.fid]
        original = finding['marker']
        row = dict(number=1, title='Existing issue', body=original,
                   url=f'https://github.com/{issues.REPOSITORY}/issues/1')
        finding['marker'] = '<!-- novel-creator-issue:' + str(uuid.uuid4()) + ' -->'
        self.service.save(run)
        with self.assertRaisesRegex(ToolError, 'marker'):
            self.connector_snapshot(dict(issue=[row], pr=[]))
        with self.assertRaisesRegex(ToolError, 'marker'):
            self.connector_intent(reviewed)
        self.assertEqual(self.service.load(self.run['run_id'])['findings'][self.fid]['creation']['state'], 'draft')
        # The same invariant applies to late receipts even after a valid reservation.
        finding['marker'] = original
        self.service.save(run)
        self.connector_intent(reviewed)
        run = self.service.load(self.run['run_id'])
        run['findings'][self.fid]['marker'] = 'changed'
        self.service.save(run)
        remote = dict(title=f['title'], body=f['body'], url=row['url'])
        with self.assertRaisesRegex(ToolError, 'marker'):
            self.connector_resume(remote)

    def test_older_gh_listing_still_supports_approved_create_and_resume(self):
        f = self.draft()
        self.approve(f)
        listing = self.fake.listing()
        f['duplicate_snapshot'] = dict(listing=listing, sha256=issues.digest(issues.encoded(listing)))
        self.service.save(self.run)
        self.publish(f)
        receipt = self.connector_resume(self.fake.remote)
        self.assertEqual(receipt['creation']['url'], self.fake.remote['url'])

    def test_equivalent_issue_and_pr_are_retained_without_creation(self):
        for kind, path in (('issue', 'issues'), ('pr', 'pull')):
            with self.subTest(kind=kind):
                self.fid = str(uuid.uuid4())
                f = self.draft()
                url = f'https://github.com/bjarkig82/novel-creator/{path}/123'
                listing = {'issue': [], 'pr': []}
                listing[kind] = [dict(number=123, title=f['title'], body=f['body'], url=url)]
                self.approve(f)
                with patch.object(self.fake, 'listing', return_value=listing):
                    self.preflight(f)
                data = dict(observed_publication_direction=True, observed_comparison_complete=True,
                            duplicate_snapshot_digest=f['duplicate_snapshot']['sha256'], equivalent_url=url)
                with patch.object(self.fake, 'preflight') as preflight:
                    self.service.publish(self.run, f, data)
                preflight.assert_not_called()
                stored = self.service.load(self.run['run_id'])['findings'][self.fid]
                self.assertEqual(stored['equivalent_url'], url)
                self.assertEqual(stored['creation']['state'], 'draft')
                self.assertEqual(self.fake.creates, 0)

    def test_equivalent_reference_keeps_exact_repository_url_boundary(self):
        f = self.draft(); self.approve(f); self.preflight(f)
        urls = (
            'http://github.com/bjarkig82/novel-creator/pull/123',
            'https://github.com.evil.invalid/bjarkig82/novel-creator/pull/123',
            'https://user@github.com/bjarkig82/novel-creator/pull/123',
            'https://github.com:443/bjarkig82/novel-creator/pull/123',
            'https://github.com/other/novel-creator/pull/123',
            'https://github.com/bjarkig82/other/pull/123',
            'https://github.com/bjarkig82/novel-creator/pulls/123',
            'https://github.com/bjarkig82/novel-creator/pull/0',
            'https://github.com/bjarkig82/novel-creator/pull/0123',
            'https://github.com/bjarkig82/novel-creator/pull/123/',
            'https://github.com/bjarkig82/novel-creator/pull/123?query=1',
            'https://github.com/bjarkig82/novel-creator/issues/123#fragment',
            123,
        )
        for url in urls:
            with self.subTest(url=url):
                with self.assertRaises(ToolError):
                    self.service.publish(self.run, f, dict(
                        observed_publication_direction=True, observed_comparison_complete=True,
                        duplicate_snapshot_digest=f['duplicate_snapshot']['sha256'], equivalent_url=url))
                self.assertNotIn('equivalent_url', f)
                self.assertEqual(f['creation']['state'], 'draft')
        self.assertEqual(self.fake.creates, 0)

    def test_creation_and_reconciliation_still_refuse_pr_urls(self):
        f = self.draft(); self.approve(f); self.preflight(f)
        url = 'https://github.com/bjarkig82/novel-creator/pull/123'
        with patch.object(self.fake, 'create', return_value=url) as create:
            with self.assertRaisesRegex(ToolError, 'issue URL'):
                self.publish(f)
        create.assert_called_once()
        self.assertEqual(f['creation']['state'], 'unknown')
        with patch.object(self.fake, 'view') as view:
            with self.assertRaisesRegex(ToolError, 'issue URL'):
                self.service.resume(self.run, f, dict(observed_reconciliation_read_direction=True, issue_url=url))
        view.assert_not_called()

    def test_upload_still_refuses_pr_urls(self):
        f = self.draft(sharing='excerpts', excerpt_text='Synthetic'); self.approve(f)
        url = 'https://github.com/bjarkig82/novel-creator/pull/123'
        f['creation'] = dict(state='created', url=url)
        with self.assertRaisesRegex(ToolError, 'issue URL'):
            self.service.attachment(self.run, f, dict(action='start', observed_upload_consent=True, issue_url=url))
        self.assertEqual(f['upload']['state'], 'pending')
    def test_debug_stop_export_frozen_and_mixed_markers(self):
        (self.root/'.novel-creator').mkdir(); (self.root/'.novel-creator/manifest.json').write_text('{}')
        service=issues.Issues(self.root,self.fake)
        session=debug.start(self.root)['debug_session']
        original_stop=debug.stop; original_export=debug.export; calls=[]
        def stop(*args):calls.append('stop');return original_stop(*args)
        def export(*args, **kwargs):calls.append('export');return original_export(*args, **kwargs)
        data=dict(request_key='debug',host_session='current',debug_session=session)
        with patch.object(debug,'stop',side_effect=stop),patch.object(debug,'export',side_effect=export):
            run=service.begin(data); again=service.begin(data)
        self.assertEqual(calls,['stop','export']);self.assertEqual(run,again)
        self.assertTrue(Path(run['capture']['path']).is_relative_to(self.root/'.novel-notebook'))
        self.assertTrue((self.root/'.novel-creator/local/debug'/session/'events.jsonl').exists())
        self.run=run;self.service=service; f=self.draft(sharing='full_debug');self.approve(f)
        self.assertEqual(f['attachments'][0]['sha256'],run['capture']['sha256'])
    def test_failed_stop_no_export(self):
        with patch.object(debug,'stop',side_effect=ToolError(3,'failed')),patch.object(debug,'export') as export:
            with self.assertRaises(ToolError):self.service.begin(dict(request_key='bad',host_session='current',debug_session=str(uuid.uuid4())))
        export.assert_not_called()
    def test_upload_unknown_cancel_and_receipt(self):
        f=self.draft(sharing='excerpts',excerpt_text='Selected synthetic text');self.approve(f);self.preflight(f);self.publish(f)
        data=dict(action='start',observed_upload_consent=True,issue_url=f['creation']['url'])
        self.service.attachment(self.run,f,data)
        with self.assertRaises(ToolError):self.service.attachment(self.run,f,data)
        self.service.attachment(self.run,f,dict(action='finish',observed_upload_receipt=True,issue_url=f['creation']['url'],attachment_url='https://github.com/user-attachments/files/123/report.zip'))
        self.assertEqual(f['upload']['state'],'reported')
        self.service.cancel(self.run,f,dict(observed_cancel_direction=True));self.assertEqual(f['creation']['state'],'created')
        with self.assertRaises(ToolError):self.publish(f)
    def test_mutated_sharing_copy(self):
        f=self.draft(sharing='excerpts',excerpt_text='Synthetic');self.approve(f)
        Path(f['attachments'][0]['path']).write_text('changed')
        with self.assertRaises(ToolError):self.preflight(f)
    def test_session_end_only_current_attestation(self):
        with self.assertRaises(ToolError):self.service.begin(dict(request_key='automatic',host_session='current',trigger='session_end'))
        result=self.service.begin(dict(request_key='automatic',host_session='current',trigger='session_end',observed_session_end_authorization=True))
        self.assertNotIn('observed_session_end_authorization',result)
        with self.assertRaises(ToolError):self.service.begin(dict(request_key='next',host_session='next',trigger='session_end'))
    def test_input_identifiers_and_ignored_storage(self):
        for value in ('../bad', 'A'*36, None):
            with self.assertRaises(ToolError):issues.identifier(value)
        path=self.root/'input.json';path.write_bytes(b'{"version":1,"version":1}')
        with self.assertRaises(ToolError):issues.read(path)
        (self.root/'.gitignore').write_text('')
        with self.assertRaises(ToolError):issues.Issues(self.root)
    def test_legacy_format_and_path_hardlink(self):
        import shutil
        shutil.rmtree(self.root / 'notebook'); shutil.rmtree(self.root / '.novel-notebook')
        (self.root/'.novel-creator').mkdir(exist_ok=True)
        (self.root/'.novel-creator/manifest.json').write_text('{}')
        service=issues.Issues(self.root,self.fake)
        run=service.begin(dict(request_key='legacy',host_session='current'))
        self.assertTrue(service.base.is_relative_to(self.root/'.novel-creator'))
        target=service.path(run['run_id']+'/state.json')
        # Windows sandbox denies creating hard links; exercise the same observed
        # filesystem metadata branch without claiming native link creation.
        original=Path.stat
        def linked(path,*args,**kwargs):
            result=original(path,*args,**kwargs)
            if path == target and kwargs.get('follow_symlinks', True):
                values=list(result);values[3]=2;return os.stat_result(values)
            return result
        with patch.object(Path,'stat',linked):
            with self.assertRaises(ToolError):service.load(run['run_id'])

    def test_malformed_capture_repeated_then_corrected(self):
        data=dict(request_key='malformed',host_session='current',debug_session='bad')
        before=list(self.service.base.glob('*/state.json'))
        for _ in range(2):
            with self.assertRaises(ToolError):self.service.begin(data)
        self.assertEqual(list(self.service.base.glob('*/state.json')),before)
        data['debug_session']=debug.start(self.root)['debug_session']
        run=self.service.begin(data)
        self.assertEqual(run['capture']['state'],'frozen')
        self.assertEqual(self.service.begin(data),run)
        data['debug_session']=None
        with self.assertRaises(ToolError):self.service.begin(data)

    def receipt_dispatch(self,f,data):
        import json
        path=self.root/'receipt-input.json';path.write_text(json.dumps(dict(version=1,**data)))
        args=parser().parse_args(['retro','issue','attachment','--novel',str(self.root),'--run',self.run['run_id'],'--finding',self.fid,'--input',str(path),'--json'])
        return issues.dispatch(args)

    def test_cancelled_receipt_dispatch_without_sharing_file(self):
        f=self.draft(sharing='excerpts',excerpt_text='Synthetic');self.approve(f);self.preflight(f);self.publish(f)
        url=f['creation']['url']
        start=dict(action='start',observed_upload_consent=True,issue_url=url)
        self.service.attachment(self.run,f,start)
        self.service.cancel(self.run,f,dict(observed_cancel_direction=True))
        Path(f['attachments'][0]['path']).unlink()
        receipt=self.receipt_dispatch(f,dict(action='finish',observed_upload_receipt=True,issue_url=url,attachment_url='https://github.com/user-attachments/files/123/report.zip'))
        self.assertTrue(receipt['cancelled']);self.assertEqual(receipt['status'],'cancelled')
        self.assertEqual(receipt['upload']['state'],'reported')
        with self.assertRaises(ToolError):self.receipt_dispatch(receipt,start)
        with self.assertRaises(ToolError):self.publish(receipt)
        self.assertEqual(self.fake.creates,1)

    def test_declined_receipt_and_resume_upload_states(self):
        f=self.draft(sharing='excerpts',excerpt_text='Synthetic');self.approve(f);self.preflight(f);self.publish(f)
        url=f['creation']['url'];reconcile=dict(observed_reconciliation_read_direction=True,issue_url=url)
        self.service.resume(self.run,f,reconcile);self.assertEqual(f['status'],'attachments_pending')
        self.service.attachment(self.run,f,dict(action='start',observed_upload_consent=True,issue_url=url))
        self.service.resume(self.run,f,reconcile);self.assertEqual(f['status'],'attachments_unknown')
        self.service.approve(self.run,f,dict(observed_author_decision=True,decision='decline',preview_digest=f['preview_digest']))
        Path(f['attachments'][0]['path']).write_text('later file changes do not erase completed receipt')
        self.service.attachment(self.run,f,dict(action='finish',observed_upload_receipt=True,issue_url=url,attachment_url='https://github.com/user-attachments/files/123/report.zip'))
        self.service.resume(self.run,f,reconcile);self.assertEqual(f['status'],'attachments_reported')
        self.service.cancel(self.run,f,dict(observed_cancel_direction=True))
        self.service.resume(self.run,f,reconcile);self.assertEqual(f['status'],'cancelled')

    def test_corrupted_nested_state_controlled_error(self):
        f=self.draft();f['upload']=None;self.service.save(self.run)
        with self.assertRaisesRegex(ToolError,'malformed'):self.service.load(self.run['run_id'])

    def test_cli_setup_and_runtime(self):
        args=parser().parse_args(['retro','issue','setup','--novel',str(self.root),'--apply','--preview','id','--expected-head','sha','--json'])
        self.assertEqual(args.issue_action,'setup');self.assertTrue(args.apply)
        with self.assertRaises(ToolError):parser().parse_args(['retro','issue','draft','--novel',str(self.root)])

if __name__=='__main__':unittest.main()


class IssuePrivacyBoundaryTests(unittest.TestCase):
    def test_actual_private_directory_must_be_ignored_before_writes(self):
        for kind in ('novel-notebook', 'novel-creator'):
            base = f'.{kind}/local/retro-issues'
            for rule, safe in ((f'.{kind}/local/', True),
                               (base + '/', True),
                               ('*.json', False),
                               (base + '/state.json', False),
                               (base + '/**/*.*', False)):
                with self.subTest(kind=kind, rule=rule), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary).resolve()
                    subprocess.run(['git', 'init', '-q', str(root)], check=True)
                    if kind == 'novel-notebook':
                        (root / 'notebook').mkdir()
                        (root / 'notebook/project.md').write_text('Synthetic', encoding='utf-8')
                        (root / '.novel-notebook/workflows').mkdir(parents=True)
                    else:
                        (root / '.novel-creator').mkdir()
                        (root / '.novel-creator/manifest.json').write_text('{}', encoding='utf-8')
                    (root / '.gitignore').write_text(rule + '\n', encoding='utf-8')
                    self.assertFalse((root / base).exists())
                    if safe:
                        service = issues.Issues(root, Fake())
                        run = service.begin(dict(request_key='synthetic', host_session='current'))
                        self.assertTrue((root / base / run['run_id'] / 'state.json').is_file())
                    else:
                        with patch.object(debug, 'stop') as stop, patch.object(debug, 'export') as export:
                            with self.assertRaisesRegex(ToolError, 'must already be ignored'):
                                service = issues.Issues(root, Fake())
                                service.begin(dict(request_key='synthetic', host_session='current', debug_session=str(uuid.uuid4())))
                        stop.assert_not_called()
                        export.assert_not_called()
                        self.assertFalse((root / base).exists(), 'No ZIP, excerpts, body or private state may be created')
