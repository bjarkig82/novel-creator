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


def read_frozen_debug(capture):
    if capture.get('state') != 'frozen':
        raise ToolError(3, 'Full debug sharing requires a successfully frozen export')
    try:
        raw = guarded(capture['path']).read_bytes()
    except FileNotFoundError as error:
        raise ToolError(3, 'Frozen debug export is missing') from error
    if digest(raw) != capture['sha256']:
        raise ToolError(3, 'Frozen debug export changed')
    return raw


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


def public_listing(value):
    """Accept only the bounded public fields needed for a local comparison."""
    if not isinstance(value, dict) or value.keys() != {'issue', 'pr'}:
        raise ToolError(2, 'Expected issue and pr listing arrays')
    numbers = set()
    for kind, section in (('issue', 'issues'), ('pr', 'pull')):
        rows = value[kind]
        if not isinstance(rows, list) or len(rows) > 100:
            raise ToolError(2, 'Expected at most 100 public records per listing')
        for row in rows:
            if not isinstance(row, dict) or row.keys() != {'number', 'title', 'body', 'url'}:
                raise ToolError(2, 'Expected compact public number, title, body and url fields')
            number = row['number']
            if (type(number) is not int or number < 1 or number in numbers or
                    row['url'] != f'https://github.com/{REPOSITORY}/{section}/{number}'):
                raise ToolError(2, 'Invalid or repeated fixed-repository public record')
            require(row, ['title'])
            if not isinstance(row['body'], str) or '\x00' in row['body']:
                raise ToolError(2, 'Expected public issue or PR body text')
            try:
                row['title'].encode('utf-8')
                row['body'].encode('utf-8')
            except UnicodeEncodeError as error:
                raise ToolError(2, 'Expected UTF-8 public listing text') from error
            numbers.add(number)
    return value


def finding_marker(finding):
    marker = finding['marker']
    _, separator, trailer = finding['body'].rpartition('\n\n')
    if not separator or trailer != marker + '\n':
        raise ToolError(3, 'Finding marker differs from the issue body')
    return marker


def marker_urls(listing, marker):
    return [row['url'] for rows in listing.values() for row in rows if marker in row['body']]


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
            if type(run['capture'].get('keep_debugging', False)) is not bool:
                raise ValueError()
            if run['capture']['state'] == 'frozen':
                require(run['capture'], ['path', 'sha256'])
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

    def begin(self, data, *, keep_debugging=False):
        require(data, ['request_key', 'host_session'])
        session = data.get('debug_session')
        if session is not None:
            identifier(session)
        trigger = data.get('trigger', 'explicit')
        if trigger not in ('explicit', 'session_end'):
            raise ToolError(2, 'Unsupported begin trigger')
        if 'keep_debugging' in data:
            raise ToolError(2, 'Use --keep-debugging to request a live snapshot')
        if keep_debugging and (session is None or trigger != 'explicit'):
            raise ToolError(2, '--keep-debugging requires an explicit retrospective and a selected debug-session UUID')
        if trigger == 'session_end':
            observed(data, 'observed_session_end_authorization')
        self.path('issue.guard')
        with self.exclusion(), inspection_guard(self.base, 'issue.guard'):
            return self._begin(data, session, trigger, keep_debugging)

    def _begin(self, data, session, trigger, keep_debugging):
        for path in self.base.glob('*/state.json') if self.base.exists() else []:
            old = read(path)
            if old.get('root') == str(self.root) and old.get('request_key') == data['request_key'] and old.get('host_session') == data['host_session']:
                existing = self.load(old['run_id'])
                capture = existing['capture']
                if capture.get('debug_session') != session or capture.get('keep_debugging', False) != keep_debugging:
                    raise ToolError(3, 'This request key already selected a different capture or mode. Inspect the retained run.', data=existing)
                if capture['state'] not in ('absent', 'frozen'):
                    raise ToolError(3, 'Selected capture is failed or interrupted; inspect retained run without repeating export', data=existing)
                if capture['state'] == 'frozen':
                    read_frozen_debug(capture)
                return existing
        run_id = str(uuid.uuid4())
        if session is None:
            capture = dict(state='absent', limitations=['No debugging capture; review only visible conversation.'])
        else:
            capture = dict(state='exporting' if keep_debugging else 'stopping',
                           debug_session=session, keep_debugging=keep_debugging)
        run = dict(version=1, run_id=run_id, root=str(self.root), request_key=data['request_key'],
                   host_session=data['host_session'], trigger=trigger, findings={}, capture=capture)
        # Write the selected capture reservation before any stop or export.
        self.save(run)
        if session is not None:
            try:
                if not keep_debugging:
                    stopped = debug.stop(self.root, session)
                    if stopped.get('state') != 'stopped':
                        raise ToolError(3, 'Selected debug session was not stopped')
                    capture['state'] = 'exporting'
                    self.save(run)
                target = self.path(run_id + '/debug.zip')
                result = debug.export(self.root, session, target, require_recording=keep_debugging)
                limitations = list(result['warnings'])
                if result['partial']:
                    limitations.insert(0, 'Partial debug snapshot. The session was still recording at export. Later events are outside this snapshot.')
                capture.update(state='frozen', path=str(target), sha256=digest(target.read_bytes()),
                               partial=result['partial'], limitations=limitations)
                self.save(run)
            except Exception as error:
                capture['state'] = 'failed'
                capture['limitations'] = ['Selected capture could not be frozen. Inspect the retained run and debug status before starting a separate request.']
                self.save(run)
                if isinstance(error, ToolError) and error.data is None:
                    error.data = run
                if isinstance(error, OSError):
                    raise ToolError(5, 'Selected capture could not be frozen. Inspect the retained run and check local paths and permissions.', data=run) from error
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
            raw = read_frozen_debug(capture)
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
        marker = finding_marker(finding)
        if finding['creation']['state'] != 'draft':
            raise ToolError(3, 'Retained creation intent/receipt forbids another create; reconcile explicitly')
        stage = data.get('stage', 'create')
        if stage in ('preflight', 'connector_preflight'):
            observed(data, 'observed_duplicate_read_direction')
            if stage == 'connector_preflight':
                observed(data, 'observed_connector_listing')
                listing = public_listing(data.get('listing'))
            else:
                listing = public_listing(self.transport.listing())
            snapshot = dict(listing=listing, preview_digest=finding['approval']['preview_digest'], stage=stage)
            snapshot.update(sha256=digest(encoded(snapshot)), limits='At most 100 issues and 100 PRs; no proof of absence.')
            finding['duplicate_snapshot'] = snapshot
            matches = marker_urls(listing, marker)
            if matches:
                finding['existing_marker_urls'] = matches
            self.save(run)
            return finding
        if stage not in ('create', 'connector_create'):
            raise ToolError(2, 'Unknown publication stage')
        snapshot = finding.get('duplicate_snapshot')
        observed(data, 'observed_comparison_complete')
        if not snapshot or data.get('duplicate_snapshot_digest') != snapshot['sha256']:
            raise ToolError(3, 'Review the retained public listing before create')
        expected_stage = 'connector_preflight' if stage == 'connector_create' else 'preflight'
        if snapshot.get('stage', 'preflight') != expected_stage:
            raise ToolError(3, 'Review the public listing for the selected publication transport')
        listing = public_listing(snapshot['listing'])
        # Older gh snapshots hashed only the listing. New reviews bind that
        # listing and its transport to this finding's unique approved preview.
        reviewed = listing
        if 'stage' in snapshot:
            if snapshot.get('preview_digest') != finding['approval']['preview_digest']:
                raise ToolError(3, 'Public results were compared against a different finding preview')
            reviewed = dict(listing=listing, preview_digest=snapshot['preview_digest'], stage=snapshot['stage'])
        if digest(encoded(reviewed)) != snapshot['sha256']:
            raise ToolError(3, 'Retained public listing or compared finding changed')
        if data.get('equivalent_url'):
            equivalent = duplicate_reference_url(data['equivalent_url'])
            if stage == 'connector_create' and not any(row['url'] == equivalent for rows in listing.values() for row in rows):
                raise ToolError(3, 'Equivalent URL must appear in the reviewed connector listing')
            finding['equivalent_url'] = equivalent
            self.save(run)
            return finding
        if finding.get('equivalent_url') or finding.get('existing_marker_urls') or marker_urls(listing, marker):
            raise ToolError(3, 'Existing equivalent or publication marker in public results forbids creation')
        if stage == 'connector_create':
            self.reserve_create(run, finding)
            # This single-use handoff exists only in the successful response.
            return dict(connector_create=dict(repository_full_name=REPOSITORY, title=finding['title'], body=finding['body']))
        self.transport.preflight()
        body_file = self.path(run['run_id'] + '/approved-body-' + digest(finding['body'].encode('utf-8')) + '.md')
        if body_file.exists() and body_file.read_bytes() != finding['body'].encode('utf-8'):
            raise ToolError(3, 'Approved body file differs')
        if not body_file.exists():
            body_file.write_bytes(finding['body'].encode('utf-8'))
        self.reserve_create(run, finding)
        try:
            url = issue_url(self.transport.create(finding['title'], body_file))
        except Exception:
            self.save(run)
            raise
        finding['creation'].update(state='created', url=url)
        self.refresh_status(finding)
        self.save(run)
        return finding

    def reserve_create(self, run, finding):
        self.approved(finding)
        finding['creation'] = dict(state='unknown', preview_digest=finding['approval']['preview_digest'])
        self.save(run)

    def resume(self, run, finding, data):
        observed(data, 'observed_reconciliation_read_direction')
        intent = finding['creation']
        if intent['state'] not in ('unknown', 'created'):
            raise ToolError(3, 'No retained create intent to reconcile')
        # Verify the preview bytes reserved at publication, even after the author
        # cancels or loses a sharing file. Receipt handling never uploads files.
        marker = finding_marker(finding)
        if intent.get('preview_digest') != digest(encoded(self.preview(finding))):
            raise ToolError(3, 'Retained publication intent differs from the finding payload')
        stage = data.get('stage', 'view')
        if stage == 'connector_search':
            observed(data, 'observed_connector_listing')
            listing = public_listing(data.get('listing'))
            return dict(creation=intent, marker_urls=marker_urls(listing, marker))
        url = issue_url(data.get('issue_url'))
        if intent.get('url', url) != url:
            raise ToolError(3, 'Confirmed issue URL differs from the candidate')
        if stage == 'connector_receipt':
            observed(data, 'observed_connector_receipt')
            remote = data.get('receipt')
        elif stage == 'view':
            remote = self.transport.view(url)
        else:
            raise ToolError(2, 'Unknown reconciliation stage')
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
    if args.input and (type(data.get('version')) is not int or data['version'] != 1):
        raise ToolError(2, 'Issue input version must be the integer 1')
    action = args.issue_action
    if action == 'status':
        return service.load(args.run) if args.run else {'version': 1, 'runs': [p.parent.name for p in service.base.glob('*/state.json')]}
    if action == 'begin':
        return service.begin(data, keep_debugging=bool(args.keep_debugging))
    service.path('issue.guard')
    with service.exclusion(mutation=action != 'resume'), inspection_guard(service.base, 'issue.guard'):
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
