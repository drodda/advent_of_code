#!/usr/bin/env python3

import re
import sys
import traceback
from common.utils import *


RE_ABBA = re.compile(r"(.)(?!\1)(.)\2\1")


def split_ip(s):
    while "[" in s:
        head, s = s.split("[", 1)
        yield head, False
        head, s = s.split("]", 1)
        yield head, True
    yield s, False


def solve_part1(lines):
    result = 0
    for line in lines:
        include = None
        for part, in_brackets in split_ip(line):
            if RE_ABBA.search(part):
                if in_brackets:
                    include = False
                elif include is None:
                    include = True
        if include:
            result += 1
            log.info(f"Including: {line}")
        else:
            log.info(f"Excluding: {line}")

    return result


def find_aba(s):
    for i in range(len(s) - 2):
        if s[i] == s[i+2] and s[i] != s[i+1]:
            yield s[i:i+3]


def solve_part2(lines):
    result = 0
    for line in lines:
        outer_matches = set()
        inner_matches = set()
        for part, in_brackets in split_ip(line):
            for match in find_aba(part):
                if in_brackets:
                    inner_matches.add(match[1:])
                else:
                    outer_matches.add(match[:2])
        if outer_matches.intersection(inner_matches):
            log.info(f"Including {line}\t{outer_matches.intersection(inner_matches)}")
            result += 1
        else:
            log.info(f"Excluding: {line}")
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve_part1(lines)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(lines)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
