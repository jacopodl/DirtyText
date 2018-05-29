import re
import urllib.error
import urllib.request as urequest

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
            itm = {"sr": match[1], "er": match[2], "gcat": match[4]}
            cat = match[3].lower().strip()
            if cat in dct:
                dct[cat].append(itm)
                continue
            dct[cat] = [itm]
    return dct
