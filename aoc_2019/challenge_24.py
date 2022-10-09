#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def evolve(world, outer=None, inner=None):
    world = world.astype(int)
    world_sum = np.zeros(world.shape, dtype=int)
    world_sum[:-1, :] += world[1:, :]
    world_sum[1:, :] += world[:-1, :]
    world_sum[:, :-1] += world[:, 1:]
    world_sum[:, 1:] += world[:, :-1]
    if outer is not None:
        world_sum[0, :] += outer[1, 2]
        world_sum[-1, :] += outer[3, 2]
        world_sum[:, 0] += outer[2, 1]
        world_sum[:, -1] += outer[2, 3]
    if inner is not None:
        world_sum[1][2] += np.sum(inner[0, :])
        world_sum[3][2] += np.sum(inner[-1, :])
        world_sum[2][1] += np.sum(inner[:, 0])
        world_sum[2][3] += np.sum(inner[:, -1])
    result = (world_sum == 1) + ((world_sum == 2) * (world == 0))
    return result


WORLD_HASH_KERNEL = np.reshape([pow(2, i) for i in range(5 * 5)], (5, 5))


def calculate_world_hash(world):
    return np.sum(world * WORLD_HASH_KERNEL)


def print_world(world):
    for row in world:
        print("".join(["#" if v else "." for v in row]))


def solve_part1(world, verbose=False):
    world_hash = calculate_world_hash(world)

    if verbose:
        print(f"0: {world_hash}")
        print_world(world)
        print()

    i = 0
    seen = {calculate_world_hash(world)}
    while True:
        world = evolve(world)
        world_hash = calculate_world_hash(world)
        i += 1
        if verbose:
            print(f"{i}: {world_hash}")
            print_world(world)
            print()
        if world_hash in seen:
            return world_hash
        seen.add(world_hash)


def print_worlds(i, worlds):
    print("################")
    print(f"Time: {i}")
    for level, world in worlds.items():
        print(f"Level: {level}")
        print_world(world)
        print()
    print()


def solve_part2(world, iterations, verbose=False):
    worlds = {0: world}
    if verbose:
        print_worlds(0, worlds)

    for i in range(iterations):
        # Calculate new worlds to evolve: each existing world +/- 1
        levels = set()
        for level in worlds.keys():
            levels.add(level - 1)
            levels.add(level)
            levels.add(level + 1)
        # Evolve each world
        _worlds = {}
        for level in sorted(levels):
            world = worlds.get(level, np.zeros([5, 5]))
            _world = evolve(world, worlds.get(level - 1), worlds.get(level + 1))
            # Clobber middle square as it is represented by another world
            _world[2, 2] = False
            # Only keep evolved world if there is anything in it
            if np.sum(_world):
                _worlds[level] = _world
        # Replace worlds
        worlds = _worlds
        if verbose:
            print_worlds(0, worlds)
    result = sum([np.sum(world) for world in worlds.values()])
    return result


def main():
    args = parse_args()
    verbose = (args.verbose >= 2)
    data_raw = [list(line) for line in read_lines(data_file_path_main(test=args.test))]
    world = np.array(data_raw) == "#"

    log_always("Part 1:")
    result = solve_part1(world, verbose=verbose)
    log_always(result)

    log_always("Part 2:")
    iterations = 10 if args.test else 200
    result = solve_part2(world, iterations, verbose=verbose)
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
