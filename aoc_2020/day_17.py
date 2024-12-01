#!/usr/bin/env python3

import sys
import traceback
import itertools
import collections

from common.utils import *


N_STEPS = 6


def parse_input(lines):
    result = []
    z = 0
    w = 0
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c == "#":
                result.append((x, y, z, w))
    return result


def generate_all_neighbours(data, use_w_axis=False):
    """ Calculate all neighbours for points in data
        If use_w_axis is true then 4-dimensional neighbours are calculated, otherwise 3-dimensional
    """
    neighbours_origin = generate_point_neighbours(0, 0, 0, 0, False, use_w_axis)
    neighbours_product = itertools.product(data, neighbours_origin)
    neighbours_full = [(x+dx, y+dy, z+dz, w+dw) for (x, y, z, w), (dx, dy, dz, dw) in neighbours_product]
    neighbours = sorted(list(set(neighbours_full)))
    return neighbours


def generate_point_neighbours(x, y, z, w, remove_self=True, use_w_axis=False):
    """ Calculate the neighbours of point (x,y,z,w)
        If remove_self then (x,y,z,w) is not in the output, otherwise it is
        If use_w_axis is true then 4-dimensional neighbours are calculated, otherwise 3-dimensional
    """
    x_range = range(x - 1, x + 2)
    y_range = range(y - 1, y + 2)
    z_range = range(z - 1, z + 2)
    w_range = range(w - 1, w + 2) if use_w_axis else [w]
    neighbours = set(itertools.product(x_range, y_range, z_range, w_range))
    if remove_self:
        neighbours.remove((x, y, z, w))
    return neighbours


def run_simulation(data, n_steps, use_w_axis=False, debug=False, verbose=False):
    """ Run the simulation with starting state data for n_steps
        args from argparse
        use_w_axis is true if the simulation should be 4-dimensional, otherwise 3-dimensional
    """
    for i in range(n_steps):
        data = step_simulation(data, use_w_axis)
        debug_print_state(data, i, debug, verbose)
    return len(data)


def step_simulation(data, use_w_axis=False):
    """ For a current state data, run the simulation and return a new data """

    # Count active neighbours for every point that is a neighbour to a point in data
    neighbour_count = collections.defaultdict(int)
    for x, y, z, w in data:
        for point in generate_point_neighbours(x, y, z, w, True, use_w_axis):
            neighbour_count[point] += 1

    # For each point that has active neighbours, check if it should be active in the next step
    result = []
    for point, count in neighbour_count.items():
        if step_element(point in data, count):
            result.append(point)
    return result


def step_element(state, occupied_neighbours):
    """ Check if a point currently in state (boolean) with occupied_neighbours currently occupied should be occupied """
    return (state and 2 <= occupied_neighbours <= 3) or (not state and occupied_neighbours == 3)


###############################################################################
# Utilities - print


def debug_print_state(data, step, debug=False, verbose=False):
    """ Print the current state """
    if debug or verbose:
        x_min, x_max = get_limit(data, 0)
        y_min, y_max = get_limit(data, 1)
        z_min, z_max = get_limit(data, 2)
        w_min, w_max = get_limit(data, 3)
        log.always("######################################")
        log.always(f"Step {step + 1}: {x_max - x_min} * {y_max - y_min} * {z_max - z_min} * {w_max - w_min}")
        if verbose:
            debug_print_data(data)


def debug_print_data(data):
    """ Print a graphical representation of data """
    x_min, x_max = get_limit(data, 0)
    y_min, y_max = get_limit(data, 1)
    z_min, z_max = get_limit(data, 2)
    w_min, w_max = get_limit(data, 3)
    for w in range(w_min, w_max + 1):
        for z in range(z_min, z_max+1):
            log.always(f"Z = {z}, W = {w}, origin {x_min},{y_min}:")
            for x in range(x_min, x_max + 1):
                row = [coord_to_char(data, x, y, z, w) for y in range(y_min, y_max+1)]
                log.always("".join(row))
            log.always()


def coord_to_char(data, x, y, z, w):
    """ Get value at x,y,z,w from data, convert to '#' (occupied) or '.' (unoccupied) """
    return "#" if (x, y, z, w) in data else "."


def get_limit(data, axis):
    """ Calculate the minimum and maximum value in a given axis """
    col_min = min([row[axis] for row in data])
    col_max = max([row[axis] for row in data])
    return col_min, col_max


###############################################################################


def main():
    args = parse_args()
    data_file = args.input
    lines = read_lines(data_file)
    data = parse_input(lines)

    log.always("Part 1")
    result = run_simulation(data, N_STEPS, False, args.debug, args.verbose)
    log.always(result)
    log.always("Part 2")
    result = run_simulation(data, N_STEPS, True, args.debug, args.verbose)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
