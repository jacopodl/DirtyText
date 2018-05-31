import json
import os.path
import re
import urllib.error
import urllib.request as urequest

DBPATH = os.path.join(os.path.dirname(__file__), "data")
CATEGORIES_PATH = os.path.join(DBPATH, "categories.json")
CONFUSABLES_PATH = os.path.join(DBPATH, "confusables.json")

CONFUSABLES_PATTERN = re.compile(r"^([0-9a-fA-F]+)\s*;\s*([0-9a-fA-F]+)\s*;.+?\)\s*([\w\s-]+).+?([\w\s-]+)")
CATEGORIES_PATTERN = re.compile(r"^([a-fA-F0-9]+)\.*([a-fA-F0-9]*)\s*;\s*([\w\s]+)\s*#\s*([\w&-]+)")


def get_confusables(from_file="ftp://ftp.unicode.org/Public/security/latest/confusables.txt"):
    def __add_uchar(uchar, desc, hlist):
        if hlist:
            for itm in hlist:
                if itm["target"] == uchar:
                    return
            hlist.append({"target": uchar, "description": desc})
            return hlist
        return [{"target": uchar, "description": desc}]

    dct = {}
    try:
        response = urequest.urlopen(from_file, timeout=5)
    except urllib.error.HTTPError:
        return {}

    line = response.readline().decode()
    while line != "":
        match = CONFUSABLES_PATTERN.search(line)
        if match:
            k1 = match[1].strip()
            k2 = match[2].strip()
            dct[k1] = __add_uchar(k2, match[4].strip(), [])
            if k2 in dct:
                dct[k2] = __add_uchar(k1, match[3].strip(), dct[k2])
            else:
                dct[k2] = __add_uchar(k1, match[3].strip(), [])
        line = response.readline().decode()
    return dct


def get_categories(from_file="ftp://ftp.unicode.org/Public/UNIDATA/Scripts.txt"):
    try:
        response = urequest.urlopen(from_file, timeout=5)
    except urllib.error.HTTPError:
        return {}
    dct = {}

    line = response.readline().decode()
    while line != "":
        match = CATEGORIES_PATTERN.search(line)
        line = response.readline().decode()
        if match:
            itm = {"range": (int(match[1], 16), int(match[2] or match[1], 16)), "gcat": match[4].lower().strip()}
            cat = match[3].lower().strip()
            if cat in dct:
                dct[cat].append(itm)
                continue
            dct[cat] = [itm]
    # sort all
    for _, v in dct.items():
        sorted(v, key=lambda t: t["range"][0])
    return dct


def read_jdb(path):
    with open(path, "r") as file:
        return json.loads(file.read())


def _write_jdb(path, data):
    with open(path, "w") as file:
        file.write(json.dumps(data))


def update_jdb(bpath=DBPATH, force=False):
    operations = [{"func": get_categories,
                   "path": CATEGORIES_PATH
                   },
                  {"func": get_confusables,
                   "path": CONFUSABLES_PATH
                   }]
    for op in operations:
        if not os.path.exists(op["path"]) or force:
            data = op["func"]()
            if data:
                _write_jdb(op["path"], data)
