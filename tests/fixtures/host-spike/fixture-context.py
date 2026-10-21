"""Fixture-only committed context; no production story-context claim."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from novel_creator import storage
root = Path(__file__).resolve().parents[2]
history = storage.read_history(root)
print(json.dumps({'fixture_only': True, 'checkpoint': storage.checkpoint(root, history),
                  'saved_messages': history[-1]['messages'] if history else [],
                  'display_confirmed': False}, ensure_ascii=False))
