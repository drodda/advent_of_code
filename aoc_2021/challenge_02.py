#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def calculate_part_1(data):
    dist = 0
    depth = 0
    for direction, value in data:
        if direction == "forward":
            dist += value
        elif direction == "down":
            depth += value
        elif direction == "up":
            depth -= value
    log.info(f"Distance: {dist}, Depth: {depth}")
    return dist * depth


def calculate_part_2(data):
    dist = 0
    depth = 0
    aim = 0
    for direction, value in data:
        if direction == "forward":
            dist += value
            depth += aim * value
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value
    log.info(f"Distance: {dist}, Depth: {depth}")
    return dist * depth


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    data = [line.split() for line in lines]
    data = [(line[0], int(line[1])) for line in data]
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
