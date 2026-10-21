"""Run from the repository root: python -B -m tests.performance.benchmark_records.

Creates only disposable repositories. Model latency and human judgments are absent.
Each operation has a bounded subprocess lifetime; a timeout never becomes a p95.
"""
import argparse
from contextlib import contextmanager
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

from novel_creator import records, storage, validation_cache
from novel_creator.context import read
from novel_creator.install import bootstrap
from tests.helpers import git, record, repository, uid


def serialized(bundle):
    return json.dumps(bundle, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def generate(novel_id, *, exchanges=5000, sessions=100, assertions=10000, minimum_bytes=25 * 1024 * 1024):
    if exchanges < 2 or not 0 < sessions < exchanges or assertions < 1 or minimum_bytes < 0:
        raise ValueError('Need >=2 exchanges, 1..exchanges-1 sessions, positive assertions and nonnegative size')
    initial = bootstrap('{"title":"Þóra: scale fixture","manuscript_language":"is"}', novel_id)
    subject = record(initial, 'story_element', element_type='character', display_name='Þóra', aliases=[],
        status='proposed', assertion_ids=[], relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[])
    initial['record_versions'].append(subject)
    initial['payload_digest'] = records.digest(initial)
    history, session_ids = [initial], []
    remaining = assertions
    unknown = {'precision': 'unknown', 'event_anchor': None, 'start': None, 'end': None, 'before_refs': [], 'after_refs': []}
    for index in range(1, exchanges):
        exchange = records.new_exchange(novel_id, previous=history[-1], messages=[
            {'message_id': uid(), 'role': 'user', 'text': 'Accept the designated fixture assertions.'},
            {'message_id': uid(), 'role': 'assistant', 'text': 'Saved structural fixture; no literary judgment.'}])
        source = records.current_user_source(exchange)
        versions = []
        if len(session_ids) < sessions:
            session = records.start_session(exchange, topic='Fixture session ' + str(index))
            session_ids.append(session['id'])
            versions.append(session)
        exchange['session_id'] = session_ids[(index - 1) % len(session_ids)]
        count = math.ceil(remaining / (exchanges - index))
        assertions_here = []
        for offset in range(count):
            perspective = ('author_truth', 'character_knowledge', 'character_belief', 'reader_revelation')[(index + offset) % 4]
            assertions_here.append(record(exchange, 'assertion', subject_element_id=subject['id'],
                predicate='fixture property ' + str(assertions - remaining + offset), value='Þóra / mixed language',
                perspective=perspective, holder_id=subject['id'] if perspective.startswith('character_') else None,
                reader_audience='reader' if perspective == 'reader_revelation' else None,
                time_ref={'chronology': unknown, 'narrative': unknown}, truth_state='affirmed',
                status='accepted', decision_ids=[], supersedes=None, source_refs=[source], origin='supplied'))
        remaining -= count
        if assertions_here:
            targets = [{'id': r['id'], 'revision': 1} for r in assertions_here]
            decision = record(exchange, 'decision', action='accept', user_message_ref=source,
                span={'start': 0, 'end': len(exchange['messages'][0]['text'])}, target_refs=targets,
                selected_parts=[], prior_refs=[], result_refs=targets, reason='Generated structural fixture',
                affected_refs=[], review_required_refs=[], source_refs=[source], origin='supplied')
            for assertion in assertions_here:
                assertion['decision_ids'] = [decision['id']]
            versions.extend([*assertions_here, decision])
        exchange.update(record_versions=versions, continuity_review={
            'coverage': 'complete', 'reviewed_record_refs': [], 'unavailable_refs': [],
            'canon_hold_refs': [], 'finding_ids': [], 'summary': 'Synthetic scale fixture, not literary evidence'})
        exchange['payload_digest'] = records.digest(exchange)
        history.append(exchange)
    size = sum(len(serialized(e)) for e in history)
    padding = math.ceil(max(0, minimum_bytes - size) / (exchanges - 1))
    for index, exchange in enumerate(history):
        if index:
            exchange['messages'][-1]['text'] += 'x' * padding
            exchange['previous_digest'] = history[index - 1]['payload_digest']
        exchange['payload_digest'] = records.digest(exchange)
    return history, {'sessions': sessions, 'exchanges': exchanges, 'active_assertions': assertions,
                     'json_bytes': sum(len(serialized(e)) for e in history),
                     'synthetic': True, 'fully_validated': False}


def worker(root, operation):
    if operation == 'read':
        started = time.perf_counter()
        data = read(root)
        count = len(data['data']['records'])
    else:
        history = storage.read_history(root)
        exchange = records.new_exchange(history[0]['novel_id'], previous=history[-1], expected_head=storage.head(root),
            messages=[{'message_id': uid(), 'role': 'user', 'text': 'Continue the benchmark.'},
                      {'message_id': uid(), 'role': 'assistant', 'text': 'Benchmark continuation.'}])
        exchange['payload_digest'] = records.digest(exchange)
        # Preparing a payload is separate from the validation/local-save target.
        # storage.save itself reads and validates the authoritative chain.
        started = time.perf_counter()
        result = storage.save(root, exchange)
        if result['data']['cleanup_required']:
            raise RuntimeError('Save requires cleanup')
        count = result['checkpoint']['sequence']
    return {'seconds': time.perf_counter() - started, 'observed_count': count}


def measure(root, operation, timeout):
    started = time.perf_counter()
    try:
        result = subprocess.run([sys.executable, '-B', '-m', 'tests.performance.benchmark_records',
            '--worker', operation, '--novel', str(root)], capture_output=True, text=True,
            encoding='utf-8', timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'status': 'timeout', 'elapsed_lower_bound_seconds': timeout,
                'wall_seconds': time.perf_counter() - started}
    if result.returncode:
        return {'status': 'error', 'returncode': result.returncode, 'stderr': result.stderr[-3000:]}
    return {'status': 'ok', **json.loads(result.stdout)}


@contextmanager
def benchmark_key(enabled):
    """Explicit trusted runtime setup, outside every disposable novel repository."""
    previous = os.environ.pop(validation_cache.KEY_ENV, None)
    try:
        if not enabled:
            yield
        else:
            with tempfile.TemporaryDirectory(prefix='novel-benchmark-key-') as folder:
                key = Path(folder).resolve() / 'key'
                descriptor = os.open(key, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                with os.fdopen(descriptor, 'wb') as stream:
                    stream.write(os.urandom(32))
                os.environ[validation_cache.KEY_ENV] = str(key)
                yield
    finally:
        if previous is None:
            os.environ.pop(validation_cache.KEY_ENV, None)
        else:
            os.environ[validation_cache.KEY_ENV] = previous


def run(args):
    result = {'environment': {'os': platform.platform(), 'python': platform.python_version(),
        'processor': platform.processor(), 'logical_cpus': os.cpu_count(),
        'git': subprocess.run(['git', '--version'], capture_output=True, text=True, check=True).stdout.strip()},
        'method': 'Fresh subprocess per operation; filesystem-warm runs; interpreter import time excluded. '
                  'Timeout deadlines include worker startup/imports. '
                  'Cold means first fixture read, not a guaranteed OS page-cache flush. '
                  'Save includes committed-history reads, validation, local Git publication and cleanup. '
                  'Fixture generated in one harness snapshot; each warm save appends one exchange.',
        'requested_warm_runs': args.runs, 'timeout_seconds': args.timeout, 'model_latency': 'excluded',
        'validation_cache': 'disabled' if args.no_validation_cache else 'opt-in; temporary private key outside novel'}
    with benchmark_key(not args.no_validation_cache), repository() as root:
        novel_id = records.loads((root / '.novel-creator/manifest.json').read_bytes())['novel_id']
        history, fixture = generate(novel_id, exchanges=args.exchanges, sessions=args.sessions,
            assertions=args.assertions, minimum_bytes=args.mib * 1024 * 1024)
        for exchange in history:
            path = root / storage.bundle_path(exchange)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(serialized(exchange))
        git(root, 'add', '--', 'story/exchanges')
        git(root, 'commit', '-m', 'Generated scale fixture snapshot')
        result['fixture'] = fixture
        if args.progress:
            print('Fixture ready; measuring cold read.', file=sys.stderr, flush=True)
        result['cold_read'] = measure(root, 'read', args.timeout)
        fixture['fully_validated'] = result['cold_read']['status'] == 'ok'
        for operation, target in [('read', 2.0), ('save', 1.0)]:
            samples = []
            failure = None
            if not fixture['fully_validated']:
                failure = {'status': 'not_run', 'reason': 'Cold validation did not complete successfully'}
            else:
                for _ in range(args.runs):
                    observed = measure(root, operation, args.timeout)
                    if args.progress:
                        print(f'{operation} {len(samples) + 1}/{args.runs}: {observed}', file=sys.stderr, flush=True)
                    if observed['status'] != 'ok':
                        failure = observed
                        break
                    samples.append(observed['seconds'])
            p95 = sorted(samples)[math.ceil(len(samples) * .95) - 1] if len(samples) == args.runs else None
            result[operation] = {'samples_seconds': samples, 'completed_runs': len(samples), 'failure': failure,
                'p95_seconds': p95, 'target_seconds': target,
                'passes': p95 is not None and p95 <= target}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exchanges', type=int, default=5000)
    parser.add_argument('--sessions', type=int, default=100)
    parser.add_argument('--assertions', type=int, default=10000)
    parser.add_argument('--mib', type=int, default=25)
    parser.add_argument('--runs', type=int, default=30)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--progress', action='store_true')
    parser.add_argument('--no-validation-cache', action='store_true')
    parser.add_argument('--worker', choices=['read', 'save'])
    parser.add_argument('--novel', type=Path)
    args = parser.parse_args()
    if args.runs < 1 or args.timeout <= 0:
        parser.error('Positive run count and timeout required')
    result = worker(args.novel, args.worker) if args.worker else run(args)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)
    return 0 if args.worker or (result['read']['passes'] and result['save']['passes']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
