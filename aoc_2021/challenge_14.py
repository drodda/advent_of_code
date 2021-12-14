#!/usr/bin/env python3

import os
import re
import sys
import traceback
from collections import Counter, defaultdict

from utils import *


def parse_replacement_str(replacement_str):
    groups = re.match(r"([a-zA-Z])([a-zA-Z]) -> ([a-zA-Z])", replacement_str).groups()
    return (groups[0], groups[1]), groups[2]


def step(polymer, replacements):
    """ Expand polymer. Return a polymer generator """
    polymer_iter = iter(polymer)
    a = next(polymer_iter)
    yield a
    for b in polymer_iter:
        yield replacements[(a, b)]
        yield b
        a = b


def simulate(polymer, replacements, n):
    """ Expand polymer n times """
    for i in range(n):
        polymer = step(polymer, replacements)
    return polymer


def simulate_part2(polymer, replacements, n):
    """ Run simulation in halves, return (most common count - least common count) """
    n1 = round(n/2)
    n2 = n - n1
    # Calculate the element counts for every element combination after n2 rounds
    element_pair_counts = {}
    for element_pair in replacements.keys():
        _polymer = simulate(element_pair, replacements, n2)
        counts = dict(Counter(_polymer))
        # Remove the original elements from the counts
        counts[element_pair[0]] -= 1
        counts[element_pair[1]] -= 1
        element_pair_counts[element_pair] = counts

    # Run simulation n1 times, look up counts from second half simulation
    counts = defaultdict(int)
    _polymer = simulate(polymer, replacements, n1)
    a = next(_polymer)
    counts[a] += 1
    for b in _polymer:
        for elem, count in element_pair_counts[(a, b)].items():
            counts[elem] += count
        counts[b] += 1
        a = b
    counts_sorted = sorted(counts.values(), reverse=True)
    return counts_sorted[0] - counts_sorted[-1]


def main():
    args = parse_args()
    (start_str, *_), replacements_str = read_multilines(data_file_path_main(test=args.test))
    replacements = dict([parse_replacement_str(line) for line in replacements_str])

    polymer = list(start_str)
    log_always("Part 1:")
    _polymer = simulate(polymer, replacements, 10)
    element_counts = Counter(_polymer).most_common()
    log_always(element_counts[0][1] - element_counts[-1][1])
    log_always("Part 2:")
    log_always(simulate_part2(polymer, replacements, 40))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
