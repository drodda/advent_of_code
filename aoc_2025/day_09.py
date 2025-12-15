#!/usr/bin/env python3
import collections
import itertools
import sys
import traceback

from common.utils import *


def parse_input(args):
    data = []
    for line in read_lines(args.input):
        x, y = map(int, line.split(","))
        data.append((x, y))
    return data


def solve_part1(data):
    result = 0
    for i, (x1, y1) in enumerate(data):
        for x2, y2 in data[i + 1:]:
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            result = max(result, area)
    return result


def solve_part2(data):
    vertical_lines = collections.defaultdict(list)
    horizontal_lines = collections.defaultdict(list)
    for (x1, y1), (x2, y2) in itertools.pairwise(data + [data[0]]):
        if x1 == x2:
            vertical_lines[x1].append((min(y1, y2), max(y1, y2)))
        else:
            horizontal_lines[y1].append((min(x1, x2), max(x1, x2)))

    result = 0
    return result


def main():
    args = parse_args()
    data = parse_input(args)

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
