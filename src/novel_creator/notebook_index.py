"""On-demand comparison of existing Markdown count tables with owning topic items."""
import re
from pathlib import Path, PureWindowsPath

from .notebook import split_document


STATES = ('accepted', 'proposed', 'rejected', 'open', 'resolved')
ALIASES = {
    'topic': ('topic', 'efni', 'viðfangsefni'),
    'accepted': ('accepted', 'accepted statements', 'samþykkt', 'samþykktar fullyrðingar'),
    'proposed': ('proposed', 'proposed statements', 'tillögur', 'lagðar til'),
    'rejected': ('rejected', 'rejected statements', 'hafnað', 'hafnaðar fullyrðingar'),
    'open': ('open', 'open questions', 'opnar', 'opnar spurningar'),
    'resolved': ('resolved', 'resolved questions', 'leystar', 'leystar spurningar'),
}
NAVIGATION = {'focus', 'recent focus', 'notes', 'category', 'áhersla', 'athugasemdir', 'flokkur'}
COLUMNS = {label: key for key, names in ALIASES.items() for label in names}
STATE_LABEL = '(?:' + '|'.join(re.escape(label) for label, key in COLUMNS.items() if key in STATES) + ')'
INLINE_COUNT = re.compile(r'\b(?:' + STATE_LABEL + r'\s*[:=]?\s*[0-9]+|[0-9]+\s+' + STATE_LABEL + r')\b', re.I)
HISTORY = {'revisions', 'revision history', 'historical revisions', 'endurskoðanir',
           'endurskoðun', 'breytingasaga', 'saga breytinga'}
SLUG = re.compile(r'[a-z][a-z0-9-]*')
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def _document(root, relative, kind):
    path = root / relative
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ValueError(f'{relative}: missing or outside the notebook')
    meta, body = split_document(path.read_text(encoding='utf-8'))
    if (not isinstance(meta, dict) or meta.get('format') != 'novel-notebook'
            or type(meta.get('version')) is not int or meta['version'] != 1
            or meta.get('kind') != kind or not isinstance(meta.get('id'), str)
            or not SLUG.fullmatch(meta['id'])):
        raise ValueError(f'{relative}: unsupported {kind} metadata')
    if kind == 'project' and meta.get('language') not in ('en', 'is'):
        raise ValueError(f'{relative}: unsupported language')
    if kind == 'topic' and not (isinstance(meta.get('category'), str) and meta['category'].strip()):
        raise ValueError(f'{relative}: missing topic category')
    return meta['id'], body


def _lines(body):
    """Ignore fenced examples while retaining source order and section boundaries."""
    fence = ''
    for line in body.splitlines():
        if fence:
            if re.fullmatch(r' {0,3}' + fence[0] + '{' + str(len(fence)) + r',}\s*', line):
                fence = ''
        else:
            match = re.match(r' {0,3}(`{3,}|~{3,})', line)
            if match:
                fence = match[1]
                yield ''
            else:
                yield line
    if fence:
        raise ValueError('unterminated Markdown fence')


def _topic_counts(body):
    counts = dict.fromkeys(STATES, 0)
    ids = set()
    fields = {}

    def finish():
        if not fields:
            return
        missing = {'Item-ID', 'Type', 'State', 'Origin', 'Perspective', 'Links'} - fields.keys()
        if missing:
            raise ValueError('missing current field(s): ' + ', '.join(sorted(missing)))
        identifier = fields.get('Item-ID', '')
        kind, state = fields.get('Type'), fields.get('State')
        if not SLUG.fullmatch(identifier) or identifier in ids:
            raise ValueError('missing, invalid or duplicate current Item-ID')
        allowed = {'statement': STATES[:3], 'question': STATES[3:]}
        if state not in allowed.get(kind, ()):
            raise ValueError(f'{identifier}: missing or invalid current Type/State')
        ids.add(identifier)
        counts[state] += 1
        fields.clear()

    history_depth = 0
    lines = list(_lines(body))
    for i, line in enumerate(lines):
        # Normalize plain setext titles. A rule following fields or an ATX
        # heading cannot turn those format markers into a different title.
        if (line.strip() and i + 1 < len(lines)
                and not re.match(r'^(?: {4}|\t| {0,3}[#>]|(?:Item-ID|Type|State|Perspective|Origin|Links):)', line)):
            underline = re.fullmatch(r' {0,3}(=+|-+)[ \t]*', lines[i + 1])
            if underline:
                line = ('# ' if underline[1][0] == '=' else '## ') + line.strip()
                lines[i + 1] = ''
        heading = re.fullmatch(r' {0,3}(#{1,6})\s+(.+?)\s*', line)
        if heading:
            finish()
            depth = len(heading[1])
            if history_depth and depth <= history_depth:
                history_depth = 0
            if not history_depth and heading[2].rstrip('#').strip().casefold() in HISTORY:
                history_depth = depth
            continue
        field = re.fullmatch(r'(Item-ID|Type|State|Perspective|Origin|Links):\s*(.*?)\s*', line)
        if history_depth or not field:
            continue
        name, value = field.groups()
        if name == 'Item-ID' and name in fields:
            finish()
        if name in fields:
            raise ValueError(f'duplicate current {name}')
        if not value:
            raise ValueError(f'empty current {name}')
        fields[name] = value
    finish()
    if not ids:
        raise ValueError('no identifiable current items')
    return counts


def _compare(root, header, row):
    if len(row) != len(header):
        raise ValueError('row width differs from its header')
    cells = dict(zip(header, row))
    for label, value in cells.items():
        if (label not in ('topic', *STATES) and label not in NAVIGATION
                and re.fullmatch(r'[-+]?[0-9]+(?:[.,][0-9]+)?', value)):
            raise ValueError(f'unrecognized numeric column: {label}')
    topic = cells['topic']
    links = LINK.findall(topic)
    if len(links) != 1:
        raise ValueError('expected one relative link in the topic cell')
    relative = links[0][1]
    path = Path(relative)
    if (PureWindowsPath(relative).drive or any(c in relative for c in ('\\', ':', '?', '#'))
            or path.is_absolute() or '..' in path.parts or path.parts[:1] != ('topics',)
            or path.suffix.lower() != '.md' or not (root / path).resolve().is_relative_to(root / 'topics')):
        raise ValueError('expected a Markdown file under notebook/topics/')
    topic_id, body = _document(root, relative, 'topic')
    prefix = topic[:LINK.search(topic).start()].strip().strip('`')
    if prefix and prefix != topic_id:
        raise ValueError(f'topic cell and owning ID disagree ({topic_id})')
    displayed = {}
    for state in STATES:
        if state in cells:
            if not re.fullmatch(r'[0-9]+', cells[state]):
                raise ValueError(f'invalid {state} count')
            displayed[state] = int(cells[state])
    correct = _topic_counts(body)
    if any(correct[state] != value for state, value in displayed.items()):
        return dict(topic=topic_id, path=relative, displayed=displayed, correct=correct)


def _cells(line):
    text = line.strip()
    cells = []
    start = 0
    for token in re.finditer(r'\\.|(\|)', text):
        if token[1]:
            if token.start() != 0:
                cells.append(text[start:token.start()].strip())
            start = token.end()
    if start < len(text):
        cells.append(text[start:].strip())
    return cells


def _table(root, lines, data):
    rows = [_cells(line) for line in lines]
    labels = [cell.casefold() for cell in rows[0]]
    header = [COLUMNS.get(label, label) for label in labels]
    if not any(state in header for state in STATES):
        # A navigation table without counts has nothing to compare. Unknown
        # numeric columns on a topic row need inspection rather than a clean bill.
        numeric_topics = any('topics/' in line and re.search(r'(?:^|\|)\s*[0-9]+\s*(?:\||$)', line)
                             for line in lines[2:])
        if not numeric_topics:
            return
    if ('topic' not in header or '' in header or len(set(header)) != len(header)
            or not any(state in header for state in STATES) or len(rows) < 2
            or len(rows[1]) != len(header) or not all(re.fullmatch(r':?-+:?', c) for c in rows[1])):
        data['unavailable'].append('Unrecognized topic count table: ' + lines[0])
        return
    for row in rows[2:]:
        try:
            mismatch = _compare(root, header, row)
        except (ValueError, OSError, RuntimeError) as exc:
            topic_column = header.index('topic')
            label = row[topic_column] if topic_column < len(row) else 'Incomplete row'
            data['unavailable'].append(f'{label}: {exc}')
        else:
            data['checked_rows'] += 1
            if mismatch:
                data['mismatches'].append(mismatch)


def check_index(target):
    data = dict(checked_rows=0, mismatches=[], unavailable=[])
    try:
        root = Path(target).resolve() / 'notebook'
        _document(root, 'project.md', 'project')
        _, summary = _document(root, 'working-summary.md', 'summary')
        table = []
        for line in _lines(summary):
            if '|' in line:
                table.append(line)
            else:
                if table:
                    _table(root, table, data)
                    table = []
                if 'topics/' in line and INLINE_COUNT.search(LINK.sub('', line)):
                    data['unavailable'].append('Possible count outside a supported topic table: ' + line)
        if table:
            _table(root, table, data)
    except (ValueError, OSError, RuntimeError) as exc:
        data['unavailable'].append(str(exc))
    return dict(ok=not (data['mismatches'] or data['unavailable']), data=data)


def describe(data):
    def counts(values):
        return ', '.join(f'{key}={value}' for key, value in values.items())
    lines = [f'Checked {data["checked_rows"]} topic-index count row(s).' if data['checked_rows']
             else 'No topic-index count rows were checked.']
    for row in data['mismatches']:
        lines.append(f'{row["topic"]} ({row["path"]}): displayed {counts(row["displayed"])}; correct {counts(row["correct"])}')
    lines.extend('Could not check: ' + message for message in data['unavailable'])
    return '\n'.join(lines)
