#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def group_by(x):
    """ Group an array into sequence of (value, len)
        Ref: https://stackoverflow.com/questions/39594631/grouping-continguous-values-in-a-numpy-array-with-their-length
    """
    idx = np.concatenate(([0], np.flatnonzero(x[:-1] != x[1:])+1, [x.size]))
    result = zip(x[idx[:-1]], np.diff(idx))
    return result


def permutations(n):
    """ Calculate the number of permutations for n bits which can have a gap of at most 2 off bits between on bits """
    if n < 1:
        return 1
    # Calculate the number of combinations for n bits where
    result = pow(2, n)
    # Subtract each combination of 3 or more in a row
    for x in range(0, n-2):
        result -= pow(2, x)
    return result


def main():
    args = parse_args()

    data_file = input_file_path_main(test=args.test)
    if args.test:
        data_file = input_file_path("test", "a")

    # Read data
    data_list = read_list_int(data_file, to_list=True)
    # Add start (0) and end (max+3)
    data_list.append(0)
    data_list.append(max(data_list) + 3)

    # Convert to numpy array and sort
    data_array = np.array(data_list)
    data_array.sort()

    # Calculate the difference between consecutive numbers
    data_diff = np.diff(data_array)
    log.debug(data_array)
    log.debug(data_diff)

    # Calculate the number of 1's and 3's
    count_1 = sum(data_diff == 1)
    count_3 = sum(data_diff == 3)
    part_1_result = count_1 * count_3

    log.always("Part 1")
    log.always(f"{count_1}, {count_3} = {part_1_result}")

    log.always("Part 2")
    # Group differences into sequence of (value, len)
    data_groups = group_by(data_diff)
    # Only values where value is 1 need to be considered
    data_groups = [(v, l) for v, l in data_groups if v == 1]

    # Calculate total number of permutations
    result = 1
    for v, l in data_groups:
        # Calculate permutations for each group
        log.verbose(f"{v} * {l} = {permutations(l-1)}")
        result *= permutations(l-1)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
