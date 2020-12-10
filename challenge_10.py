#!/usr/bin/env python3

import os
import sys
import traceback
import ipdb as pdb
import re
import json
import numpy as np
import string
import copy

from utils import *


def calculate_tribonacci(n, start=(0, 0, 1), trim=True):
    result = copy.copy(list(start))
    for i in range(n):
        result.append(sum(result[-3:]))
    if trim:
        result = result[len(start):]
    return result


def group_by(x):
    """ Group an array into sequence of (value, len)
        Ref: https://stackoverflow.com/questions/39594631/grouping-continguous-values-in-a-numpy-array-with-their-length
    """
    idx = np.concatenate(([0], np.flatnonzero(x[:-1] != x[1:])+1, [x.size]))
    result = zip(x[idx[:-1]], np.diff(idx))
    return result


def main():
    args = parse_args()

    data_file = data_file_path_main(test=args.test)
    if args.test:
        data_file = data_file_path("test", "a")

    data_list = read_list_int(data_file, degen=True)
    data_list.append(0)
    data_list.append(max(data_list) + 3)

    # Convert to numpy array and sort
    data_array = np.array(data_list)
    data_array.sort()

    # Calculate the difference between consecutive numbers
    data_diff = np.diff(data_array)
    print_debug(data_array)
    print_debug(data_diff)

    # Calculate the number of 1's and 3's
    count_1 = sum(data_diff == 1)
    count_3 = sum(data_diff == 3)
    part_1_result = count_1 * count_3

    print("Part 1")
    print(f"{count_1}, {count_3} = {part_1_result}")

    print("Part 2")
    # Group differences into sequence of (value, len)
    data_groups = list(group_by(data_diff))
    # Only values where value is 1 need to be considered
    data_groups = [(v, l) for v, l in data_groups if v == 1]
    max_len = max([l for _, l in data_groups])
    tribonacci = calculate_tribonacci(max_len)

    result = 1
    for v, l in data_groups:
        # Calculate permutations for each group
        print_verbose(f"{v} * {l} = {tribonacci[l-1]}")
        result *= tribonacci[l-1]
    print(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
