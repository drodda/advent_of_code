#!/usr/bin/env python3
import collections
import math
import sys
import traceback

from common.utils import *


def parse_input(input_path):
    data_str = open(input_path).read()
    return list(map(int, data_str.split()))


def num_digits(n):
    try:
        return math.floor(math.log10(n) + 1)
    except ValueError:
        return 0


def evaluate(stone):
    stone_num_digits = num_digits(stone)
    if stone == 0:
        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        yield 1
    elif stone_num_digits % 2 == 0:
        # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
        # The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone.
        # (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        _mod = int(math.pow(10, stone_num_digits / 2))
        yield from divmod(stone, _mod)
    else:
        # If none of the other rules apply, the stone is replaced by a new stone;
        # the old stone's number multiplied by 2024 is engraved on the new stone.
        yield stone * 2024


def simulate(data, iterations):
    cache = {}
    stones = collections.Counter(data)
    for step in range(iterations):
        _stones = collections.defaultdict(int)
        for stone, n in stones.items():
            if stone in cache:
                outputs = cache[stone]
            else:
                outputs = evaluate(stone)
            for output in outputs:
                _stones[output] += n
        stones = _stones
    return sum(stones.values())


def main():
    args = parse_args()
    data = parse_input(args.input)

    log.always("Part 1:")
    result = simulate(data, 25)
    log.always(result)

    log.always("Part 2:")
    result = simulate(data, 75)
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
