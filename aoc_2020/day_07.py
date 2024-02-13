#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(filename):
    lines = read_lines(filename, strip_empty=True)
    bag_dict = {}
    for line in lines:
        bag_col, bag_contains = rtrim(line.replace("bags", "bag"), " bag.").split(" bag contain ", 1)
        bag_contents = bag_contains.split(" bag, ")

        bag_list = []
        if bag_contains == "no other":
            bag_dict[bag_col] = []
        else:
            for item in bag_contents:
                n, col = item.split(" ", 1)
                log.debug(f"  {n} = {col}")
                bag_list.append((int(n), col))
        bag_dict[bag_col] = bag_list
    return bag_dict


def bag_can_contain(bag_dict, bag_col, target="shiny gold"):
    for _, col in bag_dict[bag_col]:
        if col == target:
            return True
    for _, col in bag_dict[bag_col]:
        if bag_can_contain(bag_dict, col, target):
            return True
    return False


def bag_contents_count(bag_dict, bag_col):
    result = 0
    for n, col in bag_dict[bag_col]:
        # Increment count for bag
        result += n
        # Increment cout for contents of bag
        result += n * bag_contents_count(bag_dict, col)
    return result


def main():
    args = parse_args()
    bag_dict = parse_input(input_file_path_main(test=args.test))

    log.always("Part 1:")

    count = 0
    for col in bag_dict.keys():
        if bag_can_contain(bag_dict, col):
            log.debug(col)
            count += 1

    log.always(count)

    log.always("Part 2:")
    if args.test:
        bag_dict = parse_input(input_file_path("test", "b"))
    log.always(bag_contents_count(bag_dict, "shiny gold"))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
