import unittest

import pyarxiv.parse as pap


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
        pap.convert_to_native_types(r)
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
        pap.convert_to_native_types(r)
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
            self.assertEqual(pap.fix_str_whitespace(s), s)

    def test_delete_first_last_space(self):
        self.assertEqual(pap.fix_str_whitespace(''), '')
        self.assertEqual(pap.fix_str_whitespace(' '), '')
        self.assertEqual(pap.fix_str_whitespace('  '), '')
        self.assertEqual(pap.fix_str_whitespace(' a '), 'a')
        self.assertEqual(pap.fix_str_whitespace(' a word '), 'a word')

    def test_delete_dupl_whitespace(self):
        self.assertEqual(pap.fix_str_whitespace('    very \n \tdupl'),
                         'very dupl')


class TestUsesNewId(unittest.TestCase):
    def test_new_id(self):
        self.assertTrue(pap.uses_new_id('1705.00557v1'))
        self.assertTrue(pap.uses_new_id('1409.6041'))

    def test_new_id_urls(self):
        self.assertTrue(pap.uses_new_id('https://arxiv.org/abs/1709.07432v1'))
        self.assertTrue(pap.uses_new_id('https://arxiv.org/abs/1709.07359'))

    def test_old_id_urls(self):
        self.assertFalse(
            pap.uses_new_id('https://arxiv.org/abs/cmp-lg/9808001v1'))
        self.assertFalse(
            pap.uses_new_id('https://arxiv.org/abs/cs/9808001v1'))

    def test_old_id(self):
        self.assertFalse(pap.uses_new_id('9808001v1'))
        self.assertFalse(pap.uses_new_id('9808001v1'))
        self.assertFalse(pap.uses_new_id('cmp-lg/9808001v1'))
        self.assertFalse(pap.uses_new_id('cs/9808001v1'))


class TestGetId(unittest.TestCase):
    def test_new_id(self):
        self.assertEqual(pap.get_arxiv_id('1705.00557v1'),
                         ('1705.00557', '1'))
        self.assertEqual(pap.get_arxiv_id('1409.6041'),
                         ('1409.6041', None))

    def test_new_id_urls(self):
        self.assertEqual(
            pap.get_arxiv_id('https://arxiv.org/abs/1709.07432v1'),
            ('1709.07432', '1'))
        self.assertEqual(
            pap.get_arxiv_id('https://arxiv.org/abs/1709.07359'),
            ('1709.07359', None))

    def test_old_id_urls(self):
        self.assertEqual(
            pap.get_arxiv_id('https://arxiv.org/abs/cmp-lg/9808001v1'),
            ('cmp-lg/9808001', '1'))
        self.assertEqual(
            pap.get_arxiv_id('https://arxiv.org/abs/cs/9808001v1'),
            ('cs/9808001', '1'))

    def test_old_id(self):
        self.assertEqual(pap.get_arxiv_id('9808001v1'),
                         ('9808001', '1'))
        self.assertEqual(pap.get_arxiv_id('9808001'),
                         ('9808001', None))
        self.assertEqual(pap.get_arxiv_id('cmp-lg/9808001v1'),
                         ('cmp-lg/9808001', '1'))
        self.assertEqual(pap.get_arxiv_id('cs/9808001v1'),
                         ('cs/9808001', '1'))


if __name__ == "__main__":
    unittest.main()
