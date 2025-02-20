import argparse
from collections import Counter
import gzip
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
    pkgs = []
    url = f'{URL_BASE}Contents-{arch}.gz'

    # download content from debian website
    try: 
        req = requests.get(url, stream=True)
        if req.status_code == 404: # check if content is found
            print(f"Content not found at {url}. Please double check the architecture exists at {URL_BASE}.")
            sys.exit(1)
    except Exception as e: # handle issues with requests itself
        print (f"There was an error downloading content at {url}")
        print (e)
        sys.exit(1)

    # read gzip encoded data
    data = req.raw
    with gzip.open(data, 'rb') as f:
        lines = f.readlines()
    
    # decode data to utf-8 and put all pkgs into list
    for l in lines:
        l = l.decode("utf-8")
        current_pkgs = l.split()[1].split(',')
        pkgs.extend(current_pkgs)
    
    #count top <count> packages. 
    pkg_count = Counter(pkgs)
    top_x = pkg_count.most_common(count)
    return top_x

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