#!/usr/bin/env python3

import sys
import traceback
import re

from common.utils import *


def parse_input(test=False):
    """ Parse input file: return list of ((sensor x, y), (beacon x, y)) coordinates """
    _re = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
    lines = read_lines(input_file_path_main(test=test))
    result = []
    for line in lines:
        s_x, s_y, b_x, b_y = map(int, _re.match(line).groups())
        result.append(((s_x, s_y), (b_x, b_y)))
    return result


def simulate_row(data, y, sort=True):
    """ Return a list of ranges covered by known not-beacon regions for row y """
    ranges = []
    for (s_x, s_y), (b_x, b_y) in data:
        d = abs(s_x - b_x) + abs(s_y - b_y)
        dy = abs(y - s_y)
        dx = max(d - dy, 0)
        if dx > 0:
            ranges.append((s_x - dx, s_x + dx))
    if sort:
        ranges = sorted(ranges)
    return ranges


def solve_part1(data, test=False):
    y = 10 if test else 2000000
    result = 0
    ranges = simulate_row(data, y, sort=True)
    # Find total region covered by row, excluding overlaps
    x_start, x_end = ranges[0]
    for _x_start, _x_end in ranges[1:]:
        if _x_start <= x_end:
            # Range overlaps: extend current range
            x_end = max(x_end, _x_end)
        else:
            # Range does not overlap: count previous range
            result += (x_end - x_start + 1)
            x_start, x_end = _x_start, _x_end
    # Count last range
    result += (x_end - x_start + 1)

    # Exclude locations where a beacon is known to be present
    result -= len(set([b_x for (s_x, s_y), (b_x, b_y) in data if b_y == y]))
    return result


def solve_part2(data, test=False):
    max_x = max_y = 20 if test else 4000000
    for y in range(0, max_y):
        if y % 10000 == 0 and not test:
            log.info(f"Testing row {y} of {max_x}...")
        # Find where ranges for row y do not overlap
        # Assume gap is not on the edge of the region - that would be silly
        _x_max = 0
        for x_min, x_max in simulate_row(data, y, sort=True):
            if x_min > _x_max + 1:
                return (_x_max + 1) * 4000000 + y
            _x_max = max(_x_max, x_max)
            if _x_max >= max_x:
                continue


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
