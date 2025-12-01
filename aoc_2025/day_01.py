#!/usr/bin/env python3
import operator
import sys
import traceback

from common.utils import *


def parse_input(args):
    data = list(read_lines(args.input))
    return data


OPERATIONS = {
    "R": operator.add,
    "L": operator.sub,
}


def solve(data):
    result1 = 0
    result2 = 0
    position = 50
    for instruction in data:
        direction = instruction[0]
        distance = int(instruction[1:])
        # Calculate new position
        prev = position
        result = OPERATIONS[direction](position, distance)
        position = result % 100
        # Part 1: count number of times dial ends up on 0
        if position == 0:
            result1 += 1
        # Part 2: Calculate the number of times dial passes 0
        result2 += abs(result // 100)
        if direction == "L":
            if position == 0:
                result2 += 1
            if prev == 0:
                result2 -= 1
    return result1, result2


def main():
    args = parse_args()
    data = parse_input(args)

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
