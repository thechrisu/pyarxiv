import dateutil.parser
import json

import pyarxiv.util as util


class ArxivEntry(object, json.JSONEncoder):
    author_detail = None
    guidislink = None
    published = None
    tags = None
    title_detail = None
    summary_detail = None
    arxiv_doi = None
    link = None
    title = None
    author = None
    links = None
    arxiv_comment = None
    id = None
    arxiv_journal_ref = None
    arxiv_primary_category = None
    authors = None
    updated = None
    summary = None

    @staticmethod
    def from_json(json_obj):
        e = ArxivEntry()
        e.author_detail = json_obj['author_detail']
        e.guidislink = json_obj['guidislink']
        e.tags = list(map(lambda x: x['term'], json_obj['tags']))
        e.title_detail = json_obj['title_detail']
        if 'value' in e.title_detail:
            e.title_detail['value'] \
                = util.fix_arxiv_whitespace(e.title_detail['value'])
        e.summary_detail = json_obj['summary_detail']
        e.link = json_obj['link']
        e.title = util.fix_arxiv_whitespace(json_obj['title'])
        e.author = json_obj['author']
        e.links = json_obj['links']
        e.id = json_obj['id']
        e.arxiv_primary_category = json_obj['arxiv_primary_category']
        e.authors = json_obj['authors']
        e.summary = util.fix_arxiv_whitespace(json_obj['summary'])
        e.published = dateutil.parser.parse(json_obj['published'])
        e.updated = dateutil.parser.parse(json_obj['updated'])
        if 'arxiv_doi' in json_obj:
            e.arxiv_doi = json_obj['arxiv_doi']
        if 'arxiv_comment' in json_obj:
            e.arxiv_comment = json_obj['arxiv_comment']
        if 'arxiv_journal_ref' in json_obj:
            e.arxiv_journal_ref = json_obj['arxiv_journal_ref']
        return e
