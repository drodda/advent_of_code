#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def priority(c):
    """ Lowercase item types a through z have priorities 1 through 26.
        Uppercase item types A through Z have priorities 27 through 52.
    """
    if c.islower():
        return ord(c) - ord("a") + 1
    if c.isupper():
        return ord(c) - ord("A") + 27
    raise ValueError(f"{c} is not letter")


def solve_part1(data):
    result = 0
    for i, item in enumerate(data):
        n = int(len(item) / 2)
        item_a = item[:n]
        item_b = item[n:]
        vals = set(item_a).intersection(item_b)
        if len(vals) == 1:
            val = vals.pop()
            log.debug(f"{i}: {item} = {val} => {priority(val)}")
            result += priority(val)
        else:
            log.error(f"ERROR: {i}: {item} Not a single duplicate {vals}")
    return result


def solve_part2(data):
    result = 0
    for i in range(0, len(data), 3):
        vals = set(data[i]).intersection(data[i + 1]).intersection(data[i + 2])
        if len(vals) == 1:
            val = vals.pop()
            log.debug(f"{i}: {val} => {priority(val)}")
            result += priority(val)
        else:
            log.error(f"ERROR: {i}: Not a single duplicate {vals}")
    return result


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)

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
