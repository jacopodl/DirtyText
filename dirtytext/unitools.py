from dirtytext.unicode_db import read_jdb, CATEGORIES_PATH, CONFUSABLES_PATH


class _singleton:
    def __init__(self, clazz):
        self.clazz = clazz
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.clazz(*args, **kwargs)
        return self.instance


@_singleton
class UniTools:
    def __init__(self):
        self.categories = read_jdb(CATEGORIES_PATH)
        self.confusables = read_jdb(CONFUSABLES_PATH)

    def is_mixed(self, string, allowed_blocks=list(["common"])):
        wrong = []
        for i in range(len(string)):
            test = False
            char = ord(string[i])
            for block in allowed_blocks:
                cat = self.categories[block]
                first = 0
                last = len(cat)
                while first <= last:
                    mid = (first + last) // 2
                    if cat[mid]["range"][0] <= char <= cat[mid]["range"][1]:
                        test = True
                        break
                    if char > cat[mid]["range"][1]:
                        first = mid + 1
                        continue
                    last = mid - 1
                if test:
                    break
            if not test:
                wrong.append({"idx": i, "char": string[i], "value": "%04X" % char})
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
                    cbles.append({"pos": i, "char": string[i], "targets": targets})

        return len(cbles) != 0, cbles
