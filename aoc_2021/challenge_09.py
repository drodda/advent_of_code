#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


# Coordinates system:
#   * y horizontal, starting at the left
#   * x vertical, starting at the top
#   * (0,0) is top-left.


def neighbours(point, dimensions):
    """ Return cartesian neighbours of point (x,y), taking into account bounds (0,0) and dimensions (x_max,y_max) """
    x, y = point
    x_max, y_max = dimensions
    if y > 0:
        yield x, y - 1
    if y < (y_max - 1):
        yield x, y + 1
    if x > 0:
        yield x - 1, y
    if x < (x_max - 1):
        yield x + 1, y


def find_low_points(data):
    """ Find all low points: lower than all surrounding points. Returns a list of (x, y) coordinates """
    def _is_low_point(pt):
        val = data[pt]
        for _pt in neighbours(pt, data.shape):
            if val >= data[_pt]:
                return False
        return True
    x_max, y_max = data.shape
    low_points = []
    for x in range(x_max):
        for y in range(y_max):
            if _is_low_point((x, y)):
                low_points.append((x, y))
    return low_points


def calculate_basin_size(data, point):
    """ Count the number of points surrounded (x, y) that are not '9' """
    # Keep track of set of points in the basin
    basin_points = set()

    def _basin_search(pt):
        if data[pt] == 9:
            return
        if pt in basin_points:
            return
        basin_points.add(pt)
        # Recurse to cartesian neighbours of _x, _y
        for _pt in neighbours(pt, data.shape):
            _basin_search(_pt)
    _basin_search(point)
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
        basin_size = calculate_basin_size(data, (x, y))
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
