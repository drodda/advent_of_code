#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def parse_input(input_path):
    data = read_lines(input_path, to_list=True)
    blizzards = collections.defaultdict(set)
    for y, line in enumerate(data[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c in DIRECTIONS:
                blizzards[(x, y)].add(c)
    max_y = len(data) - 2
    max_x = len(data[0]) - 2
    return (max_x, max_y), blizzards


def move_with_warp(dims, pos, _dir):
    """ Move position 1 step in given direction, warping if outside dimensions """
    return (pos[0] + DIRECTIONS[_dir][0]) % dims[0], (pos[1] + DIRECTIONS[_dir][1]) % dims[1]


def moves(dims, pos):
    """ Move position 1 step in given direction. Return valid positions in dimensions """
    for dx, dy in DIRECTIONS.values():
        _x = pos[0] + dx
        _y = pos[1] + dy
        if 0 <= _x < dims[0] and 0 <= _y < dims[1]:
            yield _x, _y


def simulate_blizzards(dims, blizzards):
    result = collections.defaultdict(set)
    for pos, dirs in blizzards.items():
        for _dir in dirs:
            _pos = move_with_warp(dims, pos, _dir)
            result[_pos].add(_dir)
    return result


def simulate(dims, blizzards, start, target):
    """ Run simulation: move from start to target """
    t = 0
    positions = [start]
    while True:
        log.info(f"Round {t}: {len(positions)} states")
        t += 1
        # Calculate blizzards next minute
        _blizzards = simulate_blizzards(dims, blizzards)
        _positions = set()
        for pos in positions:
            # Can stay if there is no blizzard
            if pos not in _blizzards:
                log.debug(f"\tNew state: {pos} (do not move)")
                _positions.add(pos)
            for _pos in moves(dims, pos):
                if _pos not in _blizzards:
                    if _pos == target:
                        # Simulate blizzards one more time to account for moving into target
                        return t + 1, simulate_blizzards(dims, _blizzards)
                    log.debug(f"\tNew state: {_pos}")
                    _positions.add(_pos)
        blizzards = _blizzards
        positions = _positions


def solve(dims, blizzards):
    start_pos = (0, -1)
    start_target = (0, 0)
    end_pos = dims[0] - 1, dims[1]
    end_target = dims[0] - 1, dims[1] - 1
    # Part 1: From start to end
    t, blizzards = simulate(dims, blizzards, start_pos, end_target)
    yield t
    # Part 2: Back to start
    _t, blizzards = simulate(dims, blizzards, end_pos, start_target)
    t += _t
    # And back to end
    _t, blizzards = simulate(dims, blizzards, start_pos, end_target)
    t += _t
    yield t


def main():
    args = parse_args()
    dims, blizzards = parse_input(args.input)

    result_1, result_2 = solve(dims, blizzards)

    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
