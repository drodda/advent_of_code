#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def calculate_paper(dims):
    l, w, h = dims
    lw = l * w
    lh = l * h
    wh = w * h
    slack = min(lw, lh, wh)
    return 2 * (lw + lh + wh) + slack


def calculate_ribon(dims):
    l, w, h = dims
    dims = sorted(dims)
    return 2 * (dims[0] + dims[1]) + l * w * h


def main():
    args = parse_args()
    data = read_lines(args.input)

    result_1 = 0
    result_2 = 0
    for line in data:
        dims = list(map(int, line.split("x")))
        result_1 += calculate_paper(dims)
        result_2 += calculate_ribon(dims)

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
