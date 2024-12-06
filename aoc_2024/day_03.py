#!/usr/bin/env python3
import re
import sys
import traceback

from common.utils import *



RE_MUL= r"mul\(\d{1,3},\d{1,3}\)"
RE_DO = r"do\(\)"
RE_DONT = r"don't\(\)"
RE_MUL_DO_DONT = r"({}|{}|{})".format(RE_MUL, RE_DO, RE_DONT)
RE_PARSE_MUL = r"mul\((\d{1,3}),(\d{1,3})\)"



def solve_part1(data):
    result = 0
    for match in re.findall(RE_MUL, data):
        mul_match = re.fullmatch(RE_PARSE_MUL, match)
        if mul_match:
            v1, v2 = map(int, mul_match.groups())
            result += v1 * v2
    return result


def solve_part2(data):
    result = 0
    enabled = True
    for match in re.findall(RE_MUL_DO_DONT, data):
        if re.fullmatch(RE_DO, match):
            enabled = True
        elif re.fullmatch(RE_DONT, match):
            enabled = False
        else:
            mul_match = re.fullmatch(RE_PARSE_MUL, match)
            if mul_match and enabled:
                v1, v2 = map(int, mul_match.groups())
                result += v1 * v2
    return result


def main():
    args = parse_args()
    data = open(args.input).read().strip()

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data)
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
