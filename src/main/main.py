import argparse
from collections import Counter
import gzip
import re
import requests
import sys

URL_BASE = f'http://ftp.uk.debian.org/debian/dists/stable/main/'

def package_repr(pkgs: list) -> None:
    """
    pretty print packages and their frequencies

    ----
    input 
    pkgs: list of tuples w/ package name and occurence frequency: list
    ----
    returns: None
    ----
    """
    result = ""
    max_len = max(len(i[0]) for i in pkgs) + 4 # set standard line length so pkg counts line up
    for i, p in enumerate(pkgs):
        idx_str = str(i+1)
        name = p[0]
        count = p[1]
        spaces = (max_len-len(name)-len(idx_str)) * " "
        result += f'{idx_str}. {name}{spaces}{count}\n'
    print (result)


def package_parser(arch: str, count: int = 10) -> list:
    """
    Gather statistics of the top number packages that have the most files associated with them. Default is 10

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
        for l in lines:
            match = re.match(r'^(.*)\s+(\S+)$', l.decode('utf-8').strip())
            if match:
                file_path, current_pkgs = match.groups()
                pkg_count.update(current_pkgs.split(','))
        
        #count top <count> packages. 
        top_x = pkg_count.most_common(count)
        return top_x
    except Exception as e: # handle issues with requests itself
        print(f"Content not found at {url}. Please double check the architecture exists at {URL_BASE}.")
        print (e)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Debian top 10 packages per architecture')
    parser.add_argument(dest="architecture", help="Enter a Debian architecture, ex. amd64, arm64, mips etc. Usage: python main.py amd64")
    args = parser.parse_args()
    if args.architecture:
        arch = args.architecture
    else:
        print("Please pass in an architecture, for example amd64, arm64, mips etc.")
        sys.exit(0)
    

    pkgs = package_parser(arch) # call function to download & parse data
    package_repr(pkgs) # pretty print data
    

if __name__ == "__main__":
    sys.exit(main())