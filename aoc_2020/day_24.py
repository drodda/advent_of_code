#!/usr/bin/env python3

import sys
import traceback
import collections

from common.utils import *


DIRECTIONS = {
    "e": (2, 0),
    "ne": (1, 1),
    "nw": (-1, 1),
    "w": (-2, 0),
    "sw": (-1, -1),
    "se": (1, -1),
}

N_STEPS = 100


###############################################################################


def split_line(line):
    """ Split hex directions into a list of directions """
    i = 0
    while i < len(line):
        l = 1 if line[i] in ["e", "w"] else 2
        val = line[i:i+l]
        i += l
        yield val


def walk_path(steps):
    """ Convert list of directions into cartesian coordinates """
    x = 0
    y = 0
    for step in steps:
        dx, dy = DIRECTIONS[step]
        x += dx
        y += dy
    return x, y


def simulation_step(tiles):
    """ Generate new tiles based on current tiles """
    # For all neighbours of all black (True) tiles, count number of black neighbouring tiles
    tile_neighbours = collections.defaultdict(int)
    for (x, y), state in tiles.items():
        if state:
            for dx, dy in DIRECTIONS.values():
                tile_neighbours[(x+dx, y+dy)] += 1
    # For all tiles that have black neighbours, determine new state
    tiles_new = {}
    for coord, count in tile_neighbours.items():
        if tiles.get(coord, False):
            # Black
            tiles_new[coord] = not ((count == 0) or (count > 2))
        else:
            # White
            tiles_new[coord] = (count == 2)
    return tiles_new


###############################################################################


def main():
    args = parse_args()
    data_file = input_file_path_main(test=args.test)
    lines = read_lines(data_file)
    log.always("Part 1")

    tiles = collections.defaultdict(bool)
    for line in lines:
        x, y = walk_path(split_line(line))
        new_state = not tiles[(x, y)]
        tiles[(x, y)] = new_state
        log.debug(f"Tile {x},{y} flipped to {new_state}")
    log.always(sum(tiles.values()))

    log.always("Part 2")
    for i in range(N_STEPS):
        tiles = simulation_step(tiles)
        log.debug(f"Day {i+1}: {sum(tiles.values())}")
    log.always(f"{sum(tiles.values())}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
