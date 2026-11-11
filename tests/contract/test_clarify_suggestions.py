"""Check shipped prompt contracts; these do not verify actual host conversation."""
from importlib.resources import files
import unittest

from novel_creator.install import bundle_files


class ClarifySuggestions(unittest.TestCase):
    def test_both_format_resources_require_suggestions_and_custom_input(self):
        legacy = bundle_files()
        notebook = files('novel_creator.notebook_resources')
        codex = files('novel_creator.codex')
        resources = {
            'legacy': (
                legacy['.novel-creator/workflows/clarify.md'].decode(),
                legacy['.agents/skills/novel-clarify/SKILL.md'].decode()),
            'notebook': (
                notebook.joinpath('workflows/clarify.md').read_text(encoding='utf-8'),
                codex.joinpath('notebook/skills/novel-clarify/SKILL.md').read_text(encoding='utf-8')),
        }
        # These are normative instructions in the resources delivered by setup
        # and explicit updates, rather than an assertion about model compliance.
        workflow_requirements = (
            'By default, accompany each substantive question with 2–4',
            'grounded in the known story',
            'short labeled list (A, B, C, D as needed)',
            'one distinct proposition',
            'never pad the list',
            'Honor requests for fewer or no suggestions',
            '**Custom — type your own answer**',
            'reply with a label or in their own words',
            'unsure, skip or defer',
            'custom choice is additional to the suggested story answers',
            'Never auto-select an answer or treat silence as acceptance',
            'custom answer has the same standing as a selected suggestion',
            'Use plain chat',
            'without a selection widget, special tool or plan mode',
            'must preserve custom free-text input',
            "conversation's language",
        )
        for format_name, (workflow, skill) in resources.items():
            with self.subTest(format=format_name):
                normalized = ' '.join(workflow.split())
                for requirement in workflow_requirements:
                    self.assertIn(requirement, normalized)
                for requirement in ('labeled suggested answers', 'explicit custom-answer choice',
                                    "label or the writer's own words", 'fewer/no suggestions'):
                    self.assertIn(requirement, ' '.join(skill.split()))
                self.assertIn('clarify.md)', skill)

    def test_legacy_saves_the_complete_question_before_display(self):
        workflow = ' '.join(bundle_files()['.novel-creator/workflows/clarify.md'].decode().split())
        self.assertIn('save the whole question, suggested answers and custom-answer invitation before displaying them',
                      workflow)
        self.assertIn('save-before-display protocol', workflow)


if __name__ == '__main__':
    unittest.main()
