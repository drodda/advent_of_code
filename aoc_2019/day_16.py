#!/usr/bin/env python3

import math
import sys
import traceback
from collections import defaultdict
import numpy as np

from common.utils import *


BASE_PATTERN = [0, 1, 0, -1]


def to_str(arr):
    return "".join(map(str, arr))


def solve_part1(data):
    data = np.array(data)
    _len = data.shape[0]
    for r in range(100):
        _data = np.zeros(data.shape, dtype=int)
        for i in range(_len):
            pattern = np.repeat(BASE_PATTERN, i + 1)
            pattern = np.tile(pattern, max(1, math.ceil(_len / pattern.shape[0])))
            pattern = np.roll(pattern, -1)[:_len]
            _data[i] = abs(np.sum(data * pattern)) % 10
        data = _data
        log.verbose(f"{r} = {_data}")
    result = to_str(data[:8])
    return result


def solve_part2(data):
    offset = int(to_str(data[:7]))
    data = np.array((data * 10000)[offset:])
    for _ in range(100):
        for i in range(len(data) - 2, -1, -1):
            data[i] = (data[i] + data[i + 1]) % 10
    result = to_str(data[:8])
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test))

    for line in lines:
        log.info(line)
        data = list(map(int, line))

        log.always("Part 1")
        result = solve_part1(data)
        log.always(result)

        log.always("Part 2")
        result = solve_part2(data)
        log.always(result)

        log.always("")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
