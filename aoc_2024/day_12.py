#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(input_path):
    data = {}
    lines = read_lines(input_path)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            data[(x, y)] = c
    return data


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


CARDINAL_DIRS = ["N", "E", "S", "W"]
DIAGONALS_DIRS = ["NE", "SE", "SW", "NW"]



def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def explore_region(data, start):
    value = data[start]
    region = {start}
    perimeter = 0
    to_explore = {start}
    while to_explore:
        pos = to_explore.pop()
        neighbours = 0
        for _dir in CARDINAL_DIRS:
            _pos = move(pos, _dir)
            if data.get(_pos) == value:
                neighbours += 1
                # More region
                if _pos not in region:
                    region.add(_pos)
                    to_explore.add(_pos)
            else:
                # Border
                perimeter += 1
    return region, perimeter


def count_sides(region):
    # Number of sides = number of corners. Find corners
    # For a corner (NE), then
    #  Neighbours (N and E) are not in the shape, or
    #  Neighbours (N and E) are in the shape and the diagonal (NE) is not in the shape
    corners = 0
    for pos in region:
        for corner_dir in DIAGONALS_DIRS:
            diagonal = move(pos, corner_dir)
            neighbours = [move(pos, _dir) in region for _dir in corner_dir]
            if not any(neighbours) or (all(neighbours) and diagonal not in region):
                log.debug(f"  Corner: {pos} {corner_dir} {neighbours}")
                # Found a corner
                corners += 1
    return corners


def solve(data):
    result_1 = 0
    result_2 = 0
    explored = set()
    for pos in data:
        if pos not in explored:
            region, perimeter = explore_region(data, pos)
            explored.update(region)
            result_1 += len(region) * perimeter
            sides = count_sides(region)
            result_2 += len(region) * sides
            log.info(f"{data[pos]} = {perimeter}, {sides}  {region}")
    return result_1, result_2


def main():
    args = parse_args()
    data = parse_input(args.input)

    result_1, result_2 = solve(data)

    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
