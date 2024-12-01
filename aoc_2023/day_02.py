#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


COLOURS = ("red", "green", "blue")
TARGET_PART1 = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_input(line):
    vals = {colour: 0 for colour in COLOURS}
    game_str, turns = line.split(": ")
    game = int(game_str.split(" ")[1])
    for turn in turns.split("; "):
        for color_str in turn.split(", "):
            n, colour = color_str.split(" ")
            vals[colour] = max(vals[colour], int(n))
    return game, vals


def solve_part1(games):
    result = 0
    for game, vals in games:
        if all([vals[colour] <= TARGET_PART1[colour] for colour in COLOURS]):
            log.debug(f"Game {game} is possible")
            result += game
    return result


def solve_part2(games):
    result = 0
    for game, vals in games:
        game_result = 1
        for colour in COLOURS:
            game_result *= vals[colour]
        log.debug(f"Game {game} = {game_result}")
        result += game_result
    return result


def main():
    args = parse_args()
    lines = read_lines(args.input)
    games = [parse_input(line) for line in lines]

    log.always("Part 1:")
    result = solve_part1(games)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(games)
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
