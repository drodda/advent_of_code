#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


DIRS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def sign(x):
    return int(x > 0) - int(x < 0)


def move_tail(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    if abs(dx) >= 2 or abs(dy) >= 2:
        return (tail[0] + sign(dx)), (tail[1] + sign(dy))
    return tail


def solve_part1(lines, rope_len):
    # Construct rope
    rope = [(0, 0) for _ in range(rope_len)]
    explored = {rope[-1], }
    # Walk rope
    for line in lines:
        d, _n = line.split(" ")
        n = int(_n)
        for step in range(n):
            rope[0] = (rope[0][0] + DIRS[d][0], rope[0][1] + DIRS[d][1])
            for i in range(1, rope_len):
                rope[i] = move_tail(rope[i - 1], rope[i])
            explored.add(rope[-1])
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
