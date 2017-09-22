import re


def fix_arxiv_whitespace(string):
    spaces_fixed = re.sub(r'\s', ' ', string)
    return re.sub(r'^\s|\s$', '', spaces_fixed)
