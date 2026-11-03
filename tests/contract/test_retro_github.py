import unittest
from novel_creator.cli import ToolError


class GithubBoundary(unittest.TestCase):
    def test_merge_identity_is_distinct_from_closed_unmerged(self):
        from novel_creator.retro_github import Github
        raw=dict(number=1,html_url='https://github.com/bjarkig82/novel-creator/pull/1',
                 head=dict(ref='synthetic',sha='a'*40),base=dict(ref='main',repo=dict(full_name='bjarkig82/novel-creator')),
                 draft=False,body='',title='Synthetic',state='closed')
        self.assertFalse(Github.normalize(raw)['merged'])
        self.assertTrue(Github.normalize(dict(raw,merged_at='2026-10-29T00:00:00Z'))['merged'])

    def test_canonical_origins_only(self):
        from novel_creator.retro_github import canonical_origin
        for origin in ('https://github.com/bjarkig82/novel-creator.git',
                       'git@github.com:bjarkig82/novel-creator.git'):
            self.assertEqual(canonical_origin(origin), 'https://github.com/bjarkig82/novel-creator.git')
        for origin in ('https://secret@github.com/bjarkig82/novel-creator.git',
                       'https://example.com/bjarkig82/novel-creator.git',
                       'https://github.com/other/repository.git'):
            with self.assertRaises(ToolError):
                canonical_origin(origin)
