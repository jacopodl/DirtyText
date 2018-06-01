from dirtytext.unicode_db import *
from dirtytext.unitools import *


def main():
    update_jdb()
    # check string:
    ck = "\u037e"
    ut = UniTools()
    print(ut.contains_confusables(ck))


if __name__ == "__main__":
    main()
