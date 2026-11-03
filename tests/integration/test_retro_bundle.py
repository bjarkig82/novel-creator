import json
import tempfile
import unittest
from pathlib import Path
from tests.helpers import git
from novel_creator.install import initialize


class RetroBundleCompatibility(unittest.TestCase):
    def test_old_pinned_bundle_is_not_upgraded_on_continuation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve()/'novel';root.mkdir()
            git(root,'init','-b','main');git(root,'config','user.name','Test')
            git(root,'config','user.email','test@example.invalid')
            initialize(root,'{}')
            manifest_path=root/'.novel-creator/manifest.json'
            manifest=json.loads(manifest_path.read_text())
            removed=[]
            for relative in list(manifest['checksums']):
                if 'retrospective' in relative or '/retro' in relative:
                    (root/relative).unlink();removed.append(relative)
                    manifest['checksums'].pop(relative)
            manifest['managed_paths']=[p for p in manifest['managed_paths'] if p not in removed]
            manifest_path.write_text(json.dumps(manifest))
            git(root,'add','--all');git(root,'commit','-m','Synthetic older pinned bundle')
            before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*')
                    if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts}
            head=git(root,'rev-parse','HEAD');index=git(root,'ls-files','--stage')
            initialize(root,'{}')
            after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*')
                    if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.parts}
            self.assertEqual(before,after)
            self.assertEqual(head,git(root,'rev-parse','HEAD'))
            self.assertEqual(index,git(root,'ls-files','--stage'))
