#!/usr/bin/env python3

import math
import sys
import traceback

from common.utils import *

def parse_input(args):
    return list(read_lines(args.input))


OPERATIONS = {
    "+": sum,
    "*": math.prod,
}


def solve_part1(lines):
    operators = lines[-1].split()
    values = [list(map(int, line.split())) for line in lines[:-1]]

    result = 0
    for i, operator in enumerate(operators):
        operation = OPERATIONS[operator]
        result += operation([row[i] for row in values])
    return result


def solve_part2(lines):
    operators = lines[-1].split()
    col_ends = [i for i in range(len(lines[-1])) if lines[-1][i] != " "] + [len(lines[-1])]
    result = 0
    for i, operator in enumerate(operators):
        col_values = []
        # Get column values
        for col in range(col_ends[i], col_ends[i+1]):
            col_str = "".join([line[col] for line in lines[:-1]])
            if not col_str.isspace():
                col_values.append(int(col_str))
        operation = OPERATIONS[operator]
        result += operation(col_values)
    return result


def main():
    args = parse_args()
    lines = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(lines)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(lines)
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
