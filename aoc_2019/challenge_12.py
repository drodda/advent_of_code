#!/usr/bin/env python3

import sys
import re
import traceback
import numpy as np

from utils import *


def step_axis(coords, velocities):
    """ Run simulation for a single axis coordinates and velocities """
    for i in range(len(coords)):
        velocities[i] += np.sum(np.sign(coords - coords[i]))
    coords += velocities


def simulate(positions, rounds):
    """ Run simulation for rounds steps. Return position and velocity matrices """
    positions = np.array(positions)
    velocities = np.zeros(positions.shape, dtype=positions.dtype)
    for axis in range(3):
        for i in range(rounds):
            step_axis(positions[:, axis], velocities[:, axis])
    return positions, velocities


def calculate_energy(positions, velocities):
    """ Calculate energy (part 1) for given positions and velocities """
    return np.sum(np.sum(np.abs(positions), 1) * np.sum(np.abs(velocities), 1))


def simulate_until_repeat(axis_coords):
    """ Run simulation for a single axis until simulation repeats. Return number of cycles until repeat """
    axis_coords = np.array(axis_coords)
    coords_original = axis_coords.copy()
    velocities = np.zeros(axis_coords.shape, dtype=axis_coords.dtype)
    i = 0
    while True:
        step_axis(axis_coords, velocities)
        i += 1
        if np.all(axis_coords == coords_original) and np.all(velocities == 0):
            break
    return i


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    positions = []
    for line in lines:
        groups = re.match(r"<x=(-?[\d]+), y=(-?[\d]+), z=(-?[\d]+)>", line).groups()
        position = list(map(int, groups))
        positions.append(position)

    log_always("Part 1")
    rounds = 100 if args.test else 1000
    _positions, _velocities = simulate(positions, rounds)
    log_always(calculate_energy(_positions, _velocities))

    log_always("Part 2")
    repeat = [simulate_until_repeat([position[i] for position in positions]) for i in range(3)]
    result = np.lcm.reduce(repeat)
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
