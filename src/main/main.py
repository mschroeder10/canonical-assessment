#!/usr/bin/python3
"""A program to display information from a Debian Contents file.

It determines the top 10 packages that have the most files associated with them.

"""

import argparse
from collections import Counter
import gzip
import re
import requests
import sys

URL_BASE = 'http://ftp.uk.debian.org/debian/dists/stable/main/'


def package_repr(pkgs: list) -> None:
    """Pretty print packages and their frequencies.

    ----
    input
    pkgs: list of tuples w/ package name and occurence frequency: list
    ----
    returns: None
    ----
    """
    # set standard line length so pkg counts line up
    max_len = max(len(i[0]) for i in pkgs) + 4
    for i, p in enumerate(pkgs, start=1):
        print(f'{i:2}. {p[0]:{max_len}}\t{p[1]}')


def package_parser(arch: str, count: int = 10) -> list:
    """Gather statistics of the top number packages that have the most files associated with them.

    ----
    input:
    arch: architecture to get: str
    count: number of packages to get: int
    ----
    returns: list of tuples containing package name and counts
    ----
    """
    pkg_count = Counter([])
    url = f'{URL_BASE}Contents-{arch}.gz'

    # download content from debian website
    try:
        req = requests.get(url, stream=True)
        req.raise_for_status()

        # read gzip encoded data
        data = req.raw
        with gzip.open(data, 'rb') as f:
            lines = f.readlines()

        # decode data to utf-8 and put all pkgs into list
        for line in lines:
            
            # Use a regular expression to parse a line in the contents file.
            # First group matches filename, beginning and ending with non-whitespace.
            # Second group matches list of packages without whitespace. Trailing whitespace is ignored.
            match = re.match(r'^(\S.*\S)\s+(\S+)\s*$', line.decode('utf-8').strip())
            if match:
                file_path, current_pkgs = match.groups()
                pkg_count.update(current_pkgs.split(','))

        # count top <count> packages.
        top_x = pkg_count.most_common(count)
        return top_x
    except Exception as e:  # handle issues with requests itself
        print(f"Content not found at {url}.")
        print(f"Please double check the architecture exists at {URL_BASE}.")
        print(e)
        sys.exit(1)


def main():
    """Run the application."""
    parser = argparse.ArgumentParser(description='Debian top 10 packages per architecture')
    parser.add_argument(dest="architecture",
                        help="Debian architecture name, ex. amd64, arm64, mips.")
    args = parser.parse_args()
    if args.architecture:
        arch = args.architecture
    else:
        print("Please pass in an architecture, for example amd64, arm64, mips etc.")
        sys.exit(0)

    pkgs = package_parser(arch)  # call function to download & parse data
    package_repr(pkgs)  # pretty print data


if __name__ == "__main__":
    sys.exit(main())
