#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(args):
    data = read_multilines(args.input)
    keys = []
    locks = []
    for lines in data:
        value = [0] * len(lines[0])
        sym = lines[0][0]
        for i, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == sym:
                    # Measure distance to bottom
                    # For locks ths is the height remaining
                    # For keys this is the key height
                    value[x] = len(lines) - i - 1
        if sym == "#":
            locks.append(value)
        else:
            keys.append(value)
    return locks, keys


def solve_part1(locks, keys):
    result = 0
    for lock in locks:
        for key in keys:
            if all([lock[i] - key[i] >= 0 for i in range(len(lock))]):
                result += 1
    return result


def main():
    args = parse_args()
    locks, keys = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(locks, keys)
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
