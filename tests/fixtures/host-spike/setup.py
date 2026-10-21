"""Build an independent disposable spike bundle, never a real novel installation."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import uuid

FRAMEWORK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(FRAMEWORK / 'src'))
from novel_creator import records, storage


def setup(target):
    if target.exists() or target.is_symlink() or target.resolve() != target:
        raise ValueError('Fixture requires a new nonsymlink directory')
    # The fixture is independent; never nest in a repository.
    for parent in target.parents:
        if parent.exists() and storage.git(parent, 'rev-parse', '--show-toplevel', check=False).returncode == 0:
            raise ValueError('Fixture must be outside any existing repository')
    target.mkdir(parents=True)
    storage.git(target, 'init', '-b', 'main')
    storage.git(target, 'config', 'user.name', 'Disposable Host Spike')
    storage.git(target, 'config', 'user.email', 'host-spike@example.invalid')
    managed = target / '.novel-creator'
    (managed / 'local').mkdir(parents=True)
    shutil.copytree(FRAMEWORK / 'src/novel_creator', managed / 'src/novel_creator',
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    shutil.copytree(FRAMEWORK / 'schemas', managed / 'src/novel_creator/schemas',
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ('run.py', 'fixture-context.py', 'fixture-prepare.py'):
        shutil.copyfile(Path(__file__).parent / name, managed / name if name == 'run.py' else managed / 'src' / name)
    shutil.copyfile(FRAMEWORK / 'adapters/codex/AGENTS.fragment.md', target / 'AGENTS.md')
    (target / '.gitignore').write_text('.novel-creator/local/\n__pycache__/\n*.pyc\n', encoding='utf-8')
    novel = str(uuid.uuid4())
    files = [p for p in managed.rglob('*') if p.is_file()]
    manifest = {'novel_id': novel, 'schema_version': '1.0', 'bundle_version': '0.1.0', 'fixture_only': True,
                'checksums': {str(p.relative_to(target)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (managed / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    # Fixture installation metadata is committed separately; production saves own
    # each subsequent exchange. This does not implement story initialization.
    storage.git(target, 'add', '--', '.novel-creator', '.gitignore', 'AGENTS.md')
    storage.git(target, 'commit', '-m', 'Install disposable host-spike fixture')
    bundle = {'schema_version': '1.0', 'novel_id': novel, 'exchange_id': str(uuid.uuid4()), 'sequence': 1,
              'previous_exchange_id': None, 'previous_digest': None, 'session_id': None,
              'expected_git_head': storage.head(target), 'recorded_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
              'operation': 'bootstrap', 'messages': [], 'input_artifacts': [], 'record_versions': [],
              'continuity_review': {'coverage': 'not_applicable', 'reviewed_record_refs': [], 'unavailable_refs': [],
               'canon_hold_refs': [], 'finding_ids': [], 'summary': 'Disposable host fixture bootstrap'}}
    bundle['payload_digest'] = records.digest(bundle)
    return storage.save(target, bundle)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--path', type=Path, required=True)
    args = p.parse_args()
    try:
        print(json.dumps(setup(args.path.absolute()), ensure_ascii=False))
    except (ValueError, OSError) as error:
        p.exit(2, str(error) + '\n')
