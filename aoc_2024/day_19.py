#!/usr/bin/env python3

import functools
import sys
import traceback

from common.utils import *


def parse_input(args) -> (tuple[str, ...], str):
    towels_str, towel_combos = read_multilines(args.input)
    towels = tuple(towels_str[0].split(", "))
    return towels, towel_combos


@functools.cache
def towel_combinations(towels: tuple[str, ...], pattern: str) -> int:
    if pattern == "":
        return 1
    result = 0
    for towel in towels:
        if pattern.startswith(towel):
            tail = pattern[len(towel):]
            result += towel_combinations(towels, tail)
    return result


def solve_part1(towels: tuple[str, ...], patterns: str) -> int:
    result = 0
    for pattern in patterns:
        if towel_combinations(towels, pattern):
            result += 1
    return result


def solve_part2(towels: tuple[str, ...], patterns: str) -> int:
    result = 0
    for pattern in patterns:
        result += towel_combinations(towels, pattern)
    return result


def main():
    args = parse_args()
    towels, patterns = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(towels, patterns)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(towels, patterns)
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
