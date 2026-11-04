"""Small fixture-only format-1 checker; deliberately not a runtime validator."""
import json
import re
from pathlib import Path

SLUG = re.compile(r"[a-z][a-z0-9-]*\Z")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
PAIR = re.compile(r"([a-z][a-z0-9-]*)#([a-z][a-z0-9-]*)\s+\[[^\]]+\]\(([^)]+)\)")


def validate_notebook(root):
    """Raise ValueError on an invalid fixture; return documents on success."""
    root = Path(root).resolve()
    documents, topics = {}, {}

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    for path in sorted(root.rglob('*.md')):
        text = path.read_text(encoding='utf-8')
        envelope = re.match(r'\A(```|~~~)json\n(.*?)\n\1\n', text, re.S)
        require(envelope, f'{path.name}: missing metadata')
        try:
            meta = json.loads(envelope[2])
        except (ValueError, TypeError) as exc:
            raise ValueError(f'{path.name}: invalid metadata') from exc
        require(isinstance(meta, dict), 'metadata must be an object')
        require(meta.get('format') == 'novel-notebook' and type(meta.get('version')) is int
                and meta['version'] == 1, 'unsupported format/version')
        require(meta.get('kind') in {'project', 'summary', 'topic'}, 'invalid kind')
        require(isinstance(meta.get('id'), str) and SLUG.fullmatch(meta['id']), 'invalid id')
        require(re.search(r'^# .+\S', text[envelope.end():], re.M), 'missing title')
        if meta['kind'] == 'project':
            require(meta.get('language') in {'en', 'is'}, 'invalid language')
        items = {}
        if meta['kind'] == 'topic':
            require(isinstance(meta.get('category'), str) and meta['category'].strip(), 'missing category')
            require(meta['id'] not in topics, 'duplicate topic id')
            topics[meta['id']] = path
            current = text.split('\n## Revisions', 1)[0]
            for block in re.split(r'^### .+\n', current, flags=re.M)[1:]:
                fields = {}
                for name in ('Item-ID', 'Type', 'State', 'Perspective', 'Origin', 'Links'):
                    values = re.findall(rf'^{name}: (.+)$', block, re.M)
                    require(len(values) == 1 and values[0].strip(), f'missing/duplicate {name}')
                    fields[name] = values[0].strip()
                item_id = fields['Item-ID']
                require(SLUG.fullmatch(item_id), 'invalid item id')
                require(item_id not in items, 'duplicate item id')
                states = {'statement': {'proposed', 'accepted', 'rejected'}, 'question': {'open', 'resolved'}}
                require(fields['Type'] in states, 'invalid type')
                require(fields['State'] in states[fields['Type']], 'invalid state')
                require(re.fullmatch(r'objective|reader|unknown|character:[a-z][a-z0-9-]*', fields['Perspective']), 'invalid perspective')
                prose = re.sub(r'^(Item-ID|Type|State|Perspective|Origin|Links):.*$', '', block, flags=re.M).strip()
                require(prose, 'missing item prose')
                items[item_id] = fields
            require(items, 'empty topic')
        documents[path] = (meta, items, text)
    require(any(m['kind'] == 'project' for m, _, _ in documents.values()), 'missing project')
    require(any(m['kind'] == 'summary' for m, _, _ in documents.values()), 'missing summary')

    def target(source, value):
        require('#' not in value and '?' not in value and ':' not in value
                and not Path(value).is_absolute(), 'link must be a relative fragment-free file')
        resolved = (source.parent / value).resolve()
        require(resolved.is_relative_to(root), 'link escapes notebook')
        require(resolved in documents, 'broken file link')
        return resolved

    for path, (_, items, text) in documents.items():
        for _, value in LINK.findall(text):
            target(path, value)
        for fields in items.values():
            perspective = fields['Perspective']
            if perspective.startswith('character:'):
                require(perspective.split(':', 1)[1] in topics, 'unknown character perspective')
            links = fields['Links']
            if links == 'none':
                continue
            pairs = PAIR.findall(links)
            require(pairs and not PAIR.sub('', links).strip(' ;'), 'unpaired semantic reference')
            for topic_id, item_id, value in pairs:
                destination = target(path, value)
                meta, target_items, _ = documents[destination]
                require(meta['kind'] == 'topic' and meta['id'] == topic_id
                        and item_id in target_items, 'incorrect semantic target')
    return documents
