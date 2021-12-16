#!/usr/bin/env python3

import sys
import traceback
from collections import defaultdict

from utils import *


def simulate(polymer, replacements, n):
    """ Expand polymer n times. Return the count of letters in the final polymer. Letter placement is lost """
    letter_count = defaultdict(int)
    for c in polymer:
        letter_count[c] += 1

    pairs_count = defaultdict(int)
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        pairs_count[pair] += 1

    for i in range(n):
        # Create a new pairs count, as all of the existing pairs will no longer be pairs after permuting
        _pairs_count = defaultdict(int)
        for pair, count in pairs_count.items():
            c = replacements[pair]
            # Add new letter to total letter count
            letter_count[c] += count
            # Add new pairs to new pairs_count
            _pairs_count[pair[0] + c] += count
            _pairs_count[c + pair[1]] += count
        pairs_count = _pairs_count
    return letter_count


def main():
    args = parse_args()
    (polymer, *_), replacements_str = read_multilines(data_file_path_main(test=args.test))
    replacements = dict([line.split(" -> ") for line in replacements_str])

    log_always("Part 1:")
    letter_count = simulate(polymer, replacements, 10)
    log_always(max(letter_count.values()) - min(letter_count.values()))
    log_always("Part 2:")
    letter_count = simulate(polymer, replacements, 40)
    log_always(max(letter_count.values()) - min(letter_count.values()))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
