#!/usr/bin/env python3

import os
import sys
import traceback
import numpy as np

from utils import *


# Coordinates system:
#   * y horizontal, starting at the left
#   * x vertical, starting at the top
#   * (0,0) is top-left.


def find_low_points(data):
    """ Find all low points: lower than all surrounding points. Returns a list of (x, y) coordinates """
    x_max, y_max = data.shape
    low_points = []
    for x in range(x_max):
        for y in range(y_max):
            val = data[x, y]
            if y > 0 and val >= data[x, y - 1]:
                continue
            if y < (y_max - 1) and val >= data[x, y + 1]:
                continue
            if x > 0 and val >= data[x - 1, y]:
                continue
            if x < (x_max - 1) and val >= data[x + 1, y]:
                continue
            low_points.append((x, y))
    return low_points


def calculate_basin_size(data, x, y):
    """ Count the number of points surrounded (x, y) that are not '9' """
    x_max, y_max = data.shape
    # Keep track of set of points in the basin
    basin_points = set()

    def _basin_search(_x, _y):
        if data[_x, _y] == 9:
            return
        if (_x, _y) in basin_points:
            return
        basin_points.add((_x, _y))
        # Recurse to cartesian neighbours of _x, _y
        if _x > 0:
            _basin_search(_x - 1, _y)
        if _x < x_max - 1:
            _basin_search(_x + 1, _y)
        if _y > 0:
            _basin_search(_x, _y - 1)
        if _y < y_max - 1:
            _basin_search(_x, _y + 1)
    _basin_search(x, y)
    return len(basin_points)


def main():
    args = parse_args()
    data_raw = read_lines(data_file_path_main(test=args.test))
    data = np.array([list(map(int, list(line))) for line in data_raw])

    log_always("Part 1:")
    low_points = find_low_points(data)
    result = len(low_points) + sum([data[x, y] for x, y in low_points])
    log_always(result)

    log_always("Part 2:")
    basin_sizes = [0] * len(low_points)
    for i, (x, y) in enumerate(low_points):
        basin_size = calculate_basin_size(data, x, y)
        basin_sizes[i] = basin_size
        log_info(f"{x},{y}: {basin_size}")

    basin_sizes = sorted(basin_sizes, reverse=True)
    log_always(np.product(basin_sizes[:3]))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
