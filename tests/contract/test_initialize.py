import copy
import hashlib
import json
import unittest

from novel_creator import records, validation
from tests.helpers import envelope, seal


class InitializationContract(unittest.TestCase):
    def bootstrap(self, brief):
        from novel_creator.install import bootstrap
        return bootstrap(json.dumps(brief, ensure_ascii=False), novel_id=None)

    def test_empty_brief_and_explicit_unknowns(self):
        bundle = self.bootstrap({})
        state = validation.validate_exchange(bundle, [])
        project = next(iter(state.values()))
        self.assertEqual(project['id'], bundle['novel_id'])
        self.assertEqual(project['title']['original_text'], 'Untitled novel')
        self.assertEqual(project['original_concept']['state'], 'unknown')
        self.assertEqual(project['manuscript_language'], 'en')
        self.assertEqual(project['review_preferences']['routine_checkpoint'], 'on_request')
        self.assertTrue(all(p['state'] == 'unknown' for p in project['creative_brief'].values()))
        self.assertFalse(bundle['messages'])
        self.assertEqual(len(state), 1)

    def test_supplied_preferences_have_exact_artifact_sources(self):
        brief = {'title': 'Bréf', 'original_concept': 'Þóra fær bréf.\r\n\n',
                 'manuscript_language': 'is', 'creative_brief': {'genre': 'Mystery',
                 'tone': {'state': 'supplied', 'original_text': 'Dökkur',
                          'interpretation': 'Quiet suspense'}},
                 'workflow_preferences': {'suggestions': 'Few'},
                 'review_preferences': {'routine_checkpoint': 'every_exchange'}}
        b = self.bootstrap(brief)
        project = validation.validate_exchange(b, [])[b['novel_id']]
        artifact = b['input_artifacts'][0]
        self.assertEqual(artifact['parsed_value'], brief)
        self.assertEqual(artifact['digest'], hashlib.sha256(artifact['original_text'].encode()).hexdigest())
        self.assertEqual(project['original_concept']['original_text'], brief['original_concept'])
        self.assertEqual(project['creative_brief']['tone']['interpretation'], 'Quiet suspense')
        for pref in [project['title'], project['original_concept'], project['creative_brief']['genre']]:
            self.assertEqual(validation.pointer(brief, pref['source_refs'][0]['pointer']), pref['original_text'])

    def test_invalid_briefs_are_rejected(self):
        from novel_creator.cli import ToolError
        for brief in [[], {'title': 7}, {'secret': 'ignored?'},
                      {'manuscript_language': 'not a language'},
                      {'review_preferences': {'routine_checkpoint': 'never'}},
                      {'creative_brief': {'genre': {'state': 'unknown', 'original_text': 'invented'}}}]:
            with self.subTest(brief=brief), self.assertRaises(ToolError) as error:
                self.bootstrap(brief)
            self.assertEqual(error.exception.code, 2)

    def test_title_revision_keeps_identity_and_original_concept(self):
        b = self.bootstrap({'original_concept': 'A letter from tomorrow.'})
        update = envelope(previous=b)
        from novel_creator.records import revise_project
        revised = revise_project(b['record_versions'][0], {'title': 'Tomorrow'}, update)
        update['record_versions'] = [revised]
        updated = validation.validate_exchange(seal(update), [b])[b['novel_id']]
        self.assertEqual(updated['title']['original_text'], 'Tomorrow')
        self.assertEqual(updated['original_concept'], b['record_versions'][0]['original_concept'])
        self.assertEqual(updated['id'], b['novel_id'])
        self.assertEqual(updated['revision'], 2)
        corrupt = copy.deepcopy(updated)
        corrupt['original_concept']['original_text'] = 'A replacement origin'
        update['record_versions'] = [corrupt]
        with self.assertRaises(ValueError):
            validation.validate_exchange(seal(update), [b])
