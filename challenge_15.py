#!/usr/bin/env python3

import traceback

from utils import *


LEN_PART1 = 2020
LEN_PART2 = 30000000


def elf_game(initial, max_len):
    # Strip head from initial data, as this will be the first element operated on
    *_initial, last = initial
    # Construct a dictionary of when each element in initial data was seen
    seen = {v: i for i, v in enumerate(_initial)}
    for i in range(len(_initial), max_len-1):
        # Calculate next element: Difference between when last was last seen and now, default to 0
        elem = i - seen.get(last, i)
        # Store last element as seen now
        seen[last] = i
        # Next element is now last element
        last = elem
    return last


def run_all_elf_games(data, max_len):
    def run_elf_game(_data):
        result = elf_game(_data, max_len)
        print(f"{_data} = {result}")

    # Run all test input
    for row in data:
        run_elf_game(row)


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    lines = read_lines(data_file)
    data = [list(map(int, line.split(","))) for line in lines]

    print("Part 1")
    run_all_elf_games(data, LEN_PART1)

    print("Part 2")
    run_all_elf_games(data, LEN_PART2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
