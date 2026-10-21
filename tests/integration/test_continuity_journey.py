import unittest
from novel_creator import storage
from novel_creator.cli import ToolError
from novel_creator.context import read
from tests.helpers import envelope, idea, repository, seal, git, held_conflict_transition, record


class ContinuityJourney(unittest.TestCase):
    def test_metadata_bypasses_preserve_checkpoint_and_user_work_then_explicit_resolution_saves(self):
        with repository() as root:
            first, acceptance, finding = held_conflict_transition(root)
            storage.save(root, first)
            checkpoint = storage.head(root)
            acceptance['expected_git_head'] = checkpoint
            (root / 'manuscript.md').write_bytes(b'Approved text, unchanged.\n')
            (root / 'notes.txt').write_bytes(b'User staged work.\n')
            git(root, 'add', '--', 'notes.txt')
            index = (root / '.git/index').read_bytes()
            for field, value in [('severity', 'advisory'), ('assessment', 'uncertainty'),
                                 ('affected_refs', [{'id': finding['id']}])]:
                for promote in (False, True):
                    with self.subTest(field=field, promote=promote):
                        exchange = seal(acceptance)
                        changed = dict(finding, revision=2, previous_revision=1, **{field: value})
                        exchange['record_versions'] = ([*exchange['record_versions'], changed]
                                                       if promote else [changed])
                        with self.assertRaises(ToolError) as error:
                            storage.save(root, seal(exchange))
                        self.assertEqual(error.exception.code, 2)
                        self.assertEqual(storage.head(root), checkpoint)
                        self.assertEqual(storage.read_history(root), [first])
                        self.assertEqual((root / '.git/index').read_bytes(), index)
                        self.assertEqual((root / 'manuscript.md').read_bytes(), b'Approved text, unchanged.\n')
            resolution = envelope(root, previous=first)
            source = {'type': 'message', 'exchange_id': resolution['exchange_id'],
                      'message_id': resolution['messages'][0]['message_id']}
            resolution['messages'][0]['text'] = 'This is intentional unreliable narration.'
            decision = record(resolution, 'decision', action='resolve', user_message_ref=source,
                span={'start': 0, 'end': 40}, target_refs=[{'id': finding['id'], 'revision': 2}],
                selected_parts=[], prior_refs=[{'id': finding['id'], 'revision': 1}], result_refs=[],
                reason='Intentional technique', affected_refs=[], review_required_refs=[])
            changed = dict(finding, revision=2, previous_revision=1, disposition='intentional',
                narrative_explanation='Unreliable narration', decision_ids=[decision['id']])
            resolution = seal(dict(resolution, record_versions=[changed, decision]))
            saved = storage.save(root, resolution)
            self.assertTrue(saved['data']['saved'])
            retried = storage.save(root, resolution)
            self.assertTrue(retried['data']['already_saved'])
            self.assertEqual(storage.head(root), saved['checkpoint']['git_head'])
            self.assertEqual(len(storage.read_history(root)), 2)

    def test_damaged_journal_blocks_append_and_exact_restoration_allows_revalidation(self):
        with repository() as root:
            bootstrap = envelope(root)
            storage.save(root, bootstrap)
            first = envelope(root, previous=bootstrap)
            first['record_versions'] = [idea(first)]
            first = seal(first)
            storage.save(root, first)
            path = root / storage.bundle_path(first)
            original = path.read_bytes()
            path.write_bytes(b'{damaged')
            git(root, 'add', '--', path.relative_to(root).as_posix())
            git(root, 'commit', '-m', 'Harness: damaged journal')
            failed_head = storage.head(root)
            next_turn = envelope(root, previous=first)
            with self.assertRaises(ToolError) as error:
                storage.save(root, next_turn)
            self.assertEqual(error.exception.code, 4)
            self.assertEqual(storage.head(root), failed_head)
            with self.assertRaises(ToolError):
                read(root)
            path.write_bytes(original)
            git(root, 'add', '--', path.relative_to(root).as_posix())
            git(root, 'commit', '-m', 'Harness: restore known original bytes')
            context = read(root)
            self.assertEqual(context['checkpoint']['sequence'], 2)
            next_turn = envelope(root, previous=first)
            next_turn['continuity_review'].update(coverage='incomplete', canon_hold_refs=['*'])
            next_turn['record_versions'] = [idea(next_turn)]
            storage.save(root, seal(next_turn))
            self.assertEqual(read(root)['data']['coverage'], 'incomplete')
