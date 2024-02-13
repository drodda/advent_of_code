#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


DIRS = {
    "R": 1j,
    "L": -1j,
}


def solve(data):
    _dir = 1
    pos = 0
    result2 = None
    explored = {pos}
    for step in data:
        turn = step[0]
        dist = int(step[1:])
        _dir *= DIRS[turn]
        for i in range(dist):
            pos += _dir
            if pos in explored and result2 is None:
                result2 = int(abs(pos.real) + abs(pos.imag))
            explored.add(pos)
    result1 = int(abs(pos.real) + abs(pos.imag))
    return  result1, result2


def main():
    args = parse_args()
    with open(input_file_path_main(test=args.test)) as f:
        data = f.read().strip().split(", ")

    result1, result2 = solve(data)

    log.always("Part 1:")
    log.always(result1)

    log.always("Part 2:")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
