#!/usr/bin/env python3
import re
import sys
import traceback

from common.utils import *


COST_A = 3
COST_B = 1


RE_BUTTON = r"Button {}: X\+(\d+), Y\+(\d+)"
RE_BUTTON_A = RE_BUTTON.format("A")
RE_BUTTON_B = RE_BUTTON.format("B")
RE_PRIZE = r"Prize: X=(\d+), Y=(\d+)"


def parse_input(input_path):
    data = []
    for block in read_multilines(input_path):
        data.append((
            list(map(int, re.fullmatch(RE_PRIZE, block[2]).groups())),  # Prize (x, y)
            list(map(int, re.fullmatch(RE_BUTTON_A, block[0]).groups())),  # Button A (x, y)
            list(map(int, re.fullmatch(RE_BUTTON_B, block[1]).groups())),  # Button B (x, y)
        ))
    return data


"""
a * x_a + b * x_b = x  # eq1
a * y_a + b * y_b = y  # eq2

a = (x - b * x_b) / x_a  # eq3: eq1 rearranged for a
a = (y - b * y_b) / y_a  # eq4: eq2 rearranged for b

(x - b * x_b) / x_a = (y - b * y_b) / y_a  # eq3 == eq4
y_a * (x - b * x_b) = x_a * (y - b * y_b)
x * y_a - b * x_b * y_a = y * x_a - b * y_b * x_a

b = (y * x_a - x * y_a) / (y_b * x_a - x_b * y_a)
a = (x - b * x_b) / x_a
"""


def solve_game(prize, button_a, button_b):
    x, y = prize
    x_a, y_a = button_a
    x_b, y_b = button_b
    b = (y * x_a - x * y_a) / (y_b * x_a - x_b * y_a)
    a = (x - b * x_b) / x_a
    if a.is_integer() and b.is_integer():
        return COST_A * int(a) + COST_B * int(b)
    return None


def solve_part1(data):
    result = 0
    for prize, button_a, button_b in data:
        _result = solve_game(prize, button_a, button_b)
        if _result is not None:
            result += _result
    return result


def solve_part2(data):
    offset = 10000000000000
    result = 0
    for (x, y), button_a, button_b in data:
        prize = (x + offset, y + offset)
        _result = solve_game(prize, button_a, button_b)
        if _result is not None:
            result += _result
    return result


def main():
    args = parse_args()
    data = parse_input(args.input)

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
