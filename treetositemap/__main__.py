#!/usr/bin/env python

import argparse

from .src.application.makesitemapindexfromfiles import MakeSiteMapIndexFromFiles
from .src.infrastructure.basicdateservice import BasicDateService
from .src.infrastructure.contentregexresultvalidator import ContentRegexResultValidator
from .src.infrastructure.inmemorysitemaprepository import \
    InMemorySiteMapRepository
from .src.infrastructure.localfilefinder import LocalFileFinder
from .src.infrastructure.xmlsitemapwriter import XmlSiteMapWriter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-x",
        "--xmlnsmobile",
        help="XMLNS-MOBILE attribute value for root XML tag",
        default="http://www.google.com/schemas/sitemap-mobile/1.0"
    )
    parser.add_argument(
        "-X",
        "--xmlns",
        help="XMLNS attribute value for root XML tag",
        default="http://www.sitemaps.org/schemas/sitemap/0.9"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Local output directory for the output sitemap resources",
        required=True
    )
    parser.add_argument(
        "-l",
        "--localpath",
        help="Local absolute path to directory that you want to index files "
             "into. For example '/var/www/html/path/to/files'",
        required=True
    )
    parser.add_argument(
        "-p",
        "--pathpattern",
        help="UNIX style pathname pattern expansion relative to --localpath. "
             "For example '**/*.htm*' will index all html and htm files",
        required=True
    )
    parser.add_argument(
        "-P",
        "--validpattern",
        help='Pattern to check the indexing files content, if the content '
             'does not match the pattern, the file is not indexed. '
             'For example: '
             '(?s)\\A(?!.*?(?<!\\w)(I do not want this file)(?!\\w)).*'
    )
    parser.add_argument(
        "-d",
        "--domain",
        help="Destination domain with path that you want the search engines "
             "index. For example 'https://mydomain.dot/path/to/files'",
        required=True
    )
    parser.add_argument(
        "-M",
        "--maxurlset",
        help="Maximum number of urlset tags for each sitemap file",
        default=250
    )
    return parser.parse_args()


def main():
    args = parse_args()

    sitemap_repository = InMemorySiteMapRepository()
    sitemap_file_service = LocalFileFinder()

    if args.validpattern:
        validator = ContentRegexResultValidator(args.validpattern)
    else:
        validator = None

    date_service = BasicDateService()
    sitemap_writer = XmlSiteMapWriter(
        args.xmlns,
        args.xmlnsmobile
    )

    use_case = MakeSiteMapIndexFromFiles(
        date_service,
        sitemap_repository,
        sitemap_file_service,
        validator,
        sitemap_writer,
        "sitemaps"
    )

    use_case.invoke(
        args.localpath,
        args.pathpattern,
        args.domain,
        args.output,
        args.maxurlset
    )


if __name__ == '__main__':
    main()
