#!/usr/bin/env python3
import argparse
import json
import sys

from dirtytext.unitools import *


def check_jdb(force_upd):
    if not UnicodeDB.exists_jdb() or force_upd:
        print("[*] Updating database, please wait...", end="", flush=True)
        UnicodeDB.update_jdb(True)
        print(" [done]")


def get_stream(filename=None):
    if filename is not None:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def exec_analysis(description, verbosity, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if verbosity:
        print("\n%s: %s" % (description, result[0]))
    return result


def make_report(results, verbosity=False, report=False):
    if verbosity or report:
        data = {"data": [itm.to_dict() for itm in results[1]]}
        if verbosity:
            print("JSON:\n%s" % json.dumps(data["data"]))
        return data
    return {}


def main():
    parser = argparse.ArgumentParser(description="Explore and sanitize unicode stream")
    parser.add_argument("--ascii", help="check if the stream contains ONLY ASCII characters", default=False,
                        action="store_true")
    parser.add_argument("--confusables", help="check if stream contains CONFUSABLES characters", nargs="+",
                        metavar="<block>")
    parser.add_argument("-c", "--check", dest="check", help="checks anomalies in a LATIN unicode stream", default=False,
                        action="store_true")
    parser.add_argument("-b", dest="blocks", help="shows unicode blocks and exit", default=False, action="store_true")
    parser.add_argument("-f", "--file", help="open file", default=None, type=str, metavar="<file>")
    parser.add_argument("--filter", dest="filter", help="filter unicode stream", default=False,
                        action="store_true")
    parser.add_argument("-p", "--pipeline", help="return modified stream to stdout", default=False, action="store_true")
    parser.add_argument("--report", help="write JSON report", default=str(), type=str, metavar="<file>")
    parser.add_argument("-s", "--save", dest="save", help="save modified stream", default=None, type=str,
                        metavar="<file>")
    parser.add_argument("--stats", help="print text composition by unicode block", default=False, action="store_true")
    parser.add_argument("--update", help="force database update", default=False, action="store_true")
    parser.add_argument("-v", "--verbose", dest="verbose", help="show details", default=False, action="store_true")
    parser.add_argument("-w", "--wipe", dest="wipe", help="removes anomaly in LATIN unicode text", default=False,
                        action="store_true")
    parser.add_argument("--zero", help="check if the stream contains ZERO-WIDTH characters", default=False,
                        action="store_true")
    args = parser.parse_args()

    report = {}

    # check db status
    check_jdb(args.update)

    if args.blocks:
        for k in UnicodeDB().categories:
            print("%s" % k)
        return 0

    stream = get_stream(args.file)
    if stream is None:
        exit(0)

    if args.check:
        data = exec_analysis("Contains suspected characters", args.verbose and not args.pipeline, is_latinsubs, stream)
        report["suspected"] = make_report(data, args.verbose and not args.pipeline, args.report)
        if args.wipe:
            stream = clean_latinsubs(stream, data[1])

    if args.ascii:
        data = exec_analysis("Contains only ascii characters", args.verbose and not args.pipeline, is_ascii, stream)
        report["non_ascii"] = make_report(data, args.verbose and not args.pipeline, args.report)
        if args.filter:
            stream = filter_string(stream, data[1])

    if args.zero:
        data = exec_analysis("Contains zero-width characters", args.verbose and not args.pipeline, contains_zerowidth,
                             stream)
        report["zero_width"] = make_report(data, args.verbose and not args.pipeline, args.report)
        if args.filter:
            stream = filter_string(stream, data[1])

    if args.confusables:
        data = exec_analysis("Contains confusables characters", args.verbose and not args.pipeline,
                             contains_confusables,
                             stream, args.confusables)
        report["confusables"] = make_report(data, args.verbose and not args.pipeline, args.report)
        if args.filter:
            stream = filter_string(stream, data[1])

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

    if args.save is not None:
        with open(args.save, "w", encoding="utf-8") as file:
            file.write(stream)

    if args.pipeline:
        sys.stdout.write(stream)
        sys.stdout.flush()

    exit(0)


if __name__ == "__main__":
    main()
