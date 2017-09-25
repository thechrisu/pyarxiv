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
    """
    Downloads an arXiv entry as PDF
    :param arxiv_entry_or_id_or_uri: Paper at hand.
    :param target_folder: Default is '.'. Can be absolute or relative
    :param target_filename: Pick file name manually,
    .pdf is appended automatically.
    :param use_title_for_filename: Use title as file name
    will be slower since we have to look up the paper on arXiv.org.
    Default filename is <id of paper>.pdf.
    :param append_id: use_title_for_filename is True, you can append the paper id here.
    """
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


def download_entries(entries_or_ids_or_uris=[], target_folder='.',
                     use_title_for_filename=False, append_id=False,
                     progress_callback=(lambda x, y: id)):
    """
    Download multiple entries at once. Will catch ValueErrors silently
    :param entries_or_ids_or_uris: ids to download
    :param target_folder: default is '.'.
    :param use_title_for_filename: If True, will query for each paper.
    :param append_id: If use_title_for_filename,
    will append each paper's id to its filename
    :param progress_callback: called when each paper is done downloading.
    Signature of progress_callback is progress_callback(element,
                                                        maybe_exception)
    element is the id/entry/uri that was just downloaded,
    maybe_exception is either None or a caught ValueError, depending on
    whether the method error'd or not
    :return: list of all exceptions thrown
    """
    exceptions = []
    for e in entries_or_ids_or_uris:
        new_exception = None
        try:
            download_entry(e, target_folder,
                           use_title_for_filename=use_title_for_filename,
                           append_id=append_id)
        except ValueError as exc:  # Maybe catch more types of exception?
            exceptions.append(exc)
            new_exception = exc
        finally:
            progress_callback(e, new_exception)
    return exceptions
