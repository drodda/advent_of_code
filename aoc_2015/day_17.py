#!/usr/bin/env python3

import itertools
import sys
import traceback

from common.utils import *


def solve(volumes, total):
    result_1 = 0
    result_2 = 0
    min_containers = None
    for i in range(1, len(volumes)):
        for combination in itertools.combinations(volumes, i):
            if sum(combination) == total:
                log.debug(f"Solution: {combination}")
                result_1 += 1
                if min_containers is None:
                    min_containers = i
                if i == min_containers:
                    result_2 += 1
    return result_1, result_2


def main():
    args = parse_args()
    volumes = read_list_int(args.input, to_list=True)

    total = 25 if args.test else 150

    result_1, result_2 = solve(volumes, total)

    log.always("Part 1")
    log.always(result_1)

    log.always("Part 2")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
