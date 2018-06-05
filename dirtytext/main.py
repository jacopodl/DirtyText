from dirtytext.unitools import *


def main():
    UnicodeDB.update_jdb()
    # check string:
    ck = "repⅼⅰcate"
    # print(ut.contains_confusables(ck))
    x = is_ascii(ck)
    print(ck)
    print(contains_confusables(ck, ["latin"]))


if __name__ == "__main__":
    main()
