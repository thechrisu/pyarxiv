import re

import dateutil.parser


def convert_to_native_types(arxiv_entry):
    """
    Replaces all JSON constructs to native Python types.
    Concretely, we
    1. Fix whitespace in all fields
    2. Replace 'tags' property with a list of the actual tags
    3. Parse dates in 'published', 'updated' to datetime.datetime objects
    :param arxiv_entry: dict of arXiv entry
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
    :param arxiv_entry: dict containing arXiv entry
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
    :param string: to be modified string
    :return: modified string
    """
    spaces_fixed = re.sub(r'\s+', ' ', string)
    return re.sub(r'^\s|\s$', '', spaces_fixed)


def get_arxiv_id(url_or_id):
    """
    Given an url or an article stub, parse its id and version.
    Examples:
    get_arxiv_id('1709.1234v1') -> ('1709.1234', '1')
    get_arxiv_id('1709.1234') -> ('1709.1234', None)
    :param url_or_id: string of url or id of entry
    :return: (str: arxiv id, str: version)
    """
    i = url_or_id.rfind('abs/')
    if i != -1:
        id_version = url_or_id[i + 4:]
    else:
        id_version = url_or_id
    id_v_parts = id_version.split('v')
    if len(id_v_parts) > 1:
        return id_v_parts[0], id_v_parts[1]
    else:
        return id_v_parts[0], None


def uses_new_id(url_or_id):
    """
    Read about it here https://arxiv.org/help/arxiv_identifier
    :param url_or_id: string containing id or full url of arxiv entry
    :return: bool: whether the id is a new type
    """
    id_version = "" + url_or_id.split('/')[-1]
    return id_version.rfind('.') != -1
