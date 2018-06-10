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


def check(ckdsc, func, *args, **kwargs):
    result = func(*args, **kwargs)
    print("\n%s: %s" % (ckdsc, result[0]))
    return result


def make_report(ckresult, verbosity=False, report=False):
    if verbosity or report:
        data = {"data": [itm.to_dict() for itm in ckresult[1]]}
        if verbosity:
            print("JSON:\n%s" % json.dumps(data["data"]))
        return data
    return {}


def main():
    parser = argparse.ArgumentParser(description="Explore and sanitize unicode stream")
    parser.add_argument("--update", help="force database update", default=False, action="store_true")
    parser.add_argument("--ascii", help="check if the stream contains ONLY ASCII characters", default=False,
                        action="store_true")
    parser.add_argument("--confusables", help="check if stream contains CONFUSABLES characters", nargs="+",
                        metavar="BLOCK")
    parser.add_argument("--stats", help="print text composition by unicode block", default=False,
                        action="store_true")
    parser.add_argument("--zero", help="check if the stream contains ZERO-WIDTH characters", default=False,
                        action="store_true")
    parser.add_argument("--file", help="open file", default=str(), type=str)
    parser.add_argument("--report", help="write JSON report", default=str(), type=str)
    parser.add_argument("-v", help="show details", default=False, action="store_true")
    args = parser.parse_args()

    report = {}

    # check db status
    check_jdb(args.update)

    stream = get_stream(args.file)
    if stream is None:
        return 0

    if args.ascii:
        data = check("Contains only ascii chars: ", is_ascii, stream)
        report["non_ascii"] = make_report(data, args.v, args.report)

    if args.zero:
        data = check("Contains zero-width chars: ", contains_zerowidth, stream)
        report["zero_width"] = make_report(data, args.v, args.report)

    if args.confusables:
        data = check("Contains confusables chars: ", contains_confusables, stream, args.confusables)
        report["confusables"] = make_report(data, args.v, args.report)

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

    if args.report and report:
        with open(args.report, "w") as file:
            file.write(json.dumps(report))


if __name__ == "__main__":
    main()
