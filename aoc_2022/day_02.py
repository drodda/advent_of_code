#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def calculate_round_part1(them, you):
    them_val = ord(them) - ord("A")
    you_val = ord(you) - ord("X")
    # Calculate result: 1 for win, 0 for draw, -1 for loss
    game_result = (you_val - them_val + 1) % 3 - 1
    result = (3 + 3 * game_result) + (you_val + 1)
    log.debug(f"{them}:{you} = {result}")
    return result


def calculate_round_part2(them, _result):
    them_val = ord(them) - ord("A")
    # Calculate result: 1 for win, 0 for draw, -1 for loss
    game_result = ord(_result) - ord("Y")
    # Calculate you_val to achieve game_result
    you_val = (them_val + game_result) % 3
    result = 3 + 3 * game_result + you_val + 1
    log.debug(f"{them}:{_result} = {result}")
    return result


def main():
    args = parse_args()
    data = [line.split() for line in read_lines(args.input)]

    log.always("Part 1:")
    result = sum([calculate_round_part1(them, you) for them, you in data])
    log.always(result)

    log.always("Part 2:")
    result = sum([calculate_round_part2(them, _result) for them, _result in data])
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
