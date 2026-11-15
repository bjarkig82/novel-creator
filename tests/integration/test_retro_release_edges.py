import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.retro_helpers import fixtures, historical
from novel_creator.cli import ToolError


class ReleaseEdges(unittest.TestCase):
    def test_operation_lock_cleanup_quarantines_before_deleting_metadata(self):
        from novel_creator.retro import lock
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'operation.lock'
            with patch('pathlib.Path.unlink',side_effect=OSError('interrupted cleanup')):
                with self.assertRaises(OSError):
                    with lock(path):pass
            self.assertFalse(path.exists())

    def test_local_bookkeeping_lock_is_released_on_process_death(self):
        from novel_creator.retro import lock
        import subprocess,sys
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'state.lock'
            code='from novel_creator.retro import lock;from pathlib import Path;import os,sys\nwith lock(Path(sys.argv[1])):os._exit(0)'
            subprocess.run([sys.executable,'-c',code,str(path)],check=True)
            with lock(path):pass

    def test_terminal_cleanup_after_owner_unlink_can_recover_dead_lock(self):
        from novel_creator.retro import Retro,document,uid
        import json,subprocess,sys
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry)
            item,grant,base=historical(service,checkout,initial,'not_started','prepared');run=item['run_id'];service.release(run)
            base=Path(service.grant()['git_common_dir'])/'novel-creator-retro'
            dead=subprocess.run([sys.executable,'-c','import os;print(os.getpid())'],capture_output=True,check=True,text=True)
            held=base/'operation.lock';held.mkdir()
            binding=document('owner',run_id=run,grant_id=service.grant()['grant_id'],novel_root=str(root))
            (held/'holder.json').write_text(json.dumps(dict(retro_version=1,document='lock',pid=int(dead.stdout),token=uid(),owner=binding)))
            self.assertFalse((base/'owner.json').exists())
            service.disable();service.enable(checkout,recovery_only=True)
            self.assertEqual(service.resume(run)['status'],'abandoned')
            self.assertFalse(held.exists())


    def test_terminal_cleanup_never_removes_foreign_claim(self):
        from novel_creator.retro import Retro,document,write,uid
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry)
            item,grant,base=historical(service,checkout,initial,'not_started','prepared');run=item['run_id'];service.release(run)
            owner=Path(service.grant()['git_common_dir'])/'novel-creator-retro/owner.json'
            foreign=document('owner',run_id=uid(),grant_id=service.grant()['grant_id'],novel_root=str(root))
            write(owner,foreign,'owner')
            service.resume(run)
            self.assertTrue(owner.exists())


    def test_inspection_mutex_excludes_other_inspectors_and_acquisition(self):
        from novel_creator.retro import inspection_guard
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp).resolve()
            with inspection_guard(base):
                with self.assertRaises(ToolError):
                    with inspection_guard(base):pass
