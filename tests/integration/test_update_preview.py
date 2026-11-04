import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

from novel_creator import update, storage, records, update_release
from novel_creator.cli import ToolError
from tests.helpers import git
from tests.update_helpers import historical_book, artifact, snapshot, add_writer_work
from tests.update_release_helpers import product_wheel, release_listing


def transport_for(version):
    return release_listing({version: artifact(version)[0].read_bytes(), '0.3.0': product_wheel()[0]})


class PreviewTests(unittest.TestCase):
    def test_unsupported_git_is_refused_before_release_lookup(self):
        from tests.update_release_helpers import FakeReleaseTransport
        with historical_book('0.2.0') as book:
            original = storage.git
            def old_git(root, *arguments, **kwargs):
                return b'git version 2.38.0\n' if arguments == ('--version',) else original(root, *arguments, **kwargs)
            before = snapshot(book.root)
            transport = FakeReleaseTransport()
            with patch('novel_creator.storage.git', side_effect=old_git):
                with self.assertRaises(ToolError) as caught:
                    update.preview(book.root, transport=transport)
            self.assertEqual(caught.exception.code, 4)
            self.assertEqual(snapshot(book.root), before)
            self.assertEqual(transport.requests, [])

    def test_unknown_or_boolean_installation_formats_fail_before_release_lookup(self):
        from tests.update_release_helpers import FakeReleaseTransport
        with historical_book('0.2.0') as book:
            path = book.root / update.MANIFEST
            original = records.loads(path.read_bytes())
            transport = FakeReleaseTransport()
            for value in (True, 3, '2'):
                with self.subTest(value=value):
                    path.write_text(json.dumps(dict(original, installation_format=value)))
                    before = snapshot(book.root)
                    with self.assertRaises(ToolError) as caught:
                        update.preview(book.root, transport=transport)
                    self.assertEqual(caught.exception.code, 4)
                    self.assertEqual(snapshot(book.root), before)
                    self.assertEqual(transport.requests, [])

    def test_book_pinned_controller_cannot_preview_or_apply_itself(self):
        with historical_book('0.2.0') as book:
            before = snapshot(book.root)
            with patch('novel_creator.update.__file__', str(book.root / '.novel-creator/src/novel_creator/update.py')):
                with self.assertRaises(ToolError) as caught:
                    update.preview(book.root, transport=transport_for('0.2.0'))
                self.assertEqual(caught.exception.code, 4)
                with self.assertRaises(ToolError):
                    update.apply(book.root, preview_id='00000000-0000-4000-8000-000000000000',
                                 version='0.3.0', expected_head=storage.head(book.root), confirm_quiescent=True)
            self.assertEqual(snapshot(book.root), before)

    def test_historical_preview_preserves_book_custom_instructions_and_staging(self):
        for version in ('0.1.0', '0.2.0'):
            with self.subTest(version=version), historical_book(version) as book, tempfile.TemporaryDirectory() as cache:
                add_writer_work(book.root)
                custom = b'# My private instructions\nKeep this exact wording.\n'
                (book.root / 'AGENTS.md').write_bytes(custom)
                before = snapshot(book.root)
                transport = transport_for(version)
                with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                    result = update.preview(book.root, transport=transport)
                self.assertEqual(snapshot(book.root), before)
                data = result['data']
                self.assertEqual(data['state'], 'preview')
                self.assertFalse(data['ready'])
                self.assertEqual(data['target_version'], '0.3.0')
                self.assertNotIn('AGENTS.md', [item['path'] for item in data['changes']])
                self.assertTrue((Path(cache) / 'previews' / (data['preview_id'] + '.json')).is_file())
                for url in transport.requests:
                    self.assertNotIn(str(book.root), url)
                self.assertEqual((book.root / 'AGENTS.md').read_bytes(), custom)

    def test_fingerprint_covers_untracked_index_and_ignored_operational_evidence(self):
        with historical_book('0.2.0') as book:
            initial = update.fingerprint(book.root)
            manuscript = book.root / 'draft.txt'
            manuscript.write_text('one')
            untracked = update.fingerprint(book.root)
            self.assertNotEqual(initial, untracked)
            git(book.root, 'add', 'draft.txt')
            staged = update.fingerprint(book.root)
            self.assertNotEqual(untracked, staged)
            local = book.root / '.novel-creator/local/private-evidence.json'
            local.write_text('{"evidence":true}')
            self.assertNotEqual(staged, update.fingerprint(book.root))

    def test_same_version_is_noop_and_failed_lookup_is_unknown(self):
        with historical_book('0.2.0') as book:
            before = snapshot(book.root)
            transport = release_listing({'0.2.0': artifact('0.2.0')[0].read_bytes()})
            with patch('novel_creator.update_release.prepare', side_effect=AssertionError('unneeded installation')):
                self.assertEqual(update.preview(book.root, transport=transport)['data']['state'], 'already_current')
            self.assertEqual(snapshot(book.root), before)
            transport.responses.clear()
            with self.assertRaises(ToolError):
                update.preview(book.root, transport=transport)
            self.assertEqual(snapshot(book.root), before)

    def test_cache_inside_book_is_refused_before_any_creation(self):
        with historical_book('0.2.0') as book:
            before = snapshot(book.root)
            with patch('novel_creator.update_release.cache_home', return_value=book.root / 'cache'):
                with self.assertRaises(ToolError):
                    update.preview(book.root, transport=transport_for('0.2.0'))
            self.assertEqual(snapshot(book.root), before)

    def test_changed_exclusive_resource_is_refused(self):
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as cache:
            manifest = records.loads((book.root / '.novel-creator/manifest.json').read_bytes())
            resource = next(path for path in manifest['managed_paths'] if path.startswith('.novel-creator/src/'))
            (book.root / resource).write_bytes(b'changed')
            before = snapshot(book.root)
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                with self.assertRaises(ToolError) as caught:
                    update.preview(book.root, transport=transport_for('0.2.0'))
            self.assertEqual(caught.exception.code, 3)
            self.assertEqual(snapshot(book.root), before)

    def test_distinct_selected_interpreter_is_bound_and_book_race_refuses_preview(self):
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as cache:
            cache = Path(cache)
            python = update_release.create_environment(cache / 'selected', sys.executable)
            before = snapshot(book.root)
            with patch('novel_creator.update_release.cache_home', return_value=cache):
                result = update.preview(book.root, python=python, transport=transport_for('0.2.0'))
                self.assertEqual(result['data']['runtime_python'], python)
                document = records.loads((cache / 'previews' / (result['data']['preview_id'] + '.json')).read_bytes())
                self.assertEqual(document['runtime_python'], python)
                self.assertEqual(document['runtime_fingerprint'], update_release.runtime_info(python)['fingerprint'])
                self.assertEqual(snapshot(book.root), before)
                def race(*args):
                    (book.root / 'concurrent-writer.txt').write_text('keep this work')
                    return {'valid': True}
                with patch('novel_creator.update_release.probe_prepared', side_effect=race):
                    with self.assertRaises(ToolError) as caught:
                        update.preview(book.root, python=python, transport=transport_for('0.2.0'))
                self.assertEqual(caught.exception.code, 3)
                self.assertEqual((book.root / 'concurrent-writer.txt').read_text(), 'keep this work')

    def test_target_collision_and_staged_affected_shared_file_are_preserved(self):
        with historical_book('0.2.0') as book, tempfile.TemporaryDirectory() as cache:
            collision = book.root / '.novel-creator/src/novel_creator/update.py'
            collision.write_bytes(b'writer-owned content')
            with patch('novel_creator.update_release.cache_home', return_value=Path(cache)):
                before = snapshot(book.root)
                with self.assertRaises(ToolError) as caught:
                    update.preview(book.root, transport=transport_for('0.2.0'))
                self.assertEqual(caught.exception.code, 3)
                self.assertEqual(snapshot(book.root), before)
                collision.unlink()
                (book.root / '.gitignore').write_bytes(b'.novel-creator/local/\n# custom staged rules\n')
                git(book.root, 'add', '.gitignore')
                before = snapshot(book.root)
                with self.assertRaises(ToolError) as caught:
                    update.preview(book.root, transport=transport_for('0.2.0'))
                self.assertEqual(caught.exception.code, 3)
                self.assertEqual(snapshot(book.root), before)
