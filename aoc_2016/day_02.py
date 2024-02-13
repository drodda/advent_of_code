#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


DIRS = {
    "U": -1j,
    "R": 1,
    "D": 1j,
    "L": -1,
}


KEYPAD_1 = ["123", "456", "789"]
KEYPAD_2 = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]


def solve(lines, keypad_text):
    # Convert keypad to complex dictionary
    keypad = {
        (x + y * 1j): c
        for y, line in enumerate(keypad_text)
        for x, c in enumerate(line)
        if c != " "
    }
    # Find start position
    pos = {v: k for k, v in keypad.items()}["5"]
    result = ""
    for line in lines:
        for c in line:
            _pos = pos + DIRS[c]
            if _pos in keypad:
                pos = _pos
        result += keypad[pos]
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve(lines, KEYPAD_1)
    log.always(result)

    log.always("Part 2:")
    result = solve(lines, KEYPAD_2)
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
