"""Verify observed public input/save/display evidence; never assign literary scores.

Run with --run tests/evaluations/phase22-runs/<run>. Missing submitted cases fail.
Public observations must be exported through the app's read_thread tool, without
reasoning; prepared driver strings and child reports cannot replace observations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from novel_creator import host_input, storage
from novel_creator.install import bundle_files


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_observation(snapshot, exchange, *, expected, thread_id, parent, commentary_review=None):
    verify_input(snapshot, exchange, expected=expected, thread_id=thread_id, parent=parent)
    return verify_display(snapshot['turns'][0], exchange, commentary_review=commentary_review)


def verify_input(snapshot, exchange, *, expected, thread_id, parent):
    """Verify the creative source independently of display or completion status.

    An app continuation can finish in another turn while the original public
    source turn retains inProgress status. This function proves only source
    identity; verify_display still requires an actual completed display turn.
    """
    require(len(snapshot.get('turns', [])) == 1, 'Expected exactly one public turn')
    turn = snapshot['turns'][0]
    items = turn['items']
    require(not any(i['type'] == 'reasoning' for i in items), 'Do not archive reasoning')
    observed = host_input.capture(snapshot, thread_id=thread_id, turn_id=turn['id'],
        source='delegated', source_thread_id=parent, evaluation_only=True)
    require(observed['text'] == expected, 'Public delegated input differs from driver')
    messages = exchange['messages']
    require(len(messages) == 2 and messages[0]['role'] == 'user' and messages[1]['role'] == 'assistant'
            and messages[0]['text'] == expected, 'Conversation roles, count or exact input differ')
    artifacts = exchange['input_artifacts']
    require(len(artifacts) == 1 and artifacts[0]['parsed_value'] == observed['input_artifact']['parsed_value'],
            'Committed source provenance differs from public input')


def verify_display(turn, exchange, *, commentary_review=None):
    """Check an actual display turn, including a separate administrative recovery turn.

    This does not verify creative input provenance; callers must verify that
    independently against the original public turn, never the recovery request.
    """
    require(turn.get('status') == 'completed', 'Public display turn has not completed')
    items = turn['items']
    require(not any(i['type'] == 'reasoning' for i in items), 'Do not archive reasoning')
    messages = exchange['messages']
    finals = [(n, i) for n, i in enumerate(items)
              if i['type'] == 'agentMessage' and i.get('phase') == 'final_answer']
    require(len(finals) == 1, 'Expected exactly one displayed final response')
    require(finals[0][1]['text'] == exchange['messages'][1]['text'], 'Saved/displayed response differs')
    saves = []
    for n, item in enumerate(items[:finals[0][0]]):
        if (item['type'] != 'commandExecution' or item.get('status') != 'completed'
                or item.get('exitCode') != 0 or item.get('output', {}).get('truncated', False)):
            continue
        for line in item.get('output', {}).get('text', '').splitlines():
            try:
                value = json.loads(line)
            except ValueError:
                continue
            if not isinstance(value, dict):
                continue
            point = value.get('checkpoint', {})
            if (value.get('ok') is True and value.get('data', {}).get('saved') is True
                    and point.get('exchange_id') == exchange['exchange_id']
                    and point.get('sequence') == exchange['sequence'] and point.get('git_head')):
                saves.append((n, point))
    require(bool(saves), 'No observed successful matching save before display')
    require(all(p == saves[0][1] for _, p in saves), 'Conflicting observed save checkpoints')
    if commentary_review is not None:
        comments = [(n, i) for n, i in enumerate(items)
                    if i['type'] == 'agentMessage' and i.get('phase') == 'commentary']
        reviewed = {r['id']: r for r in commentary_review}
        require(len(reviewed) == len(commentary_review)
                and set(reviewed) == {i['id'] for _, i in comments}, 'Commentary review is incomplete')
        for n, item in comments:
            assessment = reviewed[item['id']]
            require(assessment['text'] == item['text'], 'Reviewed commentary differs from public text')
            require(assessment.get('classification') in ('administrative', 'story', 'failure_disclosure')
                    and bool(assessment.get('reason')), 'Commentary needs an explicit scoped agent judgment')
            if assessment['classification'] == 'story':
                require(n > saves[0][0], 'Story commentary precedes its confirmed save')
                require(item['text'] in messages[1]['text'], 'Story commentary contains unsaved response text')
    return saves[0][1]


def verify_run(folder, case_ids=None, languages=None):
    run = json.loads((folder / 'run.json').read_bytes())
    results = []
    failures = []
    for driver in sorted(folder.glob('*-driver.json')):
        case = json.loads(driver.read_bytes())
        if not case.get('submitted', False):
            continue
        if case_ids and case['case_id'] not in case_ids:
            continue
        for language, expected in case['inputs'].items():
            if languages and language not in languages:
                continue
            if case.get('transport_transform') == 'administrative_case_placeholder_html_escape':
                require(case['case_id'] == 'GATE', 'Transport exception is restricted to administrative gate')
                expected = expected.replace('<case>', '&lt;case&gt;')
            raw_path = folder / f"{case['case_id']}-{language}-public.json"
            require(raw_path.is_file(), f'Missing submitted observation: {raw_path.name}')
            snapshot = json.loads(raw_path.read_bytes())
            task = dict(run['tasks'][language])
            task.update(case.get('task_overrides', {}).get(language, {}))
            novel = Path(task['novel_path'])
            # A sandbox-denied Git read must fail explicitly, not look like an empty novel.
            storage.git(novel, 'rev-parse', '--verify', 'HEAD')
            history = storage.read_history(novel)
            turn_id = snapshot['turns'][0]['id']
            matches = [e for e in history if e['operation'] == 'conversation' and e['input_artifacts']
                and e['input_artifacts'][0]['parsed_value'].get('thread_id') == task['thread_id']
                and e['input_artifacts'][0]['parsed_value'].get('turn_id') == turn_id]
            if len(matches) != 1:
                failures.append({'case_id': case['case_id'], 'language': language,
                    'thread_id': task['thread_id'], 'turn_id': turn_id,
                    'error': 'Expected exactly one committed exchange for public turn',
                    'matched_exchanges': len(matches)})
                continue
            exchange = matches[0]
            review_path = folder / f"{case['case_id']}-{language}-commentary-review.json"
            review = json.loads(review_path.read_bytes()) if review_path.exists() else None
            require(not case.get('require_commentary_review') or review is not None,
                    'Submitted case requires separate commentary review')
            try:
                point = verify_observation(snapshot, exchange, expected=expected,
                    thread_id=task['thread_id'], parent=run['authorization']['parent_thread_id'],
                    commentary_review=review)
            except ValueError as error:
                archives = folder / 'failed-exchanges'
                archives.mkdir(exist_ok=True)
                (archives / f"{case['case_id']}-{language}.json").write_text(
                    json.dumps(exchange, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                failures.append({'case_id': case['case_id'], 'language': language,
                    'thread_id': task['thread_id'], 'turn_id': turn_id,
                    'exchange_id': exchange['exchange_id'], 'error': str(error)})
                continue
            blob = storage.git(novel, 'show', point['git_head'] + ':' + storage.bundle_path(exchange))
            require(json.loads(blob) == exchange, 'Published checkpoint differs from current committed history')
            manifest_path = novel / '.novel-creator/manifest.json'
            manifest = json.loads(manifest_path.read_bytes())
            for relative, digest in manifest['checksums'].items():
                require(hashlib.sha256((novel / relative).read_bytes()).hexdigest() == digest,
                        f'Installed manifest mismatch: {relative}')
            current_source = {name: hashlib.sha256(raw).hexdigest() for name, raw in bundle_files().items()}
            expected_source = run.get('bundle_source_sha256', current_source)
            require(set(expected_source) == set(current_source), 'Pinned source manifest has a different file set')
            for relative, digest in expected_source.items():
                require(hashlib.sha256((novel / relative).read_bytes()).hexdigest() == digest,
                        f'Installed source mismatch: {relative}')
            archives = folder / 'exchanges'
            archives.mkdir(exist_ok=True)
            (archives / f"{case['case_id']}-{language}.json").write_bytes(blob)
            results.append({'case_id': case['case_id'], 'language': language, 'thread_id': task['thread_id'],
                'turn_id': turn_id, 'exchange_id': exchange['exchange_id'], 'checkpoint': point,
                'exact_input_saved': True, 'exact_response_saved_and_displayed': True,
                'save_precedes_display': True, 'source_type': 'delegated', 'native_user_input': False,
                'novice_evidence': False, 'installed_bundle_verified': True,
                'installed_bundle_matches_current_source': expected_source == current_source,
                'commentary_agent_reviewed': review is not None,
                'record_kinds': [r['kind'] for r in exchange['record_versions']],
                'response': exchange['messages'][1]['text']})
    require(bool(results or failures), 'No submitted observations; an empty run cannot pass')
    return {'ok': not failures, 'scope': 'Public delegated persistence/display/source checks only',
            'case_filter': sorted(case_ids) if case_ids else None,
            'language_filter': sorted(languages) if languages else None,
            'all_submitted_cases_checked': not bool(case_ids or languages),
            'semantic_assessment': 'Separate agent judgments required; no human/native result inferred',
            'cases': results, 'failures': failures}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True, type=Path)
    parser.add_argument('--case', action='append', help='Check only named cases; never a complete-run result')
    parser.add_argument('--language', action='append', choices=('en', 'is'), help='Scope a report to named languages')
    args = parser.parse_args()
    output = verify_run(args.run.resolve(), set(args.case) if args.case else None,
                        set(args.language) if args.language else None)
    report_name = 'observation-verification.json' if not args.case else 'observation-verification-' + '-'.join(args.case) + '.json'
    if args.language:
        report_name = report_name.removesuffix('.json') + '-' + '-'.join(args.language) + '.json'
    (args.run / report_name).write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ok': output['ok'], 'verified_observations': len(output['cases']), 'failures': output['failures']}))
    sys.exit(0 if output['ok'] else 1)
