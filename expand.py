#!/usr/bin/env python3

import argparse
import glob
import re
import sys

reGroup = re.compile('{[^{}]*}', re.I)


def expandBraces(entry):
    if entry is None:
        return None
    expandedEntries = []
    match = reGroup.search(entry)
    if match is not None:
        group = match.group()
        items = group[1:-1].split(',')
        for item in items:
            expanded = entry[:match.start()] + item + entry[match.end():]
            expandedEntries = expandedEntries + expandBraces(expanded)
    else:
        if entry in expandedEntries:
            expandedEntries = []
        else:
            expandedEntries = [entry]
    return expandedEntries


def get_quot(args):
    if args.single_quotes:
        quot = "'"
    elif args.double_quotes:
        quot = '"'
    else:
        quot = ''
    return quot


def get_print_out(args):
    return sys.stdout.write if args.single_line else print


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-s', '--single-line', action='store_true')
    parser.add_argument('-q', '--single-quotes', action='store_true')
    parser.add_argument('-d', '--double-quotes', action='store_true')
    parser.add_argument('-D', '--delimiter', default=' ')
    parser.add_argument('pattern', nargs='*')
    args = parser.parse_args(sys.argv[1:])
    quot = get_quot(args)
    print_out = get_print_out(args)
    for arg in args.pattern:
        i = 0
        for expanded in expandBraces(arg):
            try:
                globs = glob.glob(expanded)
            except Exception:
                globs = glob.glob(glob.escape(expanded))
            for g in globs:
                if args.single_line and i > 0:
                    sys.stdout.write(args.delimiter)
                print_out(quot + g + quot)
                i += 1
    if args.single_line:
        print()
