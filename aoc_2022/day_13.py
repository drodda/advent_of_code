#!/usr/bin/env python3

import ast
import functools
import itertools
import sys
import traceback
from common.utils import *


PART2_DIVIDERS = """
[[2]]
[[6]]
""".strip().splitlines()


def compare(left, right):
    """ Compare left to right
        return -1 if left is smaller, 0 if the same, 1 if larger
    """
    # Integers: compare directly
    if isinstance(left, int) and isinstance(right, int):
        return int(left > right) - int(left < right)
    # Convert any remaining integers to lists
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    # Compare matching elements
    for _left, _right in zip(left, right):
        _result = compare(_left, _right)
        if _result != 0:
            return _result
    # Compare length of lists
    return compare(len(left), len(right))


def solve_part1(data):
    result = 0
    for i, (left, right) in enumerate(data):
        _result = compare(left, right)
        if _result == -1:
            result += (i + 1)
    return result


def solve_part2(data):
    # Evaluate part 2 dividers to Python objects
    dividers = [ast.literal_eval(item) for item in PART2_DIVIDERS]
    # Merge all lines in data
    data = list(itertools.chain(*data)) + dividers
    # Sort using custom comparator
    data = sorted(data, key=functools.cmp_to_key(compare))
    # Find index of dividers
    result = 1
    for i, v in enumerate(data):
        if v in dividers:
            result *= (i + 1)
    return result


def main():
    args = parse_args()
    data = [
        # Evaluate to Python objects
        list(map(ast.literal_eval, items))
        for items in read_multilines(args.input)
    ]

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
