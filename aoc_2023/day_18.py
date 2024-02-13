#!/usr/bin/env python3

import collections
import sys
import time
import traceback
from common.utils import *


DIRS = {
    "U": -1j,
    "R": 1+0j,
    "D": 1j,
    "L": -1+0j,
}


HEX_DIRS = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


def parse_part1(lines):
    return [(_dir, int(dist_str)) for _dir, dist_str, _ in [line.split() for line in lines]]


def parse_part2(lines):
    return [(HEX_DIRS[val[7]], int(int(val[2:7], 16))) for _, _, val in [line.split() for line in lines]]


def solve(data):
    pos = 0
    area = 0
    perimeter = 0
    for _dir, _dist in data:
        _pos = pos + DIRS[_dir] * _dist
        area += 0.5 * (_pos.real * pos.imag - _pos.imag * pos.real)
        perimeter += _dist
        pos = _pos
    return int(abs(area) + perimeter / 2 + 1)


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve(parse_part1(lines))
    log.always(result)

    log.always("Part 2:")
    result = solve(parse_part2(lines))
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
