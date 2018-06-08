import argparse
import json
import sys

from dirtytext.unitools import *


def check_jdb(force_upd):
    if not UnicodeDB.exists_jdb() or force_upd:
        print("[*] Updating database, please wait...", end="", flush=True)
        UnicodeDB.update_jdb(True)
        print(" [done]")


def get_stream(filename=""):
    if filename != "":
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def print_results(ckname, result, verbosity=False):
    print("\n%s: %s" % (ckname, result[0]))
    if verbosity:
        print("JSON:\n%s" % json.dumps([itm.to_dict() for itm in result[1]]))


def main():
    parser = argparse.ArgumentParser(description="Explore and sanitize unicode stream")
    parser.add_argument("--update", help="force database update", default=False, action="store_true")
    parser.add_argument("--ascii", help="check if the stream contains only ASCII characters", default=False,
                        action="store_true")
    parser.add_argument("--stats", help="check if the stream contains only ASCII characters", default=False,
                        action="store_true")
    parser.add_argument("--zero", help="check if the stream contains zero width characters", default=False,
                        action="store_true")
    parser.add_argument("--confusables", help="check if stream contains confusables characters",
                        nargs="+")
    parser.add_argument("--file", help="open file", default=str(), type=str)
    parser.add_argument("-v", help="show details", default=False, action="store_true")
    args = parser.parse_args()

    # check db status
    check_jdb(args.update)

    stream = get_stream(args.file)
    if stream is None:
        return 0

    if args.ascii:
        print_results("Contains only ascii chars: ", is_ascii(stream), args.v)

    if args.zero:
        print_results("Contains zero-width chars: ", contains_zerowidth(stream), args.v)

    if args.confusables:
        print_results("Contains confusables chars: ", contains_confusables(stream, args.confusables), args.v)

    if args.stats:
        print("\nStream compositions:")
        total = len(stream) / 100
        maxlen = 0
        result = stats(stream)

        # find key maxlen:
        for k in result.keys():
            if len(k) > maxlen:
                maxlen = len(k)

        for k, v in result.items():
            kspaced = k + ":"
            kspaced += " " * (maxlen - len(kspaced))
            bar = "#" * (int((v / total) / 10))
            print("%s\t%s\t| %d\t(%f%%)" % (kspaced, bar, v, v / total))


if __name__ == "__main__":
    main()
