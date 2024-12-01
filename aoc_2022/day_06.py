#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def solve(data, marker_len):
    result = None
    for i in range(len(data) - marker_len + 1):
        _set = set(data[i:i + marker_len])
        if len(_set) == marker_len:
            result = i + marker_len
            break
    return result


def main():
    args = parse_args()
    data = open(args.input).read().strip()

    log.always("Part 1:")
    result = solve(data, 4)
    log.always(result)

    log.always("Part 2:")
    result = solve(data, 14)
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
