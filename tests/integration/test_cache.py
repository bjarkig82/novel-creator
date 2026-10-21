"""A disposable validation proof can never become a source of story facts."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from novel_creator import records, storage
from novel_creator.cli import ToolError
from tests.helpers import envelope, idea, repository, seal, git


class ValidationCacheTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='novel-trusted-key-')
        self.addCleanup(temporary.cleanup)
        self.key = Path(temporary.name).resolve() / 'private-key'
        self.key.write_bytes(os.urandom(32))
        self.key.chmod(0o600)
        configured = patch.dict(os.environ, {'NOVEL_CREATOR_VALIDATION_KEY_FILE': str(self.key)})
        configured.start()
        self.addCleanup(configured.stop)

    def test_novel_supplied_key_is_never_a_validation_authority(self):
        with repository() as root:
            first = envelope(root)
            storage.save(root, first)
            local = root / '.novel-creator/local/cache/key'
            local.write_bytes(os.urandom(32))
            with patch.dict(os.environ, {'NOVEL_CREATOR_VALIDATION_KEY_FILE': str(local)}):
                _, chain = storage.read_snapshot(root)
            self.assertFalse(chain.cache_hit)

    def test_changed_installed_schema_invalidates_prior_proof(self):
        from novel_creator.install import initialize
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            git(root, 'init', '-b', 'main')
            git(root, 'config', 'user.name', 'Schema Cache Test')
            git(root, 'config', 'user.email', 'schema@example.invalid')
            initialize(root, '{}')
            launcher = root / '.novel-creator/run.py'
            command = [sys.executable, '-I', '-B', str(launcher), 'context', '--novel', str(root), '--json']
            valid = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(valid.returncode, 0, valid.stderr)
            before = storage.head(root)
            schema_path = root / '.novel-creator/src/novel_creator/schemas/v1/exchange.schema.json'
            schema = records.loads(schema_path.read_bytes())
            schema['properties']['sequence']['maximum'] = 0
            schema_path.write_text(json.dumps(schema), encoding='utf-8')
            invalid = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(invalid.returncode, 4, invalid.stderr)
            self.assertFalse(json.loads(invalid.stdout)['ok'])
            self.assertEqual(storage.head(root), before)

    def test_cached_blob_content_is_checked_even_when_git_object_id_does_not_change(self):
        import zlib
        with repository() as root:
            first = envelope(root)
            storage.save(root, first)
            storage.read_history(root)
            oid = storage.committed_entries(root, storage.head(root))[storage.bundle_path(first)][1]
            path = root / '.git/objects' / oid[:2] / oid[2:]
            raw = zlib.decompress(path.read_bytes())
            changed = raw.replace(b'Fixture only', b'Fixture evil')
            self.assertNotEqual(raw, changed)
            path.chmod(0o600)
            path.write_bytes(zlib.compress(changed))
            with self.assertRaises(ToolError) as error:
                storage.read_history(root)
            self.assertEqual(error.exception.code, 4)

    def test_warm_read_and_cache_deletion_rebuild_the_same_authoritative_state(self):
        with repository() as root:
            first = envelope(root)
            first = seal(dict(first, record_versions=[idea(first)]))
            storage.save(root, first)
            history, chain = storage.read_snapshot(root)
            expected = chain.snapshot()
            _, warm = storage.read_snapshot(root)
            self.assertTrue(warm.cache_hit)
            cache = root / '.novel-creator/local/cache'
            proof = records.loads((cache / 'validation.json').read_bytes())
            self.assertTrue(proof['derived'])
            self.assertNotIn('records', proof)
            self.assertEqual(git(root, 'status', '--porcelain'), '')
            (cache / 'validation.json').unlink()
            _, rebuilt = storage.read_snapshot(root)
            self.assertFalse(rebuilt.cache_hit)
            self.assertEqual(rebuilt.snapshot(), expected)
            self.assertEqual(storage.read_history(root), history)
            _, warm_again = storage.read_snapshot(root)
            self.assertTrue(warm_again.cache_hit)

    def test_forged_proof_cannot_hide_an_invalid_new_git_snapshot(self):
        with repository() as root:
            first = envelope(root)
            storage.save(root, first)
            storage.read_history(root)
            cache = root / '.novel-creator/local/cache/validation.json'
            proof = records.loads(cache.read_bytes())
            path = root / storage.bundle_path(first)
            path.write_bytes(b'[]')
            git(root, 'add', '--', storage.bundle_path(first))
            git(root, 'commit', '-m', 'Harness invalid context')
            proof['git_head'] = storage.head(root)
            cache.write_text(json.dumps(proof), encoding='utf-8')
            with self.assertRaises(ToolError) as error:
                storage.read_history(root)
            self.assertEqual(error.exception.code, 4)

    def test_tampered_cache_rebuilds_but_new_canon_still_requires_current_authorization(self):
        with repository() as root:
            first = envelope(root)
            first = seal(dict(first, record_versions=[idea(first)]))
            storage.save(root, first)
            storage.read_history(root)
            cache = root / '.novel-creator/local/cache/validation.json'
            cache.write_bytes(b'{damaged cache')
            _, rebuilt = storage.read_snapshot(root)
            self.assertFalse(rebuilt.cache_hit)
            self.assertEqual(rebuilt.snapshot()[first['record_versions'][0]['id']]['status'], 'proposed')
            exchange = envelope(root, previous=first)
            accepted = dict(first['record_versions'][0], revision=2, previous_revision=1, status='accepted')
            exchange = seal(dict(exchange, record_versions=[accepted]))
            before = storage.head(root)
            with self.assertRaises(ToolError) as error:
                storage.save(root, exchange)
            self.assertEqual(error.exception.code, 2)
            self.assertEqual(storage.head(root), before)

    def test_tracked_cache_key_is_not_trusted_after_repository_transfer(self):
        with repository() as root:
            first = envelope(root)
            storage.save(root, first)
            storage.read_history(root)
            (root / '.novel-creator/local/cache/key').write_bytes(b'x' * 32)
            git(root, 'add', '-f', '--', '.novel-creator/local/cache')
            git(root, 'commit', '-m', 'Harness tracked cache is untrusted')
            _, chain = storage.read_snapshot(root)
            self.assertFalse(chain.cache_hit)
