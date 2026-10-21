import hashlib
import unittest
from novel_creator import records, storage
from novel_creator.context import read
from tests.helpers import envelope, idea, record, repository, seal, uid


class CanonJourney(unittest.TestCase):
    def test_five_revisions_retain_sources_history_direct_impact_and_manuscript(self):
        with repository() as root:
            manuscript = root / 'chapter.md'
            manuscript.write_bytes('Approved: Þóra waits.\n'.encode())
            digest = hashlib.sha256(manuscript.read_bytes()).hexdigest()
            bootstrap = envelope(root)
            storage.save(root, bootstrap)
            previous = bootstrap
            current = None
            for index in range(6):
                exchange = envelope(root, previous=previous)
                text = ('Accept' if index == 0 else 'Revise') + f' the sender proposition to version {index}.'
                exchange['messages'][0]['text'] = text
                source = records.current_user_source(exchange)
                if current is None:
                    updated = idea(exchange)
                else:
                    updated = dict(current, revision=current['revision'] + 1, previous_revision=current['revision'])
                updated.update(statement=f'Sender version {index}', status='accepted', source_refs=[source], origin='supplied')
                decision = record(exchange, 'decision', action='accept' if index == 0 else 'revise',
                    source_refs=[source], origin='supplied', user_message_ref=source, span={'start': 0, 'end': len(text)},
                    target_refs=[{'id': updated['id'], 'revision': updated['revision']}], selected_parts=[],
                    prior_refs=[{'id': current['id'], 'revision': current['revision']}] if current else [],
                    result_refs=[{'id': updated['id'], 'revision': updated['revision']}], reason=text,
                    affected_refs=[], review_required_refs=[])
                updated['decision_ids'] = [decision['id']]
                versions = [updated, decision]
                if index == 0:
                    dependency = record(exchange, 'story_element', element_type='event', display_name='Arrival', aliases=[],
                        status='proposed', assertion_ids=[], relationship_ids=[], dependency_refs=[{'id': updated['id']}],
                        time_ref=None, decision_ids=[], origin='supplied', source_refs=[source])
                    versions.append(dependency)
                else:
                    decision['affected_refs'] = [{'id': dependency['id']}]
                    decision['review_required_refs'] = [{'id': dependency['id']}]
                exchange['record_versions'] = versions
                exchange = seal(exchange)
                storage.save(root, exchange)
                current, previous = updated, exchange
            inspection = read(root, operation='inspect', identifier=current['id'])
            self.assertEqual(len(inspection['data']['history']), 6)
            self.assertEqual(inspection['data']['records'][0]['statement'], 'Sender version 5')
            self.assertEqual([r['id'] for r in inspection['data']['directly_affected'] if r['kind'] == 'story_element'], [dependency['id']])
            self.assertTrue(all(r['source_refs'] for r in inspection['data']['history']))
            self.assertEqual(hashlib.sha256(manuscript.read_bytes()).hexdigest(), digest)
            checkpoint = storage.head(root)
            retry = storage.save(root, previous)
            self.assertTrue(retry['data']['already_saved'])
            self.assertEqual(storage.head(root), checkpoint)
