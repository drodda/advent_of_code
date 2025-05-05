#!/usr/bin/env python3
import collections
import functools
import sys
import traceback

from common.utils import *


def parse_input(args):
    data = list(map(int, read_lines(args.input)))
    return data

SECRET_NUMBER_STEPS = [
    # Multiply by 64
    lambda n: n << 6,
    # Divide by 32
    lambda n: n >> 5,
    # Multiply by 2048
    lambda n: n << 11,
]


def next_secret_number(secret_number):
    """Calculate the next sequence number for a given secret number"""
    for op in SECRET_NUMBER_STEPS:
        secret_number = secret_number ^ op(secret_number)
        secret_number = secret_number % 16777216
    return secret_number


def calculate_secret_numbers(secret_number, n):
    """Generate the next n secret numbers"""
    for _ in range(n):
        secret_number = next_secret_number(secret_number)
        yield secret_number


def solve_part1(data):
    result = 0
    for secret_number in data:
        *_, secret_number = calculate_secret_numbers(secret_number, 2000)
        result += secret_number
    return result


def calculate_price_sequences(secret_number, n):
    """Generate the first n price delta sequences"""
    old_price = secret_number % 10
    price_deltas = tuple()
    for secret_number in calculate_secret_numbers(secret_number, n):
        price = secret_number % 10
        price_delta = price - old_price
        price_deltas = price_deltas[-3:] + (price_delta, )
        if len(price_deltas) == 4:
            yield price_deltas, price
        old_price = price


def solve_part2(data):
    results = collections.defaultdict(int)
    for secret_number in data:
        seen = set()
        for price_deltas, price in calculate_price_sequences(secret_number, 2000):
            if price_deltas not in seen:
                results[price_deltas] += price
                seen.add(price_deltas)
    return max(results.values())


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
