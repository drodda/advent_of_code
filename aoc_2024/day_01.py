#!/usr/bin/env python3

import collections
import sys
import traceback

from common.utils import *


def parse(input_path):
    lines = list(read_lines(input_path))
    left = [int(line.split()[0]) for line in lines]
    right = [int(line.split()[1]) for line in lines]
    return left, right


def solve_part1(left, right):
    result = 0
    for v1, v2 in zip(sorted(left), sorted(right)):
        result += abs(v2 - v1)
    return result


def solve_part2(left, right):
    right_counter = collections.Counter(right)
    result = 0
    for v in left:
        result += v * right_counter.get(v, 0)
    return result


def main():
    args = parse_args()
    left, right = parse(args.input)

    log.always("Part 1:")
    result = solve_part1(left, right)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(left, right)
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
