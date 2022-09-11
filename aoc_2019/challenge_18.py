#!/usr/bin/env python3

import sys
import traceback
import string
import collections
import numpy as np

from common.utils import *


def neighbours(pos):
    yield pos[0] - 1, pos[1]
    yield pos[0], pos[1] + 1
    yield pos[0] + 1, pos[1]
    yield pos[0], pos[1] - 1


def find_paths(world, start_pos):
    """ Find the shortest path from start_pos to each key it connects to, including locks passed """
    paths = {}
    path_heads = HeapQ([(0, start_pos, "")])
    explored = {start_pos, }
    while path_heads:
        cost, pos, locks = path_heads.pop()
        for _pos in neighbours(pos):
            sym = world[_pos]
            if _pos not in explored and sym in ".@" + string.ascii_letters + string.digits:
                explored.add(_pos)
                _locks = locks
                _cost = cost + 1
                if sym in string.ascii_lowercase:
                    # Found a path
                    paths[sym] = (_cost, _locks)
                else:
                    if sym in string.ascii_uppercase:
                        _locks = _locks + sym
                    path_heads.push((_cost, _pos, _locks))
    return paths


def path_slug(location, keys):
    """ Create slug from location key and possessed keys. Used to identify non-unique paths """
    keys = "".join(sorted(keys))
    return f"{location}:{keys}"


def simulate_part1(world):
    # Find all location positions, + start
    destinations = {}
    for y in range(len(world)):
        for x in range(len(world[y])):
            pos = (y, x)
            if world[pos] in "@" + string.ascii_lowercase:
                destinations[world[pos]] = pos
    all_keys = set(sorted([destination for destination in destinations if destination != "@"]))

    paths = {}
    for location, pos in destinations.items():
        paths[location] = find_paths(world, pos)

    # Dijkstra search for the shortest path to find all keys
    # Track explored paths as combination of location (current location) and found keys
    explored = set()
    path_heads = HeapQ([(0, "@", "")])
    while path_heads:
        cost, location, keys = path_heads.pop()
        # Check if all keys have been found
        if set(keys) == all_keys:
            return cost, keys
        # Check that location has not already been explored with current keys
        # Create slug from location key and possessed keys. Used to identify non-unique paths
        if path_slug(location, keys) in explored:
            continue
        explored.add(path_slug(location, keys))

        # Explore all possible locations from location
        for _location, (_path_cost, _locks) in paths[location].items():
            # Add location key to keys, if it is not already
            _keys = keys
            if _location not in _keys:
                _keys = keys + _location
            _cost = cost + _path_cost
            # Check if location can be reached with current keys
            if not set(_locks.lower()).issubset(set(keys)):
                continue
            # Continue searching from _location
            path_heads.push((_cost, _location, _keys))
    return None, None


def patch_world(world):
    """ Patch world for part 2. Use 0-3 in place of @ """
    world = world.copy()
    patch = np.array([["0", "#", "1"], ["#", "#", "#"], ["2", "#", "3"]])
    print_world(patch)
    for y in range(1, len(world) - 1):
        for x in range(1, len(world[y]) - 1):
            if world[y][x] == "@":
                world[y-1:y+2, x-1:x+2] = patch
                return world
    raise AttributeError("Entrance not found")


def simulate_part2(world):
    world = patch_world(world)
    print_world(world)

    # Find all location positions, + start
    destinations = {}
    for y in range(len(world)):
        for x in range(len(world[y])):
            pos = (y, x)
            if world[pos] in string.ascii_lowercase + string.digits:
                destinations[world[pos]] = pos

    all_keys = set(sorted([destination for destination in destinations if destination not in string.digits]))

    paths = {}
    for location, pos in destinations.items():
        paths[location] = find_paths(world, pos)

    # Dijkstra search for the shortest path to find all keys
    # Track explored paths as combination of location (current location) and found keys
    explored = set()
    path_heads = HeapQ([(0, ["0", "1", "2", "3"], "")])
    while path_heads:
        cost, locations, keys = path_heads.pop()
        # Check if all keys have been found
        if set(keys) == all_keys:
            return cost, keys
        # Check that location has not already been explored with current keys
        # Create slug from location key and possessed keys. Used to identify non-unique paths
        if path_slug(locations, keys) in explored:
            continue
        explored.add(path_slug(locations, keys))

        # Explore all possible locations from location
        for i in range(len(locations)):
            location = locations[i]
            for _location, (_path_cost, _locks) in paths[location].items():
                # Add location key to keys, if it is not already
                _keys = keys
                if _location not in _keys:
                    _keys = keys + _location
                _cost = cost + _path_cost
                # Check if location can be reached with current keys
                if not set(_locks.lower()).issubset(set(keys)):
                    continue
                # Continue searching from _location
                _locations = locations[:i] + [_location] + locations[i+1:]
                path_heads.push((_cost, _locations, _keys))
    return None, None


def print_world(world):
    for y in range(len(world)):
        log_debug("".join(world[y]))
    log_debug("")


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)

    world = np.array([[c for c in s] for s in data])
    print_world(world)

    log_always("Part 1")
    cost, keys = simulate_part1(world)
    if cost is not None:
        log_always(cost)
        log_always(keys)
    else:
        log_always("No Solution")
    log_always("")

    log_always("Part 2")
    cost, keys = simulate_part2(world)
    if cost is not None:
        log_always(cost)
        log_always(keys)
    else:
        log_always("No Solution")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
