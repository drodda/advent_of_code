#!/usr/bin/env python3

import re
import sys
import traceback
import numpy as np

from common.utils import *


def visualise(grid):
    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            print("\u25A0" if grid[x, y] else " ", end="")
        print()


def fold(grid, axis, val):
    if axis == "x":
        grid_a = grid[:val, :]
        grid_b = np.flipud(grid[(val + 1):, :])
    else:
        grid_a = grid[:, :val]
        grid_b = np.fliplr(grid[:, (val + 1):])
    # Get size of each grid to create final grid
    x_a, y_a = grid_a.shape
    x_b, y_b = grid_b.shape
    x = max(x_a, x_b)
    y = max(y_a, y_b)
    # Add grid_a and grid_b
    grid = np.zeros([x, y], dtype=bool)
    grid[(x - x_a):, (y - y_a):] += grid_a
    grid[(x - x_b):, (y - y_b):] += grid_b
    return grid


def main():
    args = parse_args()
    points_str, folds_str = read_multilines(data_file_path_main(test=args.test))

    points = [list(map(int, line.split(","))) for line in points_str]
    x_max = max([x for x, y in points])
    y_max = max([y for x, y in points])
    grid = np.zeros([x_max + 1, y_max + 1], dtype=bool)
    for x, y in points:
        grid[x, y] = True

    for i, line in enumerate(folds_str):
        axis, val = re.match(r"fold along ([xy])=(\d+)", line).groups()
        val = int(val)
        grid = fold(grid, axis, val)
        if i == 0:
            log.always("Part 1:")
            log.always(np.sum(grid))
    log.always("Part 2:")
    visualise(grid)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
