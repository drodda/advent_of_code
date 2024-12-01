#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


def parse(line):
    game_str, cards_str = line.split(": ", 1)
    game = int(game_str.split(" ", 1)[1])
    winning_cards_str, held_cards_str = cards_str.split(" | ")
    winning_cards = set(map(int, winning_cards_str.strip().replace("  ", " ").split(" ")))
    held_cards = set(map(int, held_cards_str.strip().replace("  ", " ").split(" ")))
    return game, winning_cards, held_cards


def solve_part1(lines):
    result = 0
    for line in lines:
        game, winning_cards, held_cards = parse(line)
        held_winning_cards = len(winning_cards.intersection(held_cards))
        if held_winning_cards > 0:
            score = pow(2, held_winning_cards - 1)
            result += score
    return result


def solve_part2(lines):
    result = 0
    card_extra_copies = collections.defaultdict(int)
    for line in lines:
        game, winning_cards, held_cards = parse(line)
        card_copies = 1 + card_extra_copies[game]
        result += card_copies
        held_winning_cards = len(winning_cards.intersection(held_cards))
        for _game in range(game + 1, game + held_winning_cards + 1):
            card_extra_copies[_game] += card_copies
    return result


def main():
    args = parse_args()
    lines = read_lines(args.input, to_list=True)

    log.always("Part 1:")
    result = solve_part1(lines)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(lines)
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
