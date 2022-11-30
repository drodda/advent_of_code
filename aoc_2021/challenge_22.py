#!/usr/bin/env python3
import re
import sys
import traceback
from collections import defaultdict

from common.utils import *


def parse_line(line):
    groups = re.match(r"(on|off) x=(-?[\d]+)..(-?[\d]+),y=(-?[\d]+)..(-?[\d]+),z=(-?[\d]+)..(-?[\d]+)", line).groups()
    return (
        groups[0] == "on", (
            (int(groups[1]), int(groups[2]) + 1),
            (int(groups[3]), int(groups[4]) + 1),
            (int(groups[5]), int(groups[6]) + 1),
        ),
    )


def calculate_overlap(cube_a, cube_b):
    """ Calculate the overlapping coordinates. Returns None if there is no overlap """
    (x_a_min, x_a_max), (y_a_min, y_a_max), (z_a_min, z_a_max) = cube_a
    (x_b_min, x_b_max), (y_b_min, y_b_max), (z_b_min, z_b_max) = cube_b
    x_min = max(x_a_min, x_b_min)
    x_max = min(x_a_max, x_b_max)
    y_min = max(y_a_min, y_b_min)
    y_max = min(y_a_max, y_b_max)
    z_min = max(z_a_min, z_b_min)
    z_max = min(z_a_max, z_b_max)
    if x_max <= x_min or y_max <= y_min or z_max <= z_min:
        return None
    return (x_min, x_max), (y_min, y_max), (z_min, z_max)


def calculate_size(cube):
    """ Calculate the size of a cube """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = cube
    return (x_max - x_min) * (y_max - y_min) * (z_max - z_min)


def calculate_cubes(data, limit_scope=None):
    """ Calcualate the number of cubes in data """

    # Record occurance of cubes: positive for cubes, negative is an anti-cube to cancel an overlapping cube
    cubes = defaultdict(int)
    for i, (state, cube) in enumerate(data):
        if limit_scope is not None:
            if min([c[0] for c in cube]) < -limit_scope or max([c[1] for c in cube]) > limit_scope:
                continue
        # For overlaps between this cube and existing cubes, create a cube that is the inverse of the overlap
        cubes_updates = defaultdict(int)
        for cube_b, cube_b_val in cubes.items():
            overlap = calculate_overlap(cube, cube_b)
            if overlap:
                cubes_updates[overlap] -= cube_b_val
        # Add overlaps to cubes
        for cube_b, cube_b_val in cubes_updates.items():
            cubes[cube_b] += cube_b_val
        # If this is an "On" cube add it to cubes
        if state:
            cubes[cube] += 1

    # Sum cubes: Cube size * cube value
    result = 0
    for cube, val in cubes.items():
        result += calculate_size(cube) * val
    return result


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    data = [parse_line(line) for line in lines]

    log.always("Part 1:")
    log.always(calculate_cubes(data, 50))
    log.always("Part 2:")
    log.always(calculate_cubes(data))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)

