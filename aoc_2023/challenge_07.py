#!/usr/bin/env python3

import sys
import traceback
from functools import cache, cmp_to_key

from common.utils import *


WILDCARD = "_"  # Represents a wildcard: can assume any card, but has the lowest value
CARDS = "AKQJT98765432" + WILDCARD

CARD_SCORE = {
    card: len(CARDS) - i
    for i, card in enumerate(CARDS)
}

HAND_FORMATS = (
    (5, ),              # Five of a kind
    (4, 1),             # Four of a kind
    (3, 2),             # Full house
    (3, 1, 1),          # Three of a kind
    (2, 2, 1),          # Two pair
    (2, 1, 1, 1),       # One pair
    (1, 1, 1, 1, 1),    # High card
)


HAND_FORMAT_SCORES = {
    hand_format: len(HAND_FORMATS) - i
    for i, hand_format in enumerate(HAND_FORMATS)
}


def most_common(lst):
    return max(set(lst), key=lst.count)


@cache
def score_hand(hand):
    """
    Score a hand: return 7 for five-of-a-kind, 1 for high card
    """
    wildcard_count = hand.count(WILDCARD)
    # Remove wildcards
    hand = [card for card in hand if card != WILDCARD]
    most_common_card = max(set(hand), key=hand.count) if len(hand) else "A"
    # Replace wildcards with most common card
    hand += [most_common_card] * wildcard_count
    hand_format = tuple(list(sorted([hand.count(c) for c in set(hand)], reverse=True)))
    return HAND_FORMAT_SCORES[hand_format]


def compare_hands(hand1, hand2):
    """
    Compare 2 hands: return +ve if hand1 > hand2, -ve if hand1 < hand2, 0 if hand1 == hand2
    """
    result = score_hand(hand1) - score_hand(hand2)
    if result != 0:
        return result
    for i in range(len(hand1)):
        result = CARD_SCORE[hand1[i]] - CARD_SCORE[hand2[i]]
        if result != 0:
            return result
    return 0


def solve(data):
    sorted_hands = sorted(data.keys(), key=cmp_to_key(compare_hands), reverse=True)
    result = 0
    for i, hand in enumerate(sorted_hands):
        result += (len(data) - i) * data[hand]
    return result


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    data = {v[0]: int(v[1]) for v in [line.split() for line in lines]}
    log.info(data)

    log.always("Part 1:")
    result = solve(data)
    log.always(result)

    # Replace jokers with wildcards
    data = {
        hand.replace("J", "_"): bid
        for hand, bid in data.items()
    }

    log.always("Part 2:")
    result = solve(data)
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
