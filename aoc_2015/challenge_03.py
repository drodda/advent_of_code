#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


DIR_MAP = {
    "^": (0, 1),
    "v": (0, -1),
    ">": (1, 0),
    "<": (-1, 0),
}


def follow_path(path, start=(0, 0), include_start=True):
    x, y = start
    if include_start:
        yield x, y
    for step in path:
        dx, dy = DIR_MAP[step]
        x += dx
        y += dy
        yield x, y


def main():
    args = parse_args()
    data = open(data_file_path_main(test=args.test)).read().strip()

    log.always("Part 1")
    result = len(set(follow_path(data)))
    log.always(result)

    log.always("Part 2")
    explored = set(follow_path(data[::2]))
    explored = explored.union(follow_path(data[1::2]))
    result = len(explored)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
