import sys
import unittest

from pyarxiv import download_entry, download_entries

if sys.version_info >= (3, 3):  # starting python 3.3
    from unittest.mock import patch

else:
    from mock import patch


class TestDownloadEntry(unittest.TestCase):
    # @patch('pyarxiv.query.query')
    @patch('pyarxiv.retrieve')
    def test_exceptions(self,
                        m_retrieve):
        with self.assertRaises(ValueError):
            download_entry()
        with self.assertRaises(ValueError):
            download_entry('1',
                           target_folder='/\/\/\/\/\\\\\\////\\\\/')

    @patch('pyarxiv.query')
    @patch('pyarxiv.retrieve')
    def test_title_for_filename_exception(self,
                                          m_retrieve,
                                          m_query):
        m_query.return_value = []
        with self.assertRaises(ValueError):
            download_entry('id_that_definitely_does_not_exist',
                           use_title_for_filename=True)

    @patch('pyarxiv.retrieve')
    def test_legit_id(self, m_retrieve):
        download_entry('1709.05312')
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/1709.05312.pdf',
            './1709.05312.pdf')

    @patch('pyarxiv.query')
    @patch('pyarxiv.retrieve')
    def test_query_extracts_title(self,
                                  m_retrieve,
                                  m_query):
        m_query.return_value = [{'title': 'test_this_title_works'}]
        download_entry('1709.05312',
                       use_title_for_filename=True)  # causes the query
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/1709.05312.pdf',
            './test_this_title_works.pdf')

    @patch('pyarxiv.query')
    @patch('pyarxiv.retrieve')
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

    @patch('pyarxiv.retrieve')
    def test_custom_title(self,
                          m_retrieve):
        download_entry('some entry',
                       target_filename='final filename')
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/some entry.pdf',
            './final filename.pdf')

    @patch('pyarxiv.retrieve')
    def test_uses_title_from_entry_if_available(self,
                                                m_retrieve):
        download_entry({'id': 'some id',
                        'title': 'some title'},
                       use_title_for_filename=True)
        m_retrieve.assert_called_once_with(
            'https://arxiv.org/pdf/some id.pdf',
            './some_title.pdf')


class TestDownloadMultipleEntries(unittest.TestCase):
    @patch('pyarxiv.download_entry')
    def test_proress_callback(self,
                              m_download_entry):
        def test_method_correctly_iterates(id_used, exception):
            self.assertIsNone(exception)
            self.assertIn(id_used, ['1', '2'])

        self.assertListEqual(
            download_entries(['1', '2'],
                             progress_callback=test_method_correctly_iterates),
            [])

    @patch('pyarxiv.download_entry')
    def test_exceptions_correctly_logged(self,
                                         m_download_entry):
        def side_effect(arg, arg2,
                        use_title_for_filename=True,
                        append_id=False):
            if arg == 'yes':
                raise ValueError
        m_download_entry.side_effect = side_effect
        self.assertEqual(
            len(download_entries(['no', 'yes', 'no', 'yes', 'no'])),
            2)


if __name__ == "__main__":
    unittest.main()
