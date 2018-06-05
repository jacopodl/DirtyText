from dirtytext.results import Match
from dirtytext.unicode_db import read_jdb, CATEGORIES_PATH, CONFUSABLES_PATH, CC_PATH, CF_PATH


class UniTools:
    def __init__(self, categories=CATEGORIES_PATH, confusables=CONFUSABLES_PATH, control=CC_PATH, format=CF_PATH):
        self.categories = read_jdb(categories)
        self.confusables = read_jdb(confusables)
        self.cc = read_jdb(control)
        self.cf = read_jdb(format)

    @staticmethod
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

    @staticmethod
    def is_ascii(string):
        wrong = []
        for i in range(len(string)):
            if ord(string[i]) > 255 or ord(string[i]) < 0:
                wrong.append(Match(i, string[i]))
        return len(wrong) != 0, wrong

    def is_mixed(self, string, allowed_blocks=list(["common"])):
        wrong = []
        for i in range(len(string)):
            test = -1
            char = ord(string[i])
            for block in allowed_blocks:
                test = UniTools._cat_bsearch(self.categories[block], char)
                if test >= 0:
                    break
            if test < 0:
                wrong.append(Match(i, string[i]))
        return len(wrong) != 0, wrong

    def contains_confusables(self, string, allowed_blocks=list()):
        cbles = []
        for i in range(len(string)):
            key = "%04X" % ord(string[i])
            if key in self.confusables:
                targets = []
                if allowed_blocks:
                    for blk in allowed_blocks:
                        for trg in self.confusables[key]:
                            if blk.upper() in trg["description"]:
                                targets.append(trg)
                else:
                    targets = self.confusables[key]
                if targets:
                    cbles.append(Match(i, string[i], targets))

        return len(cbles) != 0, cbles

    def contains_zerowidth(self, string):
        wrong = []
        for i in range(len(string)):
            char = ord(string[i])
            for func in [self.is_control_char, self.is_format_char]:
                test = func(char)
                if test > -1:
                    wrong.append(Match(i, string[i]))
                    break
        return len(wrong) != 0, wrong

    def is_control_char(self, char):
        return UniTools._cat_bsearch(self.cc, char)

    def is_format_char(self, char):
        return UniTools._cat_bsearch(self.cf, char)

    @staticmethod
    def filter(string, matchs):
        idx = 0
        for match in matchs:
            pos = match.idx - idx
            string = string[:pos] + string[pos + 1:]
            idx += 1
        return string
