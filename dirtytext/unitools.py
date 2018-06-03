from dirtytext.results import Match
from dirtytext.unicode_db import read_jdb, CATEGORIES_PATH, CONFUSABLES_PATH, CC_PATH, CF_PATH


class _Singleton:
    def __init__(self, clazz):
        self.clazz = clazz
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.clazz(*args, **kwargs)
        return self.instance


class UniTools:
    def __init__(self, categories=CATEGORIES_PATH, confusables=CONFUSABLES_PATH, control=CC_PATH, format=CF_PATH):
        self.categories = read_jdb(categories)
        self.confusables = read_jdb(confusables)
        self.cc = read_jdb(control)
        self.cf = read_jdb(format)
        print()

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
