"""Generate checked-in marketplace metadata and dependency-free plugin archives."""
import argparse
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/novel-creator'
SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'


def generated_files():
    match = re.search(r'^__version__ = "([^"]+)"$', (ROOT / 'src/novel_creator/__init__.py').read_text(encoding='utf-8'), re.M)
    if not match:
        raise ValueError('Package version could not be read without importing the package')
    version = match[1]
    description = 'Independent story notebooks with shared writing workflows for Codex and Claude Code.'
    shared = {'name': 'novel-creator', 'version': version, 'description': description,
              'author': {'name': 'bjarkig82'}, 'repository': 'https://github.com/bjarkig82/novel-creator'}
    portable = {'$schema': SCHEMA, **shared, 'extensions': {'com.openai': {
        'onboardingSkill': './skills/setup/SKILL.md', 'interface': {
            'displayName': 'Novel Creator', 'shortDescription': 'Create and write independent story notebooks.',
            'developerName': 'bjarkig82', 'category': 'Productivity'}}}}
    codex = {'name': 'novel-creator-marketplace', 'interface': {'displayName': 'Novel Creator'},
             'plugins': [{'name': 'novel-creator', 'source': {'source': 'local', 'path': './plugins/novel-creator'},
                          'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'}]}
    claude = {'name': 'novel-creator-marketplace', 'description': description, 'owner': {'name': 'bjarkig82'},
              'plugins': [{'name': 'novel-creator', 'source': './plugins/novel-creator',
                           'description': description, 'version': version}]}
    documents = {'plugins/novel-creator/plugin.json': portable,
                 'plugins/novel-creator/.claude-plugin/plugin.json': shared,
                 '.agents/plugins/marketplace.json': codex,
                 '.claude-plugin/marketplace.json': claude}
    return version, {name: json.dumps(value, ensure_ascii=False, indent=2) + '\n' for name, value in documents.items()}


def plugin_files():
    # Explicit product trees prevent caches, credentials, editor state, and
    # arbitrary local files from entering a distributable archive.
    paths = [PLUGIN / 'plugin.json', PLUGIN / '.claude-plugin/plugin.json', PLUGIN / 'README.md']
    paths.extend((PLUGIN / 'skills').glob('*/SKILL.md'))
    paths.extend((PLUGIN / 'references').glob('*.md'))
    paths.append(PLUGIN / 'scripts/bootstrap.py')
    for path in sorted(paths):
        if not path.is_file() or path.is_symlink() or any(p.is_symlink() for p in path.parents):
            raise ValueError('Missing or redirected plugin product file: ' + str(path))
        yield path


def archive(path, files):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for source, name in files:
            info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated metadata for drift without writes or archives')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist', help='Directory for plugin and marketplace zip files')
    args = parser.parse_args(argv)
    version, documents = generated_files()
    if args.check:
        drift = [name for name, text in documents.items() if not (ROOT / name).is_file() or (ROOT / name).read_text(encoding='utf-8') != text]
        if drift:
            print('Generated plugin metadata drift: ' + ', '.join(drift), file=sys.stderr)
            return 1
        print('Plugin metadata matches package version ' + version)
        return 0
    for name, text in documents.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    paths = list(plugin_files())
    args.output.mkdir(parents=True, exist_ok=True)
    archive(args.output / ('novel-creator-plugin-' + version + '.zip'),
            [(path, path.relative_to(PLUGIN).as_posix()) for path in paths])
    marketplace = [(path, path.relative_to(ROOT).as_posix()) for path in paths]
    marketplace += [(ROOT / name, name) for name in documents if name.startswith('.')]
    archive(args.output / ('novel-creator-marketplace-' + version + '.zip'), marketplace)
    print('Built plugin and marketplace archives for ' + version + ' in ' + str(args.output))
    return 0


if __name__ == '__main__':
    sys.exit(main())
