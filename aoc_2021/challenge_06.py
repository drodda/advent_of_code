#!/usr/bin/env python3

import os
import sys
import traceback
import numpy as np

from utils import *


SPAWN_FIRST = 9
SPAWN_NEXT = 7


def calculate_part_1(data, n_days):
    # Calculate the number of fish spawned (self + children) by a fish spawned for each day, in reverse
    # Count up to -SPAWN_FIRST days, as existing fish were spawned in the past
    fish_spawned_per_day = {}
    for i in range(n_days, -SPAWN_FIRST, -1):
        count = 1
        for j in range(i + SPAWN_FIRST, n_days, SPAWN_NEXT):
            count += fish_spawned_per_day[j]
        fish_spawned_per_day[i] = count
    # Sum the fish spawned from each fish in input
    result = 0
    for v in data:
        result += fish_spawned_per_day[v - SPAWN_FIRST]
    return result


def main():
    args = parse_args()
    data = np.array(list(map(int, open(data_file_path_main(test=args.test)).read().strip().split(","))))
    log_always("Part 1:")
    log_always(calculate_part_1(data, 80))
    log_always("Part 2:")
    log_always(calculate_part_1(data, 256))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
