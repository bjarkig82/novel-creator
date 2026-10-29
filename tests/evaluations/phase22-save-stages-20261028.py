"""Current-source ordinary-layout stage timings. No GC, guard, parser or Git policy changes."""
from contextlib import ExitStack
import hashlib,json,shutil,statistics,sys,threading,time
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path.cwd()))
from novel_creator import records,storage,validation,validation_cache
from novel_creator.context import read
from tests.helpers import repository,git
from tests.performance import benchmark_records as benchmark
with benchmark.benchmark_key(True),repository() as root:
    novel_id=records.loads((root/'.novel-creator/manifest.json').read_bytes())['novel_id']
    history,fixture=benchmark.generate(novel_id)
    for exchange in history:
        path=root/storage.bundle_path(exchange);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(benchmark.serialized(exchange))
    git(root,'add','--','story/exchanges');git(root,'commit','-m','Current ordinary-layout save stage timing fixture')
    del history,exchange
    read(root);fixture['fully_validated']=True
    frozen=hashlib.sha256(Path(storage.__file__).read_bytes()).hexdigest()
    print(json.dumps({'fixture':fixture,'source_sha256':frozen,'git_executable':shutil.which('git'),'method':'Two untraced controls around two lightweight traced save calls on one ordinary-layout default-Git fixture; preparation graph retained as in benchmark; timings overlap across threads, not additive; not p95'}),flush=True)
    for traced in (False,True,True,False):
        prior=storage.read_history(root)
        exchange=records.new_exchange(novel_id,previous=prior[-1],expected_head=storage.head(root),messages=[{'message_id':benchmark.uid(),'role':'user','text':'Continue.'},{'message_id':benchmark.uid(),'role':'assistant','text':'Continuation.'}])
        exchange['payload_digest']=records.digest(exchange)
        events=[];counters={};origin=time.perf_counter()
        def wrapped(original,name):
            def invoke(*args,**kwargs):
                start=time.perf_counter();cpu_start=time.thread_time() if name=='_checked_path' else None
                try:return original(*args,**kwargs)
                finally:
                    end=time.perf_counter();thread=threading.get_ident()
                    if name=='_checked_path':
                        count,elapsed,cpu=counters.get(thread,(0,0,0));counters[thread]=(count+1,elapsed+end-start,cpu+time.thread_time()-cpu_start)
                    else:
                        item={'stage':name,'thread':thread,'start':start-origin,'end':end-origin,'seconds':end-start}
                        if name=='git':
                            item['command']=args[1]
                            if args[1]=='hash-object':item['full_managed_files']='--stdin-paths' in args
                        events.append(item)
            return invoke
        with ExitStack() as stack:
            if traced:
                for name in ('git','_read_snapshot','check_managed','_verify_candidate','atomic_json','sync_index','_checked_path','fsync_directory'):
                    stack.enter_context(patch.object(storage,name,wrapped(getattr(storage,name),name)))
                for name in ('trusted','remember'):
                    stack.enter_context(patch.object(validation_cache,name,wrapped(getattr(validation_cache,name),'cache.'+name)))
                stack.enter_context(patch.object(validation.ExchangeValidator,'append',wrapped(validation.ExchangeValidator.append,'validate_new_exchange')))
            start=time.perf_counter();result=storage.save(root,exchange);seconds=time.perf_counter()-start
        assert not result['data']['cleanup_required']
        data={'traced':traced,'seconds':seconds,'sequence':result['checkpoint']['sequence']}
        if traced:
            data.update(events=sorted(events,key=lambda e:e['start']),path_counters={str(k):{'calls':v[0],'seconds':v[1],'thread_cpu_seconds':v[2]} for k,v in counters.items()})
            h=next(e for e in events if e['stage']=='_read_snapshot')
            guards=sorted((e for e in events if e['stage']=='check_managed'),key=lambda e:e['start'])
            data['first_guard_history_overlap_seconds']=max(0,min(h['end'],guards[0]['end'])-max(h['start'],guards[0]['start']))
        print(json.dumps(data),flush=True)
    assert frozen==hashlib.sha256(Path(storage.__file__).read_bytes()).hexdigest()

