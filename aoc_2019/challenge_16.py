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


def run_simulation(data):
    _len = data.shape[0]
    for r in range(100):
        _data = np.zeros(data.shape, dtype=int)
        for i in range(_len):
            pattern = np.repeat(BASE_PATTERN, i + 1)
            pattern = np.tile(pattern, max(1, math.ceil(_len / pattern.shape[0])))
            pattern = np.roll(pattern, -1)[:_len]
            _data[i] = abs(np.sum(data * pattern)) % 10
        data = _data
        log_verbose(f"{r} = {_data}")
    return data


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))


    for line in lines:
        log_info(line)
        log_always("Part 1")
        data = np.array(list(map(int, line)))
        result = to_str(run_simulation(data))  # [:8]
        log_always(result)

        log_always("Part 2")
        offset = int(to_str(data[:7]))
        print(offset)
        _len = data.shape[0]
        offset = offset % _len
        print(offset)
        result = to_str(np.roll(data, -offset)[:8])
        print(result)
        # data = np.tile(data, max(1, math.ceil(800 / _len)))
        # result = run_simulation(data)
        # log_always(result)

        print()



    # log_always(cost)
    # log_always("Part 2")
    # log_always(qtty_best)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
