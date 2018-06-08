from dirtytext.results import Match
from dirtytext.unicode_db import UnicodeDB


def _cat_bsearch(data, search):
    dlen = len(data)
    first = 0
    last = dlen
    while first <= last:
        mid = (first + last) // 2
        if mid >= dlen:
            break
        if data[mid]["range"][0] <= search <= data[mid]["range"][1]:
            return mid
        if search > data[mid]["range"][1]:
            first = mid + 1
            continue
        last = mid - 1
    return -1


def is_ascii(string):
    wrong = []
    for i in range(len(string)):
        if not is_ascii_char(ord(string[i])):
            wrong.append(Match(i, string[i]))
    return len(wrong) == 0, wrong


def is_mixed(string, allowed_blocks=list(["common"])):
    wrong = []
    for i in range(len(string)):
        test = -1
        char = ord(string[i])
        for block in allowed_blocks:
            test = _cat_bsearch(UnicodeDB().categories[block], char)
            if test >= 0:
                break
        if test < 0:
            wrong.append(Match(i, string[i]))
    return len(wrong) != 0, wrong


def contains_confusables(string, of_blocks=list()):
    confusables = UnicodeDB().confusables
    cbles = []
    for i in range(len(string)):
        key = "%04X" % ord(string[i])
        if key in confusables:
            targets = []
            if of_blocks:
                for blk in of_blocks:
                    for trg in confusables[key]:
                        if blk.upper() in trg["description"]:
                            targets.append(trg)
            else:
                targets = confusables[key]
            if targets:
                cbles.append(Match(i, string[i], targets))

    return len(cbles) != 0, cbles


def contains_zerowidth(string):
    wrong = []
    for i in range(len(string)):
        char = ord(string[i])
        for func in [is_control_char, is_format_char]:
            test = func(char)
            if test > -1:
                wrong.append(Match(i, string[i]))
                break
    return len(wrong) != 0, wrong


def is_ascii_char(char):
    char = ord(char) if type(char) != int else char
    return 0 <= char <= 255


def is_control_char(char):
    char = ord(char) if type(char) != int else char
    return _cat_bsearch(UnicodeDB().cc, char)


def is_format_char(char):
    char = ord(char) if type(char) != int else char
    return _cat_bsearch(UnicodeDB().cf, char)


def is_latinsubs(string):
    wrong = []
    if is_mixed(string, ["latin", "common"])[0]:
        raise RuntimeError("is_latinsubs accepts only latin script")

    chk = contains_confusables(string, ["latin"])
    if chk[0]:
        for itm in chk[1]:
            if not is_ascii_char(ord(itm.char)):
                wrong.append(itm)
    return len(wrong) != 0, wrong


def filter_string(string, matches):
    idx = 0
    for match in matches:
        pos = match.idx - idx
        string = string[:pos] + string[pos + 1:]
        idx += 1
    return string
