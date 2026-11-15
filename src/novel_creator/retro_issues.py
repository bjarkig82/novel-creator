"""Author-reviewed issue reports; ignored local receipts never confer host authority."""
from contextlib import nullcontext
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import uuid

from . import debug, storage
from .cli import ToolError
from .maintenance import normal_operation
from .retro import inspection_guard
from .retro_github import REPOSITORY, environment


def identifier(value):
    return debug._identifier(value)


def guarded(path):
    path = debug._guard(path)
    if path.exists() and path.is_file() and path.stat().st_nlink != 1:
        raise ToolError(2, 'Issue files cannot have hard links')
    return path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return debug._json(value)


def read(path):
    try:
        value = debug._loads(guarded(path).read_bytes())
        if not isinstance(value, dict):
            raise ValueError()
        return value
    except (ValueError, UnicodeError, RecursionError) as error:
        raise ToolError(2, 'Issue input must be strict UTF-8 JSON object') from error


def require(value, keys):
    for key in keys:
        if not isinstance(value.get(key), str) or not value[key].strip() or '\x00' in value[key]:
            raise ToolError(2, 'Required nonempty text: ' + key)


def observed(value, key):
    if value.get(key) is not True:
        raise ToolError(3, 'Current directly observed host attestation required: ' + key)


def issue_url(value):
    if not isinstance(value, str) or not re.fullmatch(r'https://github\.com/bjarkig82/novel-creator/issues/[1-9][0-9]*', value):
        raise ToolError(2, 'Expected exact designated-repository issue URL')
    return value


def duplicate_reference_url(value):
    if not isinstance(value, str) or not re.fullmatch(r'https://github\.com/bjarkig82/novel-creator/(?:issues|pull)/[1-9][0-9]*', value):
        raise ToolError(2, 'Expected exact designated-repository issue or PR URL')
    return value


class Github:
    """Fixed public listings and exact-file create only. Existing gh credentials."""
    def call(self, args):
        try:
            result = subprocess.run(['gh', *args], capture_output=True, timeout=60, env=environment())
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ToolError(5, 'GitHub transport unavailable or outcome uncertain') from error
        if result.returncode:
            raise ToolError(5, 'GitHub command failed; retained local receipt requires inspection')
        return result.stdout.decode('utf-8', 'strict').strip()

    def preflight(self):
        self.call(['auth', 'status', '--hostname', 'github.com'])

    def listing(self):
        return {kind: json.loads(self.call([kind, 'list', '--repo', REPOSITORY, '--state', 'all',
                    '--limit', '100', '--json', 'number,title,body,url'])) for kind in ('issue', 'pr')}

    def create(self, title, body_file):
        return self.call(['issue', 'create', '--repo', REPOSITORY, '--title', title, '--body-file', str(body_file)])

    def view(self, url):
        return json.loads(self.call(['issue', 'view', issue_url(url), '--repo', REPOSITORY,
                                    '--json', 'title,body,url']))


class Issues:
    def __init__(self, novel, transport=None):
        self.root, self.debug_kind, _ = debug._project(novel)
        # Notebook authority wins for mixed-marker projects; debugging deliberately
        # continues to use debug._project's legacy store for the selected session.
        self.notebook = guarded(self.root / 'notebook/project.md').is_file() and guarded(self.root / '.novel-notebook/workflows').is_dir()
        self.base = guarded(self.root / ('.novel-notebook' if self.notebook else '.novel-creator') / 'local/retro-issues')
        if debug._git(self.root, 'check-ignore', '--no-index', '--', self.base.as_posix() + '/') is None:
            raise ToolError(3, 'Issue storage must already be ignored by project Git rules; run issue setup')
        self.transport = transport or Github()

    def path(self, name):
        return guarded(self.base / name)

    def save(self, run):
        path = self.path(run['run_id'] + '/state.json')
        path.parent.mkdir(parents=True, exist_ok=True)
        storage.atomic_json(path, run)

    def load(self, run_id):
        run = read(self.path(identifier(run_id) + '/state.json'))
        if run.get('version') != 1 or run.get('root') != str(self.root) or run.get('run_id') != run_id:
            raise ToolError(3, 'Issue run identity or project differs')
        try:
            require(run, ['request_key', 'host_session'])
            if not isinstance(run['capture'], dict) or run['capture'].get('state') not in ('absent', 'stopping', 'exporting', 'frozen', 'failed') or not isinstance(run['findings'], dict):
                raise ValueError()
            for key, finding in run['findings'].items():
                identifier(key)
                if not isinstance(finding, dict) or finding.get('outcome') not in ('no_action', 'issue'):
                    raise ValueError()
                if finding['outcome'] == 'no_action':
                    continue
                require(finding, ['repository', 'title', 'body', 'marker', 'sharing', 'preview_digest'])
                if finding['repository'] != REPOSITORY or not isinstance(finding['attachments'], list) or not isinstance(finding['limitations'], list):
                    raise ValueError()
                for attachment in finding['attachments']:
                    require(attachment, ['name', 'path', 'sha256'])
                    if type(attachment['size']) is not int or attachment['size'] < 0:
                        raise ValueError()
                if finding['creation']['state'] not in ('draft', 'unknown', 'created') or finding['upload']['state'] not in ('none', 'pending', 'unknown', 'reported'):
                    raise ValueError()
                approval = finding['approval']
                if approval is not None and (not isinstance(approval, dict) or approval.get('decision') not in ('approve', 'decline') or not isinstance(approval.get('preview_digest'), str)):
                    raise ValueError()
        except (KeyError, TypeError, ValueError, AttributeError, ToolError) as error:
            raise ToolError(3, 'Issue run state is malformed; preserve it for inspection') from error
        return run

    def exclusion(self, mutation=True):
        # Status is entirely local and does not create operational storage.
        return normal_operation(self.root) if mutation and self.debug_kind == 'legacy' else nullcontext()

    def begin(self, data):
        require(data, ['request_key', 'host_session'])
        session = data.get('debug_session')
        if session is not None:
            identifier(session)
        if data.get('trigger', 'explicit') not in ('explicit', 'session_end'):
            raise ToolError(2, 'Unsupported begin trigger')
        if data.get('trigger') == 'session_end':
            observed(data, 'observed_session_end_authorization')
        for path in self.base.glob('*/state.json') if self.base.exists() else []:
            old = read(path)
            if old.get('root') == str(self.root) and old.get('request_key') == data['request_key'] and old.get('host_session') == data['host_session']:
                existing = self.load(old['run_id'])
                if existing['capture'].get('debug_session') != session:
                    raise ToolError(3, 'Request key already selected a different capture; inspect retained run', data=existing)
                if existing['capture']['state'] not in ('absent', 'frozen'):
                    raise ToolError(3, 'Selected capture is failed or interrupted; inspect retained run without repeating export', data=existing)
                return existing
        run_id = str(uuid.uuid4())
        run = dict(version=1, run_id=run_id, root=str(self.root), request_key=data['request_key'],
                   host_session=data['host_session'], trigger=data.get('trigger', 'explicit'), findings={},
                   capture={'state': 'absent', 'limitations': ['No debugging capture; review only visible conversation.']})
        # Persist reservation before stop/export; repeated begin cannot repeat export.
        self.save(run)
        if session is not None:
            run['capture'] = dict(state='stopping', debug_session=session)
            self.save(run)
            try:
                stopped = debug.stop(self.root, session)
                if stopped.get('state') != 'stopped':
                    raise ToolError(3, 'Selected debug session was not stopped')
                run['capture']['state'] = 'exporting'
                self.save(run)
                target = self.path(run_id + '/debug.zip')
                result = debug.export(self.root, session, target)
                run['capture'].update(state='frozen', path=str(target), sha256=digest(target.read_bytes()),
                                      limitations=result.get('warnings', []))
                self.save(run)
            except Exception:
                run['capture']['state'] = 'failed'
                run['capture']['limitations'] = ['Selected capture could not be stopped/exported successfully; recording log was not reviewed.']
                self.save(run)
                raise
        return run

    def finding(self, run, finding_id):
        identifier(finding_id)
        if finding_id not in run['findings']:
            raise ToolError(2, 'Finding not found in selected run')
        return run['findings'][finding_id]

    def preview(self, finding):
        return {key: finding[key] for key in ('repository', 'title', 'body', 'sharing', 'attachments', 'limitations')}

    def preview_digest(self, finding):
        for attachment in finding['attachments']:
            path = guarded(attachment['path'])
            if not path.is_relative_to(self.base) or digest(path.read_bytes()) != attachment['sha256']:
                raise ToolError(3, 'Sharing attachment changed; draft and approval must be renewed')
        return digest(encoded(self.preview(finding)))

    def draft(self, run, finding_id, data):
        identifier(finding_id)
        previous = run['findings'].get(finding_id)
        if previous and previous.get('creation', {}).get('state', 'draft') != 'draft':
            raise ToolError(3, 'Cannot replace a finding with retained publication intent or receipt')
        if data.get('outcome') == 'no_action':
            run['findings'][finding_id] = {'outcome': 'no_action', 'reason': data.get('reason', '')}
            self.save(run)
            return run['findings'][finding_id]
        fields = ['title', 'problem', 'environment', 'reproduction', 'expected', 'actual', 'evidence', 'uncertainties', 'acceptance_criteria']
        require(data, fields)
        sharing = data.get('sharing', 'generalized')
        if sharing not in ('generalized', 'excerpts', 'full_debug'):
            raise ToolError(2, 'Unsupported sharing tier')
        attachments = []
        directory = self.path(run['run_id'] + '/' + finding_id + '/' + str(uuid.uuid4()))
        directory.mkdir(parents=True)
        if sharing == 'full_debug':
            capture = run['capture']
            if capture.get('state') != 'frozen':
                raise ToolError(3, 'No successfully stopped frozen debug export')
            raw = guarded(capture['path']).read_bytes()
            if digest(raw) != capture['sha256']:
                raise ToolError(3, 'Frozen debug export changed')
            contents = [('debug.zip', raw)]
        elif sharing == 'excerpts':
            require(data, ['excerpt_text'])
            contents = [('excerpts.txt', data['excerpt_text'].encode('utf-8'))]
        else:
            contents = []
        for name, raw in contents:
            target = guarded(directory / name)
            target.write_bytes(raw)
            attachments.append(dict(name=name, path=str(target), sha256=digest(raw), size=len(raw)))
        marker = '<!-- novel-creator-issue:' + str(uuid.uuid4()) + ' -->'
        body = '\n\n'.join('## ' + field.replace('_', ' ').title() + '\n\n' + data[field] for field in fields[1:])
        if data.get('suggestions'):
            require(data, ['suggestions'])
            body += '\n\n## Supported suggestions\n\n' + data['suggestions']
        body += '\n\n' + marker + '\n'
        finding = dict(outcome='issue', repository=REPOSITORY, title=data['title'], body=body, marker=marker,
                       sharing=sharing, attachments=attachments, limitations=run['capture'].get('limitations', []),
                       approval=None, creation={'state': 'draft'}, upload={'state': 'pending' if attachments else 'none'})
        finding['preview_digest'] = self.preview_digest(finding)
        run['findings'][finding_id] = finding
        self.save(run)
        return finding

    def approve(self, run, finding, data):
        observed(data, 'observed_author_decision')
        current = self.preview_digest(finding)
        if data.get('preview_digest') != current or data.get('decision') not in ('approve', 'decline'):
            raise ToolError(3, 'Exact current preview digest and approve/decline decision required')
        finding['approval'] = dict(decision=data['decision'], preview_digest=current)
        self.save(run)
        return finding

    def approved(self, finding):
        if finding.get('approval') != dict(decision='approve', preview_digest=self.preview_digest(finding)):
            raise ToolError(3, 'Exact outgoing preview requires observed author approval')

    def publish(self, run, finding, data):
        if finding.get('cancelled'):
            raise ToolError(3, 'Cancelled finding cannot create again')
        observed(data, 'observed_publication_direction')
        self.approved(finding)
        if finding['creation']['state'] != 'draft':
            raise ToolError(3, 'Retained creation intent/receipt forbids another create; reconcile explicitly')
        if data.get('stage') == 'preflight':
            observed(data, 'observed_duplicate_read_direction')
            listing = self.transport.listing()
            finding['duplicate_snapshot'] = dict(listing=listing, sha256=digest(encoded(listing)), limits='At most 100 issues and 100 PRs; no proof of absence.')
            self.save(run)
            return finding
        snapshot = finding.get('duplicate_snapshot')
        observed(data, 'observed_comparison_complete')
        if not snapshot or data.get('duplicate_snapshot_digest') != snapshot['sha256']:
            raise ToolError(3, 'Review the retained public listing before create')
        if data.get('equivalent_url'):
            finding['equivalent_url'] = duplicate_reference_url(data['equivalent_url'])
            self.save(run)
            return finding
        self.transport.preflight()
        body_file = self.path(run['run_id'] + '/approved-body-' + digest(finding['body'].encode('utf-8')) + '.md')
        if body_file.exists() and body_file.read_bytes() != finding['body'].encode('utf-8'):
            raise ToolError(3, 'Approved body file differs')
        if not body_file.exists():
            body_file.write_bytes(finding['body'].encode('utf-8'))
        self.approved(finding)
        finding['creation'] = {'state': 'unknown', 'preview_digest': self.preview_digest(finding)}
        self.save(run)  # durable create intent BEFORE potentially ambiguous network write
        try:
            url = issue_url(self.transport.create(finding['title'], body_file))
        except Exception:
            self.save(run)
            raise
        finding['creation'].update(state='created', url=url)
        self.refresh_status(finding)
        self.save(run)
        return finding

    def resume(self, run, finding, data):
        # Default performs no writes to GitHub. Supplied URL must match exact payload.
        observed(data, 'observed_reconciliation_read_direction')
        url = issue_url(data.get('issue_url'))
        if finding['creation']['state'] not in ('unknown', 'created'):
            raise ToolError(3, 'No retained create intent to reconcile')
        remote = self.transport.view(url)
        if remote != {'url': url, 'title': finding['title'], 'body': finding['body']}:
            raise ToolError(3, 'Issue repository, URL or exact payload differs')
        finding['creation'].update(state='created', url=url)
        self.refresh_status(finding)
        self.save(run)
        return finding

    def refresh_status(self, finding):
        if finding.get('cancelled'):
            finding['status'] = 'cancelled'
        elif finding['creation']['state'] == 'created':
            state = finding['upload']['state']
            finding['status'] = 'created' if state == 'none' else 'attachments_' + state
        else:
            finding['status'] = finding['creation']['state']

    def attachment(self, run, finding, data):
        url = issue_url(data.get('issue_url'))
        if finding['creation'].get('url') != url or finding['creation']['state'] != 'created':
            raise ToolError(3, 'Attachment requires confirmed exact issue URL')
        if not finding['attachments']:
            raise ToolError(3, 'No approved attachments')
        action = data.get('action')
        if action == 'start':
            if finding.get('cancelled'):
                raise ToolError(3, 'Cancelled finding cannot upload again')
            self.approved(finding)
            observed(data, 'observed_upload_consent')
            if finding['upload']['state'] != 'pending':
                raise ToolError(3, 'Interrupted upload intent is uncertain; do not retry automatically')
            finding['upload'] = dict(state='unknown', issue_url=url)
        elif action == 'finish':
            observed(data, 'observed_upload_receipt')
            attachment_url = data.get('attachment_url', '')
            if (finding['upload']['state'] != 'unknown' or finding['upload'].get('issue_url') != url or
                    not isinstance(attachment_url, str) or not re.fullmatch(r'https://github\.com/(?:user-attachments/(?:files/[0-9]+/[^\s?#]+|assets/[a-f0-9-]+)|files/[0-9]+/[^\s?#]+)', attachment_url)):
                raise ToolError(3, 'Expected relevant GitHub attachment URL after explicit start')
            finding['upload'].update(state='reported', attachment_url=attachment_url,
                                     verification='Observed host receipt only; URL does not prove uploaded bytes or content integrity.')
        else:
            raise ToolError(2, 'Attachment action must be start or finish')
        self.refresh_status(finding)
        self.save(run)
        return finding

    def cancel(self, run, finding, data):
        observed(data, 'observed_cancel_direction')
        finding['cancelled'] = True
        finding['approval'] = None
        self.refresh_status(finding)
        self.save(run)
        return finding


def dispatch(args):
    if args.issue_action == 'setup':
        from . import retro_issue_setup
        return retro_issue_setup.setup(args)
    service = Issues(args.novel)
    data = read(args.input) if args.input else {}
    if data and data.get('version') != 1:
        raise ToolError(2, 'Issue input version must be 1')
    action = args.issue_action
    if action == 'status':
        return service.load(args.run) if args.run else {'version': 1, 'runs': [p.parent.name for p in service.base.glob('*/state.json')]}
    service.path('issue.guard')
    with service.exclusion(mutation=action != 'resume'), inspection_guard(service.base, 'issue.guard'):
        if action == 'begin':
            return service.begin(data)
        run = service.load(args.run)
        if action == 'draft':
            return service.draft(run, args.finding, data)
        finding = service.finding(run, args.finding)
        if finding.get('outcome') != 'issue':
            raise ToolError(3, 'No-action finding has no outgoing issue')
        receipt_only = action == 'attachment' and data.get('action') == 'finish'
        if finding.get('cancelled') and action != 'resume' and not receipt_only:
            raise ToolError(3, 'Finding cancelled; unknown receipts remain retained')
        return getattr(service, action)(run, finding, data)
