#!/usr/bin/env python3

import os
import sys
import traceback
from collections import Counter

from utils import *


SPAWN_FIRST = 9
SPAWN_NEXT = 7


def parse_data(data, n):
    """ Parse input data, return a list of counts of fish on each day of their spawn cycle """
    counter = Counter(data)
    fish = [counter.get(i, 0) for i in range(n)]
    return fish


def run_sim(fish_count, n_days):
    """ Run simulation for n_days, return state """
    assert(len(fish_count) == SPAWN_FIRST)
    for i in range(n_days):
        new = fish_count[0]
        # Fish on day 0 spawn again in SPAWN_NEXT days
        fish_count[SPAWN_NEXT] += new
        # Each fish is 1 day closer to spawning; Spawn new fish from fish on day 0
        fish_count = fish_count[1:] + [new]
    return fish_count


def main():
    args = parse_args()
    data = map(int, open(data_file_path_main(test=args.test)).read().strip().split(","))
    fish_count = parse_data(data, SPAWN_FIRST)
    log_always("Part 1:")
    fish_count = run_sim(fish_count, 80)
    log_always(sum(fish_count))
    log_always("Part 2:")
    fish_count = run_sim(fish_count, 256 - 80)
    log_always(sum(fish_count))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
