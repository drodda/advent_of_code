#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def calculate_part_1(data):
    # For constant distance-cost ideal position is median:
    position = np.sort(data)[int(np.round(data.size/2))]
    power = np.sum(np.abs(data - position))
    return power


def calculate_part_2(data):
    result = None
    for i in range(np.min(data) + 1, np.max(data)):
        distances = np.abs(data - i)
        # Power for each item is sum(1 ... n) = n(n+1)/2
        power = int(np.sum(distances * (distances + 1) / 2))
        log.verbose(f"{i}: {int(power)}")
        if result is None or power < result:
            result = power
    return result


def main():
    args = parse_args()
    data = np.array(read_csv_int(args.input, to_list=True))
    log.always("Part 1:")
    log.always(calculate_part_1(data))
    log.always("Part 2:")
    log.always(calculate_part_2(data))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
