#!/usr/bin/env python3
import math
import sys
import traceback

from common.utils import *


def parse_input(args):
    with open(args.input) as f:
        pairs = f.read().split(",")
    data = []
    for pair in pairs:
        a, b = pair.split("-")
        data.append((int(a), int(b)))
    return data


def find_invalid(start, end, max_repeats=None):
    """Find all invalid values that contain repeated digits between start and end with at least min_digits repeated"""
    start_digits = len(str(start))
    end_digits = len(str(end))

    if max_repeats is not None:
        repeats = [max_repeats]
    else:
        repeats = list(range(2, end_digits + 1))

    invalid_numbers = set()
    for sequence_digits in range(1, end_digits + 1):
        for repeat in repeats:
            if sequence_digits * repeat > end_digits:
                continue
            for digits in range(max(start_digits, 2), end_digits + 1):
                if digits % sequence_digits == 0:
                    log.debug(f"    can be made up of {digits} * {repeat}")
                    # It is possible to make up a number with 'digits' repeated 'repeat' times
                    # Try to find possible sequences that match those criteria
                    modulo = 10 ** sequence_digits
                    sequence_start = max(start // (modulo ** (repeat - 1)), modulo // 10)
                    sequence_end = min(end // (modulo ** (repeat - 1)), modulo - 1)
                    for sequence in range(sequence_start, sequence_end + 1):
                        invalid_number = int(str(sequence) * repeat)
                        if start <= invalid_number <= end:
                            invalid_numbers.add(invalid_number)
    return sorted(invalid_numbers)


def solve_part1(data):
    result = 0
    for start, end in data:
        log.info(f"  {start}-{end}:")
        for value in find_invalid(start, end, max_repeats=2):
            log.info(f"    {value}")
            result += value
    return result


def solve_part2(data):
    result = 0
    for start, end in data:
        log.info(f"  {start}-{end}:")
        for value in find_invalid(start, end):
            log.info(f"    {value}")
            result += value
    return result


def main():
    args = parse_args()
    data = parse_input(args)

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
