#!/usr/bin/env python3

import traceback

from utils import *


LEN_PART1 = 2020
LEN_PART2 = 30000000


INPUT = [11, 0, 1, 10, 5, 19]
INPUT_TEST = [
    [0, 3, 6],
    [1, 3, 2],
    [2, 1, 3],
    [1, 2, 3],
    [2, 3, 1],
    [3, 2, 1],
    [3, 1, 2],
]


def elf_game(initial, max_len):
    # Strip head from initial data, as this will be the first element operated on
    *_initial, elem = initial
    # Construct a dictionary of when each element in initla data was seen
    seen = {v: i for i, v in enumerate(_initial)}
    for i in range(len(initial)-1, max_len-1):
        # Look up when elem was last seen, or default to now
        last_seen = seen.get(elem, i)
        # Store elem as seen now
        seen[elem] = i
        # Next element is time since last element was seen, or default to 0
        elem = i - last_seen
    return elem


def run_all_elf_games(max_len):
    def run_elf_game(_data, label):
        result = elf_game(_data, max_len)
        print(f"{label} {_data} = {result}")

    # Run all test input
    for data in INPUT_TEST:
        run_elf_game(data, "Test")
    # Run real input
    run_elf_game(INPUT, "Real")


def main():
    parse_args()

    print("Part 1")
    run_all_elf_games(LEN_PART1)

    print("Part 2")
    run_all_elf_games(LEN_PART2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
