#!/usr/bin/env python3

import sys
import traceback
from collections import defaultdict, Counter

from common.utils import *


BOARD_MAX = 10
DICE_DETERMINISTIC = 100
DICE_DIRAC = 3


def mod_natural(val, n):
    """ Natural mod: return a number between 1 and n inclusive """
    return (val - 1) % n + 1


def simulate_deterministic(pos_1, pos_2):
    rolls = 0
    dice = 1

    scores = [0, 0]
    positions = [pos_1, pos_2]
    player = 0

    while max(scores) < 1000:
        roll = dice + (dice + 1) + (dice + 2)
        # Dice value does not need to be mod'd as the maximum dice value is a multiple of board positions.
        dice += 3
        rolls += 3
        # Dice rollover is taken care of here
        positions[player] = mod_natural(positions[player] + roll, BOARD_MAX)
        scores[player] += positions[player]
        log.info(f"Player {player} rolled {roll}, board {positions} score {scores}")
        player = (player + 1) % len(positions)
    return scores[player] * rolls


def simulate_quantum(pos_1, pos_2):
    wins = [0, 0]
    # Calculate all possible dice values and their occurrence
    dice_values = list(Counter(
        i + j + k
        for i in range(1, DICE_DIRAC + 1)
        for j in range(1, DICE_DIRAC + 1)
        for k in range(1, DICE_DIRAC + 1)
    ).items())

    # Keep all possible outcomes of the game: ((scores), (positions), player): count of games with this outcome
    outcomes = {((0, 0), (pos_1, pos_2), 0): 1}
    while outcomes:
        outcomes_next = defaultdict(int)
        for (scores, positions, player), count in outcomes.items():
            next_player = (player + 1) % 2
            for roll, n in dice_values:
                _positions = list(positions)
                _scores = list(scores)
                _positions[player] = mod_natural(positions[player] + roll, BOARD_MAX)
                _scores[player] = scores[player] + _positions[player]
                if _scores[player] >= 21:
                    wins[player] += count * n
                else:
                    # Add next move to next outcomes
                    outcomes_next[(tuple(_scores), tuple(_positions), next_player)] += count * n
        outcomes = outcomes_next
    return max(wins)


def main():
    args = parse_args()
    data_raw = read_lines(data_file_path_main(test=args.test), to_list=True)
    pos_1 = int(data_raw[0].split(" ")[-1])
    pos_2 = int(data_raw[1].split(" ")[-1])

    log.always("Part 1:")
    result = simulate_deterministic(pos_1, pos_2)
    log.always(result)

    log.always("Part 2:")
    result = simulate_quantum(pos_1, pos_2)
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

