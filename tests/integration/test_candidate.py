"""Candidate verification rejects altered trees, ancestry and exchange bytes."""
from contextlib import contextmanager, ExitStack
import json
import hashlib
import stat
import unittest
from unittest.mock import patch
import zlib

from novel_creator import storage
from novel_creator.cli import ToolError
from tests.helpers import envelope, repository, seal, git


@contextmanager
def corrupt_loose_blob(root, oid, raw):
    path = root / '.git/objects' / oid[:2] / oid[2:]
    original = path.read_bytes()
    mode = stat.S_IMODE(path.stat().st_mode)
    path.chmod(mode | stat.S_IWUSR)
    try:
        path.write_bytes(zlib.compress(b'blob ' + str(len(raw)).encode() + b'\0' + raw))
        yield
    finally:
        path.write_bytes(original)
        path.chmod(mode)


class CandidateTests(unittest.TestCase):
    def candidate(self, root, changes, parents):
        environment = {'GIT_INDEX_FILE': str(root / '.novel-creator/local/candidate-index')}
        storage.git(root, 'read-tree', 'HEAD', env=environment)
        for path, raw in changes.items():
            if raw is None:
                storage.git(root, 'update-index', '--force-remove', '--', path, env=environment)
            else:
                oid = storage.git(root, 'hash-object', '-w', '--stdin', input=raw).decode().strip()
                storage.git(root, 'update-index', '--add', '--cacheinfo', f'100644,{oid},{path}', env=environment)
        tree = storage.git(root, 'write-tree', env=environment).decode().strip()
        arguments = ['commit-tree', tree, '-m', 'Unpublished test candidate']
        for parent in parents:
            arguments += ['-p', parent]
        return storage.git(root, *arguments).decode().strip()

    def test_candidate_rejects_corrupt_blob_with_equivalent_json_for_both_object_formats(self):
        for object_format in ('sha1', 'sha256'):
            with self.subTest(object_format=object_format), repository(object_format=object_format) as root:
                initial = storage.head(root)
                index = (root / '.git/index').read_bytes()
                baseline = storage.committed_entries(root, initial)
                bundle = envelope(root)
                path = storage.bundle_path(bundle)
                raw = json.dumps(bundle, ensure_ascii=False, indent=2).encode('utf-8')
                candidate = self.candidate(root, {path: raw}, [initial])
                oid = storage.committed_entries(root, candidate)[path][1]
                # Git's loose-object reader returns these bytes under the requested
                # OID without recomputing their identity. Meaning and payload digest
                # are unchanged, but publishing this object would confirm corruption.
                equivalent = json.dumps(bundle, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
                self.assertEqual(json.loads(raw), json.loads(equivalent))
                body = b'blob ' + str(len(equivalent)).encode() + b'\0' + equivalent
                self.assertNotEqual(hashlib.new(object_format, body).hexdigest(), oid)
                with corrupt_loose_blob(root, oid, equivalent):
                    self.assertEqual(storage.git(root, 'cat-file', 'blob', oid), equivalent)
                    with self.assertRaises(ToolError) as error:
                        storage._verify_candidate(root, candidate, initial, baseline, [path], bundle)
                    self.assertEqual(error.exception.code, 5)
                    self.assertEqual(storage.head(root), initial)
                    self.assertEqual((root / '.git/index').read_bytes(), index)

    def test_save_rejects_corrupt_new_blob_without_publication_then_retries_once(self):
        for object_format in ('sha1', 'sha256'):
            with self.subTest(object_format=object_format), repository(object_format=object_format) as root:
                first = envelope(root)
                storage.save(root, first)
                initial = storage.head(root)
                index = (root / '.git/index').read_bytes()
                pending = envelope(root, previous=first)
                path = storage.bundle_path(pending)
                equivalent = json.dumps(pending, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
                original_git = storage.git
                with ExitStack() as corrupted:
                    def corrupt_candidate(root, *args, **kwargs):
                        result = original_git(root, *args, **kwargs)
                        if args[0] == 'commit-tree':
                            candidate = result.decode().strip()
                            oid = storage.committed_entries(root, candidate)[path][1]
                            corrupted.enter_context(corrupt_loose_blob(root, oid, equivalent))
                        return result
                    with patch.object(storage, 'git', corrupt_candidate):
                        with self.assertRaises(ToolError) as error:
                            storage.save(root, pending)
                        self.assertEqual(error.exception.code, 5)
                        self.assertEqual(storage.head(root), initial)
                        self.assertEqual((root / '.git/index').read_bytes(), index)
                        self.assertEqual(storage.read_history(root), [first])
                        receipt = root / '.novel-creator/local' / (pending['exchange_id'] + '.json')
                        state = storage.read_receipt(root, receipt)
                        self.assertEqual(state['state'], 'pending')
                        self.assertEqual(state['bundle'], pending)
                        self.assertTrue((root / path).is_file())
                saved = storage.save(root, pending)
                self.assertTrue(saved['data']['saved'])
                self.assertFalse(saved['data']['cleanup_required'])
                self.assertEqual(storage.read_history(root), [first, pending])
                repeated = storage.save(root, pending)
                self.assertTrue(repeated['data']['already_saved'])
                self.assertEqual(repeated['checkpoint'], saved['checkpoint'])

    def test_candidate_rejects_truncated_or_forged_batch_objects(self):
        with repository() as root:
            initial = storage.head(root)
            baseline = storage.committed_entries(root, initial)
            bundle = envelope(root)
            path = storage.bundle_path(bundle)
            raw = json.dumps(bundle).encode()
            candidate = self.candidate(root, {path: raw}, [initial])
            oid = storage.committed_entries(root, candidate)[path][1]
            commit = storage.git(root, 'cat-file', 'commit', candidate)
            response = (f'{candidate} commit {len(commit)}\n'.encode() + commit + b'\n' +
                        f'{oid} blob {len(raw)}\n'.encode() + raw + b'\n')
            original = storage.git
            for bad in (response[:-2], response + b'extra',
                        response.replace(b' commit ', b' blob ', 1),
                        response.replace(b'Unpublished test candidate', b'Unpublished evil candidate'),
                        response.replace(b'Fixture only', b'Fixture evil')):
                self.assertNotEqual(bad, response)
                def altered(root, *args, **kwargs):
                    return bad if args[:2] == ('cat-file', '--batch') else original(root, *args, **kwargs)
                with self.subTest(response=bad[-20:]), patch.object(storage, 'git', altered):
                    with self.assertRaises(ToolError) as error:
                        storage._verify_candidate(root, candidate, initial, baseline, [path], bundle)
                    self.assertEqual(error.exception.code, 5)
            self.assertEqual(storage.head(root), initial)

    def test_candidate_checks_full_tree_parent_and_exact_exchange_for_both_object_formats(self):
        self.assertTrue(callable(getattr(storage, '_verify_candidate', None)),
                        'Candidate verification needs a shared tree/parent/content check')
        for object_format in ('sha1', 'sha256'):
            with self.subTest(object_format=object_format), repository(object_format=object_format) as root:
                (root / 'manuscript.txt').write_bytes(b'Protected original manuscript\n')
                git(root, 'add', 'manuscript.txt')
                git(root, 'commit', '-m', 'Existing manuscript')
                initial = storage.head(root)
                baseline = storage.committed_entries(root, initial)
                index = (root / '.git/index').read_bytes()
                bundle = envelope(root)
                bundle['continuity_review']['summary'] = 'Exact Þóra text\r\nwith a final newline\n'
                bundle = seal(bundle)
                path = storage.bundle_path(bundle)
                raw = json.dumps(bundle, ensure_ascii=False, indent=2).encode('utf-8')
                valid = self.candidate(root, {path: raw}, [initial])
                verified = storage._verify_candidate(root, valid, initial, baseline, [path], bundle)
                self.assertEqual(verified, storage.committed_entries(root, valid))
                changed = seal(dict(bundle, recorded_at='2026-10-22T12:00:00Z'))
                cases = [
                    ({path: raw, 'foreign.txt': b'Unexpected file'}, [initial]),
                    ({path: raw, 'manuscript.txt': b'Changed manuscript'}, [initial]),
                    ({path: raw, 'manuscript.txt': None}, [initial]),
                    ({path: raw}, []),
                    ({path: json.dumps(changed).encode()}, [initial]),
                    ({path: b'{broken JSON'}, [initial]),
                ]
                for changes, parents in cases:
                    with self.subTest(paths=list(changes), parents=parents):
                        candidate = self.candidate(root, changes, parents)
                        with self.assertRaises(ToolError) as error:
                            storage._verify_candidate(root, candidate, initial, baseline, [path], bundle)
                        self.assertEqual(error.exception.code, 5)
                        self.assertEqual(storage.head(root), initial)
                        self.assertEqual((root / '.git/index').read_bytes(), index)
                        self.assertEqual((root / 'manuscript.txt').read_bytes(), b'Protected original manuscript\n')
