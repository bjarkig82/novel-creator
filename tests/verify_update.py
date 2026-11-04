"""Offline installed-controller qualification; never a production update source.

Explicit public historical source archives and a controlled target wheel only.
Every book, package environment, transport and synthetic exchange is disposable.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

from packaging.utils import parse_wheel_filename
from packaging.version import Version


def installed_matrix(sources, target):
    from novel_creator import update, storage, update_release
    from tests.update_helpers import historical_book, add_writer_work, snapshot, SOURCE_WHEELS
    from tests.update_release_helpers import release_listing
    target = Path(target).resolve(strict=True)
    _, version, _, _ = parse_wheel_filename(target.name)
    raw = target.read_bytes()
    cases = []
    for source in sources:
        source = Path(source).resolve(strict=True)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        origin = next((key for key, (_, expected) in SOURCE_WHEELS.items() if expected == digest), None)
        if origin is None or version <= Version(origin):
            raise ValueError('Each source must be an approved historical wheel older than the target')
        language = 'en' if origin == '0.1.0' else 'is'
        with historical_book(origin, wheel=source, language=language) as book, tempfile.TemporaryDirectory() as cache:
            seed = json.loads(book.run('''
import json,uuid
from novel_creator import records,storage
root=sys.argv[1]; previous=storage.read_history(root)[-1]
exchange=records.new_exchange(previous['novel_id'],previous=previous,expected_head=storage.head(root),messages=[
 {'message_id':str(uuid.uuid4()),'role':'user','text':'Synthetic session request.'},
 {'message_id':str(uuid.uuid4()),'role':'assistant','text':'Synthetic saved reply.'}])
session=records.start_session(exchange,topic='Þóra / qualification fixture')
exchange.update(session_id=session['id'],record_versions=[session]);exchange['payload_digest']=records.digest(exchange)
assert storage.save(root,exchange)['data']['saved']
print(json.dumps(session))
'''))
            add_writer_work(book.root)
            instructions = b'# Exact custom instructions\nPreserve this file.\n'
            (book.root / 'AGENTS.md').write_bytes(instructions)
            before = snapshot(book.root)
            config = (book.root / '.git/config').read_bytes()
            history = storage.read_history(book.root)
            story = {path.name: path.read_bytes() for path in (book.root / 'story/exchanges').glob('*.json')}
            staged = storage.index_entries(book.root, ['notes.txt'])
            transport = release_listing({origin: source.read_bytes(), str(version): raw})
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                preview = update.preview(book.root, transport=transport)['data']
                assert snapshot(book.root) == before
                requests = list(transport.requests)
                result = update.apply(book.root, preview_id=preview['preview_id'], version=str(version),
                    expected_head=preview['reviewed_head'], confirm_quiescent=True)
                assert result['data']['ready'] and not result['data']['cleanup_required']
                commit = storage.head(book.root)
                assert storage.git(book.root, 'rev-parse', 'HEAD^').decode().strip() == before['head']
                assert transport.requests == requests
                assert storage.read_history(book.root) == history
                assert storage.index_entries(book.root, ['notes.txt']) == staged
                repeated = update.apply(book.root, preview_id=preview['preview_id'], version=str(version),
                    expected_head=preview['reviewed_head'], confirm_quiescent=True)
                assert repeated['data']['ready'] and storage.head(book.root) == commit
                recovered = update.recover(book.root, operation_id=preview['preview_id'], retry=True, expected_head=commit)
                assert recovered['data']['ready'] and storage.head(book.root) == commit
            assert (book.root / 'AGENTS.md').read_bytes() == instructions
            assert (book.root / '.git/config').read_bytes() == config
            assert (book.root / 'notes.txt').read_bytes() == b'working\n'
            assert (book.root / 'untracked.txt').read_bytes() == b'preserve untracked\n'
            for name, content in story.items():
                assert (book.root / 'story/exchanges' / name).read_bytes() == content
            reopened = book.launch('context', '--novel', book.root, '--session', seed['id'], '--json')
            assert reopened.returncode == 0
            context = json.loads(reopened.stdout)
            assert context['data']['selected_session'] == seed
            assert context['data']['manuscript_language'] == language
            followup = json.loads(book.run('''
import json,uuid
from pathlib import Path
from novel_creator import records,storage
root=Path(sys.argv[1]); session=json.loads(sys.argv[2]); previous=storage.read_history(root)[-1]
exchange=records.new_exchange(previous['novel_id'],previous=previous,expected_head=storage.head(root),session_id=session['id'],messages=[
 {'message_id':str(uuid.uuid4()),'role':'user','text':'Höldum áfram / continue.'},
 {'message_id':str(uuid.uuid4()),'role':'assistant','text':'Synthetic saved continuation.'}])
exchange['record_versions']=[records.revise_session(session,exchange)];exchange['payload_digest']=records.digest(exchange)
result=storage.save(root,exchange)
assert all(Path(module.__file__).resolve().is_relative_to(root/'.novel-creator/src')
 for name,module in sys.modules.items() if name.startswith('novel_creator') and getattr(module,'__file__',None))
print(json.dumps(result))
''', json.dumps(seed), pinned=True))
            assert followup['data']['saved'] and not followup['data']['cleanup_required']
            assert storage.read_history(book.root)[:-1] == history
            assert storage.index_entries(book.root, ['notes.txt']) == staged
            # Completion is durable when an ordinary saved exchange advances HEAD.
            after_save = snapshot(book.root)
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                report = update.status(book.root, operation_id=preview['preview_id'])
                assert report['data']['ready'] and not report['data']['cleanup_required']
                inspection = update.recover(book.root, operation_id=preview['preview_id'])
                assert inspection['data']['state'] == 'complete' and inspection['data']['ready']
                assert not inspection['data']['cleanup_required'] and not inspection['data']['retry_eligible']
                assert update.apply(book.root, preview_id=preview['preview_id'], version=str(version),
                    expected_head=preview['reviewed_head'], confirm_quiescent=True)['data']['ready']
                from novel_creator.cli import ToolError
                try:
                    update.recover(book.root, operation_id=preview['preview_id'], retry=True,
                        expected_head=storage.head(book.root))
                except ToolError as error:
                    assert error.code == 3  # Later writer work changes original recovery evidence.
                else:
                    raise AssertionError('Recovery must refuse a changed original checkpoint')
            assert snapshot(book.root) == after_save
            cases.append({'source_version': origin, 'source_sha256': digest, 'language': language,
                'target_version': str(version), 'target_sha256': hashlib.sha256(raw).hexdigest(),
                'preview_read_only': True, 'framework_commit': commit, 'single_update_commit': True,
                'history_and_writer_work_preserved': True, 'guided_session_restored': True,
                'pinned_product_origins': True, 'subsequent_synthetic_save': True,
                'completed_status_after_subsequent_save': True,
                'completed_recovery_inspection_after_subsequent_save': True,
                'changed_recovery_checkpoint_refused': True})
    return {'ok': True, 'scope': 'offline disposable installed-controller CLI qualification; not native host or publication',
            'cases': cases}


def verify(sources, target):
    from novel_creator import update_release
    checkout = Path(__file__).resolve().parents[1]
    sys.path.append(str(checkout))
    from tests.update_release_helpers import release_listing
    target = Path(target).resolve(strict=True)
    name, version, _, _ = parse_wheel_filename(target.name)
    if str(name) != 'novel-creator':
        raise ValueError('Target must be a Novel Creator wheel')
    transport = release_listing({str(version): target.read_bytes()})
    selected = update_release.select_release(update_release.release_index(transport), version=str(version))
    with tempfile.TemporaryDirectory(prefix='verify-update-controller-') as cache:
        with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
            prepared = update_release.prepare(selected, transport=transport)
        program = '''
import sys,json
from pathlib import Path
import novel_creator
assert Path(novel_creator.__file__).parent == Path(sys.argv[1])
sys.path.append(sys.argv[2])
from tests.verify_update import installed_matrix
result=installed_matrix(json.loads(sys.argv[3]),sys.argv[4])
assert all(Path(module.__file__).resolve().is_relative_to(Path(sys.argv[1]))
 for name,module in sys.modules.items() if name.startswith('novel_creator') and getattr(module,'__file__',None))
print(json.dumps(result))
'''
        result = update_release._run([prepared['env_python'], '-I', '-B', '-X', 'utf8', '-c', program,
            prepared['package_root'], checkout, json.dumps([str(Path(path).resolve(strict=True)) for path in sources]), target], cwd=cache)
        return json.loads(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-wheel', action='append', required=True)
    parser.add_argument('--target-wheel', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.source_wheel, args.target_wheel), ensure_ascii=False, indent=2))
