#!/usr/bin/env python3

import sys
import traceback
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


def calculate_winning_times(_time, dist):
    # This is slow - it calculates the distance for every time between 1 and _time - 1, and compares to dist
    # Distance traveled is
    #   d = t * (_time - t)
    # or
    #   d = -t^2 + t + _time
    # Given we want to solve for when d > dist, that is equivalent to solving for
    #   -t^2 + t + _time - dist > 0
    # The points where
    #   -t^2 + t + _time - dist = 0
    # can be calculated by solving the quadratic
    result = 0
    for t in range(1, _time):
        d = t * (_time - t)
        if d > dist:
            log.debug(f"{_time}:{dist} beaten by {t} = {d}")
            result += 1
    return result


def solve(data):
    result = 1
    for _time, dist in data:
        result *= calculate_winning_times(_time, dist)
    return result


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)

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
