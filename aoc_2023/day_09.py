#!/usr/bin/env python3

import sys
import traceback

import numpy as np

from common.utils import *


def calculate_next(lst, reverse=False):
    index = 0 if reverse else -1
    diffs = []
    _lst = np.array(lst)
    while np.any(_lst):
        _lst = np.diff(_lst)
        diffs.append(_lst[index])
    result = lst[index]
    if reverse:
        for i, v in enumerate(diffs):
            result -= v * (1 if (i % 2 == 0) else -1)
    else:
        result += sum(diffs)
    return result


def solve(data, reverse=False):
    result = 0
    for i, _lst in enumerate(data):
        _result = calculate_next(_lst, reverse=reverse)
        log.info(f"{i} = {_result}")
        result += _result
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)
    data = [list(map(int, line.split())) for line in lines]

    log.always("Part 1:")
    result = solve(data)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, reverse=True)
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
