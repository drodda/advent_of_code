#!/usr/bin/env python3

import sys
import traceback
import numpy as np
import re

from common.utils import *

N_CARDS_TEST = 10
N_CARDS_1 = 10007
TARGET_1 = 2019
N_CARDS_2 = 119315717514047
TARGET_2 = 2020
REPEATS_2 = 101741582076661


RE_COMMAND = re.compile(r"^(?P<cmd>[\D]+?) ?(?P<val>-?[\d]*)$")


def parse_operations(lines):
    """ Split instruction into command and value """
    result = []
    for i, line in enumerate(lines):
        m = RE_COMMAND.match(line)
        cmd = m.group("cmd")
        val_str = m.group("val")
        val = int(val_str) if val_str else None
        result.append((i, cmd, val))
    return result


def deal_cut(deck, n):
    """ Simulate: apply cut operation to deck """
    return np.roll(deck, -n)


def deal_new_stack(deck):
    """ Simulate: apply new stack operation to deck """
    return np.flip(deck)


def deal_increment(deck, n):
    """ Simulate: apply increment operation to deck """
    result = np.zeros(deck.shape, dtype=int)
    for i, v in enumerate(deck):
        index = (i * n) % len(deck)
        result[index] = v
    return result


def np_index(arr, val):
    """ Find the first index of val in arr """
    index = np.where(arr == val)[0]
    if index.size:
        return index[0]
    return None


def simulate(operations, n_cards, target, verbose=False):
    """ Simulation solution - solve the slow way """
    deck = np.arange(n_cards)
    for i, cmd, val in operations:
        if cmd == "deal into new stack":
            deck = deal_new_stack(deck)
        elif cmd == "cut":
            deck = deal_cut(deck, val)
        elif cmd == "deal with increment":
            deck = deal_increment(deck, val)
        else:
            log.error(f"Invalid command: {cmd}")
            return None
        if verbose:
            log.debug(f"{i}: {cmd} {val}")
            log.debug(" ".join(map(str, deck.tolist())))
            log.debug("")
    result = np_index(deck, target)
    return result


def mod_inv(a, n):
    """ Fermat's little theorem to find modular inverse
        Solve for a*x mod n = 1
    """
    return pow(a, n-2, n)


def solve(operations, n_cards, target, iterations=1):
    """ Use maths to calculate the position of target card after applying operations to n_cards """
    # Calculate deck parameters after a single shuffle
    offset = 0  # Offset of 0 card
    increment = 1  # Spacing between cards
    for i, cmd, val in operations:
        if cmd == "deal into new stack":
            # Reverse deck: reverse increment
            increment *= -1
            offset += increment
        elif cmd == "cut":
            # Cut: shifts card forward.
            offset += increment * val
        elif cmd == "deal with increment":
            increment *= mod_inv(val, n_cards)
        else:
            log.error(f"Invalid command: {cmd}")
            return None
        offset %= n_cards
        increment %= n_cards

    # Apply multiple iterations
    offset = offset * (1 - pow(increment, iterations, n_cards)) * mod_inv((1 - increment) % n_cards, n_cards)
    offset %= n_cards
    increment = pow(increment, iterations, n_cards)

    # Find location of target card
    card = (offset + target * increment) % n_cards
    return card


def main():
    args = parse_args()
    verbose = (args.verbose >= 2)
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    operations = parse_operations(lines)

    log.always("Part 1:")
    n_cards = N_CARDS_TEST if args.test else N_CARDS_1
    result = simulate(operations, n_cards, TARGET_1, verbose=verbose)
    log.always(result)

    log.always("Part 2:")
    n_cards = N_CARDS_TEST if args.test else N_CARDS_2
    result = solve(operations, n_cards, TARGET_2, iterations=REPEATS_2)
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
