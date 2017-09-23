import sys

if sys.version_info < (3, 0):
    from urllib import quote_plus
    from urllib import urlopen
else:
    from urllib.parse import quote_plus
    from urllib.request import urlopen

import feedparser

ARXIV_API_BASE_URI = 'http://export.arxiv.org/api/query?'


def query(max_results=100, ids=[], categories=[],
          title='', authors='', abstract='', journal_ref='',
          querystring=''):
    """
    :param max_results: Max number of results, by default 100.
    :param ids: arXiv ids of entries to be found (ORed together).
    :param categories: A valid entry is e.g. ['math.AG', 'cs.AI']
    to search for papers in Algebraic Geometry and AI.
    :param title: Restrict search to papers with this string in their title.
    :param authors: Restrict search with this string in author name(s).
    :param abstract: Restrict search with this string in abstract.
    :param journal_ref: Restrict search to e.g. 'Phys Rev Lett'.
    :param querystring: Simply enter a query string ('manual mode').
    This query string must be properly escaped as by the arXiv API docs:
    https://arxiv.org/help/api/user-manual#query_details
    If this argument is present, all other values,
    except for max_results and ids are ignored.
    :return: list of dictionaries of arXiv entries matching query.
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
    raw_d = urlopen(
        ARXIV_API_BASE_URI + query).read()
    d = feedparser.parse(raw_d)
    return d.entries


def get_querystring(categories=[], title='', authors='',
                    abstract='', journal_ref=''):
    """
    Helper function for query() builds up a custom search query.
    :param categories: categories to be used.
    :param title: title of papers.
    :param authors: authors.
    :param abstract: abstract.
    :param journal_ref: journal ref.
    :return: Properly escaped search query.
    """
    query_elements = []
    if len(categories) > 0 and isinstance(categories, list):
        used_categories = " OR ".join(
            list(map(lambda x: 'cat:' + x, categories)))
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
