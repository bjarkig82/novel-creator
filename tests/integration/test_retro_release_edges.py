import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.retro_helpers import fixtures
from tests.retro_contribution_helpers import prepared,ready_prepare
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
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.release(run)
            base=Path(service.grant()['git_common_dir'])/'novel-creator-retro'
            dead=subprocess.run([sys.executable,'-c','import os;print(os.getpid())'],capture_output=True,check=True,text=True)
            held=base/'operation.lock';held.mkdir()
            binding=document('owner',run_id=run,grant_id=service.grant()['grant_id'],novel_root=str(root))
            (held/'holder.json').write_text(json.dumps(dict(retro_version=1,document='lock',pid=int(dead.stdout),token=uid(),owner=binding)))
            self.assertFalse((base/'owner.json').exists())
            service.disable();service.enable(checkout,authorize=True)
            self.assertEqual(service.resume(run)['status'],'abandoned')
            self.assertFalse(held.exists())

    def test_terminal_cleanup_retries_without_republishing(self):
        from novel_creator.retro import Retro
        from tests.retro_contribution_helpers import selected
        for terminal in ('published', 'abandoned', 'duplicate'):
            with self.subTest(terminal=terminal), fixtures() as (root,checkout,registry,fake,initial):
                service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
                run,data=prepared(service,root,initial);service.validate_contribution(run,data)
                with patch.object(service,'release_owner',side_effect=OSError('interrupted cleanup')):
                    with self.assertRaises((OSError,ToolError)):
                        if terminal=='abandoned':service.release(run)
                        else:service.publish(run)
                item=service.run(run)
                # A duplicate terminal receipt has the same durable ownership boundary.
                if terminal=='duplicate':item['status']='duplicate';service.save_run(item)
                owner=Path(service.grant()['git_common_dir'])/'novel-creator-retro/owner.json'
                self.assertTrue(owner.exists())
                before=list(fake.calls);service.disable()
                with self.assertRaises(ToolError):service.resume(run)
                self.assertTrue(owner.exists());self.assertEqual(fake.calls,before)
                service.enable(checkout,authorize=True)
                service.release(run)
                self.assertFalse(owner.exists())
                self.assertEqual(fake.calls.count('create'),0 if terminal=='abandoned' else 1)
                fake.pulls.clear()
                later=selected(service,root,initial,turn='later')
                self.assertEqual(ready_prepare(service,later)['status'],'prepared')

    def test_terminal_cleanup_never_removes_foreign_claim(self):
        from novel_creator.retro import Retro,document,write,uid
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.release(run)
            owner=Path(service.grant()['git_common_dir'])/'novel-creator-retro/owner.json'
            foreign=document('owner',run_id=uid(),grant_id=service.grant()['grant_id'],novel_root=str(root))
            write(owner,foreign,'owner')
            service.resume(run)
            self.assertTrue(owner.exists())

    def test_release_preserves_pr_discovered_during_reconciliation(self):
        from novel_creator.retro import Retro
        with fixtures() as (root,checkout,registry,fake,initial):
            service=Retro(root,github=fake,registry=registry);service.enable(checkout,authorize=True)
            run,data=prepared(service,root,initial);service.validate_contribution(run,data)
            fake.unknown_create=True
            with self.assertRaises(ToolError):service.publish(run)
            self.assertEqual(service.release(run)['status'],'published')
            self.assertEqual(service.run(run)['status'],'published')

    def test_inspection_mutex_excludes_other_inspectors_and_acquisition(self):
        from novel_creator.retro import inspection_guard
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp).resolve()
            with inspection_guard(base):
                with self.assertRaises(ToolError):
                    with inspection_guard(base):pass
