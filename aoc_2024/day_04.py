#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *


def rotate(data):
    for i in range(len(data[0])):
        yield "".join(row[i] for row in data)


def diagonals(data):
    n_rows = len(data)
    n_cols = len(data[0])
    for start_row in reversed(range(n_rows)):
        max_i = min(n_rows - start_row, n_cols)
        yield "".join(data[start_row + i][i] for i in range(max_i))
    for start_col in range(1, n_cols):
        max_i = min(n_rows, n_cols - start_col)
        yield "".join(data[i][start_col + i] for i in range(max_i))


def all_combinations(data):
    for line in data:
        yield line
    for line in rotate(data):
        yield line
    for line in diagonals(data):
        yield line
    for line in diagonals(list(reversed(data))):
        yield line


def solve_part1(data):
    result = 0
    for line in all_combinations(data):
        result += len(re.findall("XMAS", line))
        result += len(re.findall("XMAS"[::-1], line))
    return result


def solve_part2(data):
    n = len("MAS")
    result = 0
    for y in range(len(data) - n + 1):
        for x in range(len(data[0]) - n + 1):
            a = "".join(data[y+i][x+i] for i in range(n))
            b = "".join(data[y+n-i-1][x+i] for i in range(n))
            if (a == "MAS" or a == "SAM") and (b == "MAS" or b == "SAM"):
                result += 1
    return result


def main():
    args = parse_args()
    data = list(read_lines(args.input))

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
