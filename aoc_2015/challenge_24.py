#!/usr/bin/env python3

import itertools
import sys
import traceback

from common.utils import *


def solve(data, n):
    target = int(sum(data) / n)
    result = None
    for i in range(len(data)):
        log_info(f"Length: {i}")
        for vals in itertools.combinations(data, i):
            if sum(vals) == target:
                _result = 1
                for _val in vals:
                    _result *= _val
                if result is None or _result < result:
                    result = _result
        if result is not None:
            return result


def main():
    args = parse_args()
    data = read_list_int(data_file_path_main(test=args.test), to_list=True)

    log_always("Part 1")
    result = solve(data, 3)
    log_always(result)

    log_always("Part 2")
    result = solve(data, 4)
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
