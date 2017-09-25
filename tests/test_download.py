import unittest
import sys

from pyarxiv.download import download_entry

if sys.version_info >= (3, 3):  # starting python 3.3
    from unittest.mock import patch, Mock

else:
    from mock import patch, Mock


class TestDownloadEntry(unittest.TestCase):
    # @patch('pyarxiv.query.query')
    @patch('pyarxiv.download.retrieve')
    def test_exceptions(self,
                        m_retrieve):
        with self.assertRaises(ValueError):
            download_entry()
        with self.assertRaises(ValueError):
            download_entry('1',
                           target_folder='/\/\/\/\/\\\\\\////\\\\/')

    @patch('pyarxiv.download.query')
    @patch('pyarxiv.download.retrieve')
    def test_title_for_filename_exception(self,
                                          m_retrieve,
                                          m_query):
        m_query.return_value = []
        with self.assertRaises(ValueError):
            download_entry('id_that_definitely_does_not_exist',
                           use_title_for_filename=True)

    @patch('pyarxiv.download.retrieve')
    def test_legit_id(self, m_retrieve):
        download_entry('1709.05312')
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/1709.05312.pdf',
            './1709.05312.pdf')

    @patch('pyarxiv.download.query')
    @patch('pyarxiv.download.retrieve')
    def test_query_extracts_title(self,
                                  m_retrieve,
                                  m_query):
        m_query.return_value = [{'title': 'test_this_title_works'}]
        download_entry('1709.05312',
                       use_title_for_filename=True)  # causes the query
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/1709.05312.pdf',
            './test_this_title_works.pdf')

    @patch('pyarxiv.download.query')
    @patch('pyarxiv.download.retrieve')
    def test_append_id(self,
                       m_retrieve,
                       m_query):
        m_query.return_value = [{'title': 'test_this_title_works'}]
        download_entry('1709.05312v1',
                       use_title_for_filename=True,
                       append_id=True)  # causes the query
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/1709.05312v1.pdf',
            './test_this_title_works1709.05312v1.pdf')

    @patch('pyarxiv.download.retrieve')
    def test_custom_title(self,
                          m_retrieve):
        download_entry('some entry',
                       target_filename='final filename')
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/some entry.pdf',
            './final filename.pdf')

    @patch('pyarxiv.download.retrieve')
    def test_uses_title_from_entry_if_available(self,
                                                m_retrieve):
        download_entry({'id': 'some id',
                        'title': 'some title'},
                       use_title_for_filename=True)
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/some id.pdf',
            './some_title.pdf')
