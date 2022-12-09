#!/usr/bin/env python3

import sys
import traceback
from common.utils import *
import numpy as np


DIRS = {
    "R": np.array([1, 0]),
    "L": np.array([-1, 0]),
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
}


def move_tail(head, tail):
    dx, dy = head - tail
    if abs(dx) >= 2 or abs(dy) >= 2:
        return tail + (np.sign(dx), np.sign(dy))
    return tail


def solve_part1(lines, rope_len):
    # Construct rope
    rope = [np.array([0, 0]) for _ in range(rope_len)]
    explored = {tuple(rope[-1]), }
    # Walk rope
    for line in lines:
        d, _n = line.split(" ")
        n = int(_n)
        for step in range(n):
            rope[0] += DIRS[d]
            for i in range(1, rope_len):
                rope[i] = move_tail(rope[i - 1], rope[i])
            explored.add(tuple(rope[-1]))
            log.debug(f"{line} {step}: {rope}")
    return len(explored)


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve_part1(lines, 2)
    log.always(result)

    log.always("Part 2:")
    result = solve_part1(lines, 10)
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
