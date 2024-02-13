#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def get_row(grid, n):
    return grid[n]


def get_col(grid, n):
    return [row[n] for row in grid]


def compare(lst1, lst2):
    _len = min(len(lst1), len(lst2))
    return _len - sum([lst1[i] == lst2[i] for i in range(_len)])


def find_reflection(grid, grid_selector, grid_len, expected_errors=0):
    for i in range(grid_len - 1):
        errors = 0
        for j in range(min(i + 1, grid_len - i - 1)):
            _errors = compare(grid_selector(grid, i - j), grid_selector(grid, i + j + 1))
            errors += _errors
        if errors == expected_errors:
            return i + 1
    return 0


def solve(data, expected_errors=0):
    result = 0
    for i, grid in enumerate(data):
        _result = find_reflection(grid, get_col, len(grid[0]), expected_errors) + 100 * find_reflection(grid, get_row, len(grid), expected_errors)
        log.info(f"{i}: {_result}")
        result += _result
    return result


def main():
    args = parse_args()
    data = list(read_multilines(input_file_path_main(test=args.test)))

    log.always("Part 1:")
    result = solve(data)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, expected_errors=1)
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
