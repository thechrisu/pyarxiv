import unittest
import sys

import pyarxiv.query as paq
from pyarxiv.arxiv_categories import ArxivCategory

if sys.version_info >= (3, 3):  # starting python 3.3
    from unittest.mock import patch, Mock

else:
    from mock import patch, Mock


class TestQuery(unittest.TestCase):
    @patch('feedparser.parse')
    @patch('pyarxiv.query.urlopen')
    def test_default(self,
                     mock_req,
                     mock_parse):
        parse_ret = Mock()
        parse_ret.entries = 'asdf'
        mock_parse.return_value = parse_ret
        self.assertEqual(paq.query(max_results=100), 'asdf')
        mock_req.assert_called_with(
            "http://export.arxiv.org/api/query?max_results=100")

    @patch('feedparser.parse')
    @patch('pyarxiv.query.urlopen')
    def test_querystring_provided_overrides_others_except_for_id(self,
                                                                 mock_req,
                                                                 mock_parse):
        paq.query(max_results=100,
                  ids=['1'],
                  authors='asdf',
                  querystring='somequerystring')
        mock_req.assert_called_with(
            "http://export.arxiv.org/api/query?max_results=100"
            "&search_query=somequerystring&id_list=1")

    @patch('feedparser.parse')
    @patch('pyarxiv.query.urlopen')
    def test_id_string_comma_separated(self,
                                       mock_req,
                                       mock_parse):
        paq.query(ids=['1', '2'])
        mock_req.assert_called_with(
            "http://export.arxiv.org/api/query?max_results=100"
            "&id_list=1,2")

    @patch('feedparser.parse')
    @patch('pyarxiv.query.urlopen')
    def test_max_results_always_there(self,
                                      mock_req,
                                      mock_parse):
        paq.query()
        mock_req.assert_called_with(
            "http://export.arxiv.org/api/query?max_results=100")


class TestQueryConstruction(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(paq.get_querystring(), '')

    def test_categories(self):
        self.assertEqual(paq.get_querystring('somestring'),
                         '')
        self.assertEqual(paq.get_querystring(['randomString']),
                         '%28cat:randomString%29')
        self.assertEqual(paq.get_querystring(['randcat', 'rand2']),
                         '%28cat:randcat+OR+cat:rand2%29')

    def test_categories_converts_arxivcategories(self):
        self.assertEqual(paq.get_querystring(['rand1',
                                              ArxivCategory.cs_AI,
                                              'otherRandomString']),
                         '%28cat:rand1+OR+cat:cs.AI+OR+'
                         'cat:otherRandomString%29')

    def test_title(self):
        self.assertEqual(paq.get_querystring(title=''), '')
        self.assertEqual(paq.get_querystring(title='some random title'),
                         'ti:%22some+random+title%22')

    def test_authors(self):
        self.assertEqual(paq.get_querystring(authors='some author name'),
                         'au:%22some+author+name%22')

    def test_abstract(self):
        self.assertEqual(paq.get_querystring(abstract='some abstract'),
                         'abs:%22some+abstract%22')

    def test_journal_ref(self):
        self.assertEqual(paq.get_querystring(journal_ref='Phys Rev Lett'),
                         'jr:%22Phys+Rev+Lett%22')

    def test_all_together_now(self):
        self.assertEqual(paq.get_querystring(['cs.AI', 'cs.INVENTED'],
                                             'some title',
                                             'some author',
                                             'some abstract',
                                             'journal ref'),
                         '%28cat:cs.AI+OR+cat:cs.INVENTED%29+AND+'
                         'ti:%22some+title%22+AND+'
                         'au:%22some+author%22+AND+'
                         'abs:%22some+abstract%22+AND+'
                         'jr:%22journal+ref%22')


if __name__ == "__main__":
    unittest.main()
