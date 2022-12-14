#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


SAND_SOURCE = (500, 0)


def parse_input(test=False):
    lines = read_lines(data_file_path_main(test=test), to_list=True)
    result = []
    for line in lines:
        parts = line.split(" -> ")
        row = tuple([tuple(map(int, part.split(","))) for part in parts])
        result.append(row)
    return result


def simulate(rocks, floor=False):
    y_max = max([pos[1] for pos in rocks])
    if floor:
        y_max = y_max + 2
        dy = y_max - SAND_SOURCE[1]
        # Add a floor at y_max. As sand moves diagonally it needs to be at most (2 * dy) long
        _floor = [(x, y_max) for x in range(SAND_SOURCE[0] - dy - 1, SAND_SOURCE[0] + dy + 2)]
        rocks = rocks.union(_floor)
    sands = set()
    i = 0
    finished = False
    while not finished:
        sand_pos = SAND_SOURCE
        # Move sand until it comes to resting point
        while True:
            # Check that sand has not overflowed
            if sand_pos[1] >= y_max:
                finished = True
                break
            for _sand_pos in [(sand_pos[0], sand_pos[1] + 1), (sand_pos[0] - 1, sand_pos[1] + 1), (sand_pos[0] + 1, sand_pos[1] + 1)]:
                if _sand_pos not in sands and _sand_pos not in rocks:
                    # Move sand. Continue looping, try to move again
                    sand_pos = _sand_pos
                    break
            else:
                # Sand can not be moved any further: it has been placed in it's resting place
                break
        if not finished:
            # No possible moves exist: sand is placed at sand_pos
            sands.add(sand_pos)
            log.info(f"{i}: {sand_pos}")
            i += 1
            if sand_pos == SAND_SOURCE:
                break
    return i


def main():
    args = parse_args()
    data = parse_input(test=args.test)

    # Convert data to set of coordinates
    rocks = set()
    for row in data:
        start = row[0]
        for end in row[1:]:
            x_bounds = sorted([start[0], end[0]])
            y_bounds = sorted([start[1], end[1]])
            for x in range(x_bounds[0], x_bounds[1] + 1):
                for y in range(y_bounds[0], y_bounds[1] + 1):
                    rocks.add((x, y))
            start = end

    log.always("Part 1:")
    result = simulate(rocks)
    log.always(result)

    log.always("Part 2:")
    result = simulate(rocks, floor=True)
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
