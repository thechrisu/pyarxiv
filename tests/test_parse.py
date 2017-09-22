import unittest

from pyarxiv.parse import fix_str_whitespace, convert_to_native_types


class TestNativeTypeConversion(unittest.TestCase):
    def test_happy_path(self):
        r = {
            'tags': [{'term': 'TERM1'},
                     {'term': 'random'}
                     ],
            'published': '2017-09-22 14:35:17.803992',
            'updated': '2017-09-22 14:35:17.803992',
            'title': ' a\n title ',
            'summary': ' a\n summary ',
            'title_detail': {
                'value': ' a\n title_detail ',
            }
        }
        convert_to_native_types(r)
        self.assertListEqual(r['tags'], ['TERM1', 'random'])
        self.assertEqual(str(r['published']), '2017-09-22 14:35:17.803992')
        self.assertEqual(str(r['updated']), '2017-09-22 14:35:17.803992')
        self.assertEqual(r['title'], 'a title')
        self.assertEqual(r['summary'], 'a summary')
        self.assertEqual(r['title_detail']['value'], 'a title_detail')

    def test_no_value_in_title_detail(self):
        r = {
            'tags': [{'term': 'TERM1'},
                     {'term': 'random'}
                     ],
            'published': '2017-09-22 14:35:17.803992',
            'updated': '2017-09-22 14:35:17.803992',
            'title': ' a\n title ',
            'summary': ' a\n summary ',
            'title_detail': {}
        }
        convert_to_native_types(r)
        self.assertDictEqual(r['title_detail'], {})


class TestOneSpaceNewLine(unittest.TestCase):
    def test_no_spaces(self):
        test_strings = [
            'TheQuickBrownFox',
            '',
            'a',
            '61421.,/,./,.,/12312=309()}{'
        ]
        for s in test_strings:
            self.assertEqual(fix_str_whitespace(s), s)

    def test_delete_first_last_space(self):
        self.assertEqual(fix_str_whitespace(''), '')
        self.assertEqual(fix_str_whitespace(' '), '')
        self.assertEqual(fix_str_whitespace('  '), '')
        self.assertEqual(fix_str_whitespace(' a '), 'a')
        self.assertEqual(fix_str_whitespace(' a word '), 'a word')

    def test_delete_dupl_whitespace(self):
        self.assertEqual(fix_str_whitespace('    very \n \tdupl'),
                         'very dupl')


if __name__ == "__main__":
    unittest.main()
