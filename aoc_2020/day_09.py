#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def data_split(data, i, preamble_len):
    """ From data extract and return:
            preamble - preamble_len preceding element i
            value - element i
        Unsafe - does not check bounds
    """
    preamble = data[i - preamble_len:i]
    value = data[i]
    return preamble, value


def data_check(preamble, value):
    """ Check if value is the sum of preamble """
    for i, x in enumerate(preamble):
        for j, y in enumerate(preamble[i + 1:]):
            if x + y == value:
                log.verbose(f"Valid: {x} * {y} = {value}")
                return True
    return False


def data_find_invalid_sum(data, value):
    """ Find the sequence of values in data that add to value, or None """
    n = len(data)
    for i in range(n):
        for j in range(i+2, n):
            data_slice = data[i:j]
            s = sum(data_slice)
            if s > value:
                continue
            if s == value:
                log.debug(f"Invalid sum found: {i}-{j} = {data_slice}")
                return data_slice
    return None


def main():
    args = parse_args()
    data = list(read_list_int(input_file_path_main(test=args.test)))

    preamble_len = 5 if args.test else 25

    for i in range(preamble_len, len(data)):
        preamble, value = data_split(data, i, preamble_len)
        if not data_check(preamble, value):
            log.always("Part 1:")
            log.always(f"Invalid: {value}")
            log.always()
            log.always("Part 2")
            data_slice = data_find_invalid_sum(data, value)
            if data_slice:
                weakness = min(data_slice) + max(data_slice)
                log.always(f"Weakness: {weakness}")
                break
            else:
                log.always("No weakness found? Continuing...")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
