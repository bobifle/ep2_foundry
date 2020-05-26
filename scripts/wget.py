import requests
import argparse
import os
import codecs


def download_file(url, fname):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download a file")
    parser.add_argument("url", type=str)
    parser.add_argument("-d", "--dst", type=str, default="")
    args = parser.parse_args()
    if not args.dst:
        args.dst = args.url.split("/")[-1]
    download_file(args.url, args.dst)
