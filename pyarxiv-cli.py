#!/usr/bin/env python
"""
Example usage:
pyarxiv download 1409.6041 1709.1337
pyarxiv download --target-folder=papers --use-title-for-filename=true --apend-id=true 1501.1729

pyarxiv query cat:cs.AI --max-results=3
--ids=13,14,1
--title='a new approach'
--authors='Andrej Karpathy'
--abstract='lol'
--journal_ref='a'
max_results=100, ids=[], categories=[],
          title='', authors='', abstract='', journal_ref='',
          querystring=''

You can also chain things, e.g.:

pyarxiv download $(pyarxiv query cat:cs.AI --max-results=50)
"""
from argparse import ArgumentParser


def main():
    parser = ArgumentParser("argparse [download | query] -h for help on subcommands")
    subparsers = parser.add_subparsers(help='download|query arXiv')

    parser_query = subparsers.add_parser('query', help='query arXiv')
    parser_query.add_argument('ids', metavar='N', type=str, nargs='*', help='ids of arXiv papers to download/query')

    parser_download = subparsers.add_parser('download', help='download arXiv.org papers')
    parser_download.add_argument('ids', metavar='N', type=str, nargs='*', help='ids of arXiv papers to download/query')
    # parser.add_argument('query', help="Query arXiv.org for a certain set of papers")
    print(parser.parse_args())
    print(parser_download.parse_args())

if __name__ == "__main__":
    main()
