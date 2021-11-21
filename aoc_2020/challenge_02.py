#!/usr/bin/env python3

import os
import sys
import traceback
import ipdb as pdb
import re

from utils import *


def parse_data_line(line):
    match = re.match(r"^(\d+)-(\d+) (.): (.+)$", line)
    if match.groups():
        x_str, y_str, ch, pw = match.groups()
        return int(x_str), int(y_str), ch, pw
    return None



def load_data(test):
    data_lines = read_lines(data_file_path_main(test=test))
    data = [parse_data_line(line) for line in data_lines]
    # Remove Nones
    data = [line for line in data if line is not None]
    return data


def xor(a, b):
    return (a or b) and not (a and b)


def main():
    args = parse_args()
    data = load_data(test=args.test)

    # log_always(data)
    log_always("Part 1:")
    valid = 0
    for line in data:
        n_min, n_max, ch, pw = line
        c = pw.count(ch)
        if n_min <= c <= n_max:
            valid += 1
        else:
            log_debug(f"PW does not match: {n_min}-{n_max} = {c} {ch}: {pw}")
    log_always(f"{valid} valid passwords")

    log_always("Part 2:")
    valid = 0
    for line in data:
        x, y, ch, pw = line
        if xor((pw[x-1] == ch), (pw[y-1] == ch)):
            valid += 1
        else:
            log_debug(f"PW does not match: {x}-{y} {ch}: {pw}")
    log_always(f"{valid} valid passwords")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
