#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def visualise(step, data):
    print("#" * data.shape[1])
    print(step)
    for y in range(data.shape[0]):
        print("".join(data[y, :].tolist()))
    print()
    sys.stdout.flush()


def move(data, sym):
    """ Move all sea cucumbers in data matching sym, if possible. Returns True if at least one sea cucumber moved """
    dy, dx = (0, 1) if sym == ">" else (1, 0) if sym == "v" else (0, 0)
    y_max, x_max = data.shape
    # Find elements that can move
    movers = []
    for y in range(y_max):
        for x in range(x_max):
            src = (y, x)
            if data[src] == sym:
                dest = ((y + dy) % y_max, (x + dx) % x_max)
                if data[dest] == ".":
                    movers.append((src, dest))
    # Move elements that can move
    for src, dest in movers:
        data[src] = "."
        data[dest] = sym

    return len(movers) > 0


def main():
    args = parse_args()
    lines = read_lines(args.input)
    data = np.array([list(line) for line in lines])

    if args.verbose:
        visualise("Start", data)

    i = 0
    moved = True
    while moved:
        i += 1
        moved = False
        moved |= move(data, ">")
        moved |= move(data, "v")

        if args.verbose:
            visualise(i, data)

    log.always("Part 1:")
    log.always(i)
    log.always("Part 2:")
    log.always("There is no part 2!")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)

