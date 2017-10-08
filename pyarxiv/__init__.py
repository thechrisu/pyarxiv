"""
Queries and downloads papers from arXiv.org
"""
import os.path
import re
import sys
import urllib  # todo check python 2

import dateutil.parser
import feedparser

from pyarxiv.arxiv_categories import ArxivCategory, arxiv_category_map

ARXIV_DL_BASE_URL = "https://arxiv.org/pdf/"
ARXIV_API_BASE_URI = 'http://export.arxiv.org/api/query?'

if sys.version_info < (3, 0):
    from urllib import quote_plus
    from urllib import urlopen
else:
    from urllib.parse import quote_plus
    from urllib.request import urlopen


def retrieve(url, file):
    if sys.version_info <= (3, 0):  # pragma: no-cover
        urllib.urlretrieve(url, file)
    else:
        urllib.request.urlretrieve(url, file)


class ArxivQueryError(Exception):
    def __init__(self, message, cause):
        super(ArxivQueryError, self).__init__(
            message + u', caused by ' + repr(cause))
        self.cause = cause


def query(max_results=100, ids=[], categories=[],
          title='', authors='', abstract='', journal_ref='',
          querystring=''):
    """
    Queries arXiv.org for papers.

    :param max_results: Max number of results, by default 100.
    :type max_results: int
    :param ids: arXiv ids of entries to be found (OR-ed together).
    :type ids: List[str]
    :param categories: A valid entry is e.g. ['math.AG', 'cs.AI']
               to search for papers in Algebraic Geometry and AI.
    :type categories: List[str], List[ArxivCategory]
    :param str title: Restrict search to papers with this string
                   in their title.
    :param str authors: Restrict search with this string in author name(s).
    :param str abstract: Restrict search with this string in abstract.
    :param str journal_ref: Restrict search to e.g. 'Phys Rev Lett'.
    :param str querystring: Simply enter a query string ('manual mode').
                   This query string must be properly escaped as by the
                   arXiv API docs:
                   https://arxiv.org/help/api/user-manual#query_details
                   If this argument is present, all other values,
                   except for max_results and ids are ignored.
    :return: List of dictionaries of arXiv entries matching query.
    :rtype: List[dict]
    """
    if len(querystring) > 0:
        real_querystring = querystring
    else:
        real_querystring = get_querystring(categories,
                                           title,
                                           authors,
                                           abstract,
                                           journal_ref)
    search_query = "&search_query=" + real_querystring
    query = 'max_results=%i' % max_results
    if len(real_querystring) > 0:
        query += search_query
    if len(ids) > 0:
        query += "&id_list=" + ",".join(ids)
    try:
        raw_d = urlopen(
            ARXIV_API_BASE_URI + query).read()
        d = feedparser.parse(raw_d)
        return d.entries
    except Exception as e:
        raise ArxivQueryError(
            'Unable to query paper with query: %s' % query, e)


def get_querystring(categories=[], title='', authors='',
                    abstract='', journal_ref=''):
    """
    Helper function for query() builds up a custom search query.

    :param categories: categories to be used.
    :type categories: List[str], List[ArxivCategory]
    :param str title: title of papers.
    :param str authors: authors.
    :param str abstract: abstract.
    :param str journal_ref: journal ref.
    :return: Properly escaped search query.
    :rtype: str
    """
    query_elements = []
    if len(categories) > 0 and isinstance(categories, list):
        str_categories = list(map(lambda x:
                                  arxiv_category_map[x]
                                  if isinstance(x, ArxivCategory)
                                  else x, categories))
        used_categories = " OR ".join(
            list(map(lambda x: 'cat:' + x, str_categories)))
        query_elements.append("(" + used_categories + ")")
    if len(title) > 0:
        query_elements.append("ti:\"" + title + "\"")
    if len(authors) > 0:
        query_elements.append("au:\"" + authors + "\"")
    if len(abstract) > 0:
        query_elements.append("abs:\"" + abstract + "\"")
    if len(journal_ref) > 0:
        query_elements.append("jr:\"" + journal_ref + "\"")
    built_query = " AND ".join(query_elements)
    return quote_plus(built_query, safe=':+')


def convert_to_native_types(arxiv_entry):
    """
    Replaces all JSON constructs to native Python types.
    Concretely, we

    1. Fix whitespace in all fields
    2. Replace 'tags' property with a list of the actual tags
    3. Parse dates in 'published', 'updated' to datetime.datetime objects

    :param dict arxiv_entry: dict of arXiv entry
    """
    fix_entry_whitespace(arxiv_entry)
    arxiv_entry['tags'] = list(map(lambda x: x['term'], arxiv_entry['tags']))
    arxiv_entry['published'] = dateutil.parser.parse(arxiv_entry['published'])
    arxiv_entry['updated'] = dateutil.parser.parse(arxiv_entry['updated'])


def fix_entry_whitespace(arxiv_entry):
    """
    Converts whitespace to spaces in relevant fields.
    Then deletes duplicate spaces.
    Currently supported fields: title, summary, title_detail.value.
    Dict is modified in-place.

    :param dict arxiv_entry: dict containing arXiv entry
    """
    arxiv_entry['title'] = fix_str_whitespace(arxiv_entry['title'])
    arxiv_entry['summary'] = fix_str_whitespace(arxiv_entry['summary'])
    if 'value' in arxiv_entry['title_detail']:
        arxiv_entry['title_detail']['value'] \
            = fix_str_whitespace(arxiv_entry['title_detail']['value'])


def fix_str_whitespace(string):
    """
    Converts all whitespace to spaces in string.
    Deletes all duplicate spaces in string.
    Then deletes all spaces at start/end of string.

    :param str string: to be modified string
    :return: modified string
    :rtype: str
    """
    spaces_fixed = re.sub(r'\s+', ' ', string)
    return re.sub(r'^\s|\s$', '', spaces_fixed)


def get_arxiv_id(url_or_id_or_entry):
    """
    Given an url or an article stub, parse its id and version.
    Examples:

    get_arxiv_id('1709.1234v1') -> ('1709.1234', '1')

    get_arxiv_id('1709.1234') -> ('1709.1234', None)

    :param url_or_id_or_entry: string of url
                               or id of entry (still str)
                               or dict, possibly with 'id' key
    :type url_or_id_or_entry: str, dict
    :return: tuple separating id and version
    :rtype: (str, str), (str, None), (None, None)
    """
    elem = None
    if isinstance(url_or_id_or_entry, str):
        elem = url_or_id_or_entry
    else:
        if isinstance(url_or_id_or_entry, dict) \
                and 'id' in url_or_id_or_entry \
                and isinstance(url_or_id_or_entry['id'], str):
            elem = url_or_id_or_entry['id']
    if elem is None:
        return None, None
    i = elem.rfind('abs/')
    if i != -1:
        id_version = elem[i + 4:]
    else:
        id_version = elem
    id_v_parts = id_version.split('v')
    if len(id_v_parts) > 1:
        return id_v_parts[0], id_v_parts[1]
    else:
        return id_v_parts[0], None


def uses_new_id(url_or_id):
    """
    Read about arxiv ids here https://arxiv.org/help/arxiv_identifier

    :param str url_or_id: string containing id
                   or full url of arxiv entry
    :return: bool: whether the id is a new type
    """
    id_version = "" + url_or_id.split('/')[-1]
    return id_version.rfind('.') != -1


def make_filename_safe(filename):
    return "".join([c if c.isalnum() or c in '.' else '_' for c in filename])


def download_entry(arxiv_entry_or_id_or_uri=None,
                   target_folder='.',
                   target_filename='',
                   use_title_for_filename=False,
                   append_id=False):
    """
    Downloads an arXiv entry as PDF.

    :param arxiv_entry_or_id_or_uri: Paper at hand.
    :type arxiv_entry_or_id_or_uri: str, dict
    :param str target_folder: Default is '.'; Can be absolute or relative
    :param str target_filename: Pick file name manually,
                   .pdf is appended automatically.
    :param bool use_title_for_filename: Use title as file name
                    will be slower since we have to look up the paper
                    on arXiv.org. Default filename is <id of paper>.pdf.
    :param bool append_id: if use_title_for_filename is True,
                    and append_id is True, the paper's arXiv id will be
                    appended to the filename.
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
                    raise ValueError(
                        'Could not find title for paper id '
                        '\"%s\"' % arxiv_id_str)
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
        retrieve(full_dl_url, os.path.join(
            target_folder, full_filename + '.pdf'))
    else:
        raise ValueError(
            'Directory %s does not exist, '
            'cannot download paper' % target_folder)


def download_entries(entries_or_ids_or_uris=[], target_folder='.',
                     use_title_for_filename=False, append_id=False,
                     progress_callback=(lambda x, y: id)):
    """
    Download multiple entries at once. Will catch ValueErrors silently.

    :param entries_or_ids_or_uris: ids to download
    :type entries_or_ids_or_uris: List[str], List[dict]
    :param str target_folder: default is '.'.
    :param bool use_title_for_filename: If True, will query for each paper.
    :param bool append_id: If use_title_for_filename,
                    will append each paper's id to its filename
    :param progress_callback: called when each paper is done downloading.
               Signature of progress_callback is
               progress_callback(element, maybe_exception)
               element is the id/entry/uri that was just downloaded,
               maybe_exception is either None or a caught ValueError,
               depending on whether the method error'd or not
    :return: list of all exceptions thrown
    :rtype: List[ValueError]
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
