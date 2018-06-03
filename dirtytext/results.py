class Match:
    __slots__ = ["idx", "char", "cval", "infos"]

    def __init__(self, index, char, infos=None):
        self.idx = index
        self.char = char
        self.cval = "%04X" % ord(self.char)
        self.infos = infos

    def __str__(self):
        return str({"idx": self.idx, "char": self.char, "cval": self.cval, "infos": self.infos})

    def __repr__(self):
        return self.__str__()
