#!/usr/bin/env python3
import re
import sys
import traceback
from common.utils import *


def parse_input(lines):
    for line in lines:
        a, b, x, y = map(int, re.split(r"[\-,]", line))
        yield (a, b), (x, y)


def contains(v1, v2):
    return v2[0] >= v1[0] and v2[1] <= v1[1]


def overlaps(v1, v2):
    return v1[0] <= v2[0] <= v1[1] or v1[0] <= v2[1] <= v1[1]


def solve(data):
    result_1 = 0
    result_2 = 0
    for i, (v1, v2) in enumerate(data):
        if contains(v1, v2) or contains(v2, v1):
            log.debug(f"Contained: {i} = {v1} {v2}")
            result_1 += 1
        if overlaps(v1, v2) or overlaps(v2, v1):
            log.debug(f"Overlaps: {i} = {v1} {v2}")
            result_2 += 1
    return result_1, result_2


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    data = list(parse_input(lines))

    result_1, result_2 = solve(data)

    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
