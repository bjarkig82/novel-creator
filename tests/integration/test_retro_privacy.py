import unittest
from novel_creator.cli import ToolError
from tests.retro_helpers import fixtures


class Privacy(unittest.TestCase):
    def test_generalization_rejects_private_markers(self):
        from novel_creator.retro import privacy_check
        for private in ('C:\\Private\\Novel', '/home/writer/private', 'sk-secretvalue123456789',
                        '.novel-creator/local', 'password=secretvalue'):
            with self.assertRaises(ToolError): privacy_check(private, private_values=[])
        with self.assertRaises(ToolError): privacy_check('Synthetic text with SECRET_STORY_MARKER',private_values=['SECRET_STORY_MARKER'])
        privacy_check('A synthetic Unicode example: Þóra.', private_values=[])
