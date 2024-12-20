#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def count_trees_in_path(lines, start_x=0, dx=3, dy=1):
    trees = 0
    line_len = len(lines[0])
    for i, y in enumerate(range(0, len(lines), dy)):
        line = lines[y]
        x = start_x + dx * i
        x_mod = x % line_len
        if line[x_mod] == "#":
            trees += 1
    return trees


PART2_STEPS = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def main():
    args = parse_args()
    lines = list(read_lines(args.input))

    log.always("Part 1:")
    log.always(count_trees_in_path(lines, 0, 3))
    log.always()

    log.always("Part 2:")
    result = 1
    for dx, dy in PART2_STEPS:
        # log.always(f"{dx}, {dy}")
        trees = count_trees_in_path(lines, 0, dx, dy)
        result = result * trees
        # log.always()
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
