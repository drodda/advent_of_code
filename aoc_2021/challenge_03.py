#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def np_bin_array_to_int(array):
    """ Convert an array of boolean values or 1/0 integers to a decimal """
    return int("".join(map(str, array*1)), 2)


def most_common_bit(array):
    """ Calculate the most common bit in an array of booleans or 1/0 integers """
    return (array.sum() >= (array.size / 2)) * 1


def calculate_part_1(data_array):
    nbits = data_array.shape[1]
    # bits = most_common_bit(data_array)
    bits = np.array([most_common_bit(data_array[:, bit]) for bit in range(nbits)])
    val_gamma = np_bin_array_to_int(bits)
    val_epsilon = np_bin_array_to_int(bits == 0)
    return val_gamma * val_epsilon


def calculate_part_2_value(data_array, invert=False):
    nbits = data_array.shape[1]
    for bit in range(nbits):
        select_bit = most_common_bit(data_array[:, bit])
        if invert:
            select_bit = int(not select_bit)
        data_array = data_array[np.where(data_array[:, bit] == select_bit)]
        if data_array.shape[0] == 1:
            return np_bin_array_to_int(data_array[0])
    return None


def calculate_part_2(data_array):
    val_oxygen = calculate_part_2_value(data_array)
    val_co2 = calculate_part_2_value(data_array, invert=True)
    return val_oxygen * val_co2


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    data = [list(map(int, line)) for line in lines]
    data_array = np.array(data)
    log_always("Part 1:")
    log_always(calculate_part_1(data_array))
    log_always("Part 2:")
    log_always(calculate_part_2(data_array))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
