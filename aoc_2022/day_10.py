#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def main():
    args = parse_args()
    data = read_lines(args.input, to_list=True)

    x = 1
    cycles = 0
    next_cycle = 20
    result_1 = 0
    pixels = [[False] * 40 for _ in range(6)]
    for line in data:
        # Calculate x and cycles after current operation
        _x = x
        _cycles = cycles
        if line == "noop":
            _cycles += 1
        elif line.startswith("addx "):
            val = int(line.split(" ")[-1])
            _x += val
            _cycles += 2
        else:
            log.error(f"Bad instruction: {line}")
        # Part 1: Update signal strengths
        if _cycles >= next_cycle:
            log.debug(f"{next_cycle}: {x}")
            result_1 += next_cycle * x
            next_cycle += 40
        # Part 2: Update display
        for i in range(cycles, _cycles):
            row, col = divmod(i, 40)
            if (x - 1) <= col <= (x + 1):
                pixels[row][col] = True
        x = _x
        cycles = _cycles

    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    for row in pixels:
        log.always("".join(["▮" if v else " " for v in row]))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
