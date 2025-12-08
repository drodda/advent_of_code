#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


DIRECTIONS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
    "NE": (1, -1),
    "SE": (1, 1),
    "SW": (-1, 1),
    "NW": (-1, -1),
}

def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def parse_input(args):
    coords = set()
    for y, line in enumerate(read_lines(args.input)):
        for x, c in enumerate(line):
            if c == "@":
                coords.add((x, y))
    return coords


def find_removable(coords):
    result = set()
    for coord in coords:
        neighbours = 0
        for _dir in DIRECTIONS:
            neighbour = move(coord, _dir)
            if neighbour in coords:
                neighbours += 1
        if neighbours < 4:
            result.add(coord)
    return result


def solve_part1(coords):
    return len(find_removable(coords))


def solve_part2(coords):
    coords = coords.copy()
    result = 0
    while True:
        removed = find_removable(coords)
        if not removed:
            break
        result += len(removed)
        coords.difference_update(removed)
    return result


def main():
    args = parse_args()
    coords = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(coords)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(coords)
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
