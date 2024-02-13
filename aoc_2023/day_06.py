#!/usr/bin/env python3
import math
import sys
import traceback
from contextlib import suppress

from common.utils import *


def parse_input_part1(lines):
    if len(lines) != 2:
        log.error(f"Bad input - expected 2, got {len(lines)} lines")
    times = list(map(int, lines[0].split()[1:]))
    dists = list(map(int, lines[1].split()[1:]))
    if len(times) != len(dists):
        log.error(f"Bad input - got uneven lengths")
    return [
        (times[i], dists[i]) for i in range(len(times))
    ]


def parse_input_part2(lines):
    if len(lines) != 2:
        log.error(f"Bad input - expected 2, got {len(lines)} lines")
    return [
        (
            int("".join(lines[0].split()[1:])),
            int("".join(lines[1].split()[1:])),
        )
    ]


def solve_quadratic(a, b, c):
    with suppress(ValueError):
        p = math.sqrt(pow(b, 2) - 4 * a * c)
        yield (-b - p) / (2 * a)
        yield (-b + p) / (2 * a)


def calculate_winning_times(_time, dist):
    # Distance traveled is
    #   d = t * (_time - t)
    # or
    #   d = -t^2 + t + _time
    # Given we want to solve for when d > dist, that is equivalent to solving for
    #   -t^2 + t + _time - dist > 0
    # The points where
    #   -t^2 + t + _time - dist = 0
    # can be calculated by solving the quadratic
    end, start = solve_quadratic(-1, _time, -1 * dist)
    # Results of solving quadratic are fractional values - round inward to the nearest whole number
    _end = math.floor(end)
    if _end == end:
        # If the zero crossing is an exact integer then the travelled distance equals but does not beat dist: skip
        _end -= 1
    _start = math.ceil(start)
    result = _end - _start + 1
    return result


def solve(data):
    result = 1
    for _time, dist in data:
        result *= calculate_winning_times(_time, dist)
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    data_part1 = parse_input_part1(lines)
    log.debug(data_part1)
    log.always("Part 1:")
    result = solve(data_part1)
    log.always(result)

    data_part2 = parse_input_part2(lines)
    log.debug(data_part2)
    log.always("Part 2:")
    result = solve(data_part2)
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
