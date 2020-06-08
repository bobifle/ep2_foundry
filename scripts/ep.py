import codecs, json
import requests
import sys
import functools
import logging
import os
import argparse
from typing import Generator, Sequence, Tuple

log = logging.getLogger("ep")
parser = argparse.ArgumentParser(
    description="Generate FVTT json data for the ep2 system."
)
parser.add_argument("type")
parser.add_argument("src")
parser.add_argument("dst")
args = parser.parse_args()

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore
img_root_url = "https://arokha.com/eclipsehelper/images/morphs"

pretty = functools.partial(json.dumps, sort_keys=True, indent=2)
compact = functools.partial(json.dumps, separators=(",", ":"))
bopen = open
open = functools.partial(codecs.open, encoding="utf8")


def getData(fname: str) -> list:
    data = None
    with open(fname, "r") as src:
        data = json.loads(src.read())
    return data


# return the image location
# fetch the url from the web if needed and serialize it on disk
def getImage(what: str, serialize_in: str) -> str:
    target = ""
    url = img_root_url + f"/{what}"
    target = serialize_in + "/" + what
    if not os.path.exists(target):
        # get it from the url
        rsp = requests.get(url)
        if "image" in rsp.headers["Content-Type"]:
            with bopen(target, "wb") as dst:
                for chunk in rsp:
                    dst.write(chunk)
    return "systems/ep2/" + target if target else target


def convert(data: Sequence, type: str) -> Generator[Tuple[dict, dict], None, None]:
    for e in data:
        # remove undesirable fields from EP2 data
        e.pop("id")
        yield {"name": e.pop("name"), "type": type, "data": e, "img": None}, e


def convert_morphs(data: Sequence) -> Generator[dict, None, None]:
    for e, d in convert(data, "morph"):
        e["img"] = getImage(d.pop("image") or "none.png", "icons/items/morphs")
        # change movement_rate structure
        mr = d.pop("movement_rate")
        d["movement_rate"] = {mov.pop("movement_type").lower(): mov for mov in mr}
        yield e


def convert_gear_items(data: Sequence) -> Generator[dict, None, None]:
    for e, d in convert(data, "gear"):
        yield e


def convert_weapon_melee(data: Sequence) -> Generator[dict, None, None]:
    for e, d in convert(data, "weapon"):
        raw = d.pop("complexity/gp", "").split("/")
        if raw is None:
            continue
        d["complexity"], d["gp"] = (
            raw[0],
            raw[-1],
        )  # sometimes "Min/R/1" drop the R until i know what it is
        yield e


convertions = {
    "morphs": convert_morphs,
    "gear_items": convert_gear_items,
    "weapons_melee": convert_weapon_melee,
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(args.dst, "w") as dst:
        dst.write(pretty(list(convertions[args.type](getData(args.src)))))
