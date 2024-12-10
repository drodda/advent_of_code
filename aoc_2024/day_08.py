#!/usr/bin/env python3
import collections
import string
import sys
import traceback

from itertools import combinations
from common.utils import *


NODES = string.ascii_letters + string.digits


def parse_input(input_path):
    result = collections.defaultdict(list)
    x = 0
    y = 0
    for y, line in enumerate(read_lines(input_path)):
        for x, c in enumerate(line):
            if c in NODES:
                result[c].append((x, y))
    return dict(result), (x + 1, y + 1)


def add(pt, delta):
    return pt[0] + delta[0], pt[1] + delta[1]


def sub(pt1, pt2):
    return pt1[0] - pt2[0], pt1[1] - pt2[1]


def in_range(pt, pt_min, pt_max):
    return pt_min[0] <= pt[0] < pt_max[0] and pt_min[1] <= pt[1] < pt_max[1]


def solve_part1(data, grid_size):
    antinodes = set()
    for sym, coords in data.items():
        for pt1, pt2 in combinations(coords, 2):
            delta = sub(pt2, pt1)
            antinodes.add(sub(pt1, delta))
            antinodes.add(add(pt2, delta))
    # Trim to nodes within grid_size
    antinodes = {pt for pt in antinodes if in_range(pt, (0, 0), grid_size)}
    return len(antinodes)


def solve_part2(data, grid_size):
    antinodes = set()
    for sym, coords in data.items():
        for pt1, pt2 in combinations(coords, 2):
            delta = sub(pt2, pt1)
            pt = pt1
            while in_range(pt, (0, 0), grid_size):
                antinodes.add(pt)
                pt = sub(pt, delta)
            pt = pt2
            while in_range(pt, (0, 0), grid_size):
                antinodes.add(pt)
                pt = add(pt, delta)
    return len(antinodes)


def main():
    args = parse_args()
    data, grid_size = parse_input(args.input)

    log.always("Part 1:")
    result = solve_part1(data, grid_size)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data, grid_size)
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
