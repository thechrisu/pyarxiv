#!/usr/bin/env python
"""
Example usage:
pyarxiv download 1409.6041 1709.1337
pyarxiv download --target-folder=papers --use-title-for-filename=true --apend-id=true 1501.1729

pyarxiv query cat:cs.AI --max-results=3
--ids=13 14 1
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

import pyarxiv


def progress_callback(elem, exc):
    if not exc is None:
        print(exc)
    else:
        tup = pyarxiv.get_arxiv_id(elem)
        i = tup[0]
        if not tup[1] is None:
            i += 'v' + tup[1]
        print('Downloaded %s' % i)


def main():
    parser = ArgumentParser("argparse [download | query] -h for help on subcommands")
    subparsers = parser.add_subparsers(help='download|query arXiv')

    parser_query = subparsers.add_parser('query', help='query arXiv')
    parser_query.set_defaults(which='query')
    parser_query.add_argument('ids', metavar='N', type=str, nargs='*', help='ids of arXiv papers to download/query')
    parser_query.add_argument('--title', '-t', type=str, nargs='?', help='Title of paper')
    parser_query.add_argument('--max-results', '-m', type=int, nargs='?', help='Max number of results to fetch')
    parser_query.add_argument('--authors', '-au', type=str, nargs='?', help='Title of paper')
    parser_query.add_argument('--abstract', '-abs', type=str, nargs='?', help='Abstract of paper')
    parser_query.add_argument('--journalref', '-jr', type=str, nargs='?', help='Journal reference of paper')
    parser_query.add_argument('--querystring', '-q', type=str, nargs='?', help='Query string')

    parser_download = subparsers.add_parser('download', help='download arXiv.org papers')
    parser_download.set_defaults(which='download')
    parser_download.add_argument('ids', metavar='N', type=str, nargs='*', help='ids of arXiv papers to download/query')
    parser_download.add_argument('--target-folder', '-t', type=str, nargs='?', help='Target folder')
    parser_download.add_argument('--use-title-for-filename', '-u',
                                 help='Use title of paper for filename', action='store_true')
    parser_download.add_argument('--append-id', '-a',
                                 help='If using use-title-for-filename, append id', action='store_true')
    parser_download.add_argument('--silent', '-s',
                                 help='Do not show progress', action='store_true')

    args = parser.parse_args()

    if args.which == 'query':
        max_r = 100
        title = ''
        authors = ''
        abstract = ''
        journal_ref = ''
        querystring = ''
        if not args.max_results is None:
            max_r = args.max_results
        if not args.title is None:
            title = args.title
        if not args.authors is None:
            authors = args.authors
        if not args.abstract is None:
            abstract = args.abstract
        if not args.journalref is None:
            journal_ref = args.journalref
        if not args.querystring is None:
            querystring = args.querystring

        ids = pyarxiv.query(ids=args.ids,
                            max_results=max_r,
                            title=title,
                            authors=authors,
                            abstract=abstract,
                            journal_ref=journal_ref,
                            querystring=querystring)
        tuples = list(map(lambda x: x[0] if x[1] is None else x[0] + 'v' + x[1],
                          map(lambda x: pyarxiv.get_arxiv_id(x), ids))
                      )
        print("\n".join(tuples))
    else:
        target = '.'
        prog = lambda x, y: id(x)
        if not args.target_folder is None:
            target = args.target_folder
        if not args.silent:
            prog = progress_callback
        pyarxiv.download_entries(args.ids,
                                 target_folder=target,
                                 use_title_for_filename=args.use_title_for_filename,
                                 append_id=args.append_id,
                                 progress_callback=prog)
        # print(parser_query.parse_args())
        # print(parser_download.parse_args())


if __name__ == "__main__":
    main()
