#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def array_diff(array, n=1):
    # Calculate the difference between elements of arr that are n apart
    return array[n:] - array[:-n]


def main():
    args = parse_args()
    data = np.array(read_list_int(args.input, to_list=True))

    log.always("Part 1:")
    result_1 = np.sum(array_diff(data) > 0)
    log.always(result_1)
    log.always("Part 2:")
    result_2 = np.sum(array_diff(data, 3) > 0)
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
