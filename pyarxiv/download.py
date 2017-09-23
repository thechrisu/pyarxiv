"""
Queries arxiv API and downloads papers (the query is a parameter).
Saves paper data in 'sample/**NUMBER**/data.json'
"""

from urllib import request
import feedparser
import json
import os

import pyarxiv.parse as pap

MAX_NUM_RESULTS = 100
MAX_PER_ITERATION = 20
ARXIV_API_BASE_URI = 'http://export.arxiv.org/api/query?'

ARXIV_CATEGORIES \
    = "cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG" \
      "+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML"

ARXIV_DIR = '../../sample/arxiv/'

def get_arxiv_feed_entries(categories, max_total_results, max_per_iter):
    used_categories = categories
    if isinstance(categories, list):
        used_categories = "+OR+".join(categories)
    entries = []
    for i in range(0, max_total_results, max_per_iter):
        query = 'search_query=%s&start=%i&max_results=%i' % (used_categories,
                                                             i,
                                                             max_per_iter)
        raw_d = request.urlopen(ARXIV_API_BASE_URI + query).read()
        d = feedparser.parse(raw_d)
        print("Downloading " + str(len(d.entries)) + " papers")
        entries += d.entries
    return entries


def save_arxiv_entry(entry, target_dir, file_name="data.json", override_existing=False):
    arxiv_id = pap.get_arxiv_id(entry)
    entry_dir = target_dir + arxiv_id + '/'
    if not os.path.isdir(entry_dir):
        os.mkdir(entry_dir)
    if override_existing or not os.path.isfile(entry_dir + file_name):
        entry_file = open(entry_dir + file_name, 'w')
        json.dump(entry, entry_file, ensure_ascii=False)
        entry_file.close()


def save_arxiv_entries(entries, target_dir, file_name="data.json"):
    """

    :param entries: list of arXiv feed
    """
    for e in entries:
        save_arxiv_entry(e, target_dir, file_name)


if __name__ == "__main__":
    entries = get_arxiv_feed_entries(ARXIV_CATEGORIES,
                                     MAX_NUM_RESULTS,
                                     MAX_PER_ITERATION)
    save_arxiv_entries(entries, ARXIV_DIR)
