"""
Queries arxiv API and downloads papers (the query is a parameter).
Saves paper data in 'sample/**NUMBER**/data.json'
"""
from pyarxiv.parse import get_arxiv_id, make_filename_safe
from pyarxiv.query import query
import os.path
import urllib  # todo check python 2
import sys

ARXIV_DL_BASE_URL = "https://arxiv.org/pdf/"


def retrieve(url, file):
    if sys.version_info <= (3, 0):  # pragma: no-cover
        urllib.retrieve(url, file)
    else:
        urllib.requests.urlretrieve(url, file)


def download_entry(arxiv_entry_or_id_or_uri=None, target_folder='.', target_filename='',
                   use_title_for_filename=False, append_id=False):
    arxiv_id = get_arxiv_id(arxiv_entry_or_id_or_uri)
    if arxiv_id[0] is None:
        raise ValueError('Illegal arxiv_id of entry %s'
                         % str(arxiv_entry_or_id_or_uri))
    arxiv_id_str = arxiv_id[0]
    if not arxiv_id[1] is None:
        arxiv_id_str += 'v' + arxiv_id[1]
    if target_filename != '':
        full_filename = target_filename
    else:
        if use_title_for_filename:
            if isinstance(arxiv_entry_or_id_or_uri, dict):
                title = arxiv_entry_or_id_or_uri['title']
            else:
                query_result = query(ids=[arxiv_id_str])
                if len(query_result) < 1:
                    raise ValueError('Could not find title for paper id \"%s\"' % arxiv_id_str)
                else:
                    title = query_result[0]['title']
            if append_id:
                full_filename = make_filename_safe(title + arxiv_id_str)
            else:
                full_filename = make_filename_safe(title)
        else:
            full_filename = make_filename_safe(arxiv_id_str)  # may contain '/'
    full_dl_url = ARXIV_DL_BASE_URL + arxiv_id_str + ".pdf"
    if os.path.isdir(target_folder):
        retrieve(full_dl_url, os.path.join(target_folder, full_filename + '.pdf'))
    else:
        raise ValueError('Directory %s does not exist, cannot download paper' % target_folder)
