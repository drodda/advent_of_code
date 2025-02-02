#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(args):
    data = [tuple(map(int, line.split(","))) for line in read_lines(args.input)]
    return data


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def in_range(pos, grid_size):
    return (0 <= pos[0] <= grid_size) and (0 <= pos[1] <= grid_size)


def shortest_path(blocks, grid_size):
    path_heads = {(0, 0), }
    end = (grid_size, grid_size)
    explored = set()
    result = 0
    while path_heads:
        result += 1
        _path_heads = set()
        for pos in path_heads:
            for _dir in DIRECTIONS:
                _pos = move(pos, _dir)
                if _pos == end:
                    return result
                if in_range(_pos, grid_size) and _pos not in blocks and _pos not in explored:
                    _path_heads.add(_pos)
                    explored.add(_pos)
        path_heads = _path_heads
    return None


def solve_part1(data, test=False):
    grid_size = 6 if test else 70
    steps = 12 if test else 1024
    blocks = data[:steps]
    return shortest_path(blocks, grid_size)


def solve_part2(data, test=False):
    grid_size = 6 if test else 70
    blocks = set()
    for block in data:
        blocks.add(block)
        # Check if there is a path from start to end
        if shortest_path(blocks, grid_size) is None:
            return ",".join(map(str, block))
    return None


def main():
    args = parse_args()
    data = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(data, args.test)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data, args.test)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
