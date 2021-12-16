#!/usr/bin/env python3

import sys
import traceback

import numpy as np

from common.utils import *


DIRS = [
    np.array([1, 0]),  # Down
    np.array([0, 1]),  # Right
    np.array([-1, 0]),  # Up
    np.array([0, -1]),  # Left
]


def add_2d(c1, c2):
    """ Add 2d coordinates """
    return c1[0] + c2[0], c1[1] + c2[1]


def in_bounds_2d(c, limits):
    """ Check if coordinate c is within bounds of limits (inclusive) """
    return 0 <= c[0] <= limits[0] and 0 <= c[1] <= limits[1]


def find_best_path(grid):
    """ Use Dijkstra's algorithm to find the best path from top-left to bottom-right of grid """
    limits = add_2d(grid.shape, (-1, -1))
    start = (0, 0)
    positions_seen = {start, }
    path_heads = HeapQ([(0, start)])
    while path_heads:
        score, position = path_heads.pop()
        if position == limits:
            break
        for _dir in DIRS:
            _position = add_2d(position, _dir)
            if in_bounds_2d(_position, limits):
                _score = score + grid[_position]
                if _position == limits:
                    # Found the destination
                    return _score
                if _position not in positions_seen:
                    # Found a new optimal way to get to _position: record it and keep searching
                    positions_seen.add(_position)
                    path_heads.push((_score, _position))


def grid_part_2(grid):
    """ Construct new grid that is 5 times the size of original grid """
    repeats = 5
    _grid = np.zeros(np.array(grid.shape) * repeats, dtype=int)
    _x, _y = grid.shape
    for x in range(repeats):
        for y in range(repeats):
            _grid[x * _x:(x + 1) * _x, y * _y:(y + 1) * _y] = grid + x + y
    _grid = (_grid - 1) % 9 + 1
    return _grid


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    grid = np.array([list(map(int, line)) for line in lines], dtype=int)

    log_always("Part 1:")
    result = find_best_path(grid)
    log_always(result)

    log_always("Part 2:")
    result = find_best_path(grid_part_2(grid))
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
