#!/usr/bin/env python3

import sys
import traceback
import re
from collections import defaultdict

from common.utils import *


def parse_line(line):
    """ Parse a single line of input, return 2 tuples of (x, y) """
    groups = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups()
    x1, y1, x2, y2 = list(map(int, groups))
    return (x1, y1), (x2, y2)


def debug_print_data(counts_dict):
    """ Print grid of counts """
    print()
    for y in range(0, max([y for x, y in counts_dict.keys()]) + 1):
        for x in range(0, max([x for x, y in counts_dict.keys()]) + 1):
            print(counts_dict[(x, y)] or ".", end="")
        print()


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test))
    vent_count_part1 = defaultdict(int)
    vent_count_part2 = defaultdict(int)
    for line in data:
        (x1, y1), (x2, y2) = parse_line(line)
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                vent_count_part1[(x1, y)] += 1
                vent_count_part2[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                vent_count_part1[(x, y1)] += 1
                vent_count_part2[(x, y1)] += 1
        else:
            # Part 2 only:
            step_x = 1 if x2 > x1 else -1
            step_y = 1 if y2 > y1 else -1
            for i in range(abs(x2 - x1) + 1):
                vent_count_part2[(x1 + i * step_x, y1 + i * step_y)] += 1
    if args.verbose:
        debug_print_data(vent_count_part1)
        print()
        debug_print_data(vent_count_part2)
    log.always("Part 1:")
    log.always(len([coord for coord, count in vent_count_part1.items() if count >= 2]))
    log.always("Part 2:")
    log.always(len([coord for coord, count in vent_count_part2.items() if count >= 2]))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
