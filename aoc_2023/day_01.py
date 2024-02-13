#!/usr/bin/env python3

import string
import sys
import traceback
from common.utils import *


NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def first_digit(line, reverse=False, replace_text=False):
    """ Get first or last digit in line
        If replace_text, also search for digits as text
    """
    _line = line
    numbers = NUMBERS
    if reverse:
        _line = _line[::-1]
        numbers = {name[::-1]: v for name, v in NUMBERS.items()}
    while _line:
        if _line[0] in string.digits:
            return int(_line[0])
        if replace_text:
            for name, v in numbers.items():
                if _line.startswith(name):
                    return v
        _line = _line[1:]
    log.warning(f"No digit in {line}")
    return 0


def solve(lines, replace_text=False):
    result = 0
    for line in lines:
        log.debug(line)
        n = first_digit(line, replace_text=replace_text) * 10 + first_digit(line, reverse=True, replace_text=replace_text)
        result += n
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve(lines)
    log.always(result)

    log.always("Part 2:")
    result = solve(lines, replace_text=True)
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
