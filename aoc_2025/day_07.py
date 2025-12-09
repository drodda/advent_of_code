#!/usr/bin/env python3

import collections
import sys
import traceback

from common.utils import *


def parse_input(args):
    return list(read_lines(args.input))


def solve(lines, add=False):
    start = lines[0].index("S")
    beams = {start: 1}
    splits = 0
    for i, row in enumerate(lines[1:]):
        new_beams = collections.defaultdict(int)
        for beam, count in beams.items():
            if row[beam] == "^":
                new_beams[beam - 1] += count
                new_beams[beam + 1] += count
                splits += 1
            else:
                new_beams[beam] += count
        beams = new_beams
    return splits, sum(beams.values())



def main():
    args = parse_args()
    lines = parse_input(args)
    log.debug(lines)

    result1, result2 = solve(lines)
    log.always("Part 1:")
    log.always(result1)
    log.always("Part 2:")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
