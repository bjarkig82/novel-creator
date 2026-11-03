"""Synthetic contribution preparation shared by publication/recovery tests."""
import sys
from tests.contract.test_retro_review import begin_input


def selected(service, root, initial, turn='task-1'):
    run = service.begin(begin_input(root,initial,turn))['run_id']
    service.review(run, {'outcome':'selected','category':'runtime',
                        'problem':'A synthetic parser rejects a valid empty collection.',
                        'reproduction':'Pass an empty synthetic collection to the parser.',
                        'evidence_refs':[initial['exchange_id']]})
    return run


def prepared(service, root, initial):
    run=selected(service,root,initial)
    target=ready_prepare(service,run)
    from pathlib import Path
    (Path(target['worktree'])/'synthetic_fix.txt').write_text('accept empty collection\n')
    body=service.path('inputs/public.md'); body.parent.mkdir(parents=True,exist_ok=True)
    body.write_text('Fix the synthetic parser. Validation: a synthetic empty collection is accepted.')
    values={'checks':[[sys.executable,'-c','print("synthetic check passed")']],
            'title':'Fix synthetic empty-collection parsing', 'body_file':str(body),
            'privacy_approved':True,'synthetic_only':True}
    return run,values


def ready_prepare(service, run):
    target=service.prepare(run)
    if target['status']=='comparison_required':
        service.compare(run,{'snapshot':target['snapshot'],'equivalent_pr':None,
                            'upstream_fix_present':False,'public_scope_reviewed':True})
        target=service.prepare(run)
    return target
