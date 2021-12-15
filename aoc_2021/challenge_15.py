#!/usr/bin/env python3

import os
import re
import sys
import traceback
import numpy as np

from utils import *


# def paths(grid, x, y, x_max, y_max):
#     val = grid[y][x]
#     if x == x_max and y == y_max:
#         yield [val]
#     else:
#         if x < x_max:
#             for _path in paths(grid, x + 1, y, x_max, y_max):
#                 yield [val] + _path
#         if y < y_max:
#             for _path in paths(grid, x, y + 1, x_max, y_max):
#                 yield [val] + _path
#
# DIRS = [
#     np.array([1, 0]),
#     np.array([0, 1]),
# ]
#
# def _path_gen(len):
#     if len == 0:
#         yield []
#     else:
#         for _dir in DIRS:
#             for _path in _path_gen(len - 1):
#                 yield [_dir] + _path
#
# def path_gen(len):
#     """ Calculate all possible paths to diagonal value """
#     for _path in _path_gen(len):
#         yield np.cumsum(_path, 0)
#
#
#
# def paths(len, dest):
#     for i in range(len):
#         pass
#     pass



def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    grid = np.array([list(map(int, line)) for line in lines], dtype=int)

    # CUT = 10
    # grid = grid[:CUT, :CUT]
    print(grid)

    score_best = np.zeros(grid.shape, dtype=int)
    # Fill top/left edges
    for x in range(1, grid.shape[1]):
        score_best[0, x] = score_best[0, x - 1] + grid[0, x]
    for y in range(1, grid.shape[0]):
        score_best[y, 0] = score_best[y - 1, 0] + grid[y, 0]
    # print(score_best)
    # Fill not top/left edges
    for y in range(1, grid.shape[0]):
        for x in range(1, grid.shape[1]):
            score_best[y, x] = min(score_best[y - 1, x], score_best[y, x - 1]) + grid[y, x]
    print(score_best)

    log_always("Part 1:")
    log_always(score_best[-1, -1])

    log_always("Part 2:")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
