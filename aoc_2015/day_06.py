#!/usr/bin/env python3

import numpy as np
import re
import sys
import traceback

from common.utils import *


def solve(lines):
    grid1 = np.zeros((1000, 1000), dtype=bool)
    grid2 = np.zeros((1000, 1000), dtype=int)
    pattern = re.compile(r"(?P<action>turn on|turn off|toggle) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)")
    for line in lines:
        m = pattern.match(line)
        action = m.group("action")
        x1, y1, x2, y2 = map(int, m.groups()[1:])
        if action == "turn on":
            grid1[x1 - 1:x2, y1 - 1:y2] = True
            grid2[x1 - 1:x2, y1 - 1:y2] += 1
        elif action == "turn off":
            grid1[x1 - 1:x2, y1 - 1:y2] = False
            grid2[x1 - 1:x2, y1 - 1:y2] -= 1
            # Ensure min 0
            grid2[grid2 < 0] = 0
        elif action == "toggle":
            grid1[x1-1:x2, y1-1:y2] = np.logical_not(grid1[x1-1:x2, y1-1:y2])
            grid2[x1 - 1:x2, y1 - 1:y2] += 2
        else:
            raise ValueError(f"Bad instruction {line}")
    return np.sum(grid1), np.sum(grid2)


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test))

    result1, result2 = solve(lines)

    log.always("Part 1")
    log.always(result1)

    log.always("Part 2")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
