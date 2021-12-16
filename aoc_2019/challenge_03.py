#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


DIRECTIONS = {
    # Directions as str to cartesian coordinates
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def iterate_path(path):
    """ Convert a path (list of direction and distance steps) into a sequence of coordinates starting from origin """
    x = 0
    y = 0
    yield x, y
    for step in path:
        direction = step[0]
        n = int(step[1:])
        dx, dy = DIRECTIONS[direction]
        for _ in range(n):
            x += dx
            y += dy
            yield x, y


def find_intersections(path1, path2):
    """ For paths path1 and path2 return a dictionary of common coordinates
         with key coordinate and value steps required to reach the coordinate
     """
    path1_coords = list(iterate_path(path1))
    path2_coords = list(iterate_path(path2))
    # Find coordinates common to both paths, excluding origin
    common_coords = set(path1_coords).intersection(set(path2_coords)).difference([(0, 0)])
    # Convert to a dict of {coord: sum_steps}
    common_coords_dict = {coord: path1_coords.index(coord) + path2_coords.index(coord) for coord in common_coords}
    return common_coords_dict


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    data = read_multilines(data_file)
    # Split paths into a list of steps
    data = [[s.split(",") for s in group] for group in data]

    for i, (path1, path2) in enumerate(data):
        intersections = find_intersections(path1, path2)
        closest_distance = min([abs(x) + abs(y) for x, y in intersections.keys()])
        closest_steps = min(intersections.values())
        log_always(f"Path {i}")
        log_debug(f"  {path1}")
        log_debug(f"  {path2}")
        log_always(f"  Part 1 - Closest distance: {closest_distance}")
        log_always(f"  Part 2 - Closest steps:    {closest_steps}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
