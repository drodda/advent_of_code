#!/usr/bin/env python3

import sys
import traceback

from common.utils import *

TARGET_SUM = 2020


def main():
    args = parse_args()
    data = list(read_list_int(args.input))

    log.always("Part 1:")
    for i, x in enumerate(data):
        for j, y in enumerate(data[i+1:]):
            if x + y == TARGET_SUM:
                log.always(f"Candidate: {x} * {y} = {x*y}")

    log.always("Part 2:")
    for i, x in enumerate(data):
        for j, y in enumerate(data[i+1:]):
            for k, z in enumerate(data[j + 1:]):
                if x + y + z == TARGET_SUM:
                    log.always(f"Candidate: {x} * {y} * {z} = {x*y*z}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
