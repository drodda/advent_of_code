#!/usr/bin/env python3

import os
import re
import sys
import traceback
from collections import deque

import numpy as np

from utils import *


DIRS = [
    np.array([1, 0]),  # Down
    np.array([0, 1]),  # Right
    np.array([-1, 0]),  # Up
    np.array([0, -1]),  # Left
]


def add_2d(c1, c2):
    return c1[0] + c2[0], c1[1] + c2[1]


def in_bounds_2d(c, limits):
    return 0 <= c[0] <= limits[0] and 0 <= c[1] <= limits[1]


def find_best_path(grid):
    limits = add_2d(grid.shape, (-1, -1))
    start = (0, 0)
    best_paths = {start: 0}
    path_heads = deque([(start, 0)])
    while path_heads:
        position, score = path_heads.popleft()
        for _dir in DIRS:
            _position = add_2d(position, _dir)
            if in_bounds_2d(_position, limits):
                _score = score + grid[_position]
                if _position not in best_paths or _score < best_paths[_position]:
                    # Found a new optimal way to get to _position: record it
                    best_paths[_position] = _score
                    if _position != limits:
                        # Keep searching from that position
                        path_heads.append((_position, _score))
    return best_paths.get(limits)


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    grid = np.array([list(map(int, line)) for line in lines], dtype=int)

    log_always("Part 1:")
    result = find_best_path(grid)
    log_always(result)

    # log_always("Part 2:")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
