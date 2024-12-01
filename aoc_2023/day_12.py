#!/usr/bin/env python3

import functools
import sys
import traceback
from common.utils import *


@functools.cache
def calculate_solutions(pattern, sets, current_set_position=0):
    if not pattern:
        if not sets and not current_set_position:
            return 1
        return 0
    result = 0
    if pattern[0] in ["#", "?"]:
        # Extend current set
        result += calculate_solutions(pattern[1:], sets, current_set_position + 1)
    if pattern[0] in [".", "?"]:
        if current_set_position:
            # Close current set if it is finished
            if sets and sets[0] == current_set_position:
                result += calculate_solutions(pattern[1:], sets[1:])
        else:
            # Not in a set: move on to next symbol
            result += calculate_solutions(pattern[1:], sets)
    return result


def solve(lines, repeats=1):
    result = 0
    for line in lines:
        pattern, sets_str = line.split()
        # Extend pattern and sets by repeats
        pattern = "?".join((pattern, ) * repeats) + "."
        sets = tuple(list(map(int, sets_str.split(","))) * repeats)
        _result = calculate_solutions(pattern, sets)
        log.info(f"{pattern}, {sets} = {_result}")
        result += _result
    return result


def main():
    args = parse_args()
    lines = read_lines(args.input, to_list=True)

    log.always("Part 1:")
    result = solve(lines)
    log.always(result)

    log.always("Part 2:")
    result = solve(lines, repeats=5)
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
