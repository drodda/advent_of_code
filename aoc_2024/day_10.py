#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


TRAIL_MAX = 9


def parse_input(input_path):
    data = {}
    lines = read_lines(input_path)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            data[(x, y)] = int(c)
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


def start_points(data):
    for pos, val in data.items():
        if val == 0:
            yield pos


def explore(data, start):
    trail_ends = {start}
    for i in range(1, TRAIL_MAX + 1):
        _trail_ends = set()
        # print(trail_ends)
        for pos in trail_ends:
            for _dir in DIRECTIONS:
                _pos = move(pos, _dir)
                if data.get(_pos) == i:
                    _trail_ends.add(_pos)
        trail_ends = _trail_ends
    return len(trail_ends)


def solve_part1(data):
    result = 0
    for pos in start_points(data):
        result += explore(data, pos)
    return result


def trail_score(data, pos):
    val = data.get(pos)
    result = 0
    for _dir in DIRECTIONS:
        _pos = move(pos, _dir)
        _val = data.get(_pos)
        if _val == val + 1:
            if _val == TRAIL_MAX:
                result += 1
            else:
                result += trail_score(data, _pos)
    return result


def solve_part2(data):
    result = 0
    for pos in start_points(data):
        result += trail_score(data, pos)
    return result


def main():
    args = parse_args()
    data = parse_input(args.input)

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data)
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
