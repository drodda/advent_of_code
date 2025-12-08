#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(args):
    range_lines, ingredient_lines = read_multilines(args.input)
    ranges = []
    for range_line in range_lines:
        ranges.append(list(map(int, range_line.split("-"))))
    ingredients = list(map(int, ingredient_lines))
    return ranges, ingredients


def solve_part1(ranges, ingredients):
    result = 0
    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                result += 1
                break
    return result


def solve_part2(ranges):
    ranges = sorted(ranges)
    result = 0

    previous_end = ranges[0][0] - 1
    for start, end in ranges:
        _start, _end = start, end
        # Shift this range to not include previous range
        start = max(start, previous_end + 1)
        end = max(end, start - 1)
        result += (end - start + 1)
        previous_end = end
    return result


def main():
    args = parse_args()
    ranges, ingredients = parse_input(args)
    # log.debug(ranges, ingredients)

    log.always("Part 1:")
    result = solve_part1(ranges, ingredients)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(ranges)
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
