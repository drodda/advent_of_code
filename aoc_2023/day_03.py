#!/usr/bin/env python3

import string
import sys
import traceback
from common.utils import *


SYMBOL_GEAR = "*"


def find_numbers(data):
    for y in range(len(data)):
        number_str = None
        x_start = None
        x_end = None
        for x in range(len(data[y])):
            is_digit = (data[y][x] in string.digits)
            if is_digit:
                if x_start is None:
                    number_str = ""
                    x_start = x
                number_str += data[y][x]
                x_end = x
            if x_start is not None and (not is_digit or (x == (len(data[y]) - 1))):
                yield y, x_start, x_end, int(number_str)
                # Reset
                number_str = None
                x_start = None
                x_end = None


def neighbours_symbol(data, y, x_start, x_end):
    max_y = len(data)
    max_x = len(data[0])
    for _y in range(max(y - 1, 0), min(y + 2, max_y)):
        for _x in range(max(x_start - 1, 0), min(x_end + 2, max_x)):
            if data[_y][_x] not in (string.digits + "."):
                return True


def solve_part1(data):
    result = 0
    for y, x_start, x_end, n in find_numbers(data):
        if neighbours_symbol(data, y, x_start, x_end):
            result += n
    return result


def solve_part2(data):
    result = 0
    numbers = list(find_numbers(data))
    for _y in range(len(data)):
        for _x in range(len(data[_y])):
            if data[_y][_x] == SYMBOL_GEAR:
                neighbour_count = 0
                neighbour_val = 1
                for y, x_start, x_end, n in numbers:
                    if (y - 1 <= _y <= y + 1) and (x_start - 1 <= _x <= x_end + 1):
                        neighbour_count += 1
                        neighbour_val *= n
                if neighbour_count == 2:
                    result += neighbour_val
    return result


def main():
    args = parse_args()
    data = read_lines(args.input, to_list=True)

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
