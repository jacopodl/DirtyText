class Match:
    __slots__ = ["idx", "char", "cval", "infos"]

    def __init__(self, index, char, infos=None):
        self.idx = index
        self.char = char
        self.cval = "%04X" % ord(self.char)
        self.infos = infos

    def to_dict(self):
        dct = {}
        for key in self.__slots__:
            dct[key] = getattr(self, key)
        return dct

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return self.__str__()
