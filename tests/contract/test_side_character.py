"""Delivery contracts plus existing journal persistence, not host/quality proof."""
from pathlib import Path, PurePosixPath
import re
import unittest

from novel_creator import storage
from novel_creator.context import read
from tests.helpers import envelope, record, repository, seal


ROOT = Path(__file__).resolve().parents[2]


class SideCharacterResources(unittest.TestCase):
    def text(self, path):
        self.assertTrue((ROOT / path).is_file(), f'Missing feature resource: {path}')
        return (ROOT / path).read_text(encoding='utf-8')

    def test_new_entries_resolve_to_their_format_specific_workflows(self):
        # Removing a shipped entry or pointing a notebook at legacy capture is a bug.
        for source, workflow, installed in (
            ('adapters/codex/skills/novel-side-character/SKILL.md',
             'workflows/side-character.md', '.novel-creator/workflows/side-character.md'),
            ('adapters/codex/notebook/skills/novel-side-character/SKILL.md',
             'notebook/workflows/side-character.md', '.novel-notebook/workflows/side-character.md'),
        ):
            with self.subTest(source=source):
                entry = self.text(source)
                self.assertIn('name: novel-side-character', entry)
                self.assertIn(installed, entry)
                self.assertTrue(self.text(workflow).startswith('# Side-character profiles'))
        cached = self.text('plugins/novel-creator/skills/novel-side-character/SKILL.md')
        for contract in ('../../references/notebook.md', 'novel_path',
                         '<novel_path>/.novel-notebook/workflows/side-character.md',
                         'plugin cache is never a book', 'preserve files'):
            self.assertIn(contract, cached)

    def test_new_workflow_links_resolve_in_each_installed_layout(self):
        for directory, prefix in (('workflows', '.novel-creator/workflows'),
                                  ('notebook/workflows', '.novel-notebook/workflows')):
            text = self.text(f'{directory}/side-character.md')
            for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
                with self.subTest(directory=directory, link=link):
                    self.assertTrue((ROOT / directory / link).is_file())
                    self.assertEqual(PurePosixPath(prefix, link).parent.as_posix(), prefix)

    def test_root_routing_is_separately_bounded_and_help_discovers_older_books(self):
        root = self.text('adapters/codex/notebook/AGENTS.md')
        section = re.search(r'<!-- novel-creator:side-character:start -->\n'
                            r'(.*?)<!-- novel-creator:side-character:end -->', root, re.S)
        self.assertIsNotNone(section)
        for contract in ('## Side-character profiles', 'side-character.md',
                         'before generic', 'chat-only', 'save this profile',
                         'older Help catalog', 'actually installed'):
            self.assertIn(contract, section[1])
        character = re.search(r'^## Character development\n.*?(?=^## |\Z)', root, re.M | re.S)[0]
        self.assertNotIn('## Side-character profiles', character)
        self.assertIn('| `$novel-side-character` |', self.text('notebook/workflows/help.md'))
        for path in ('adapters/codex/AGENTS.production.md', 'workflows/entry.md',
                     'workflows/brainstorm.md', 'workflows/help.md',
                     'notebook/workflows/brainstorming.md'):
            self.assertIn('side-character.md', self.text(path), path)

    def test_format_specific_save_boundaries_are_explicit(self):
        notebook = self.text('notebook/workflows/side-character.md')
        for contract in ('ONE AT A TIME', '400–700', 'save this profile',
                         'no notebook file writes', 'every role', 'no guaranteed recovery',
                         'unrelated staging', 'partial', 'Item-ID', 'project language'):
            self.assertIn(contract, notebook)
        legacy = self.text('workflows/side-character.md')
        for contract in ('ONE AT A TIME', '400–700', 'save this profile',
                         'save-before-display', 'exact current input', 'current-user decision',
                         'proposed', 'story_element', 'assertion', 'relationship',
                         'no separate authoritative profile', 'project language'):
            self.assertIn(contract, legacy)
        self.assertNotIn('no notebook file writes', legacy)


class SideCharacterLegacyStorage(unittest.TestCase):
    def test_proposed_profile_acceptance_retains_sources_identity_history_and_retry(self):
        # This tests the existing storage path the new workflow specifies. It
        # does not decide whether an arbitrary human utterance grants authority.
        with repository() as root:
            initial = envelope(root)
            storage.save(root, initial)
            proposal = envelope(root, previous=initial)
            prose = 'Þóra repairs harbour radios. She speaks softly and protects her privacy.'
            proposal['messages'][0]['text'] = 'Create a minor character who repairs radios.'
            proposal['messages'][1]['text'] = prose
            generated_source = {'type': 'message', 'exchange_id': proposal['exchange_id'],
                                'message_id': proposal['messages'][1]['message_id']}
            character = record(proposal, 'story_element', element_type='character',
                display_name='Þóra', aliases=[], status='proposed', assertion_ids=[],
                relationship_ids=[], dependency_refs=[], time_ref=None, decision_ids=[],
                source_refs=[generated_source], origin='interpreted')
            unknown_axis = {'precision': 'unknown', 'event_anchor': None, 'start': None,
                            'end': None, 'before_refs': [], 'after_refs': []}
            profile = record(proposal, 'assertion', subject_element_id=character['id'],
                predicate='profile', value=prose, perspective='author_truth', holder_id=None,
                reader_audience=None, time_ref={'chronology': unknown_axis, 'narrative': unknown_axis},
                truth_state='unknown', status='proposed',
                decision_ids=[], supersedes=None, source_refs=[generated_source], origin='interpreted')
            character['assertion_ids'] = [profile['id']]
            proposal = seal(dict(proposal, record_versions=[character, profile]))
            storage.save(root, proposal)
            self.assertEqual(read(root)['data']['current_canon'], [])

            approval = envelope(root, previous=proposal)
            approval['messages'][0]['text'] = 'Save this profile.'
            approval['messages'][1]['text'] = 'The current profile is accepted and saved.'
            user_source = {'type': 'message', 'exchange_id': approval['exchange_id'],
                           'message_id': approval['messages'][0]['message_id']}
            refs = [{'id': item['id'], 'revision': 2} for item in (character, profile)]
            decision = record(approval, 'decision', action='accept', user_message_ref=user_source,
                span={'start': 0, 'end': len('Save this profile.')}, target_refs=refs,
                selected_parts=[], prior_refs=[{'id': item['id'], 'revision': 1}
                                              for item in (character, profile)],
                result_refs=refs, reason='Explicit save of the current complete profile',
                affected_refs=[], review_required_refs=[], source_refs=[user_source], origin='supplied')
            accepted = [dict(item, revision=2, previous_revision=1, status='accepted',
                             source_refs=[generated_source, user_source], decision_ids=[decision['id']])
                        for item in (character, profile)]
            approval = seal(dict(approval, record_versions=[*accepted, decision]))
            saved = storage.save(root, approval)
            retried = storage.save(root, approval)
            self.assertTrue(retried['data']['already_saved'])
            self.assertEqual(retried['checkpoint'], saved['checkpoint'])
            inspected = read(root, operation='inspect', identifier=profile['id'])['data']
            self.assertEqual(inspected['records'][0]['value'], prose)
            self.assertEqual(inspected['records'][0]['status'], 'accepted')
            self.assertEqual(inspected['history'], [profile, accepted[1]])
            self.assertEqual(inspected['exchanges'][1]['messages'][1]['text'], prose)
            self.assertEqual(len(storage.read_history(root)), 3)
