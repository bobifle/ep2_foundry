import requests
import argparse
import os
import codecs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download a file")
    parser.add_argument("url", type=str)
    parser.add_argument("-d", "--dst", type=str, default="")
    args = parser.parse_args()
    if not args.dst:
        args.dst = os.path.basename(args.url)
    rsp = requests.get(args.url)
    txt = "text" in rsp.headers["Content-type"]
    _args = ("w",) if txt else ("wb",)
    _kwargs = {"encoding": "utf8"} if txt else {}
    with open(args.dst, *_args, **_kwargs) as dst:
        if txt:
            dst.write(rsp.text)
        else:
            for chunk in rsp:
                dst.write(chunk)
