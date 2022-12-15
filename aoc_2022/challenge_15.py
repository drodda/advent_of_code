#!/usr/bin/env python3

import sys
import traceback
import re

from common.utils import *


def parse_input(test=False):
    _re = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    lines = read_lines(data_file_path_main(test=test))
    result = []
    for line in lines:
        s_x, s_y, b_x, b_y = map(int, _re.match(line).groups())
        result.append(((s_x, s_y), (b_x, b_y)))
    return result


def solve_part1(data, test=False):
    y = 10 if test else 2000000
    result = set()
    for (s_x, s_y), (b_x, b_y) in data:
        d = abs(s_x - b_x) + abs(s_y - b_y)
        dy = abs(y - s_y)
        dx = max(d - dy, 0)
        if dx >= 0:
            _result = list(range(s_x - dx, s_x + dx + 1))
            result = result.union(_result)

    # Exclude locations where a beacon is known to be present
    result = result.difference([b_x for (s_x, s_y), (b_x, b_y) in data if b_y == y])
    return len(result)


def solve_part2(data, test=False):
    max_x = max_y = 20 if test else 4000000
    for y in range(0, max_y):
        if y % 10000 == 0 and not test:
            log.info(f"Testing row {y} of {max_x}...")
        ranges = []
        for (s_x, s_y), (b_x, b_y) in data:
            d = abs(s_x - b_x) + abs(s_y - b_y)
            dy = abs(y - s_y)
            dx = max(d - dy, 0)
            if dx > 0:
                ranges.append((s_x - dx, s_x + dx))
        ranges = sorted(ranges)
        _x_max = 0
        for x_min, x_max in ranges:
            if x_min > _x_max + 1:
                return (_x_max + 1) * 4000000 + y
            _x_max = max(_x_max, x_max)


def main():
    args = parse_args()
    data = parse_input(test=args.test)

    log.always("Part 1:")
    result = solve_part1(data, test=args.test)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data, test=args.test)
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
