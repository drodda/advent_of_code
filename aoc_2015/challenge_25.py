#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *


def parse_input(line):
    match = re.search(f"row (\d+), column (\d+)", line)
    _row, _col = map(int, match.groups())
    return _row - 1, _col - 1


def solve(line):
    row, col = parse_input(line)
    _row = row + col
    val = int(_row * (_row + 1) / 2 + 1) + col - 1
    result = 20151125
    for i in range(val):
        result = (result * 252533) % 33554393
    return result


def main():
    args = parse_args()
    line = open(data_file_path_main(test=args.test)).read().strip()

    log.always("Part 1")
    result = solve(line)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
