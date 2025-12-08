#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(args):
    data = []
    for line in read_lines(args.input):
        values = list(map(int, line))
        data.append(values)
    return data


def solve(data, n_items):
    result = 0
    for values in data:
        value = 0
        for i in reversed(range(n_items)):
            # Find the largest digit in the head of the list, ensuring there are enough digits after
            max_digit = max(values[:(-i or None)])
            value = value * 10 + max_digit
            # Remove up to that digit from the list
            values = values[values.index(max_digit) + 1:]
        result += value

        log.info(f"{"".join(map(str, values))}: {value}")
    return result



def main():
    args = parse_args()
    data = parse_input(args)

    log.always("Part 1:")
    result = solve(data, 2)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, 12)
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
