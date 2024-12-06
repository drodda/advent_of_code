#!/usr/bin/env python3

import sys
import traceback

import numpy as np

from common.utils import *



def is_safe(report):
    diff = np.diff(report)
    return (all(diff >= 1) and all(diff <= 3)) or all(diff >= -3) and all(diff <= -1)


def solve_part1(data):
    result = 0
    for report in data:
        if is_safe(report):
            result += 1
    return result


def solve_part2(data):
    result = 0
    for report in data:
        if is_safe(report):
            result += 1
        else:
            for i in range(len(report)):
                _report = report[:max(i, 0)] + report[i + 1:]
                if is_safe(_report):
                    result += 1
                    break
    return result


def main():
    args = parse_args()
    data = list(read_csv_int_multiline(args.input, sep=" ", to_list=True))

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
