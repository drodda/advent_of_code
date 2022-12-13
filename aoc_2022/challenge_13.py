#!/usr/bin/env python3

from functools import cmp_to_key
import itertools
import sys
import traceback
from common.utils import *


PART2_DIVIDERS = [
    "[[2]]",
    "[[6]]",
]


def in_order(left, right):
    result = None
    if isinstance(left, int) and isinstance(right, int):
        if left != right:
            result = left < right
    else:
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]

        for _left, _right in zip(left, right):
            _result = in_order(_left, _right)
            if _result is not None:
                result = _result
                break
        if result is None:
            if len(left) != len(right):
                result = len(left) < len(right)
    return result


def solve_part1(data):
    result = 0
    for i, (_left, _right) in enumerate(data):
        # Convert to Python objects
        left = eval(_left)
        right = eval(_right)
        _result = in_order(left, right)
        if _result:
            result += (i + 1)
    return result


def solve_part2(data):
    def comparator(x, y):
        _result = in_order(x, y)
        if _result is True:
            return 1
        elif _result is None:
            return 0
        else:
            return -1

    # Convert part 2 divisors to Python objects
    divisors = [eval(item) for item in PART2_DIVIDERS]
    # Merge all lines in data, convert to Python objects
    data = [eval(item) for item in itertools.chain(*data)] + divisors
    # Sort
    data = sorted(data, key=cmp_to_key(comparator), reverse=True)
    # Find index of divisors
    result = 1
    for i, v in enumerate(data):
        if v in divisors:
            result *= (i + 1)
    return result


def main():
    args = parse_args()
    data = list(read_multilines(data_file_path_main(test=args.test)))

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
