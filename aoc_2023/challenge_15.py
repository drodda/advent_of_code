#!/usr/bin/env python3

import collections
import re
import sys
import traceback
from common.utils import *


def compute_hash(_str, start=0):
    result = 0
    for c in _str:
        result = ((result + ord(c)) * 17) % 256
    return result


def solve_part1(data):
    result = 0
    for _str in data:
        _hash = compute_hash(_str)
        log.info(f"{_str} = {_hash}")
        result += _hash
    return result


def solve_part2(data):
    boxes = collections.defaultdict(collections.OrderedDict)
    for _str in data:
        label, operand, val = re.split("([=-])", _str)
        lens = int(val or "0")
        _hash = compute_hash(label)
        if operand == "=":
            boxes[_hash][label] = lens
        elif operand == "-":
            boxes[_hash].pop(label, None)
    result = 0
    for i, lenses in boxes.items():
        # log.info(f"{i} = {lenses}")
        for j, (label, lens) in enumerate(lenses.items()):
            log.info(f"{i:3d}\t{label:8s} {lens:3d} = {i + 1} * {j + 1} * {lens}")
            result += (i + 1) * (j + 1) * lens
    return result


def main():
    args = parse_args()
    with open(data_file_path_main(test=args.test)) as f:
        data = f.read().strip().split(",")

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
