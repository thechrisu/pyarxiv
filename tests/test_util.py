import unittest

from pyarxiv.util import fix_arxiv_whitespace


class TestOneSpaceNewLine(unittest.TestCase):
    def test_no_spaces(self):
        test_strings = [
            'TheQuickBrownFox',
            '',
            'a',
            '61421.,/,./,.,/12312=309()}{'
        ]
        for s in test_strings:
            self.assertEqual(fix_arxiv_whitespace(s), s)

    def test_delete_first_last_space(self):
        self.assertEqual(fix_arxiv_whitespace(''), '')
        self.assertEqual(fix_arxiv_whitespace(' '), '')
        self.assertEqual(fix_arxiv_whitespace('  '), '')
        self.assertEqual(fix_arxiv_whitespace(' a '), 'a')
        self.assertEqual(fix_arxiv_whitespace(' a word '), 'a word')

if __name__ == "__main__":
    unittest.main()
