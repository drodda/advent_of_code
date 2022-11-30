#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


INPUT_TEST = "389125467"
INPUT_FULL = "135468729"

STEPS_PART1 = 100
STEPS_PART2 = 10000000
NCUPS_PART2 = 1000000


###############################################################################


def play(initial, ncups, rounds):
    ncups = max(ncups, len(initial))
    # Use a list of integers, the value is the node (index) that is next
    cups = [0] + [(i + 1) for i in range(1, ncups + 1)]

    first = initial[0]
    cur = first
    # Apply initial
    for cup in initial[1:]:
        cups[cur] = cup
        cur = cup
    if ncups > len(initial):
        # Patch last in initial to the first of the remainder
        cups[cur] = max(initial) + 1
        # Patch last to first to complete loop
        cups[-1] = first
    else:
        # Patch last to first to complete loop
        cups[cur] = first

    cur = first
    for r in range(rounds):
        # Find picked cups
        a = cups[cur]
        b = cups[a]
        c = cups[b]
        picked = (a, b, c)
        # Remove - link current to after picked (c)
        cups[cur] = cups[c]

        # Set destination, adjusting for removed cups
        dest = cur
        while True:
            dest = mod_natural(dest - 1, ncups)
            if dest not in picked:
                break

        # Insert picked cups after dest
        cups[c] = cups[dest]
        cups[dest] = a

        # Select next cup
        cur = cups[cur]

    return cups


def mod_natural(n, modulus):
    """ Calculate natural mod: between 1 and modulus """
    return ((n-1) % modulus) + 1


###############################################################################


def main():
    args = parse_args()
    input_str = INPUT_TEST if args.test else INPUT_FULL
    data = [int(c) for c in input_str]

    log.always("Part 1")
    cups = play(data, 0, STEPS_PART1)
    result = ''
    cup = cups[1]
    while cup != 1:
        result += str(cup)
        cup = cups[cup]
    log.always(f"{result}")

    log.always("Part 2")
    cups = play(data, NCUPS_PART2, STEPS_PART2)
    cup1 = cups[1]
    cup2 = cups[cup1]
    log.always(f"{cup1 * cup2}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
