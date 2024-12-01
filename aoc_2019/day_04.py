#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def to_digits(n, n_digits=0):
    """ Convert a number to a list of digits of at least length n_digits """
    return [int(x) for x in str(n).zfill(n_digits)]


def check_increasing(digits):
    """ Check that digits are increasing """
    return all([digits[i] <= digits[i+1] for i in range(len(digits) - 1)])


def check_repeat(digits):
    """ Check that digits contain at least one pair of repeated numbers """
    return any([digits[i] == digits[i + 1] for i in range(len(digits) - 1)])


def check_repeat_exactly_two(digits):
    """ Check that digits contain at least one pair of repeated numbers, with neighbours not the same """
    _digits = [None] + digits + [None]
    return any(
        [
            (_digits[i] == _digits[i + 1] and not _digits[i] == _digits[i - 1] and not _digits[i + 1] == _digits[i + 2])
            for i in range(1, len(digits))
        ]
    )


def find_valid_passwords(val_min, val_max, *criteria):
    """ Iterate over all possible passwords between val_min and val_max and return passwords that match all criteria """
    valid = []
    for val in range(val_min, val_max + 1):
        val_digits = to_digits(val, 6)
        if all([_criteria(val_digits) for _criteria in criteria]):
            log.verbose(f"Valid password: {val}")
            valid.append(valid)
    return valid


###############################################################################


def main():
    args = parse_args()
    data_file = args.input
    val_min, val_max = read_list_int(data_file)
    valid = find_valid_passwords(val_min, val_max, check_increasing, check_repeat)
    log.always("Part 1")
    log.always(len(valid))
    valid = find_valid_passwords(val_min, val_max, check_increasing, check_repeat_exactly_two)
    log.always("Part 2")
    log.always(len(valid))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
